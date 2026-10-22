"""Supplement: top-2 gap share G2 = (two largest gaps)/range, p under the same three nulls."""
import sys
import numpy as np
sys.path.insert(0, ".")
import analyse as A
from data import OBJECTS

def g2(X):
    X = np.sort(X, 1); g = np.sort(np.diff(X, axis=1), 1)
    return (g[:, -1] + g[:, -2]) / (X[:, -1] - X[:, 0])

J = OBJECTS["Jublains"]; T = OBJECTS["Tongeren"]; R = OBJECTS["Romford"]
sets = {"Jublains10": (J["ring_A"] + J["ring_B"], 0.5),
        "Tongeren12": ([v for p in T["pairs"] for v in p], 0.1),
        "Romford9": ([A.mean_d(p) for p in R["faces"].values()], 0.01)}
for name, (x, prec) in sets.items():
    o = g2(np.array(sorted(x))[None, :])[0]
    row = [f"{name}: G2={o:.3f}"]
    for lab, X in [("unif", A.null_uniform(x, prec)), ("gr0.5", A.null_graded(x, prec, 0.5)),
                   ("gr1.0", A.null_graded(x, prec, 1.0))]:
        row.append(f"{lab} p={(g2(X) >= o - 1e-12).mean():.4f}")
    print("  ".join(row))
