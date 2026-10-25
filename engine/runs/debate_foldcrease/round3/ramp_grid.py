"""Balanced-ramp grid at R=5.5 and 7 mm: slope for 20/10 set, phi_g=0, T=4000; keep only sane branches (Rn>R)."""
import sys; sys.dont_write_bytecode=True
from lever3 import solve, crease, zt
for R in (5.5e-3,7e-3):
    rows=[]
    for L1 in (20,22,25,28,30,35):
        for L2 in (6,7,8,9,10,12):
            g=solve(R,L1*1e-3,L2*1e-3)
            if g is None or g['Rn']<R: continue
            d,sl,cv=crease(g,0,4000); d1,sl1,_=crease(g,1e-3,4000)
            rows.append((sl,L1,L2,g,d,d1,sl1))
    rows.sort(key=lambda r:r[0])
    for sl,L1,L2,g,d,d1,sl1 in rows[:8]:
        print(f"R{R*1e3:.1f} {L1}/{L2}: Rn {g['Rn']*1e3:.1f} zone {g['zone']*1e3:.0f} width {g['width']*1e3:.1f} | T4000 phi_g0 {d*1e6:.2f} um {sl*1e3:.4f} mrad | phi_g1e-3 {d1*1e6:.2f} um {sl1*1e3:.4f} mrad")
