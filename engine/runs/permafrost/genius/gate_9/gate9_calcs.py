"""Gate 9 kill test: KILLER margin and CHAIN ratio for 8 ideas.
Every decisive input carries its source (URL from web search) or is marked ASSUMPTION / LEDGER.
"""
import math

RUB = 84.0  # RUB/USD, LEDGER cross-cutting
out = {}

def p(*a):
    print(*a)

# ============================================================== IDEA 1
p("\n=== IDEA 1 Snow-bedded seasonal crude hose (archetype E) ===")
annual_t = 0.2e6                       # LEDGER E: 0.2 Mt/yr field
season_d = 151                          # idea: whole volume in 5 winter months (Nov-Mar)
API = 34.0                              # ESPO blend API 34 (oilmonster.com/oil-grade/russia-far-east-siberia/espo-blend/19)
SG = 141.5 / (131.5 + API)
rho = SG * 999.0
bbl_t = 1 / (SG * 0.158987)
q_req_bpd = annual_t * bbl_t / season_d
q_req = q_req_bpd * 0.158987 / 86400
# viscosity 5.2 cSt (ESPO, oilmonster; taken at 20 C) extrapolated with ASTM D341 Walther slope 3.8 (ASSUMPTION, light crude)
def walther(nu_ref, t_ref, t, m=3.8):
    A = math.log(math.log(nu_ref + 0.7)) + m * math.log(t_ref + 273.15)
    return math.exp(math.exp(A - m * math.log(t + 273.15))) - 0.7
T_bed = -30.0   # snow-bed temp: Yakutsk Jan mean ~ -37 C air (ru.ruwiki.ru/wiki/Якутск); bed under snow somewhat warmer
nu = walther(5.2, 20, T_bed)
pour_point = -40.0   # light E-Siberian crude (Yurubcheno-Tokhomskoye), rogtecmagazine.com
mu = rho * nu * 1e-6
D, L = 0.305, 300e3                    # 12-in lay-flat hose, 300 km (idea)
P_rate = 200 * 6894.76                 # 12" TPU layflat max WP 200 psi, -40F..180F (midwesthose.com TPU-Layflat-Hose-All-Sizes.pdf)
dP = P_rate - 0.1e6                    # keep >=1 bar so lay-flat stays open (ASSUMPTION)
q_max = dP * math.pi * D**4 / (128 * mu * L)   # laminar Hagen-Poiseuille, single pump, no intermediate boosters
v = q_req / (math.pi * D**2 / 4)
Re = v * D / (nu * 1e-6)
# cooling length in compacted snow (Sturm 1997 quadratic, rho=0.45 g/cm3 -> k~0.34 W/mK), hose centre 0.4 m deep
ks = 0.138 - 1.01 * 0.45 + 3.233 * 0.45**2
Ul = 2 * math.pi * ks / math.acosh(2 * 0.4 / D)
Lcool = q_req * rho * 1900 / Ul / 1000
m1 = q_max / q_req
p(f"bbl/t={bbl_t:.2f}  required {q_req_bpd:,.0f} bbl/d; nu(-30C)={nu:.1f} cSt (pour point {pour_point} C)")
p(f"Re={Re:.0f} (laminar) ; Qmax at 200 psi single segment={q_max*86400/0.158987:,.0f} bbl/d ; cooling e-fold length {Lcool:.0f} km")
p(f"MARGIN1 = {m1:.2f}")
now1 = 82.0                            # LEDGER E delivered $/bbl FOB Kozmino
truck = 10.0                           # LEDGER E trucking $10/bbl
hose = 2.5                             # idea's own claim $2-3/bbl (optimistic)
cap = 0.13 * now1                      # LEDGER E capital share 13%
penalty = cap * ((12 / 5) ** 0.6 - 1)  # 2.4x peak capacity, six-tenths capacity-cost rule (ASSUMPTION, standard)
with1 = now1 - truck + hose + penalty
r1 = now1 / with1
p(f"capacity penalty ${penalty:.2f}/bbl ; with idea ${with1:.1f}/bbl ; RATIO1={r1:.2f} ; ceiling (free hose, no penalty) {now1/(now1-truck):.2f}")
out[1] = (m1, r1)

