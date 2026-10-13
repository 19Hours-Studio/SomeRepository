# Seed (known family): 2-layer pre-LN causal transformer, rotary positions (RoPE).
def rope(q, base=10000.0):
    B, H, T, D = q.shape; half = D // 2
    f = base ** (-torch.arange(half, device=q.device) / half); a = torch.arange(T, device=q.device)[:, None] * f[None]
    c, s = a.cos(), a.sin(); q1, q2 = q[..., :half], q[..., half:]
    return torch.cat([q1 * c - q2 * s, q1 * s + q2 * c], -1)

class Block(nn.Module):
    def __init__(self, d, h):
        super().__init__(); self.h = h; self.n1 = nn.LayerNorm(d); self.qkv = nn.Linear(d, 3 * d); self.o = nn.Linear(d, d)
        self.n2 = nn.LayerNorm(d); self.ff = nn.Sequential(nn.Linear(d, 3 * d), nn.GELU(), nn.Linear(3 * d, d))
    def forward(self, x, pad):
        B, T, D = x.shape; q, k, v = self.qkv(self.n1(x)).view(B, T, 3, self.h, D // self.h).permute(2, 0, 3, 1, 4)
        q, k = rope(q), rope(k); a = (q @ k.transpose(-1, -2)) / math.sqrt(D // self.h)
        a = a.masked_fill(torch.ones(T, T, dtype=torch.bool, device=x.device).triu(1), -1e9).softmax(-1)
        x = x + self.o((a @ v).transpose(1, 2).reshape(B, T, D))
        return x + self.ff(self.n2(x))

class _Base(nn.Module):
    def __init__(self, vocab_size, max_len, d=64):
        super().__init__(); self.emb = nn.Embedding(vocab_size, d)
        self.blocks = nn.ModuleList([Block(d, 4) for _ in range(2)]); self.n = nn.LayerNorm(d); self.out = nn.Linear(d, vocab_size)
    def forward(self, x):
        pad = x == 0; h = self.emb(x)
        for b in self.blocks: h = b(h, pad)
        return self.out(self.n(h))


class _Scale(nn.Module):
    def __init__(self, c): super().__init__(); self.c = c
    def forward(self, w): return w * self.c

class Model(_Base):
    # control: the seed RoPE transformer with the researcher's 3x effective step size (W = 3 * W'), nothing else changed
    def __init__(self, vocab_size, max_len):
        super().__init__(vocab_size, max_len)
        import torch.nn.utils.parametrize as P
        for m in list(self.modules()):
            for name, p in list(m._parameters.items()):
                if p is None: continue
                P.register_parametrization(m, name, _Scale(3.0)); getattr(m.parametrizations, name).original.data.div_(3.0)
