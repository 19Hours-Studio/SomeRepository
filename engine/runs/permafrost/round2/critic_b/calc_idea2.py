"""Idea 2 - Self-feeding ore-ice buttress dam."""
import math

Lf = 334e3; rho_w = 1000.0; cw = 4186.0
print("== 1. Heat to release 1 m3 of ice-cemented gravel ==")
for ice_frac, T0 in ((0.30, -5.0), (0.30, -2.0), (0.25, -5.0), (0.20, -3.0)):
    m_ice = ice_frac * 917
    solids = (1 - ice_frac) * 2650
    q = m_ice * Lf + (solids * 750 + m_ice * 2100) * (-T0)
    print(f" ice {ice_frac:.2f} vol, T0={T0}: {q/1e6:.0f} MJ/m3")
q = 101e6
for w in (4.3, 7.6):
    print(f" {w} m3 of water per m3 -> water must cool by {q/(w*rho_w*cw):.2f} K (from 8 C to {8-q/(w*rho_w*cw):.2f} C)")
print(" if 8 C water fully cooled to 0.5 C: %.2f m3 per m3" % (q / (rho_w*cw*7.5)))
# sluice water ratio, Yukon data: 1000-1100 US gal/yd3 ; Ross plants 1400-2900
for gal in (650, 1050, 2000, 2900):
    print(f" {gal} US gal/yd3 = {gal*3.785e-3/0.7646:.1f} m3 water per m3 gravel")

print("\n== 2. Rate x duration ==")
Q = 0.047  # m3/s
day = 86400
print(" baseflow per day = %.0f m3" % (Q*day))
for w in (4.3, 6.3, 7.6):
    print(f" 60,000 m3 at {w} m3/m3 needs {60000*w:,.0f} m3 water = {60000*w/(Q*day):.0f} days of 47 L/s")
print(" buttress: 75 m / 0.8 m/day = %.0f days" % (75/0.8))
print(" daily feed = %.0f m3 -> face area = %.0f m2" % (60000/(75/0.8), 60000/75))
P_need = 60000/(75/0.8) * q / day
print(" heat needed = %.0f kW; required water cooling at 47 L/s = %.2f K" % (P_need/1e3, P_need/(Q*rho_w*cw)))
print(" face heat flux needed = %.0f W/m2" % (0.8*q/day))
# feed sensitivity to water temperature (outlet ~0.5 C)
for Tw in (2, 4, 6, 8, 10):
    feed = Q*rho_w*cw*max(Tw-0.5,0)*day/q
    print(f"  creek water {Tw} C -> feed {feed:.0f} m3/day ; water:solids {Q*day/feed if feed>0 else float('inf'):.1f}")

print("\n== 3. Face film hydraulics and debris armour ==")
width = 100.0  # m (800 m2 face / 8 m high)
q_unit = Q / width
nu = 1.8e-6
for slope_deg in (35, 60):
    s = math.sin(math.radians(slope_deg))
    delta = (3*nu*q_unit/(9.81*s))**(1/3)
    tau = rho_w*9.81*delta*s
    dmax = tau / (0.045*1650*9.81)
    print(f" slope {slope_deg} deg: film {delta*1000:.2f} mm, bed shear {tau:.1f} Pa, largest movable clast {dmax*1000:.1f} mm")
# conduction through a thawed debris coat
k_th = 2.0
for dT in (4.0, 7.5):
    dmax = k_th*dT/(0.8*q/day)
    print(f" debris coat limiting thickness for 0.8 m/day with dT={dT}: {dmax*100:.1f} cm")
for coat_cm in (5, 10, 20):
    flux = k_th*6.0/(coat_cm/100)
    print(f"  coat {coat_cm} cm -> flux {flux:.0f} W/m2 -> retreat {flux*day/q:.3f} m/day")

print("\n== 4. Seepage through an un-iced hoisted stockpile ==")
H = 8.0; L = 75.0; A = 800.0
for K in (1e-3, 1e-2, 1e-1):
    print(f" K={K:g} m/s: seepage {K*H/L*A:.2f} m3/s vs creek 0.047 m3/s")
# water to ice-saturate the pile in winter
for voids in (0.30, 0.40):
    print(f" ice-saturating 60,000 m3 with void {voids:.2f}: {60000*voids*0.9:,.0f} m3 of winter water (creeks frozen)")

print("\n== 5. Dam break (Froehlich 1995: Qp = 0.607 V^0.295 H^1.24) ==")
for Qp in (460.0, 128.0):
    for Hh in (5.0, 8.0, 10.0):
        V = (Qp/(0.607*Hh**1.24))**(1/0.295)
        print(f" Qp={Qp} m3/s, H={Hh} m -> implied stored volume {V:,.0f} m3")
print(" 128 m3/s / 0.047 m3/s baseflow = %.0f x" % (128/0.047))

print("\n== 6. Peat cover thaw (Stefan) ==")
k_peat = 0.5
for wfrac in (0.80, 0.90):
    Lv = wfrac*1000*Lf
    for TDD in (800, 1000, 1400):
        X = math.sqrt(2*k_peat*TDD*86400/Lv)
        print(f" peat water {wfrac}, thaw degree-days {TDD}: {X:.2f} m")
