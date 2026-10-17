"""Gate 2 kill test: KILLER margin and CHAIN ratio for 8 ideas.
All decisive inputs carry a source tag [S#] (listed in SOURCES at the bottom) or are
marked ASSUMPTION. Ledger values are from TASK.md.
"""
import math

USD_RUB = 84.0                 # ledger
DIESEL_LHV = 35.8e6            # J/l, standard diesel lower heating value (ASSUMPTION, textbook)
BOILER = 0.85                  # ASSUMPTION
L_ICE = 334e3                  # J/kg, latent heat of fusion (constant)
RHO_ICE = 917.0                # kg/m3 (constant)
R = 8.314
G = 9.81

def crf(i, n):
    return i / (1 - (1 + i) ** -n)

print("=" * 70)
print("IDEA 1  Flash-unlocked refractory gold")
Tb = 2856 + 273.15             # Au normal boiling point [S1]
dHv = 324.4e3                  # Au enthalpy of vaporisation J/mol [S1]
T = 3000 + 273.15              # idea: ~3,000 C pulse
p_au = math.exp(-(dHv / R) * (1 / T - 1 / Tb))          # atm, Clausius-Clapeyron
kB = 1.380649e-23; m_au = 196.97 * 1.66054e-27
P = p_au * 101325
mflux = P / math.sqrt(2 * math.pi * m_au * kB * T) * m_au  # kg/m2/s Hertz-Knudsen
r = 0.5e-6
t_ev = (4 / 3 * math.pi * r ** 3 * 19300) / (mflux * 4 * math.pi * r ** 2)
evap_meas = 0.60               # >60% Au evaporated by FJH at ~3,400 K, <1 s [S2]
ret_avail = 1 - evap_meas      # upper bound on gold left in calcine
ret_req = 0.90                 # needed to compete with POX-route recovery (ASSUMPTION threshold)
m1 = ret_avail / ret_req
print(f"p_Au(3000C) = {p_au:.2f} atm ; 1-um Au particle evaporates in {t_ev*1e6:.0f} us")
print(f"retained available <= {ret_avail:.2f}, required >= {ret_req:.2f} -> MARGIN {m1:.2f}")
now_A = 2550.0                                           # ledger A $/oz
conc_g_t = 9.3e6 * 31.1035 / 4.3e6                       # POX-2 feed grade [S3]
oz_t = conc_g_t * 0.95 / 31.1035
pox_capex_oz = 431e6 / 9.3e6                              # [S3]
pox_opex_t = 250.0                                       # generous upper bound (ASSUMPTION, cf. $150-250/t saving [S4])
transport_t = (300 * 20 + 8000) / USD_RUB                # ledger: 300 km winter road + LORP barge
removed = pox_capex_oz + (pox_opex_t + transport_t) / oz_t
added = 939 * (41 / USD_RUB) / oz_t                      # 939 kWh/t FJH [S2]; 41 rub/kWh diesel (ledger)
with1 = now_A - removed + added
added_npp = 939 * (6.45 / USD_RUB) / oz_t
print(f"conc grade {conc_g_t:.1f} g/t ; removed POX+freight ${removed:.0f}/oz ; added flash power ${added:.0f}/oz")
print(f"CHAIN now {now_A:.0f} with {with1:.0f} $/oz RATIO {now_A/with1:.2f} (NPP-price power: {now_A/(now_A-removed+added_npp):.2f})")

print("=" * 70)
print("IDEA 2  Woven lay-flat crude line")
rho20 = 851.0                                            # ESPO density [S5]
Q = 0.2e9 / rho20 / (8760 * 3600)                        # m3/s
D = 0.1; A = math.pi * D ** 2 / 4; v = Q / A
Z = lambda nu: math.log10(math.log10(nu + 0.7))
B = (Z(11.28) - Z(5.81)) / (math.log10(313.15) - math.log10(283.15))   # Siberian Light slope [S6]
def nu_espo(Tc):
    Tk = Tc + 273.15
    z = Z(6.95) + B * (math.log10(293.15) - math.log10(Tk))            # ESPO 6.95 cSt @20C [S5]
    return 10 ** (10 ** z) - 0.7
