# Repair calculations for the 4 permafrost ideas. Every constant is tagged:
#   [S#] = number found in this session (see NOTES.md source list)
#   [REF] = standard textbook/handbook value (not fetched this session)
#   [ASM] = my assumption; ranges are swept so the verdict does not hinge on it
import math

def hdr(t): print("\n" + "=" * 8 + " " + t + " " + "=" * 8)

RHO_I, LF = 917.0, 334e3               # ice density kg/m3, latent heat J/kg [REF]
DIESEL_MJ_L = 36.0                     # MJ per litre [REF]
DIESEL_RUB_L = 90.0                    # Far-North diesel price, rub/l [ASM 80-100]

# ============================ IDEA 1 ============================
hdr("IDEA 1  talik dredging under lakes")
# 1a lake ice: Stefan with snow coefficient a=0.017-0.024 m/sqrt(degC d) [REF Michel 1971/Lepparanta]
for fdd in (5000, 6500):               # Kolyma/Yana valleys freezing degree-days [ASM]
    print(f"FDD {fdd}: max lake ice {0.017*math.sqrt(fdd):.2f}-{0.024*math.sqrt(fdd):.2f} m  -> lake must be >~2 m deep")
# 1b steady talik depth under centre of circular lake (Lachenbruch 1957) [REF]
def talik_depth(R, Ts=-6.0, Tb=3.0, G=0.03):
    f = lambda z: Ts + G*z + (Tb - Ts)*(1 - z/math.sqrt(z*z + R*R))
    z = 0.0
    while z < -Ts/G:
        if f(z) < 0: return z
        z += 0.1
    return float('inf')   # open (through) talik
for R in (25, 50, 100, 200):
    print(f"lake radius {R:4d} m: steady talik {talik_depth(R):6.1f} m (Ts=-6, Tb=+3)   colder Ts=-9: {talik_depth(R,Ts=-9):6.1f} m")
# time for thaw front to reach bedrock at D (Stefan, no losses = lower bound)
n_ice, k_u, dT = 0.25, 2.0, 3.0
Lv = n_ice*RHO_I*LF
for D in (10, 15, 25):
    t = Lv*D*D/(2*k_u*dT)/3.156e7
    print(f"thaw to {D} m below lake floor needs >= {t:5.0f} yr (lakes are 1e2-1e4 yr old)")
# 1c reach budget: water + silt + pay + 0.5 m bedrock vs dredge digging depth
reach = {"250 L": 18.0, "380 L": 30.0, "600 L": 50.0}   # [ASM, class values; idea quoted 45 m]
for Hw, Ho, Hp in ((2.5, 4, 2), (4, 8, 2), (6, 15, 3), (8, 30, 3)):
    need = Hw + Ho + Hp + 0.5
    ok = [k for k, v in reach.items() if v >= need]
    print(f"water {Hw} + silt {Ho} + pay {Hp}: dig depth {need:4.1f} m -> fits {ok}")
# 1d winter thermal budget. bulk formulae, U=3 m/s, CH=CE=1.5e-3, open water 0 C [REF Maykut 1978 leads 400-700 W/m2]
def open_water_loss(Ta, U=3.0):
    rho_a, cp = 1.40, 1005.0
    sens = rho_a*cp*1.5e-3*U*(0 - Ta)
    qs0 = 3.8e-3; qa = 0.62*6.112*math.exp(22.46*Ta/(272.6+Ta))/1013.0  # sat over ice
    lat = rho_a*2.5e6*1.5e-3*U*(qs0 - qa)
    lw = 0.97*5.67e-8*273.15**4 - 0.70*5.67e-8*(273.15+Ta)**4
    return sens + lat + lw
for Ta in (-20, -35, -45):
    q = open_water_loss(Ta)
    print(f"air {Ta} C: open-water loss {q:5.0f} W/m2 -> new ice {q*86400/(RHO_I*LF)*100:4.1f} cm/day on open water")
