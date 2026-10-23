"""Gate screening for 8 permafrost_v5 ideas. Kit functions used wherever available.
Own code (checked once below): berth-pool heat reserve, SPoT $/lb -> RUB/t-km, daily ice growth from FDD."""
import sys
sys.path.insert(0, '/home/user/SomeRepository/engine')
from kit import ice, thermal, naval, econ, climate, data

FX = data.get('price.fx_rub_usd')
G = 9.81
P = lambda *a: print(*a)

# ---------------- self-checks of own code on known answers
# 1 m3 of water cooled 1 K releases 4.19 MJ
assert abs(1.0 * 1000 * 4186 * 1.0 - 4.186e6) < 1
# 1 short ton (2000 lb) = 0.907 t -> $1/lb = $2204.6/t
assert abs(2204.62 * 0.4536 - 1000) < 0.1
# daily FDD accumulation of a constant -10 C over 100 d = 1000 C*d -> ice 0.024*sqrt(1000)=0.759 m
assert abs(ice.ice_thickness(1000, 0.024) - 0.759) < 0.005

flex = tuple(v*1e6 for v in data.lo_hi('ice.flexural_strength'))  # MPa -> Pa
P('ice flexural strength', flex, data.info('ice.flexural_strength').source)
util_t_person = 3.0                       # base.arctic_yakutia_utility_coal ~3 t/person
village_coal = 1000 * util_t_person       # 1,000-person village, t/yr
boiler = data.get('price.settlement_coal_at_boiler')   # 23,000 RUB/t
depot = data.get('price.kolyma_depot_coal')            # 6,962 RUB/t delivered riverside depot
lorp = data.get('price.lorp_seasonal_haul_rub_t')      # 8,000 RUB/t barge haul
P('village coal t/yr', village_coal, '| boiler', boiler, '| Kolyma depot', depot, '| LORP haul', lorp)

# ---------------- generic river dry-cargo barge (est.): 80 x 15 m, Cb 0.9, design draught 2.5 m, light 0.45 m
L, B, Cb, T_full, T_light = 80.0, 15.0, 0.9, 2.5, 0.45
light_t = naval.displacement_t(L, B, T_light, Cb)
full_pay = naval.payload_at_draught(L, B, T_full, light_t, Cb)
P(f'\nbarge 80x15: lightship {light_t:.0f} t, full payload {full_pay:.0f} t')

# ================= IDEA 1 backhaul coal
P('\n=== IDEA 1')
lo, hi = data.lo_hi('river.yana_indigirka_low_water_depth')   # 1.5-2.0 m late-season (proxy)
for d in (lo, hi):
    pay = naval.payload_at_draught(L, B, d - 0.2, light_t, Cb)
    P(f' late-season depth {d} m -> payload {pay:.0f} t = {pay/full_pay:.2f} of full')
# chain: barge leg = LORP 8,000 of 23,000; backhaul at marginal cost halves it (generous)
share_barge = lorp / boiler
P(f' barge share {share_barge:.2f}; ceiling if barge free {econ.ceiling_ratio(share_barge):.2f}')
r1 = econ.ratio_vs_baseline(boiler, boiler - 0.5 * lorp)
r1d = econ.ratio_vs_baseline(depot, depot - 0.5 * 0.5 * depot)  # riverside depot, barge ~50% of depot price (est.)
P(f' ratio at boiler (barge halves) {r1:.2f}; riverside depot {r1d:.2f}')

