"""Extra checks: cascade split sensitivity, Fe(CO)5 equilibrium, compressor discharge T vs CO margin."""
import math
R = 8.314
def ptop(s, m, N):
    q = (1 - s) / s
    if abs(q - 1) < 1e-12:
        return m / (N + 1)
    return (1 - q**m) / (1 - q**(N + 1))
xs = 1.2 / 7.5
print("=== Cascade sensitivity (N=9, feed stage 1, spodumene 7.5% Li2O) ===")
for sv in (0.80, 0.85, 0.88):
    for sw in (0.40, 0.45, 0.50):
        rv, rw = ptop(sv, 1, 9), ptop(sw, 1, 9)
        grade = xs * rv * 7.5 / (xs * rv + (1 - xs) * rw)
        print(f"split {sv}/{sw}: recovery {rv*100:.1f}%, grade {grade:.2f}% Li2O")
# binomial-type precision needed: to tell 45% from 50% forward with 95% conf on particle counts
for n in (100, 400, 1000):
    se = math.sqrt(0.45 * 0.55 / n)
    print(f"tracer particles n={n}: 95% CI on 45% split = +/-{1.96*se*100:.1f} points")

print("\n=== Fe(CO)5 equilibrium on pipe steel: Fe + 5CO = Fe(CO)5(g) ===")
dH = -733.8 - 5 * (-110.53)
dS = 445.2 - 27.28 - 5 * 197.66
for TC in (5, 25, 50):
    T = TC + 273.15
    K = math.exp(-(dH * 1e3 - T * dS) / (R * T))
    for xco in (0.0015, 0.0005, 0.00035):
        p = K * (xco * 98) ** 5
        print(f"T {TC} C, CO {xco*100:.3f}% at 98 bar: eq Fe(CO)5 {p/98*1e6:.3g} ppm")

print("\n=== Compressor discharge temperature vs CO margin ===")
dHn = 160.8e3; dSn = 409.9
def xco_eq(TC, xni, P=98.0):
    T = TC + 273.15
    K = math.exp(-(dHn - T * dSn) / (R * T))
    return (K * xni * P) ** 0.25 / P
for T1 in (5, 15, 20, 25):
    for ratio in (1.44,):
        T2 = (T1 + 273.15) * ratio ** (0.3 / (1.3 * 0.85)) - 273.15
        print(f"suction {T1} C, ratio {ratio}: discharge {T2:.0f} C; CO_eq for 0.04% Ni {xco_eq(T2,0.0004)*100:.3f}%, for 0.027% {xco_eq(T2,0.00027)*100:.3f}%")
for TC in (55, 60, 65):
    print(f"{TC} C: CO_eq 0.04% Ni = {xco_eq(TC,0.0004)*100:.3f}% ; 0.027% Ni = {xco_eq(TC,0.00027)*100:.3f}%")
