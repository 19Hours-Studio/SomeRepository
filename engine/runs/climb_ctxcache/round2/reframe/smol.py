"""Minimal Llama forward pass for SmolLM2-135M-Instruct (GGUF from the PyPI wheel
`llm-smollm2`), with an explicit, editable KV cache.

The KV cache is a per-layer tensor of *post-RoPE* keys and values plus the
integer position each entry was encoded at.  That lets us delete spans, keep
position gaps, re-rotate keys to new positions, and recompute chosen tokens --
the operations a splicing serving stack would perform.
"""
import sys, os, torch, numpy as np
import gguf
from gguf.quants import dequantize
from tokenizers import Tokenizer, models, pre_tokenizers, decoders

HERE = os.path.dirname(os.path.abspath(__file__))
GGUF = os.path.join(HERE, "dl/x/llm_smollm2/SmolLM2-135M-Instruct.Q4_1.gguf")
torch.set_grad_enabled(False)
torch.set_flush_denormal(True)
torch.set_num_threads(int(os.environ.get("THREADS", 1)))  # multi-threading is contended on this VM


def _field(r, k):
    return r.fields[k].contents()


class Smol:
    def __init__(self, path=GGUF, dtype=torch.float32):
        r = gguf.GGUFReader(path)
        cp = path + ".dequant.pt"
        self.L = _field(r, "llama.block_count")
        self.d = _field(r, "llama.embedding_length")
        self.nh = _field(r, "llama.attention.head_count")
        self.nkv = _field(r, "llama.attention.head_count_kv")
        self.hd = self.d // self.nh
        self.theta = _field(r, "llama.rope.freq_base")
        self.eps = _field(r, "llama.attention.layer_norm_rms_epsilon")
        if os.path.exists(cp):
            W = torch.load(cp)
        else:
            W = {}
            for t in r.tensors:
                a = dequantize(t.data, t.tensor_type)
                a = np.asarray(a, dtype=np.float32).reshape(list(reversed(t.shape.tolist())))
                W[t.name] = torch.from_numpy(a.copy()).to(dtype)
            torch.save(W, cp)
        self.W = W
        self.emb = W["token_embd.weight"]  # [vocab, d]
        self.out = W.get("output.weight", self.emb)
        inv = 1.0 / (self.theta ** (torch.arange(0, self.hd, 2, dtype=torch.float64) / self.hd))
        self.inv = inv
        # tokenizer from GGUF vocab + merges (GPT-2 byte-level BPE, digits split)
        toks = _field(r, "tokenizer.ggml.tokens")
        merges = [tuple(m.split(" ", 1)) for m in _field(r, "tokenizer.ggml.merges")]
        vocab = {t: i for i, t in enumerate(toks)}
        tk = Tokenizer(models.BPE(vocab=vocab, merges=merges))
        tk.pre_tokenizer = pre_tokenizers.Sequence([
            pre_tokenizers.Digits(individual_digits=True),
            pre_tokenizers.ByteLevel(add_prefix_space=False, use_regex=True)])
        tk.decoder = decoders.ByteLevel()
        specials = [t for t in toks if t.startswith("<|") and t.endswith("|>")]
        tk.add_special_tokens(specials)
        self.tok = tk
        self.vocab = vocab

    # ---- tokenizer -----------------------------------------------------
    def enc(self, s):
        return self.tok.encode(s, add_special_tokens=False).ids

    def dec(self, ids):
        return self.tok.decode(ids)

    # ---- RoPE (GGUF llama weights use adjacent-pair rotation) -------------
    def _cs(self, pos):
        ang = pos.to(torch.float64)[:, None] * self.inv[None, :]
        return torch.cos(ang).float(), torch.sin(ang).float()

    def rope(self, x, pos, cs=None):
        # x: [T, H, hd]; pos: [T] integer positions, any order
        c, s = self._cs(pos) if cs is None else cs
        c = c[:, None, :]; s = s[:, None, :]
        x1 = x[..., 0::2]; x2 = x[..., 1::2]
        o = torch.empty_like(x)
        o[..., 0::2] = x1 * c - x2 * s
        o[..., 1::2] = x1 * s + x2 * c
        return o

    def rerotate(self, k, dpos):
        """Rotate post-RoPE keys k [T,H,hd] by a per-token position delta."""
        return self.rope(k, dpos)

    def _norm(self, x, w):
        return x * torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + self.eps) * w

    # ---- forward ------------------------------------------------------
    def empty_cache(self):
        return {"k": [torch.zeros(0, self.nkv, self.hd) for _ in range(self.L)],
                "v": [torch.zeros(0, self.nkv, self.hd) for _ in range(self.L)],
                "pos": torch.zeros(0, dtype=torch.long)}

    def forward(self, ids, pos, cache=None, return_logits=True, chunk=1024):
        """Run tokens `ids` at positions `pos`, attending to everything in
        `cache` plus causally to themselves.  Returns (logits, new_cache) where
        new_cache = cache + these tokens.  Processes in chunks to bound memory."""
        if cache is None:
            cache = self.empty_cache()
        ids = torch.as_tensor(ids, dtype=torch.long)
        pos = torch.as_tensor(pos, dtype=torch.long)
        outs = []
        for s in range(0, len(ids), chunk):
            lo, c = self._fwd(ids[s:s + chunk], pos[s:s + chunk], cache, return_logits)
            cache = c
            if return_logits:
                outs.append(lo)
        return (torch.cat(outs) if return_logits else None), cache

    def _fwd(self, ids, pos, cache, return_logits):
        W = self.W; T = len(ids); g = self.nh // self.nkv
        x = self.emb[ids]
        nk, nv = [], []
        P = cache["k"][0].shape[0]
        mask = torch.ones(T, P + T, dtype=torch.bool)
        mask[:, P:] = torch.tril(torch.ones(T, T, dtype=torch.bool))
        cs = self._cs(pos)
        for l in range(self.L):
            p = f"blk.{l}."
            h = self._norm(x, W[p + "attn_norm.weight"])
            q = (h @ W[p + "attn_q.weight"].T).view(T, self.nh, self.hd)
            k = (h @ W[p + "attn_k.weight"].T).view(T, self.nkv, self.hd)
            v = (h @ W[p + "attn_v.weight"].T).view(T, self.nkv, self.hd)
            q = self.rope(q, pos, cs); k = self.rope(k, pos, cs)
            K = torch.cat([cache["k"][l], k]); V = torch.cat([cache["v"][l], v])
            nk.append(K); nv.append(V)
            Kx = K.repeat_interleave(g, dim=1); Vx = V.repeat_interleave(g, dim=1)
            a = torch.nn.functional.scaled_dot_product_attention(
                q.transpose(0, 1), Kx.transpose(0, 1), Vx.transpose(0, 1),
                attn_mask=mask[None])
            a = a.transpose(0, 1).reshape(T, self.d)
            x = x + a @ W[p + "attn_output.weight"].T
            h = self._norm(x, W[p + "ffn_norm.weight"])
            f = torch.nn.functional.silu(h @ W[p + "ffn_gate.weight"].T) * (h @ W[p + "ffn_up.weight"].T)
            x = x + f @ W[p + "ffn_down.weight"].T
        newc = {"k": nk, "v": nv, "pos": torch.cat([cache["pos"], pos])}
        lo = None
        if return_logits:
            lo = self._norm(x, W["output_norm.weight"]) @ self.out.T
        return lo, newc


