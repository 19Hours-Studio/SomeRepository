import torch, math
import torch.nn as nn
import torch.nn.functional as F

def turn(v, zr, zi):
    # rotate the complex pairs (v[:k], v[k:]) of v (..., 2k) by unit spins z = zr + i*zi (..., k)
    k = zr.shape[-1]; a, b = v[..., :k], v[..., k:]
    return torch.cat([a * zr - b * zi, a * zi + b * zr], -1)

class Spins(nn.Module):
    # z_t = exp(i*theta[x_t]) * normalize((1 - p[x_t]) * z_{t-1} + p[x_t]); |z| = 1 always, so no decay with length
    def __init__(self, vocab_size, K):
        super().__init__()
        rates = 0.04 * 80 ** (torch.arange(K) / (K - 1))
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
        return torch.stack(R, 1), torch.stack(I, 1)                       # B,T,K each

class Model(nn.Module):
    def __init__(self, vocab_size, max_len, d=64, K=16, dk=32, hops=2):
        super().__init__(); self.K, self.dk, self.hops = K, dk, hops
        self.emb = nn.Embedding(vocab_size, d); self.spins = Spins(vocab_size, K); self.read = nn.Linear(2 * K, d)
        self.q = nn.Linear(d, dk, bias=False); self.k = nn.Linear(d, dk, bias=False); self.ks = nn.Linear(d, dk, bias=False)
        self.qp = nn.Linear(d, hops * 2 * K)                                # per-hop phase query (what relative phase to seek)
        self.kp = nn.Parameter(0.5 * torch.randn(2 * K))                    # constant key, carried only by its spin
        self.w = nn.ModuleList([nn.Linear(d, d) for _ in range(hops)]); self.g = nn.Linear(d, hops)
        self.n = nn.LayerNorm(d); self.ff = nn.Sequential(nn.Linear(d, 4 * d), nn.GELU(), nn.Linear(4 * d, d))
        self.n2 = nn.LayerNorm(d); self.out = nn.Linear(d, vocab_size)
    def forward(self, x):
        B, T = x.shape; pad = x == 0
        e = self.emb(x); zr, zi = self.spins(x)
        h = e + self.read(torch.cat([zr, zi], -1))                         # spin readout: parity / task / counts
        nxt = torch.cat([e[:, 1:], torch.zeros_like(e[:, :1])], 1)          # pointer stored in each cell
        r = torch.cat([torch.zeros_like(e[:, :1]), e[:, :-1]], 1)           # register starts at the previous token
        key = self.k(e) + self.ks(nxt)                                      # content address (B,T,dk)
        krot = turn(self.kp.expand(B, T, 2 * self.K), zr, zi)               # phase address (B,T,2K)
        P = self.qp(h).view(B, T, self.hops, 2 * self.K)
        gate = torch.sigmoid(self.g(h))                                     # B,T,hops
        for i in range(self.hops):
            sp = turn(P[:, :, i], zr, zi) @ krot.transpose(1, 2)            # depends only on relative spin phase
            s = (self.q(r) @ key.transpose(1, 2) + sp) / math.sqrt(self.dk)
            a = s.masked_fill(pad[:, None, :], -1e9).softmax(-1)
            r = a @ nxt                                                     # dereference: r <- *r
            h = h + gate[..., i:i + 1] * self.w[i](r)
        h = h + self.ff(self.n(h))
        return self.out(self.n2(h))