# ================= frozen-in family: common hull-year economics
P('\n=== frozen-in barge family (2,3,4,8)')
capex_5kt_usd = 3.0e6                    # Ukrrechflot 2020: ~$3 M per 5,000 t barge (gmk.center)
capex_3kt = econ.six_tenths_scaling(capex_5kt_usd * FX, 5000, 3000)
hull_year_new = econ.annualised_capex(capex_3kt, 0.14, 25, om_frac=0.03)
P(f' new 3 kt barge {capex_3kt/1e6:.0f} M RUB -> {hull_year_new/1e6:.1f} M RUB/yr = {hull_year_new/village_coal:.0f} RUB/t')
boiler_capex = 40e6                      # est. containerised 3-5 MW coal boiler module + fuel feed
pipe_capex = 200 * 2 * 20e3              # est. 200 m twin insulated main, 20k RUB/m
extras_year = econ.annualised_capex(boiler_capex + pipe_capex, 0.14, 15, 0.03)
P(f' boiler+pipe {extras_year/1e6:.1f} M RUB/yr = {extras_year/village_coal:.0f} RUB/t (existing shore boilerhouse is sunk)')
# removed at a RIVERSIDE settlement (barge reaches it, so no winter road): unloading + stockpile + losses
removed_riverside = 1000 + 0.03 * depot  # est. 1,000 RUB/t handling + 3% stockpile loss
P(f' removed at riverside settlement ~{removed_riverside:.0f} RUB/t = {removed_riverside/(depot+removed_riverside):.2f} of delivered')

# uplift when the cargo is burnt (class 11)
Awp = L * B
rise = naval.rise_per_tonne(Awp) * village_coal
perim = 2 * (L + B)
q_up = village_coal * 1000 * G / perim
for h in (1.2, 1.5, 2.0):
    cap = ice.edge_line_load_capacity(flex[1], h)
    P(f' burn {village_coal:.0f} t: hull wants to rise {rise:.2f} m; uplift {q_up/1e3:.0f} kN/m vs ice {h} m capacity {cap/1e3:.0f} kN/m (sigma {flex[1]/1e6} MPa) margin {cap/q_up:.2f}')

# ================= IDEA 2
P('\n=== IDEA 2')
T_load = naval.draught(light_t + village_coal, L, B, Cb)
for h in data.lo_hi('ice.upper_kolyma_end_winter'):
    P(f' loaded draught {T_load:.2f} m, ice {h} m -> depth needed {naval.depth_needed(T_load, h):.2f} m')
c2_now = depot + removed_riverside
c2_new = depot + (hull_year_new + extras_year) / village_coal
P(f' chain riverside: now {c2_now:.0f}, with idea {c2_new:.0f}, ratio {c2_now/c2_new:.2f}')
m2 = removed_riverside / ((hull_year_new + extras_year) / village_coal)
P(f' removed cost / added hull+boiler cost margin {m2:.2f}')

# ================= IDEA 3 bubbler
P('\n=== IDEA 3')
q_open = thermal.open_water_heat_loss(-40, 3.0)
moat = perim * 1.0                       # 1 m wide moat around hull
need_W = q_open * moat
pool_V = (L + 40) * (B + 40) * 3.0       # berth pool around hull, 3 m deep (est.)
Tw = 0.2                                 # winter bottom water 0.01-0.2 C (DTIC ADA148739); Lena delta -0.1..+0.8
heat = pool_V * 1000 * 4186 * Tw
days = heat / need_W / 86400
ice_days = data.get('river.kolyma_ice_cover_days')
P(f' open-water loss {q_open:.0f} W/m2 x {moat:.0f} m2 = {need_W/1e3:.0f} kW; pool heat at {Tw} C = {heat/1e9:.1f} GJ -> {days:.1f} d vs {ice_days} d: margin {days/ice_days:.3f}')
# through-flow alternative: flow needed at 0.1 K
Qneed = need_W / (1000 * 4186 * 0.1)
P(f' through-flow needed at 0.1 K above freezing: {Qneed:.2f} m3/s of that water drawn to the hull')
scrap_hull = light_t * 25e3              # est. scrap 25k RUB/t steel
hull_year_scrap = econ.annualised_capex(scrap_hull, 0.14, 5) + 5e6   # + est. 5 M RUB/yr survey/repair
added3 = (hull_year_scrap + extras_year) / 2500
P(f' near-scrap hull {scrap_hull/1e6:.1f} M RUB -> {hull_year_scrap/1e6:.1f} M/yr; added per hold-t (2.5 kt) {added3:.0f} vs removed {removed_riverside:.0f} (claimed 11-15k)')
c3_new = depot + added3
P(f' chain riverside ratio {c2_now/c3_new:.2f}')

