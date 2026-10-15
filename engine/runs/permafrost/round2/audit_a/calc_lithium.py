"""Audit checks for ideas 1, 4, 5 (night-sky lithium freeze cascade)."""
import math
import numpy as np

h = 6.62607015e-34; c = 2.99792458e8; kB = 1.380649e-23; sigma = 5.670374e-8

def planck_band(T, l1, l2, n=20000):
    lam = np.linspace(l1, l2, n)
    B = 2 * math.pi * h * c**2 / lam**5 / (np.exp(h * c / (lam * kB * T)) - 1)
    return np.trapezoid(B, lam)

print("=== Radiative window ===")
for TC in (-40, -45, -50, -52):
    T = TC + 273.15
    band = planck_band(T, 8e-6, 13e-6)
    tot = sigma * T**4
    print(f"T={TC} C: blackbody {tot:.1f} W/m2, 8-13um {band:.1f} W/m2 ({band/tot*100:.1f}%)")

print("\n=== LCE / Li basics ===")
M_Li, M_LCE = 6.941, 73.89
Li_per_tLCE = 1000 * 2 * M_Li / M_LCE
print(f"Li per t LCE = {Li_per_tLCE:.1f} kg")

# Idea 1: 11,600 m2 x 55 kg/m2 -> implied brine Li
for area, kg in ((11600, 55), (13000, 36), (35600, 36)):
    brine_t = area * kg / 1000
    print(f"area {area} m2 x {kg} kg/m2 = {brine_t:.0f} t brine/t LCE -> implied Li {Li_per_tLCE/brine_t*1000:.0f} mg/kg (100% recovery)")
# Idea 5 says 147 mg/L; convert to mg/kg for CaCl2 brine densities
for rho in (1.25, 1.30, 1.35):
    mgkg = 147 / rho
    brine_t = Li_per_tLCE / (mgkg / 1e6) / 1000
    print(f"147 mg/L at rho {rho}: {mgkg:.0f} mg/kg -> {brine_t:.0f} t brine -> {brine_t*1000/36:.0f} m2 at 36 kg/m2")
print("cost per m2-yr implied by $55k/11,600 m2:", 55000/11600, " ; Idea5 65k/13000:", 65000/13000, " 178k/35600:", 178000/35600)
print("Idea1 niche 100 m2 x $4.74 =", 100*55000/11600)

print("\n=== Hours below threshold (normal model of hourly T within month) ===")
from math import erf, sqrt, exp, pi
def Phi(z): return 0.5 * (1 + erf(z / sqrt(2)))
# Udachny monthly means: Jan -39.4 (Wikipedia table). Dec/Feb assumed -36/-35 (similar to Yakutsk structure)
months = {"Dec": (-36.0, 31), "Jan": (-39.4, 31), "Feb": (-35.0, 28)}
for sd in (5.0, 6.0, 7.0):
    hrs = sum(Phi((-45 - mu) / sd) * d * 24 for mu, d in months.values())
    # mean excess below -45 in Jan
    z = (-45 + 39.4) / sd
    excess = sd * (exp(-z*z/2)/sqrt(2*pi) / Phi(z) + z)
    print(f"SD {sd}: hours <= -45 C ~ {hrs:.0f} h; Jan mean excess below -45 = {excess:.2f} K")

print("\n=== Above-eutectic CaCl2.6H2O crystallisation (Idea 5) ===")
for x0 in (0.36, 0.40, 0.24):
    for xf in (0.31, 0.32):
        if x0 <= xf:
            continue
        s = (x0 - xf) / (0.5066 - xf)  # kg hexahydrate per kg brine
        print(f"x0={x0} xf={xf}: hexahydrate {s:.3f} kg/kg, liquid {1-s:.3f} -> Li x{1/(1-s):.2f}")
