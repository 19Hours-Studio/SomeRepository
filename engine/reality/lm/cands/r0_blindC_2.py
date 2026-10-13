# Assumes the natural sorted vocabulary: '\n' -> 0, chr(32..126) -> 1..95.
# If the mapping differs, the model stays valid and causal; the counters just carry less signal.
_NL = 0


def _cid(c):
    return ord(c) - 31


def _rope(x, cos, sin):
    x1, x2 = x[..., 0::2], x[..., 1::2]
    return torch.stack((x1 * cos - x2 * sin, x1 * sin + x2 * cos), dim=-1).flatten(-2)


class _Block(nn.Module):
    def __init__(self, d, h, mult):
        super().__init__()
        self.h = h
        self.ln1 = nn.LayerNorm(d)
        self.qkv = nn.Linear(d, 3 * d, bias=False)
        self.proj = nn.Linear(d, d, bias=False)
        self.ln2 = nn.LayerNorm(d)
        self.fc1 = nn.Linear(d, mult * d)
        self.fc2 = nn.Linear(mult * d, d)

    def forward(self, x, cos, sin):
        B, T, C = x.shape
        q, k, v = self.qkv(self.ln1(x)).view(B, T, 3, self.h, C // self.h).permute(2, 0, 3, 1, 4)
        q, k = _rope(q, cos, sin), _rope(k, cos, sin)
        a = F.scaled_dot_product_attention(q, k, v, is_causal=True)
        x = x + self.proj(a.transpose(1, 2).reshape(B, T, C))
        return x + self.fc2(F.gelu(self.fc1(self.ln2(x))))


def _at(v, idx):
    # v[b, idx[b,t]] with idx == -1 meaning "before the window" -> 0
    return torch.where(idx >= 0, v.gather(1, idx.clamp(min=0)), torch.zeros_like(v))


class Model(nn.Module):
    def __init__(self, vocab_size, max_len):
        super().__init__()
        d, h = 80, 4
        dh = d // h
        self.emb = nn.Embedding(vocab_size, d)
        self.e_col = nn.Embedding(64, d)    # column of the next char
        self.e_lead = nn.Embedding(42, d)   # leading spaces so far (41 = past indentation)
        self.e_ind = nn.Embedding(41, d)    # indent of most recent line containing code
        self.e_diff = nn.Embedding(26, d)   # leading-so-far minus code indent (25 = n/a)
        self.e_dep = nn.Embedding(8, d)     # unclosed ([{ depth within window
        self.e_q = nn.Embedding(4, d)       # parity of " and ' on current line
        for m in (self.e_col, self.e_lead, self.e_ind, self.e_diff, self.e_dep, self.e_q):
            nn.init.normal_(m.weight, std=0.3)
        self.blocks = nn.ModuleList([_Block(d, h, 2) for _ in range(2)])
        self.ln = nn.LayerNorm(d)
        self.head = nn.Linear(d, vocab_size)
        self.register_buffer('inv_freq', 1.0 / (10000 ** (torch.arange(0, dh, 2).float() / dh)), persistent=False)
        self.register_buffer('opn', torch.tensor([_cid(c) for c in '([{']), persistent=False)
        self.register_buffer('cls', torch.tensor([_cid(c) for c in ')]}']), persistent=False)
        self.sp, self.dq, self.sq = _cid(' '), _cid('"'), _cid("'")

    @torch.no_grad()
    def _features(self, x):
        B, T = x.shape
        pos = torch.arange(T, device=x.device).expand(B, T)
        neg = torch.full_like(pos, -1)
        is_nl = x == _NL
        is_sp = x == self.sp
        nonsp = ~(is_nl | is_sp)
        lastnl = torch.cummax(torch.where(is_nl, pos, neg), 1).values        # last '\n' at <= t
        prevnl = torch.cat([neg[:, :1], lastnl[:, :-1]], 1)                   # last '\n' at < t
        cns = nonsp.long().cumsum(1)
        lead = is_sp & ((cns - _at(cns, prevnl)) == 0)                         # leading-indent space
        clead = lead.long().cumsum(1)
        line_ind = clead - _at(clead, prevnl)                                  # indent of t's own line
        lastns = torch.cummax(torch.where(nonsp, pos, neg), 1).values
        code_ind = _at(line_ind, lastns)                                       # indent of last code line
        # state of the line the NEXT character belongs to
        col = pos - lastnl                                                     # 0 right after '\n'
        in_lead = (cns - _at(cns, lastnl)) == 0                                # no code yet on that line
        f_col = col.clamp(max=63)
        f_lead = torch.where(in_lead, col.clamp(max=40), torch.full_like(col, 41))
        f_ind = code_ind.clamp(max=40)
        f_diff = torch.where(in_lead, (col - code_ind).clamp(-12, 12) + 12, torch.full_like(col, 25))
        o = (x.unsqueeze(-1) == self.opn).any(-1).long()
        c = (x.unsqueeze(-1) == self.cls).any(-1).long()
        dep = (o - c).cumsum(1)
        f_dep = (dep - torch.cummin(dep, 1).values.clamp(max=0)).clamp(0, 7)
        cd = (x == self.dq).long().cumsum(1)
        cs = (x == self.sq).long().cumsum(1)
        f_q = ((cd - _at(cd, lastnl)) % 2) * 2 + ((cs - _at(cs, lastnl)) % 2)
        return f_col, f_lead, f_ind, f_diff, f_dep, f_q

    def forward(self, x):
        B, T = x.shape
        f_col, f_lead, f_ind, f_diff, f_dep, f_q = self._features(x)
        h = (self.emb(x) + self.e_col(f_col) + self.e_lead(f_lead) + self.e_ind(f_ind)
             + self.e_diff(f_diff) + self.e_dep(f_dep) + self.e_q(f_q))
        t = torch.arange(T, device=x.device, dtype=h.dtype)
        fr = torch.outer(t, self.inv_freq)
        cos, sin = fr.cos(), fr.sin()
        for b in self.blocks:
            h = b(h, cos, sin)
        return self.head(self.ln(h))
