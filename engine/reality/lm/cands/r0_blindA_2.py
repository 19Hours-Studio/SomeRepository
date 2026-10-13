class _Block(nn.Module):
    def __init__(self, d, H, ff):
        super().__init__()
        self.H = H
        self.ln1 = nn.LayerNorm(d)
        self.qkv = nn.Linear(d, 3 * d, bias=False)
        self.proj = nn.Linear(d, d, bias=False)
        self.ln2 = nn.LayerNorm(d)
        self.fc1 = nn.Linear(d, ff)
        self.fc2 = nn.Linear(ff, d)

    def forward(self, x, cos, sin):
        B, T, D = x.shape
        H = self.H
        hd = D // H
        q, k, v = self.qkv(self.ln1(x)).view(B, T, 3, H, hd).permute(2, 0, 3, 1, 4).unbind(0)
        q = _rope(q, cos, sin)
        k = _rope(k, cos, sin)
        y = F.scaled_dot_product_attention(q, k, v, is_causal=True)
        x = x + self.proj(y.transpose(1, 2).reshape(B, T, D))
        x = x + self.fc2(F.gelu(self.fc1(self.ln2(x))))
        return x


def _rope(x, cos, sin):
    x1, x2 = x[..., 0::2], x[..., 1::2]
    return torch.cat([x1 * cos - x2 * sin, x1 * sin + x2 * cos], dim=-1)


def _at(a, pos):
    # value of a at index pos along dim 1, 0 where pos < 0
    return torch.where(pos >= 0, a.gather(1, pos.clamp(min=0)), torch.zeros_like(a))


def _syntax(x, V):
    # all features at t use only x[:, :t+1]  (prefix scans: cumsum / cummax / gather of earlier positions)
    B, T = x.shape
    idx = torch.arange(T, device=x.device).unsqueeze(0).expand(B, T)
    neg = torch.full_like(x, -1)
    is_nl = x == 0
    is_sp = x == 1
    ns = ~(is_nl | is_sp)
    P = torch.cummax(torch.where(is_nl, idx, neg), dim=1).values          # last newline <= t
    known = P >= 0
    cns = torch.cumsum(ns.long(), dim=1)
    nsl = cns - _at(cns, P)                                                 # non-space chars in current line so far
    lead = nsl == 0                                                         # still in leading whitespace
    clead = torch.cumsum((is_sp & lead).long(), dim=1)
    indent = clead - _at(clead, P)                                          # indent of current line (so far)
    col = idx - P
    Q = torch.cummax(torch.where(ns, idx, neg), dim=1).values               # last non-space char <= t
    prevpos = torch.where(known, Q.gather(1, P.clamp(min=0)), neg)          # last non-space before this line
    pk = prevpos >= 0
    ppc = prevpos.clamp(min=0)
    prev_known = pk & (P.gather(1, ppc) >= 0)
    prev_indent = indent.gather(1, ppc)
    prev_char = torch.where(pk, x.gather(1, ppc), torch.full_like(x, V))
    opn = (x == 9) | (x == 60) | (x == 92)                                  # ( [ {
    cls = (x == 10) | (x == 62) | (x == 94)                                 # ) ] }
    depth = torch.cumsum(opn.long() - cls.long(), dim=1)
    f_col = torch.where(known, col.clamp(max=79), torch.full_like(x, 80))
    f_ind = torch.where(known, indent.clamp(max=31), torch.full_like(x, 32))
    f_pind = torch.where(prev_known, prev_indent.clamp(max=31), torch.full_like(x, 32))
    diff = (indent - prev_indent).clamp(-16, 8) + 16
    f_diff = torch.where(known & prev_known,
                         torch.where(lead, diff, torch.full_like(x, 25)),
                         torch.full_like(x, 26))
    f_dep = depth.clamp(-4, 7) + 4
    return f_col, f_ind, f_pind, f_diff, prev_char, f_dep


class Model(nn.Module):
    def __init__(self, vocab_size, max_len):
        super().__init__()
        d, H, ff = 64, 4, 320
        self.V = vocab_size
        self.emb = nn.Embedding(vocab_size, d)
        self.e_col = nn.Embedding(81, d)
        self.e_ind = nn.Embedding(33, d)
        self.e_pind = nn.Embedding(33, d)
        self.e_diff = nn.Embedding(27, d)
        self.e_pch = nn.Embedding(vocab_size + 1, d)
        self.e_dep = nn.Embedding(12, d)
        for e in [self.emb, self.e_col, self.e_ind, self.e_pind, self.e_diff, self.e_pch, self.e_dep]:
            nn.init.normal_(e.weight, std=0.02)
        self.blocks = nn.ModuleList([_Block(d, H, ff) for _ in range(2)])
        self.lnf = nn.LayerNorm(d)
        self.out = nn.Linear(d, vocab_size)
        hd = d // H
        inv = 1.0 / (10000 ** (torch.arange(0, hd, 2, dtype=torch.float32) / hd))
        self.register_buffer('inv', inv, persistent=False)

    def forward(self, x):
        B, T = x.shape
        f_col, f_ind, f_pind, f_diff, f_pch, f_dep = _syntax(x, self.V)
        h = (self.emb(x) + self.e_col(f_col) + self.e_ind(f_ind) + self.e_pind(f_pind)
             + self.e_diff(f_diff) + self.e_pch(f_pch) + self.e_dep(f_dep))
        t = torch.arange(T, device=x.device, dtype=torch.float32)
        ang = t[:, None] * self.inv[None, :]
        cos, sin = ang.cos(), ang.sin()
        for blk in self.blocks:
            h = blk(h, cos, sin)
        return self.out(self.lnf(h))
