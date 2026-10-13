def turn(q, zr, zi):
    # rotate q (B,H,T,D) by complex spin z = zr + i*zi (B,H,T,D/2); q.k then depends on the relative spin phase
    h = q.shape[-1] // 2; q1, q2 = q[..., :h], q[..., h:]
    return torch.cat([q1 * zr - q2 * zi, q1 * zi + q2 * zr], -1)

class Spins(nn.Module):
    # per token: precession angle theta and keep-gate g; z_t = exp(i*theta_t) * (g_t * z_{t-1} + (1 - g_t))
    def __init__(self, vocab_size, heads, k):
        super().__init__()
        w = (0.04 * 80 ** (torch.arange(k) / (k - 1))).repeat(heads)       # rates 0.04 .. 3.2 rad per token, per head
        self.theta = nn.Parameter(w[None].repeat(vocab_size, 1) + 0.01 * torch.randn(vocab_size, heads * k))
        self.keep = nn.Parameter(2.0 + 2.0 * torch.randn(vocab_size, heads * k))
    def forward(self, x):
        th = self.theta[x]; g = torch.sigmoid(self.keep[x]); c, s = th.cos(), th.sin()
        zr = torch.ones_like(th[:, 0]); zi = torch.zeros_like(zr); R, I = [], []
        for t in range(x.shape[1]):
            ar = g[:, t] * zr + 1 - g[:, t]; ai = g[:, t] * zi
            zr = ar * c[:, t] - ai * s[:, t]; zi = ar * s[:, t] + ai * c[:, t]
            R.append(zr); I.append(zi)
        return torch.stack(R, 1), torch.stack(I, 1)

class Block(nn.Module):
    def __init__(self, d, h):
        super().__init__(); self.h = h; self.n1 = nn.LayerNorm(d); self.qkv = nn.Linear(d, 3 * d); self.o = nn.Linear(d, d)
        self.n2 = nn.LayerNorm(d); self.ff = nn.Sequential(nn.Linear(d, 3 * d), nn.GELU(), nn.Linear(3 * d, d))
    def forward(self, x, pad, zr, zi):
        B, T, D = x.shape; q, k, v = self.qkv(self.n1(x)).view(B, T, 3, self.h, D // self.h).permute(2, 0, 3, 1, 4)
        q, k = turn(q, zr, zi), turn(k, zr, zi); a = (q @ k.transpose(-1, -2)) / math.sqrt(D // self.h)
        a = a.masked_fill(pad[:, None, None, :], -1e9).softmax(-1)
        x = x + self.o((a @ v).transpose(1, 2).reshape(B, T, D))
        return x + self.ff(self.n2(x))

class Model(nn.Module):
    def __init__(self, vocab_size, max_len, d=64, H=4):
        super().__init__(); self.H = H; self.emb = nn.Embedding(vocab_size, d)
        self.spins = Spins(vocab_size, H, d // H // 2); self.read = nn.Linear(d, d)
        self.blocks = nn.ModuleList([Block(d, H) for _ in range(2)]); self.n = nn.LayerNorm(d); self.out = nn.Linear(d, vocab_size)
    def forward(self, x):
        B, T = x.shape; pad = x == 0
        zr, zi = self.spins(x)                                              # B,T,d/2 each
        h = self.emb(x) + self.read(torch.cat([zr, zi], -1))                # spin readout (parity = sign of a spin)
        zr = zr.view(B, T, self.H, -1).transpose(1, 2); zi = zi.view(B, T, self.H, -1).transpose(1, 2)
        for b in self.blocks: h = b(h, pad, zr, zi)
        return self.out(self.n(h))