# dredge (250 L class) numbers [ASM]: 1.0 Mm3 per 165-day season [S: season 160-180 d, Nafikov SFU]
V_day = 1.0e6/165          # m3/day summer
P_el = 1.1e6               # W average electrical draw
waste = 0.9*P_el           # recoverable genset heat W
winter_f = 0.7             # winter productivity factor
cut_thick = 8.5            # m dug below lake floor (silt+pay+bedrock)
area_day = V_day*winter_f/cut_thick
pond = 1500.0              # m2 kept broken around ladder & stern spill (rest left frozen)
for Ta, h_ice in ((-20, 0.6), (-35, 1.2), (-45, 1.7)):
    q = open_water_loss(Ta)
    # a broken pond regrows ~ a few cm/d; melting that brash in the plant:
    brash = pond*q*86400/(RHO_I*LF)                        # m3/day, uncapped regrowth
    melt_W = brash*RHO_I*LF/86400
    advance_ice = area_day*h_ice                           # m3/day of sheet ice ahead of the bow
    melt_adv_W = advance_ice*RHO_I*LF/86400
    kerf = area_day*1.0                                    # m of saw cut/day for 2x2 m blocks
    print(f"air {Ta}: mined area {area_day:4.0f} m2/d, sheet ice ahead {advance_ice:5.0f} m3/d "
          f"(melt would need {melt_adv_W/1e6:4.1f} MW) -> saw {kerf:4.0f} m/d & sink blocks; "
          f"pond brash melt {melt_W/1e6:4.2f} MW vs waste heat {waste/1e6:4.2f} MW")
# 1e cost per gram. rub per bank m3 dug. [ASM ranges, cross-check S7: Yukon floater $0.90/loose yd3]
usd = 85.0
yukon = 0.90/0.7646*1.25*usd
print(f"Yukon floating plant $0.90/loose yd3 = {yukon:4.0f} rub per bank m3 (cross-check)")
grade, rec = 0.35, 0.85                      # g/m3 of dug rock mass, recovery [ASM, dredge fields]
def per_g(c): return c/(grade*rec)
cases = {}
for tag, dredge, thaw, strip, oh, cap, days in (
    ("B3 permafrost dredge field (thaw+strip)", 120, 70, 30, 60, 60, 165),
    ("B2 summer dredge in lake talik",           120,  0,  5, 60, 60, 165),
    ("IDEA winter+summer in lake talik",         140,  0,  5, 60, 60, 300),
    ("B1 drain lake + open-cut talik (excav+truck+sluice)", 260, 0, 40, 60, 25, 120)):
    # capital & overhead are fixed per year -> spread over operating days
    c = dredge + thaw + strip + (oh + cap)*165/days
    cases[tag] = c
    print(f"{tag:55s}: {c:5.0f} rub/m3  -> {per_g(c):6.0f} rub/g recovered")
base = min(cases["B3 permafrost dredge field (thaw+strip)"], cases["B1 drain lake + open-cut talik (excav+truck+sluice)"])
print(f"ratio best baseline/IDEA = {base/cases['IDEA winter+summer in lake talik']:.2f};  "
      f"vs B2 (summer-only talik) = {cases['B2 summer dredge in lake talik']/cases['IDEA winter+summer in lake talik']:.2f}")
for thaw in (40, 70, 120):
    b3 = 120 + thaw + 30 + 120
    print(f"  sensitivity thaw cost {thaw}: B3 {b3} vs IDEA {cases['IDEA winter+summer in lake talik']:.0f} -> {b3/cases['IDEA winter+summer in lake talik']:.2f}x")

# ============================ IDEA 2 ============================
hdr("IDEA 2  jacked frozen-block stripping")
g = 9.81
def idea2(L, H=10.0, Hp=1.5, gam=1.9, phi=33, uplift=0.0, w=0.20, ice_ob=0.40, eta_k=0.4):
    A = L*L
    W = gam*A*H                                        # t
    sig_n = (gam - uplift*1.0)*g*H                     # kPa effective normal stress under block
    F = math.tan(math.radians(phi))*sig_n*A/1000.0     # MN base sliding on thawed pay
    face = F/(L*H)                                     # MPa on jacked face
    react = 0.20*A                                     # MN, next block base adfreeze 0.2 MPa long-term (-2..-3 C) [REF SP 25.13330]
    e_k = ice_ob*RHO_I*LF/1e6 + 2.0*3                  # MJ/m3 kerf
    kerf_l = 2*w*e_k/(L*eta_k*0.85*DIESEL_MJ_L)        # l diesel per m3 overburden
    jack_l = F*1e6*L/0.35/1e6/DIESEL_MJ_L/(A*H)        # l per m3
    return W, F, face, react, kerf_l, jack_l
