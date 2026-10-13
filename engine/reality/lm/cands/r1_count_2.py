def _rope(t, cos, sin):
    h = t.shape[-1] // 2
    a, b = t[..., :h], t[..., h:]
    return torch.cat([a * cos - b * sin, a * sin + b * cos], -1)


class GridBlock(nn.Module):
    def __init__(self, d, nh, nshift, hid, nbins):
        super().__init__()
        self.nh, self.ns = nh, nshift
        self.n1 = nn.LayerNorm(d)
        self.qkv = nn.Linear(d, 3 * d, bias=False)
        self.o = nn.Linear(d, d, bias=False)
        self.n2 = nn.LayerNorm(d)
        self.f1 = nn.Linear(d, hid, bias=False)
        self.f2 = nn.Linear(hid, d, bias=False)
        self.gb = nn.Parameter(torch.zeros(nh, nbins))

    def forward(self, h, cos, sin, mask, gidx):
        B, T, D = h.shape
        dh = D // self.nh
        r = self.nh - self.ns
        q, k, v = self.qkv(self.n1(h)).view(B, T, 3, self.nh, dh).permute(2, 0, 3, 1, 4).unbind(0)
        # first r heads: RoPE; last ns heads: key at s taken from position s-1 (induction/copy heads), no RoPE
        q = torch.cat([_rope(q[:, :r], cos, sin), q[:, r:]], 1)
        k = torch.cat([_rope(k[:, :r], cos, sin), F.pad(k[:, r:, :-1], (0, 0, 1, 0))], 1)
        att = (q @ k.transpose(-1, -2)) / math.sqrt(dh)
        att = att + self.gb[:, gidx].transpose(0, 1)                               # [B,nh,T,T] grid bias
        att = att.masked_fill(~mask, float('-inf')).softmax(-1)
        y = (att @ v).transpose(1, 2).reshape(B, T, D)
        h = h + self.o(y)
        return h + self.f2(F.gelu(self.f1(self.n2(h))))


class Model(nn.Module):
    def __init__(self, vocab_size, max_len):
        super().__init__()
        d, nh, nshift, hid, nl = 96, 4, 2, 160, 2
        self.C, self.NL = 12, 4
        nbins = self.NL * (2 * self.C + 1)
        self.emb = nn.Embedding(vocab_size, d)
        nn.init.normal_(self.emb.weight, std=0.05)
        self.blocks = nn.ModuleList([GridBlock(d, nh, nshift, hid, nbins) for _ in range(nl)])
        self.nf = nn.LayerNorm(d)
        self.out_b = nn.Parameter(torch.zeros(vocab_size))
        dh = d // nh
        self.register_buffer('inv', 1.0 / (10000.0 ** (torch.arange(dh // 2).float() / (dh // 2))), persistent=False)

    def forward(self, x):
        B, T = x.shape
        dev = x.device
        ang = torch.arange(T, device=dev).float()[:, None] * self.inv[None, :]
        cos, sin = ang.cos(), ang.sin()
        causal = torch.ones(T, T, dtype=torch.bool, device=dev).tril()
        # exact causal grid coordinates (assumes '\n' == 0 in the vocabulary)
        nlm = (x == 0)
        ar = torch.arange(T, device=dev)
        line = torch.cumsum(nlm.long(), 1) - nlm.long()                            # newlines strictly before t
        last = torch.where(nlm, ar[None, :].expand(B, T), torch.full_like(x, -1)).cummax(1).values
        last_ex = torch.cat([torch.full_like(x[:, :1], -1), last[:, :-1]], 1)
        col = ar[None, :] - last_ex - 1
        dl = (line[:, :, None] - line[:, None, :]).clamp(0, self.NL - 1)           # [B,T(query),T(key)]
        dc = (col[:, None, :] - col[:, :, None]).clamp(-self.C, self.C) + self.C
        gidx = dl * (2 * self.C + 1) + dc
        h = self.emb(x)
        for blk in self.blocks:
            h = blk(h, cos, sin, causal, gidx)
        h = self.nf(h)
        return h @ self.emb.weight.t() + self.out_b
