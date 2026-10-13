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


class Model(nn.Module):
    def __init__(self, vocab_size, max_len):
        super().__init__()
        d, H, ff, dc = 80, 4, 224, 64
        self.V = vocab_size
        self.emb = nn.Embedding(vocab_size, d)
        nn.init.normal_(self.emb.weight, std=0.02)
        self.blocks = nn.ModuleList([_Block(d, H, ff) for _ in range(2)])
        self.lnf = nn.LayerNorm(d)
        self.out = nn.Linear(d, vocab_size)
        # copy / cache head
        self.cq = nn.Linear(d, dc, bias=False)          # shared projection for query and key (symmetric match)
        self.log_tau = nn.Parameter(torch.tensor(math.log(10.0)))
        self.sink = nn.Parameter(torch.zeros(1))         # "no match" slot -> falls back to vocab softmax
        self.gate = nn.Linear(d, 1)
        nn.init.zeros_(self.gate.weight)
        nn.init.constant_(self.gate.bias, 2.0)           # start mostly on the vocab softmax
        hd = d // H
        inv = 1.0 / (10000 ** (torch.arange(0, hd, 2, dtype=torch.float32) / hd))
        self.register_buffer('inv', inv, persistent=False)

    def forward(self, x):
        B, T = x.shape
        t = torch.arange(T, device=x.device, dtype=torch.float32)
        ang = t[:, None] * self.inv[None, :]
        cos, sin = ang.cos(), ang.sin()
        h = self.emb(x)
        for blk in self.blocks:
            h = blk(h, cos, sin)
        h = self.lnf(h)                                   # [B,T,d]
        pv = F.softmax(self.out(h), dim=-1)               # [B,T,V]
        # similarity between context at t and context at j; value = char that followed j
        z = F.normalize(self.cq(h), dim=-1)               # [B,T,dc]
        sim = torch.bmm(z, z.transpose(1, 2)) * self.log_tau.exp()   # [B,T,T]
        allowed = torch.ones(T, T, dtype=torch.bool, device=x.device).tril(-1)  # j <= t-1 so x[j+1] is known
        sim = sim.masked_fill(~allowed, float('-inf'))
        sim = torch.cat([sim, self.sink.view(1, 1, 1).expand(B, T, 1)], dim=-1)  # [B,T,T+1]
        a = F.softmax(sim, dim=-1)
        nxt = torch.cat([x[:, 1:], x[:, :1]], dim=1)      # nxt[j] = x[j+1]; last column always masked
        pc = torch.bmm(a[..., :T], F.one_hot(nxt, self.V).to(a.dtype))  # [B,T,V], mass = 1 - a_sink
        g = torch.sigmoid(self.gate(h))                   # [B,T,1]
        wv = g + (1.0 - g) * a[..., T:]                   # sink mass returns to the vocab distribution
        p = wv * pv + (1.0 - g) * pc                      # sums to 1
        return torch.log(p.clamp_min(1e-8))