for L, upl in ((20, 0.0), (20, 1.0), (30, 1.0), (40, 1.0)):
    W, F, face, react, kl, jl = idea2(L, uplift=upl)
    print(f"block {L}x{L}x10 m, W={W:6.0f} t, kerfs flooded={bool(upl)}: push {F:5.1f} MN "
          f"({math.ceil(F/5)} x 5-MN jacks), face {face:4.2f} MPa, reaction FS {react/F:4.1f}, "
          f"diesel kerf {kl:5.3f} + jack {jl:6.4f} l/m3")
# paystreak thaw under intact lid: energy & water [S8: ~10 m3 water per m3 thawed]
e_pay = 0.25*RHO_I*LF/1e6 + 2.0*3                     # MJ/m3
for L in (20, 40):
    Vp = L*L*1.5
    water_ideal = Vp*e_pay/(7*4.18)                    # m3 water cooling 8->1 C
    print(f"pay under {L} m block: {Vp:5.0f} m3, heat {Vp*e_pay/1e3:5.0f} GJ, ideal water {water_ideal:6.0f} m3, "
          f"practice (10:1) {Vp*10:6.0f} m3, needles at 3 m grid: {math.ceil(L/3)**2} x {10+1.5:.1f} m")
# season throughput: water season ~80 d with creek water >4 C [ASM]; cycle = thaw + push + mine
for L, thaw_d in ((20, 10), (20, 25), (40, 10), (40, 25)):
    cycle = thaw_d + 1 + (2 if L == 20 else 5)
    blocks = 80//cycle
    print(f"L={L}, thaw {thaw_d} d: cycle {cycle} d -> {blocks} blocks/row/season = {blocks*L*L*10/1e3:5.0f} k m3 per row")
