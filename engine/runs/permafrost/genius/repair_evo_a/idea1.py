"""Idea 1 - Drowned-valley reservoir floor dredging (Kolyma reservoir).
All estimates in code. Sources in comments; [est] = engineering estimate, not sourced.
"""
import numpy as np

print("=== IDEA 1: reservoir floor dredging ===")
# --- Reservoir geometry (voda.gov.ru register via search; ru.wikipedia Kolyma HPP) ---
NPU, UMO = 451.5, 432.0        # m a.s.l. (register gives NPU 450.0, wiki 451.5)
A_NPU, A_UMO = 443.4, 292.0    # km2 at NPU / UMO (voda.gov.ru)
z0 = 451.5 - 134.5             # approx. river bed at dam (dam height 134.5 m, wiki)
p = np.log(A_UMO / A_NPU) / np.log((UMO - z0) / (NPU - z0))
A = lambda z: A_NPU * ((z - z0) / (NPU - z0)) ** p
V = A_NPU * 1e6 * (NPU - z0) / (p + 1) / 1e9
print(f"hypsometry exponent p={p:.2f}; implied volume {V:.1f} km3 (reported 14.56-15.08) -> fit OK")
h_ice = 1.5                    # m, reservoir ice; Kolyma river ice 0.8-1.3 m (BRE); use 1.5 conservative
for lo in (25, 40):
    band = A(UMO - h_ice) - A(UMO - lo)
    print(f"floor band never ice-contacted, {h_ice}-{lo} m below UMO: {band:.0f} km2")

# --- Talik under the floor: 1D enthalpy model, 40 years since filling (1980-1989) ---
def talik_depth(Tb, years=40, Tpf=-4.0, theta=0.30, kt=2.0, kf=2.8, Ct=2.6e6, Cf=2.0e6,
                qgeo=0.05, H=60.0, dz=0.25):
    L = theta * 334e6                      # J/m3 volumetric latent heat (saturated gravel)
    n = int(H / dz); dt = 0.2 * dz**2 * min(Ct, Cf) / max(kt, kf)
    # enthalpy: H<0 frozen, 0..L mushy, >L thawed
    T = np.full(n, Tpf); E = Cf * T
    steps = int(years * 3.156e7 / dt)
    for _ in range(steps):
        T = np.where(E < 0, E / Cf, np.where(E > L, (E - L) / Ct, 0.0))
        k = np.where(E > L / 2, kt, kf)
        kf_ = 2 * k[:-1] * k[1:] / (k[:-1] + k[1:])
        flux = -kf_ * (T[1:] - T[:-1]) / dz          # positive downward
        top = -k[0] * (T[0] - Tb) / (dz / 2)
        dE = np.zeros(n)
        dE[0] += top; dE[:-1] -= flux; dE[1:] += flux; dE[-1] += qgeo
        E = E + dE * dt / dz
    thawed = np.where(E > L / 2)[0]
    return (thawed.max() + 1) * dz if len(thawed) else 0.0

for Tb in (1.0, 2.0, 3.0, 4.0):
    print(f"mean bottom water {Tb:.0f} C -> talik after 40 yr = {talik_depth(Tb):.1f} m "
          f"(permafrost -4 C, 30% vol. ice)")
# Burn 2002 / Arp 2016: talik forms where water deeper than max ice; MAT lake-bed 1-4 C typical

# --- Dredge throughput & season (Damen DOP: up to 100 m depth, DOP250 1250 m3/h mixture) ---
season_d = 120          # open water days, ice-free ~mid-June..mid-Oct [est; Kolyma ice cover ~200 d, BRE]
avail = 0.70
def season_volume(solids_m3h): return solids_m3h * 24 * season_d * avail
for name, s in (("DOP-class 350 mm", 120), ("500 mm ladder pump", 300), ("700 mm", 600)):
    print(f"{name}: {s} m3/h solids -> {season_volume(s)/1e3:.0f} k m3/season")

