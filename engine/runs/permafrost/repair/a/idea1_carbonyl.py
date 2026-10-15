"""Idea 1 - Carbonyl nickel riding in a gas trunk line. All estimates in code.
Sources (see LOG.md):
 [A] Ni(CO)4 vapour pressure: Chemeo/NIST correlation ln P[kPa] = 14.5275 - 2836.86/(T - 28.762), 228-337 K
     (checks: gives 101 kPa at 315.5 K = normal bp 42-43 C).
 [B] Power of Siberia: 38 bcm/yr, 1420 mm, working pressure 9.8 MPa, permafrost route (gazprom.com/projects/power-of-siberia).
 [C] Thermo data (NIST/CRC): dHf Ni(CO)4(g) = -602.9 kJ/mol, S = 410.6 J/molK; CO(g) dHf=-110.53, S=197.66; Ni(s) S=29.87.
 [D] Ni concentrate payability 70-76% (Centaurus Jaguar FS 2024: 76%; CRU via RNC: conventional 70-75%).
 [E] Kun-Manie: PFS needs a 338 km road to BAM rail (Mining Weekly 2018).
 [F] Metal-carbonyl guard beds / decomposition guard catalysts exist (US6165428; Clariant ActiSorb 400).
 [G] NIOSH IDLH: Ni(CO)4 2 ppm; H2S 50 ppm.
Assumptions flagged with 'ASSUME'.
"""
import math
R = 8.314

def psat_kpa(T):
    return math.exp(14.5275 - 2836.86 / (T - 28.762))

print("== Round 1: dew point check (ideal gas, no enhancement factor => conservative) ==")
P_line = 9800.0  # kPa [B]
for TC in (20, 5, 0, -5, -10, -20, -25):
    T = TC + 273.15
    ps = psat_kpa(T)
    print(f"T={TC:>4} C  Psat={ps:6.2f} kPa  max mol% at 9.8 MPa (100% sat)={100*ps/P_line:6.3f}  at 70% sat={70*ps/P_line:6.3f}")

# throughput -> Ni per year
bcm = 38e9
mol_gas = bcm / 0.024055  # Russian standard m3 at 20 C, 101.325 kPa
print(f"\nmol gas/yr = {mol_gas:.3e}")
for x in (0.001, 0.0005, 0.0004, 0.0003, 0.0002):
    t_ni = mol_gas * x * 58.69e-6
    print(f"dose {x*100:.3f} mol% -> Ni {t_ni/1e3:7.1f} kt/yr ; Ni(CO)4 liquid {mol_gas*x*170.73e-3/3.15e7:5.2f} kg/s")

print("\n== Round 1b: thermodynamic stability vs CO partial pressure ==")
dH = -602.9 - 4 * (-110.53)   # kJ/mol for Ni + 4CO -> Ni(CO)4(g)
dS = (410.6 - 29.87 - 4 * 197.66) / 1000  # kJ/molK
print(f"dH={dH:.1f} kJ/mol dS={dS*1000:.1f} J/molK")
def K(Tc):
    T = Tc + 273.15
    dG = dH - T * dS
    return math.exp(-dG / (R * 1e-3 * T))  # bar^-3
x_ni = 0.0004
p_ni = x_ni * 98.0  # bar
for Tc in (25, 50, 60, 70, 80, 90):
    pco = (p_ni / K(Tc)) ** 0.25
    print(f"T={Tc} C K={K(Tc):.3g}  min p_CO={pco:.3f} bar = {100*pco/98:.3f} mol% CO (for 0.04% Ni(CO)4)")

print("\n== decomposer at the receiving plant: residual Ni(CO)4 at equilibrium ==")
x_co = 0.0015 + 4 * x_ni  # stabiliser + released CO
for Tc in (150, 180, 200, 220):
    p_res = K(Tc) * (x_co * 98) ** 4
    print(f"T={Tc} C residual Ni(CO)4 = {1e6*p_res/98:.3f} ppm -> capture {100*(1-p_res/p_ni):.2f}%")

# heating the whole gas flow with a recuperator
m_gas = bcm * 0.68 / 3.15e7  # kg/s (0.68 kg/m3 methane-rich gas at 20C)
cp = 2.6  # kJ/kgK at ~6-10 MPa, ASSUME
dT_hot, approach = 190 - 5, 20.0
Q_total = m_gas * cp * dT_hot / 1e3  # MW
Q_net = m_gas * cp * approach / 1e3
fuel_m3 = Q_net * 1e6 * 3.15e7 / 0.9 / 34e6
print(f"gas {m_gas:.0f} kg/s; recuperated duty {Q_total:.0f} MW; net fired {Q_net:.0f} MW = {fuel_m3/1e6:.0f} Mm3/yr = {100*fuel_m3/bcm:.2f}% of throughput")
U, lmtd = 400.0, approach
area = Q_total * 1e6 / (U * lmtd)
print(f"recuperator area ~{area:,.0f} m2 (U=400 W/m2K ASSUME)")