Tcold = -57.8                                            # Kirensk record low [S7]
nu = nu_espo(Tcold) * 1e-6
rho = rho20 * (1 + 0.0008 * (20 - Tcold))
Re = v * D / nu
f = 64 / Re if Re < 2300 else 0.316 * Re ** -0.25
dP = f * (15000 / D) * rho * v ** 2 / 2 + rho * G * 100   # +100 m rise between skids (ASSUMPTION)
T_hoop = 77 * 6894.76 * (27 * 0.3048 / 2)                # LIFE burst 77 psi, 27 ft dia [S8]
P_work = T_hoop / 0.05 / 4                               # same strap on r=0.05 m, NASA SF 4
m2 = P_work / dP
print(f"Q={Q*3600:.1f} m3/h v={v:.2f} m/s ; nu(-57.8C)={nu*1e6:.0f} cSt Re={Re:.0f}")
print(f"required {dP/1e5:.0f} bar per 15 km ; available {P_work/1e5:.0f} bar -> MARGIN {m2:.1f} (vs 300-psi catalogue hose {20.7e5/dP:.2f})")
now_E = 82.0
hose_m = 549.69 / (10 * 0.3048)                          # aramid TPU 4" layflat $/m [S9]
capex2 = hose_m * 300e3
bbl = 0.2e9 / rho20 * 6.2898                             # bbl/yr (6.2898 bbl per m3)
line_bbl = capex2 * crf(0.12, 10) / bbl                  # hose only; skids/O&M excluded (generous)
with2 = now_E - 10 + line_bbl
print(f"hose ${hose_m:.0f}/m capex ${capex2/1e6:.1f}M -> ${line_bbl:.2f}/bbl ; CHAIN now 82 with {with2:.1f} RATIO {now_E/with2:.3f} (claim $1/bbl: {now_E/73:.3f})")

print("=" * 70)
print("IDEA 3  Bell-hole thaw-lift")
grade = 1.75                                             # g/m3 sands, Kolyma placer [S10]
rec = 0.85                                               # ASSUMPTION
ice = 0.20                                               # pore ice, gravel 'not much ice' [S11]
thaw_J = ice * RHO_ICE * L_ICE + 2.0e6 * 4               # + sensible 4 K
eta = 0.6                                                # heat into paystreak vs roof/pillars/slurry (ASSUMPTION)
thaw_l = thaw_J / eta / (DIESEL_LHV * BOILER)
jet_J = 6 * 2e6 / (0.7 * 0.38)                           # 6 m3 water @2 MPa (ASSUMPTION)
lift_J = 8000 * G * 22 / 0.3 / 0.38                      # airlift 22 m (ASSUMPTION)
mech_l = (jet_J + lift_J) / DIESEL_LHV
req3 = (thaw_l + mech_l) / (grade * rec)
ideal3 = thaw_J / (DIESEL_LHV * BOILER) / (grade * rec)
m3 = 2.0 / req3
print(f"thaw {thaw_J/1e6:.0f} MJ/m3 -> {thaw_l:.2f} l/m3 ; mech {mech_l:.2f} l/m3 ; need {req3:.2f} l/g (ideal thaw only {ideal3:.2f}) -> MARGIN {m3:.2f}")
save_d = now_A * 0.22 * (1 - req3 / 11)                  # energy+inbound scale with fuel
save_f = 0.5 * (0.20 + 0.15 + 0.20) * now_A              # generous: half of processing, capital, labour
cost_m = 53.81 / 0.3048                                  # $/m double-cased 8" (lower bound for 12") [S12]
oz_hole = math.pi * 9 * 2.0 * grade * rec / 31.1035      # 2 m paystreak (ASSUMPTION)
drill = 22 * cost_m / oz_hole                            # 20 m cover + 2 m (ASSUMPTION)
with3 = now_A - save_d - save_f + drill
print(f"{oz_hole:.2f} oz/hole, drilling ${drill:.0f}/oz ; CHAIN now 2550 with {with3:.0f} RATIO {now_A/with3:.2f}")

print("=" * 70)
print("IDEA 4  Flash-distilled lithium")
ore = 1.96e6; lce = 45e3                                 # ledger
req_tpd = ore / 365
m4 = 5.0 / req_tpd                                       # largest FJH plant target ~5 t/day [S13]
print(f"ore/LCE {ore/lce:.1f} t/t ; need {req_tpd:.0f} t/d vs 5 t/d -> MARGIN {m4:.4f} ; power {ore*939/8760/1e3:.0f} MW ({ore*939/8760/1e3*2/3:.0f} MW after TPV)")
now_D = 10200.0
save_cap = 0.9 * (0.70 * 91 / 131) * 0.42 * now_D        # process plant = 70% of 91 bn (ASSUMPTION), cut 10x (claim)
save_proc = 0.5 * 0.18 * now_D                           # ASSUMPTION: reagent/kiln opex halved
new_E = ore / lce * 939 * (2 / 3) * 6.45 / USD_RUB       # FJH 939 kWh/t [S2], TPV 1/3 (claim), 6.45 rub/kWh (ledger NPP)
with4 = now_D - save_cap - save_proc - 0.09 * now_D + new_E
print(f"new energy {ore/lce*939*2/3/1e3:.1f} MWh/t = ${new_E:.0f}/t ; CHAIN now 10200 with {with4:.0f} RATIO {now_D/with4:.2f}")