# ================= IDEA 4 shallow 0.8 m hull holds the year's coal?
P('\n=== IDEA 4')
for (l, b, lt) in ((80, 15, light_t), (100, 16.5, None)):
    lt = lt or naval.displacement_t(l, b, T_light, Cb)
    pay = naval.payload_at_draught(l, b, 0.8, lt, Cb)
    P(f' hull {l}x{b} at 0.8 m: payload {pay:.0f} t vs village {village_coal:.0f} t -> margin {pay/village_coal:.2f}')
P(f' pool depth needed (kit) {naval.depth_needed(0.8, 2.0):.2f} m; idea own rule {0.8+2.0:.1f} m')
# chain: winter-road village; delivered by 0.8 m barge to village removes winter road (300 km x 20) + transship
wr = econ.freight_cost(data.get('price.winter_road_rub_tkm'), 300)
n_hulls = village_coal / naval.payload_at_draught(80, 15, 0.8, light_t, Cb)
pay08 = naval.payload_at_draught(80, 15, 0.8, light_t, Cb)
hull08 = econ.annualised_capex(econ.six_tenths_scaling(capex_5kt_usd * FX, 5000, pay08), 0.14, 25, 0.03)
added4 = n_hulls * hull08 / village_coal + extras_year / village_coal
c4_new = boiler - wr - 1000 - 0.03 * depot + added4
P(f' winter road {wr:.0f}; {n_hulls:.1f} hulls frozen in -> added {added4:.0f} RUB/t; with idea {c4_new:.0f}; ratio {boiler/c4_new:.2f}')

# ================= IDEA 5 sled trains
P('\n=== IDEA 5')
m = data.monthly('Verkhoyansk')
daily = climate.daily_temperatures(m)
# season start Oct 1 (day 273); accumulate FDD from first freezing day
start = next(i for i in range(200, 365) if daily[i] < 0)
fdd, hs = 0.0, []
order = list(range(start, 365)) + list(range(0, 200))
for i in order:
    if daily[i] < 0:
        fdd += -daily[i]
    hs.append((i, ice.ice_thickness(fdd, 0.024), daily[i]))
tractor_t = 40.0                          # est. wide-track tractor for 150-250 t drawbar (Challenger MT865 ~ 20-25 t + ballast/ fuel)
h_req = ice.gold_required_thickness(tractor_t)
truck_t = 40.0                            # loaded winter-road truck, 25 t payload
ok = [i for i, h, t in hs if h >= h_req and t < -5]   # bearing and still cold (before spring decay)
P(f' tractor {tractor_t} t needs {h_req:.2f} m (Gold A 3.5), same as {truck_t} t truck; days with ice >= that and T<-5 C: {len(ok)} (Verkhoyansk normals)')
P(f' season margin {len(ok)/150:.2f} vs claimed 150 d; first day-of-year {ok[0]}')
spot_usd_lb = 3.60                        # DTIC ADA602402 SPoT 2008-11
spot_km = 1660
spot_rub_tkm = spot_usd_lb * 2204.62 / spot_km * FX
P(f' SPoT delivered {spot_usd_lb} $/lb over {spot_km} km = {spot_rub_tkm:.0f} RUB/t-km; target 5 -> margin {5/spot_rub_tkm:.3f}; even /10 for flat Arctic: {50/spot_rub_tkm:.2f}')
bladder_t = 24000 * 3.785 * 0.80 / 1000
P(f' measured tow per tractor 4 bladder sleds 24,000 gal = {bladder_t:.0f} t vs 150-250 t claimed: margin {bladder_t/200:.2f}')

# ================= IDEA 6 bluff lignite
P('\n=== IDEA 6')
tdd = data.lo_hi('climate.thawing_index_N_Yakutia')
Lv = thermal.latent_heat_per_m3(0.40)      # lignite ~30% moisture x 1.25 t/m3 -> ~0.4 vol ice (est.)
for k in (0.33, 0.55):                     # Herrin & Deming 1996: coal matrix 0.22-0.55, mean 0.33 W/mK
    for n in (1.0, 1.3):
        X = thermal.stefan_depth_degree_days(tdd[1], Lv, k, n)
        P(f' k {k} n {n}: Stefan thaw {X:.2f} m vs 1.5 m claimed -> margin {X/1.5:.2f}')
