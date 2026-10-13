import math
import torch
import torch.nn as nn
import torch.nn.functional as F

_M31 = (1 << 31) - 1
_GOLD = 2654435761


class CountMemory(nn.Module):
    """Non-trainable (context of last k chars -> next char) count tables, k = 1..K,
    filled only from PAST training batches (update is called after the forward)."""
    def __init__(self, V, K=8, log2_buckets=22):
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
        xp = F.pad(x + 1, (K - 1, 0), value=0)
        h = torch.zeros_like(x)
        out = []
        for j in range(K):
            c = xp[:, K - 1 - j:K - 1 - j + T]
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
        return self.table[idx]                              # [B,T,K,V]

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


class Model(nn.Module):
    def __init__(self, vocab_size, max_len):
        super().__init__()
        V = vocab_size
        self.V, self.K, self.L, self.E, H = V, 8, 8, 12, 272
        S = 2 * self.K
        self.S = S
        self.mem = CountMemory(V, self.K)
        self.alpha = nn.Parameter(torch.full((S,), -0.5))
        self.emb = nn.Embedding(V + 1, self.E)              # index 0 = before window
        nin = self.L * self.E + 2 * S
        self.ln = nn.LayerNorm(nin)
        self.fc1 = nn.Linear(nin, H)
        self.fc2 = nn.Linear(H, H)
        self.out = nn.Linear(H, S + V)
        with torch.no_grad():
            self.out.weight.mul_(0.1)
            self.out.bias.zero_()
            self.out.bias[:S] = 0.1

    def local_counts(self, bases, x):
        B, T = x.shape
        bs = torch.stack(bases, 1)                           # [B,K,T]
        eq = bs.unsqueeze(-1) == bs.unsqueeze(-2)            # [B,K,t,j]
        past = torch.ones(T, T, dtype=torch.bool, device=x.device).tril(-1)  # j < t
        E = (eq & past).float()
        Y = F.pad(F.one_hot(x[:, 1:], self.V).float(), (0, 0, 0, 1))        # Y[j] = onehot(x[j+1])
        return torch.matmul(E, Y.unsqueeze(1)).permute(0, 2, 1, 3)          # [B,T,K,V]

    def forward(self, x):
        B, T = x.shape
        L = self.L
        bases = self.mem.bases(x)
        C = torch.cat([self.mem.query(bases), self.local_counts(bases, x)], 2)  # [B,T,S,V]
        logp, conf = count_features(C, self.alpha)
        xp = F.pad(x + 1, (L - 1, 0), value=0)
        ctx = torch.cat([self.emb(xp[:, L - 1 - j:L - 1 - j + T]) for j in range(L)], -1)
        z = self.ln(torch.cat([ctx, conf], -1))
        z = F.gelu(self.fc1(z))
        z = F.gelu(self.fc2(z)) + z
        o = self.out(z)
        w, r = o[..., :self.S], o[..., self.S:]
        logits = r + (w.unsqueeze(-1) * logp).sum(2)
        if self.training and torch.is_grad_enabled():
            self.mem.update(bases, x)                        # only after use: causal
        return logits
