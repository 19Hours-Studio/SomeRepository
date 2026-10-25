# Minimal exact Llama forward pass for SmolLM2-135M-Instruct (GGUF Q4_1, bundled in the PyPI wheel
# llm-smollm2==0.1.2, fetched by get_model.sh), with an explicit, editable KV cache so that a cached
# span can be deleted and the downstream keys RoPE-shifted (the "splice" of Idea 3).
# Weights are dequantized to float32 with the gguf package; nothing is downloaded from huggingface.
import numpy as np, torch, gguf
from tokenizers import Tokenizer, models, pre_tokenizers, decoders, AddedToken
torch.set_grad_enabled(False); torch.set_num_threads(int(__import__("os").environ.get("THREADS", 1)))

class Smol:
    def __init__(self, path):
        r = gguf.GGUFReader(path); f = {k: v.contents() for k, v in r.fields.items()
                                        if k.startswith(("llama.", "tokenizer.ggml.tokens", "tokenizer.ggml.merges"))}
        self.L = f["llama.block_count"]; self.d = f["llama.embedding_length"]
        self.nh = f["llama.attention.head_count"]; self.nkv = f["llama.attention.head_count_kv"]
        self.hd = self.d // self.nh; self.eps = f["llama.attention.layer_norm_rms_epsilon"]
        base = f["llama.rope.freq_base"]
        W = {}
        for t in r.tensors:
            a = gguf.quants.dequantize(t.data, t.tensor_type)
            W[t.name] = torch.from_numpy(np.ascontiguousarray(a, dtype=np.float32))
        self.W = W
        self.inv = 1.0 / (base ** (torch.arange(0, self.hd, 2, dtype=torch.float64) / self.hd))
        vocab = {s: i for i, s in enumerate(f["tokenizer.ggml.tokens"])}
        merges = [tuple(m.split(" ", 1)) for m in f["tokenizer.ggml.merges"]]
        tk = Tokenizer(models.BPE(vocab, merges))
        tk.pre_tokenizer = pre_tokenizers.Sequence([pre_tokenizers.Digits(individual_digits=True),
                                                     pre_tokenizers.ByteLevel(add_prefix_space=False, use_regex=True)])
        tk.decoder = decoders.ByteLevel()
        tk.add_special_tokens([AddedToken(s, special=True) for s in ("<|im_start|>", "<|im_end|>", "<|endoftext|>")])
        self.tk = tk

    def enc(self, s): return self.tk.encode(s).ids

    def rope(self, x, pos):  # x [T, H, hd]; GGML "normal" RoPE (adjacent pairs), as GGUF llama weights expect
        ang = pos.to(torch.float64)[:, None] * self.inv[None, :]
        c = torch.cos(ang).float()[:, None, :]; s = torch.sin(ang).float()[:, None, :]
        x0, x1 = x[..., 0::2], x[..., 1::2]
        out = torch.empty_like(x); out[..., 0::2] = x0 * c - x1 * s; out[..., 1::2] = x0 * s + x1 * c
        return out

    def rms(self, x, w): return x * torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + self.eps) * w

    def new_cache(self): return {"k": [None] * self.L, "v": [None] * self.L, "pos": torch.zeros(0, dtype=torch.long)}

    def forward(self, ids, cache, pos=None, want_logits=True, chunk=1024, last=None):
        """Append ids to cache (in place). pos: absolute positions (default: continue after max cached pos).
        Returns logits [len(ids), V] (float32) if want_logits; only for the last `last` tokens if given."""
        ids = torch.tensor(ids, dtype=torch.long)
        if pos is None:
            start = int(cache["pos"].max()) + 1 if len(cache["pos"]) else 0
            pos = torch.arange(start, start + len(ids))
        outs = []; n = len(ids); lf = 0 if last is None else n - last
        for a in range(0, n, chunk):
            o = self._fwd(ids[a:a + chunk], pos[a:a + chunk], cache, want_logits and a + chunk > lf)
            if want_logits and a + chunk > lf: outs.append(o[max(0, lf - a):])
        return torch.cat(outs) if want_logits else None

    def _fwd(self, ids, pos, cache, want_logits):
        W = self.W; T = len(ids); m = len(cache["pos"])
        x = W["token_embd.weight"][ids]
        # causal mask over cache entries + new tokens (cache order = sequence order)
        mask = torch.ones(T, m + T, dtype=torch.bool); mask[:, m:] = torch.tril(torch.ones(T, T, dtype=torch.bool))
        for l in range(self.L):
            p = f"blk.{l}."
            h = self.rms(x, W[p + "attn_norm.weight"])
            q = (h @ W[p + "attn_q.weight"].T).view(T, self.nh, self.hd)
            k = (h @ W[p + "attn_k.weight"].T).view(T, self.nkv, self.hd)
            v = (h @ W[p + "attn_v.weight"].T).view(T, self.nkv, self.hd)
            q = self.rope(q, pos); k = self.rope(k, pos)
            K = k if cache["k"][l] is None else torch.cat([cache["k"][l], k]); V = v if cache["v"][l] is None else torch.cat([cache["v"][l], v])
            cache["k"][l], cache["v"][l] = K, V
            rep = self.nh // self.nkv
            Kh = K.repeat_interleave(rep, 1).transpose(0, 1); Vh = V.repeat_interleave(rep, 1).transpose(0, 1)
            o = torch.nn.functional.scaled_dot_product_attention(q.transpose(0, 1), Kh, Vh, attn_mask=mask)
            x = x + o.transpose(0, 1).reshape(T, self.d) @ W[p + "attn_output.weight"].T
            h = self.rms(x, W[p + "ffn_norm.weight"])
            g = torch.nn.functional.silu(h @ W[p + "ffn_gate.weight"].T) * (h @ W[p + "ffn_up.weight"].T)
            x = x + g @ W[p + "ffn_down.weight"].T
        cache["pos"] = torch.cat([cache["pos"], pos])
        if not want_logits: return torch.zeros(0)
        return self.rms(x, W["output_norm.weight"]) @ W["token_embd.weight"].T

    def splice(self, cache, a, b, shift=True):
        """Delete cache entries [a, b) (sequence indices). If shift, RoPE-rotate all later keys by -(b-a)
        so positions stay contiguous (llama.cpp seq_rm + seq_add / Leyline); else leave a position gap."""
        n = b - a
        for l in range(self.L):
            K, V = cache["k"][l], cache["v"][l]
            tail = K[b:]
            if shift and len(tail):
                tail = self.rope(tail, torch.full((len(tail),), -n, dtype=torch.long))  # rotation composes
            cache["k"][l] = torch.cat([K[:a], tail]); cache["v"][l] = torch.cat([V[:a], V[b:]])
        P = cache["pos"]; tailp = P[b:] - (n if shift else 0)
        cache["pos"] = torch.cat([P[:a], tailp])

    def insert_at(self, cache, a, ids, shift=True):
        """Compute KV for ids placed at sequence index a, conditioned on cache[:a] only (exact for the
        placeholder, since its prefix is unchanged), and insert it there, shifting later keys by +len(ids).
        shift=False: the placeholder takes positions inside the gap left by an unshifted splice; later keys stay."""
        n = len(ids)
        pre = {"k": [k[:a] for k in cache["k"]], "v": [v[:a] for v in cache["v"]], "pos": cache["pos"][:a]}
        start = int(pre["pos"].max()) + 1 if a else 0
        self.forward(ids, pre, pos=torch.arange(start, start + n), want_logits=False)
        for l in range(self.L):
            tail = cache["k"][l][a:]
            if shift: tail = self.rope(tail, torch.full((len(tail),), n, dtype=torch.long))
            cache["k"][l] = torch.cat([pre["k"][l], tail]); cache["v"][l] = torch.cat([pre["v"][l], cache["v"][l][a:]])
        cache["pos"] = torch.cat([pre["pos"], cache["pos"][a:] + (n if shift else 0)])
