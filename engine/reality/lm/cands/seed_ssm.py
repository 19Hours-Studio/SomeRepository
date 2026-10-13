# Seed (known family): minimal selective state-space / gated linear recurrence (Mamba-like), 2 layers, causal scan.
class Mixer(nn.Module):
    def __init__(self, d, e=2):
        super().__init__(); self.n = nn.LayerNorm(d); self.inp = nn.Linear(d, 2 * e * d); self.dt = nn.Linear(d, e * d)
        self.A = nn.Parameter(torch.rand(e * d) * 2 + 0.5); self.out = nn.Linear(e * d, d)
    def forward(self, x):
        u, z = self.inp(self.n(x)).chunk(2, -1); dt = F.softplus(self.dt(self.n(x)))
        a = torch.exp(-dt * self.A); h = torch.zeros_like(u[:, 0]); ys = []
        for t in range(x.shape[1]):
            h = a[:, t] * h + (1 - a[:, t]) * u[:, t]; ys.append(h)
        return x + self.out(torch.stack(ys, 1) * F.silu(z))

class Model(nn.Module):
    def __init__(self, vocab_size, max_len, d=72):
        super().__init__(); self.emb = nn.Embedding(vocab_size, d); self.layers = nn.ModuleList([Mixer(d) for _ in range(2)])
        self.n = nn.LayerNorm(d); self.out = nn.Linear(d, vocab_size)
    def forward(self, x):
        h = self.emb(x)
        for l in self.layers: h = l(h)
        return self.out(self.n(h))
