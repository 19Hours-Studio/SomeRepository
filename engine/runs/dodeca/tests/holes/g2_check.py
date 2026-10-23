"""Supplement v2: top-2 gap share G2 = (two largest gaps)/range, under the continuum nulls
U and N and the graded-series nulls L0.5 / L1.0 (see holestats.py; validated in
validate.py).  v1 is kept as sources/g2_check_v1_backup.py.

The main analysis (analyse.py) already reports pG2; this script prints it alone, for the
main hole set of every object in data.py (10 ringed holes where the unringed pair is
known, otherwise all 12).
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import holestats as H  # noqa: E402
from analyse import object_table  # noqa: E402
from data import OBJECTS  # noqa: E402

NSIM = 100_000
rng = np.random.default_rng(7)

for name, o in OBJECTS.items():
    labels, vals, opp, ringed = object_table(name, o)
    x = [vals[labels.index(k)] for k in ringed] if ringed else vals
    r = H.clustering_test(x, o["precision"], NSIM, rng)
    row = [f"{name:24s} n={len(x):2d} G2={r['G2']:.3f}"]
    for lab in ("U", "N", "L0.5", "L1.0"):
        row.append(f"{lab} p={r[lab]['p_G2']:.4f}")
    print("  ".join(row))
