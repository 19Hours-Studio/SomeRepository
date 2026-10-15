"""Idea 3 repair: freeze-and-float of OVERSIZE boulders (>1.2 m) left standing on the mined pit floor;
ice never reaches the floor (gap), boulder tops freeze into the floe, spring snowmelt rise lifts. [S]/[A]/[R] tags."""
import numpy as np
from math import erf,sqrt,pi
rw,ri,rs=1000,917,2650
Phi=lambda z:0.5*(1+erf(z/sqrt(2)))
# R1: lift capacity per m2 at spring (top melt 0.3 m [R], slush 10-20 kg/m2 after plowing [A] vs 40-120 unplowed [R])
for h0 in (1.7,2.0):
    for melt,load in ((0.3,15),(0.3,120)):
        lift=(rw-ri)*(h0-melt)-load
        print(f"ice {h0} m, melt {melt}, load {load} kg/m2: net lift {lift:.0f} kg/m2 = {max(lift,0)/(rs-rw):.3f} m3 stone/m2")
# boulder (sphere-equivalent) needs floe area:
for D in (1.2,1.5,2.0,2.5):
    V=pi/6*D**3; Wsub=V*(rs-rw); 
    for lift in (95,140):
        A=Wsub/lift
        print(f"boulder D={D} m: V={V:.2f} m3, submerged {Wsub/1000:.1f} t, floe area needed {A:.0f} m2 at {lift} kg/m2 (spacing {sqrt(A):.1f} m)")
# grip: adfreeze on embedded cap (embed e=0.2-0.3 m); adfreeze near 0 C 0.05-0.1 MPa [A: lower range of published 0.1-1 MPa]
for D in (1.5,2.5):
    V=pi/6*D**3; W=V*(rs-rw)*9.81
    for e in (0.2,0.3):
        cap=2*pi*(D/2)*e
        for tau in (0.05e6,0.1e6):
            print(f"D={D} e={e} tau={tau/1e6} MPa: grip {cap*tau/1e3:.0f} kN vs weight {W/1e3:.0f} kN -> margin {cap*tau/W:.1f}x")
# R2: timing/reliability. plowed ice: mean 1.8 m, sigma 0.08 (FDD only [R 0.07-0.10]); unplowed sigma 0.10-0.25 [R]
for mu,sd,lab in ((1.8,0.08,"plowed"),(1.7,0.20,"unplowed")):
    depth=0.917*(mu+2.33*sd)+0.3   # ice BOTTOM (draft 0.917h) stays >=0.3 m above floor in 99% of winters
    for Hb in (1.2,1.5,2.0):
        # gripped (>=0.2 m embedment) if draft > depth-(Hb-0.2)
        p=1-Phi(((depth-(Hb-0.2))/0.917-mu)/sd)
        print(f"{lab}: water depth {depth:.2f} m; boulder protruding {Hb} m gripped with P={p:.3f}; floor-freeze P=0.01")
# R3: number of winters to clear (defect 5 -> now clean-up of oversize left after the gravel is mined, not pre-mining clearing)
# R4: economics. oversize >1.2 m share of pay volume 1-5% [A]; secondary blasting+doze of oversize $4-8/m3 boulder [A, orig $6]
# ice method per m3 boulder: plow ice (~$0.03/m2) + snowmelt routing + winch floe (~2 h per floe, 1 floe per 3 boulders) [A]
for share in (0.01,0.05):
    for blast,ice in ((4,2.0),(8,2.5)):
        save=share*(blast-ice)
        print(f"oversize {share:.0%}: saving ${save:.3f} per m3 pay; vs total surface placer cost $11-48/m3 [S BLM Koyukuk $4.23-18.43/lcy 1990s x ~2 CPI] -> {save/48:.2%}-{save/11:.2%}")
# NPV of the delay: only pay under boulders (assume 5% of pay) waits 1 year at 15%
print("NPV loss from 1-yr delay of 5% of pay at 15%:", round(0.05*(1-1/1.15)*100,2),"% of project NPV")
# breach: pond is in the mined-out pit below grade -> no retaining embankment; volume per sector e.g. 50x100x2.4 m
print("sector pond volume",50*100*2.4,"m3, below grade -> no dam-break peak")
