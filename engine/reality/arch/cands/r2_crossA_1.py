class Model(nn.Module):
    def __init__(self, vocab_size, max_len, d=64, k=16, dk=32, hops=2):
        super().__init__(); self.hops = hops; self.dk = dk
        self.emb = nn.Embedding(vocab_size, d)
        self.angle = nn.Embedding(vocab_size, k)                 # per-token rotation of k phase channels
        with torch.no_grad():
            self.angle.weight[:, :k // 2].uniform_(-math.pi, math.pi)   # fast channels (mod-2 style state)
            self.angle.weight[:, k // 2:].uniform_(-0.3, 0.3)          # slow channels (counters that do not wrap by 2x)
        self.mix = nn.Linear(2 * k, d)
        # linked-list memory: cell s = (address e_s, pointer e_{s+1}); addresses carry content AND running phase
        self.q = nn.Linear(d, dk, bias=False); self.k = nn.Linear(d, dk, bias=False); self.ks = nn.Linear(d, dk, bias=False)
        self.pb = nn.Parameter(torch.zeros(hops, 2))
        self.head = nn.Sequential(nn.LayerNorm((hops + 1) * d), nn.Linear((hops + 1) * d, 256), nn.GELU(),
                                  nn.Linear(256, vocab_size))
    def forward(self, x):
        B, T = x.shape; pad = x == 0
        th = self.angle(x).masked_fill(pad[..., None], 0.0).cumsum(1)        # [B, T, k], magnitude never decays
        e = self.emb(x) + self.mix(torch.cat([th.cos(), th.sin()], -1))      # [B, T, d]
        e = e.masked_fill(pad[..., None], 0.0)
        nxt = torch.cat([e[:, 1:], torch.zeros_like(e[:, :1])], 1)          # pointer stored in each cell
        r = torch.cat([torch.zeros_like(e[:, :1]), e[:, :-1]], 1)           # register starts at previous token
        key = self.k(e) + self.ks(nxt)                                      # [B, T, dk]
        par = torch.arange(T, device=x.device) % 2
        reads = [e]
        for i in range(self.hops):                                          # same dereference applied repeatedly
            s = self.q(r) @ key.transpose(1, 2) / math.sqrt(self.dk) + self.pb[i][par][None, None, :]
            r = s.masked_fill(pad[:, None, :], -1e9).softmax(-1) @ nxt      # r <- *r, again in embedding space
            reads.append(r)
        return self.head(torch.cat(reads, -1))                              # [B, T, vocab_size]
