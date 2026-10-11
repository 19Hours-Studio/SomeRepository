"""SIEVE model: a small tree-aware transformer with typed, calibrated outputs (no free text).

Heads (read from the CLS position):
  verdict  - logit of P(statement is true); trained only on verified labels with log loss (calibrated)
  witness  - per-variable, per-bit logits of a counterexample (x, y); trained on found counterexamples
Configs: tiny (CPU tests), small (~25M), base (~85M) for an RTX 3060.
"""
import torch
import torch.nn as nn
from bitworld import W, UN, BIN

OPS = list(UN) + list(BIN)
SPECIAL = ["[PAD]", "[CLS]", "[L]", "[R]", "[PRE]", "[INST]", "x", "y", "c"]
PRES = ["none", "disjoint", "x_even", "x_msb0", "y_zero", "x_eq_y", "y_sub_x"]
INSTS = ["none", "y=x", "y=~x", "y=0", "y=2x", "y=-x"]
VOCAB = SPECIAL + OPS + ["PRE:" + p for p in PRES] + ["INST:" + s for s in INSTS]
TOK = {t: i for i, t in enumerate(VOCAB)}
SEG = {"cls": 0, "L": 1, "R": 2, "PRE": 3, "INST": 4}
MAX_DEPTH = 16

CONFIGS = {
    "tiny": dict(d=64, layers=2, heads=4, max_len=96),
    "small": dict(d=512, layers=8, heads=8, max_len=128),
    "base": dict(d=768, layers=12, heads=12, max_len=128),
}


def _walk(e, depth, child, out):
    """Prefix walk emitting (token, depth, child_index, const_value)."""
    t = e[0]
    if t == "c": out.append(("c", depth, child, e[1])); return
    out.append((t, depth, child, 0))
    for k, a in enumerate(e[1:]): _walk(a, depth + 1, k + 1, out)


def encode(stmt, max_len):
    """Statement -> parallel lists: token ids, segment ids, depth, child index, constant bits."""
    rows = [("[CLS]", "cls", 0, 0, 0)]
    for side, e in (("L", stmt.lhs), ("R", stmt.rhs)):
        rows.append(("[" + side + "]", side, 0, 0, 0)); seq = []; _walk(e, 1, 0, seq)
        rows += [(t, side, d, c, v) for t, d, c, v in seq]
    rows.append(("PRE:" + (stmt.pre or "none"), "PRE", 0, 0, 0))
    rows.append(("INST:" + (stmt.inst or "none"), "INST", 0, 0, 0))
    rows = rows[:max_len]
    tok = [TOK[r[0]] for r in rows]; seg = [SEG[r[1]] for r in rows]
    dep = [min(r[2], MAX_DEPTH - 1) for r in rows]; chi = [min(r[3], 2) for r in rows]
    cst = [[(r[4] >> b) & 1 for b in range(W)] for r in rows]
    return tok, seg, dep, chi, cst


def batch_encode(stmts, max_len, device="cpu"):
    enc = [encode(s, max_len) for s in stmts]; n = max(len(e[0]) for e in enc)
    def pad(k, fill): return [e[k] + [fill] * (n - len(e[k])) for e in enc]
    T = lambda x, dt=torch.long: torch.tensor(x, dtype=dt, device=device)
    tok = T(pad(0, 0)); return dict(tok=tok, seg=T(pad(1, 0)), dep=T(pad(2, 0)), chi=T(pad(3, 0)),
                                    cst=T(pad(4, [0] * W), torch.float32), mask=tok.eq(0))


class Sieve(nn.Module):
    def __init__(self, d=256, layers=4, heads=4, max_len=128, dropout=0.0):
        super().__init__()
        self.max_len = max_len
        self.tok = nn.Embedding(len(VOCAB), d); self.seg = nn.Embedding(len(SEG), d)
        self.dep = nn.Embedding(MAX_DEPTH, d); self.chi = nn.Embedding(3, d); self.cst = nn.Linear(W, d, bias=False)
        layer = nn.TransformerEncoderLayer(d, heads, 4 * d, dropout, batch_first=True, norm_first=True, activation="gelu")
        self.enc = nn.TransformerEncoder(layer, layers, enable_nested_tensor=False)
        self.norm = nn.LayerNorm(d)
        self.verdict = nn.Linear(d, 1)
        self.witness = nn.Sequential(nn.Linear(d, d), nn.GELU(), nn.Linear(d, 2 * W))
        self.log_t = nn.Parameter(torch.zeros(()), requires_grad=False)  # temperature, set on R-free families

    def forward(self, b):
        h = self.tok(b["tok"]) + self.seg(b["seg"]) + self.dep(b["dep"]) + self.chi(b["chi"]) + self.cst(b["cst"])
        h = self.norm(self.enc(h, src_key_padding_mask=b["mask"]))[:, 0]
        return dict(verdict=self.verdict(h).squeeze(-1), witness=self.witness(h).view(-1, 2, W))

    @torch.no_grad()
    def prob(self, b):
        return torch.sigmoid(self.forward(b)["verdict"] / self.log_t.exp())


def build(name):
    return Sieve(**CONFIGS[name])


def n_params(m): return sum(p.numel() for p in m.parameters())