print("=" * 70)
print("IDEA 5  Thaw-scored slab toppling")
rho_ob = 1800.0                                          # ASSUMPTION
W = 450e3 / (rho_ob * 30)
w = 0.2                                                  # thin slot (ASSUMPTION, generous)
frac = (10 * W + 10 * 3 + 3 * W) * w / (30 * W)
ice5 = 0.30                                              # low end of 30-90 vol% for fine permafrost [S14]
req5 = frac * (ice5 * RHO_ICE * L_ICE + 2.0e6 * 4) / (DIESEL_LHV * BOILER)   # ideal 100% heat use
dozer_lph = 455 * 0.65 * 0.215 / 0.84                    # D375A-6 455 kW [S15]; LF 0.65, bsfc (ASSUMPTION)
dozer_lm3 = dozer_lph / 150                              # 150 bcm/h ripped frozen ground (ASSUMPTION)
m5 = 0.1 * dozer_lm3 / req5
F = 1e5 * 10 * W; Mo = F * 5; Mr = 450e3 * G * 1.5
print(f"W={W:.2f} m thawed {frac*100:.1f}% -> {req5:.3f} l/m3 ; dozer {dozer_lm3:.2f} l/m3 -> budget {0.1*dozer_lm3:.3f} -> MARGIN {m5:.2f} ; topple moment ratio {Mo/Mr:.1f}")
phys = (0.10 + 0.20 + 0.12 + 0.002 + 0.20 + 0.15) * now_A
strip = 0.7 * (2 / 3) * phys                             # ledger 2/3 earthmoving; 70% of it stripping (ASSUMPTION)
thaw_lpg = req5 / dozer_lm3 * 11 * 0.7
with5 = now_A - strip + 0.1 * strip + thaw_lpg * (135 / USD_RUB) * 31.1035
print(f"stripping ${strip:.0f}/oz ; thaw diesel {thaw_lpg:.1f} l/g ; CHAIN now 2550 with {with5:.0f} RATIO {now_A/with5:.2f}")

print("=" * 70)
print("IDEA 6  Flooded-pit floating mine")
mat = 70e6 * 25 * 1.8                                    # 70 Mtpa [ledger/S16], ~25 yr, SR 0.8 [S16]
vol = mat / 2.7 / 1e9
for a in (3, 5):
    print(f"  footprint {a} km2: mean depth {vol/a*1e3:.0f} m, cone max {3*vol/a*1e3:.0f} m")
print(f"  year-1 deepening on 1 km2: {70e6*1.8/2.7/1e6:.0f} m ; ore traced to 750 m [S17]")
m6 = 45 / 400                                            # Spartacus 45 m [S18]
now_B = 8500.0; with6 = now_B * (1 - 0.5 * 0.41)
print(f"MARGIN {m6:.2f} ; CHAIN now 8500 with {with6:.0f} RATIO {now_B/with6:.2f}")

print("=" * 70)
print("IDEA 7  Lake-breach thermo-erosion canal")
b, h, n, S = 15.0, 1.5, 0.03, 1e-4                       # <=400 t barges [S19]; geometry/n/S ASSUMPTION (generous)
Ach = b * h; Rh = Ach / (b + 2 * h)
Qreq = Ach * (1 / n) * Rh ** (2 / 3) * S ** 0.5
Vreq = Qreq * 86400 * 100                                # 100-day season (ASSUMPTION; ice Oct-mid May)
Vlake = 5e6 * 2.35                                       # 5 km2 (ASSUMPTION) x 2.2-2.5 m mean depth [S20]
m7 = Vlake / Vreq
heat_km = Ach * 1000 * 0.65 * RHO_ICE * L_ICE            # yedoma 65-90 vol% ice [S21]
water_km = heat_km / (4.18e6 * 12.5)
print(f"Q needed {Qreq:.1f} m3/s -> {Vreq/1e6:.0f} Mm3/season vs lake {Vlake/1e6:.1f} Mm3 -> MARGIN {m7:.2f}")
print(f"  heat check: {water_km/1e3:.0f} k m3 lake water per km (ideal) -> one lake cuts {Vlake/water_km:.0f} km")
L = 100; sav = L * (20 - 4)                              # ledger winter road 20, barge 3-5 rub/t-km
print(f"CHAIN now 23000 with {23000-sav} rub/t RATIO {23000/(23000-sav):.3f}")

