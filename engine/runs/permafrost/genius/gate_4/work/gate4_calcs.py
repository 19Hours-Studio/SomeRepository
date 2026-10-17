# Gate 4 kill test - KILLER (margin) and CHAIN (ratio) for 8 ideas.
# Every decisive input is tagged with its source (URL from web search) or marked
# PHYS (physical constant / textbook law) or ASSUMP (engineering assumption, stated).
import math

RUBUSD = 84.0                       # ledger
CRF = 3485.0 / 28000.0              # ledger-implied capital charge: B capital 41% x $8,500 = $3,485/t vs $28k per annual t
print(f"capital charge implied by ledger B: {CRF:.3f}/yr")

def e_ice(T):   # Pa, Murphy & Koop 2005 (PHYS)
    return math.exp(9.550426 - 5723.265 / T + 3.53068 * math.log(T) - 0.00728332 * T)

def rho_v(T, rh=1.0):  # kg/m3 water vapour
    return rh * e_ice(T) * 0.018015 / (8.314 * T)

def verdict(m, r):
    if m < 0.3 or r < 1.1:
        return "DEAD"
    if m >= 1 and r >= 1.5:
        return "ALIVE"
    return "WOUNDED"

out = {}

# ---------------------------------------------------------------- IDEA 1
print("\n=== IDEA 1 Freeze-Engine Vitriol Winning")
Lf = 334e3                     # J/kg PHYS
cu_pls = 2.0                   # g/L; heap-leach PLS 0.5-8 g/L (911metallurgist SX training), patent avg 0.5-3 g/L
K = 0.1                        # ASSUMP ice/liquid distribution coefficient (layer freezing)
cu_sat = 40.0                  # g/L, ~CuSO4.5H2O saturation near 0 C in acidic sulfate (PHYS, approx)
CF = cu_sat / cu_pls
f = 1 - CF ** (-1 / (1 - K))   # Rayleigh: C/C0 = (1-f)^(K-1)
print(f"concentration factor {CF:.0f}, fraction frozen f = {f:.3f}")
dTf0 = 1.0                     # K initial freezing-point depression of PLS (ASSUMP, ~40-60 g/L sulfates)
# mean freezing-point depression weighted over the frozen mass
n = 2000
mean_dTf = sum(dTf0 * (1 - (i + 0.5) / n * f) ** (K - 1) for i in range(n)) / n
dT_evap, dT_cond, eta2, parasitic = 5.0, 10.0, 0.6, 0.10   # ASSUMP approaches, 2nd-law eff (generous), pumps/fans

def kJ_per_kg(Tair_C):
    Th = 273.15 - mean_dTf - dT_evap
    Tc = 273.15 + Tair_C + dT_cond
    return Lf * (1 - Tc / Th) * eta2 * (1 - parasitic) / 1e3

liq_per_kgCu = 1000.0 / cu_pls * f   # kg liquor frozen per kg Cu
EW_req = 2.0                         # kWh/kg Cu (industrial EW ~2 V, ~2 kWh/kg: investigadores.anid.cl work 56823)
faraday = 2 * 96485 / 0.063546 * 2.0 / 0.90 / 3.6e6
print(f"Faraday check: 2.0 V, 90% CE -> {faraday:.2f} kWh/kg Cu")
for T in (-31.0, -35.0, -40.0, -50.0):
    e = kJ_per_kg(T)
    av = e * liq_per_kgCu / 3600
    print(f"Tair {T:5.1f} C: {e:5.1f} kJ/kg frozen (idea claims 15-30) -> {av:4.2f} kWh/kg Cu, margin {av/EW_req:4.2f}")
