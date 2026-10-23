"""Statistics shared by analyse.py, g2_check.py and validate.py (v2, 2026-10-22).

(a) classes vs continuum
    statistics (all location/scale invariant):
      LGR  = largest gap / mean gap of the sorted sizes
      G2   = (two largest gaps) / range
      GAP  = max over k=2..4 of  E0[log(W_k/T)] - log(W_k/T)   (k-means gap statistic,
             E0 taken from the same null sample)
    nulls (each simulated, then rounded to the precision the source reports):
      U    = continuum, uniform: n-2 sizes uniform between the observed min and max
      N    = continuum, smooth unimodal: n sizes ~ Normal(observed mean, observed sd)
      L(s) = evenly spaced 'graded series' over the observed range + Gaussian scatter s mm.
             NOT a continuum null: it is a near-lattice, so it is rejected by almost any
             random set (see validate.py); kept only for comparison with results_v1.
    A 'classes' verdict needs rejection under BOTH continuum nulls U and N.
(b) opposite holes: sum |d| over the source's opposite pairs vs ALL perfect matchings
    of the same values (uniform over matchings = random assignment of sizes to faces).
(c) hemispheres: L1 distance between the sorted size lists of the two rings of five
    around the unringed poles vs all 252 splits of the ten ringed sizes into 5+5.
"""
import itertools
import math

import numpy as np

KS = (2, 3, 4)


# ----------------------------------------------------------------- (a) clustering
def _cut_sets(n, k):
    return list(itertools.combinations(range(1, n), k - 1))


def wss_min(X, k):
    """Optimal 1-D k-means within-SS for each row of row-sorted X (exhaustive, contiguous)."""
    n = X.shape[1]
    S1 = np.concatenate([np.zeros((X.shape[0], 1)), np.cumsum(X, 1)], 1)
    S2 = np.concatenate([np.zeros((X.shape[0], 1)), np.cumsum(X * X, 1)], 1)
    best = np.full(X.shape[0], np.inf)
    for cuts in _cut_sets(n, k):
        b = (0,) + cuts + (n,)
        w = np.zeros(X.shape[0])
        for lo, hi in zip(b[:-1], b[1:]):
            s1 = S1[:, hi] - S1[:, lo]
            s2 = S2[:, hi] - S2[:, lo]
            w += s2 - s1 * s1 / (hi - lo)
        best = np.minimum(best, w)
    return best


def stats(X):
    """Return LGR, G2 and {k: log(W_k/T)} for each row of X (any order)."""
    X = np.sort(np.atleast_2d(np.asarray(X, float)), 1)
    n = X.shape[1]
    g = np.diff(X, axis=1)
    rngw = np.maximum(X[:, -1] - X[:, 0], 1e-12)
    lgr = g.max(1) / (rngw / (n - 1))
    gs = np.sort(g, 1)
    g2 = (gs[:, -1] + gs[:, -2]) / rngw
    T = np.maximum(((X - X.mean(1, keepdims=True)) ** 2).sum(1), 1e-12)
    L = {k: np.log(np.maximum(wss_min(X, k), 1e-12) / T) for k in KS}
    return lgr, g2, L


def rnd(X, prec):
    return np.round(X / prec) * prec if prec else X


def null_uniform(x, prec, nsim, rng):
    n = len(x)
    lo, hi = min(x), max(x)
    U = rng.uniform(lo, hi, size=(nsim, n - 2))
    X = np.concatenate([np.full((nsim, 1), lo), np.full((nsim, 1), hi), U], 1)
    return rnd(X, prec)


def null_normal(x, prec, nsim, rng):
    x = np.asarray(x, float)
    X = rng.normal(x.mean(), x.std(ddof=1), size=(nsim, len(x)))
    return rnd(X, prec)


def null_lattice(x, prec, nsim, rng, sigma):
    n = len(x)
    t = np.linspace(min(x), max(x), n)
    X = t[None, :] + rng.normal(0, sigma, size=(nsim, n))
    return rnd(X, prec)


NULLS = {
    "U": lambda x, p, ns, r: null_uniform(x, p, ns, r),
    "N": lambda x, p, ns, r: null_normal(x, p, ns, r),
    "L0.5": lambda x, p, ns, r: null_lattice(x, p, ns, r, 0.5),
    "L1.0": lambda x, p, ns, r: null_lattice(x, p, ns, r, 1.0),
}


