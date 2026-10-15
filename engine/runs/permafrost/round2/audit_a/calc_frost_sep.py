"""Audit checks for ideas 2, 9, 12 (self-charging frost separator cascade)."""
import math
eps0 = 8.854e-12; g = 9.81

print("=== Max grain charge (surface breakdown) ===")
for rho in (2650, 3150):
    r = 150e-6
    qmax = eps0 * 3e6 * 4 * math.pi * r**2
    m = 4/3 * math.pi * r**3 * rho
    print(f"rho {rho}: q/m max = {qmax/m*1e6:.0f} uC/kg; 5% = {0.05*qmax/m*1e6:.1f} uC/kg")

def drift(qm, E, H):  # no drag, from rest
    return qm * E * H / g

print("\n=== Drift (no drag), fall 1.5 m ===")
for idea, E, gap, qm in (("12: 45 kV over 1 m", 45e3, 1.0, 10e-6), ("2: 90 kV over 0.3 m", 3e5, 0.3, None), ("9: 75 kV over 0.5 m", 1.5e5, 0.5, 10e-6)):
    if qm is None:
        qm = 0.41 * g / (3e5 * 1.5)
        print(f"Idea 2 implied q/m for 41 cm: {qm*1e6:.2f} uC/kg")
    x = drift(qm, E, 1.5)
    hit = (gap/2) * g / (qm * E)
    print(f"Idea {idea}: E={E/1e3:.0f} kV/m drift {x*100:.1f} cm; half-gap {gap/2*100:.0f} cm reached after {hit:.2f} m fall")
E_needed = [0.30 * g / (10e-6 * 1.5), 0.60 * g / (10e-6 * 1.5)]
print("Field needed for 30-60 cm at 10 uC/kg over 1.5 m:", [f"{e/1e3:.0f} kV/m" for e in E_needed])

print("\n=== Space charge limit vs self-excitation current ===")
def mdot_limit(E, qm, alpha, f=0.5, z=0.75):
    v = math.sqrt(2 * g * z)
    return alpha * eps0 * E * v / (f * qm)  # kg/s per metre width
for E, qm in ((45e3, 10e-6), (1.5e5, 10e-6), (3e5, 8.94e-6)):
    for alpha in (0.18, 1.0):
        md = mdot_limit(E, qm, alpha)
        I = md * 0.5 * qm
        print(f"E={E/1e3:.0f} kV/m alpha={alpha}: m'={md:.3f} kg/s/m = {md*3.6:.2f} t/h/m, sorted current/bin ~{I*1e6:.2f} uA/m")
# Idea 12: 45 kV with 1e10 ohm leakage
I_leak = 45e3 / 1e10
md_needed = I_leak / (0.5 * 10e-6)
v = math.sqrt(2 * g * 0.75)
ratio = (md_needed / v * 0.5 * 10e-6) / (eps0 * 45e3)
print(f"Idea 12: leakage current at 45 kV/1e10 ohm = {I_leak*1e6:.1f} uA -> needs m' >= {md_needed:.2f} kg/s/m ({md_needed*3.6:.1f} t/h/m); space-charge field / applied = {ratio:.1f}")
# charging time claim
for C in (30e-12, 100e-12):
    print(f"  C={C*1e12:.0f} pF: 45 kV in 1.4 s needs {C*45e3/1.4*1e6:.2f} uA")
# plant width for Idea 12: 1 Mt/yr, circulating load 7.2
feed = 1e6 / 8000
md_lim = mdot_limit(45e3, 10e-6, 0.18) * 3.6
print(f"Idea 12 total stage throughput {feed*7.2:.0f} t/h -> plate width {feed*7.2/md_lim:.0f} m at {md_lim:.2f} t/h/m")

print("\n=== Cascade (gambler's ruin, feed at stage m of N) ===")
def ptop(s, m, N):
    q = (1 - s) / s
    if abs(q - 1) < 1e-12:
        return m / (N + 1)
    return (1 - q**m) / (1 - q**(N + 1))
def visits(s, m, N):
    # expected number of stage passes for a particle starting at m (absorbing at 0 and N+1)
    import numpy as np
    P = np.zeros((N, N))
    for i in range(N):
        if i + 1 < N: P[i, i+1] = s
        if i - 1 >= 0: P[i, i-1] = 1 - s
    Nmat = np.linalg.inv(np.eye(N) - P)
    return Nmat[m-1].sum()
for Li2O_spod in (7.5, 8.0):
    xs = 1.2 / Li2O_spod
    for (sv, sw, N) in ((0.85, 0.45, 9), (0.85, 0.45, 8), (0.80, 0.50, 22), (0.75, 0.55, 40)):
        best = None
        for m in range(1, N + 1):
            rv, rw = ptop(sv, m, N), ptop(sw, m, N)
            grade = xs * rv * Li2O_spod / (xs * rv + (1 - xs) * rw)
            cl = xs * visits(sv, m, N) + (1 - xs) * visits(sw, m, N)
            if best is None or (rv >= 0.80 and grade > best[2]):
                best = (m, rv, grade, cl)
        m, rv, grade, cl = best
        print(f"spod {Li2O_spod}% Li2O, split {sv}/{sw}, N={N}: feed stage {m}, recovery {rv*100:.1f}%, grade {grade:.2f}% Li2O, stage passes/feed {cl:.1f}")
