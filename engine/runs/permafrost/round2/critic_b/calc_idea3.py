"""Idea 3 - Freeze-and-float boulder pond."""
import math
rho_w, rho_i, rho_s = 1000.0, 917.0, 2650.0
dB_ice = rho_w - rho_i          # excess buoyancy per m3 ice
dW_st = rho_s - rho_w           # submerged weight per m3 stone
print("== 1. Lift capacity (neutral buoyancy, zero freeboard) ==")
for h in (1.6, 1.8, 3.1, 3.3):
    print(f" ice {h} m: max stone {dB_ice*h/dW_st:.3f} m3/m2 (claim 0.08-0.17)")
print(" ratio stone/ice volume at neutral buoyancy = %.4f" % (dB_ice/dW_st))

print("\n== 2. Same capacity after realistic spring loads ==")
for h in (1.7, 3.2):
    for snow in (0.0, 40.0, 80.0, 120.0):          # kg/m2 snow or slush on floe
        for topmelt in (0.0, 0.3):                  # m of top melt before the rise
            cap = (dB_ice*(h-topmelt) - snow)/dW_st
            print(f" ice {h} m, snow {snow:3.0f} kg/m2, top melt {topmelt} m -> {max(cap,0):.3f} m3/m2")

print("\n== 3. Freeze-in of the bed after the ice touches boulder tops ==")
# Stefan growth: h^2 = a2 * FDD_eff ; a2 = 2 k_i /(rho_i L) per C-day
k_i, L = 2.2, 334e3
a2 = 2*k_i/(rho_i*L)*86400
print(" a2 = %.2e m2/(C day)" % a2)
for h0 in (1.7,):
    for fdd_day, days, snow_factor in ((20, 30, 0.5), (12, 30, 0.5), (20, 45, 0.6)):
        # ice growth rate dh/dt = a2*FDD/(2h)*snow_factor (snow insulation reduces)
        dh = a2*fdd_day*snow_factor/(2*h0)*days
        # in saturated gravel with porosity n the latent heat per m is n times that of ice -> front moves ~1/n faster, minus talik heat (take 50%)
        for n in (0.30,):
            bed = dh/n*0.5
            solids = bed*(1-n)
            print(f" FDD {fdd_day}/day x {days} d, snow factor {snow_factor}: equivalent ice growth {dh*100:.0f} cm -> bed frozen ~{bed*100:.0f} cm -> {solids:.3f} m3/m2 solids (lift cap 0.08)")

print("\n== 4. Interannual ice-thickness scatter vs the 'touch in March' window ==")
# window: ice reaching tops between ~Mar 1 and Mar 31 => thickness band = growth in March
h_mar1 = 1.55; h_mar31 = 1.70   # natural ice growing ~0.15 m in March under snow
band = h_mar31 - h_mar1
from math import erf, sqrt
def P_in(sig):
    z = band/2/sig
    return erf(z/sqrt(2))
for sig in (0.10, 0.15, 0.20, 0.25):
    print(f" interannual sigma of max ice {sig} m: P(touch in March) = {P_in(sig):.2f}; P(touch before Mar = grounded) = {(1-P_in(sig))/2:.2f}; P(never touches) = {(1-P_in(sig))/2:.2f}")
# Stefan sensitivity: h ~ sqrt(FDD) and snow
for cv_fdd in (0.08, 0.12):
    print(f" FDD CV {cv_fdd:.0%} alone -> ice CV {cv_fdd/2:.0%} -> sigma {1.7*cv_fdd/2:.2f} m (snow-depth variability adds to this)")

print("\n== 5. Wave orbital velocity (stated 0.03 m/s at 1 m) ==")
Hs, T = 0.1, 1.2
Lw = 9.81*T**2/(2*math.pi)
k = 2*math.pi/Lw
ub = math.pi*Hs/(T*math.sinh(k*1.0))
print(f" Hs {Hs} m T {T} s: L {Lw:.2f} m, u_bottom(1 m) = {ub:.3f} m/s")

print("\n== 6. Years of ponding to clear a bouldery pay ==")
for pay, bfrac in ((2.0, 0.15), (2.0, 0.25), (3.0, 0.25)):
    vol = pay*bfrac
    for cap in (0.04, 0.08, 0.17):
        print(f" pay {pay} m, boulders {bfrac:.0%} -> {vol:.2f} m3/m2; at {cap} m3/m2/yr -> {vol/cap:.1f} years")
for yrs in (3, 5):
    for r in (0.10, 0.15):
        print(f" {yrs}-year delay at {r:.0%} discount: PV factor {1/(1+r)**yrs:.2f}")

print("\n== 7. Pond thaw beneath water (Stefan) ==")
for k_t, n in ((2.0, 0.30),):
    for wdd in (600, 1000, 1500):
        X = math.sqrt(2*k_t*wdd*86400/(n*rho_w*L))
        print(f" bed degree-days {wdd}: thaw {X:.2f} m")

print("\n== 8. Floe mass to winch ==")
for side in (10, 20):
    A = side*side
    m = A*(1.7*917 + 0.085*2650)
    print(f" {side}x{side} m floe at 1.7 m with 0.085 m3/m2 stone: {m/1000:.0f} t")