# Decisive case: -31 C = Yakutsk Nov-Mar mean (Jan -38.6 C kupi.com; Nov ~ -26 C), i.e. the 150-day freeze season used below
av1 = kJ_per_kg(-31.0) * liq_per_kgCu / 3600
m1 = av1 / EW_req
# CHAIN: ledger B, $8,500/t Cu; heap-leach SX-EW variant on diesel power ($0.49/kWh ledger)
now1 = 8500.0
energy = 0.11 * now1           # ~ EW power 2 kWh/kg x $0.49 = $980/t, consistent with 11%
sx_opex = 0.15 * now1 / 3      # SX ~1/3 of processing (ASSUMP)
inbound_diesel = 0.03 * now1 / 2
heat_kWth = liq_per_kgCu * 1000 * Lf / (150 * 86400) / 1000   # kWth per (t Cu/yr), 150-day freeze season
kWe = EW_req * 1000 / (150 * 24)                               # kWe per (t Cu/yr) to run EW in winter only
pond_m2 = 1000.0 / cu_pls * 1.0 / 3.0                          # m2 per (t/yr): whole summer PLS stored 3 m deep
capex_add = heat_kWth * (100 + 100) + kWe * 3000 + pond_m2 * 20 + pond_m2 * 5 + 1.33 * 1500 - 1500
#            radiators+ice coils $/kWth (ASSUMP) | ORC $3000/kWe | lined pond $20/m2 + ice yard | EW tankhouse x2.33 | SX plant avoided
print(f"freeze duty {heat_kWth:.1f} kWth, ORC {kWe:.2f} kWe, pond {pond_m2:.0f} m2 per t/yr Cu; net added capex ${capex_add:,.0f} per t/yr")
save1 = min(1, m1) * (energy + inbound_diesel) + sx_opex - 150.0   # $150/t freeze-plant O&M (ASSUMP)
with1 = now1 - save1 + capex_add * CRF
r1 = now1 / with1
print(f"CHAIN: now ${now1:,.0f}/t, with idea ${with1:,.0f}/t, ratio {r1:.2f}")
# even with margin forced to 1:
with1b = now1 - ((energy + inbound_diesel) + sx_opex - 150.0) + capex_add * CRF
print(f"  (if freezing supplied ALL EW power: ${with1b:,.0f}/t, ratio {now1/with1b:.2f})")
out[1] = (m1, r1, av1, now1, with1)

# ---------------------------------------------------------------- IDEA 2
print("\n=== IDEA 2 Frozen-gravel dry gold plant")
por, rs, ri = 0.35, 2650.0, 917.0       # saturated alluvial sand porosity (ASSUMP 0.3-0.4), densities PHYS
ice_per_t = por * ri / ((1 - por) * rs) * 1000   # kg ice per t of mineral grains
left = ice_per_t * 0.25                 # generous: breaker + air knock 3/4 of the ice off as chips
spec = 5.0                              # kg/t (0.5%) dry, free-flowing feed for HTR (Carrara: dry free-flowing 40-800 um; BGS sands preheated to 110 C)
req2 = left - spec
rv = rho_v(243.15)                      # bone-dry air leaving saturated at -30 C
air_m3_per_t = 1000.0                   # ASSUMP pneumatic separator, ~1 kg solids per m3 air
av2 = air_m3_per_t * rv
m2 = av2 / req2
print(f"pore ice {ice_per_t:.0f} kg/t; left on grains {left:.0f} kg/t; must remove {req2:.0f} kg/t")
print(f"e_ice(-30C) = {e_ice(243.15):.1f} Pa, sat vapour density {rv*1e3:.3f} g/m3 -> air needed {req2/rv:,.0f} m3/t (at 70% RHice: {req2/(0.3*rv):,.0f})")
print(f"available 'free drying' at {air_m3_per_t:.0f} m3/t: {av2:.2f} kg/t -> margin {m2:.4f}")
# CHAIN ledger A, $2,550/oz; physical 78%, other 22% (MET $474/oz + $87)
now2 = 2550.0
met = 474.0 / now2 * 100; oth = 22 - met
phys = 78 - 5 - 1 + 5 - 3 - 3    # processing -25%, energy -1, frozen-digging premium +5, capital -20% (winter use), camp -15%
rec = 1.05                       # +5% gold from fine-gold capture (ASSUMP, generous)
idx2 = phys / rec + met + oth / rec
r2 = 100 / idx2
print(f"CHAIN: index {idx2:.1f} -> with idea ${now2*idx2/100:,.0f}/oz, ratio {r2:.2f}")
out[2] = (m2, r2, req2, av2, now2 * idx2 / 100)

