"""Desk test: classes vs continuum in Roman dodecahedron hole sizes.

(a) clustering: largest-gap ratio (LGR = max gap / mean gap) and a k-means gap statistic
    (max over k=2..4 of E0[log(W_k/T)] - log(W_k/T)), each against
    null 1: n sizes uniform over the object's observed range (endpoints pinned),
    null 2: graded continuum (equally spaced intended sizes over the range) + freehand
            Gaussian scatter sigma = 0.5 and 1.0 mm;
    all simulated values rounded to the precision the source reports. 100,000 sims each.
(b) hemisphere multisets (Jublains only: the only object with pole/ring identification).
(c) opposite holes: sum |diff| over the given opposite pairs vs all perfect matchings.
"""
import itertools
import math
import sys

import numpy as np

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from data import OBJECTS  # noqa: E402

NSIM = 100_000
KS = (2, 3, 4)
rng = np.random.default_rng(20261022)


def mean_d(p):
    return (p[0] + p[1]) / 2.0


def cut_sets(n, k):
    return list(itertools.combinations(range(1, n), k - 1))


def wss_min(X, k):
    """Optimal 1-D k-means WSS for each row of sorted X (contiguous partitions, exhaustive)."""
    n = X.shape[1]
    S1 = np.concatenate([np.zeros((X.shape[0], 1)), np.cumsum(X, 1)], 1)
    S2 = np.concatenate([np.zeros((X.shape[0], 1)), np.cumsum(X * X, 1)], 1)
    best = np.full(X.shape[0], np.inf)
    for cuts in cut_sets(n, k):
        b = (0,) + cuts + (n,)
        w = np.zeros(X.shape[0])
        for lo, hi in zip(b[:-1], b[1:]):
            s1 = S1[:, hi] - S1[:, lo]
            s2 = S2[:, hi] - S2[:, lo]
            w += s2 - s1 * s1 / (hi - lo)
        best = np.minimum(best, w)
    return best


def stats(X):
    X = np.sort(X, 1)
    n = X.shape[1]
    g = np.diff(X, axis=1)
    rngw = X[:, -1] - X[:, 0]
    lgr = g.max(1) / (rngw / (n - 1))
    T = ((X - X.mean(1, keepdims=True)) ** 2).sum(1)
    L = {k: np.log(np.maximum(wss_min(X, k), 1e-12) / T) for k in KS}
    return lgr, L


def rnd(X, prec):
    return np.round(X / prec) * prec


def null_uniform(x, prec):
    n = len(x)
    lo, hi = min(x), max(x)
    U = rng.uniform(lo, hi, size=(NSIM, n - 2))
    X = np.concatenate([np.full((NSIM, 1), lo), np.full((NSIM, 1), hi), U], 1)
    return rnd(X, prec)


def null_graded(x, prec, sigma):
    n = len(x)
    t = np.linspace(min(x), max(x), n)
    X = t[None, :] + rng.normal(0, sigma, size=(NSIM, n))
    return rnd(X, prec)


def clustering_test(name, x, prec):
    x = np.array(sorted(x), float)
    lgr_o, L_o = stats(x[None, :])
    out = {"n": len(x), "LGR": float(lgr_o[0])}
    for lab, X in [("uniform", null_uniform(x, prec)),
                   ("graded+0.5", null_graded(x, prec, 0.5)),
                   ("graded+1.0", null_graded(x, prec, 1.0))]:
        lgr_s, L_s = stats(X)
        E0 = {k: L_s[k].mean() for k in KS}
        gap_o = {k: E0[k] - L_o[k][0] for k in KS}
        gmax_o = max(gap_o.values())
        gmax_s = np.max(np.stack([E0[k] - L_s[k] for k in KS]), 0)
        kbest = max(gap_o, key=gap_o.get)
        out[lab] = dict(p_LGR=float((lgr_s >= lgr_o[0]).mean()),
                        p_gap=float((gmax_s >= gmax_o - 1e-12).mean()),
                        gap=round(gmax_o, 3), kbest=kbest)
    return out


def matchings(items):
    if not items:
        yield []
        return
    a = items[0]
    for i in range(1, len(items)):
        rest = items[1:i] + items[i + 1:]
        for m in matchings(rest):
            yield [(a, items[i])] + m


def opposite_test(vals, pairs_idx):
    obs = sum(abs(vals[i] - vals[j]) for i, j in pairs_idx)
    idx = list(range(len(vals)))
    tot = le = 0
    sums = []
    for m in matchings(idx):
        s = sum(abs(vals[i] - vals[j]) for i, j in m)
        sums.append(s)
        tot += 1
        le += s <= obs + 1e-9
    return obs, le / tot, tot, float(np.mean(sums)), float(min(sums))


