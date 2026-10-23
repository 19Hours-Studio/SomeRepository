"""Knob-tip wear test on the 3D scans, with a detection-limit calibration on synthetic knobs.

Metric (same code as ../sim_mount/geom_scan.py): sphere fitted to the top 1.2 mm of a knob ("cap")
divided by the sphere fitted to its top 3 mm ("body"). A fresh spherical knob gives ~1; a tip worn
flat by depth delta gives a larger cap radius.
1) calibration: icosphere knobs r = 2.9 mm, edge ~0.3 / 0.45 mm (scan density: Hunt median edge
   0.31 mm), tip flattened by delta = 0 ... 0.5 mm, Gaussian normal noise 0.03 / 0.08 mm, 40 reps.
2) scans: per-knob ratio, and the one-face pattern test (mean ratio of the 5 knobs of each face,
   largest face mean vs 20,000 random reassignments of the ratios to knobs).
Run: python knobs_check.py > knobs_check.txt
"""
import json, os, sys
import numpy as np
import trimesh

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "sim_mount"))
from geom_scan import sphere_fit  # noqa: E402

rng = np.random.default_rng(7)


def knob_ratio(V, vdir):
    P = V[np.degrees(np.arccos(np.clip((V / np.linalg.norm(V, axis=1, keepdims=True)) @ vdir, -1, 1))) < 12]
    rP = P @ vdir; tip = rP.max()
    _, rc, _ = sphere_fit(P[rP > tip - 1.2]); _, rb, _ = sphere_fit(P[rP > tip - 3.0])
    return rc / rb


def synth(r, subdiv, delta, noise, dist=33.0):
    s = trimesh.creation.icosphere(subdivisions=subdiv, radius=r)
    R = trimesh.transformations.random_rotation_matrix(rng.random(3)); s.apply_transform(R)
    V = s.vertices.copy(); n = V / np.linalg.norm(V, axis=1, keepdims=True)
    V = V + n * rng.normal(0, noise, (len(V), 1))
    z = V[:, 2]; cut = r - delta
    if delta > 0: V[z > cut, 2] = cut
    V[:, 2] += dist
    keep = V[:, 2] > dist - r + 0.5  # the knob neck hides the lower part on a real piece
    return V[keep]


print("CALIBRATION (cap/body ratio, mean +- sd over 40 synthetic knobs)")
calib = {}
for subdiv, edge in ((5, 0.18), (4, 0.36)):
    for noise in (0.03, 0.08):
        row = []
        for delta in (0.0, 0.05, 0.1, 0.15, 0.2, 0.3, 0.5):
            x = np.array([knob_ratio(synth(2.9, subdiv, delta, noise), np.array([0, 0, 1.0])) for _ in range(40)])
            calib[(edge, noise, delta)] = (x.mean(), x.std()); row.append(f"d={delta:.2f}:{x.mean():.2f}+-{x.std():.2f}")
        print(f" edge~{edge}mm noise {noise}mm  " + "  ".join(row))

print("\nSCANS")
for name in ("saalburg", "hunt"):
    g = json.load(open(os.path.join(HERE, "..", "sim_mount", "results", f"scan_geometry_{name}.json")))
    K = g["knobs"]; ratio = np.array([k["cap_radius"] / k["body_radius"] for k in K])
    faces = [set(k["faces"]) for k in K]
    fm = np.array([ratio[[j for j in range(20) if f in faces[j]]].mean() for f in range(12)])
    obs = fm.max() - ratio.mean()
    sims = []
    for _ in range(20000):
        r = rng.permutation(ratio)
        sims.append(max(r[[j for j in range(20) if f in faces[j]]].mean() for f in range(12)) - r.mean())
    p = (np.array(sims) >= obs - 1e-12).mean()
    print(f"== {name}: per-knob ratio mean {ratio.mean():.2f} sd {ratio.std():.2f} min {ratio.min():.2f} max {ratio.max():.2f}")
    print(f"   knobs with ratio > 1.15: {int((ratio > 1.15).sum())} of 20; sorted: {np.round(np.sort(ratio), 2).tolist()}")
    print(f"   one-face pattern: face means {np.round(fm, 2).tolist()}; max face {int(fm.argmax())} "
          f"excess {obs:.3f}, P(random >=) = {p:.3f}")
