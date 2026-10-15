"""Checks for Ideas 3, 8, 10 (under-ice ore pods)."""
import math

RHO_W, RHO_I = 1000.0, 917.0
NET_ICE = RHO_W - RHO_I  # kg buoyancy per m3 of ice
L_VOL = 334e3 * RHO_I

print("=== IDEA 3 ===")
# pod 5.0 x 2.2 x 1.2 m
a, b, c = 5.0, 2.2, 1.2
V = a * b * c
A = 2 * (a * b + a * c + b * c)
print(f"pod volume {V:.1f} m3, surface {A:.1f} m2")
melt = 0.06
dB = A * melt * NET_ICE
print(f"6 cm shell melt (idea's own) -> buoyancy loss {dB:.0f} kg over 45 d = {dB/45:.1f} kg/day")
for B0 in (3, 9):
    print(f"  trim +{B0} kg reaches 0 after {B0/(dB/45):.1f} days")
# transit time vs velocity
for days in (41, 68):
    v = 700e3 / (days * 86400)
    print(f"700 km in {days} d -> mean pod speed {v:.3f} m/s")
# shell melt over 68 days at idea's own rate
for days in (41, 68):
    print(f"melt over {days} d at 6 cm/45 d: {6*days/45:.1f} cm vs 8-10 cm shell")
# drag at 0.16 m/s broadside
for Cd in (1.2, 2.0):
    for Afr in (a * c, b * c):
        F = 0.5 * RHO_W * Cd * Afr * 0.16 ** 2
        print(f"drag Cd={Cd} A={Afr:.1f} m2 at 0.16 m/s: {F:.0f} N")
# friction of buoyancy window
for B in (3, 9):
    print(f"friction mu 0.5 x {B} kg = {0.5*B*9.81:.0f} N")
# implied snow density for 0.28, 0.74, 0.86 m3/t
for name, rho_s, vs in (("coal", 1350, 0.28), ("rock", 2700, 0.74), ("sulphide", 4200, 0.86)):
    excess = 1000 - 1000 * RHO_W / rho_s
    print(f"{name}: excess weight {excess:.0f} kg/t; snow {vs} m3/t -> needs net lift {excess/vs:.0f} kg/m3 -> snow density {RHO_W-excess/vs:.0f} kg/m3 (no shell credit)")
# throughput
pods = 1200 / 10
print(f"1,200 t/day in 10 t pods = {pods:.0f} pods/day = {pods/24:.1f}/h; 144 kt / 1.2 kt/d = {144/1.2:.0f} days")
# load-cell accuracy: 0.1 % of 10 t capacity
print("crane load cell 0.1% FS on 10 t =", 0.001 * 10000, "kg ; 0.05% FS =", 0.0005 * 10000, "kg vs 6 kg window")
# water density variation: 0 C vs 4 C (999.84 vs 999.97) over pod volume
print("density change 0->4 C over pod volume:", (999.97 - 999.84) * V, "kg")
# suspended sediment 50 g/m3 -> density +0.031 kg/m3
print("sediment 50 g/m3 changes buoyancy by", 0.05 * (1 - 1 / 2.65) * V, "kg")
# ice shell plate bending under 1 m water head differential
for t in (0.08, 0.10):
    p = 9810 * 1.0
    span = 2.2
    sigma = 0.75 * p * (span / t) ** 2 / 1e6 * 0.5  # long plate, fixed edges approx 0.5*0.75 (beta ~0.5)
    print(f"ice shell t={t} m, span 2.2 m, 10 kPa: bending stress ~{sigma:.1f} MPa vs ice flexural strength ~0.5-1 MPa")
# lost pod value
for name, val in (("coal", 60), ("rock ore concentrate-grade", 300), ("sulphide ore", 150)):
    print(f"5% loss of {name} worth ${val}/t = ${0.05*val:.1f}/t")

print("\n=== IDEA 8 ===")
# cold reserve
for T in (-4, -25):
    Q = 8000 * 1.3e3 * (-T)
    ice_m3 = Q / L_VOL
    print(f"8 t coal at {T} C: freezes {ice_m3:.3f} m3 ice -> +{ice_m3*NET_ICE:.0f} kg")
