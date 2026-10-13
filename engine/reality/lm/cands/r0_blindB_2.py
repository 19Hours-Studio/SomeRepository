def _rope(x, cos, sin):
    h = x.shape[-1] // 2
    x1, x2 = x[..., :h], x[..., h:]
    return torch.cat([x1 * cos - x2 * sin, x1 * sin + x2 * cos], -1)


class _Block(nn.Module):
    def __init__(self, d, n_heads, hidden):
        super().__init__()
        self.h = n_heads
        self.hd = d // n_heads
        self.ln1 = nn.LayerNorm(d)
        self.qkv = nn.Linear(d, 3 * d, bias=False)
        self.out = nn.Linear(d, d, bias=False)
        self.ln2 = nn.LayerNorm(d)
        self.fc1 = nn.Linear(d, hidden, bias=False)
        self.fc2 = nn.Linear(hidden, d, bias=False)

    def forward(self, x, cos, sin):
        B, T, D = x.shape
        q, k, v = self.qkv(self.ln1(x)).view(B, T, 3, self.h, self.hd).permute(2, 0, 3, 1, 4)
        q, k = _rope(q, cos, sin), _rope(k, cos, sin)
        a = F.scaled_dot_product_attention(q, k, v, is_causal=True)
        x = x + self.out(a.transpose(1, 2).reshape(B, T, D))
        return x + self.fc2(F.gelu(self.fc1(self.ln2(x))))


class Model(nn.Module):
    def __init__(self, vocab_size, max_len):
        super().__init__()
        d, n_heads, hidden = 96, 4, 144
        hd = d // n_heads
        self.n_abs, self.n_line = 8, 8
        self.emb = nn.Embedding(vocab_size, d)
        nn.init.normal_(self.emb.weight, std=d ** -0.5)
        # per-character increments (e.g. '(' -> +1, ')' -> -1, quote -> +1 for parity)
        self.inc = nn.Linear(d, self.n_abs + self.n_line)
        # per-character reset strength for line-level counters (e.g. newline -> reset)
        self.reset = nn.Linear(d, self.n_line)
        nn.init.constant_(self.reset.bias, -3.0)
        self.feat = nn.Linear(2 * (self.n_abs + self.n_line), d)
        self.blocks = nn.ModuleList([_Block(d, n_heads, hidden) for _ in range(2)])
        self.lnf = nn.LayerNorm(d)
        self.bias = nn.Parameter(torch.zeros(vocab_size))
        self.register_buffer(
            "inv_freq",
            1.0 / (10000 ** (torch.arange(0, hd // 2).float() / (hd // 2))),
            persistent=False,
        )

    def forward(self, x):
        B, T = x.shape
        e = self.emb(x)
        u = self.inc(e)                                            # [B,T,16]
        # exact unbounded counters: c_t = sum_{s<=t} u_s
        c_abs = torch.cumsum(u[..., :self.n_abs], dim=1)          # [B,T,8]
        # resettable counters: c_t = keep_t * c_{t-1} + u_t, computed exactly with a masked T x T matrix
        logkeep = F.logsigmoid(-self.reset(e)).transpose(1, 2)     # [B,8,T], <= 0
        L = torch.cumsum(logkeep, dim=-1)                          # [B,8,T]
        diff = L[..., :, None] - L[..., None, :]                   # [B,8,T(t),T(s)] = L_t - L_s
        mask = torch.ones(T, T, dtype=torch.bool, device=x.device).tril()
        W = diff.masked_fill(~mask, float("-inf")).exp()           # causal: only s <= t
        u_line = u[..., self.n_abs:].transpose(1, 2).unsqueeze(-1) # [B,8,T,1]
        c_line = (W @ u_line).squeeze(-1).transpose(1, 2)          # [B,T,8]
        c = torch.cat([c_abs, c_line], dim=-1)                     # [B,T,16]
        h = e + self.feat(torch.cat([torch.tanh(c), torch.cos(math.pi * c)], dim=-1))
        pos = torch.arange(T, device=x.device, dtype=torch.float32)
        ang = pos[:, None] * self.inv_freq[None, :]
        cos, sin = ang.cos(), ang.sin()
        for blk in self.blocks:
            h = blk(h, cos, sin)
        return F.linear(self.lnf(h), self.emb.weight, self.bias)