# Udachnaya measured TDS 280-406 g/L -> CaCl2 wt%
for tds in (280, 391, 406):
    for frac in (0.75, 0.85):
        cacl2_gL = tds * frac
        rho = 1.0 + 0.0085 * cacl2_gL / 10  # rough: 30% CaCl2 ~ 1.28-1.3 kg/L
        print(f"TDS {tds} g/L, CaCl2 share {frac}: ~{cacl2_gL:.0f} g/L ~ {cacl2_gL/(rho*1000)*100:.1f} wt% (rho~{rho:.2f})")
print("36-40 wt% CaCl2 brine = ", 0.36*1.36*1000, "-", 0.40*1.40*1000, "g/L CaCl2 (rho 1.36-1.40)")

print("\n=== Freeze concentration with imperfect rejection (Scheil, Ideas 1/5 '30x') ===")
for k in (0.0, 0.05, 0.1, 0.2, 0.3):
    fL = 1/30
    CL = fL**(k - 1)
    rec = fL * CL
    print(f"k_eff={k}: liquid conc factor {CL:.1f}x, Li recovery in liquid {rec*100:.0f}%")

print("\n=== Idea 1 niche ice per m2 ===")
for eluate in (0.3, 0.5, 1.0):  # g/L Li
    V = Li_per_tLCE / eluate  # m3 eluate per t LCE
    ice = V * (1 - 1/30)
    flux = ice * 1000 * 334e3 / 100 / (150 * 86400)
    print(f"eluate {eluate} g/L: {V:.0f} m3/t LCE, ice {ice:.0f} t -> {ice/100:.2f} t/m2/winter, mean flux {flux:.0f} W/m2 over 150 d")

print("\n=== Idea 4: RO 6 g/L osmotic, MVR replaced, Li drift losses ===")
mLiCl = 6 / M_Li  # mol/L
for T, phi in ((278, 0.93), (293, 0.93)):
    print(f"pi at 6 g/L Li, {T} K: {2*mLiCl*0.08314*T*phi:.1f} bar")
# product 20.6 g/L Li -> LiCl wt% and freezing point
LiCl = 20.6 * 42.39 / M_Li
rho = 1.07
m = (LiCl / 42.39) / ((rho * 1000 - LiCl) / 1000)
for phi in (1.12, 1.18):
    print(f"20.6 g/L Li = {LiCl:.0f} g/L LiCl, {m:.2f} mol/kg, Tf ~ {-1.86*2*m*phi:.1f} C (phi {phi})")
water_evap = Li_per_tLCE / 6 - Li_per_tLCE / 20.6
print(f"water removed 6->20.6 g/L = {water_evap:.1f} m3/t LCE")
for kwh in (20, 40, 60):
    for p in (0.05, 0.08, 0.30):
        print(f"  MVR {kwh} kWh/m3 at ${p}/kWh: energy ${water_evap*kwh*p:.0f}/t LCE")
print("Idea4 MVR claim $470-1085/t LCE = $/m3 evaporated:", 470/water_evap, 1085/water_evap)
# feed per pass with 53% Li per pass
F = Li_per_tLCE / (0.53 * 6)
print(f"spray feed per stage-1 pass ~ {F:.1f} m3/t LCE; ice/stage ~ {F*(1-0.53*6/20.6):.0f} t")
# drift loss sensitivity: sprays per unit Li = 1/0.53 per stage x 2 stages
sprays = 2 / 0.53
for drift in (0.005, 0.01, 0.02, 0.05):
    loss = 1 - (1 - drift)**sprays
    print(f"drift {drift*100:.1f}%/pass -> Li lost {loss*100:.1f}% -> ${loss*10000:.0f}/t LCE at $10k/t")
# storage
for cap in (10000, 20000):
    print(f"{cap} t LCE/yr: RO concentrate {Li_per_tLCE/6*cap/1e6:.2f} Mm3/yr; 7/12 stored = {Li_per_tLCE/6*cap*7/12/1e6:.2f} Mm3")
