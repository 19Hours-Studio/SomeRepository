import numpy as np
from crease import teardrop_profile, solve, metrics, residual_kr
from study1 import smooth, run as run_lin
# same calibration as study1 (eps_c=0.003, base 150 um at R=2, linear model)
d_unit=run_lin(2.0,1.0,0)['depth_um']; c2=150/d_unit; phi=c2/residual_kr(2.0,1.0,0.003); c3=residual_kr(3.0,phi,0.003)
for sm in [0,2.0]:
  for T in [0,1000,2000,3150]:
    x,k=teardrop_profile(3.0,n=260); k=smooth(x,k,sm)
    for sign in [+1,-1]:
      w,s,cu=solve(x,sign*c3*k,T,contact=True); m=metrics(x,w,s,cu)
      print(f"contact sm={sm} T={T} sign={sign:+d}: depth {m['depth_um']:.2f} slope {m['slope_mrad']:.2f} curv {m['curv_inv_m']:.2f}")