def main():
    res = {}
    J = OBJECTS["Jublains"]
    ringed = J["ring_A"] + J["ring_B"]
    poles = [mean_d(J["pole_A"]), mean_d(J["pole_B"])]
    res["Jublains (10 ringed)"] = clustering_test("J10", ringed, J["precision"])
    res["Jublains (12, ovals as mean axis)"] = clustering_test("J12", ringed + poles, 0.25)

    T = OBJECTS["Tongeren"]
    tvals = [v for p in T["pairs"] for v in p]
    res["Tongeren (12)"] = clustering_test("T", tvals, T["precision"])

    R = OBJECTS["Romford"]
    rvals = [mean_d(p) for p in R["faces"].values()]
    res["Romford (9 of 12)"] = clustering_test("R", rvals, R["precision"])

    for k, v in res.items():
        print(k, v)

    # pooled: Fisher combination (independent objects); confirmatory set excludes Jublains
    def fisher(ps):
        ps = [max(p, 1.0 / NSIM) for p in ps]
        X2 = -2 * sum(math.log(p) for p in ps)
        dfree = 2 * len(ps)
        # chi-square survival, even df closed form
        m = X2 / 2
        return math.exp(-m) * sum(m ** i / math.factorial(i) for i in range(dfree // 2))

    print("\nPooled Fisher p (gap statistic):")
    for lab in ("uniform", "graded+0.5", "graded+1.0"):
        allp = [res[k][lab]["p_gap"] for k in ("Jublains (10 ringed)", "Tongeren (12)",
                                               "Romford (9 of 12)")]
        conf = allp[1:]
        print(f"  {lab}: all three {fisher(allp):.4f} | Tongeren+Romford only {fisher(conf):.4f}")
    for lab in ("uniform", "graded+0.5", "graded+1.0"):
        allp = [res[k][lab]["p_LGR"] for k in ("Jublains (10 ringed)", "Tongeren (12)",
                                               "Romford (9 of 12)")]
        print(f"  LGR {lab}: all three {fisher(allp):.4f} | Tongeren+Romford {fisher(allp[1:]):.4f}")

    # (b) Jublains hemispheres
    A, B = J["ring_A"], J["ring_B"]
    allv = A + B
    D_obs = sum(abs(a - b) for a, b in zip(sorted(A), sorted(B)))
    cnt = le = 0
    for comb in itertools.combinations(range(10), 5):
        a = sorted(allv[i] for i in comb)
        b = sorted(allv[i] for i in range(10) if i not in comb)
        cnt += 1
        le += sum(abs(x - y) for x, y in zip(a, b)) <= D_obs + 1e-9
    print(f"\n(b) Jublains sorted-ring L1 distance {D_obs} mm; P(random 5+5 split <=) = {le/cnt:.3f}")
    # class-based exact probabilities (classes S<14<M<19<L)
    cls = lambda v: "S" if v < 14 else ("M" if v < 19 else "L")
    print("   classes A:", [cls(v) for v in A], " B:", [cls(v) for v in B])
    p_multiset = (2 * math.comb(4, 2) * math.comb(4, 2)) / math.comb(10, 5)
    p_rot = 5 * 30 / (math.factorial(10) / (math.factorial(2) * math.factorial(4) ** 2))
    print(f"   P(same class multiset | 2S,4M,4L random) = {p_multiset:.3f}")
    print(f"   P(class pattern invariant under a pole-swapping 2-fold rotation) = {p_rot:.4f}")
    # continuous rotation test: proper 2-fold rotations map ring A i -> ring B (i+c)%5
    def Srot(a, b):
        return min(sum(abs(a[i] - b[(i + c) % 5]) for i in range(5)) for c in range(5))
    s_obs = Srot(A, B)
    arr = np.array(allv)
    sims = np.array([rng.permutation(arr) for _ in range(NSIM)])
    SA, SB = sims[:, :5], sims[:, 5:]
    best = np.min(np.stack([np.abs(SA - np.roll(SB, -c, axis=1)).sum(1) for c in range(5)]), 0)
    print(f"   best proper-rotation L1 = {s_obs} mm; P(random <=) = {(best <= s_obs + 1e-9).mean():.4f}")
    anti = sum(abs(A[i] - B[4 - i]) for i in range(5))
    print(f"   antipodal (opposite-face) L1 = {anti} mm")

    # (c) opposite holes
    pj = [(i, 5 + 4 - i) for i in range(5)]
    o, p, tot, mu, mn = opposite_test(allv, pj)
    print(f"\n(c) Jublains ringed opposite pairs: sum|d|={o} (diffs "
          f"{[abs(allv[i]-allv[j]) for i,j in pj]}), P(random matching <=)={p:.3f} of {tot}, "
          f"mean {mu:.1f}, min {mn:.1f}")
    tp = [(2 * i, 2 * i + 1) for i in range(6)]
    for alt in (26.3, 26.0):
        tv = list(tvals)
        tv[7] = alt
        o, p, tot, mu, mn = opposite_test(tv, tp)
        print(f"(c) Tongeren (pair4={alt}): sum|d|={o:.1f}, P(random matching <=)={p:.4f} of {tot}, "
              f"mean {mu:.1f}, min {mn:.1f}")
    print("   Tongeren diffs:", [round(b - a, 1) for a, b in T["pairs"]],
          " ratios:", [round(b / a, 3) for a, b in T["pairs"]])


if __name__ == "__main__":
    main()
