"""Idea 2 - Freeze-engine vitriol winning. All estimates in code.
Sources (see LOG.md):
 [A] CuSO4 solubility 14.3 g/100 g H2O at 0 C (CRC Handbook) -> ~57 g/L Cu in pure water; lower with H2SO4 / other sulfates.
 [B] Glaciothermal engine: latent heat of freezing water boils organic fluid, condensed by polar air, 9-11 % net
     efficiency at interior sites (Smith, PhD thesis, Univ. Tasmania); Lock 1989 Arctic 42(3):253 (~5 %, NH3, 0 C vs -25 C).
 [C] Isolated Far-North diesel power 10-40 RUB/kWh (ipolytech.elpub.ru); 1 USD ~ 90 RUB.
 [D] Udokan (Zabaykalsky, permafrost) runs leach-SX-EW, cathode start Sept 2026 (Kitco/Reuters).
 [E] Copper EW specific energy ~2.0 kWh/kg Cu (standard industry figure, cell voltage ~2 V at ~90 % current efficiency).
ASSUME flags mark assumptions.
"""
import math

Lf = 334.0  # kJ/kg ice
def engine_kj_per_kg(T_freeze_C, T_air_C, dT_evap=3.0, dT_cond=12.0, frac_carnot=0.55):
    Th = T_freeze_C - dT_evap + 273.15
    Tc = T_air_C + dT_cond + 273.15
    eta = (1 - Tc / Th) * frac_carnot
    return Lf * eta, eta

print("== Round 1: electricity per kg of ice ==")
for Tair in (-25, -30, -35, -40, -45):
    w, eta = engine_kj_per_kg(-3.0, Tair)
    print(f"air {Tair} C: eta={eta*100:4.1f}%  -> {w:4.1f} kJ_e per kg ice")
print("cross-check: Smith thesis 9-11% net at interior Antarctic sites (colder air); Lock 1989 ~5% at -25 C")

EW = 2.0 * 3600  # kJ per kg Cu [E]

def freeze_balance(c0, cu_sat=45.0, R=0.80, Fe0=2.0, acid0=4.0, Tair=-35.0, fe_max=90.0, acid_max=400.0):
    """c0 g/L Cu in PLS. Freeze until a fraction phi of liquor remains. Cu crystallises above cu_sat.
    Returns ice per kg Cu, power per kg Cu, Fe and acid in final brine."""
    phi = c0 * (1 - R) / cu_sat
    ice_per_L = 1.0 * (1 - phi)          # kg ice per L PLS (density ~1)
    cu_per_L = c0 * R / 1000.0            # kg Cu per L
    ice_per_kgcu = ice_per_L / cu_per_L
    w, _ = engine_kj_per_kg(-3.0, Tair)
    power = ice_per_kgcu * w
    return dict(phi=phi, ice=ice_per_kgcu, power_ratio=power / EW, Fe=Fe0 / phi, acid=acid0 / phi)

print("\n== Round 1b: ice per kg Cu and energy self-sufficiency (R=80 %, Cu_sat=45 g/L ASSUME in mixed sulfate) ==")
for c0 in (1, 2, 2.5, 3, 5, 10):
    r = freeze_balance(c0)
    print(f"PLS {c0:>4} g/L Cu: phi={r['phi']:.4f} ice={r['ice']:6.0f} kg/kg Cu  engine/EW={r['power_ratio']:.2f}  final Fe={r['Fe']:6.0f} g/L acid={r['acid']:6.0f} g/L")

print("\n== Round 2: iron/acid ceiling. Fe3+ sulfate hydrates and acid limit the concentration factor ==")
print("A PLS with Fe0=2 g/L, acid 4 g/L: at 2.5 g/L Cu final Fe = 2/phi ... too high -> Fe co-crystallises.")
print("Repair: (a) oxide-ore heap (malachite/brochantite) PLS with Cu/Fe >= 2, (b) acid-limited: run heap at low acid,")
print("(c) stop freezing at Fe ceiling and bleed brine back to heap; recover only Cu above saturation in the bleed-limited liquor.")
for Fe0, acid0 in ((0.5, 2.0), (1.0, 3.0), (2.0, 4.0)):
    for c0 in (2.5, 4.0):
        # maximum concentration factor set by Fe and acid ceilings
        cf_max = min(90.0 / Fe0, 400.0 / acid0)
        phi_min = 1 / cf_max
        R = max(0.0, 1 - phi_min * 45.0 / c0)
        print(f"Fe0={Fe0} acid0={acid0} c0={c0}: max CF={cf_max:5.0f}, Cu recovery per freeze season={R*100:4.0f}%")

