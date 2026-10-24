import numpy as np
from crease import *
TARGET_D, TARGET_S = 5.0, 1.0      # um, mrad  (invisibility targets, see NOTES)
def run(R, c, T, contact=True, neck_ratio=3.0):
    x,k=teardrop_profile(R,n=500,neck_ratio=neck_ratio); w,s,cu=solve(x,c*k,T,contact=contact); return metrics(x,w,s,cu)
# 1. calibrate: today's phone R=2 mm, no tension, baseline crease 60..150 um (FACT4 'good'<60; reviewers still see Fold creases)
for eps_c in [0.003,0.005]:
  for base in [60,150]:
    lo,hi=1e-3,5.0
    for _ in range(40):
        phi=np.sqrt(lo*hi); c=residual_kr(2.0,phi,eps_c)
        d=run(2.0,c,0)['depth_um']; lo,hi=(phi,hi) if d<base else (lo,phi)
    c2=residual_kr(2.0,phi,eps_c); c3=residual_kr(3.0,phi,eps_c)
    m3=run(3.0,c3,0)
    print(f"eps_c={eps_c:.3f} base@R2={base}um -> phi={phi:.3f} c(R2)={c2:.4f} c(R3)={c3:.4f}  R3 untensioned {m3}")
    for T in [300,1000,2000,3150,5000]:
        m=run(3.0,c3,T); print(f"     T={T:5d} N/m  depth {m['depth_um']:6.2f} um  slope {m['slope_mrad']:5.2f} mrad  curv {m['curv_inv_m']:.2f} 1/m")
