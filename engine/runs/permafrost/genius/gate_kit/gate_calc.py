"""Kill-test screening of the 8 ideas in TASK.md with the verified kit (engine/kit).
Margins = available / required. Chain ratio = current best-practice delivered cost / cost with the idea.
Run: python3 gate_calc.py
"""
import math
import sys

sys.path.insert(0, '/home/user/SomeRepository/engine')
from kit import ice, thermal, geotech, hydro, naval, econ, stats, climate, data  # noqa: E402

FX = data.get('price.fx_rub_usd')
G_OZ = data.G_PER_OZ
LIMIT = data.get('limit.fishery_ss_increment_high')          # +0.25 mg/L
CURT = data.get('limit.silt_curtain_efficiency')
yak = data.monthly('Yakutsk')

# ---- ledger A: non-mining part of the delivered gold cost (other incl. MET + outbound), RUB/g
A_RUB_G = 6900.0
A_REST = A_RUB_G * (0.22 + 0.002)                              # ~1,532 RUB/g, same with or without the idea
gold_price_rub_g = data.get('price.gold') * FX / G_OZ


def chain_gold(base_step, idea_step):
    return econ.ratio_vs_baseline(base_step + A_REST, idea_step + A_REST)


def p(*a):
    print(*a)


p(f"Ledger A rest-of-chain {A_REST:.0f} RUB/g; gold price {gold_price_rub_g:.0f} RUB/g; fishery limit {LIMIT} mg/L")

# =====================================================================================  IDEA 1
p("\n=== IDEA 1 Under-ice talik crawler")
# 7 turbidity: 3,400 mg/L per day without the cell (idea's own figure); hung curtain under ice: kit says <=0.45
c_out_045 = hydro.silt_curtain_outside(3400, CURT['floating_alone'])
c_out_095 = hydro.silt_curtain_outside(3400, CURT['combined_cage'])
m1_turb = LIMIT / c_out_045
p(f"turbidity outside cell after 1 day: {c_out_045:.0f} mg/L (eff .45), {c_out_095:.0f} (eff .95) vs +{LIMIT}"
  f" -> margin {m1_turb:.1e} .. {LIMIT / c_out_095:.1e}")
# 2 ice bearing: 25 t parked for months beside the 1.4x1.4 m slot / moon-pool, ice 1.1 m
cap = ice.stationary_load_capacity(1.1, 168) * ice.edge_capacity_factor(1.1)
cap_int = ice.stationary_load_capacity(1.1, 168)
m1_ice = cap / 25.0
p(f"ice 1.1 m parked (<=7 d heuristic) {cap_int:.1f} t interior, {cap:.1f} t at slot edge vs 25 t -> margin {m1_ice:.2f}"
  " (parked >7 d: Gold not applicable)")
# 1 window: date of 1.1 m ice with snow-covered alpha vs claimed a=0.027
fdd_claim = (1.1 / 0.027) ** 2
for a in (0.024, 0.020, 0.017):
    fdd = (1.1 / a) ** 2
    delay = (fdd - fdd_claim) / ((-yak['Dec'] - yak['Jan']) / 2)
    p(f"  alpha {a}: FDD {fdd:.0f} vs {fdd_claim:.0f} -> {delay:.0f} d later than mid-Dec")
under_ice_days_claim = 270 - 125           # 270 d/yr total minus ~125 d open water
delay_mid = ((1.1 / 0.020) ** 2 - fdd_claim) / 37.5
m1_win = (under_ice_days_claim - delay_mid) / under_ice_days_claim
p(f"window: under-ice days {under_ice_days_claim} claimed, lose {delay_mid:.0f} d at alpha .020 -> margin {m1_win:.2f}")
# 6 moon-pool 2 m2 kept open with 2 kW at Yakutsk January
q2 = thermal.open_water_heat_loss(yak['Jan'], 2.0)
q5 = thermal.open_water_heat_loss(yak['Jan'], 5.0)
m1_moon = 2000 / (2 * q5)
p(f"moon-pool loss {q2:.0f}-{q5:.0f} W/m2 -> need {2*q2/1e3:.1f}-{2*q5/1e3:.1f} kW vs 2 kW -> margin {m1_moon:.2f}-{2000/(2*q2):.2f}")
# chain: lake placer that cannot be drained -> summer suction dredge 2,140; drainable -> 1,930
r1 = chain_gold(2140, 1600)
r1b = chain_gold(1930, 1600)
p(f"chain ratio {r1:.2f} (vs suction dredge), {r1b:.2f} (vs drain+dozer)")
p("verdict", econ.gate_verdict(m1_turb, r1))