# ============================================================== IDEA 2
p("\n=== IDEA 2 Creeping-floor solar copper pond (archetype B) ===")
lat = 56.9   # Udokan/Chara; Udokan ore chalcocite-bornite, 1.56% Cu (repository.geologyscience.ru/handle/123456789/24252)
nday = [17, 47, 75, 105, 135, 162, 198, 228, 258, 288, 318, 344]
mdays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
def H0(lat, n):  # Duffie & Beckman daily extraterrestrial irradiation, kWh/m2/day
    phi = math.radians(lat)
    dec = math.radians(23.45 * math.sin(math.radians(360 * (284 + n) / 365)))
    ws = math.acos(max(-1, min(1, -math.tan(phi) * math.tan(dec))))
    E = 1 + 0.033 * math.cos(math.radians(360 * n / 365))
    return 24 * 3600 * 1367 / math.pi * E * (math.cos(phi) * math.cos(dec) * math.sin(ws) + ws * math.sin(phi) * math.sin(dec)) / 3.6e6
H = [H0(lat, n) for n in nday]
winter = [10, 11, 0, 1, 2, 3]          # Nov..Apr, ice-covered
summer = [4, 5, 6, 7, 8, 9]
x = 0.2 + 1.25                         # UCZ 0.15-0.30 m + NCZ 1.0-1.5 m typical (vinca.rs TSCI180518060S)
tau = 0.36 - 0.08 * math.log(x)        # Bryant-Colbeck fraction reaching depth x
k_br = 0.6                             # brine conductivity W/mK (ASSUMPTION, NaCl brine ~0.57-0.6)
T_lcz = 70.0                           # idea: 60-80 C bottom brine
Kt_w, Kt_s = 0.60, 0.50                # clearness index winter (generous, anticyclone) / summer (ASSUMPTION)
GHI = [H[i] * (Kt_w if i in winter else Kt_s) * mdays[i] for i in range(12)]
solar_w = sum(GHI[i] for i in winter) * 0.90 * 0.70 * tau   # 10% reflection, clear snow-free ice 0.70 (generous)
solar_s = sum(GHI[i] for i in summer) * 0.94 * tau
days_w = sum(mdays[i] for i in winter); days_s = 365 - days_w
loss_w = k_br * (T_lcz - 0) / 1.25 * days_w * 24 / 1000          # top under ice at 0 C
loss_s = k_br * (T_lcz - 10) / 1.25 * days_s * 24 / 1000         # summer UCZ ~ +10 C (ASSUMPTION)
heatcap = 1.5 * 1190 * 3.3e3 + 0.5 * 1800 * 850                   # J/m2K: LCZ 1.5 m brine + 0.5 m ore bed
stored = heatcap * 20 / 3.6e6                                       # 80 -> 60 C, kWh/m2
m2 = (stored + solar_w) / loss_w
dT = (loss_w - solar_w) * 3.6e6 / heatcap
p(f"annual GHI={sum(GHI):.0f} kWh/m2 ; tau(1.45 m)={tau:.3f}")
p(f"WINTER: loss {loss_w:.0f} kWh/m2 vs stored {stored:.0f} + solar {solar_w:.0f} -> MARGIN2={m2:.2f}; LCZ would cool by {dT:.0f} K (no ORC/ore draw)")
net = solar_s + solar_w - loss_s - loss_w
grade, rec = 0.0156, 0.85              # Udokan 1.56% Cu; recovery ASSUMPTION
cu_t = grade * rec * 1000              # kg Cu per t ore
ore_heat = (0.85 * 77 + 0.03 * (2.1 * 7 + 334 + 4.19 * 70)) / 3600 * 1000 / cu_t   # kWh_th/kg Cu, -7C ore, 3% ice
ew = 1.1 + 0.1                         # cuprous-chloride EW 1.1 kWh/kg (USBM, onemine.org RI 8076) + aux
eta = 0.5 * (1 - 268 / 343)            # ORC at half Carnot, sink -5 C annual mean
demand = ore_heat + ew / eta
area = 1000 * demand / net             # m2 per (t Cu/yr)
p(f"annual net useful heat {net:.0f} kWh/m2/yr ; demand {demand:.1f} kWh_th/kg Cu ; pond {area:.0f} m2 per t/yr")
draw_w = net * days_w / 365            # winter share of the useful heat the pond is sized to deliver (year-round claim)
m2 = (stored + solar_w) / (loss_w + draw_w)
# LCZ temperature at end of February (Nov-Feb), starting 80 C, no draw
nf = [10, 11, 0, 1]
sol_nf = sum(GHI[i] for i in nf) * 0.90 * 0.70 * tau
loss_nf = k_br * 70 / 1.25 * sum(mdays[i] for i in nf) * 24 / 1000
T_feb = 80 - (loss_nf - sol_nf) * 3.6e6 / heatcap
p(f"WINTER incl. draw: required {loss_w + draw_w:.0f} vs available {stored + solar_w:.0f} kWh/m2 -> MARGIN2={m2:.2f}; LCZ ~{T_feb:.0f} C by end Feb even with zero draw")
now2 = 8500.0                          # LEDGER B $/t Cu gross
chg = 0.41 * now2 / 28000              # LEDGER: capital 41%, $28k per annual t -> capital charge rate
r2 = {}
for cpm in (35, 70, 105):              # pond $35-43/m2 (osti.gov 109854; arid.my Jordan), $105/m2 (2011 article), $145 Arizona
    capex = 0.5 * 28000 + area * cpm + 2500    # keep 50% (mine etc., ASSUMPTION) + pond + EW/ORC (ASSUMPTION)
    w = capex * chg + now2 * (0.11 * 0.4 + 0.15 * 0.6 + 0.05 / 4.84 + 0.03 * 0.5 + 0.11 + 0.14)
    r2[cpm] = now2 / w
    p(f"  pond ${cpm}/m2: capex/t/yr ${capex:,.0f} ; with ${w:,.0f}/t ; RATIO={now2/w:.2f}")
