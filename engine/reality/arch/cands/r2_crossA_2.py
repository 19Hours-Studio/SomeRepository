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
    def __init__(self, vocab_size, max_len, d=64, k=8, dk=32, hops=2):
        super().__init__(); self.hops = hops; self.dk = dk
        self.emb = nn.Embedding(vocab_size, d)
        self.angle = nn.Embedding(vocab_size, k)
        nn.init.uniform_(self.angle.weight, -math.pi, math.pi)
        self.mix = nn.Linear(2 * k, d)
        self.q = nn.Linear(d, dk, bias=False); self.k = nn.Linear(d, dk, bias=False); self.ks = nn.Linear(d, dk, bias=False)
        self.pb = nn.Parameter(torch.zeros(hops, 2))
        self.w = nn.ModuleList([nn.Linear(d, d) for _ in range(hops)])
        self.block = Block(d, 4)
        self.n = nn.LayerNorm(d); self.out = nn.Linear(d, vocab_size)
    def forward(self, x):
        B, T = x.shape; pad = x == 0
        th = self.angle(x).masked_fill(pad[..., None], 0.0).cumsum(1)        # running phase, never decays
        e = self.emb(x) + self.mix(torch.cat([th.cos(), th.sin()], -1))      # one shared address space
        e = e.masked_fill(pad[..., None], 0.0)
        nxt = torch.cat([e[:, 1:], torch.zeros_like(e[:, :1])], 1)
        r = torch.cat([torch.zeros_like(e[:, :1]), e[:, :-1]], 1)
        key = self.k(e) + self.ks(nxt)
        par = torch.arange(T, device=x.device) % 2
        h = e
        for i in range(self.hops):
            s = self.q(r) @ key.transpose(1, 2) / math.sqrt(self.dk) + self.pb[i][par][None, None, :]
            r = s.masked_fill(pad[:, None, :], -1e9).softmax(-1) @ nxt
            h = h + self.w[i](r)
        h = self.block(h, pad)
        return self.out(self.n(h))
