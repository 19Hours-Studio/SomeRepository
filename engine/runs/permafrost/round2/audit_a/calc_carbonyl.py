"""Audit checks for ideas 3, 6, 8 (Ni(CO)4 in Power of Siberia gas)."""
import math
R = 8.314
M_Ni, M_CO, M_NiCO4 = 58.693, 28.010, 170.73

# flows
Vstd = 38e9  # m3/yr at 20 C (Russian standard)
mol_yr = Vstd / 0.024055
print(f"gas moles/yr {mol_yr:.3e}")
for x in (0.0004, 0.00027, 0.001):
    ni_t = mol_yr * x * M_Ni / 1e6
    print(f"dose {x*100:.3f} mol%: {ni_t/1e3:.1f} kt Ni/yr; Ni(CO)4 {mol_yr*x*M_NiCO4/1e3/3.156e7:.2f} kg/s")
rho_std = 0.73
mdot = Vstd * rho_std / 3.156e7
print(f"mass flow {mdot:.0f} kg/s")
A = math.pi * (1.42 - 2 * 0.0257)**2 / 4
for p, T, Z in ((9.8e6, 278, 0.82), (7.5e6, 278, 0.86), (5.5e6, 278, 0.90)):
    rho = p * 0.0175 / (Z * R * T)
    print(f"p {p/1e6} MPa: rho {rho:.0f} kg/m3, v {mdot/(rho*A):.1f} m/s")
print("transit 2159 km at 8.3 m/s:", 2159e3/8.3/3600, "h ; 300 km:", 300e3/8.3/3600, "h")

print("\n=== Ni(CO)4 vapour pressure (Clausius-Clapeyron, nbp 316.15 K, dHvap 29.5-30 kJ/mol) ===")
def psat(TC, dH=29.5e3):
    T = TC + 273.15
    return 101.325 * math.exp(-dH / R * (1/T - 1/316.15))
for TC in (20, -10, -13, -20):
    print(f"{TC} C: {psat(TC):.2f} kPa (dH 29.5) / {psat(TC,30.5e3):.2f} kPa (dH 30.5)")
for x, TC in ((0.0004, -20), (0.001, -13), (0.00027, -10)):
    pp = x * 9800
    print(f"x={x*100:.3f}% at 9.8 MPa: p={pp:.2f} kPa, S at {TC} C = {pp/psat(TC):.2f}-{pp/psat(TC,30.5e3):.2f}")

print("\n=== Equilibrium CO needed: Ni(CO)4(g) = Ni + 4 CO ===")
dH = 4 * (-110.53) - (-602.9)  # kJ
dS = 29.87 + 4 * 197.66 - 410.6  # J/K
print(f"dH {dH:.1f} kJ/mol, dS {dS:.1f} J/mol/K")
def xco_eq(TC, xni, P=98.0):
    T = TC + 273.15
    K = math.exp(-(dH * 1e3 - T * dS) / (R * T))
    pCO = (K * xni * P) ** 0.25
    return pCO / P
for TC, xni in ((50, 0.0004), (80, 0.0004), (45, 0.00027), (40, 0.0004)):
    print(f"T {TC} C, x_Ni {xni*100:.3f}%: CO_eq {xco_eq(TC,xni)*100:.3f} mol%")
# decomposer residual at 190-250 C
for TC, xco, P in ((190, 0.0015 + 0.0016, 98), (200, 0.0005 + 0.0016, 98), (250, 0.0005 + 0.0016, 98), (200, 0.0005 + 0.0016, 50)):
    T = TC + 273.15
    K = math.exp(-(dH * 1e3 - T * dS) / (R * T))
    pni = (xco * P) ** 4 / K
    print(f"decomposer {TC} C, CO {xco*100:.2f}%, {P} bar: residual Ni(CO)4 {pni/P*1e9:.2f} ppb")

