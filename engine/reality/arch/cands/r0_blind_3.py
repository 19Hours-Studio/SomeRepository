import math
import torch
import torch.nn as nn
import torch.nn.functional as F

PERIODS = (2.0, 3.0, 5.0, 7.0)


def rotate(v, cos, sin):
    R = cos.shape[-1]
    v1, v2, rest = v[..., :R], v[..., R:2 * R], v[..., 2 * R:]
    return torch.cat([v1 * cos - v2 * sin, v1 * sin + v2 * cos, rest], dim=-1)


class Block(nn.Module):
    def __init__(self, d, n_heads):
        super().__init__()
        self.h, self.dh = n_heads, d // n_heads
        self.ln1 = nn.LayerNorm(d)
        self.qkv = nn.Linear(d, 3 * d)
        self.o = nn.Linear(d, d)
        self.ln2 = nn.LayerNorm(d)
        self.mlp = nn.Sequential(nn.Linear(d, 2 * d), nn.GELU(), nn.Linear(2 * d, d))

    def forward(self, h, cos, sin, mask):
        B, T, D = h.shape
        q, k, v = self.qkv(self.ln1(h)).view(B, T, 3, self.h, self.dh).permute(2, 0, 3, 1, 4)
        q, k = rotate(q, cos, sin), rotate(k, cos, sin)
        att = (q @ k.transpose(-1, -2)) / math.sqrt(self.dh)
        att = att.masked_fill(~mask, float('-inf')).softmax(-1)
        y = (att @ v).transpose(1, 2).reshape(B, T, D)
        h = h + self.o(y)
        return h + self.mlp(self.ln2(h))


class Model(nn.Module):
    def __init__(self, vocab_size, max_len, d=64, n_heads=4, n_layers=3, n_par=8):
        super().__init__()
        self.R = len(PERIODS)
        V = vocab_size
        self.emb = nn.Embedding(V, d)
        self.prev = nn.Embedding(V, d)
        # gate logits: attention clocks start as near-absolute counters with some random resets;
        # parity counters start with almost no resets and random increments
        self.reset_logit = nn.Parameter(torch.cat([0.7 * torch.randn(V, self.R) - 0.5,
                                                   0.5 * torch.randn(V, n_par) - 1.5], dim=1))
        self.inc_logit = nn.Parameter(torch.cat([0.5 * torch.randn(V, self.R) + 1.0,
                                                 torch.randn(V, n_par)], dim=1))
        self.sharp = 4.0
        freqs = [2 * math.pi / p for p in PERIODS] + [math.pi] * n_par
        self.register_buffer('freqs', torch.tensor(freqs))
        self.par_proj = nn.Linear(2 * n_par, d)
        self.blocks = nn.ModuleList([Block(d, n_heads) for _ in range(n_layers)])
        self.ln = nn.LayerNorm(d)
        self.out = nn.Linear(d, V)

    def clocks(self, x):
        keep = 1.0 - torch.sigmoid(self.sharp * self.reset_logit[x])   # [B,T,C]
        inc = torch.sigmoid(self.sharp * self.inc_logit[x])
        n = torch.zeros_like(inc[:, 0])
        out = []
        for t in range(x.shape[1]):
            n = keep[:, t] * n + inc[:, t]
            out.append(n)
        return torch.stack(out, dim=1)                                   # [B,T,C]

    def forward(self, x):
        B, T = x.shape
        xp = F.pad(x, (1, 0))[:, :T]
        h = self.emb(x) + self.prev(xp)
        ang = self.clocks(x) * self.freqs                                # [B,T,C]
        a_att, a_par = ang[..., :self.R], ang[..., self.R:]
        h = h + self.par_proj(torch.cat([a_par.cos(), a_par.sin()], dim=-1))
        cos, sin = a_att.cos().unsqueeze(1), a_att.sin().unsqueeze(1)    # [B,1,T,R]
        causal = torch.ones(T, T, dtype=torch.bool, device=x.device).tril()
        mask = causal.unsqueeze(0).unsqueeze(0) & (x != 0)[:, None, None, :]
        for blk in self.blocks:
            h = blk(h, cos, sin, mask)
        return self.out(self.ln(h))
