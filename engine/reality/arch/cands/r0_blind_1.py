import math
import torch
import torch.nn as nn
import torch.nn.functional as F

PERIODS = (2.0, 3.0, 5.0, 7.0)  # lcm 210 > 72, so delta = 0 is the unique full-phase match


def seg_index(x):
    # number of steps since the last delimiter (separator 1 or task markers 3..6)
    B, T = x.shape
    delim = (x == 1) | ((x >= 3) & (x <= 6))
    pos = torch.arange(T, device=x.device).unsqueeze(0).expand(B, T)
    last = torch.cummax(torch.where(delim, pos, torch.zeros_like(pos)), dim=1).values
    return (pos - last).float()


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
        q, k = rotate(q, cos, sin), rotate(k, cos, sin)          # [B,H,T,dh]
        att = (q @ k.transpose(-1, -2)) / math.sqrt(self.dh)
        att = att.masked_fill(~mask, float('-inf')).softmax(-1)
        y = (att @ v).transpose(1, 2).reshape(B, T, D)
        h = h + self.o(y)
        return h + self.mlp(self.ln2(h))


class Model(nn.Module):
    def __init__(self, vocab_size, max_len, d=64, n_heads=4, n_layers=3, n_phase=16):
        super().__init__()
        self.emb = nn.Embedding(vocab_size, d)
        self.prev = nn.Embedding(vocab_size, d)                   # token shift: previous token
        self.phase_logit = nn.Parameter(0.5 * torch.randn(vocab_size, n_phase))
        self.phase_proj = nn.Linear(2 * n_phase, d)
        self.blocks = nn.ModuleList([Block(d, n_heads) for _ in range(n_layers)])
        self.ln = nn.LayerNorm(d)
        self.out = nn.Linear(d, vocab_size)
        self.register_buffer('freqs', torch.tensor([2 * math.pi / p for p in PERIODS]))

    def forward(self, x):
        B, T = x.shape
        xp = F.pad(x, (1, 0))[:, :T]
        h = self.emb(x) + self.prev(xp)
        # parity channel: per-token phase saturating to {0, pi}, accumulated
        theta = math.pi * torch.sigmoid(6.0 * self.phase_logit[x])  # [B,T,P]
        phi = torch.cumsum(theta, dim=1)
        h = h + self.phase_proj(torch.cat([phi.cos(), phi.sin()], dim=-1))
        # delimiter-relative rotary angles
        ang = seg_index(x).unsqueeze(-1) * self.freqs              # [B,T,R]
        cos, sin = ang.cos().unsqueeze(1), ang.sin().unsqueeze(1)  # [B,1,T,R]
        causal = torch.ones(T, T, dtype=torch.bool, device=x.device).tril()
        mask = causal.unsqueeze(0).unsqueeze(0) & (x != 0)[:, None, None, :]
        for blk in self.blocks:
            h = blk(h, cos, sin, mask)
        return self.out(self.ln(h))