# =====================================================================================  IDEA 2
p("\n=== IDEA 2 Wintering coal CHP barge")
fuel_MW = 0.3 / (0.8 * 0.16)
days = 1780 * 21e9 / (fuel_MW * 1e6) / 86400
p(f"fuel {fuel_MW:.2f} MW; 1,780 t at 21 GJ/t lasts {days:.0f} d at full output; reject heat {0.8*fuel_MW-0.3:.2f} MW")
L, B = 80.0, 15.0                                   # typical 2,000 t river dry-cargo barge (assumed)
dr = naval.draught_from_payload(1780 + 100, L, B)   # coal + ~100 t CHP plant
need = naval.depth_needed(dr, h_ice=1.75)
avail_arctic = data.get('river.guaranteed_depth_lena')['Arctic Lena-basin reaches']
yana = data.lo_hi('river.yana_indigirka_low_water_depth')
m2_depth = avail_arctic / need
p(f"draught {dr:.2f} m; wintering depth needed {need:.2f} m vs Arctic Lena-basin {avail_arctic} m (Yana/Indigirka {yana})"
  f" -> margin {m2_depth:.2f} ({yana[0]/need:.2f}-{yana[1]/need:.2f}); Lena main stem 2.9 m -> {2.9/need:.2f}")
perim = 2 * (L + B)
for w in (0.5, 1.0):
    for U in (2.0, 5.0):
        q = thermal.open_water_heat_loss(-38.6, U)
        p(f"  moat {w} m wide, U {U}: {q:.0f} W/m2 -> {q*perim*w/1e3:.0f} kW vs 104 kW")
q5 = thermal.open_water_heat_loss(-38.6, 5.0)
m2_moat = 104e3 / (q5 * perim * 0.5)
p(f"moat margin (0.5 m, 5 m/s) {m2_moat:.2f}")
net_t = 1780 - 381 * 0.8                              # coal out, ash back in hold
rise = net_t * naval.rise_per_tonne(L * B * 0.95)
P = net_t * 1e3 * 9.81 / perim
cap_line = ice.edge_line_load_capacity(0.75e6, 1.5)
p(f"hull rise {rise:.2f} m; uplift {P/1e3:.0f} kN/m vs edge capacity {cap_line/1e3:.0f} kN/m (1.5 m ice, 0.75 MPa)"
  f" -> margin {cap_line/P:.2f} only if moat freezes")
# chain: winter kWh; capex as written + operators at local wages
crf = econ.crf(0.14, 15)
kwh = 0.3e3 * days * 24
for capex in (132e6, 237e6):
    c = (capex * (crf + 0.03) + 6 * 2.0e6) / kwh
    p(f"  capex {capex/1e6:.0f} M RUB -> {c:.0f} RUB/kWh incl. 6 local operators")
extra_fuel = (fuel_MW - (0.8 * fuel_MW - 0.3 - 0.148) / 0.65) / fuel_MW    # moat+hold take 148 kW of reject heat
fuel_rub_kwh = extra_fuel * fuel_MW / 0.3 * 10000 / 5800                    # 10k RUB/t coal, 5.8 MWh/t
c_lo = (132e6 * (crf + 0.03) + 6 * 2.0e6) / kwh + fuel_rub_kwh
c_hi = (237e6 * (crf + 0.03) + 6 * 2.0e6) / kwh + fuel_rub_kwh
diesel = 0.30 * 135 + 15          # village genset 0.30 l/kWh x 135 RUB/l (ledger 120-150) + ~15 O&M/capital
r2 = econ.ratio_vs_baseline(diesel, (c_lo + c_hi) / 2)
p(f"extra fuel {fuel_rub_kwh:.1f} RUB/kWh; idea {c_lo:.0f}-{c_hi:.0f} RUB/kWh; village diesel {diesel:.0f} (idea 45-75)")
p(f"chain ratio {r2:.2f} (range {econ.ratio_vs_baseline(45, c_hi):.2f}-{econ.ratio_vs_baseline(75, c_lo):.2f});"
  f" at 2x capex (Far North premium): {econ.ratio_vs_baseline(diesel, ((264e6+474e6)/2*(crf+0.03)+12e6)/kwh):.2f}")
