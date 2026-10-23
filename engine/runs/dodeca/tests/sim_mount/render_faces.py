"""Shaded orthographic view of each of the 12 faces (geometry only, raking light), to check
which holes carry engraved rings. Writes results/faces_<scan>.png."""
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from common import load_scan_mm, load_json, RESULTS
import os


def frame(n):
    a = np.array([1.0, 0, 0]) if abs(n[0]) < 0.9 else np.array([0, 1.0, 0])
    e1 = np.cross(n, a); e1 /= np.linalg.norm(e1)
    return e1, np.cross(n, e1)


def main(name):
    g = load_json(f"scan_geometry_{name}.json")
    m = load_scan_mm(name)
    c = np.asarray(g["centre"]); N = np.asarray(g["normals"])
    V = m.vertices - c; F = m.faces
    cen = V[F].mean(1)
    fn = m.face_normals
    cd = cen / np.linalg.norm(cen, axis=1)[:, None]
    fig, axs = plt.subplots(3, 4, figsize=(16, 12))
    for i, n in enumerate(N):
        ax = axs.flat[i]; e1, e2 = frame(n)
        light = 0.5 * n + 0.85 * e1; light /= np.linalg.norm(light)
        sel = np.where((cd @ n > 0.6) & (fn @ n > 0.0))[0]
        sel = sel[np.argsort(cen[sel] @ n)]
        polys = np.stack([V[F[sel]] @ e1, V[F[sel]] @ e2], -1)
        shade = np.clip(fn[sel] @ light, 0, 1)
        ax.add_collection(PolyCollection(polys, facecolors=plt.cm.gray(shade), edgecolors="none",
                                         linewidths=0, antialiased=False))
        h = g["holes"][i]
        ax.set_xlim(-25, 25); ax.set_ylim(-25, 25); ax.set_aspect("equal")
        ax.set_title(f"{name} face {i} (opp {g['opposite'][i]}): hole {h['d_mic']:.1f} mm")
    plt.tight_layout()
    out = os.path.join(RESULTS, f"faces_{name}.png")
    plt.savefig(out, dpi=60)
    print(out)


if __name__ == "__main__":
    for nm in (sys.argv[1:] or ["saalburg", "hunt"]):
        main(nm)
