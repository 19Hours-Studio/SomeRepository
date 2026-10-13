def _rope(t, cos, sin):
    h = t.shape[-1] // 2
    a, b = t[..., :h], t[..., h:]
    return torch.cat([a * cos - b * sin, a * sin + b * cos], -1)


class Block(nn.Module):
    def __init__(self, d, nh, hid):
        super().__init__()
        self.nh = nh
        self.n1 = nn.LayerNorm(d)
        self.qkv = nn.Linear(d, 3 * d, bias=False)
        self.o = nn.Linear(d, d, bias=False)
        self.n2 = nn.LayerNorm(d)
        self.f1 = nn.Linear(d, hid, bias=False)
        self.f2 = nn.Linear(hid, d, bias=False)

    def forward(self, h, cos, sin, mask):
        B, T, D = h.shape
        dh = D // self.nh
        q, k, v = self.qkv(self.n1(h)).view(B, T, 3, self.nh, dh).permute(2, 0, 3, 1, 4).unbind(0)
        q, k = _rope(q, cos, sin), _rope(k, cos, sin)
        att = (q @ k.transpose(-1, -2)) / math.sqrt(dh)
        att = att.masked_fill(~mask, float('-inf')).softmax(-1)
        y = (att @ v).transpose(1, 2).reshape(B, T, D)
        h = h + self.o(y)
        return h + self.f2(F.gelu(self.f1(self.n2(h))))


class Model(nn.Module):
    def __init__(self, vocab_size, max_len):
        super().__init__()
        d, nh, hid, nl = 96, 4, 160, 2
        self.V, self.K, self.dp = vocab_size, 12, 16
        self.emb = nn.Embedding(vocab_size, d)
        nn.init.normal_(self.emb.weight, std=0.05)
        self.blocks = nn.ModuleList([Block(d, nh, hid) for _ in range(nl)])
        self.nf = nn.LayerNorm(d)
        self.out_b = nn.Parameter(torch.zeros(vocab_size))
        self.pq = nn.Linear(d, self.dp, bias=False)
        self.pk = nn.Linear(d, self.dp, bias=False)
        self.null = nn.Linear(d, 1)
        nn.init.zeros_(self.null.weight)
        nn.init.constant_(self.null.bias, 2.0)
        # bias per exact match length 0..K (0 = current char differs -> discourage copying)
        self.lenb = nn.Parameter(torch.cat([torch.tensor([-4.0]), torch.arange(1, self.K + 1).float()]))
        dh = d // nh
        self.register_buffer('inv', 1.0 / (10000.0 ** (torch.arange(dh // 2).float() / (dh // 2))), persistent=False)

    def forward(self, x):
        B, T = x.shape
        dev = x.device
        ang = torch.arange(T, device=dev).float()[:, None] * self.inv[None, :]
        cos, sin = ang.cos(), ang.sin()
        causal = torch.ones(T, T, dtype=torch.bool, device=dev).tril()
        h = self.emb(x)
        for blk in self.blocks:
            h = blk(h, cos, sin, causal)
        h = self.nf(h)
        p_lm = torch.softmax(h @ self.emb.weight.t() + self.out_b, -1)            # [B,T,V]
        # exact causal suffix-match length M[t,j] = #k with x[t-i]==x[j-i] for i<k, j<t
        strict = torch.ones(T, T, dtype=torch.bool, device=dev).tril(-1)
        E = ((x[:, :, None] == x[:, None, :]) & strict).float()                   # [B,T,T]
        M = E
        for _ in range(self.K - 1):
            M = E * (1.0 + F.pad(M[:, :-1, :-1], (1, 0, 1, 0)))
        s = (self.pq(h) @ self.pk(h).transpose(1, 2)) / math.sqrt(self.dp) + self.lenb[M.long()]
        s = s.masked_fill(~strict, float('-inf'))
        w = torch.softmax(torch.cat([self.null(h), s], -1), -1)                   # [B,T,1+T]
        nxt = torch.cat([x[:, 1:], x[:, :1]], 1)                                  # source j copies x[j+1] (j<t => j+1<=t)
        p = w[..., :1] * p_lm + w[..., 1:] @ F.one_hot(nxt, self.V).float()
        return torch.log(p.clamp_min(1e-8))
