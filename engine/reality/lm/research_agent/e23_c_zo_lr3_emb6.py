# knobs (edited per experiment)
LR_MULT = 3.0   # effective learning-rate multiplier via weight reparametrization W = c * W'
D, NH, HID, NL, REPEAT = 96, 4, 156, 2, 1   
ZERO_OUT = True   # zero-init residual output projections
CANON = True   # causal depthwise conv (k=4) residual mixers inside every block
CK = 4
NGRAM = 0          # >0: trainable hashed bigram+trigram input tables with this many dims
NB_BI, NB_TRI = 1024, 2048
CANON_SET = 'abc'  # which canon points: a=pre-attn, b=qkv, c=pre-mlp, d=mlp hidden
LR_EMB = 6.0   # separate lr multiplier for the (tied) embedding
NCOPY = -1         # number of shifted-key copy heads per block (-1: half)


def _rope(x, cos, sin):
    h = x.shape[-1] // 2
    x1, x2 = x[..., :h], x[..., h:]
    return torch.cat([x1 * cos - x2 * sin, x1 * sin + x2 * cos], -1)


class _Scale(nn.Module):
    def __init__(self, c):
        super().__init__()
        self.c = c

    def forward(self, w):
        return w * self.c


def _apply_lr_mult(model, c):
    import torch.nn.utils.parametrize as P
    for m in list(model.modules()):
        cm = LR_EMB if (LR_EMB is not None and isinstance(m, nn.Embedding)) else c
        if cm == 1.0:
            continue
        for name, p in list(m._parameters.items()):
            if p is None:
                continue
            P.register_parametrization(m, name, _Scale(cm))
            getattr(m.parametrizations, name).original.data.div_(cm)


def _cconv(conv, x):
    k = conv.weight.shape[-1]
    return conv(F.pad(x.transpose(1, 2), (k - 1, 0))).transpose(1, 2)


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
        if CANON:
            self.ca = nn.Conv1d(d, d, CK, groups=d); self.cb = nn.Conv1d(3 * d, 3 * d, CK, groups=3 * d); self.cc = nn.Conv1d(d, d, CK, groups=d)
            self.cd = nn.Conv1d(hidden, hidden, CK, groups=hidden)
            for c in (self.ca, self.cb, self.cc, self.cd):
                nn.init.zeros_(c.weight); nn.init.zeros_(c.bias)
            for nm in 'abcd':
                if nm not in CANON_SET:
                    delattr(self, 'c' + nm)
        if ZERO_OUT:
            nn.init.zeros_(self.out.weight); nn.init.zeros_(self.fc2.weight)

    def forward(self, x, cos, sin):
        B, T, D_ = x.shape
        g = self.h // 2 if NCOPY < 0 else self.h - NCOPY
        if CANON and 'a' in CANON_SET:
            x = x + _cconv(self.ca, x)
        z = self.qkv(self.ln1(x))
        if CANON and 'b' in CANON_SET:
            z = z + _cconv(self.cb, z)
        q, k, v = z.view(B, T, 3, self.h, self.hd).permute(2, 0, 3, 1, 4)
        q_pos = _rope(q[:, :g], cos, sin)
        k_pos = _rope(k[:, :g], cos, sin)
        k_copy = F.pad(k[:, g:], (0, 0, 1, 0))[:, :, :T]
        q = torch.cat([q_pos, q[:, g:]], 1)
        k = torch.cat([k_pos, k_copy], 1)
        a = F.scaled_dot_product_attention(q, k, v, is_causal=True)
        x = x + self.out(a.transpose(1, 2).reshape(B, T, D_))
        if CANON and 'c' in CANON_SET:
            x = x + _cconv(self.cc, x)
        u = self.fc1(self.ln2(x))
        if CANON and 'd' in CANON_SET:
            u = u + _cconv(self.cd, u)
        return x + self.fc2(F.gelu(u))


class Model(nn.Module):
    def __init__(self, vocab_size, max_len):
        super().__init__()
        d = D
        hd = d // NH
        self.emb = nn.Embedding(vocab_size, d)
        nn.init.normal_(self.emb.weight, std=d ** -0.5)
        self.conv = nn.Conv1d(d, d, 4, groups=d)
        self.blocks = nn.ModuleList([_Block(d, NH, HID) for _ in range(NL)])
        self.lnf = nn.LayerNorm(d)
        self.bias = nn.Parameter(torch.zeros(vocab_size))
        if NGRAM:
            self.bi = nn.Embedding(NB_BI, NGRAM); self.tri = nn.Embedding(NB_TRI, NGRAM)
            nn.init.normal_(self.bi.weight, std=0.1); nn.init.normal_(self.tri.weight, std=0.1)
            self.ngp = nn.Linear(2 * NGRAM, d, bias=False)
        self.register_buffer("inv_freq", 1.0 / (10000 ** (torch.arange(0, hd // 2).float() / (hd // 2))), persistent=False)
        _apply_lr_mult(self, LR_MULT)

    def forward(self, x):
        B, T = x.shape
        e = self.emb(x)
        h = e + self.conv(F.pad(e.transpose(1, 2), (3, 0))).transpose(1, 2)
        if NGRAM:
            p1 = F.pad(x, (1, 0))[:, :T]; p2 = F.pad(x, (2, 0))[:, :T]
            hb = (x * 7919 + p1 * 104729 + 13) % NB_BI
            ht = (x * 7919 + p1 * 104729 + p2 * 1299709 + 17) % NB_TRI
            h = h + self.ngp(torch.cat([self.bi(hb), self.tri(ht)], -1))
        pos = torch.arange(T, device=x.device, dtype=torch.float32)
        ang = pos[:, None] * self.inv_freq[None, :]
        cos, sin = ang.cos(), ang.sin()
        for _ in range(REPEAT):
            for blk in self.blocks:
                h = blk(h, cos, sin)
        return F.linear(self.lnf(h), self.emb.weight, self.bias)