# ---------------------------------------------------------------- IDEA 3
print("\n=== IDEA 3 Winter Wind Deflation Placer")
rate_mm = 1.0                   # idea: up to ~1 mm/day of layer freed (and 1 km2 per season)
ice_vol = 0.25                  # ASSUMP volumetric ice of saturated pay gravel (0.25-0.35)
req3 = rate_mm * 1e-3 * ice_vol * ri       # kg/m2/day (= mm w.e./day)
season_m3 = rate_mm * 1e-3 * 1e6 * 150
av3 = 0.07                      # mm w.e./day: tundra surface sublimation (UAF Imnavait 0.06-0.07; six Alaska sites 0.08-0.15)
m3 = av3 / req3
snowfall = 0.08 / 0.21          # Alaska: sublimation ~21% of solid precipitation -> snowfall mm w.e./day
print(f"required {req3:.3f} kg/m2/day (1 km2 -> {season_m3:,.0f} m3/season); available {av3} -> margin {m3:.2f}")
print(f"snowfall onto pad ~{snowfall:.2f} mm w.e./day > sublimation -> net ~0 unless snow is cleared")
print(f"pad needed for 150,000 m3 at measured rate: {1/m3:.1f} km2")
now3 = 2550.0
phys3 = 78 - 10 - 2 - 2 + 5 + 20   # wash volume cut (-10), smaller plant (-2), pumps (-2), frozen ripping (+5), spread/harrow/sweep/rehandle (+20)
idx3 = phys3 + 22
r3 = 100 / idx3
print(f"CHAIN: index {idx3:.0f} -> ${now3*idx3/100:,.0f}/oz, ratio {r3:.2f}")
out[3] = (m3, r3, req3, av3, now3 * idx3 / 100)

# ---------------------------------------------------------------- IDEA 4
print("\n=== IDEA 4 Etched thermokarst freight canals")
depth_req, years = 1.5, 5.0      # ASSUMP barge depth 1.5 m, 'within a few years' = 5
req4 = depth_req / years         # m/yr
av4 = 0.062                      # m/yr thaw subsidence below yedoma lakes, Yukechi (Ulrich et al. 2017, epic.awi.de/id/eprint/44608)
m4 = av4 / req4
print(f"required {req4:.2f} m/yr, available {av4} m/yr -> margin {m4:.2f}; years to 1.5 m: {depth_req/av4:.0f}")
print(f"  (Fedorov & Konstantinov boundary maximum 0.15 m/yr -> margin {0.15/req4:.2f})")
now4 = 23000.0                   # rub/t settlement coal (ledger C)
L, F = 300.0, 200e3              # ASSUMP: 300 km winter-road leg replaced, 200 kt/yr through the canal
mats = 0.2e6 * RUBUSD            # rub/km: 2 banks x 10 m XPS mats ~$10/m2 (ASSUMP)
canal = mats * CRF * L / F
with4 = now4 - L * 20 + L * 4 + canal   # ledger: winter road 20 rub/t-km, barge 3-5 rub/t-km
r4 = now4 / with4
print(f"CHAIN: canal capital {canal:,.0f} rub/t; with idea {with4:,.0f} rub/t; ratio {r4:.2f}")
out[4] = (m4, r4, req4, av4, with4)