out[2] = (m2, r2[70])

# ============================================================== IDEA 3
p("\n=== IDEA 3 Transpolar Drift freight (archetype C export) ===")
surv = 0.20     # ~1/5 of young ice from shallow Russian seas reaches TPD, 80% melts (AWI/Krumpen 2019; PMC6445075)
m3 = surv / 1.0
now3 = 83.0                            # LEDGER C export $/t FOB
nonout = (1 - 0.55) * now3             # all but outbound logistics
Vext = 6.058 * 2.438 * 2.591; tare = 2.2; Vint = 33.2
pay = min(Vint * 0.85, Vext * 1.025 * 0.85 - tare)  # coal bulk 0.85 t/m3 vs 15% reserve buoyancy
box = 2700.0                           # used 20ft container avg 2026 (latestcost.com/shipping-container-cost/)
box_t = box / (pay * surv)
carry = (nonout + box / pay) * (1.10 ** 2.5 - 1)   # 2.5 yr at 10%/yr (ASSUMPTION)
with3 = nonout + box_t + carry
r3 = now3 / with3
p(f"payload {pay:.1f} t ; container per delivered t ${box_t:.0f} ; with ${with3:.0f}/t ; MARGIN3={m3:.2f} RATIO3={r3:.2f}")
out[3] = (m3, r3)