# cost per m3 of overburden, rub [ASM unit costs]
def jack_cost(L, thaw_d):
    cycle = thaw_d + 1 + (2 if L == 20 else 5); vol = (80//cycle)*L*L*10
    crew = 6*0.8e6                          # 6 people x 0.8 Mrub/season
    capex = (12e6 + 3e6*(L/20) + 4e6)/5     # hot-water drill, jacks, pumps / 5 yr
    _, _, _, _, kl, jl = idea2(L, uplift=1.0)
    return (crew + capex)/vol + (kl + jl + 0.03)*DIESEL_RUB_L
for L, td in ((20, 10), (40, 10), (40, 25)):
    print(f"jacked stripping L={L}, thaw {td} d: {jack_cost(L, td):5.0f} rub/m3")
# baseline: dozer D10/D375 class 55-75 l/h; production frozen ripped 80-200 bank m3/h; layer-thaw 150-300 [REF Cat handbook, ASM]
for name, lph, prod in (("rip+doze frozen", 65, 100), ("natural layer-thaw doze (cheapest)", 65, 220), ("drill-blast+excavator+truck", 0, 0)):
    if prod: print(f"baseline {name}: {lph/prod:4.2f} l/m3")
base_strip = {"layer-thaw dozing": 110, "rip+doze": 160, "drill-blast-truck": 220}   # rub/m3 all-in [ASM]
H, Hp, gpay, rec2 = 10.0, 1.5, 1.5, 0.9
other = 350 + 250                                   # pay excavation+washing, overhead per m3 pay [ASM]
for k, c in base_strip.items():
    cg = (c*H/Hp + other)/(gpay*rec2)
    print(f"baseline {k:18s}: {cg:6.0f} rub/g")
cj = (jack_cost(40, 10)*H/Hp + other + 15)/(gpay*rec2)   # +15 rub/m3 pay for injection pumping
print(f"jacked 40 m blocks: {cj:6.0f} rub/g ; ratio to cheapest baseline {(110*H/Hp+other)/(gpay*rec2)/cj:4.2f}")

# ============================ IDEA 3 ============================
hdr("IDEA 3  floating bluff coal miner")
# demand: Verkhoyansk district 77 kt/yr [S12]; ~7 t/person/yr (population ~11k [ASM])
for pop in (500, 1000, 2000):
    print(f"settlement {pop}: {pop*7:6.0f} t coal/yr")
# restack material balance: removed rock (bulk factor 1.4 as dry-stone) must fit into coal void + original rock space
for m in (1.5, 2.0, 3.0, 5.0):
    Hmax = m*(1 + 1/0.4)     # overburden swell 0.4 must fit into coal void m
    print(f"seam {m} m: full restack in place only if bluff (seam floor to top) <= {Hmax:4.1f} m, i.e. overburden/seam <= 2.5")
# production: season, excavator in frozen coal, dry-stone placement rate
nav_days = 110; mine_days = 60; hours = 12
for rate in (60, 120):
    print(f"excavator {rate} t/h: {rate*hours*mine_days/1e3:5.0f} kt/season")
for Hb, m, d in ((10, 2, 10), (10, 2, 20), (20, 2, 20)):
    rev = 1.2*Hb*1.0/(1.3*m*d)                        # m3 revetment per t coal (1.0 m skin) [S15: CRR >=0.8-1.5 m]
    for st in (5, 15, 30):                            # m3/h dry-stone placement [ASM; HEAP 12 t machine, rate unpublished]
        cap = st*hours*mine_days/rev
        print(f"bluff {Hb} m, seam {m} m, cut {d} m: {rev:4.2f} m3 revetment/t -> stacking {st:2d} m3/h caps coal at {cap/1e3:6.1f} kt/season")
# delivered cost rub/t at boilerhouse
cap_rub = 200e6*0.15; opex = 15e6 + 18e6 + 10e6
for tons in (20e3, 50e3):
    mine = (cap_rub + opex)/tons
    for D, rkm in ((50, 4), (150, 4)):
        tot = mine + D*rkm + 600                       # +600 unloading/yard/truck [ASM]
        print(f"floating miner {tons/1e3:3.0f} kt/yr, haul {D} km: {tot:6.0f} rub/t; per GJ at 18 MJ/kg (oxidised) {tot/18:5.0f} rub/GJ")
print(f"baseline A Kolyma depots tender 701.6 Mrub/100,778 t = {701.57e6/100778:5.0f} rub/t (S11) -> {701.57e6/100778/21:4.0f} rub/GJ at 21 MJ/kg")
print(f"baseline B small land pit 2,000 rub/t + 60 km winter-road truck @15 rub/t-km + 600 = {2000+60*15+600} rub/t  [ASM]")
print("baseline C Arctic multi-leg chain: up to 25,000 rub/t (S10, REC range 3.5-25 k)")

# ============================ IDEA 4 ============================
hdr("IDEA 4  wintering miner-barge boilerhouse")
def draft(Q, L, B, Cb=0.88, light_frac=0.22):
    return Q*(1 + light_frac)/(1.0*L*B*Cb)
for Q, L, B in ((8000, 130, 22), (5000, 110, 18), (2000, 90, 18), (2000, 100, 22), (1500, 80, 18)):
    print(f"hold {Q:5d} t, {L}x{B} m: draft {draft(Q, L, B):4.2f} m  (Arctic tributaries <~1.5-2 m in low water, S12)")
# heat: 2,000 t coal x 20 MJ/kg x 0.75 over 270 d
for Q in (2000, 5000, 8000):
    E = Q*1e3*20e6*0.75
    print(f"{Q} t/winter: average {E/(270*86400)/1e6:4.1f} MW, peak ~{2.5*E/(270*86400)/1e6:4.1f} MW, ~{Q/7:5.0f} people")
# time window: leave after break-up/heating end (~1 Jun), back before heating start (~1 Sep): 92 d
for D in (300, 800, 1500):
    trip = D/(9*20) + D/(15*20) + 8000/(100*20) + 5
    print(f"D={D} km: round trip + mining {trip:4.1f} d vs window 92 d")
# per-tonne economics vs status quo (river settlement)
for D in (300, 800, 1500):
    for rkm in (3, 5):
        idea = 1500 + D*rkm                                 # mined at own seam (~1,500 rub/t, Idea-3 cost) + own freight
        hull = (30e6*0.15)/2000                             # used 2,000 t hull + winter fittings, 30 Mrub [ASM]
        main = (15e6*0.12)/2000                             # 0.5 km heat main [ASM]
        saved = 400 + 300 + 0.06*6960                       # transshipment, truck to boilerhouse, 6 % stock losses [ASM]
        net = idea + hull + main
        print(f"D={D:4d} km @{rkm} rub/t-km: idea {net:6.0f} rub/t (incl. hull {hull:4.0f}, main {main:3.0f}) "
              f"vs status quo {6960+saved:6.0f} rub/t at Kolyma prices -> ratio {(6960+saved)/net:4.2f}")
newhull = (150e6*0.15)/2000
print(f"if hull is new (150 Mrub): +{newhull:5.0f} rub/t -> kills the advantage")

hdr("ROUND-2 additions")
# Idea 1: if dredge is grid-powered there is no free genset heat -> diesel boiler for pond
for Ta in (-35, -45):
    q = open_water_loss(Ta); W_need = pond*q
    l_day = W_need*86400/(DIESEL_MJ_L*1e6*0.85)
    print(f"Idea1 grid-powered dredge, air {Ta}: pond heat {W_need/1e6:4.2f} MW = {l_day:5.0f} l/d -> {l_day*DIESEL_RUB_L/(V_day*winter_f):4.0f} rub/m3 extra")
# Idea 2 round 2: one hot-water drill + crew shared by staggered rows; drill-limited throughput
for L, vdrill in ((40, 1.0), (40, 0.5), (30, 1.0)):
    holes_m = (2*L/0.15)*10 + (math.ceil(L/3)**2)*11.5          # kerf holes at 0.15 m spacing + needles
    drill_days = holes_m/(vdrill*60)/20                          # 20 h/day
    blocks = int(80/ drill_days)
    vol = blocks*L*L*10
    crew = 6*0.8e6; capex = (12e6 + 3e6*(L/20) + 4e6)/5
    _, _, _, _, kl, jl = idea2(L, uplift=1.0)
    c = (crew + capex)/vol + (kl + jl + 0.03)*DIESEL_RUB_L
    cg = (c*H/Hp + other + 15)/(gpay*rec2)
    print(f"Idea2 L={L}, drill {vdrill} m/min: {holes_m:6.0f} m drilled/block, {drill_days:4.1f} d/block, "
          f"{blocks} blocks = {vol/1e3:4.0f} k m3/season/drill -> {c:4.0f} rub/m3, {cg:5.0f} rub/g, "
          f"vs layer-thaw dozing {(110*H/Hp+other)/(gpay*rec2)/cg:4.2f}x")
# slot refreeze time (half-width 0.1 m, -3 C ground)
print(f"Idea2 thawed 0.2 m slot refreezes in ~{0.4*RHO_I*LF*0.1**2/(2*2.0*3)/86400:3.1f} d unless flushed with creek water")
# Idea 3 round 2: rock handling shares the excavator; strip ratio SR (m3 rock per m3 coal)
for SR in (0.5, 1.0, 2.5):
    for rate in (90,):
        coal_m3h = rate/(1 + SR)
        tons = coal_m3h*1.3*hours*mine_days
        mine = (cap_rub + opex)/tons
        tot = mine + 50*4 + 600
        print(f"Idea3 SR {SR}: {tons/1e3:5.1f} kt/season, delivered (50 km) {tot:5.0f} rub/t = {tot/18:4.0f} rub/GJ "
              f"vs Kolyma depots {6962/21:4.0f} rub/GJ -> {6962/21/(tot/18):4.2f}x ; vs land pit {3500/21/(tot/18):4.2f}x")
# Idea 4 round 2: barge does charter freight 75 d in summer -> hull capital offset
for D in (300, 500, 800):
    idea = 1500 + D*4 + 0 + (5e6*0.12)/2000         # hull paid by summer charter; short 150 m main 5 Mrub
    print(f"Idea4 D={D} km, hull paid by charter, short main: {idea:5.0f} rub/t vs 8078 -> {8078/idea:4.2f}x")