print("=" * 70)
print("IDEA 8  Mast-hung coal belt")
req_tph = 25e6 / (8760 * 0.85)
m8 = 1200 / req_tph                                      # largest RopeCon built [S22]
now_C = 83 - 0.55 * 83 + 12                              # Elga railway route (ledger)
capex_km = 2.066e6 * (25 / 10) ** 0.6 * 2                # $2,066/m @10 Mtpa [S23], scale^0.6, Far North x2 (ledger 2-3x)
capex8 = capex_km * 450
conv_t = capex8 * crf(0.10, 25) / 25e6 + 0.02 * capex8 / 25e6
with8 = now_C - 12 + conv_t
print(f"need {req_tph:.0f} t/h vs 1,200 t/h -> MARGIN {m8:.2f}")
print(f"conveyor capex ${capex8/1e9:.1f}bn -> ${conv_t:.1f}/t ; CHAIN now {now_C:.1f} with {with8:.1f} RATIO {now_C/with8:.2f}")
print(f"  Thundersaid $0.1/t-km [S24] -> ${0.1*450:.0f}/t -> RATIO {now_C/(now_C-12+45):.2f} ; claim $6.5/t -> {now_C/(now_C-12+6.5):.2f}")
print(f"  Elga railway 100 bn rub / 531 km [S25] = ${100e9/USD_RUB/531/1e6:.2f}M/km")

SOURCES = """
S1 gordonengland.co.uk/xelements/au.htm ; en.wikipedia.org/wiki/Heats_of_vaporization_of_the_elements_(data_page)
S2 Deng et al., Nat Commun 2021 'Urban mining by flash Joule heating' (PMC8490403; news.rice.edu 2021; controleng.com)
S3 miningweekly.com/article/polymetal-approves-431m-pox-2-project-2019-02-11
S4 fs.moex.com/emidocs/2016/08/22/1220016_ENG-12938515.html
S5 cdn.supl.biz/media/attachments/2022/12/3/103015_Content_1.pdf (ESPO export spec)
S6 ceypetco.gov.lk/wp-content/uploads/2026/03/ANNEX-2-PROPERTIES-OF-CRUDE-C1-C8.pdf (Siberian Light)
S7 en.wikipedia.org/wiki/Kirensk (climate table)
S8 universetoday.com/159222 ; spaceinsider.tech/?p=21720 (Sierra Space LIFE UBP test)
S9 shop.midwesthose.com/products/polycrete-tpu-layflat
S10 mindat.org/loc-18223.html (Topky placer, Kolyma)
S11 emrlibrary.gov.yk.ca/emrlibrary/ebooks/characteristics_of_permafrost_and_ice_rich_ground.pdf
S12 softlive.floridadep.gov/sites/default/files/DrillingRateSchedule-LSSI_0.pdf
S13 announcements.asx.com.au/asxpdf/20260316/pdf/06xgm1127mjyzn.pdf ; stockhead.com.au (Metallium FJH)
S14 pubs.usgs.gov/bul/1083a/report.pdf (Black: 30-90 vol% ice in fine permafrost)
S15 dealsonwheels.co.nz/construction/reviews/1304/komatsu-d375a-6-dozer
S16 kazminerals.com 2018 acquisition release (SR 0.8, ~25 yr) ; KAZ BFS 2021 (70 Mtpa)
S17 igeotech.ru/wp-content/uploads/2021/03/sp513-2020-178.full_chitalin_et-al_peschanka.pdf
S18 bairdmaritime.com (Spartacus, 45 m; 35 m industry standard)
S19 bairdmaritime.com (Rechvodput Kolyma buoy tenders, barges <=400 t)
S20 epic.awi.de/35770 (Kolyma lowland lakes mean depth 2.2-2.5 m)
S21 epic.awi.de/id/eprint/35773 (Yedoma 65-90 vol% ice)
S22 newsroom.doppelmayr.com (Alcoa Jamaica 1,200 t/h); mining-report.de (Booysendal 909 t/h)
S23 bulk-online.com/de/node/69516 ($2,066/m, 10 Mtpa)
S24 thundersaidenergy.com/downloads/conveyor-costs-economics-of-moving-bulk-material/
S25 eastrussia.ru/material/guba-dlya-elgi/ (100 bn rub)
"""
print(SOURCES)