m2 = min(m2_depth, m2_moat)
p("verdict", econ.gate_verdict(m2, r2))

# =====================================================================================  IDEA 3
p("\n=== IDEA 3 Ice-deck borehole talik mining")
gold_18 = ice.gold_allowable_load(1.8)
h_nat = ice.ice_thickness(climate.degree_days({k: yak[k] for k in ('Nov', 'Dec', 'Jan')})[0] + 240, 0.024)
flood = 1.8 - h_nat
gold_fl = ice.gold_allowable_load(h_nat, flooded_m=flood)
park = ice.stationary_load_capacity(1.8, 120) * ice.edge_capacity_factor(1.8)
park_fl = 0.5 * gold_fl * ice.edge_capacity_factor(1.8)
m3_ice = park_fl / 25.0
p(f"Gold 1.8 m clear {gold_18:.0f} t; natural ice end-Jan {h_nat:.2f} m + {flood:.2f} m flooded -> {gold_fl:.0f} t;"
  f" parked at hole edge {park:.0f} t (clear) / {park_fl:.0f} t (flooded) vs 25 t -> margin {park/25:.2f} / {m3_ice:.2f}")
# 7 turbidity in the closed under-ice lake: tailings back down caved holes connected to the lake bed
rel = hydro.fines_release_rate(30, 1.9, 0.2, 0.005)        # kg/s at 0.5% escape (kit default)
for V in (0.16e6, 1.0e6):
    inc = rel * 86400 / V * 1e3                               # mg/L per day, no outflow under ice
    p(f"  under-ice volume {V/1e6:.2f} Mm3: +{inc:.2f} mg/L per day vs +{LIMIT} -> margin {LIMIT/inc:.2f}")
m3_turb = LIMIT / (rel * 86400 / 1.0e6 * 1e3)
# 5 jet reach R = 9 m in a flooded cavity
u9 = hydro.jet_centreline_velocity(120, 0.025, 9.0)
tau = 0.5 * 1000 * 0.01 * u9 ** 2
dmov = hydro.critical_grain_size(tau)
p(f"jet 25 mm @120 m/s at 9 m: {u9:.2f} m/s, tau {tau:.0f} Pa moves d <= {dmov*100:.1f} cm (pay <15 cm, d50 ~2-3 cm)")
cover = math.pi / 4
p(f"18 m grid, R 9 m circles cover {cover:.3f} of area x 0.86-0.89 in-circle = {cover*0.86:.2f}-{cover*0.89:.2f} overall")
r3 = chain_gold(8800, 3900)
p(f"chain ratio {r3:.2f} (range {chain_gold(8800, 4800):.2f}-{chain_gold(8800, 3000):.2f})")
m3 = min(m3_ice, m3_turb)
p("verdict", econ.gate_verdict(m3, r3))

# =====================================================================================  IDEA 4
p("\n=== IDEA 4 Frozen-roof jet adits")
E = thermal.thaw_energy_per_m3(0.3, -4)
dT = 6.0
for v_mh in (3.7, 8.0):
    h_req = v_mh / 3600 * E / dT
    p(f"  advance {v_mh} m/h needs face-average h {h_req/1e3:.1f} kW/m2K at dT {dT}")
h_stag = thermal.h_jet_stagnation(15, 0.05)
h_face = h_stag / 3
h_req_lo = 3.7 / 3600 * E / dT
h_req_hi = 8.0 / 3600 * E / dT
m4_face = h_face / ((h_req_lo + h_req_hi) / 2)
p(f"jet stagnation h {h_stag/1e3:.1f} kW/m2K (50 mm, 15 m/s), face-average ~{h_face/1e3:.1f} -> margin"
  f" {h_face/h_req_hi:.2f}-{h_face/h_req_lo:.2f} (stagnation-only {h_stag/h_req_hi:.2f}-{h_stag/h_req_lo:.2f})")
