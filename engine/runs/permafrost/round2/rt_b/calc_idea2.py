"""Idea 2 repair: self-dosing frozen ore pile (feed = water flow x heat). [S]=sourced, [A]=assumed, [R]=reviewer."""
import numpy as np
rho=1000; cw=4186; g=9.81
E_thaw=101e6  # J per m3 frozen gravel, 30% ice at -5C [R reproduces]; 67-86 MJ at 20-25% ice
# --- R1: debris coat. Spread film (original) vs concentrated toe channel (repair)
def manning_depth(Q,b,S,n):
    lo,hi=1e-4,3
    for _ in range(80):
        h=(lo+hi)/2; A=b*h; P=b+2*h; Qc=A*(A/P)**(2/3)*S**0.5/n
        lo,hi=(h,hi) if Qc<Q else (lo,h)
    return h,A/P,Q/(b*h)
def dmax(tau,theta=0.045): return tau/(theta*1650*g)
for lab,Q,b,S,n in [("original film 47 L/s over 60 m face",0.047,60,0.5,0.03),("toe channel 47 L/s, 0.6 m wide, S=0.05",0.047,0.6,0.05,0.035),
                    ("toe channel 100 L/s, 0.8 m wide, S=0.08",0.10,0.8,0.08,0.035)]:
    h,R,U=manning_depth(Q,b,S,n); tau=rho*g*R*S
    print(f"{lab}: depth {h*1000:.1f} mm, U {U:.2f} m/s, tau {tau:.0f} Pa, clears clasts < {dmax(tau)*1000:.0f} mm")
# heat transfer in channel: q = rho cw St U dT; St 0.002-0.006 (rough bed; Douglas et al. 2023 found rates ~3x smooth theory)
h_,R_,U_=manning_depth(0.047,0.6,0.05,0.035); P=0.6+2*h_
for St in (0.002,0.006):
    hcoef=rho*cw*St*U_; Lefold=rho*cw*0.047/(P*hcoef)
    print(f"St={St}: h={hcoef:.0f} W/m2K, e-folding heat-exchange length {Lefold:.1f} m; local wall retreat at dT=4K: {hcoef*4/E_thaw*86400:.1f} m/day")
# --- R2: water heat. creek temps (defect 3) and solar pond pre-heater
def feed(Q,dT,eta): return Q*86400*rho*cw*dT*eta/E_thaw   # m3/day
print("\nFeed m3/day at Q=47 L/s:")
for T in (2,4,6,8,10):
    print(f" water {T} C: eta 0.7 -> {feed(0.047,T,0.7):5.0f}; eta 0.95 (channel, >3 e-fold lengths) -> {feed(0.047,T,0.95):5.0f}")
# solar pond: June-July daily mean global radiation ~200-230 W/m2 at 62-64N (Susuman/Ust-Nera) [A, typical NASA POWER magnitude]
# net gain of a 0.4 m deep dark-bottom pond held 3-6 K above creek temp, with LW/evap/sensible losses ~40-50% of absorbed [A]
for net in (80,120):
    for dT in (4,6):
        A=0.047*rho*cw*dT/net
        print(f" solar pond raise {dT} K at 47 L/s with net gain {net} W/m2 needs {A/1e4:.2f} ha; volume at 0.4 m {A*0.4:.0f} m3")
# season output: creek 4C + pond +5K = 9C, eta 0.9, 90 days
for Tw in (4,9):
    print(f" season (90 d) at {Tw} C, eta 0.9: {feed(0.047,Tw,0.9)*90:,.0f} m3")
# --- R3: water ratio control (defect 4). Face water ratio = E/(rho cw dT_ext); add fixed bypass to chute
for dTe in (2,4,8,10):
    r=E_thaw/(rho*cw*dTe)
    print(f" dT extracted {dTe} K: face water ratio {r:.1f} m3/m3 -> {'bypass to 4' if r<4 else 'ok (3.2-14 band [S Yukon atlas]; 3 optimal [S kuzstu 2023])'}")
# --- R4: breach hazard (defect 5): Froehlich 1995 peak Qp=0.607 V^0.295 H^1.24
for V,H,lab in [(12000,8,"original forebay"),(4000,1.5,"repair: lined solar pond, 1.5 m embankment, ore pile retains no water")]:
    print(f" {lab}: Qp={0.607*V**0.295*H**1.24:.1f} m3/s")
# --- R5: economics per recovered gram (defect 6). Underground (winter) placer mining total cost [A] $40-80/m3 sands;
# baseline washing-stage cost incl. stockpile thaw, rip, doze-feed, pump, wash: original $6.7 (unsourced) -> range 4-8 [A]
# repaired: no feed dozer, gravity water (intake 300 m upstream at 3% grade = 9 m head), but oversize+tailings stacking remain
grade=0.8; rec=0.9  # g/m3, recovery [A]
for total in (40,80):
    for base_wash,new_wash in ((4.0,2.0),(8.0,3.5)):
        c0=total; c1=total-base_wash+new_wash
        print(f" total {total}$/m3, wash {base_wash}->{new_wash}: $/g {c0/(grade*rec):.1f} -> {c1/(grade*rec):.1f}  ratio {c0/c1:.2f}x")
# oversize at toe: 15% +130 mm [A] of 600 m3/day = 90 m3/day -> loader 0.4 h per 100 m3 [A]
print(" oversize to remove daily (15% of 600 m3):",0.15*600,"m3 -> ~2-3 loader-h/day")
