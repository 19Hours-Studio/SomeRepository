"""Desk test v2: classes vs continuum, opposite holes, hemispheres (output -> results.txt).

Statistics and nulls are defined and documented in holestats.py and validated on simulated
objects with known truth in validate.py (-> validation.txt).  v1 is kept as
sources/analyse_v1_backup.py and its output as results_v1.txt.

Run:  OPENBLAS_NUM_THREADS=1 python analyse.py > results.txt
"""
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import holestats as H  # noqa: E402
from data import OBJECTS  # noqa: E402

NSIM = 100_000
rng = np.random.default_rng(20261023)


def d(v):
    return (v[0] + v[1]) / 2.0 if isinstance(v, tuple) else float(v)


def object_table(name, o):
    """Return labels, values, opposite index pairs, ringed labels (or None)."""
    if "faces" in o:
        labels = list(o["faces"])
        vals = [d(o["faces"][k]) for k in labels]
        opp = [(labels.index(a), labels.index(b)) for a, b in o["opposite"]]
    else:
        labels, vals, opp = [], [], []
        for i, (a, b) in enumerate(o["pairs"]):
            labels += [f"p{i + 1}a", f"p{i + 1}b"]
            vals += [a, b]
            opp.append((2 * i, 2 * i + 1))
    ringed = None
    if o.get("poles"):
        ringed = [k for k in labels if k not in o["poles"]]
    return labels, vals, opp, ringed


def fmt_clu(r):
    s = f"n={r['n']} LGR={r['LGR']:.2f} G2={r['G2']:.2f} | "
    parts = []
    for lab in ("U", "N", "L0.5", "L1.0"):
        q = r[lab]
        parts.append(f"{lab}: pGAP={q['p_GAP']:.4f} pLGR={q['p_LGR']:.4f} pG2={q['p_G2']:.4f}"
                     f" (k*={q['kbest']})")
    return s + " ; ".join(parts)


