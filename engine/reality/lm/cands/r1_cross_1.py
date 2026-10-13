import math
import torch
import torch.nn as nn
import torch.nn.functional as F


def _rot(x, cos, sin):
    # rotate the first 2*f dims of each head, leave the rest position-free (pure content matching)
    f = cos.shape[-1]
    x1, x2, xp = x[..., :f], x[..., f:2 * f], x[..., 2 * f:]
    return torch.cat([x1 * cos - x2 * sin, x1 * sin + x2 * cos, xp], dim=-1)


class ColShiftAttention(nn.Module):
    def __init__(self, d, H):
        super().__init__()
        self.H, self.hd = H, d // H
        self.q = nn.Linear(d, d, bias=False)
        self.k = nn.Linear(d, d, bias=False)
        self.v = nn.Linear(d, d, bias=False)
        self.o = nn.Linear(d, d, bias=False)
        self.k0 = nn.Parameter(torch.randn(1, 1, d) * 0.02)  # stands in for h[-1]

    def forward(self, h, cq, sq, ck, sk):
        B, T, d = h.shape
        hk = torch.cat([self.k0.expand(B, 1, d), h[:, :-1]], dim=1)  # key at s built from h[s-1]
        q = self.q(h).view(B, T, self.H, self.hd).transpose(1, 2)
        k = self.k(hk).view(B, T, self.H, self.hd).transpose(1, 2)
        v = self.v(h).view(B, T, self.H, self.hd).transpose(1, 2)
        q = _rot(q, cq, sq)
        k = _rot(k, ck, sk)
        y = F.scaled_dot_product_attention(q, k, v, is_causal=True)
        return self.o(y.transpose(1, 2).reshape(B, T, d))


class Block(nn.Module):
    def __init__(self, d, H, ff):
        super().__init__()
        self.n1 = nn.LayerNorm(d)
        self.att = ColShiftAttention(d, H)
        self.n2 = nn.LayerNorm(d)
        self.mlp = nn.Sequential(nn.Linear(d, ff), nn.GELU(), nn.Linear(ff, d))

    def forward(self, h, cq, sq, ck, sk):
        h = h + self.att(self.n1(h), cq, sq, ck, sk)
        return h + self.mlp(self.n2(h))


class Model(nn.Module):
    def __init__(self, vocab_size, max_len):
        super().__init__()
        d, H, ff, L = 80, 4, 240, 2
        hd = d // H          # 20
        f = hd // 4          # 5 rotated pairs -> 10 column-rotated dims, 10 content-only dims
        self.emb = nn.Embedding(vocab_size, d)
        self.blocks = nn.ModuleList([Block(d, H, ff) for _ in range(L)])
        self.norm = nn.LayerNorm(d)
        self.head = nn.Linear(d, vocab_size)
        self.register_buffer('inv', 1.0 / (64.0 ** (torch.arange(f).float() / f)), persistent=False)

    def forward(self, x):
        B, T = x.shape
        idx = torch.arange(T, device=x.device, dtype=torch.float32).unsqueeze(0).expand(B, T)
        nl = torch.where(x == 0, idx, torch.full_like(idx, -1.0))   # '\n' has id 0
        last_nl = torch.cummax(nl, dim=1).values                     # causal prefix scan
        col = idx - last_nl                                          # column of each position
        colk = torch.cat([col[:, :1] - 1.0, col[:, :-1]], dim=1)     # column of s-1 for shifted keys
        aq = (col.unsqueeze(-1) * self.inv).unsqueeze(1)             # [B,1,T,f]
        ak = (colk.unsqueeze(-1) * self.inv).unsqueeze(1)
        cq, sq, ck, sk = aq.cos(), aq.sin(), ak.cos(), ak.sin()
        h = self.emb(x)
        for blk in self.blocks:
            h = blk(h, cq, sq, ck, sk)
        return self.head(self.norm(h))