print("\n== Round 2: hazard - toxic-equivalent H2S content (IDLH ratio [G]) ==")
for x in (0.001, 0.0004, 0.0002):
    ppm = x * 1e6
    print(f"Ni(CO)4 {ppm:.0f} ppm ~ H2S-equivalent {ppm*50/2/1e4:.1f} mol% H2S (IDLH ratio 25)")

print("\n== Round 3: cost per t Ni, carbonyl route vs selling concentrate ==")
price = 16500.0  # $/t Ni, ASSUME (LME 2024-26 range 15-18k)
gas_price = 0.10  # $/m3 at field, ASSUME (Russian domestic regulated ~ 5-6 RUB/m3 + margin)
conc_grade = 0.12   # ASSUME pentlandite concentrate 10-14% Ni
t_conc = 1 / conc_grade
road_km, road_rate = 338, 0.12   # [E] distance; ASSUME 0.10-0.15 $/t.km (winter/forest road, Russian Far East)
rail_km, rail_rate = 2500, 0.035  # ASSUME BAM/Transsib to smelter/port
freight = t_conc * (road_km * road_rate + rail_km * rail_rate)
for pay in (0.70, 0.76):
    conv = (1 - pay) * price + freight
    print(f"conventional: payability {pay:.2f}: value lost {(1-pay)*price:,.0f} + freight {freight:,.0f} = {conv:,.0f} $/t Ni")

ni_kt = 37.0
# CO and O2 for carbonylation (4 CO per Ni consumed - CO leaves with the gas) + stabiliser
co_per_ni = 4 + 0.0015 / x_ni  # mol CO / mol Ni
ch4_t = co_per_ni * 16.04 / 58.69  # t CH4 per t Ni (POX: 1 CH4 -> 1 CO + 2 H2)
gas_m3 = ch4_t * 1000 / 0.668
o2_t = co_per_ni * 0.5 * 32 / 58.69
asu_kwh = o2_t * 1000 * 0.30
print(f"CO per Ni = {co_per_ni:.2f} mol; CH4 {ch4_t:.2f} t/t Ni = {gas_m3:,.0f} m3 -> ${gas_m3*gas_price:,.0f}; O2 {o2_t:.2f} t, ASU {asu_kwh:,.0f} kWh")
# H2 co-product (2 per CO) covers NiO/FeO reduction: needs ~1.5-2 mol H2 per Ni (Ni + part of Fe)
h2 = 2 * co_per_ni
print(f"H2 co-produced {h2:.1f} mol/mol Ni vs ~2-3 needed for NiO + partial FeO reduction -> surplus burned for roaster/kiln heat")

def carbonyl_cost(capex_per_annual_t, crf=0.12, om_frac=0.04, other_opex=900.0, so2=400.0, receiver=None):
    cap = capex_per_annual_t * (crf + om_frac)
    if receiver is None:
        rec_capex = area * 1500 / (ni_kt * 1e3)   # $/annual t, $1500/m2 HP exchanger ASSUME
        rec_fuel = fuel_m3 * gas_price / (ni_kt * 1e3)
        receiver = rec_capex * (crf + om_frac) + rec_fuel
    gas_cost = gas_m3 * gas_price + asu_kwh * 0.05
    total = cap + other_opex + so2 + receiver + gas_cost
    return total, dict(capital=cap, opex=other_opex, so2=so2, receiver=receiver, gas_o2=gas_cost)

for capex in (8000, 12000, 18000):
    tot, parts = carbonyl_cost(capex)
    print(f"carbonyl capex {capex} $/annual t: total {tot:,.0f} $/t Ni  parts " + ", ".join(f"{k}={v:,.0f}" for k, v in parts.items()))

print("\n== Round 4: regime where the anchor is strongest - awaruite / pre-reduced feed (no roast, no SO2) ==")
for capex in (6000, 9000):
    tot, parts = carbonyl_cost(capex, so2=0.0, other_opex=600.0)
    conv = (1 - 0.73) * price + freight
    print(f"awaruite-type feed capex {capex}: {tot:,.0f} $/t Ni vs conventional {conv:,.0f} -> ratio {conv/tot:.2f}x")
# transport-only comparison (the step the anchor actually replaces)
pipe_marginal = (0.0015 + x_ni) * 1.0  # fraction of line capacity consumed by additives ~ 0.19%
tariff = 0.012  # $/1000m3/km ASSUME typical trunk tariff ~ 1-1.5 $/1000 m3 per 100 km
km = 300
transport_pipe = (pipe_marginal * 1000 * (1 / (x_ni)) ) # placeholder not used
# per t Ni: the additives occupy (x_ni + x_co) of the molar flow; charge that share of the tariff
mol_ni_per_t = 1e6 / 58.69
m3_occupied = mol_ni_per_t * (1 + 0.0015 / x_ni) * 0.024055
cost_pipe = m3_occupied / 1000 * tariff * km
print(f"pipeline share charged at tariff for {km} km: {m3_occupied:,.0f} m3 -> ${cost_pipe:,.2f} per t Ni vs truck+rail concentrate ${freight:,.0f} per t Ni")
