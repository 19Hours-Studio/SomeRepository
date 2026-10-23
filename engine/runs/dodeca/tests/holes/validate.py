"""Validation of the v2 statistics on simulated objects with KNOWN truth (run before
analyse.py; output -> validation.txt).

For each truth scenario we simulate R objects with n = 10 holes (rounded to 0.5 mm, as at
Jublains and Vienne), compute the p-value of every statistic under every null (NNULL
simulations per object), and report the rejection rate at alpha = 0.05.
  - continuum truths: rejection rate = false-positive 'classes' rate (should be <= 0.05)
  - class truths:     rejection rate = power
Then the same for (b) opposite-pair and (c) hemisphere tests.
"""
import numpy as np

import holestats as H

R = 400
NNULL = 1000
ALPHA = 0.05
rng = np.random.default_rng(1)


def classes(centers, counts, sd):
    def f():
        x = np.concatenate([rng.normal(c, sd, k) for c, k in zip(centers, counts)])
        return x
    return f


SCEN = {
    "C1 continuum: uniform U(10,22)": lambda: rng.uniform(10, 22, 10),
    "C2 continuum: normal N(16,3.5)": lambda: rng.normal(16, 3.5, 10),
    "C3 continuum: lognormal (skewed)": lambda: np.exp(rng.normal(np.log(16), 0.25, 10)),
    "C4 graded series: 10 evenly spaced 10-22 + N(0,0.5)":
        lambda: np.linspace(10, 22, 10) + rng.normal(0, 0.5, 10),
    "K1 3 classes 2/4/4 at 11,16.5,21.5 sd 0.3": classes((11, 16.5, 21.5), (2, 4, 4), 0.3),
    "K2 3 classes 2/4/4 at 11,16.5,21.5 sd 0.5": classes((11, 16.5, 21.5), (2, 4, 4), 0.5),
    "K3 3 classes 2/4/4 at 11,16.5,21.5 sd 1.0": classes((11, 16.5, 21.5), (2, 4, 4), 1.0),
    "K4 2 classes 5/5 at 13,20 sd 0.5": classes((13, 20), (5, 5), 0.5),
    "K5 4 classes 3/3/2/2 at 11,14.5,18,21.5 sd 0.4":
        classes((11, 14.5, 18, 21.5), (3, 3, 2, 2), 0.4),
    "P1 5 equal PAIRS, pair sizes uniform 10-22, sd 0.3":
        lambda: np.repeat(rng.uniform(10, 22, 5), 2) + rng.normal(0, 0.3, 10),
}


def run_a():
    print("=== (a) clustering: rejection rate at alpha=0.05, n=10, rounding 0.5 mm, "
          f"R={R} objects/scenario, {NNULL} null sims/object ===")
    labs = ["U", "N", "L0.5", "L1.0"]
    hdr = "scenario".ljust(56) + " ".join(f"{s}|{l}".rjust(9) for l in labs
                                          for s in ("LGR", "GAP", "G2")) + "  U&N(GAP)"
    print(hdr)
    for name, gen in SCEN.items():
        rej = {(l, s): 0 for l in labs for s in ("LGR", "GAP", "G2")}
        both = 0
        for _ in range(R):
            x = H.rnd(gen(), 0.5)
            if np.ptp(x) == 0:
                continue
            r = H.clustering_test(x, 0.5, NNULL, rng, nulls=labs)
            for l in labs:
                for s in ("LGR", "GAP", "G2"):
                    rej[(l, s)] += r[l]["p_" + s] < ALPHA
            both += (r["U"]["p_GAP"] < ALPHA) and (r["N"]["p_GAP"] < ALPHA)
        row = name.ljust(56) + " ".join(f"{rej[(l, s)] / R:9.3f}" for l in labs
                                        for s in ("LGR", "GAP", "G2"))
        print(row + f"  {both / R:9.3f}")


def run_b():
    print("\n=== (b) opposite-pair test (sum|d| vs all 945 matchings of 10 holes) ===")
    pairs = [(2 * i, 2 * i + 1) for i in range(5)]
    for name, sd in [("random assignment (null true)", None), ("equal pairs + sd 0.3", 0.3),
                     ("equal pairs + sd 1.0", 1.0), ("equal pairs + sd 2.0", 2.0)]:
        rej = 0
        for _ in range(R):
            if sd is None:
                x = H.rnd(rng.uniform(10, 22, 10), 0.5)
            else:
                x = H.rnd(np.repeat(rng.uniform(10, 22, 5), 2) + rng.normal(0, sd, 10), 0.5)
            rej += H.opposite_test(x, pairs)["p"] < ALPHA
        print(f"  {name:36s} rejection rate {rej / R:.3f}")


def run_c():
    print("\n=== (c) hemisphere test (sorted L1 vs all 252 5+5 splits) ===")
    for name, sd in [("random assignment (null true)", None),
                     ("same multiset + sd 0.3", 0.3), ("same multiset + sd 1.0", 1.0)]:
        rej = 0
        for _ in range(R):
            if sd is None:
                x = H.rnd(rng.uniform(10, 22, 10), 0.5)
                A, B = x[:5], x[5:]
            else:
                base = rng.uniform(10, 22, 5)
                A = H.rnd(base + rng.normal(0, sd, 5), 0.5)
                B = H.rnd(rng.permutation(base) + rng.normal(0, sd, 5), 0.5)
            rej += H.hemisphere_test(A, B)["p"] < ALPHA
        print(f"  {name:36s} rejection rate {rej / R:.3f}")


if __name__ == "__main__":
    run_a()
    run_b()
    run_c()
