import math
import torch
import torch.nn as nn
import torch.nn.functional as F


def _rot(x, cos, sin):
    f = cos.shape[-1]
    x1, x2, xp = x[..., :f], x[..., f:2 * f], x[..., 2 * f:]
    return torch.cat([x1 * cos - x2 * sin, x1 * sin + x2 * cos, xp], dim=-1)


class RopeAttention(nn.Module):
    def __init__(self, d, H):
        super().__init__()
        self.H, self.hd = H, d // H
        self.qkv = nn.Linear(d, 3 * d, bias=False)
        self.o = nn.Linear(d, d, bias=False)

    def forward(self, h, cos, sin):
        B, T, d = h.shape
        q, k, v = self.qkv(h).view(B, T, 3, self.H, self.hd).permute(2, 0, 3, 1, 4)
        q = _rot(q, cos, sin)
        k = _rot(k, cos, sin)
        y = F.scaled_dot_product_attention(q, k, v, is_causal=True)
        return self.o(y.transpose(1, 2).reshape(B, T, d))


class Block(nn.Module):
    def __init__(self, d, H, ff):
        super().__init__()
        self.n1 = nn.LayerNorm(d)
        self.att = RopeAttention(d, H)
        self.n2 = nn.LayerNorm(d)
        self.mlp = nn.Sequential(nn.Linear(d, ff), nn.GELU(), nn.Linear(ff, d))

    def forward(self, h, cos, sin):
        h = h + self.att(self.n1(h), cos, sin)
        return h + self.mlp(self.n2(h))


class Model(nn.Module):
    def __init__(self, vocab_size, max_len):
        super().__init__()
        d, H, ff, L, K = 80, 4, 240, 2, 8
        hd = d // H
        self.V, self.K = vocab_size, K
        self.emb = nn.Embedding(vocab_size, d)
        self.lenemb = nn.Embedding(K + 1, d)      # longest in-context match order (0 = none)
        self.blocks = nn.ModuleList([Block(d, H, ff) for _ in range(L)])
        self.norm = nn.LayerNorm(d)
        self.head = nn.Linear(d, vocab_size)
        self.gate = nn.Linear(d, K)               # context-dependent trust per match order
        nn.init.zeros_(self.gate.weight)
        with torch.no_grad():
            self.gate.bias.copy_(0.15 * torch.arange(1, K + 1).float())
        self.register_buffer('inv', 1.0 / (10000.0 ** (torch.arange(0, hd, 2).float() / hd)), persistent=False)

    @torch.no_grad()
    def _copy_counts(self, x):
        B, T = x.shape
        E = x.unsqueeze(2) == x.unsqueeze(1)                                   # E[b,t,s] = x[t]==x[s]
        past = torch.ones(T, T, dtype=torch.bool, device=x.device).tril(-1)    # s < t, so x[s+1] is visible
        Y = F.pad(F.one_hot(x[:, 1:], self.V).float(), (0, 0, 0, 1))          # Y[b,s] = onehot(x[s+1])
        M = E & past
        longest = torch.zeros(B, T, dtype=torch.long, device=x.device)
        feats = []
        for k in range(1, self.K + 1):
            if k > 1:
                j = k - 1
                Es = torch.zeros_like(E)
                Es[:, j:, j:] = E[:, :-j, :-j]                                 # x[t-j]==x[s-j]
                M = M & Es
            C = torch.bmm(M.float(), Y)                                        # [B,T,V] next-char counts
            feats.append(torch.log1p(C))
            longest = torch.where(M.any(-1), torch.full_like(longest, k), longest)
        return torch.stack(feats, dim=-1), longest                             # [B,T,V,K], [B,T]

    def forward(self, x):
        B, T = x.shape
        feats, longest = self._copy_counts(x)
        pos = torch.arange(T, device=x.device).float()
        ang = pos[:, None] * self.inv[None, :]
        cos, sin = ang.cos()[None, None], ang.sin()[None, None]               # [1,1,T,hd/2]
        h = self.emb(x) + self.lenemb(longest)
        for blk in self.blocks:
            h = blk(h, cos, sin)
        h = self.norm(h)
        g = self.gate(h)                                                       # [B,T,K]
        return self.head(h) + torch.einsum('btvk,btk->btv', feats, g)
