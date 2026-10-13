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


class _InductionCopy(nn.Module):
    """query = local context ending at t, key = local context ending at j (< t),
    value = embedding of the character that FOLLOWED j, i.e. x[j+1] (j+1 <= t, so causal)."""

    def __init__(self, d, h=2, dk=32, kw=5):
        super().__init__()
        self.h, self.dk, self.kw = h, dk, kw
        self.ln = nn.LayerNorm(d)
        self.dw = nn.Conv1d(d, d, kw, groups=d)  # causal (left-padded) local n-gram summary
        self.wq = nn.Linear(d, h * dk, bias=False)
        self.wk = nn.Linear(d, h * dk, bias=False)
        with torch.no_grad():
            self.wk.weight.copy_(self.wq.weight)  # start as a context-similarity matcher
        self.wv = nn.Linear(d, d, bias=False)
        self.proj = nn.Linear(d, d, bias=False)
        self.sink = nn.Parameter(torch.zeros(h, 1, 1))  # "no match" option, value 0

    def forward(self, x, e):
        B, T, C = x.shape
        z = F.pad(self.ln(x).transpose(1, 2), (self.kw - 1, 0))
        z = self.dw(z).transpose(1, 2)                                              # [B,T,C]
        q = self.wq(z).view(B, T, self.h, self.dk).transpose(1, 2)                  # [B,h,T,dk]
        k = self.wk(z[:, :-1]).view(B, T - 1, self.h, self.dk).transpose(1, 2)      # keys j=0..T-2
        v = self.wv(e[:, 1:]).view(B, T - 1, self.h, C // self.h).transpose(1, 2)   # value_j = emb(x[j+1])
        s = (q @ k.transpose(-1, -2)) / math.sqrt(self.dk)                          # [B,h,T,T-1]
        allowed = torch.ones(T, T - 1, dtype=torch.bool, device=x.device).tril(-1)  # j < t
        s = s.masked_fill(~allowed, float('-inf'))
        s = torch.cat([self.sink.expand(B, self.h, T, 1), s], dim=-1)
        p = torch.softmax(s, dim=-1)[..., 1:]
        o = (p @ v).transpose(1, 2).reshape(B, T, C)
        return x + self.proj(o)


class Model(nn.Module):
    def __init__(self, vocab_size, max_len):
        super().__init__()
        d, h = 80, 4
        dh = d // h
        self.emb = nn.Embedding(vocab_size, d)
        self.b1 = _Block(d, h, 2)
        self.copy = _InductionCopy(d, h=2, dk=32, kw=5)
        self.b2 = _Block(d, h, 2)
        self.ln = nn.LayerNorm(d)
        self.head = nn.Linear(d, vocab_size)
        self.register_buffer('inv_freq', 1.0 / (10000 ** (torch.arange(0, dh, 2).float() / dh)), persistent=False)

    def forward(self, x):
        B, T = x.shape
        e = self.emb(x)
        t = torch.arange(T, device=x.device, dtype=e.dtype)
        fr = torch.outer(t, self.inv_freq)
        cos, sin = fr.cos(), fr.sin()
        h = self.b1(e, cos, sin)
        h = self.copy(h, e)
        h = self.b2(h, cos, sin)
        return self.head(self.ln(h))
