"""Radial profile of the outer face surface around each hole (engraved rings = grooves).
Writes results/ring_profiles_<scan>.png and ring_profiles.json (groove radii, widths, depths)."""
import sys, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from common import load_scan_mm, load_json, save_json, RESULTS


def frame(n):
    a = np.array([1.0, 0, 0]) if abs(n[0]) < 0.9 else np.array([0, 1.0, 0])
    e1 = np.cross(n, a); e1 /= np.linalg.norm(e1)
    return e1, np.cross(n, e1)


def profile(m, c, n, h_out, cxy, rmax=15.0, binw=0.15):
    V = m.vertices - c
    Vd = V / np.linalg.norm(V, axis=1)[:, None]
    e1, e2 = frame(n)
    VN = m.vertex_normals
    # outer surface only: outward-facing vertices within 0.9 mm of the outer plane
    sel = (Vd @ n > 0.7) & (VN @ n > 0.3) & (V @ n - h_out > -0.9) & (V @ n - h_out < 0.8)
    P = V[sel]
    rho = np.hypot(P @ e1 - cxy[0], P @ e2 - cxy[1])
    z = P @ n - h_out
    bins = np.arange(0, rmax + binw, binw)
    idx = np.digitize(rho, bins)
    prof = np.full(len(bins) - 1, np.nan)
    for k in range(1, len(bins)):
        zz = z[idx == k]
        if len(zz) >= 3:
            prof[k - 1] = np.median(zz)
    return 0.5 * (bins[1:] + bins[:-1]), prof


def main(name):
    g = load_json(f"scan_geometry_{name}.json")
    m = load_scan_mm(name)
    c = np.asarray(g["centre"]); N = np.asarray(g["normals"])
    fig, axs = plt.subplots(3, 4, figsize=(18, 10), sharey=True)
    out = {}
    for i, n in enumerate(N):
        h = g["holes"][i]
        r, p = profile(m, c, n, g["h_out"][i], h["centre_xy"])
        ok = ~np.isnan(p) & (r > h["d_eq"] / 2 + 0.4) & (r < 13.5)
        rr, pp = r[ok], p[ok]
        # grooves = minima with prominence > 0.05 mm
        pk, prop = find_peaks(-pp, prominence=0.05, width=1)
        grooves = [dict(r=float(rr[k]), depth=float(prop["prominences"][j]),
                        width=float(prop["widths"][j] * 0.15)) for j, k in enumerate(pk)]
        out[i] = dict(hole_r=h["d_eq"] / 2, grooves=grooves)
        ax = axs.flat[i]
        ax.plot(r, p, "k-", lw=1)
        for gg in grooves:
            ax.axvline(gg["r"], color="r", lw=0.6)
        ax.axvline(h["d_eq"] / 2, color="b", lw=0.8)
        ax.set_title(f"{name} face {i}: hole r={h['d_eq']/2:.1f}; grooves at " +
                     ",".join(f"{gg['r']:.1f}" for gg in grooves), fontsize=8)
        ax.set_xlim(4, 15); ax.set_ylim(-1.0, 0.6)
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS, f"ring_profiles_{name}.png"), dpi=60)
    return out


if __name__ == "__main__":
    res = {nm: main(nm) for nm in (sys.argv[1:] or ["saalburg", "hunt"])}
    for nm, d in res.items():
        for i, v in d.items():
            print(nm, i, "hole r %.1f" % v["hole_r"], [(round(x["r"], 1), round(x["depth"], 2), round(x["width"], 2)) for x in v["grooves"]])
    save_json("ring_profiles.json", res)
