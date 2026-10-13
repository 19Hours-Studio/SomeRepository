import math
import torch
import torch.nn as nn
import torch.nn.functional as F


class Model(nn.Module):
    class Block(nn.Module):
        def __init__(self, d, h, f):
            super().__init__()
            self.h = h
            self.ln1 = nn.LayerNorm(d)
            self.qkv = nn.Linear(d, 3 * d, bias=False)
            self.o = nn.Linear(d, d, bias=False)
            self.ln2 = nn.LayerNorm(d)
            self.f1 = nn.Linear(d, f, bias=False)
            self.f2 = nn.Linear(f, d, bias=False)

        @staticmethod
        def _rope(t, cos, sin):
            half = t.size(-1) // 2
            t1, t2 = t[..., :half], t[..., half:]
            return torch.cat([t1 * cos - t2 * sin, t1 * sin + t2 * cos], -1)

        def forward(self, x, cos, sin):
            B, T, D = x.shape
            q, k, v = self.qkv(self.ln1(x)).view(B, T, 3, self.h, D // self.h).permute(2, 0, 3, 1, 4)
            q, k = self._rope(q, cos, sin), self._rope(k, cos, sin)
            a = F.scaled_dot_product_attention(q, k, v, is_causal=True)
            x = x + self.o(a.transpose(1, 2).reshape(B, T, D))
            return x + self.f2(F.gelu(self.f1(self.ln2(x))))

    def __init__(self, vocab_size, max_len):
        super().__init__()
        d, h, f, dk = 80, 4, 160, 32
        self.V = vocab_size
        self.emb = nn.Embedding(vocab_size, d)
        self.blocks = nn.ModuleList([self.Block(d, h, f) for _ in range(2)])
        self.lnf = nn.LayerNorm(d)
        self.head = nn.Linear(d, vocab_size)
        half = (d // h) // 2
        self.register_buffer("inv", 1.0 / (10000.0 ** (torch.arange(half).float() / half)), persistent=False)
        # hard-wired induction / copy pointer
        self.cemb = nn.Embedding(vocab_size, dk)
        self.cconv = nn.Conv1d(dk, dk, 4)          # signature of the last 4 characters (causal via left pad)
        self.cq = nn.Linear(d, dk, bias=False)      # contextual refinement of the query
        self.ck = nn.Linear(d, dk, bias=False)      # contextual refinement of the key
        self.lnq = nn.LayerNorm(dk)
        self.lnk = nn.LayerNorm(dk)
        self.null = nn.Linear(d, 1)                 # score of "do not copy, use the generator"
        self.cscale = nn.Parameter(torch.tensor(8.0))

    def forward(self, x):
        B, T = x.shape
        ang = torch.arange(T, device=x.device, dtype=torch.float32)[:, None] * self.inv[None, :]
        cos, sin = ang.cos(), ang.sin()
        h = self.emb(x)
        for blk in self.blocks:
            h = blk(h, cos, sin)
        h = self.lnf(h)
        p_gen = F.softmax(self.head(h), -1)                                            # [B,T,V]

        g = self.cconv(F.pad(self.cemb(x).transpose(1, 2), (3, 0))).transpose(1, 2)    # [B,T,dk], uses x[t-3..t]
        q = self.lnq(g + self.cq(h))
        k = self.lnk(g + self.ck(h))
        s = torch.bmm(q, k.transpose(1, 2)) * (self.cscale / q.size(-1))              # [B,T,T] ~ scaled cosine
        valid = torch.ones(T, T, dtype=torch.bool, device=x.device).tril(-1)           # source s < t, so s+1 <= t
        s = s.masked_fill(~valid, float("-inf"))
        a = F.softmax(torch.cat([self.null(h), s], -1), -1)                            # [B,T,1+T]
        nxt = torch.cat([x[:, 1:], x[:, :1]], 1)                                       # char after source s (last column never valid)
        p_copy = torch.bmm(a[..., 1:], F.one_hot(nxt, self.V).to(a.dtype))             # [B,T,V]
        p = a[..., :1] * p_gen + p_copy                                                # sums to 1
        return torch.log(p.clamp_min(1e-9))