v_stag = thermal.face_retreat_rate(h_stag, dT, E) * 3600
v_gn = thermal.face_retreat_rate(thermal.h_gnielinski(1.0, 0.2, roughness_factor=3), dT, E) * 3600
v_coat = thermal.debris_coat_limited_flux(2.0, dT, 0.01) / E * 3600
p(f"retreat: stagnation point {v_stag:.2f} m/h, rough channel {v_gn:.2f} m/h, 1 cm debris coat {v_coat*1000:.1f} mm/h")
# 6 pond 2 ha net gain claimed 80-150 W/m2 (Yakutsk GHI, recirculating water ~4 C)
ghi = data.get('climate.ghi_Yakutsk_MJm2_month')
fl = []
for m, Ta in (('Jun', yak['Jun']), ('Jul', yak['Jul']), ('Aug', yak['Aug'])):
    sw = ghi[m] * 1e6 / (data.MONTH_DAYS[m] * 86400)
    f = thermal.water_surface_net_flux(sw, Ta, 4.0)
    fl.append(f)
    p(f"  {m}: SW {sw:.0f} W/m2, Ta {Ta} -> pond net {f:.0f} W/m2")
m4_pond = (sum(fl) / 3) / 115
p(f"pond mean {sum(fl)/3:.0f} W/m2 vs claimed 80-150 (mid 115) -> margin {m4_pond:.2f}")
# 4 pillars: 0.4-1.2 MPa vs long-term frozen gravel
lt = data.lo_hi('ground.frozen_gravel_long_term')
p(f"pillar: stress 0.4-1.2 MPa vs long-term {lt} MPa -> margin {lt[0]/1.2:.2f}-{lt[1]/0.4:.1f};"
  f" 20 m cover tributary {geotech.pillar_tributary_stress(20e3, 20, 0.5)/1e6:.2f} MPa at 50% extraction")
r4 = chain_gold((1040 + 1670) / 2, (550 + 660) / 2)
p(f"chain ratio {r4:.2f} (range {chain_gold(1040, 660):.2f}-{chain_gold(1670, 550):.2f})")
p("verdict", econ.gate_verdict(m4_face, r4))

# =====================================================================================  IDEA 5
p("\n=== IDEA 5 Barge-mounted bluff auger coal")
cap_season = econ.season_capacity(60, 100, availability=0.56)
p(f"season capacity 60 t/h x 100 d x 0.56 = {cap_season/1e3:.0f} kt; at historical 21.5 t/h:"
  f" {econ.season_capacity(21.5, 100, availability=0.56)/1e3:.0f} kt -> window margin"
  f" {econ.window_margin(100, 80e3, 60*24*0.56):.2f} / {econ.window_margin(100, 80e3, 21.5*24*0.56):.2f}")
ay = data.get('base.arctic_yakutia_utility_coal')
district = ay[0] / 13
p(f"80 kt = {econ.market_share(80e3, ay[0]):.2f} of all Arctic Yakutia utility coal, "
  f"{econ.market_share(80e3, 122e3):.2f} of all Yakutian waterborne communal coal")
m5_mkt = district / 80e3
p(f"one Arctic district (205 kt/13) {district/1e3:.1f} kt vs 80 kt -> margin {m5_mkt:.2f};"
  f" 10 kt village cluster -> {10e3/80e3:.2f}")
