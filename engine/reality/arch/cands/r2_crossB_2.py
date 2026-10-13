import torch, math
import torch.nn as nn
import torch.nn.functional as F

def turn(v, zr, zi):
    k = zr.shape[-1]; a, b = v[..., :k], v[..., k:]
    return torch.cat([a * zr - b * zi, a * zi + b * zr], -1)

class Spins(nn.Module):
    # unit-size token-driven spins; first half of the channels start at rate 0 (pure content), second half spread 0.04..3.2
    def __init__(self, vocab_size, K):
        super().__init__(); h = K // 2
        rates = torch.cat([torch.zeros(K - h), 0.04 * 80 ** (torch.arange(h) / max(h - 1, 1))])
        self.theta = nn.Parameter(rates[None].repeat(vocab_size, 1) + 0.01 * torch.randn(vocab_size, K))
        self.reset = nn.Parameter(-2.0 + 2.0 * torch.randn(vocab_size, K))
    def forward(self, x):
        th = self.theta[x]; p = torch.sigmoid(self.reset[x]); c, s = th.cos(), th.sin()
        zr = torch.ones_like(th[:, 0]); zi = torch.zeros_like(zr); R, I = [], []
        for t in range(x.shape[1]):
            ar = (1 - p[:, t]) * zr + p[:, t]; ai = (1 - p[:, t]) * zi
            m = torch.rsqrt(ar * ar + ai * ai + 1e-3); ar, ai = ar * m, ai * m
            zr = ar * c[:, t] - ai * s[:, t]; zi = ar * s[:, t] + ai * c[:, t]
            R.append(zr); I.append(zi)
        return torch.stack(R, 1), torch.stack(I, 1)

class Model(nn.Module):
    def __init__(self, vocab_size, max_len, d=64, K=24, hops=3):
        super().__init__(); self.K, self.hops = K, hops
        self.emb = nn.Embedding(vocab_size, d); self.spins = Spins(vocab_size, K); self.read = nn.Linear(2 * K, d)
        self.q = nn.Linear(d, 2 * K); self.k = nn.Linear(d, 2 * K); self.ks = nn.Linear(d, 2 * K, bias=False)
        self.sel = nn.Linear(d, hops + 1); self.w = nn.Linear(d, d)          # how many hops to take; one tied readout
        self.n = nn.LayerNorm(d); self.ff = nn.Sequential(nn.Linear(d, 4 * d), nn.GELU(), nn.Linear(4 * d, d))
        self.n2 = nn.LayerNorm(d); self.out = nn.Linear(d, vocab_size)
    def forward(self, x):
        B, T = x.shape; pad = x == 0
        e = self.emb(x); zr, zi = self.spins(x)
        h = e + self.read(torch.cat([zr, zi], -1))
        nxt = torch.cat([e[:, 1:], torch.zeros_like(e[:, :1])], 1)
        r = torch.cat([torch.zeros_like(e[:, :1]), e[:, :-1]], 1)
        key = turn(self.k(e) + self.ks(nxt), zr, zi)                        # address = (token, successor) x spin
        mix = self.sel(h).softmax(-1)                                       # B,T,hops+1 (index 0 = no lookup)
        sc = 1.0 / math.sqrt(2 * self.K); acc = 0
        for i in range(self.hops):
            s = (turn(self.q(r), zr, zi) @ key.transpose(1, 2)) * sc        # same lookup every hop
            a = s.masked_fill(pad[:, None, :], -1e9).softmax(-1)
            r = a @ nxt                                                     # r <- *r
            acc = acc + mix[..., i + 1:i + 2] * r
        h = h + self.w(acc)
        h = h + self.ff(self.n(h))
        return self.out(self.n2(h))
