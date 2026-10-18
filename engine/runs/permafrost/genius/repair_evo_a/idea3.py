"""Idea 3 - Barge highwall coal augers into frozen river-bluff seams.
Sources: scroll-auger patent US6293628 (30-in auger ~10 ft/min ~118 t/h); auger depth typ. 55-67 m,
BryDet 1.83 m single-flight to ~244 m; auger recovery ~35-50 % (CDC/NIOSH, Mae Tan case).
[est] = engineering estimate.
"""
import numpy as np
print("=== IDEA 3: barge highwall augers ===")
rho_c = 1.30   # t/m3 bituminous (Zyryanka-type hard coal); brown coal ~1.2
# --- production: cycle per hole (frozen coal -> slow cutting assumed) ---
def hole_cycle(D=1.8, L=100.0, pen=0.3, flight=6.0, add_min=8, pull_min=5, move_h=1.0):
    t_cut = L / pen / 60
    n = L / flight
    t = t_cut + n * add_min / 60 + n * pull_min / 60 + move_h
    tons = np.pi / 4 * D**2 * L * rho_c
    return tons, t
for pen in (0.3, 0.6, 1.0):
    tons, t = hole_cycle(pen=pen)
    print(f"1.8 m x 100 m hole: {tons:.0f} t, cycle {t:.1f} h at {pen} m/min -> {tons/t:.0f} t/h average")
tons, t = hole_cycle(pen=0.3)
need = 20000
print(f"20 kt season -> {need/tons:.0f} holes, {need/tons*t/24:.0f} days at 24 h; "
      f"bluff length {need/tons*2.4:.0f} m (1.8 m holes + 0.6 m webs)")
# 30-in reference: 10 ft/min ~118 t/h  ->  cutting is not limiting; flight handling dominates

# --- web pillar check (Mark-Bieniawski, in-situ coal strength S1 ~6 MPa unfrozen; frozen > 2x) ---
D, w, hseam = 1.8, 0.6, 2.2
for cover in (15, 30, 50):
    sv = 0.024 * cover
    sp = sv * (D + w) / w
    S = 6.0 * (0.64 + 0.36 * w / hseam)
    print(f" cover {cover} m: web stress {sp:.1f} MPa vs unfrozen strength {S:.1f} MPa (FoS {S/sp:.1f}); frozen FoS > {2*S/sp:.1f}")

# --- thrust reaction: spuds vs permafrost adfreeze anchors ---
thrust = 300e3   # N  [est for 1.8 m auger, 100 m string]
# adfreeze long-term ~100-150 kPa (Andersland & Ladanyi, steel in frozen ground at -3 C)
for tau in (100e3, 150e3):
    anchor = tau * np.pi * 0.15 * 6.0
    print(f" one 150 mm x 6 m frozen-ground anchor at {tau/1e3:.0f} kPa: {anchor/1e3:.0f} kN -> "
          f"{int(np.ceil(thrust/anchor))} anchors for {thrust/1e3:.0f} kN")
# spud (Broms, free-head, gravel phi=35 deg, embed 3 m, D 0.6 m) with lever arm reduces to ~1/3
Kp = np.tan(np.radians(45 + 35/2))**2
Pu = 0.5 * 3 * Kp * 10e3 * 0.6 * 3**2
print(f" one spud ultimate ~{Pu/1e3:.0f} kN, with 4 m lever ~{Pu/3/1e3:.0f} kN usable")

# --- recovery ---
rec_panel = (np.pi / 4 * D**2) / ((D + w) * hseam)
print(f"panel recovery (2.2 m seam) {rec_panel*100:.0f} %")

# --- water-level window: auger frame adjustable +/-3 m; stage fall after June flood ~5-10 cm/day [est]
for fall in (0.05, 0.10):
    print(f" stage fall {fall*100:.0f} cm/day -> 6 m frame window lasts {6/fall:.0f} days (need ~{need/tons*t/24:.0f})")

# --- cost per tonne delivered to the village shore (2025 rub) ---
diesel, wage = 95.0, 300e3
villages, kt_each = 3, 20e3
total_t = villages * kt_each
capex = 220e6; crf = 0.15 / (1 - 1.15 ** -7)
days = villages * need / tons * t / 24 + 30          # augering + moves/transit
charter = 400e3 * days                               # pusher + 2-3 kt barges [est]
fuel = 400 * 0.25 * diesel * 24 * days               # 400 kW auger power pack
crew = 12 * wage * 4
consum = 100 * total_t
geol = 10e6
unload = 400 * total_t                               # barge -> village shore stockpile
tot = capex * crf + 0.08 * capex + charter + fuel + crew + consum + geol + unload
print(f"\nbarge-auger: {days:.0f} days, {tot/1e6:.0f} M rub/yr -> {tot/total_t:.0f} rub/t delivered (incl. shore unloading)")
# Baselines (rub/t delivered): (a) river delivery from established mine: mine price 2,500-3,500 + river
# freight 1,000-2,000 km at 2-3 rub/t-km + 2 transshipments 800 -> ; (b) local micro-pit + winter road
for mine, km, rate in ((2500, 1000, 2.0), (3500, 2000, 3.0)):
    print(f" baseline river delivery: mine {mine} + {km} km x {rate} + 800 handling = {mine+km*rate+800:.0f} rub/t")
# micro-pit: strip 1.77 t rock/t at ~250 rub/t moved (frozen, ripping) + mining 400 + bank protection 300
# + winter road truck 150 km at 15 rub/t-km + loading 300
mp = 1.77 * 250 + 400 + 300 + 150 * 15 + 300
print(f" baseline micro-pit + winter road: {mp:.0f} rub/t")