def main():
    print("RESULTS v2 (analyse.py, data.py v2, NSIM=%d per null)\n" % NSIM)
    A_main, B_main, C_main = {}, {}, {}
    B_dist = {}
    for name, o in OBJECTS.items():
        labels, vals, opp, ringed = object_table(name, o)
        prec = o["precision"]
        print("=" * 100)
        print(f"{name}  [grade {o['grade']}; independent={o['independent']}]")
        print("  values: " + ", ".join(f"{k}={v:g}" for k, v in zip(labels, vals)))

        # ---------------- (a) classes vs continuum
        if ringed:
            xr = [vals[labels.index(k)] for k in ringed]
            r10 = H.clustering_test(xr, prec, NSIM, rng)
            print("  (a) 10 ringed: " + fmt_clu(r10))
            r12 = H.clustering_test(vals, max(prec, 0.25), NSIM, rng)
            print("  (a) all 12   : " + fmt_clu(r12))
            A_main[name] = r10
        else:
            r12 = H.clustering_test(vals, prec, NSIM, rng)
            print("  (a) all 12   : " + fmt_clu(r12))
            # sensitivity: drop the pair with the largest mean (possible production pair)
            big = max(opp, key=lambda p: vals[p[0]] + vals[p[1]])
            x10 = [v for i, v in enumerate(vals) if i not in big]
            r10 = H.clustering_test(x10, prec, NSIM, rng)
            print(f"  (a) 10 (largest pair {vals[big[0]]:g}/{vals[big[1]]:g} dropped): "
                  + fmt_clu(r10))
            A_main[name] = r12

        # ---------------- (b) opposite holes
        diffs = [round(abs(vals[i] - vals[j]), 2) for i, j in opp]
        print(f"  (b) opposite |d| per pair: {diffs}")
        rb12 = H.opposite_test(vals, opp)
        print(f"  (b) all 12 (10395 matchings): {rb12}")
        if ringed:
            ri = [labels.index(k) for k in ringed]
            sub = [vals[i] for i in ri]
            opp10 = [(ri.index(i), ri.index(j)) for i, j in opp if i in ri and j in ri]
            rb10 = H.opposite_test(sub, opp10)
            print(f"  (b) 10 ringed (945 matchings): {rb10}")
            main = (sub, opp10, rb10)
        else:
            big = max(opp, key=lambda p: vals[p[0]] + vals[p[1]])
            keep = [i for i in range(len(vals)) if i not in big]
            sub = [vals[i] for i in keep]
            opp10 = [(keep.index(i), keep.index(j)) for i, j in opp if i in keep and j in keep]
            rb10 = H.opposite_test(sub, opp10)
            print(f"  (b) 10 (largest pair dropped, 945 matchings): {rb10}")
            main = (vals, opp, rb12)
        B_main[name] = main[2]
        B_dist[name] = (H.matching_null(main[0]), main[2]["obs"])
        for key, lab in (("superseded_opposite", "SUPERSEDED pairing (Sparavigna 2012)"),
                         ("alt_opposite", "ALTERNATIVE pairing (k,k')")):
            if key in o:
                alt = [(labels.index(a), labels.index(b)) for a, b in o[key]]
                ri = [labels.index(k) for k in ringed]
                sub = [vals[i] for i in ri]
                alt10 = [(ri.index(i), ri.index(j)) for i, j in alt if i in ri and j in ri]
                print(f"  (b) {lab}, 10 ringed: |d|="
                      f"{[round(abs(sub[i] - sub[j]), 2) for i, j in alt10]} "
                      f"{H.opposite_test(sub, alt10)}")

        # ---------------- (c) hemispheres
        if ringed and o.get("ringA"):
            A = [vals[labels.index(k)] for k in o["ringA"]]
            B = [vals[labels.index(k)] for k in o["ringB"]]
            rc = H.hemisphere_test(A, B)
            cg = H.congruence_test(A, B, NSIM, rng)
            print(f"  (c) ring A {A} | ring B {B}")
            print(f"  (c) sorted A {sorted(A)} | sorted B {sorted(B)} -> multiset test {rc}")
            print(f"  (c) best pole-swapping congruence: {cg}")
            C_main[name] = rc
        elif ringed:
            ri = [labels.index(k) for k in ringed]
            # rings: faces opposite each other lie in different rings; ring A = unprimed labels
            A = [vals[i] for i in ri if "'" not in labels[i]]
            B = [vals[i] for i in ri if "'" in labels[i]]
            rc = H.hemisphere_test(A, B)
            print(f"  (c) ring A (unprimed) {sorted(A)} | ring B (primed) {sorted(B)} -> {rc}"
                  "  [ring membership assumes labels 2-6 surround pole 1]")
            C_main[name] = rc
        else:
            print("  (c) not testable (no pole/ring information)")
        print()

    # ---------------- pooled
    indep = [k for k, o in OBJECTS.items() if o["independent"]]
    gradeA = [k for k in indep if OBJECTS[k]["grade"] == "A"]
    print("=" * 100)
    print("POOLED (Fisher combination over independent objects; p floored at 1/NSIM)")
    for lab in ("U", "N", "L0.5", "L1.0"):
        for st in ("GAP", "LGR", "G2"):
            ps = [A_main[k][lab]["p_" + st] for k in indep]
            pa = [A_main[k][lab]["p_" + st] for k in gradeA]
            print(f"  (a) {lab:5s} {st:3s}: all {len(ps)}: {H.fisher(ps, 1 / NSIM):.4f}"
                  f" | grade A ({len(pa)}): {H.fisher(pa, 1 / NSIM):.4f}"
                  f" | per object {[round(p, 4) for p in ps]}")
    ps = [B_main[k]["p"] for k in indep]
    print(f"\n  (b) opposite, Fisher: all {len(ps)} objects {H.fisher(ps, 1e-6):.5f} "
          f"| grade A only {H.fisher([B_main[k]['p'] for k in gradeA], 1e-6):.5f}")
    # stratified Monte Carlo on the sum of per-object z-scores (exact per-object nulls)
    for label, keys in (("all independent", indep), ("grade A", gradeA),
                        ("without Mereaux (selection bias)",
                         [k for k in indep if "Mereaux" not in k])):
        zs_obs, zsim = 0.0, np.zeros(200_000)
        for k in keys:
            S, obs = B_dist[k]
            mu, sd = S.mean(), S.std()
            zs_obs += (obs - mu) / sd
            zsim += (rng.choice(S, size=zsim.size) - mu) / sd
        print(f"  (b) stratified MC, sum of z over {label} ({len(keys)}): sum z = {zs_obs:.2f}, "
              f"P(sim <= obs) = {(zsim <= zs_obs + 1e-9).mean():.5f}")
    if C_main:
        ps = [C_main[k]["p"] for k in C_main]
        print(f"\n  (c) hemispheres, Fisher over {list(C_main)}: {H.fisher(ps, 1 / 252):.4f}")


if __name__ == "__main__":
    main()