print("\n=== CO consumption per t Ni ===")
base = 4 * M_CO / M_Ni
for xco, xni in ((0.0015, 0.0004), (0.0005, 0.0004), (0.00035, 0.00027)):
    tot = base + (xco / xni) * M_CO / M_Ni
    print(f"CO {xco*100:.3f}% / Ni {xni*100:.3f}%: {tot:.2f} t CO/t Ni (min {base:.2f})")
print("Idea 8 $514/t Ni / 2.53 =", 514/2.53, "$/t CO")
for cco in (150, 200, 300):
    print(f"CO at ${cco}/t: Idea 6 one-way CO (3.70 t) = ${3.70*cco:.0f}/t Ni ; minimum 1.91 t = ${1.91*cco:.0f}")
# CO in sales gas after decomposition
print(f"CO in sales gas after decomposition (Idea 6): {0.15 + 4*0.04:.2f} mol%; Idea 8: {0.035 + 4*0.027:.3f} mol%")

print("\n=== Releases ===")
# rupture section inventory
L = 30e3
V = A * L
for p, Z, x in ((9.8e6, 0.82, 0.0004), (7.5e6, 0.86, 0.0004), (9.8e6, 0.82, 0.00027)):
    n = p * V / (Z * R * 278)
    m = n * x * M_NiCO4 / 1e6
    print(f"30 km at {p/1e6} MPa, x {x*100:.3f}%: gas {n:.2e} mol, Ni(CO)4 {m:.1f} t")
mol_12t = 12e6 / M_NiCO4
for name, ppm in (("IDLH", 2), ("AEGL-3 60 min", 0.16), ("AEGL-2 60 min", 0.036)):
    print(f"12 t Ni(CO)4 dilution volume to {name} {ppm} ppm: {mol_12t/(ppm*1e-6)*0.0245:.2e} m3")
# compressor unit blowdown, EPA default 15 Mcf
bd = 15e3 * 0.0283168
for x in (0.0004, 0.00027):
    kg = bd / 0.024055 * x * M_NiCO4 / 1000
    print(f"one compressor blowdown {bd:.0f} m3 at {x*100:.3f}%: {kg:.2f} kg Ni(CO)4 -> {kg/M_NiCO4*1000/(0.036e-6)*0.0245:.2e} m3 to AEGL-2 1h; per yr (3-52 events x 9 CS): {kg*3*9:.0f}-{kg*52*9:.0f} kg")
# O2 spec vs carbonyl
print("O2 up to 200 ppm (Russian spec) vs Ni(CO)4 270-400 ppm: O2/Ni ratio", 200/400, "-", 200/270)
# half-life plume
for hl in (40, 60, 600, 3600):
    for u in (1, 2, 5):
        t = 1000 / u
        print(f"t1/2 {hl}s wind {u} m/s: surviving at 1 km {0.5**(t/hl)*100:.3g}%")

print("\n=== Decomposer heating (Idea 6) and Idea 8 gross ===")
for cp in (2.6, 2.8):
    print(f"cp {cp}: heat 879 kg/s by 185 K = {879*cp*185/1e3:.0f} MW")
gas_LHV = mdot * 47.5
print(f"line energy {gas_LHV:.0f} MW; 0.12% = {gas_LHV*0.0012:.0f} MW")
# value of 0.12% of gas
for price in (150, 250):
    cost = 0.0012 * 38e9 / 1000 * price / 37.1e3
    print(f"0.12% of 38 bcm at ${price}/1000 m3: ${cost:.0f}/t Ni")

print("\n=== Idea 3 ratio check ===")
for c in (109, 947):
    print(f"truck $1067 / pipeline {c} = {1067/c:.2f}x")
print("Idea 6: pipeline share $7 vs $1067 =", 1067/7)
# capacity share by moles
share = 0.0004 + 0.0015
print(f"Idea 6 molar share of line taken by Ni(CO)4+CO: {share*100:.2f}% -> {share*38e9/1e6:.0f} Mm3/yr equivalent capacity")
for tariff in (30, 60):  # $ per 1000 m3 transport over line
    print(f"  at transport value ${tariff}/1000 m3: ${share*38e9/1000*tariff/37.1e3:.0f}/t Ni")