# 4 web pillars between 1.5 m auger holes, 62% recovery, 25 m bluff
B_h = 1.5
w_web = B_h * (1 - 0.62) / 0.62
s_web = geotech.web_pillar_stress(22e3, 25, w_web, B_h)
S_web = geotech.mark_bieniawski_strength(6.0e6, w_web, B_h)
p(f"web {w_web:.2f} m: stress {s_web/1e6:.2f} MPa vs strength {S_web/1e6:.1f} MPa -> margin {S_web/s_web:.1f}")
anc = geotech.adfreeze_capacity(math.pi * 0.1, 3.0, -0.5, 'clay')
p(f"thrust-frame anchor (100 mm, 3 m, -0.5 C) {anc/1e3:.0f} kN each -> {300e3/anc:.1f} anchors per 300 kN")
lm = (1100 + 3400) / 2
r5 = econ.ratio_vs_baseline((2800 + 3700) / 2 + lm, 1800 + lm)
p(f"chain ratio at boiler {r5:.2f} (step {(2800+3700)/2/1800:.2f}); at market-limited 20 kt (4,100 RUB/t):"
  f" {econ.ratio_vs_baseline((2800+3700)/2 + lm, 4100 + lm):.2f}")
p("verdict", econ.gate_verdict(m5_mkt, r5))

# =====================================================================================  IDEA 6
p("\n=== IDEA 6 Channel-talik seam dredging")
rel_cut = hydro.fines_release_rate(55, 1.0, 0.10, 0.005)
rel_scr = hydro.fines_release_rate(55, 1.0, 0.05, 1.0)          # sub-screen fines go overboard with the water
q_cut = hydro.dilution_flow_required(rel_cut)
q_all = hydro.dilution_flow_required(rel_cut + rel_scr)
p(f"cutter only (10% fines, 0.5%): {rel_cut:.3f} kg/s -> {q_cut:.0f} m3/s; + screen underflow (5% <63 um):"
  f" {rel_cut+rel_scr:.2f} kg/s -> {q_all:.0f} m3/s full mixing")
# plume width at a 500 m control section, bank source, river 5 m deep, U 1 m/s, S 1e-4
ustar = math.sqrt(9.81 * 5 * 1e-4)
eps = hydro.transverse_mixing_coefficient(5, ustar)
sig = math.sqrt(2 * eps * 500 / 1.0)
q_plume = 2 * 2 * sig * 5 * 1.0                                   # ~2 sigma half-width against the bank
Q_kol = 3109.0
p(f"eps_y {eps:.2f} m2/s, plume ~{4*sig:.0f} m wide at 500 m -> dilution flow ~{q_plume:.0f} m3/s;"
  f" full-mixing length (1 km wide) {hydro.mixing_length(1.0, 1000, eps)/1e3:.0f} km")
m6_turb = q_plume / q_all
p(f"turbidity margin at control section {m6_turb:.3f}; full mixing on Kolyma mean {Q_kol:.0f} m3/s: {Q_kol/q_all:.2f};"
  f" cutter-only at control section {q_plume/q_cut:.1f}")
dd = (8 + 25) / 2
m6_win = econ.window_margin(61, 4 * dd + 8, 1.0)
p(f"window: 4 bends x {dd} d + 8 d transit in Jun-Jul 61 d -> margin {m6_win:.2f} ({61/(4*25+8):.2f}-{61/(4*8+8):.2f})")
lm_g = lm / 3.67
idea_g = (730 + 930) / 2
pit_g = idea_g * (1.4 + 2.4) / 2
r6 = econ.ratio_vs_baseline(pit_g + lm_g, idea_g + lm_g)
p(f"chain ratio at boiler vs bank micro-pit {r6:.2f} (micro-pit {pit_g:.0f}, idea {idea_g:.0f}, last mile {lm_g:.0f} RUB/Gcal)")
p("verdict", econ.gate_verdict(m6_turb, r6))

# =====================================================================================  IDEA 7
p("\n=== IDEA 7 Thermal drift-and-drop placer caving")
E7 = thermal.thaw_energy_per_m3(0.3, -4)
for dT7 in (4.0, 5.0):
    wr = thermal.water_ratio(E7, dT7)
    p(f"  water ratio at dT {dT7}: {wr:.1f} m3/m3 at 100%, {wr/0.5:.1f} at 50% vs claimed 3-8")
