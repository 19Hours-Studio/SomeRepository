"""Why the scanned pieces are loaded dice: face-down frequency vs the centre-of-mass offset along
each face normal, plus the predicted knob-wear map (share of summed contact impulse per knob).
Run: python bias_check.py > results/bias_check.txt
"""
import json, os
import numpy as np
from scipy.stats import spearmanr
import throw

HERE = os.path.dirname(os.path.abspath(__file__))
out = {}
for name in ("saalburg", "hunt"):
    V, m, com, I, N, K, holes = throw.body_def(name)
    r = json.load(open(os.path.join(HERE, "results", f"{name}_cloth_toss_2400_0.0005.json")))
    g = json.load(open(os.path.join(HERE, "..", "sim_mount", "results", f"scan_geometry_{name}.json")))
    opp = g["opposite"]
    up = np.bincount([x["top"] for x in r], minlength=12) / len(r)
    down = np.array([up[opp[f]] for f in range(12)])
    proj = N @ com * 1000  # mm, COM offset toward each face
    rho, p = spearmanr(proj, down)
    print(f"== {name}: mass {m*1000:.0f} g (8.7 g/cm3 assumed), COM offset {np.linalg.norm(com)*1000:.2f} mm")
    print("   face: hole mm | P(down) | COM offset toward face (mm)")
    for f in np.argsort(-down):
        print(f"   {f:2d}: {holes[f]:5.1f} | {down[f]:.3f} | {proj[f]:+.3f}")
    print(f"   Spearman(COM offset toward face, P(face down)) = {rho:.2f}, p = {p:.4f}")
    rh, ph = spearmanr([holes[f] for f in range(12)], down)
    print(f"   Spearman(hole size, P(face down)) = {rh:.2f}, p = {ph:.4f}")
    imp = {}
    for s in ("cloth", "wood", "earth"):
        rr = json.load(open(os.path.join(HERE, "results", f"{name}_{s}_toss_2400_0.0005.json")))
        a = np.array([x["impulse"] for x in rr]).sum(0); imp[s] = a / a.sum()
    rs = spearmanr(imp["cloth"], imp["wood"])[0]
    print(f"   knob impulse share (cloth): min {imp['cloth'].min():.3f} max {imp['cloth'].max():.3f} "
          f"(even = 0.050); rank agreement cloth vs wood rho = {rs:.2f}")
    out[name] = dict(face_down=down.tolist(), com_offset_mm=proj.tolist(),
                     knob_impulse_share={k: v.tolist() for k, v in imp.items()})
json.dump(out, open(os.path.join(HERE, "results", "wear_prediction.json"), "w"), indent=1)
