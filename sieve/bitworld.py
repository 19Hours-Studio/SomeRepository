"""Bit world: hypotheses about w-bit machine arithmetic (the language of ALUs), with an exact verifier.

A statement is   forall x, y in {0..2^w-1}:  pre(x, y)  ->  L(x, y) == R(x, y)
optionally instantiated with y := s(x).  The verifier is exhaustive (w = 8: 65 536 pairs), so every
label is exact; a FALSE verdict comes with a counterexample.

Families are built around rewrite rules: true identities (x ^ y == (x | y) - (x & y), ...) and
near-miss rules that hold on many inputs and only under a precondition (x + y == x | y iff x & y == 0).
Each family is a small implication lattice: the seed is the strongest node; adding a precondition or
instantiating y gives weaker statements (seed => child).
"""
import random
import numpy as np

W = 8
MASK = (1 << W) - 1
_XS, _YS = np.meshgrid(np.arange(1 << W, dtype=np.uint16), np.arange(1 << W, dtype=np.uint16), indexing="ij")
XS, YS = _XS.ravel(), _YS.ravel()           # all 2^(2W) pairs
X1 = np.arange(1 << W, dtype=np.uint16)     # single-variable domain (after instantiation)

UN = {"not": lambda a: ~a, "neg": lambda a: -a, "shl1": lambda a: a << 1, "shr1": lambda a: (a & MASK) >> 1}
BIN = {"add": lambda a, b: a + b, "sub": lambda a, b: a - b, "and": lambda a, b: a & b,
       "or": lambda a, b: a | b, "xor": lambda a, b: a ^ b, "mul": lambda a, b: a * b}


def ev(e, x, y):
    """Evaluate expression tree e on uint16 arrays; result reduced mod 2^W."""
    t = e[0]
    if t == "x": return x & MASK
    if t == "y": return y & MASK
    if t == "c": return np.full_like(x, e[1] & MASK)
    if t in UN: return UN[t](ev(e[1], x, y)) & MASK
    return BIN[t](ev(e[1], x, y), ev(e[2], x, y)) & MASK


def sub(e, var, val):
    """Substitute variable leaf `var` by expression `val`."""
    if e[0] == var: return val
    if e[0] in ("x", "y", "c"): return e
    return (e[0],) + tuple(sub(a, var, val) for a in e[1:])


def tokens(e):
    """Prefix serialization."""
    if e[0] == "c": return ["c%d" % e[1]]
    if e[0] in ("x", "y"): return [e[0]]
    return [e[0]] + [t for a in e[1:] for t in tokens(a)]


X, Y = ("x",), ("y",)
C = lambda v: ("c", v & MASK)
A_, B_ = ("A",), ("B",)

# rewrite rules over pattern variables A, B: (name, lhs, rhs, truth)
RULES = [
    ("xor_or_and", ("xor", A_, B_), ("sub", ("or", A_, B_), ("and", A_, B_)), True),
    ("add_xor_carry", ("add", A_, B_), ("add", ("xor", A_, B_), ("shl1", ("and", A_, B_))), True),
    ("not_neg", ("not", A_), ("sub", ("neg", A_), C(1)), True),
    ("sub_not", ("sub", A_, B_), ("add", ("add", A_, ("not", B_)), C(1)), True),
    ("or_xor_and", ("or", A_, B_), ("add", ("xor", A_, B_), ("and", A_, B_)), True),
    ("add_or_and", ("add", A_, B_), ("add", ("or", A_, B_), ("and", A_, B_)), True),
    ("demorgan", ("and", A_, B_), ("not", ("or", ("not", A_), ("not", B_))), True),
    ("mul2_shl", ("mul", A_, C(2)), ("shl1", A_), True),
    # near misses: true only on part of the domain
    ("add_as_or", ("add", A_, B_), ("or", A_, B_), False),
    ("add_as_xor", ("add", A_, B_), ("xor", A_, B_), False),
    ("sub_as_xor", ("sub", A_, B_), ("xor", A_, B_), False),
    ("shl_shr_id", ("shr1", ("shl1", A_)), A_, False),
    ("shr_shl_id", ("shl1", ("shr1", A_)), A_, False),
    ("or_as_xor", ("or", A_, B_), ("xor", A_, B_), False),
    ("add_xor_carry_noshift", ("add", A_, B_), ("add", ("xor", A_, B_), ("and", A_, B_)), False),
    ("mul2_shr", ("mul", A_, C(2)), ("shr1", A_), False),
]