def clustering_test(x, prec, nsim, rng, nulls=("U", "N", "L0.5", "L1.0")):
    """p-values (upper tail = more clustered than the null) for LGR, G2, GAP."""
    x = np.sort(np.asarray(x, float))
    lgr_o, g2_o, L_o = stats(x[None, :])
    out = {"n": len(x), "LGR": float(lgr_o[0]), "G2": float(g2_o[0])}
    for lab in nulls:
        X = NULLS[lab](x, prec, nsim, rng)
        lgr_s, g2_s, L_s = stats(X)
        E0 = {k: L_s[k].mean() for k in KS}
        gap_o = {k: E0[k] - L_o[k][0] for k in KS}
        gmax_o = max(gap_o.values())
        gmax_s = np.max(np.stack([E0[k] - L_s[k] for k in KS]), 0)
        out[lab] = dict(
            p_LGR=float((lgr_s >= lgr_o[0] - 1e-12).mean()),
            p_G2=float((g2_s >= g2_o[0] - 1e-12).mean()),
            p_GAP=float((gmax_s >= gmax_o - 1e-12).mean()),
            gap=round(float(gmax_o), 3), kbest=max(gap_o, key=gap_o.get))
    return out


# ----------------------------------------------------------------- (b) opposite pairs
def matchings(items):
    if not items:
        yield []
        return
    a = items[0]
    for i in range(1, len(items)):
        rest = items[1:i] + items[i + 1:]
        for m in matchings(rest):
            yield [(a, items[i])] + m


_MATCH_CACHE = {}


def _all_matchings(n):
    if n not in _MATCH_CACHE:
        _MATCH_CACHE[n] = np.array([[p for pair in m for p in pair]
                                    for m in matchings(list(range(n)))], int)
    return _MATCH_CACHE[n]


def matching_null(vals):
    """Exact distribution of sum|d| over all perfect matchings of vals."""
    v = np.asarray(vals, float)
    M = _all_matchings(len(v))
    a, b = v[M[:, 0::2]], v[M[:, 1::2]]
    return np.abs(a - b).sum(1)


def opposite_test(vals, pairs_idx):
    v = np.asarray(vals, float)
    obs = float(sum(abs(v[i] - v[j]) for i, j in pairs_idx))
    S = matching_null(v)
    return dict(obs=round(obs, 3), p=float((S <= obs + 1e-9).mean()), n_match=len(S),
                mean=round(float(S.mean()), 3), sd=round(float(S.std()), 3),
                min=round(float(S.min()), 3), z=round(float((obs - S.mean()) / S.std()), 3),
                ratio=round(obs / float(S.mean()), 3))


# ----------------------------------------------------------------- (c) hemispheres
def hemisphere_test(ringA, ringB):
    A, B = list(ringA), list(ringB)
    allv = A + B
    D_obs = sum(abs(a - b) for a, b in zip(sorted(A), sorted(B)))
    cnt = le = 0
    for comb in itertools.combinations(range(10), 5):
        a = sorted(allv[i] for i in comb)
        b = sorted(allv[i] for i in range(10) if i not in comb)
        cnt += 1
        le += sum(abs(x - y) for x, y in zip(a, b)) <= D_obs + 1e-9
    return dict(L1=round(D_obs, 3), p=le / cnt, n_split=cnt)


def congruence_test(ringA, ringB, nsim, rng):
    """Duval-convention rings (both numbered counter-clockwise seen from above, B seen
    'en transparence', face k' opposite face k).  Pole-swapping symmetries of the
    dodecahedron map ring A position i to ring B position (c - i) mod 5 (proper 2-fold
    rotations) or (i + c) mod 5 (improper: inversion times a rotation about the pole axis;
    c = 0 is the antipodal map).  Statistic: best L1 over each family; null: random
    assignment of the ten ringed sizes to the ten faces."""
    A = np.asarray(ringA, float)
    B = np.asarray(ringB, float)

    def best(AA, BB, kind):
        idx = np.arange(5)
        outs = []
        for c in range(5):
            j = (c - idx) % 5 if kind == "proper" else (idx + c) % 5
            outs.append(np.abs(AA - BB[..., j]).sum(-1))
        return np.min(np.stack(outs), 0)

    allv = np.concatenate([A, B])
    sims = np.array([rng.permutation(allv) for _ in range(nsim)])
    res = {}
    for kind in ("proper", "improper"):
        o = float(best(A[None, :], B[None, :], kind)[0])
        s = best(sims[:, :5], sims[:, 5:], kind)
        res[kind] = dict(L1=round(o, 3), p=float((s <= o + 1e-9).mean()))
    return res


# ----------------------------------------------------------------- pooling
def fisher(ps, floor):
    ps = [max(p, floor) for p in ps]
    X2 = -2 * sum(math.log(p) for p in ps)
    m = X2 / 2
    return math.exp(-m) * sum(m ** i / math.factorial(i) for i in range(len(ps)))
