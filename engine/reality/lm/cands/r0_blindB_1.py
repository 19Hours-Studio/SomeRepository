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
        g = self.h // 2
        q, k, v = self.qkv(self.ln1(x)).view(B, T, 3, self.h, self.hd).permute(2, 0, 3, 1, 4)  # each [B,H,T,hd]
        # positional heads: ordinary rotary attention
        q_pos = _rope(q[:, :g], cos, sin)
        k_pos = _rope(k[:, :g], cos, sin)
        # copy heads: key at s is built from position s-1 (causal: s-1 < s <= t), value from s
        k_copy = F.pad(k[:, g:], (0, 0, 1, 0))[:, :, :T]
        q = torch.cat([q_pos, q[:, g:]], 1)
        k = torch.cat([k_pos, k_copy], 1)
        a = F.scaled_dot_product_attention(q, k, v, is_causal=True)
        x = x + self.out(a.transpose(1, 2).reshape(B, T, D))
        return x + self.fc2(F.gelu(self.fc1(self.ln2(x))))


class Model(nn.Module):
    def __init__(self, vocab_size, max_len):
        super().__init__()
        d, n_heads, hidden = 96, 4, 160
        hd = d // n_heads
        self.emb = nn.Embedding(vocab_size, d)
        nn.init.normal_(self.emb.weight, std=d ** -0.5)
        # causal depthwise conv: gives every position a summary of its last 4 chars (sharp match keys)
        self.conv = nn.Conv1d(d, d, 4, groups=d)
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
        h = e + self.conv(F.pad(e.transpose(1, 2), (3, 0))).transpose(1, 2)
        pos = torch.arange(T, device=x.device, dtype=torch.float32)
        ang = pos[:, None] * self.inv_freq[None, :]
        cos, sin = ang.cos(), ang.sin()
        for blk in self.blocks:
            h = blk(h, cos, sin)
        return F.linear(self.lnf(h), self.emb.weight, self.bias)