# preconditions (weakening operators)
PRES = {
    "disjoint": lambda x, y: (x & y) == 0,
    "x_even": lambda x, y: (x & 1) == 0,
    "x_msb0": lambda x, y: (x & (1 << (W - 1))) == 0,
    "y_zero": lambda x, y: y == 0,
    "x_eq_y": lambda x, y: x == y,
    "y_sub_x": lambda x, y: (y & ~x & MASK) == 0,
}
# instantiations y := s(x) (weakening operators)
INSTS = {"y=x": X, "y=~x": ("not", X), "y=0": C(0), "y=2x": ("shl1", X), "y=-x": ("neg", X)}


def rand_term(rng, depth):
    if depth == 0 or rng.random() < 0.35:
        return rng.choice([X, Y, X, Y, C(1), C(rng.randrange(1 << W))])
    if rng.random() < 0.3:
        return (rng.choice(list(UN)), rand_term(rng, depth - 1))
    return (rng.choice(["add", "sub", "and", "or", "xor"]), rand_term(rng, depth - 1), rand_term(rng, depth - 1))


class Stmt:
    __slots__ = ("lhs", "rhs", "pre", "inst", "rule", "fam")

    def __init__(self, lhs, rhs, pre=None, inst=None, rule="", fam=-1):
        self.lhs, self.rhs, self.pre, self.inst, self.rule, self.fam = lhs, rhs, pre, inst, rule, fam

    def key(self):
        return (repr(self.lhs), repr(self.rhs), self.pre, self.inst)

    def verify(self):
        """Exact verdict: (True, None) or (False, counterexample (x, y))."""
        if self.inst:
            x = X1; y = ev(INSTS[self.inst], x, x)
        else:
            x, y = XS, YS
        ok = ev(self.lhs, x, y) == ev(self.rhs, x, y)
        if self.pre: ok |= ~PRES[self.pre](x, y)
        if ok.all(): return True, None
        i = int(np.argmin(ok)); return False, (int(x[i]), int(y[i]))


def make_family(rng, fam_id, n_grand=6):
    """Seed + weakenings. Returns (stmts, edges) with edges (i, j): stmts[i] => stmts[j]."""
    name, lhs, rhs, _ = rng.choice(RULES)
    a, b = rand_term(rng, 2), rand_term(rng, 2)
    ctx = rng.random() < 0.4
    L, R = sub(sub(lhs, "A", a), "B", b), sub(sub(rhs, "A", a), "B", b)
    if ctx:  # same outer context on both sides keeps true rules true
        op, t = rng.choice(["xor", "add", "and"]), rand_term(rng, 1)
        L, R = (op, L, t), (op, R, t)
    stmts = [Stmt(L, R, rule=name, fam=fam_id)]; edges = []
    pre_idx, inst_idx = {}, {}
    for p in PRES:
        pre_idx[p] = len(stmts); edges.append((0, len(stmts))); stmts.append(Stmt(L, R, pre=p, rule=name, fam=fam_id))
    for s in INSTS:
        inst_idx[s] = len(stmts); edges.append((0, len(stmts))); stmts.append(Stmt(L, R, inst=s, rule=name, fam=fam_id))
    combos = [(p, s) for p in PRES for s in INSTS]; rng.shuffle(combos)
    for p, s in combos[:n_grand]:
        k = len(stmts); stmts.append(Stmt(L, R, pre=p, inst=s, rule=name, fam=fam_id))
        edges += [(pre_idx[p], k), (inst_idx[s], k)]
    return stmts, edges


def build_pool(n_fam, seed):
    rng = random.Random(seed); stmts, edges = [], []
    for f in range(n_fam):
        s, e = make_family(rng, f); off = len(stmts)
        stmts += s; edges += [(i + off, j + off) for i, j in e]
    truth = np.array([st.verify()[0] for st in stmts], dtype=bool)
    return stmts, edges, truth


if __name__ == "__main__":
    st, ed, tr = build_pool(50, 0)
    print(f"{len(st)} statements, {len(ed)} edges, true share {tr.mean():.2f}")
    for s in st[:3]:
        print(s.rule, s.pre, s.inst, " ".join(tokens(s.lhs)), "==", " ".join(tokens(s.rhs)), s.verify())
