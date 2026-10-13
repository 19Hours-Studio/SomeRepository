import math
import torch
import torch.nn as nn
import torch.nn.functional as F

PERIODS = (2.0, 3.0, 5.0, 7.0)


def seg_index(x):
    B, T = x.shape
    delim = (x == 1) | ((x >= 3) & (x <= 6))
    pos = torch.arange(T, device=x.device).unsqueeze(0).expand(B, T)
    last = torch.cummax(torch.where(delim, pos, torch.zeros_like(pos)), dim=1).values
    return (pos - last).float()


class Model(nn.Module):
    def __init__(self, vocab_size, max_len, d=64, n_phase=16, n_iter=2, d_ctx=32):
        super().__init__()
        V = vocab_size
        self.V, self.n_iter = V, n_iter
        self.E = nn.Embedding(V, d)
        self.Wq = nn.Linear(d, d, bias=False)                     # shared across iterations
        self.Wk = nn.Linear(d, d, bias=False)
        self.tok_bias = nn.Embedding(V, 1)                        # learned "is a readable slot" bias
        nn.init.zeros_(self.tok_bias.weight)
        self.pool_score = nn.Embedding(V, 1)                      # attention pooling -> sequence context
        self.ctx_emb = nn.Embedding(V, d_ctx)
        self.coef = nn.Linear(d_ctx, 7 + n_iter)                  # content, even, 4 pos, null, gates
        self.register_buffer('freqs', torch.tensor([2 * math.pi / p for p in PERIODS]))
        self.phase_logit = nn.Parameter(0.5 * torch.randn(V, n_phase))
        self.head = nn.Sequential(nn.Linear(d + 2 * n_phase + d_ctx, 128), nn.GELU(), nn.Linear(128, V))

    def forward(self, x):
        B, T = x.shape
        V = self.V
        valid = x != 0
        # length-robust sequence context (learns to focus on the task marker)
        ps = self.pool_score(x).squeeze(-1).masked_fill(~valid, float('-inf'))
        ctx = (ps.softmax(-1).unsqueeze(-1) * self.ctx_emb(x)).sum(1)       # [B,d_ctx]
        cf = self.coef(ctx)
        scale = (1.0 + cf[:, 0])[:, None, None] / math.sqrt(self.E.weight.shape[1])
        g_even = cf[:, 1][:, None, None]
        w_pos = cf[:, 2:6]
        null = cf[:, 6][:, None, None].expand(B, T, 1)
        gates = F.softplus(cf[:, 7:])                                        # [B,n_iter]
        # delimiter-relative positional kernel: sum_k w_k cos(omega_k (c_t - c_s))
        c = seg_index(x)
        ang = c.unsqueeze(-1) * self.freqs                                   # [B,T,4]
        cs, sn = ang.cos(), ang.sin()
        pos = (cs * w_pos[:, None, :]) @ cs.transpose(1, 2) + (sn * w_pos[:, None, :]) @ sn.transpose(1, 2)
        even = torch.cos(math.pi * c)[:, None, :]                            # key parity within segment
        static = pos + g_even * even + self.tok_bias(x).squeeze(-1)[:, None, :]
        mask = torch.ones(T, T, dtype=torch.bool, device=x.device).tril(-1).unsqueeze(0) & valid[:, None, :]
        static = static.masked_fill(~mask, float('-inf'))                   # strictly earlier, non-pad keys
        xp = F.pad(x, (1, 0))[:, :T]
        K = self.Wk(self.E(xp))                                              # key = previous token
        onehot = F.one_hot(x, V).float()                                     # value = own token
        p = F.one_hot(xp, V).float()                                         # pointer starts at previous token
        logits = 0.0
        for r in range(self.n_iter):
            Q = self.Wq(p @ self.E.weight)                                   # re-embed pointer distribution
            sc = scale * (Q @ K.transpose(1, 2)) + static                    # [B,T,T]
            att = torch.cat([sc, null], dim=-1).softmax(-1)[..., :T]         # null slot absorbs "nothing"
            p = att @ onehot                                                 # [B,T,V]
            logits = logits + gates[:, r, None, None] * torch.log(p + 1e-3)
        theta = math.pi * torch.sigmoid(6.0 * self.phase_logit[x])
        phi = torch.cumsum(theta, dim=1)
        feats = torch.cat([self.E(x), phi.cos(), phi.sin(), ctx[:, None, :].expand(B, T, ctx.shape[-1])], dim=-1)
        return logits + self.head(feats)
