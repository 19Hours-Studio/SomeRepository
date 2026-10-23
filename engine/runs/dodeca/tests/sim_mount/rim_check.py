"""Rim regularity of every hole on the scans (question: is the unringed pair rubbed, as Duval 1981
p. 200 saw on the Vienne piece?). Rim = the hole contour found by geom_scan.measure(); residual =
radial distance of the contour from its least-squares ellipse. Calibrated on synthetic pieces
(synth.py) with 0.05 / 0.1 mm scan noise, whose rims are perfect.
Run: python rim_check.py > results/rim_check.txt
"""
import numpy as np
from geom_scan import measure, fit_ellipse
from common import load_scan_mm
from synth import build, perturb


def rim_stats(poly):
    x, y = poly[:, 0], poly[:, 1]
    (x0, y0), (A, B), th = fit_ellipse(x, y)
    a, b = A / 2, B / 2
    phi = np.arctan2(y - y0, x - x0) - th
    re = a * b / np.sqrt((b * np.cos(phi)) ** 2 + (a * np.sin(phi)) ** 2)
    res = np.hypot(x - x0, y - y0) - re
    return np.sqrt(np.mean(res ** 2)), res.max() - res.min(), A - B


def report(tag, g, poles=None):
    rows = [(h["face"],) + rim_stats(np.asarray(h["poly"])) for h in g["holes"]]
    if poles is None:
        d = {h["face"]: h["ell_major"] for h in g["holes"]}
        f0 = max(d, key=d.get); poles = (f0, g["opposite"][f0])
    ring = [r for r in rows if r[0] not in poles]; pol = [r for r in rows if r[0] in poles]
    print(f"== {tag}: poles {poles}")
    for r in pol: print(f"   pole face {r[0]}: rim rms {r[1]:.3f} mm, peak-valley {r[2]:.2f} mm, ovality {r[3]:.2f} mm")
    R = np.array([r[1:] for r in ring])
    print(f"   10 ringed: rim rms {R[:,0].mean():.3f} (max {R[:,0].max():.3f}), peak-valley {R[:,1].mean():.2f} "
          f"(max {R[:,1].max():.2f}), ovality {R[:,2].mean():.2f} (max {R[:,2].max():.2f})")
    allr = np.array([r[1] for r in rows]); rank = [int((allr > p[1]).sum()) + 1 for p in pol]
    print(f"   rank of the pole rims by rms among 12 (1 = roughest): {rank}")


HOLES = [23.0, 16.5, 15.2, 19.6, 11.9, 15.9, 11.4, 13.9, 16.2, 24.6, 20.0, 16.4]
for noise in (0.05, 0.1):
    m = build(holes=HOLES, ovals={0: (26.0, 21.5)})
    mp, _ = perturb(m, noise=noise, seed=1, rotate=True)
    report(f"synthetic, perfect rims, noise {noise} mm", measure(mp, verbose=False))
for name in ("saalburg", "hunt"):
    report(f"scan {name}", measure(load_scan_mm(name), verbose=False), poles=(0, 9))
