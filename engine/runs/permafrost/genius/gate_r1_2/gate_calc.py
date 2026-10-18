# Gate r1_2 kill test: KILLER margin and CHAIN ratio for the 6 ideas.
# Every decisive input carries its source tag; "est." = screening estimate.
RUB_USD = 84.0          # ledger
AU_PRICE = 4150.0       # $/oz, ledger
G_OZ = 31.1035
CRF = 0.124             # capital recovery implied by ledger D: 42% x 10,200 / (131 bn rub / 84 / 45 kt)

def p(*a): print(*a)

# ---------------------------------------------------------------- IDEA 1
p("=== IDEA 1 Wintering Miner-Barge Boilerhouses")
draft_req = 3.75        # m, Nibulon B5000M 5,000 t barge, 101x17 m (thepage.ua / gmk.center)
depth_avail = 2.00      # m, guaranteed depth, Lena-basin Arctic reach (Mintrans 10 Sep 2026: 230 cm = guaranteed+30)
p("draft required %.2f m, guaranteed depth %.2f m, MARGIN %.2f" % (draft_req, depth_avail, depth_avail/draft_req))
p("share of Lena-basin network with any guaranteed depth: %.0f%%" % (100*3558/16000))  # Mintrans 3,558 km; >16,000 km maintained
now1 = 23000.0                                   # rub/t at boiler, ledger
cut = 0.15*now1                                  # non-logistics ledger shares (mine-side cost) kept as barge cutting cost
barge_capex = 3.0e6*1.3*RUB_USD                  # $3M per 5,000 t barge 2020 (Ukrrechflot, gmk.center) x1.3 escalation (est.)
barge_cap = barge_capex*CRF/5000                 # one round trip per year: whole capital charge on 5,000 t
tug = 12.5*400e3/5000                            # 12.5 tug-days x 400k rub/day (est.)
crew_maint = 0.03*barge_capex/5000 + 0.0         # 3%/yr of capex (est.)
with1 = cut + barge_cap + tug + crew_maint
with1_claim = cut + 1500*4.0                     # idea's own 3-5 rub/t-km x 1,500 km
p("cut %.0f + barge capital %.0f + tug %.0f + crew/maint %.0f = %.0f rub/t ; RATIO %.2f (idea's own freight claim: %.0f rub/t, ratio %.2f)"
  % (cut, barge_cap, tug, crew_maint, with1, now1/with1, with1_claim, now1/with1_claim))

# ---------------------------------------------------------------- IDEA 2
p("\n=== IDEA 2 River-Stripped Terrace Gold Barge")
retreat = 1.0      # m/yr, gravel-floored banks, Adycha (Murzin 2020, e.nlrs.ru/open/137191)
pay = 1.5          # m basal pay (est.)
grade = 0.30       # g/m3, top of big-river alluvium range 0.01-0.3 (resar.elpub.ru 2014, B. Kuonamka)
reach_km = 50      # km of auriferous cut-bank worked per barge-season (est., generous)
flux_km = retreat*pay*grade*1000/1000            # kg per km per yr
avail = flux_km*reach_km
crew = 12*60e3                                   # 12 workers x $60k (ledger)
barge_cost = 2.5e6*CRF + crew + 200e3*1.6 + 0.10*2.5e6 + 0.2e6   # capital, labour, 200 m3 diesel @$1.6/l, repairs, misc
other = 0.22*2550                                 # MET+other per oz, stays
target_nontax = 2550/2 - other                    # 'removes over half of delivered cost'
req = barge_cost/(target_nontax/G_OZ)/1000        # kg/yr
p("barge cost $%.2fM/yr; required %.1f kg/yr = %.2f kg/km/yr over %d km; available %.2f kg/km/yr; MARGIN %.2f"
  % (barge_cost/1e6, req, req/reach_km, reach_km, flux_km, flux_km/(req/reach_km)))
with2 = barge_cost/(avail*1000)*G_OZ + other
p("cost with idea $%.0f/oz vs $2550 ; RATIO %.2f" % (with2, 2550/with2))

# ---------------------------------------------------------------- IDEA 3
p("\n=== IDEA 3 Flooded Kimberlite Pit Brine")
inflow = 300.0     # m3/h, Udachny brine inflow 270-300 m3/h (ynalrosa.ru hydrodynamics paper)
li_lo, li_hi = 67.4, 165.9   # mg/L, Udachnaya brines (search: Udachnaya brine studies)
need_fill = 0.1e9/(3*8760)   # m3/h to place 0.1 km3 within 3 years
p("fill rate needed %.0f m3/h vs available %.0f ; MARGIN %.3f ; years to 0.1 km3: %.0f"
  % (need_fill, inflow, inflow/need_fill, 0.1e9/(inflow*8760)))
