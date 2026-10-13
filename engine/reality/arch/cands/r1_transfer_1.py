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

class Deref(nn.Module):
    # Linked-list memory: cell s = (address e_s, pointer e_{s+1}). Reading = following the pointer; the result is
    # again a token embedding, so the SAME lookup can be applied again (pointer chasing).
    def __init__(self, d, dk=32, hops=2):
        super().__init__(); self.hops = hops; self.dk = dk
        self.q = nn.Linear(d, dk, bias=False); self.k = nn.Linear(d, dk, bias=False); self.ks = nn.Linear(d, dk, bias=False)
        self.pb = nn.Parameter(torch.zeros(hops, 2))
        self.w = nn.ModuleList([nn.Linear(d, d) for _ in range(hops)])
    def forward(self, e, pad):
        B, T, D = e.shape
        nxt = torch.cat([e[:, 1:], torch.zeros_like(e[:, :1])], 1)          # pointer stored in each cell
        r = torch.cat([torch.zeros_like(e[:, :1]), e[:, :-1]], 1)           # address register = previous token
        key = self.k(e) + self.ks(nxt)                                      # address (+ what it points to)
        par = torch.arange(T, device=e.device) % 2
        out = 0
        for i in range(self.hops):
            s = self.q(r) @ key.transpose(1, 2) / math.sqrt(self.dk) + self.pb[i][par][None, None, :]
            a = s.masked_fill(pad[:, None, :], -1e9).softmax(-1)
            r = a @ nxt                                                     # dereference: r <- *r
            out = out + self.w[i](r)
        return out

class Model(nn.Module):
    def __init__(self, vocab_size, max_len, d=64):
        super().__init__(); self.emb = nn.Embedding(vocab_size, d)
        self.blocks = nn.ModuleList([Block(d, 4) for _ in range(2)]); self.deref = Deref(d)
        self.n = nn.LayerNorm(d); self.out = nn.Linear(d, vocab_size)
    def forward(self, x):
        pad = x == 0; e = self.emb(x)
        h = self.blocks[0](e, pad)
        h = h + self.deref(e, pad)
        h = self.blocks[1](h, pad)
        return self.out(self.n(h))