wr50 = thermal.water_ratio(E7, 5.0, 0.5)
m7_water = 5.5 / wr50
v_coat_lo = thermal.debris_coat_limited_flux(2.0, 5.0, 0.02) / E7 * 86400
v_coat_hi = thermal.debris_coat_limited_flux(2.0, 5.0, 0.01) / E7 * 86400
v_req = 45 / 30.0                                   # 45 m drift in <=30 d of a 90-d water season
m7_thaw = (v_coat_lo + v_coat_hi) / 2 / v_req
p(f"drift face retreat (1-2 cm coat, dT 5) {v_coat_lo:.2f}-{v_coat_hi:.2f} m/day vs {v_req:.1f} m/day needed"
  f" -> margin {m7_thaw:.2f}; vs 5 m/day theory {((v_coat_lo+v_coat_hi)/2)/5:.2f}; window"
  f" {econ.window_margin(90, 45, (v_coat_lo+v_coat_hi)/2):.2f} drifts/season")
p(f"water margin (mid 5.5 vs {wr50:.1f} at 50%, dT 5) {m7_water:.2f}")
# 4 roof caving at 10 m cover: Vyalov fits through kit's typical tensile ranges
for s1, s2, lab in ((1.0e6, 0.2e6, 'weak'), (1.5e6, 0.35e6, 'central'), (2.0e6, 0.5e6, 'strong')):
    beta, Bv = geotech.vyalov_fit(s1, 60, s2, 50 * 3.156e7)
    out = []
    for span in (18, 22, 25):
        s = geotech.beam_self_weight_stress(19e3, span, 10)
        out.append(f"{span} m {s/1e6:.2f} MPa -> {geotech.vyalov_time_to_failure(s, beta, Bv)/86400:.3g} d")
    p(f"  roof {lab}: " + "; ".join(out))
r7 = chain_gold((2270 + 3980) / 2, 1930)
p(f"chain ratio {r7:.2f} (range {chain_gold(2270, 1930):.2f}-{chain_gold(3980, 1930):.2f})")
m7 = min(m7_thaw, m7_water)
p("verdict", econ.gate_verdict(m7, r7))

# =====================================================================================  IDEA 8
p("\n=== IDEA 8 Wintering barge bunker swap")
L8, B8 = 75.0, 14.0
dr8 = naval.draught(660 + 0.22 * 1500, L8, B8, Cb=0.88)
for h in (1.3, 1.75):
    p(f"  ice {h} m: depth needed {naval.depth_needed(dr8, h_ice=h):.2f} m vs 1.2 m; "
      f"freezes to bed at FDD 5,500: {ice.freezes_to_bed(1.2, 5500)}")
m8_depth = 1.2 / naval.depth_needed(dr8, h_ice=1.3)
p(f"draught {dr8:.2f} m -> margin {m8_depth:.2f} (Lena Tabaga ice 1.3 m); Arctic 1.75 m:"
  f" {1.2/naval.depth_needed(dr8, h_ice=1.75):.2f}")
per8 = 2 * (L8 + B8)
m8_moat = 55e3 / (thermal.open_water_heat_loss(-38.6, 5.0) * per8 * 0.4)
p(f"moat 0.4 m x {per8:.0f} m at 5 m/s needs {thermal.open_water_heat_loss(-38.6, 5.0)*per8*0.4/1e3:.0f} kW vs 55 -> {m8_moat:.2f}")
hold_loss = 0.4 * L8 * B8 * 38.6      # 0.5 m frozen coal crust k~0.2 -> U 0.4 W/m2K
p(f"hold: frozen-crust heat loss ~{hold_loss/1e3:.0f} kW vs 27 kW -> {27e3/hold_loss:.2f}")
avoided = (1100 + 3400) / 2
c_now = data.get('price.settlement_coal_at_boiler')
r8 = econ.ratio_vs_baseline(c_now, c_now - (avoided - 1360))
p(f"chain ratio {r8:.3f} (range {econ.ratio_vs_baseline(c_now, c_now-(1100-1360)):.3f}-"
  f"{econ.ratio_vs_baseline(c_now, c_now-(3400-1360)):.3f}); ceiling if all avoided cost were free"
  f" {econ.ceiling_ratio(3400/c_now):.2f}")
p("verdict", econ.gate_verdict(min(m8_depth, m8_moat), r8))