# ---------------------------------------------------------------- IDEA 5
print("\n=== IDEA 5 Snow-Sculpted Under-Ice Sluice")
V_bulk, poro = 100e3, 0.4        # ASSUMP one washing plant's season of screened sand
d, s, Cf, g = 1e-3, 2.65, 0.004, 9.81
T = 120 * 86400                  # keel-developed under-ice period
def Qreq(U, h):
    th = Cf * U**2 / ((s - 1) * g * d)
    phi = 8 * max(th - 0.047, 0) ** 1.5
    qs = phi * math.sqrt((s - 1) * g * d**3)       # m2/s solids (Meyer-Peter Mueller)
    conc = qs / (U * h)
    return V_bulk * (1 - poro) / (conc * T), th
for U, h in ((1.0, 0.4), (1.5, 0.4), (2.0, 0.3)):
    q, th = Qreq(U, h)
    print(f"U {U} m/s, h {h} m: Shields {th:.2f}, required winter discharge {q:5.1f} m3/s")
req5, _ = Qreq(1.5, 0.4)
frac = 162.7 / 3109.0            # Kolyma at Kolymskaya: April mean / annual mean (GRDC via compositerunoff.sr.unh.edu), HPP-regulated
av5 = 10.0 * frac                # generous placer-valley river, 10 m3/s annual mean; small streams freeze to the bed
m5 = av5 / req5
print(f"available {av5:.2f} m3/s ({frac*100:.1f}% of annual mean) -> margin {m5:.3f}")
now5 = 2550.0
phys5 = 78 - 10 - 3 - 2 + 1 + 6  # no summer washing ops (-10), pump diesel (-3), wash plant capital (-2), winter crew (+1), windrow placement (+6)
idx5 = phys5 + 22
r5 = 100 / idx5
print(f"CHAIN: index {idx5} -> ${now5*idx5/100:,.0f}/oz, ratio {r5:.2f}")
out[5] = (m5, r5, req5, av5, now5 * idx5 / 100)

# ---------------------------------------------------------------- IDEA 6
print("\n=== IDEA 6 Sub-ambient photonic permafrost shields")
def tdd(months):  # (mean C, days)
    return sum(t * dd for t, dd in months if t > 0)
noril = [(6.0, 30), (14.4, 31), (10.0, 31), (3.0, 30)]      # Norilsk Jun-Sep means (climate-zone.com; Jul 13.8 kupi.com)
yak = [(7.5, 31), (16.4, 30), (19.5, 31), (15.2, 31), (6.1, 30)]  # Yakutsk May-Sep (Jul ~+20: search sources)
k_th, X, rho_d, w = 2.0, 2.0, 2000.0, 0.07                    # ASSUMP 2 m gravel pad, 7% moisture
Lv = rho_d * w * Lf
tdd_allow = X**2 * Lv / (2 * k_th) / 86400                    # Stefan
avail_dT = 4.9 * 0.48            # Raman 2014 clear-sky 4.9 K (convection-shielded) x 48% clear/partly-cloudy chance on Norilsk's clearest day (WeatherSpark)
for name, mon in (("Norilsk", noril), ("Yakutsk", yak)):
    TDD = tdd(mon); days = sum(dd for t, dd in mon)
    need = (TDD - tdd_allow) / days
    print(f"{name}: air TDD {TDD:.0f}, allowable surface TDD {tdd_allow:.0f}, required mean sub-ambient dT {need:.1f} K; available {avail_dT:.1f} K -> margin {avail_dT/need:.2f}")
TDDn = tdd(noril); req6 = (TDDn - tdd_allow) / sum(dd for t, dd in noril)
m6 = avail_dT / req6
now6 = 8500.0
save6 = 0.41 * 0.05 * 0.6 + 0.005   # permafrost-protection items ~5% of capex, film saves 60% of them; +0.5% failure avoidance (ASSUMP)
with6 = now6 * (1 - save6)
r6 = now6 / with6
print(f"CHAIN: with idea ${with6:,.0f}/t Cu, ratio {r6:.3f}")
out[6] = (m6, r6, req6, avail_dT, with6)

