"""Audit checks for ideas 7, 10, 11 (freeze-engine vitriol winning)."""
import math

def p_butane(TK):  # NIST Antoine (Das et al.), bar, 195-273 K
    return 10 ** (3.85002 - 909.65 / (TK - 36.146))
def T_butane(pbar):
    return 909.65 / (3.85002 - math.log10(pbar)) + 36.146
print("=== n-butane saturation ===")
for p in (0.87, 0.97, 0.19, 0.30, 0.73):
    print(f"{p} bar -> {T_butane(p)-273.15:.1f} C")
print("propane hydrate I-H-V: 0.1 MPa at -14 C (lit.), quadruple point ~0 C/1.7 bar; propane boiling 3.5-3.9 bar at -6..-8 C is >2x the hydrate pressure")

print("\n=== Ice per kg Cu and residual-liquor impurity factor ===")
C_eut = 0.118 * 1130 * 63.55 / 159.61  # g/L Cu at CuSO4-ice eutectic (11.8 wt%, rho~1.13)
print(f"Cu at CuSO4-ice eutectic ~ {C_eut:.0f} g/L (0.837 mol/kg water, -1.6 C)")
for feed, rec in ((2.5, 0.8), (2.5, 0.9), (10, 0.8), (15, 0.8)):
    V = 1 / (feed * rec)  # m3 feed per kg Cu recovered... in m3 per kg -> L per g
    Lpkg = 1000 / (feed * rec)
    resid_frac = (1 - rec) * feed / C_eut
    ice = Lpkg * (1 - resid_frac) - 1000 / feed * 0  # approx, ignore crystal water
    print(f"feed {feed} g/L, rec {rec}: {Lpkg:.0f} L feed/kg Cu, residual liquor {resid_frac*100:.2f}% of feed -> impurities x{1/resid_frac:.0f}; ice ~{Lpkg*(1-resid_frac) - 1000/feed*rec*0:.0f} kg/kg Cu")

print("\n=== Freezing point of residual liquor vs working-fluid boiling point ===")
# H2SO4 ice liquidus (approx, CRC concentrative properties): wt% -> Tf (C)
h2so4 = [(0, 0), (2, -0.8), (5, -2.1), (8, -3.7), (10, -5.0), (15, -9.0), (20, -14.5), (25, -21.5), (30, -32)]
def tf_acid(wt):
    for (w1, t1), (w2, t2) in zip(h2so4, h2so4[1:]):
        if w1 <= wt <= w2:
            return t1 + (t2 - t1) * (wt - w1) / (w2 - w1)
    return -40
for feed, acid, rec in ((2.5, 2.5, 0.8), (2.5, 1.0, 0.8), (2.5, 2.0, 0.85), (2.5, 3.0, 0.9), (10, 2.5, 0.8), (10, 1.0, 0.8), (15, 2.5, 0.8)):
    resid = (1 - rec) * feed / C_eut
    acid_res = acid / resid
    wt = acid_res / 1200 * 100
    tf = tf_acid(wt) - 1.6  # additive with CuSO4 eutectic depression (Zdanovskii-type rough)
    print(f"Cu {feed} g/L acid {acid} g/L rec {rec}: residual acid {acid_res:.0f} g/L (~{wt:.1f} wt%) -> liquor Tf ~ {tf:.1f} C")
# max acid for which butane at 0.87 bar (-4.4 C) with 1 K approach can still freeze: Tf >= -3.4
for feed in (2.5, 10):
    for rec in (0.8,):
        resid = (1 - rec) * feed / C_eut
        # Tf_acid must be >= -3.4+1.6 = -1.8 -> wt ~ 4.3%
        wt_max = 4.3
        print(f"Cu {feed} g/L rec {rec}: residual acid must be <= ~{wt_max*12:.0f} g/L -> feed acid <= {wt_max*12*resid:.2f} g/L")

