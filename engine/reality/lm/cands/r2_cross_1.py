def _rope(x, cos, sin):
    h = x.shape[-1] // 2
    x1, x2 = x[..., :h], x[..., h:]
    return torch.cat([x1 * cos - x2 * sin, x1 * sin + x2 * cos], dim=-1)


class _Block(nn.Module):
    def __init__(self, d, nh, ff):
        super().__init__()
        self.nh = nh
        self.n1 = nn.LayerNorm(d)
        self.n2 = nn.LayerNorm(d)
        self.qkv = nn.Linear(d, 3 * d, bias=False)
        self.o = nn.Linear(d, d, bias=False)
        self.f1 = nn.Linear(d, ff, bias=False)
        self.f2 = nn.Linear(ff, d, bias=False)

    def forward(self, h, cos, sin):
        B, T, D = h.shape
        q, k, v = self.qkv(self.n1(h)).view(B, T, 3, self.nh, D // self.nh).permute(2, 0, 3, 1, 4)
        q, k = _rope(q, cos, sin), _rope(k, cos, sin)
        a = F.scaled_dot_product_attention(q, k, v, is_causal=True)
        h = h + self.o(a.transpose(1, 2).reshape(B, T, D))
        return h + self.f2(F.gelu(self.f1(self.n2(h))))


class Model(nn.Module):
    # params: 2 blocks 133760 + emb 7680 + norm 160 + out_bias 96 + suffix encoder 3104 + beta 1 + null 81 = 144882
    def __init__(self, vocab_size, max_len, d=80, nh=4, ff=256, n_layers=2, c=32, L=12):
        super().__init__()
        self.V, self.L = vocab_size, L
        self.emb = nn.Embedding(vocab_size, d)
        nn.init.normal_(self.emb.weight, std=0.1)
        self.blocks = nn.ModuleList([_Block(d, nh, ff) for _ in range(n_layers)])
        self.norm = nn.LayerNorm(d)
        self.out_bias = nn.Parameter(torch.zeros(vocab_size))
        hd = d // nh
        self.register_buffer(
            "inv_freq",
            1.0 / (10000.0 ** (torch.arange(0, hd // 2).float() / (hd // 2))),
            persistent=False,
        )
        # one suffix encoder shared by the query (suffix ending at t) and the key (suffix ending at j-1)
        self.cemb = nn.Embedding(vocab_size, c)
        r = torch.linspace(0.15, 0.92, c)
        self.decay = nn.Parameter(torch.log(r / (1 - r)))
        self.log_beta = nn.Parameter(torch.tensor(math.log(16.0)))
        self.null = nn.Linear(d, 1)
        nn.init.zeros_(self.null.weight)
        nn.init.constant_(self.null.bias, 1.0)

    def forward(self, x):
        B, T = x.shape
        f = torch.arange(T, device=x.device, dtype=torch.float32)[:, None] * self.inv_freq[None, :]
        cos, sin = f.cos(), f.sin()
        h = self.emb(x)
        for blk in self.blocks:
            h = blk(h, cos, sin)
        h = self.norm(h)
        lm = h @ self.emb.weight.t() + self.out_bias                      # B,T,V

        # causal suffix code g[t] = sum_i r^i * e[x[t-i]], i < L
        e = self.cemb(x).transpose(1, 2)                                  # B,c,T
        r = torch.sigmoid(self.decay)                                     # c
        pw = torch.arange(self.L - 1, -1, -1, device=x.device, dtype=e.dtype)
        ker = (r[:, None] ** pw[None, :]).unsqueeze(1)                    # c,1,L (last tap = current char)
        g = F.conv1d(F.pad(e, (self.L - 1, 0)), ker, groups=e.shape[1]).transpose(1, 2)
        g = F.normalize(g, dim=-1)                                        # B,T,c
        key = F.pad(g, (0, 0, 1, 0))[:, :T]                               # key[j] = g[j-1]
        sc = torch.exp(self.log_beta) * (g @ key.transpose(1, 2) - 1.0)   # B,T,T ; exact repeat -> 0
        valid = torch.ones(T, T, dtype=torch.bool, device=x.device).tril()
        valid[:, 0] = False                                               # j in [1, t]
        sc = sc.masked_fill(~valid, float("-inf"))
        att = torch.softmax(torch.cat([sc, self.null(h)], dim=-1), dim=-1)  # B,T,T+1
        copy = att[..., :T] @ F.one_hot(x, self.V).to(att.dtype)         # B,T,V (reads x[j], j <= t)
        p = att[..., T:] * torch.softmax(lm, dim=-1) + copy
        return torch.log(p + 1e-6)
