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

    # Vocabulary assumption: id 0 = '\n', id i = chr(31 + i) for printable ASCII (sorted order).
    # ' '=1, '"'=3, "'"=8, '('=9, ')'=10, '['=60, ']'=62, '{'=92, '}'=94
    def __init__(self, vocab_size, max_len):
        super().__init__()
        d, h, f = 80, 4, 160
        self.V = vocab_size
        self.emb = nn.Embedding(vocab_size, d)
        self.e_col = nn.Embedding(65, d)              # column 0..63, 64 = line start unseen
        self.e_ind = nn.Embedding(34, d)              # current-line indent 0..32, 33 = unknown
        self.e_pind = nn.Embedding(34, d)             # previous-line indent 0..32, 33 = unknown
        self.e_plast = nn.Embedding(vocab_size + 1, d)  # last char of previous line, V = unknown
        self.e_dep = nn.Embedding(12, d)              # bracket depth estimate 0..11
        self.e_quo = nn.Embedding(5, d)               # (" parity, ' parity) within line, 4 = unknown
        for e in (self.e_col, self.e_ind, self.e_pind, self.e_plast, self.e_dep, self.e_quo):
            nn.init.normal_(e.weight, std=0.3)
        self.blocks = nn.ModuleList([self.Block(d, h, f) for _ in range(2)])
        self.lnf = nn.LayerNorm(d)
        self.head = nn.Linear(d, vocab_size)
        half = (d // h) // 2
        self.register_buffer("inv", 1.0 / (10000.0 ** (torch.arange(half).float() / half)), persistent=False)

    def structure(self, x):
        B, T = x.shape
        V = self.V
        idx = torch.arange(T, device=x.device).unsqueeze(0).repeat(B, 1)
        unk = lambda val: torch.full_like(idx, val)
        nl = x == 0
        last = torch.where(nl, idx, unk(-1)).cummax(1).values      # last newline at or before t
        seen = last >= 0
        lastc = last.clamp(min=0)

        def seg(v):  # count of v strictly after the last newline, up to and including t
            c = v.long().cumsum(1)
            return c - torch.where(seen, c.gather(1, lastc), torch.zeros_like(c))

        sp = x == 1
        col = torch.where(seen, (idx - last).clamp(max=63), unk(64))
        lead = seen & (seg(~nl & ~sp) == 0)                          # still in the leading whitespace
        ind = seg(lead & sp)                                         # indentation of the current line so far
        ind_id = torch.where(seen, ind.clamp(max=32), unk(33))
        p = (last - 1).clamp(min=0)                                  # last char of the previous line
        has_prev = last >= 1
        pvalid = has_prev & seen.gather(1, p)
        pind_id = torch.where(pvalid, ind.gather(1, p).clamp(max=32), unk(33))
        plast = torch.where(has_prev, x.gather(1, p), unk(V))
        opn = (x == 9) | (x == 60) | (x == 92)
        cls = (x == 10) | (x == 62) | (x == 94)
        dep = (opn.long() - cls.long()).cumsum(1)
        dep = dep - dep.cummin(1).values.clamp(max=0)                # lower-bound estimate of absolute depth
        dep_id = dep.clamp(max=11)
        quo = (seg(x == 3) % 2) * 2 + seg(x == 8) % 2
        quo_id = torch.where(seen, quo, unk(4))
        return (self.e_col(col) + self.e_ind(ind_id) + self.e_pind(pind_id)
                + self.e_plast(plast) + self.e_dep(dep_id) + self.e_quo(quo_id))

    def forward(self, x):
        B, T = x.shape
        ang = torch.arange(T, device=x.device, dtype=torch.float32)[:, None] * self.inv[None, :]
        cos, sin = ang.cos(), ang.sin()
        h = self.emb(x) + self.structure(x)
        for blk in self.blocks:
            h = blk(h, cos, sin)
        return self.head(self.lnf(h))
