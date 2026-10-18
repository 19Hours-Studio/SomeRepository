"""Idea 2 - Creek-undercut overburden caving (frozen deep placers).
[est] = engineering estimate. Standard heat-transfer / sediment-transport correlations.
"""
import numpy as np
print("=== IDEA 2: creek-undercut caving ===")
rho_w, cw = 1000.0, 4.18e6          # J/m3K
# Thaw energy per m3 of frozen pay gravel (20 % vol ice, -4 C) - Andersland & Ladanyi typical values
theta_i, Tpf = 0.20, -4.0
E_thaw = theta_i * 917 * 334e3 + 2.0e6 * abs(Tpf)
print(f"thaw energy of pay: {E_thaw/1e6:.0f} MJ/m3")

# --- Round 1: original - creek flowing through a gallery; heat transfer + armouring ---
nu, kw, Pr = 1.52e-6, 0.57, 11.2    # water at 5 C
for Q, b, hgal in ((1.0, 2.0, 1.5), (0.3, 2.0, 1.5)):
    A = b * hgal * 0.6               # flow fills ~60 % of gallery
    u = Q / A; Dh = 4 * A / (2 * 0.6 * hgal + b)
    Re = u * Dh / nu; Nu = 0.023 * Re**0.8 * Pr**0.4; h = Nu * kw / Dh
    q = h * 8.0                      # 8 K excess
    print(f"Q={Q} m3/s gallery {b}x{hgal} m: u={u:.2f} m/s Re={Re:.1e} h={h:.0f} W/m2K "
          f"-> {q/1e3:.1f} kW/m2 -> bare-face thaw {q/E_thaw*86400:.1f} m/day (IF thawed gravel removed)")
# Armouring: can that flow carry the thawed gravel? Meyer-Peter Mueller, D50 = 40 mm
def mpm(Q, b, S, D=0.04, n=0.035):
    # solve Manning for depth in rectangular channel
    d = 0.05
    for _ in range(200):
        A = b * d; R = A / (b + 2 * d); Qc = A * R**(2/3) * S**0.5 / n
        d *= (Q / Qc) ** 0.4
    tau = rho_w * 9.81 * R * S; ts = tau / (1650 * 9.81 * D)
    qs = 8 * max(ts - 0.047, 0) ** 1.5 * np.sqrt(1.65 * 9.81 * D**3) * b   # m3/s solids
    return d, ts, qs
for S in (0.005, 0.01, 0.02):
    d, ts, qs = mpm(1.0, 2.0, S)
    print(f" slope {S}: depth {d:.2f} m, Shields {ts:.3f}, gravel capacity {qs*86400:.0f} m3/day")
# Gold: tau*_gold for 1 mm grain -> settles out on the gallery floor (natural sluice, lost under cave)
d, ts, qs = mpm(1.0, 2.0, 0.01)
ts_gold = ts * 1650 * 0.04 / (18300 * 0.001)
print(f" gold 1 mm Shields at same flow ~{ts_gold:.3f} -> partially mobile only; gold concentrates on "
      "floor under the caving roof -> ROUND-1 FAIL (gold lost / transport-limited)")

# --- Round 2: monitor jets of creek water at the face + hydro-elevator slurry lift (no gold on floor) ---
water_ratio = 7.0                    # m3 water per m3 gravel (hydraulicking 6-15 typical)
for dT in (3.0, 6.0, 9.0):
    heat_ratio = water_ratio * cw * dT / E_thaw
    print(f"jet water {dT+1:.0f} C cooled to ~1 C: heat delivered/needed = {heat_ratio:.2f}")
# Closed circuit pond as solar collector (Russian placers must recycle water)
pond_ha, solar = 3.0, 180.0          # W/m2 mean Jul-Aug absorbed [est, 60-65N]
print(f"recycle pond {pond_ha} ha absorbs ~{pond_ha*1e4*solar/1e6:.1f} MW in Jul-Aug")
monitor_Q = 0.15                    # m3/s per monitor
for dT in (5.0,):
    P_heat = monitor_Q * cw * dT
    thaw_m3h = P_heat * 0.5 / E_thaw * 3600     # 50 % heat-use efficiency [est]
    print(f"one monitor 0.15 m3/s, dT {dT} K: {P_heat/1e6:.1f} MW -> {thaw_m3h:.0f} m3/h thawed at 50% eff; "
          f"water-limited rate {monitor_Q*3600/water_ratio:.0f} m3/h")
rate = min(monitor_Q * cw * 5 * 0.5 / E_thaw * 3600, monitor_Q * 3600 / water_ratio)
season = 70                         # days with water >= 5-6 C (Jul-Aug) [est]
vol = 2 * rate * 20 * season
print(f"2 monitors x {rate:.0f} m3/h x 20 h x {season} d = {vol/1e3:.0f} k m3 pay/season")

# --- Roof caving spans: frozen overburden, long-term tensile 0.2-0.5 MPa, instantaneous 1-2 MPa ---
rho_o = 1900.0
for h in (6, 10, 15):
    for st in (0.2, 0.5, 1.5):
        W = np.sqrt(2 * h * st * 1e6 / (rho_o * 9.81))        # clamped beam across panel
        Lc = np.sqrt(h * st * 1e6 / (3 * rho_o * 9.81))       # cantilever behind face
        print(f" overburden {h} m, sigma_t {st} MPa: panel span to cave {W:.0f} m, goaf cantilever {Lc:.1f} m")

# --- Cost per m3 pay (2025 rub) ---
diesel, wage = 95.0, 300e3
P_pump_kW = 2 * monitor_Q * 1.2e6 / 0.7 / 1e3 + 2 * 150   # monitors at 1.2 MPa + elevator boost [est]
energy = P_pump_kW * 20 * season
fuel = energy * 0.25 * diesel
capex = 150e6; crf = 0.15 / (1 - 1.15 ** -5)
dev = 20e6                                       # portal cut, starter drive, bypass, ponds per season
crew = 10 * wage * 4
wash = 100.0 * vol                               # sluice / small plant
tot = capex * crf + 0.1 * capex + fuel + dev + crew + wash
c_ucc = tot / vol
print(f"\npump power {P_pump_kW:.0f} kW; cost: {tot/1e6:.0f} M rub/yr -> {c_ucc:.0f} rub/m3 pay")
rec_ucc, rec_oc, rec_ug = 0.70, 0.90, 0.80
g = 1.5   # g/m3 pay, deep placers richer [est]
print(" K   open-cut c_s=200   c_s=350   underground drill-blast(2500-4000/m3)   undercut-caving")
for K in (4, 6, 8, 12):
    oc1 = (K * 200 + 350) * 1.3 / (g * rec_oc); oc2 = (K * 350 + 350) * 1.3 / (g * rec_oc)
    ug = (2500 / (g * rec_ug), 4000 / (g * rec_ug))
    uc = c_ucc / (g * rec_ucc)
    print(f" {K:2d}   {oc1:6.0f}            {oc2:6.0f}    {ug[0]:.0f}-{ug[1]:.0f}                          {uc:6.0f}  rub/g "
          f"(ratio vs cheapest {min(oc1, ug[0])/uc:.1f}x)")