# --- Cost per m3 of section, bottom-up (2025 rub) ---
diesel = 95.0            # rub/L delivered north [est]
wage = 300e3             # rub/month fully loaded per worker [est]
def dredge_cost(solids, capex, MW, crew, grid=False, months=6):
    vol = season_volume(solids)
    crf = 0.15 / (1 - 1.15 ** -5)                   # 5 yr, 15 %
    energy_kwh = MW * 1e3 * 24 * season_d * avail * 0.8
    fuel = energy_kwh * (4.0 if grid else 0.25 * diesel)   # grid ~4 rub/kWh from Kolyma HPP [est]
    total = capex * crf + 0.08 * capex + fuel + crew * wage * months + 40e6
    return total / vol, total, vol
for grid in (False, True):
    for solids, capex, MW, crew in ((300, 800e6, 2.5, 30), (600, 1.3e9, 5.0, 40)):
        c, tot, vol = dredge_cost(solids, capex, MW, crew, grid)
        print(f"reservoir dredge {solids} m3/h, capex {capex/1e6:.0f} M, grid={grid}: "
              f"{c:.0f} rub/m3 section ({tot/1e6:.0f} M rub/yr, {vol/1e3:.0f} k m3)")

# --- Baselines (per m3 of pay sands, then per gram) ---
# Open-cut bulldozer-ripper stripping of frozen overburden + sluice washing (dominant Magadan practice)
def opencut_per_m3_pay(K, c_strip, c_wash=350): return (K * c_strip + c_wash) * 1.3   # +30% G&A/reclam.
# Land bucket-line dredge in thawed ground (cheapest where talik exists), whole section through dredge
def landdredge_per_m3_pay(K, c=250, prethaw=0): return (K + 1) * (c + prethaw)
# Reservoir dredge: overburden pumped to waste costs ~0.6 of full dredge cost/m3 [est]
def resdredge_per_m3_pay(K, c): return K * 0.6 * c + c

g_pay, rec_open, rec_res, rec_land = 0.8, 0.85, 0.70, 0.85   # g/m3 pay; recoveries [est]
print("\ncost per gram recovered (rub/g), pay grade 0.8 g/m3:")
print(" K  open-cut(c_s=200) open-cut(c_s=350) land-dredge(+prethaw150) reservoir(c=450) reservoir(c=650)")
for K in (1, 2, 4, 6):
    oc1 = opencut_per_m3_pay(K, 200) / (g_pay * rec_open)
    oc2 = opencut_per_m3_pay(K, 350) / (g_pay * rec_open)
    ld = landdredge_per_m3_pay(K, 250, 150) / (g_pay * rec_land)
    r1 = resdredge_per_m3_pay(K, 450) / (g_pay * rec_res)
    r2 = resdredge_per_m3_pay(K, 650) / (g_pay * rec_res)
    print(f" {K}   {oc1:7.0f}           {oc2:7.0f}            {ld:7.0f}                {r1:7.0f}          {r2:7.0f}")
# Cross-check: WGC Russian AISC 2022 = $1,018/oz = $32.7/g ~ 2,300-3,000 rub/g -> open-cut model in range

# --- Consistency: level vs reach, turbidity ---
print("\nlevel window: summer level 433->451 m; floor band 405-430 m -> water depth "
      f"{433-430:.0f}-{451-405:.0f} m; DOP pump on winch reaches 50-100 m -> OK; dig adds talik depth")
fines_frac, escape = 0.15, 0.05
for vol in (season_volume(300),):
    fines_t = vol * 1.8 * fines_frac
    for Q in (300, 800):
        c = fines_t * escape * 1e6 / (season_d * 86400 * Q)  # g/m3 = mg/L
        print(f"fines {fines_t/1e3:.0f} kt/season, 5% escape, flow {Q} m3/s -> +{c:.2f} mg/L "
              f"(fishery limit +0.25 / +0.75 mg/L)")
