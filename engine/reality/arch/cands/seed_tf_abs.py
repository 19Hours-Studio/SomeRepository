# Seed (known family): 2-layer pre-LN transformer, bidirectional attention, learned absolute positions.
class Block(nn.Module):
    def __init__(self, d, h):
        super().__init__(); self.n1 = nn.LayerNorm(d); self.att = nn.MultiheadAttention(d, h, batch_first=True)
        self.n2 = nn.LayerNorm(d); self.ff = nn.Sequential(nn.Linear(d, 3 * d), nn.GELU(), nn.Linear(3 * d, d))
    def forward(self, x, pad):
        h = self.n1(x); x = x + self.att(h, h, h, key_padding_mask=pad, need_weights=False)[0]
        return x + self.ff(self.n2(x))

class Model(nn.Module):
    def __init__(self, vocab_size, max_len, d=64):
        super().__init__(); self.emb = nn.Embedding(vocab_size, d); self.pos = nn.Embedding(max_len, d)
        self.blocks = nn.ModuleList([Block(d, 4) for _ in range(2)]); self.n = nn.LayerNorm(d); self.out = nn.Linear(d, vocab_size)
    def forward(self, x):
        pad = x == 0; h = self.emb(x) + self.pos(torch.arange(x.shape[1], device=x.device))
        for b in self.blocks: h = b(h, pad)
        return self.out(self.n(h))
