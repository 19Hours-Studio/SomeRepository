import math
import torch
import torch.nn as nn
import torch.nn.functional as F

_M31 = (1 << 31) - 1
_GOLD = 2654435761


class CountMemory(nn.Module):
    """Non-trainable (context of last k chars -> next char) count tables, k = 1..K.
    Orders 1-2 are indexed exactly, higher orders are hashed (context, next-char) cells.
    Filled only from PAST training batches (update is called after the forward)."""
    def __init__(self, V, K=7, log2_buckets=22):
        super().__init__()
        self.V, self.K = V, K
        self.mask = (1 << log2_buckets) - 1
        sizes = [V * V, (V + 1) * V * V] + [1 << log2_buckets] * (K - 2)
        offs, tot = [], 0
        for s in sizes:
            offs.append(tot)
            tot += s
        self.offs = offs
        self.register_buffer('table', torch.zeros(tot))

    def bases(self, x):
        V, K = self.V, self.K
        B, T = x.shape
        xp = F.pad(x + 1, (K - 1, 0), value=0)          # 0 = before the window
        h = torch.zeros_like(x)
        out = []
        for j in range(K):
            c = xp[:, K - 1 - j:K - 1 - j + T]            # x[t-j]+1, or 0
            h = (h * 1000003 + c) & _M31
            if j == 0:
                out.append(x)
            elif j == 1:
                out.append(c * V + x)
            else:
                g = h ^ (h >> 13)
                g = (g * 0x5bd1e995) & _M31
                out.append(g ^ (g >> 15))
        return out

    def _cell(self, k, b, ch):
        if k < 2:
            return b * self.V + ch + self.offs[k]
        return ((b + ch * _GOLD) & self.mask) + self.offs[k]

    def query(self, bases):
        ar = torch.arange(self.V, device=bases[0].device)
        idx = torch.stack([self._cell(k, b.unsqueeze(-1), ar) for k, b in enumerate(bases)], 2)
        return self.table[idx]                             # [B,T,K,V], no grad

    @torch.no_grad()
    def update(self, bases, x):
        if x.shape[1] < 2:
            return
        y = x[:, 1:]
        idx = torch.cat([self._cell(k, b[:, :-1], y).reshape(-1) for k, b in enumerate(bases)])
        self.table.index_put_((idx,), torch.ones(idx.numel(), device=idx.device), accumulate=True)


def count_features(C, alpha):
    V = C.shape[-1]
    N = C.sum(-1, keepdim=True)
    a = F.softplus(alpha).view(1, 1, -1, 1)
    logp = torch.log(C + a) - torch.log(N + V * a)
    conf = torch.cat([torch.log1p(N.squeeze(-1)), torch.log1p(C.amax(-1))], -1)
    return logp, conf


def rope(x, cos, sin):
    x1, x2 = x[..., 0::2], x[..., 1::2]
    return torch.stack([x1 * cos - x2 * sin, x1 * sin + x2 * cos], -1).flatten(-2)


class Block(nn.Module):
    def __init__(self, d, nh, n_rope, ff):
        super().__init__()
        self.nh, self.hd, self.nr = nh, d // nh, n_rope
        self.ln1 = nn.LayerNorm(d)
        self.ln2 = nn.LayerNorm(d)
        self.q = nn.Linear(d, d, bias=False)
        self.k = nn.Linear(d, d, bias=False)
        self.v = nn.Linear(d, d, bias=False)
        self.o = nn.Linear(d, d, bias=False)
        self.fc1 = nn.Linear(d, ff)
        self.fc2 = nn.Linear(ff, d)

    def forward(self, x, cos, sin):
        B, T, D = x.shape
        h = self.ln1(x)
        q, k, v = self.q(h), self.k(h), self.v(h)
        kp = F.pad(k, (0, 0, 1, 0))[:, :T]                 # key from h[s-1]
        nf = self.nr * self.hd
        k = torch.cat([k[..., :nf], kp[..., nf:]], -1)
        q = q.view(B, T, self.nh, self.hd).transpose(1, 2)
        k = k.view(B, T, self.nh, self.hd).transpose(1, 2)
        v = v.view(B, T, self.nh, self.hd).transpose(1, 2)
        q = torch.cat([rope(q[:, :self.nr], cos, sin), q[:, self.nr:]], 1)
        k = torch.cat([rope(k[:, :self.nr], cos, sin), k[:, self.nr:]], 1)
        a = F.scaled_dot_product_attention(q, k, v, is_causal=True)
        x = x + self.o(a.transpose(1, 2).reshape(B, T, D))
        return x + self.fc2(F.gelu(self.fc1(self.ln2(x))))


class Model(nn.Module):
    def __init__(self, vocab_size, max_len):
        super().__init__()
        V, d, nh, ff, K = vocab_size, 80, 4, 240, 7
        self.V, self.hd = V, d // nh
        self.emb = nn.Embedding(V, d)
        self.blocks = nn.ModuleList([Block(d, nh, 2, ff) for _ in range(2)])
        self.lnf = nn.LayerNorm(d)
        self.head = nn.Linear(d, V)
        self.mem = CountMemory(V, K)
        self.alpha = nn.Parameter(torch.full((K,), -0.5))
        self.gate = nn.Linear(d + 2 * K, K)
        nn.init.zeros_(self.gate.weight)
        nn.init.constant_(self.gate.bias, 0.15)

    def forward(self, x):
        B, T = x.shape
        inv = 1.0 / (10000 ** (torch.arange(0, self.hd, 2, device=x.device).float() / self.hd))
        ang = torch.arange(T, device=x.device).float()[:, None] * inv[None]
        cos, sin = ang.cos(), ang.sin()
        h = self.emb(x)
        for blk in self.blocks:
            h = blk(h, cos, sin)
        h = self.lnf(h)
        bases = self.mem.bases(x)
        C = self.mem.query(bases)
        logp, conf = count_features(C, self.alpha)
        w = self.gate(torch.cat([h, 0.25 * conf], -1))      # [B,T,K]
        logits = self.head(h) + (w.unsqueeze(-1) * logp).sum(2)
        if self.training and torch.is_grad_enabled():
            self.mem.update(bases, x)                       # only after use: causal
        return logits