# ---------------------------------------------------------------- IDEA 7
print("\n=== IDEA 7 Grinding mill brews its lixiviant")
E_mech = 26.9e11 / 1e3 / 3.6e6   # kWh per kg NH3, best mechanocatalysis (Nat Commun 2025, s41467-025-63145-3)
mill = 15.0                      # kWh/t ore, ASSUMP ball-mill specific energy (Bond Wi ~13-15)
av7 = mill / E_mech              # kg NH3 / t ore, upper bound (all mill energy as effective as a dedicated reactor)
S = 10 * (8 * 32.06 / (4.5 * 58.69)) + 10 * (2 * 32.06 / 63.55)   # kg S/t ore for 1% Ni (pentlandite) + 1% Cu (chalcopyrite)
req7 = S / 32.06 * 2 * 17.03     # kg NH3/t ore tied up as (NH4)2SO4 (Sherritt chemistry, nickelinstitute.org)
m7 = av7 / req7
print(f"mechanocatalysis {E_mech:.0f} kWh/kg NH3 (Haber-Bosch ~8); available {av7*1000:.0f} g/t ore; required {req7:.1f} kg/t -> margin {m7:.4f}")
print(f"  even vs 1 kg/t loss-only make-up: margin {av7/1.0:.3f}")
now7 = 8500.0
nh3_per_t_metal = req7 / 20.0 * 1000         # kg NH3 per t (Ni+Cu)
h2 = nh3_per_t_metal * 3 * 1.008 / 17.03     # kg H2 per t metal
p_npp = 6.45 / RUBUSD                         # $/kWh Baimskaya floating NPP (ledger)
h2_cost = h2 * 52 * p_npp                     # 52 kWh/kg H2 electrolysis (ASSUMP)
with7 = now7 - 0.03 * now7 - (0.05 - 0.015) * now7 + h2_cost + 2500 * p_npp + 0.02 * now7 + 0.20 * 0.41 * now7
#       inbound gone | concentrate->metal freight | H2 | metal EW 2.5 MWh/t | dry grinding +30% energy | +20% capital for leach/recovery plant
r7 = now7 / with7
print(f"H2 {h2:.0f} kg/t metal -> ${h2_cost:,.0f}/t; CHAIN with idea ${with7:,.0f}/t, ratio {r7:.2f}")
out[7] = (m7, r7, req7, av7, with7)

# ---------------------------------------------------------------- IDEA 8
print("\n=== IDEA 8 Cold-Dry-Air Charge Sorting")
feed, conc, rec8 = 1.80, 4.0, 0.771     # dry electrostatic on Li pegmatite (Minerals Eng. 2022 lepidolite study, ResearchGate 362691254)
cut = (conc / feed) / rec8
req8 = 5.0                              # idea's lower bound of 5-20x tonnage cut
m8 = cut / req8
dms_cut = (5.7 / 0.6) / 0.90            # DMS on low-grade spodumene (Springer JSM 2025)
print(f"electrostatic mass cut {cut:.2f}x at {rec8*100:.0f}% rec (DMS benchmark {dms_cut:.1f}x at 90%) -> margin {m8:.2f}")
now8 = 10200.0
conc_share = 0.18 * 0.35 + 0.42 * 0.20 + 0.09 * 0.30 + 0.14 * 0.15   # ASSUMP concentrator share of delivered cost
idx8 = 1 - conc_share * 0.5 + 0.25 * (0.85 / rec8 - 1) + (0.18 * 0.65 + 0.42 * 0.5) * 0.3
#        tribo at half the concentrator cost | more ore mined for lower recovery | 1.5x concentrate mass through the chemical plant
with8 = now8 * idx8
r8 = now8 / with8
print(f"CHAIN: concentrator share {conc_share*100:.1f}%, with idea ${with8:,.0f}/t LCE, ratio {r8:.2f}")
out[8] = (m8, r8, req8, cut, with8)

print("\n=== SUMMARY")
for i in range(1, 9):
    m, r = out[i][0], out[i][1]
    print(f"IDEA {i}: MARGIN {m:.3g}  RATIO {r:.2f}  -> {verdict(m, r)}")