# persistent misbehaviour: fraction phi of gangue behaves like spodumene (locked/micaceous), 85/45, N=9, m=1
xs = 1.2 / 7.5
for phi in (0.0, 0.02, 0.05, 0.10):
    rv = ptop(0.85, 1, 9); rw = ptop(0.45, 1, 9)
    waste_top = (1 - xs) * ((1 - phi) * rw + phi * rv)
    grade = xs * rv * 7.5 / (xs * rv + waste_top)
    print(f"persistently mis-sorted gangue {phi*100:.0f}%: grade {grade:.2f}% Li2O at recovery {rv*100:.0f}%")
# what if 5% of spodumene (locked) behaves like gangue
for psi in (0.05, 0.10):
    rv = (1 - psi) * ptop(0.85, 1, 9) + psi * ptop(0.45, 1, 9)
    print(f"locked spodumene {psi*100:.0f}% behaving as gangue: recovery {rv*100:.1f}%")

print("\n=== Humidity / drying (Idea 12, 2, 9) ===")
def psat_ice(TC):
    T = TC + 273.15
    return 611.15 * math.exp(22.452 * TC / (272.55 + TC))
def psat_w(TC):
    return 611.2 * math.exp(17.62 * TC / (243.12 + TC))
pv = 0.9 * psat_ice(-40)
print(f"psat_ice(-40)={psat_ice(-40):.2f} Pa, psat_w(-40)={psat_w(-40):.2f} Pa, psat(0)={psat_w(0):.0f} Pa; 90%RHice air -> RH at 0C = {pv/psat_w(0)*100:.2f}%")
rho_m40 = 101325 * 0.02897 / (8.314 * 233.15)
air_kg = 690 * rho_m40
print(f"690 m3 at -40C = {air_kg:.0f} kg air; heating to 0C = {air_kg*1.005*40/1000:.1f} MJ/t")
for moist in (0.0003, 0.002, 0.004, 0.01):
    w = moist * 1000 / air_kg + pv / 101325 * 0.622
    pv2 = w / (0.622 + w) * 101325
    print(f"ore moisture {moist*100:.2f}% -> air humidity ratio {w*1000:.2f} g/kg -> RH at 0 C {pv2/psat_w(0)*100:.0f}%")
# ore warming from -40 to 0 and mill energy
print(f"ore -40->0 C: {0.80*40:.0f} MJ/t; total with air {0.80*40 + air_kg*1.005*40/1000:.0f} MJ/t")
for Wi in (12, 14, 16):
    for F80 in (6000, 10000):
        W = 10 * Wi * (1/math.sqrt(300) - 1/math.sqrt(F80))
        print(f"Bond Wi {Wi} kWh/t, F80 {F80} um -> P80 300 um: {W:.1f} kWh/t = {W*3.6:.0f} MJ/t")
print(f"preheat ore -40 -> +100 C (Peretti & Zucca needed >100 C): {0.8*140:.0f} MJ/t")

print("\n=== Economics checks ===")
ore_Li2O = 1.2; rec = 0.82
kg_Li2O_per_t = ore_Li2O * 10 * rec
print(f"Li2O recovered per t ore {kg_Li2O_per_t:.2f} kg")
print(f"Idea 12 $27/t ore = ${27/kg_Li2O_per_t*1000:.0f}/t Li2O ; haul part 0.161*105 = ${0.161*105:.1f}/t ore -> separation ${27-0.161*105:.1f}/t ore")
print(f"Idea 2 $3,994/t Li2O = ${3994*kg_Li2O_per_t/1000:.1f}/t ore ; Idea 9 $4,100-4,960 = ${4100*kg_Li2O_per_t/1000:.1f}-{4960*kg_Li2O_per_t/1000:.1f}/t ore")
print(f"mass pull 1.2*0.82/6.1 = {1.2*0.82/6.1*100:.1f}%")
# HV supply cost that self-charging avoids
for kV, uA in ((90, 5), (75, 1.4)):
    print(f"HV supply power {kV} kV x {uA} uA/m = {kV*1e3*uA*1e-6:.2f} W per m; for 700-5000 m: {kV*1e3*uA*1e-6*5000/1000:.2f} kW max")
print("vs throughput 125 t/h -> kWh/t:", 90e3*5e-6*5000/1000/125)
# Idea 2 numbers: 700 m plates for 1 Mt/yr at 1.47 t/h/m
print("Idea 2: 1 Mt/yr / 8000 h / 1.47 =", 1e6/8000/1.47, "m per pass; x ~7-8 passes =", 1e6/8000/1.47*7.5)
print("Idea 2: drying 1-2% moisture: sublimation", 10*2.83, "-", 20*2.83, "MJ/t")
