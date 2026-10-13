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
        a = a.masked_fill(pad[:, None, None, :], -1e9).softmax(-1)
        x = x + self.o((a @ v).transpose(1, 2).reshape(B, T, D))
        return x + self.ff(self.n2(x))

class Model(nn.Module):
    def __init__(self, vocab_size, max_len, d=64, k=8):
        super().__init__()
        self.emb = nn.Embedding(vocab_size, d)
        self.angle = nn.Embedding(vocab_size, k)          # per-token rotation angle for k phase channels
        nn.init.uniform_(self.angle.weight, -math.pi, math.pi)
        self.mix = nn.Linear(2 * k, d)
        self.blocks = nn.ModuleList([Block(d, 4) for _ in range(2)])
        self.n = nn.LayerNorm(d); self.out = nn.Linear(d, vocab_size)
    def forward(self, x):
        pad = x == 0
        a = self.angle(x).masked_fill(pad[..., None], 0.0)    # [B, T, k], padding does not rotate
        th = a.cumsum(1)                                       # running phase, magnitude exactly 1
        h = self.emb(x) + self.mix(torch.cat([th.cos(), th.sin()], -1))
        for b in self.blocks: h = b(h, pad)
        return self.out(self.n(h))