# ============================================================== IDEA 4
p("\n=== IDEA 4 Under-ice sphere strings (archetype B) ===")
Vs = math.pi / 6; A = math.pi / 4
B = 0.005 * 1000 * 9.81 * Vs            # 0.5% positive buoyancy (idea)
slope = 29.0                            # mean keel slope 29 deg (fennia.journal.fi/article/view/8919)
F_req = B * math.tan(math.radians(slope))
v4 = 0.15                               # Lena main channel under ice 12-18 cm/s (April) (hess / 2019 delta study via search)
Cd = 0.47
F_av = 0.5 * 1000 * Cd * A * v4**2
m4 = F_av / F_req
v_need = math.sqrt(F_req / (0.5 * 1000 * Cd * A))
# freeze-in once stalled: basal growth under 1.5 m ice, -30 C top; adfreeze >=0.1 MPa (trid.trb.org/View/296123: 0.1-1.6 MPa)
grow = 2.2 * 30 / 1.5 / (917 * 334e3) * 86400 * 1000   # mm/day
pull = 100 * 0.5 * 1000 * Cd * A * v4**2               # whole held string
t_freeze = pull / (2 * math.pi * 0.5 * 0.1e6) * 1000 / grow * 24
p(f"B={B:.1f} N ; required drag {F_req:.1f} N (needs v={v_need:.2f} m/s) ; available {F_av:.2f} N ; MARGIN4={m4:.2f}")
p(f"stalled sphere bonds beyond whole-string pull ({pull:.0f} N) in ~{t_freeze:.1f} h")
cu = 70e6 * 0.0047 * 0.88              # Baimskaya 70 Mtpa, 0.47% Cu (kazminerals BFS); recovery 0.88 ASSUMPTION
conc_per_cu = 1.4e6 / cu               # LEDGER 1.4 Mt/yr concentrate
payload = 1000 * Vs * 0.995 - 30       # kg, 30 kg shell ASSUMPTION
n_sph = 1.4e6 * 1000 / payload         # one round trip per year (empties back by summer barge)
price = 502.27 * (1 / 0.762) ** 2      # 30-in foam-filled PE buoy $502 (fisheriessupply.com), scaled by area
fleet = n_sph * price
cap4 = fleet * chg / cu
barge = n_sph * 1.0 / 1.5 * 8000 / RUB / cu   # 1 m3 stowed per sphere, 1.5 m3 per t-eq (ASSUMPTION), LORP 8,000 rub/t (LEDGER)
with4 = now2 - now2 * (0.03 + 0.05) + cap4 + barge
r4 = now2 / with4
p(f"Cu {cu/1e3:.0f} kt/yr ; spheres {n_sph/1e6:.2f} M at ${price:.0f} ; sphere capital ${cap4:.0f}/t Cu ; barge ${barge:.0f}/t Cu")
p(f"with ${with4:,.0f}/t ; RATIO4={r4:.2f} ; ceiling (free logistics) {now2/(now2*(1-0.08)):.3f}")
out[4] = (m4, r4)

# ============================================================== IDEA 5
p("\n=== IDEA 5 Relocatable frozen-tundra ore railway (archetype D) ===")
P_loco = 6 * 23.0 * 1000               # 6-axle loco section at ~23 t/axle (RZD standard axle load 23-23.5 t)
A_gold = 3.5                           # kg/cm2, Gold's formula low-quality ice (en.wikipedia.org/wiki/Ice_road; tac-atc.ca barrette.pdf)
h_req = math.sqrt(P_loco / A_gold)     # cm
h_nat = 175.0                          # natural max 150-200 cm on arctic tundra rivers (e3s-conferences 202016305003); delta >1.5 m
m5 = (h_nat / h_req) ** 2
p(f"h_req={h_req:.0f} cm ; natural late-winter {h_nat:.0f} cm ; MARGIN5 (load) = {m5:.2f}")
now5 = 10200.0                         # LEDGER D $/t LCE
cap5 = 0.42 * now5
road = cap5 * 40 / 131; plant = cap5 * 91 / 131 * 0.7; mine = cap5 * 91 / 131 * 0.3   # plant 70% of 91 bn (ASSUMPTION)
L_line = 150                            # km (ASSUMPTION)
line_rub = L_line * 13e6               # worn rails ~130 t/km near scrap + used sleepers + laying ~13 M rub/km (ASSUMPTION)
road_new = road * line_rub / 40e9
plant_new = plant / 2.5                # Far-North build premium 2-3x (LEDGER) removed
energy = 0.09 * now5 * (0.7 * 6.45 / 41 + 0.3)   # processing power to grid-like 6.45 vs diesel 41 rub/kWh (LEDGER)
labour = 0.14 * now5 * 0.8
inbound = 0.04 * now5 * 0.4
fixed = now5 * (0.015 + 0.18 + 0.12)
ore_per_lce = 1.96e6 / 45e3            # LEDGER D
rail = ore_per_lce * (L_line * 3.0 + 150) / RUB   # 3 rub/t-km seasonal line + 150 rub/t stockpile rehandle (ASSUMPTION)
maint = 0.10 * line_rub / RUB / 45e3
with5 = road_new + plant_new + mine + energy + labour + inbound + fixed + rail + maint
r5 = now5 / with5
p(f"with ${with5:,.0f}/t LCE (raw-ore haul ${rail:.0f}) ; RATIO5={r5:.2f}")
for prem in (1.5, 3.0):
    w = with5 - plant_new + plant / prem
    p(f"  premium {prem}: RATIO={now5/w:.2f}")
out[5] = (m5, r5)