li_flux = [inflow*8760*c/1e6 for c in (li_lo, li_hi)]          # t Li/yr
lce = [x*5.323*0.9/1000 for x in li_flux]                      # kt LCE/yr at 90% recovery
p("Li supply %.0f-%.0f t/yr -> %.2f-%.2f kt LCE/yr vs 45 kt/yr archetype" % (li_flux[0], li_flux[1], lce[0], lce[1]))
# DLE cost basis: E3 Lithium Clearwater PFS (Jun 2024): C$2.47bn, 32,250 t/yr LHM, opex C$6,200/t LHM
cad = 0.73; lce_t = 32250*0.8806
capex_t = 2.47e9*cad/lce_t; opex_t = 6200*cad/0.8806
big = capex_t*0.75*CRF + opex_t                                   # pit replaces wellfield: -25% capex (est.)
scale = (lce_t/1000/lce[1])**0.4                                  # 0.6 scale exponent to inflow-limited plant
small = capex_t*0.75*scale*CRF + opex_t*1.3
p("DLE capex $%.0f/annual t, opex $%.0f/t; at E3 scale $%.0f/t (ratio %.2f); at inflow-limited %.1f kt/yr $%.0f/t ; RATIO %.2f"
  % (capex_t, opex_t, big, 10200/big, lce[1], small, 10200/small))

# ---------------------------------------------------------------- IDEA 4
p("\n=== IDEA 4 Robot-Milled Summer Peat")
nordic = (300*1000)**0.5          # m3/ha/yr geometric mean of 300-1,000 (Malkki & Frilander 1997 via Research Square)
rho = 0.33                        # t/m3 loose milled peat at 50% (est.; ~1 MWh/m3 Finnish energy peat, AIPH/Bioenergia)
y50 = nordic*rho; y425 = y50*0.50/0.575
pen = (0.90/0.10 - 0.425/0.575)/(0.80/0.20 - 0.425/0.575)   # water to evaporate: undrained 90% vs drained 80% (est.)
yperm = y425/pen
p("Nordic %.0f t/ha at 42.5%%; undrained-permafrost penalty x%.2f -> %.0f t/ha vs required 50 ; MARGIN %.2f (range %.2f-%.2f)"
  % (y425, pen, yperm, yperm/50, 300*rho*0.8696/pen/50, 1000*rho*0.8696/pen/50))
coal_cost = 3000*23000                         # rub/yr, ledger
peat_t = 6500                                  # t/yr at 42.5% (idea: 130 ha x 50 t)
mach = 110e6; field = 150*0.48e6; boiler = 40e6
annual = (mach+field+boiler)*CRF + 3*1.8e6 + 1.5*peat_t*123 + 0.08*mach + 150*peat_t
annual *= 1.10
p("peat chain %.1f M rub/yr vs coal %.1f M rub/yr ; RATIO %.2f" % (annual/1e6, coal_cost/1e6, coal_cost/annual))
fin = 17.5*1.15*RUB_USD                        # Finnish delivered milled peat EUR 16.1-18.8/MWh (Statistics Finland)
mwh = peat_t*10.5/3.6
for k in (1.0, 1.5, 2.0):
    p("  cross-check Finnish price x%.1f: ratio %.2f" % (k, coal_cost/(fin*k*mwh + boiler*CRF)))

# ---------------------------------------------------------------- IDEA 5
p("\n=== IDEA 5 Robot Pillar Robbing")
H = 30; gamma = 0.020; extraction = 0.80        # m cover, MN/m3, chamber-and-pillar (est.)
sig_p = gamma*H/(1-extraction)
sig_lt = 1.25                                   # MPa long-term (decades) strength frozen sandy gravel -3..-5C (est.)
p("pillar stress %.1f MPa vs long-term strength %.2f MPa ; MARGIN %.2f" % (sig_p, sig_lt, sig_lt/sig_p))
robot_capex = 5e6
per_m3 = (robot_capex*CRF + 6*60e3)/20000 + 50*0.49 + 0.10*robot_capex/20000 + 8   # 20,000 m3/season (2x33.4 m3/shift x 300, Kularzoloto)
for g in (3.0, 5.5, 10.0):
    c = per_m3/(g*0.9)*G_OZ + other
    p("  %.1f g/m3: $%.0f/m3 -> $%.0f/oz ; ratio %.2f" % (g, per_m3, c, 2550/c))

# ---------------------------------------------------------------- IDEA 6
p("\n=== IDEA 6 Crewless Micro-Placer Nomads")
mtbf = 100.0       # h, Komatsu PC4000-6 MTBF target (observed 80 h), repository.sgu.ac.id
season = 2000.0    # h unattended per placer-season (est.: ~100 days x 20 h)
p("MTBF %.0f h vs unattended season %.0f h ; MARGIN %.3f" % (mtbf, season, mtbf/season))
fuel = [11*kg*1000/1000 for kg in (10, 100)]   # m3 diesel at ledger 11 l/g
p("diesel per placer %.0f-%.0f m3 (ledger 11 l/g)" % tuple(fuel))
kg = 50
prem = (1.5e6*CRF + 4*60e3 + 100e3)/(kg*1000)*G_OZ
with6 = 2550*(1-0.20-0.04) + prem
p("with idea $%.0f/oz (premium $%.0f/oz) ; RATIO %.2f ; ideal ceiling %.2f" % (with6, prem, 2550/with6, 1/0.76))
