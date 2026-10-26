"""Steady heat conduction on an n x n plate (finite volumes): every cell makes heat q = 1; heat leaves only through a
sink at the middle of the bottom edge held at T = 0; all other edges are insulated. A design puts high-conductivity
material (k = 200) in at most 10% of the cells; the rest has k = 1. The figure of merit is the hottest cell.

Usage: python3 sim.py design.txt   (n lines of n characters, '1' = high-conductivity material, '0' = base material)
       -> one JSON line: {"ok", "fraction", "t_max", "score" = t_max of the bare plate / t_max of the design}
"""
import json, sys
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spl

N, KH, PHI, SINK = 101, 200.0, 0.10, 5  # sink: the 5 middle cells of the bottom row


def t_max(design):
    k = 1.0 + (KH - 1.0) * design.astype(float); n = N; idx = np.arange(n * n).reshape(n, n)
    rows, cols, vals = [], [], []; diag = np.zeros(n * n)
    for a, b in ((k[:, :-1], k[:, 1:]), ):  # horizontal faces
        g = 2 * a * b / (a + b); i, j = idx[:, :-1].ravel(), idx[:, 1:].ravel(); g = g.ravel()
        rows += [i, j]; cols += [j, i]; vals += [-g, -g]; np.add.at(diag, i, g); np.add.at(diag, j, g)
    a, b = k[:-1, :], k[1:, :]; g = (2 * a * b / (a + b)).ravel(); i, j = idx[:-1, :].ravel(), idx[1:, :].ravel()
    rows += [i, j]; cols += [j, i]; vals += [-g, -g]; np.add.at(diag, i, g); np.add.at(diag, j, g)
    c0 = (n - SINK) // 2; s = idx[0, c0:c0 + SINK]; diag[s] += 2 * k[0, c0:c0 + SINK]  # half a cell to the sink face
    A = sp.csr_matrix((np.concatenate(vals + [diag]), (np.concatenate(rows + [np.arange(n * n)]), np.concatenate(cols + [np.arange(n * n)]))), shape=(n * n, n * n))
    return float(spl.spsolve(A.tocsc(), np.ones(n * n)).max())


def read(path):
    lines = [l.strip() for l in open(path) if l.strip()]
    if len(lines) != N or any(len(l) != N or set(l) - set("01") for l in lines): raise ValueError(f"need {N} lines of {N} characters 0/1")
    return np.array([[c == "1" for c in l] for l in lines])  # row 0 is the bottom row (the sink side)


if __name__ == "__main__":
    try: d = read(sys.argv[1])
    except Exception as e: print(json.dumps({"ok": False, "error": str(e)})); sys.exit()
    f = d.mean()
    if f > PHI + 1e-9: print(json.dumps({"ok": False, "fraction": round(f, 4), "error": f"more than {PHI:.0%} of the cells"})); sys.exit()
    t0, t = t_max(np.zeros((N, N), bool)), t_max(d)
    print(json.dumps({"ok": True, "fraction": round(f, 4), "t_max": round(t, 2), "score": round(t0 / t, 3)}))
