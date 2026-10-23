"""Summarise throw results: face frequencies (chi-square vs uniform), pole faces, behaviour, and the
per-knob contact map (predicted wear). Note: MuJoCo's plane-convex collision reports at most 4
contact points, so 'knobs touching at rest' is not counted; the top-face tilt is used instead.
Usage: python summarise.py results/<file>.json [...]  (pole faces 0 and 9 for both scans)
"""
import json, sys
import numpy as np
from scipy.stats import chisquare

for f in sys.argv[1:]:
    r = json.load(open(f))
    nf = 6 if "cube" in f else 12
    top = np.array([x["top"] for x in r])
    cnt = np.bincount(top, minlength=nf)
    chi = chisquare(cnt)
    t = np.array([x["t"] for x in r])
    tilt = np.array([x["tilt"] for x in r])
    b = np.array([x["bounces"] for x in r])
    tr = np.array([x["travel"] for x in r])
    ev = np.array([x["events"] for x in r]).sum(0)
    im = np.array([x["impulse"] for x in r]).sum(0)
    print(f"== {f.split('/')[-1]}  n={len(r)}")
    print(f"   faces up: {cnt.tolist()}  chi2={chi.statistic:.1f} p={chi.pvalue:.3f}  (expected {len(r)/nf:.0f} each)")
    if nf == 12:
        pole = cnt[0] + cnt[9]
        print(f"   pole faces 0+9 up: {pole} = {pole/len(r):.3f} (fair 2/12 = 0.167)")
    print(f"   came to rest: {np.mean(t < 7.99):.3f}; time to rest median {np.median(t):.2f} s; bounces median "
          f"{np.median(b):.0f}; travel median {np.median(tr)*100:.1f} cm (p90 {np.percentile(tr,90)*100:.1f})")
    print(f"   top-face tilt at rest: median {np.median(tilt):.2f} deg, p95 {np.percentile(tilt,95):.2f}, "
          f"share > 3 deg {np.mean(tilt > 3):.3f}")
    print(f"   knob contacts per throw {ev.sum()/len(r):.1f}; per knob max/min = {ev.max()/ev.min():.2f} "
          f"(CV {ev.std()/ev.mean():.3f}); impulse max/min = {im.max()/im.min():.2f} (CV {im.std()/im.mean():.3f})")