def cache_select(c, idx):
    idx = torch.as_tensor(idx, dtype=torch.long)
    return {"k": [k[idx] for k in c["k"]], "v": [v[idx] for v in c["v"]], "pos": c["pos"][idx]}


def cache_cat(a, b):
    return {"k": [torch.cat([x, y]) for x, y in zip(a["k"], b["k"])],
            "v": [torch.cat([x, y]) for x, y in zip(a["v"], b["v"])],
            "pos": torch.cat([a["pos"], b["pos"]])}


if __name__ == "__main__":
    m = Smol()
    prompt = ("<|im_start|>system\nYou are a helpful AI assistant named SmolLM, trained by Hugging Face<|im_end|>\n"
              "<|im_start|>user\nWhat is the capital of France? Answer in one sentence.<|im_end|>\n<|im_start|>assistant\n")
    ids = m.enc(prompt)
    print("ntok", len(ids))
    lo, c = m.forward(ids, range(len(ids)))
    out = []
    nxt = int(lo[-1].argmax())
    for i in range(30):
        out.append(nxt)
        if nxt == m.vocab["<|im_end|>"]:
            break
        lo, c = m.forward([nxt], [len(ids) + i], c)
        nxt = int(lo[-1].argmax())
    print(repr(m.dec(out)))
    # consistency: incremental vs full
    full, _ = m.forward(ids + out, range(len(ids) + len(out)))
    print("max |full-incr| logit diff:", float((full[-2] - lo[-1]).abs().max()))