# ============================================================== IDEA 6
p("\n=== IDEA 6 Self-charging frost separator cascade (archetype B) ===")
d_need = 30.0   # regrind P80 ~30 um for shipping-grade Cu conc (911metallurgist.com/blog/effect-of-regrinding)
d_min = 75.0    # electrostatic separators typically limited to >75 um; free-fall units 1-8 mm (onemine STET paper; patent 11305295)
m6 = d_need / d_min
saved = now2 * (0.15 * 0.35 + 0.11 * 0.10)       # flotation share of processing 35%, of energy 10% (ASSUMPTION)
dry = now2 * 0.11 * 0.70 * 0.30                  # dry grinding +30% on grinding (70% of energy) (ASSUMPTION)
with6 = now2 - saved + dry                        # equal recovery assumed (generous)
r6 = now2 / with6
p(f"MARGIN6={m6:.2f} ; with ${with6:,.0f}/t ; RATIO6={r6:.2f} ; ceiling (all processing+energy free) {now2/(now2*(1-0.26)):.2f}")
out[6] = (m6, r6)

# ============================================================== IDEAS 7, 8 (archetype A)
p("\n=== IDEAS 7/8 robot drift mining (archetype A) ===")
now_g = 6900 / RUB                      # LEDGER A $/g
other = 0.22 * now_g
earth = 0.78 * now_g * 2 / 3            # LEDGER: earthmoving ~2/3 physically
Vt = 11.0 / 1.2                         # 11 l/g diesel (LEDGER) / 1.2 l per m3 moved (ASSUMPTION) -> m3 per g
prod = 33.4                             # m3 per machine-shift, mechanized permafrost placer mine (rudmet.net Article_MJ_09_16, Kularzoloto)
shifts = 2 * 210                        # winter-only ventilation season (e.nlrs.ru/open/36931: summer operation thaws roof)
robot = 1.0e6                           # $ per autonomous battery robot (ASSUMPTION)
per_shift = robot * (chg + 0.10) / shifts + 60000 * 0.5 / shifts   # capital charge + 10% maint + 0.5 worker-yr supervision
energy_m3 = 10 * 0.49                   # 10 kWh/m3 (ASSUMPTION) at $0.49/kWh mine diesel power (LEDGER)
c_m3 = per_shift / prod + energy_m3
p(f"open-cut earthmoving ${earth:.1f}/g = ${earth/Vt:.2f}/m3 over {Vt:.1f} m3/g ; robot ${c_m3:.1f}/m3")
# idea 7: excavator, 5-10x less ground (use 7.5), cobble-pillar stacking +30% machine time
m7 = 0.25 / 1.5   # excavators dig frozen ground w/o pre-loosening only to 0.25 m (dnaop.com/html/45827_6.html) vs 1-2 m frozen face
u7 = Vt / 7.5 * (per_shift * 1.3 / prod + energy_m3)
with7 = now_g - earth + u7
r7 = now_g / with7
p(f"IDEA7 MARGIN7={m7:.2f} ; underground ${u7:.1f}/g ; with ${with7:.1f}/g ; RATIO7={r7:.2f}")
# idea 8: cutting moles, tenfold less ground
Vu8 = Vt / 10
u8 = Vu8 * c_m3
with8 = now_g - earth + u8
r8 = now_g / with8
P_req = per_shift / (earth / Vu8 - energy_m3)    # break-even productivity vs open-cut earthmoving
m8 = prod / P_req
p(f"IDEA8 required {P_req:.1f} m3/shift vs available {prod} -> MARGIN8={m8:.2f} ; with ${with8:.1f}/g ; RATIO8={r8:.2f}")
for rb in (2.0e6,):
    ps = rb * (chg + 0.10) / shifts + 60000 * 0.5 / shifts
    w = now_g - earth + Vu8 * (ps / prod + energy_m3)
    p(f"  robot ${rb/1e6:.0f}M: RATIO8={now_g/w:.2f} ; margin {prod/(ps/(earth/Vu8-energy_m3)):.2f}")
out[7] = (m7, r7); out[8] = (m8, r8)

p("\n=== SUMMARY ===")
for i in range(1, 9):
    m, r = out[i]
    verdict = "ALIVE" if (m >= 1 and r >= 1.5) else ("DEAD" if (m < 0.3 or r < 1.1) else "WOUNDED")
    p(f"IDEA {i}: MARGIN {m:.2f} RATIO {r:.2f} -> {verdict}")
