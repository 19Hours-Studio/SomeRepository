class Block(nn.Module):
    def __init__(self, d, h, vocab, base=1000.0):
        super().__init__(); self.h = h; self.dh = d // h; nf = self.dh // 2; self.nf = nf
        self.n1 = nn.LayerNorm(d); self.qkv = nn.Linear(d, 3 * d); self.o = nn.Linear(d, d)
        self.n2 = nn.LayerNorm(d); self.ff = nn.Sequential(nn.Linear(d, 2 * d), nn.GELU(), nn.Linear(2 * d, d))
        # per-token phase increments (one counter per head x frequency), separate for queries and keys
        self.aq = nn.Embedding(vocab, h * nf); self.ak = nn.Embedding(vocab, h * nf)
        nn.init.normal_(self.aq.weight, 1.0, 0.1); nn.init.normal_(self.ak.weight, 1.0, 0.1)  # starts as plain RoPE
        self.off = nn.Parameter(torch.zeros(h, nf))  # learned phase offset on queries (e.g. "previous position")
        self.register_buffer('freq', base ** (-torch.arange(nf).float() / nf))

    def rot(self, z, ph):  # z [B,h,T,dh], ph [B,T,h,nf]
        ph = ph.permute(0, 2, 1, 3); c, s = ph.cos(), ph.sin()
        z1, z2 = z[..., :self.nf], z[..., self.nf:]
        return torch.cat([z1 * c - z2 * s, z1 * s + z2 * c], -1)

    def forward(self, x, tok, pad):
        B, T, D = x.shape
        q, k, v = self.qkv(self.n1(x)).view(B, T, 3, self.h, self.dh).permute(2, 0, 3, 1, 4)
        pq = torch.cumsum(self.aq(tok).view(B, T, self.h, self.nf), 1) * self.freq + self.off
        pk = torch.cumsum(self.ak(tok).view(B, T, self.h, self.nf), 1) * self.freq
        q, k = self.rot(q, pq), self.rot(k, pk)
        a = (q @ k.transpose(-1, -2)) / math.sqrt(self.dh)
        a = a.masked_fill(pad[:, None, None, :], -1e9).softmax(-1)
        x = x + self.o((a @ v).transpose(1, 2).reshape(B, T, D))
        return x + self.ff(self.n2(x))

class Model(nn.Module):
    def __init__(self, vocab_size, max_len, d=64, P=16):
        super().__init__(); self.emb = nn.Embedding(vocab_size, d)
        # residual phase counters: cumulative learned angle per token, read out as cos/sin (parity = phase pi per 1-bit)
        self.ap = nn.Embedding(vocab_size, P); nn.init.uniform_(self.ap.weight, 0.0, math.pi)
        self.pin = nn.Linear(2 * P, d)
        self.blocks = nn.ModuleList([Block(d, 4, vocab_size) for _ in range(3)])
        self.n = nn.LayerNorm(d); self.out = nn.Linear(d, vocab_size)

    def forward(self, x):
        pad = x == 0
        ph = torch.cumsum(self.ap(x), 1)
        h = self.emb(x) + self.pin(torch.cat([ph.cos(), ph.sin()], -1))
        for b in self.blocks: h = b(h, x, pad)
        return self.out(self.n(h))
# params: emb 2048 + ap 512 + pin 2112 + 3 x 35552 + norm 128 + out 2080 = 113,536