# loss rates vs dT using heat-transfer coefficient inferred
# 3.7 kg/day at 0.01 K -> melt volume per day
for rate, dT in ((3.7, 0.01), (11, 0.03), (18.4, 0.05)):
    melt_m3 = rate / NET_ICE
    print(f"{rate} kg/d at +{dT} K -> melt {melt_m3:.3f} m3/day of ice")
# pod geometry: 8 t coal flooded voids + 1.76 m3 snow pocket, 1.2 m tall
coal_bulk = 8 / 0.85
vol = coal_bulk + 1.76
print(f"cargo volume {vol:.1f} m3 -> footprint at 1.2 m height (interior ~1.0 m) ~{vol/1.0:.1f} m2")
# trip length
for v in (0.18, 0.25, 0.33):
    kmd = v * 86.4
    for rate in (3.7, 11, 18.4):
        for win in (90, 404):
            print(f"v={v} rate={rate} window={win}: {win/rate:.1f} d -> {win/rate*kmd:.0f} km")
# Zyryanka-Srednekolymsk 330 km
for v in (0.18, 0.33):
    d = 330 / (v * 86.4)
    print(f"330 km at {v} m/s: {d:.1f} days; loss at 3.7/11/18.4 kg/d = {3.7*d:.0f}/{11*d:.0f}/{18.4*d:.0f} kg vs 90 kg window")
# winter road per t-km
print("winter road $39/t / 330 km =", 39 / 330, "$/t-km;  idea 3 $59-176 over 500-1500 km:", 59 / 500, 176 / 1500)
print("idea 10: $124/t at 0.118 $/t-km ->", 124 / 0.118, "km")
# flow area / depth under ice at 327 m3/s
for v in (0.18, 0.33):
    Aflow = 327 / v
    for W in (400, 700, 1000):
        print(f"Q=327 v={v}: flow area {Aflow:.0f} m2, width {W} m -> mean under-ice depth {Aflow/W:.2f} m")
# drag needed for 90 & 404 kg window at mu=0.15
for win in (90, 404):
    print(f"window {win} kg at mu 0.15 -> drag {0.15*win*9.81:.0f} N")

print("\n=== IDEA 10 ===")
T1, T2 = 273.15 - 35, 273.15
p = 101.325 * (T2 / T1)
print(f"sealed at -35 C, warmed to 0 C: {p:.1f} kPa abs -> +{p-101.325:.1f} kPa")
# external pressure at pod centre: ice draft + radius
for ice in (0.6, 1.0, 1.5):
    z = ice * 0.917 + 0.8
    print(f"ice {ice} m: log centre depth {z:.2f} m -> hydrostatic +{9.81*z:.1f} kPa; bottom {9.81*(z+0.8):.1f} kPa")
# thermal shock stress ice -35 -> 0
E, alpha, nu = 9e9, 5.1e-5, 0.33
for dT in (5, 16, 35):
    sig = E * alpha * dT / (1 - nu) / 1e6
    print(f"thermal stress dT={dT} K: {sig:.1f} MPa (ice tensile ~1-2 MPa; King&Fletcher median crack at -16 C)")
# Vionnet 2012 viscosity
def eta(rho, T=0.0):
    eta0, a_eta, b_eta, c_eta = 7.62237e6, 0.1, 0.023, 250.0
    return eta0 * (rho / c_eta) * math.exp(a_eta * (0 - T) + b_eta * rho)
for rho in (250, 350, 550):
    for sig in (2e3, 15e3):
        rate = sig / eta(rho)
        print(f"snow {rho} kg/m3, stress {sig/1e3:.0f} kPa: eta {eta(rho):.2e} Pa s, strain/day {rate*86400:.4f}, per 45 d {rate*86400*45:.3f}")
# snow volumes per tonne at 550
for name, rho_s, stated in (("coal", 1350, 0.74), ("rock", 2700, 1.6)):
    excess = 1000 - 1000 * RHO_W / rho_s
    print(f"{name}: {excess/(1000-550):.2f} m3/t snow without shell (stated {stated})")