print("\n=== Idea 10 impurities x24 ===")
for mg in (1, 2):
    mg_res = mg * 24
    mgso4 = mg_res * 120.37 / 24.305
    print(f"Mg {mg} g/L -> {mg_res} g/L Mg = {mgso4:.0f} g/L MgSO4 (~{mgso4/1250*100:.0f} wt%) vs MgSO4-ice eutectic ~17 wt% at -3.9 C")
for fe in (1,):
    print(f"Fe {fe} g/L -> {fe*24} g/L Fe = {fe*24*151.9/55.85:.0f} g/L FeSO4")
for cl in (0.1, 0.5):
    print(f"Cl {cl} g/L in PLS -> {cl*24:.1f} g/L in mother liquor; 8% adhering liquor on crystals -> electrolyte at 45 g/L Cu gets ~{cl*24*0.08/1.3/0.254*45:.0f} mg/L Cl? (limit ~25-30 mg/L)")

print("\n=== Engine output (Carnot x eta) ===")
L = 333.0  # kJ/kg ice
for fluid, Tb, cases in (("propane", -7.0, ((-35, 7), (-40, 7), (-45, 7))), ("butane", -3.0, ((-35, 6), (-40, 6), (-45, 6)))):
    for Ta, appr in cases:
        Tc = Ta + appr
        eta = 1 - (Tc + 273.15) / (Tb + 273.15)
        print(f"{fluid} boil {Tb} C, air {Ta} C, cond {Tc} C: Carnot {eta*100:.1f}% -> {L*eta:.1f} kJ/kg; x0.5 = {L*eta*0.5:.1f}")
EW = 2.0  # kWh/kg Cu
for ice, w in ((494, 12), (494, 15), (492, 6), (492, 9), (123, 6), (123, 9), (77, 7.6), (117, 7.6)):
    print(f"ice {ice} kg/kg Cu x {w} kJ/kg = {ice*w/3600:.2f} kWh/kg Cu = {ice*w/3600/EW*100:.0f}% of {EW} kWh/kg EW")

print("\n=== Natural-draft dry tower draft ===")
def rho_air(TC):
    return 101325 * 0.02897 / (8.314 * (TC + 273.15))
for Ta in (-35, -40, -45):
    for Tout in (-37.0, -29.0, -23.0):
        if Tout <= Ta:
            continue
        for H in (60, 80):
            dp = 9.81 * H * (rho_air(Ta) - rho_air(Tout))
            print(f"ambient {Ta} C, exhaust {Tout} C (<= butane cond. T), H {H} m: draft {dp:.0f} Pa")

print("\n=== Idea 11 scale: 10 kt Cu/yr ===")
ice = 10e6 * 494
Q = ice * L * 1e3
for days in (150, 80, 52):
    print(f"freezing season {days} d: heat rate {Q/(days*86400)/1e6:.0f} MW")
print("electricity 4.5 MW x 3600 h =", 4.5*3600/1e3, "GWh vs EW need", 10e6*2.0/1e9*1e3/1e3, "GWh (10 kt x 2.0 kWh/kg)")
ice_rate = 127e6 / (L * 1e3)
print(f"127 MW -> ice {ice_rate:.0f} kg/s = {ice_rate*3.6:.0f} t/h = {ice_rate*86.4:.0f} t/d")
air = 127e6 / (1005 * 5)
print(f"air flow for 127 MW at 5 K rise: {air:.0f} kg/s = {air/1.48:.0f} m3/s")
# Yakutsk hours below -35 (normal model)
from math import erf, sqrt
def Phi(z): return 0.5 * (1 + erf(z / sqrt(2)))
months = {"Nov": (-28, 30), "Dec": (-38, 31), "Jan": (-39, 31), "Feb": (-34, 28), "Mar": (-21, 31)}
for sd in (6, 7):
    hrs = {k: Phi((-35 - mu) / sd) * d * 24 for k, (mu, d) in months.items()}
    print(f"Yakutsk SD {sd}: hours <= -35 C ~ {sum(hrs.values()):.0f} h ({ {k: round(v) for k, v in hrs.items()} })")
