# Minimal Qwen3 forward pass with an explicit, editable KV cache (keys stored post-RoPE).
# Lets us splice the cache (drop a span, insert a placeholder, re-rotate downstream keys)
# and compare against exact recomputation. Weights: Qwen3-0.6B safetensors (Docker Hub ai/qwen3:0.6b-safetensors).
import json, math, mmap, os, struct, torch

DIR = os.environ.get("QWEN_DIR", "/tmp/claude-0/w/qwen3")
DT = {"bf16": torch.bfloat16, "fp32": torch.float32}[os.environ.get("QWEN_DT", "bf16")]

class Qwen3:
    def __init__(self, d=DIR):
        c = json.load(open(f"{d}/config.json")); self.c = c
        self.w = {k.replace("model.", ""): v.to(DT) for k, v in self.load(f"{d}/model.safetensors").items()}
        self.L, self.H, self.KV, self.D = c["num_hidden_layers"], c["num_attention_heads"], c["num_key_value_heads"], c["head_dim"]
        self.eps = c["rms_norm_eps"]
        self.inv = 1.0 / (c["rope_theta"] ** (torch.arange(0, self.D, 2, dtype=torch.float64) / self.D))
        self.emb = self.w["embed_tokens.weight"]
        self.lm = self.w.get("lm_head.weight", self.emb)

    @staticmethod
    def load(path):  # safetensors via a private file mmap: weights stay file-backed (reclaimable), not anonymous memory
        f = open(path, "rb"); n = struct.unpack("<Q", f.read(8))[0]; hdr = json.loads(f.read(n))
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_COPY); out = {}
        for k, v in hdr.items():
            if k == "__metadata__": continue
            assert v["dtype"] == "BF16"; a, b = v["data_offsets"]
            out[k] = torch.frombuffer(mm, dtype=torch.bfloat16, count=(b - a) // 2, offset=8 + n + a).view(v["shape"])
        return out

    def rms(self, x, g): return x * torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + self.eps) * g

    def cs(self, pos):  # pos: 1-D int tensor (may be negative for shifts)
        f = pos.to(torch.float64)[:, None] * self.inv[None]
        e = torch.cat([f, f], -1)
        return e.cos().to(DT), e.sin().to(DT)

    @staticmethod
    def rot(x, cos, sin):  # x [..., T, D]
        h = x.shape[-1] // 2
        r = torch.cat([-x[..., h:], x[..., :h]], -1)
        return x * cos + r * sin

    def shift_keys(self, K, delta):  # re-rotate post-RoPE keys by a constant position delta
        cos, sin = self.cs(torch.tensor([delta]))
        return self.rot(K, cos, sin)

    @torch.no_grad()
    def forward(self, ids, cache=None, start=None, want_logits=True, keep=True):
        """ids: list[int]. cache: list of (K,V) per layer, each [KV, T, D]. New tokens are placed at
        positions start..start+n (default: right after cache). Returns (logits [n,V] or None, new cache)."""
        n = len(ids); T0 = 0 if cache is None else cache[0][0].shape[1]
        start = T0 if start is None else start
        pos = torch.arange(start, start + n)
        cos, sin = self.cs(pos)
        x = self.emb[torch.tensor(ids)]
        newc = []
        # causal mask: new token i sees all cache + new tokens <= i
        m = torch.full((n, T0 + n), 0.0, dtype=DT)
        m[:, T0:] = torch.triu(torch.full((n, n), float("-inf"), dtype=DT), 1)
        g = self.H // self.KV
        for l in range(self.L):
            p = f"layers.{l}."
            h = self.rms(x, self.w[p + "input_layernorm.weight"])
            q = (h @ self.w[p + "self_attn.q_proj.weight"].T).view(n, self.H, self.D).transpose(0, 1)
            k = (h @ self.w[p + "self_attn.k_proj.weight"].T).view(n, self.KV, self.D).transpose(0, 1)
            v = (h @ self.w[p + "self_attn.v_proj.weight"].T).view(n, self.KV, self.D).transpose(0, 1)
            q = self.rms(q, self.w[p + "self_attn.q_norm.weight"]); k = self.rms(k, self.w[p + "self_attn.k_norm.weight"])
            q = self.rot(q, cos, sin); k = self.rot(k, cos, sin)
            if cache is not None:
                K = torch.cat([cache[l][0], k], 1); V = torch.cat([cache[l][1], v], 1)
            else: K, V = k, v
            if keep == "new": newc.append((k, v))
            elif keep: newc.append((K, V))
            Kq = K.repeat_interleave(g, 0); Vq = V.repeat_interleave(g, 0)
            a = torch.nn.functional.scaled_dot_product_attention(q[None], Kq[None], Vq[None], attn_mask=m)[0]
            x = x + a.transpose(0, 1).reshape(n, -1) @ self.w[p + "self_attn.o_proj.weight"].T
            h = self.rms(x, self.w[p + "post_attention_layernorm.weight"])
            x = x + (torch.nn.functional.silu(h @ self.w[p + "mlp.gate_proj.weight"].T) * (h @ self.w[p + "mlp.up_proj.weight"].T)) @ self.w[p + "mlp.down_proj.weight"].T
        logits = self.rms(x, self.w["norm.weight"]) @ self.lm.T if want_logits else None
        return logits, (newc if keep else cache)