print("\n== Round 3: hardware & cost per t Cu (10 kt/yr cathode, PLS 2.5 g/L, Fe 0.5, acid 2) ==")
cap_t = 10000.0
c0, R = 2.5, 0.80
r = freeze_balance(c0, R=R, Fe0=0.5, acid0=2.0)
ice_t = r['ice'] * cap_t  # t ice/yr
season_s = 150 * 86400   # ASSUME 150 days with air <= -25 C (Chara/Udokan, Jan mean ~ -33 C)
Q_MW = ice_t * 1e3 * Lf * 1e3 / season_s / 1e6
w, eta = engine_kj_per_kg(-3.0, -35.0)
P_MWe = ice_t * 1e3 * w * 1e3 / season_s / 1e6
print(f"ice {ice_t/1e6:.2f} Mt/yr; heat rejection {Q_MW:.0f} MWth; turbine {P_MWe:.1f} MWe; EW needs {cap_t*1e3*EW*1e3/season_s/1e6:.1f} MWe if EW runs only in winter")
# Design A: harvested ice crystallizer (direct-contact propane boiling in the liquor, wash column)
crf, om = 0.12, 0.03
designs = {
  'A direct-contact crystallizer + wash column': dict(cryst=1200.0 * ice_t / (season_s / 86400) / 1.0, acc=130.0, turb=1500.0),
  'B static ice-on-panel in the storage pond (no harvest)': None,
}
cryst_A = 1200.0 * (ice_t / (season_s / 86400))  # $ per (m3/day) capacity ASSUME freeze-desal ~1000-1500
acc = 130.0 * Q_MW * 1e3   # $/kWth air-cooled condenser ASSUME (power-plant ACC ~100-150)
turb = 1500.0 * P_MWe * 1e3
capA = cryst_A + acc + turb
# Design B: evaporator panels hang in the pond; ice grows in place on them all winter (Stefan), meltwater in spring
k_ice, rho_ice = 2.2, 917.0
dT_panel = 6.0
delta = math.sqrt(2 * k_ice * dT_panel * season_s / (rho_ice * Lf * 1e3))
kg_per_m2 = 2 * rho_ice * delta  # both faces
area = ice_t * 1e3 / kg_per_m2
panel_cost = 60.0  # $/m2 HDPE/steel pillow plate ASSUME
capB = area * panel_cost + acc + turb
print(f"Stefan ice on panel at dT={dT_panel} K over season: {delta:.2f} m per face -> {kg_per_m2:.0f} kg/m2; panel area {area/1e6:.2f} km2")
for name, cap in (("A crystallizer", capA), ("B ice-on-panel pond", capB)):
    ann = cap * (crf + om)
    labour = 1.5e6
    per_t = (ann + labour) / cap_t
    print(f"{name}: capex ${cap/1e6:.0f}M -> {per_t:,.0f} $/t Cu (annualised + O&M + labour)")

# baseline: SX + EW on diesel power
diesel = 30.0 / 90.0  # $/kWh [C] mid-range
sx_opex = 150.0       # $/t Cu ASSUME extractant/diluent losses, SX power, crud
sx_capex_ann = 4000.0 * 0.15  # $/annual t SX plant ASSUME ~ $4k/annual t, annualised
ew_power = 2.0 * 1000 * diesel
base = sx_opex + sx_capex_ann + ew_power
print(f"baseline SX ({sx_opex + sx_capex_ann:,.0f}) + diesel EW power ({ew_power:,.0f}) = {base:,.0f} $/t Cu")
print(f"freeze route replaces both; ratio baseline/freeze: A {base/((capA*(crf+om)+1.5e6)/cap_t):.2f}x  B {base/((capB*(crf+om)+1.5e6)/cap_t):.2f}x")

print("\n== Round 4: strongest regime = colder air and the pond as crystallizer, panels re-used as summer heap-solution heaters ==")
for Tair in (-30, -40, -45):
    w, eta = engine_kj_per_kg(-3.0, Tair)
    print(f"air {Tair}: {w:.1f} kJ/kg ice -> engine/EW at 2.5 g/L = {r['ice']*w/EW:.2f}")