# chain: 1,000-person village, 3,000 t hard coal (~5,500 kcal) -> lignite 3,500 kcal
lig_t = village_coal * 5500 / 3500
face_m = lig_t / (3.0 * 1.5 * 1.25 * 1.0)  # 3 m seam x 1.5 m thaw x 1.25 t/m3
labour = 2.5 * data.get('price.fifo_worker_year')
equip = econ.annualised_capex(45e6, 0.14, 10, 0.05)   # est. excavator + 2 trucks + loader
haul = lig_t * econ.freight_cost(data.get('price.winter_road_rub_tkm'), 30)
other = 5e6                                # est. licence, survey, compliance, stockpile
c6 = (labour + equip + haul + other) / lig_t * 5500 / 3500
P(f' lignite {lig_t:.0f} t/yr, face {face_m:.0f} m/yr; cost {c6:.0f} RUB per hard-coal-equivalent t; ratio {boiler/c6:.2f}')

# ================= IDEA 7 flood crest
P('\n=== IDEA 7')
T_l = naval.draught(light_t + full_pay, L, B, Cb)
for h in data.lo_hi('ice.upper_kolyma_end_winter'):
    P(f' loaded {T_l:.2f} m wintering, ice {h} m -> depth needed {naval.depth_needed(T_l, h):.2f} m')
q_down = full_pay * 1000 * G / perim
for h in (1.05, 1.5):
    cap = ice.edge_line_load_capacity(flex[1], h)
    P(f' winter loading {full_pay:.0f} t into frozen-in hull: {q_down/1e3:.0f} kN/m vs ice {h} m {cap/1e3:.0f} kN/m -> margin {cap/q_down:.2f}; sink {naval.rise_per_tonne(Awp)*full_pay:.2f} m')
# season: Mintrans 23 May open Oroek-Zyryanka .. 10 Oct close Zyryanka-Srednekolymsk = 140 d; ~1,000 km, ~10 d round trip -> ~5 trips (est.)
trips = 5
base_loads = trips * 0.5
new_loads = 1 + (trips - 1) * 0.5
cut = 1 - base_loads / new_loads
P(f' trips {trips}: barge cost/t falls {cut:.2f} (not 0.5)')
for share, lab in ((lorp / boiler, 'boiler 23k'), (0.5, 'riverside depot')):
    P(f'  {lab}: ratio {1/(1-share*cut):.2f}')
P(f' crest window: flood mid-May..Sep (BRE), transit ~4 d; window/transit ~ {40/4:.0f}')

# ================= IDEA 8
P('\n=== IDEA 8')
share_after = removed_riverside / (depot + removed_riverside)
P(f' share after barge haul (riverside) {share_after:.2f} vs required 0.65 -> margin {share_after/0.65:.2f}')
P(f' ceiling ratio if all of it removed free {econ.ceiling_ratio(share_after):.2f}; with hull-year cost ratio {c2_now/c2_new:.2f}')

# ---- IDEA 6 turbidity (class 7): excavator at the toe, 30 m3/h, 1.25 t/m3, 20% fines, 2% falls into river (est.)
from kit import hydro
mr = hydro.fines_release_rate(30, 1.25, 0.20, 0.02)
Qneed = hydro.dilution_flow_required(mr, data.get('limit.fishery_ss_increment_high'))
P(f'\nIDEA 6 turbidity: {mr:.3f} kg/s needs {Qneed:.0f} m3/s full mixing at +0.25 mg/L (small Yakutian river summer Q ~10-300 m3/s, est.)')
for Q in (50, 300):
    P(f'  Q {Q}: margin {Q/Qneed:.2f}')
# ---- IDEA 6 season window (class 1): 4,714 t at 50 t/h, 10 h/day, 0.7 avail, 60 d thawed window
P(f'IDEA 6 window margin {econ.window_margin(60, 4714, 50*10*0.7):.1f}')
