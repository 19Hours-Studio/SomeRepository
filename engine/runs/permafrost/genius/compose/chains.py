"""Compose whole chains from the reviewed pieces P1-P8 and compute honest chain ratios.

Run:  python3 chains.py  > chains_out.txt
All money in RUB (FX 84 RUB/USD from kit.data). Ranges are sampled uniformly (Monte Carlo, fixed seed);
P10/P50/P90 are reported. "est." marks an engineering estimate made here (no source); every other number
is a reviewed piece number, a kit/ledger value, or a value from TASK.md.
"""
import sys
import math
import random

sys.path.insert(0, '/home/user/SomeRepository/engine')
from kit import econ, naval, ice, climate, thermal, hydro, data, stats  # noqa: E402

FX = data.get('price.fx_rub_usd')
N = 20000
RNG = random.Random(20261019)


def U(a, b):
    return RNG.uniform(a, b)


def pct(xs, p):
    s = sorted(xs)
    k = (len(s) - 1) * p
    lo, hi = int(math.floor(k)), int(math.ceil(k))
    return s[lo] + (s[hi] - s[lo]) * (k - lo)


def p3(xs):
    return pct(xs, 0.10), pct(xs, 0.50), pct(xs, 0.90)


def fmt3(xs, nd=0):
    a, b, c = p3(xs)
    f = f"{{:,.{nd}f}}"
    return f"{f.format(b)} ({f.format(a)}-{f.format(c)})"


def share_ge(xs, thr):
    return sum(1 for x in xs if x >= thr) / len(xs)


KCAL_PER_MWH = 859845.0  # 1 MWh = 0.8598 Gcal
GCAL_PER_MWH = 0.8598

out = []


def P(*a):
    s = " ".join(str(x) for x in a)
    out.append(s)
    print(s)


# =====================================================================================================
P("=" * 100)
P("0. WHICH ARCHETYPE CAN REACH 2x AT ALL (ceiling = 1/(1 - share the pieces can touch))")
P("=" * 100)
# Shares from TASK.md 'Where the money goes today'
arche = {
    "A gold placer": dict(touch=0.52, note="earthmoving ~2/3 of physical (78%) = 52%; MET/other 22% untouched"),
    "B Cu (Baimskaya)": dict(touch=0.41 * 0.06, note="P8 foundations <= ~6% of the 41% capital share"),
    "C1 export coal": dict(touch=0.41, note="pieces touch mining only (all non-outbound physical 41%); rail 55% untouched"),
    "C2 settlement coal": dict(touch=0.985, note="everything but 'other' 1.5% (outbound logistics 85%)"),
    "D lithium": dict(touch=0.0, note="no piece touches it"),
    "E oil (0.2 Mt/yr)": dict(touch=0.47, note="fiscal 53% untouched"),
}
for k, v in arche.items():
    c = econ.ceiling_ratio(v["touch"]) if v["touch"] < 1 else float('inf')
    P(f"  {k:22s} max ratio if every touched cost went to ZERO: {c:6.2f}x   ({v['note']})")
P("  -> only settlement coal (C2) has room for 'several times'; gold cannot pass ~2.1x even with free earthmoving,")
P("     oil cannot pass 1.89x even with free everything physical. Chains 1-3 are settlement-heat chains; chain 4 (gold)")
P("     is computed only to show it fails.")

# =====================================================================================================
P()
P("=" * 100)
P("1. SITE: a Yana-type Arctic river (Verkhoyansk normals), village cluster + coal seam in a 20-30 m bluff <=300 km")
P("=" * 100)
VK = data.monthly('Verkhoyansk')
daily = climate.daily_temperatures(VK)
FDD, TDD = climate.degree_days(VK)
warm8 = climate.days_above(VK, 8.0)
# heating load ~ (20 - T) on days with mean < +8 C (Russian heating-season rule)
load = [(20.0 - t) if t < 8.0 else 0.0 for t in daily]
tot_load = sum(load)
# day index 0 = 1 Jan. Bunker barge leaves after break-up (~1 Jun = day 151), next bunker arrives ~20 Sep (day 262)
DAY_OUT, DAY_IN = 151, 262
shore_share = sum(load[DAY_OUT:DAY_IN]) / tot_load
freeze_day = next(i for i in range(200, 365) if daily[i] < 0.0)
P(f"  Verkhoyansk FDD {FDD:,.0f} C*d, days with mean > 8 C: {warm8} (kit: 90)")
P(f"  Heat load while the bunker barge is away (1 Jun-20 Sep, {DAY_IN - DAY_OUT} d): {shore_share:.1%} of the year"
  f" -> comes from a small SHORE stock burned in the existing shore boiler-house (fixes P7 MAJOR 1)")
P(f"  First day with daily mean < 0 C: day {freeze_day} (~{freeze_day - 243 + 1} Sep)")
h_ice_lo, h_ice_hi = ice.ice_thickness(FDD, 0.017), ice.ice_thickness(FDD, 0.024)
P(f"  End-of-winter ice at the berth: {h_ice_lo:.2f}-{h_ice_hi:.2f} m (alpha 0.017-0.024)")

# ---- P7 hull: 100 x 22 m, 2,000 t, Cb 0.88, lightship 22%
L, B, CB, LF_LIGHT = 100.0, 22.0, 0.88, 0.22
T_full = naval.draught_from_payload(2000, L, B, CB, LF_LIGHT)
P(f"  P7 hull 100x22 m, 2,000 t payload: draught {T_full:.2f} m (P7: 1.26 m)")


def payload_at_depth(depth, ukc):
    T = depth - ukc
    return min(2000.0, T * L * B * CB / (1 + LF_LIGHT))


for dep in (1.5, 1.75, 2.0):
    P(f"    low-water depth {dep:.2f} m, under-keel 0.3-0.4 m -> payload {payload_at_depth(dep, 0.4):,.0f}-"
      f"{payload_at_depth(dep, 0.3):,.0f} t (kit: Yana/Indigirka low water 1.5-2.0 m)")
P(f"  Wintering berth depth needed (loaded at freeze-up, ice {h_ice_hi:.2f} m): "
  f"{naval.depth_needed(T_full, h_ice_hi):.2f} m at late-winter low water (backwater must be >= this)")
awp = L * B * 0.95
rise = naval.rise_per_tonne(awp) * 2000
P(f"  Hull rise as 2,000 t is drawn from the hold over winter: {rise:.2f} m -> hull must not stay bonded to the ice:"
  f" a slot is cut round it (standard 'obkolka' in winter harbours) or kept open by heat (chain 2)")

# =====================================================================================================
P()
P("=" * 100)
P("2. CURRENT PRACTICE for the target village type (archetype C2): 23,000 RUB/t at the boiler")
P("=" * 100)
NOW_T = data.get('price.settlement_coal_at_boiler')  # 23,000 RUB/t [L], logistics 85%
now_links = [
    ("mine at a distant pit (Dzhebariki-Khaya/Zyryanka), physical", 0.135 * NOW_T, "ledger C2 shares 13.5%"),
    ("mine 'other' (MET, overheads)", 0.015 * NOW_T, "ledger C2 'other' 1.5%"),
    ("long river / river-sea haul", 8000.0, "LORP seasonal haul 8,000 RUB/t [L]"),
    ("transshipment + storage at river depot", 1500.0, "est. (split of the 85% logistics share)"),
    ("winter-road last mile ~450 km x 20 RUB/t-km", 9000.0, "winter road 20 RUB/t-km [L] (distance est.)"),
    ("village depot handling + stockpile losses", NOW_T * 0.85 - 8000 - 1500 - 9000, "remainder of 85% logistics"),
]
s = sum(v for _, v, _ in now_links)
for n_, v, src in now_links:
    P(f"  {n_:55s} {v:8,.0f} RUB/t  [{src}]")
P(f"  {'TOTAL':55s} {s:8,.0f} RUB/t")
P("  Coal: long-flame (D) hard coal, LHV 5,100-5,400 kcal/kg (Kuznetsk D example; Dzhebariki-Khaya is D grade) -> "
  f"{NOW_T / 5.25:,.0f} RUB/Gcal of fuel at 5.25 Gcal/t")
P("  Note: river-bank villages served directly by barge pay far less: 7,100-11,600 RUB/t (P5), 8,080 (P7), Kolyma depot"
  f" tender {data.get('price.kolyma_depot_coal'):,.0f} RUB/t (kit). The chain only targets winter-road-last-mile villages.")

# =====================================================================================================
# CHAIN 1: P5 bluff auger -> direct discharge into P7 shallow hulls -> shuttle in the low-water window ->
#          last cargo of the season winters as the bunker of the SHORE boiler-house (P7 anchor, repaired)
# =====================================================================================================


def sample_coal_chain(mining="P5", rng_end="bunker_mix"):
    """One Monte Carlo draw of the local-coal supply chain. Returns dict of per-tonne link costs and context."""
    r = U(0.10, 0.15)
    o = {}
    o['r'] = r
    other = 0.015 * NOW_T  # MET/overheads kept (untouched share)
    o['other'] = other
    # ---------------- mining
    if mining == "P5":
        rate100 = U(21.0, 38.0)      # t/h at 100% availability and 62% geometric recovery (P5 review MAJOR 2)
        rec = U(0.30, 0.50)          # field recovery (P5 review MAJOR 4)
        f = 0.62 / rec               # holes per tonne x1.24-2.07
        days = U(60.0, 90.0)         # effective low-water campaign: extended-travel frame, collars above campaign
                                     # low water, rain-flood downtime (fix for P5 review MAJOR 3) - est.
        Q = econ.season_capacity(rate100 / f, days, 24.0, 0.75)
        F = 61e6 + U(3e6, 6e6) + U(4e6, 8e6)   # P5 fixed (review) + frame extension + bluff monitoring/remote op (est.)
        v = 1030.0 * f                          # P5 variable (review) scaled by holes per tonne
        o.update(rate100=rate100, rec=rec, days=days, Q=Q, F=F)
        o['mine'] = F / Q + v
        o['load'] = 0.0                         # auger discharges straight into the hull (coupling)
        o['LHV'] = U(3.5, 5.0)                  # Gcal/t, seam rank unknown (B3 brown to D) - est.
        o['eta_rel'] = U(0.95, 1.0)
        o['loss_shore'] = U(0.03, 0.08)
    elif mining == "PIT":
        o['mine'] = U(2800.0, 3700.0)           # bank pit under a 20-30 m bluff (P5, reproduced by review)
        o['load'] = U(150.0, 300.0)             # loader/conveyor to barge (est.)
        o['LHV'] = U(3.5, 5.0)
        o['eta_rel'] = U(0.95, 1.0)
        o['loss_shore'] = U(0.03, 0.08)
        o['Q'] = None
    elif mining == "P4":
        claimed = U(2700.0, 4300.0)             # P4 claimed delivered RUB/t at 4 bends x 10 kt
        other_p4 = U(1200.0, 2000.0)            # haul+screen+handling inside the claim (est.)
        D_season = (claimed - other_p4) * 40000.0
        window = U(45.0, 61.0)                  # June-July window (P4 review MAJOR 3)
        Q = econ.season_capacity(13.3, window, 24.0, 0.75)   # 13.3 t/h at 150 kW (P4 review MAJOR 1)
        o.update(Q=Q, D_season=D_season)
        o['mine'] = D_season / Q
        o['load'] = 0.0                         # dredge pumps into the hopper hull (coupling)
        o['LHV'] = U(2.64, 3.40)                # 37-49% moisture (P4 review MAJOR 2)
        o['eta_rel'] = U(0.90, 0.97)            # very wet fuel in a stoker boiler (est.)
        o['loss_shore'] = U(0.05, 0.12)         # wet brown coal, self-heating risk (est.)
    elif mining == "PIT_B":                     # bank pit for P4's seam: dry-mined at bed moisture
        o['mine'] = U(2800.0, 3700.0)
        o['load'] = U(150.0, 300.0)
        o['LHV'] = None                         # set by caller
        o['eta_rel'] = U(0.93, 1.0)
        o['loss_shore'] = U(0.04, 0.10)
    # ---------------- haul (P7 hull, conventional shuttle mode in summer)
    depth = U(1.5, 2.0)
    ukc = U(0.3, 0.4)
    pay = payload_at_depth(depth, ukc)
    km = U(150.0, 300.0)
    rate_tkm = U(3.0, 5.0)                       # LORP 3-5 RUB/t-km [L]
    term = U(200.0, 400.0)                       # terminal / waiting under the miner (est.)
    o['payload'] = pay
    o['haul'] = econ.freight_cost(rate_tkm, km) * (2000.0 / pay) + term
    o['km'] = km
    # shuttle cycle: hulls needed so the miner never waits (coupling: miner output <-> hull count)
    Qs = o['Q'] if o.get('Q') else 25000.0
    days_c = o.get('days', 75.0) if mining != "P4" else 53.0
    fill_d = pay / (Qs / days_c)
    trip_d = 2 * km / (U(8.0, 10.0) * 24.0) + U(1.0, 2.0)          # push-tow 8-10 km/h + unloading (est.)
    n_hulls = 1 + math.ceil(trip_d / fill_d) + 1                     # working + spare
    o['fill_d'], o['trip_d'], o['n_hulls'] = fill_d, trip_d, n_hulls
    s_b = min(1.0, n_hulls * pay / Qs) * (1 - shore_share)          # each hull's LAST cargo winters as a bunker
    o['s_b'] = s_b
    # ---------------- village end
    value = o['mine'] + o['load'] + other + o['haul']
    reclaim = U(200.0, 400.0)                    # excavator with ripper from hold (est.)
    slot = U(0.3, 0.6) * U(1.2e6, 1.8e6) / pay if rng_end != "bunker_chp" else 0.0  # stokers cut the slot (est.);
                                                 # in chain 2 the CHP reject heat keeps the moat open instead
    monitor = U(0.3e6, 0.6e6) / pay              # CO/temperature probes, hatch covers (est.)
    berth = econ.annualised_capex(U(1e6, 3e6), r, 15, 0.03) / pay   # deadmen/piles in a backwater (est.)
    insure = U(0.5e6, 1.5e6) / pay               # break-up / ice risk on an (almost empty) hull (est.)
    bunker_t = reclaim + slot + monitor + berth + insure + 0.01 * value
    shore_t = U(300.0, 600.0) + o['loss_shore'] * value
    o['bunker_t'] = bunker_t
    o['shore_t'] = shore_t
    hull_cap = econ.annualised_capex(U(15e6, 50e6), r, 15, 0.03) / pay   # used hull, ONE cargo a year (P7 as designed)
    o['hull_cap_t'] = hull_cap
    if rng_end == "bunker_mix":
        o['end'] = s_b * bunker_t + (1 - s_b) * shore_t
    elif rng_end == "p7_as_designed":
        o['end'] = (1 - shore_share) * (bunker_t + hull_cap) + shore_share * shore_t
    elif rng_end in ("bunker_all", "bunker_chp"):
        o['end'] = bunker_t
    else:
        o['end'] = shore_t
    o['total_t'] = o['mine'] + o['load'] + other + o['haul'] + o['end']
    return o


def now_per_gcal():
    return NOW_T / U(5.1, 5.4)


def pit_alt_per_t(o, a):
    """Best competent alternative per tonne: bank pit at the same bluff + loader + the same hulls and haul +
    everything through a shore pile (current-practice village handling)."""
    base = a['mine'] + a['load'] + a['other'] + o['haul']
    return base + U(300.0, 600.0) + o['loss_shore'] * base


KEYS1 = ("now", "ch", "bca", "r_now", "r_bca", "r_bca_now", "mine", "mine_t", "haul", "end", "Q", "LHV", "tot_t",
         "bca_t", "end_b", "end_s", "pay", "n_hulls", "s_b", "fill_d", "trip_d", "hull_cap", "bca_mine")


def run_chain1(end_mode="bunker_mix"):
    R = {k: [] for k in KEYS1}
    for _ in range(N):
        o = sample_coal_chain("P5", end_mode)
        a = sample_coal_chain("PIT", "shore")
        a_t = pit_alt_per_t(o, a)
        g = o['LHV'] * o['eta_rel']          # same seam, same boiler for chain and alternative
        ch = o['total_t'] / g
        bca = a_t / g
        nw = now_per_gcal()
        R['now'].append(nw); R['ch'].append(ch); R['bca'].append(bca)
        R['r_now'].append(nw / ch); R['r_bca'].append(bca / ch); R['r_bca_now'].append(nw / bca)
        R['mine'].append((o['mine'] + o['other']) / g); R['mine_t'].append(o['mine'] + o['other'])
        R['haul'].append(o['haul'] / g); R['end'].append(o['end'] / g)
        R['Q'].append(o['Q']); R['LHV'].append(o['LHV'])
        R['tot_t'].append(o['total_t']); R['bca_t'].append(a_t)
        R['end_b'].append(o['bunker_t']); R['end_s'].append(o['shore_t']); R['pay'].append(o['payload'])
        R['n_hulls'].append(o['n_hulls']); R['s_b'].append(o['s_b']); R['fill_d'].append(o['fill_d'])
        R['trip_d'].append(o['trip_d']); R['hull_cap'].append(o['hull_cap_t'])
        R['bca_mine'].append((a['mine'] + a['load'] + a['other']) / g)
    return R


P()
P("=" * 100)
P("3. CHAIN 1: P5 bluff auger -> P7 shallow hulls (direct discharge, low-water shuttle) -> each hull's last cargo")
P("   winters as a bunker of the SHORE boiler-house (P7 anchor, repaired) | product: fuel heat into the boiler, RUB/Gcal")
P("=" * 100)
R1 = run_chain1("bunker_mix")
P(f"  P5 season output Q = {fmt3(R1['Q'])} t/yr  (review: 38-68 kt at 100 d/75%; here 60-90 effective d and"
  " field recovery 30-50%)")
q50 = p3(R1['Q'])[1]
P(f"  market: {econ.market_share(q50, 205e3):.0%} of Arctic Yakutia utility coal (205 kt) at P50 = {q50 / 3:,.0f} people"
  " at 3 t/person within 300 km of one bluff (P5 review MAJOR 1)")
P(f"  P5 mining cost incl. MET/other: {fmt3(R1['mine_t'])} RUB/t  vs bank pit under the same 20-30 m bluff"
  " 2,800-3,700 (+150-300 loading)")
P(f"  shuttle: one hull filled every {fmt3(R1['fill_d'], 1)} d, round trip {fmt3(R1['trip_d'], 1)} d ->"
  f" {fmt3(R1['n_hulls'])} hulls; bunker share of the coal {fmt3(R1['s_b'], 2)} (one bunker cargo per hull)")
P(f"  per tonne delivered: chain {fmt3(R1['tot_t'])} RUB/t ; best competent alternative {fmt3(R1['bca_t'])} RUB/t ;"
  f" now {NOW_T:,.0f}")
P(f"  village end per tonne: bunker {fmt3(R1['end_b'])} vs shore pile {fmt3(R1['end_s'])} RUB/t"
  f" -> the P7 bunker is NOT cheaper than a shore pile (it saves one handling and 2-7% losses but adds reclaim,"
  " slot cutting, berth, monitoring, insurance)")
P()
P("  LINK TABLE (RUB per Gcal of fuel heat delivered into the village boiler; P50 with P10-P90)")
P(f"  {'link':28s} | {'method now':38s} | {'now':>6s} | {'method with chain':42s} | {'chain':>20s} | source")
nowG = p3(R1['now'])[1]
rows_now = [v / 5.25 for _, v, _ in now_links]
P(f"  {'1 mining':28s} | {'distant pit, D coal (incl. MET 1.5%)':38s} | {rows_now[0] + rows_now[1]:6,.0f} | "
  f"{'P5 floating bluff auger, repaired':42s} | {fmt3(R1['mine']):>20s} | P5 + review")
P(f"  {'2 loading':28s} | {'(inside haul)':38s} | {0:6,.0f} | {'auger discharges into the hull (coupling)':42s} |"
  f" {'0':>20s} | P5, P7")
P(f"  {'3 haul':28s} | {'2,000+ km river, depot, 450 km zimnik':38s} | {rows_now[2] + rows_now[3] + rows_now[4]:6,.0f} |"
  f" {'P7 1.26 m hulls, 150-300 km, low water':42s} | {fmt3(R1['haul']):>20s} | P7; LORP 3-5 RUB/t-km")
P(f"  {'4 village storage/handling':28s} | {'depot pile, reload, losses':38s} | {rows_now[5]:6,.0f} | "
  f"{'P7 bunker (last cargoes) + shore pile':42s} | {fmt3(R1['end']):>20s} | P7 + est.")
P(f"  {'TOTAL':28s} | {'':38s} | {nowG:6,.0f} | {'':42s} | {fmt3(R1['ch']):>20s} |")
P(f"  CHAIN RATIO vs current practice:          {fmt3(R1['r_now'], 2)}   P(>=2x) {share_ge(R1['r_now'], 2):.0%}"
  f"  P(>=3x) {share_ge(R1['r_now'], 3):.0%}")
P(f"  CHAIN RATIO vs best competent alternative: {fmt3(R1['r_bca'], 2)}   (bank pit at the same bluff, same hulls,"
  " shore pile)")
P(f"  that alternative alone vs current practice: {fmt3(R1['r_bca_now'], 2)}  <- the gain is 'mine locally', not the pieces")
P(f"  ceiling (MET/other 1.5% untouched): {econ.ceiling_ratio(0.985):.0f}x - not binding")
R1d = run_chain1("p7_as_designed")
P(f"  best-competent-alternative links, RUB/Gcal (P50): mining+loading {p3(R1['bca_mine'])[1]:,.0f} | haul"
  f" {p3(R1['haul'])[1]:,.0f} | shore pile {p3([e / (l * 0.975) for e, l in zip(R1['end_s'], R1['LHV'])])[1]:,.0f} |"
  f" total {p3(R1['bca'])[1]:,.0f}  -> weakest link of the chain = P5 mining ({p3(R1['mine'])[1]:,.0f} vs"
  f" {p3(R1['bca_mine'])[1]:,.0f})")
P(f"  P7 as designed (one dedicated used hull per 2,000 t, one cargo a year, hull 15-50 M RUB): hull charge"
  f" {fmt3(R1d['hull_cap'])} RUB/t, chain ratio vs now {fmt3(R1d['r_now'], 2)}  (P7 review MAJOR 3 confirmed)")

# ------- couplings for chain 1
P()
P("  COUPLINGS (computed):")
pay50 = p3(R1['pay'])[1]
nh50 = p3(R1['n_hulls'])[1]
fd50 = p3(R1['fill_d'])[1]
CAMPAIGN_END = 255   # ~12 Sep: last loading; low-water campaign mid-Jun/Jul to mid-Sep (est.)
first_bunker_load = CAMPAIGN_END - nh50 * fd50
P(f"   a) timing + vessel: the floating auger reaches the seam only in the low-water window, which is exactly when"
  f" only <=1.3 m hulls can run the Yana/Indigirka; payload {payload_at_depth(1.5, 0.4):,.0f}-2,000 t at 1.5-2.0 m;"
  f" P50 output {q50:,.0f} t = {q50 / pay50:.1f} hull-loads, one every {fd50:.1f} d -> {nh50:.0f} hulls and one tug keep"
  f" the auger loading with no shore stockpile, loader or transshipment at the mine")
P(f"   b) freeze-up vs self-heating: bunker cargoes are the last {nh50:.0f} loads (from day {first_bunker_load:.0f} to"
  f" {CAMPAIGN_END}); air means drop below 0 C on day {freeze_day}: {freeze_day - CAMPAIGN_END}-"
  f"{freeze_day - first_bunker_load:.0f} warm days in a covered hold for coal that leaves the seam FROZEN (onset >=14 d"
  f" for open brown-coal piles) -> CO/temperature probes, hatch covers, bunker burned FIRST (Oct-Jan) so the hull is"
  f" light long before break-up")
P(f"   c) ice: hull rises {rise:.2f} m as the hold is emptied; the boiler-house stokers cut a slot (0.3-0.6 FTE);"
  f" berth needs >= {naval.depth_needed(T_full, h_ice_hi):.2f} m at late-winter low water")
P(f"   d) hull capital: shuttle hulls winter loaded at villages instead of empty in a winter harbour -> no extra hull;"
  f" the price is that only {p3(R1['s_b'])[1]:.0%} of the coal can be bunkered")

# ------- sensitivity / decisive unknown for chain 1
P()
P("  SENSITIVITY (tornado: one input at a range end, others at mid) - chain-1 ratio vs current practice")


def chain1_det(rate100=29.5, rec=0.40, days=75.0, LHV=4.25, km=225.0, rate_tkm=4.0, now_t=NOW_T, eta=0.975,
               depth=1.75, extra_F=10.5e6, lhv_now=5.25, mining_cost=None, n_hulls=3):
    f = 0.62 / rec
    Q = econ.season_capacity(rate100 / f, days, 24.0, 0.75)
    mine = (61e6 + extra_F) / Q + 1030.0 * f if mining_cost is None else mining_cost
    other = 0.015 * NOW_T
    pay = payload_at_depth(depth, 0.35)
    haul = econ.freight_cost(rate_tkm, km) * 2000.0 / pay + 300.0
    value = mine + other + haul
    bunker = 300 + 0.45 * 1.5e6 / pay + 0.45e6 / pay + econ.annualised_capex(2e6, 0.125, 15, 0.03) / pay + 1e6 / pay \
        + 0.01 * value
    shore = 450 + 0.055 * value
    s_b = min(1.0, n_hulls * pay / Q) * (1 - shore_share)
    end = s_b * bunker + (1 - s_b) * shore
    tot = mine + other + haul + end
    return (now_t / lhv_now) / (tot / (LHV * eta)), Q, mine, tot


base = chain1_det()[0]
tor = [
    ("field recovery 0.30 / 0.50", chain1_det(rec=0.30)[0], chain1_det(rec=0.50)[0]),
    ("effective campaign 60 / 90 d", chain1_det(days=60)[0], chain1_det(days=90)[0]),
    ("cycle rate 21 / 38 t/h", chain1_det(rate100=21)[0], chain1_det(rate100=38)[0]),
    ("local coal LHV 3.5 / 5.0 Gcal/t", chain1_det(LHV=3.5)[0], chain1_det(LHV=5.0)[0]),
    ("haul 300 / 150 km", chain1_det(km=300)[0], chain1_det(km=150)[0]),
    ("barge rate 5 / 3 RUB/t-km", chain1_det(rate_tkm=5)[0], chain1_det(rate_tkm=3)[0]),
    ("low-water depth 1.5 / 2.0 m", chain1_det(depth=1.5)[0], chain1_det(depth=2.0)[0]),
    ("today's price 17,000 / 25,000 RUB/t", chain1_det(now_t=17000)[0], chain1_det(now_t=25000)[0]),
]
P(f"   mid-point ratio {base:.2f}x")
for n_, lo, hi in sorted(tor, key=lambda x: -(abs(x[2] - x[1]))):
    P(f"   {n_:38s} {lo:5.2f}x .. {hi:5.2f}x  (swing {abs(hi - lo):.2f})")


def solve(fun, lo, hi, target=2.0, it=80):
    flo = fun(lo) - target
    for _ in range(it):
        mid = 0.5 * (lo + hi)
        fm = fun(mid) - target
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return 0.5 * (lo + hi)


def ratio_at_Q(Q, LHV=4.25, rec=0.40):
    mine = (61e6 + 10.5e6) / Q + 1030.0 * 0.62 / rec
    return chain1_det(mining_cost=mine, LHV=LHV, rec=rec, days=75.0 * Q / chain1_det(rec=rec)[1])[0]


Q_thr = solve(lambda q: ratio_at_Q(q), 3000.0, 60000.0)
P(f"   THRESHOLD (decisive unknown): chain < 2x when one rig delivers < {Q_thr:,.0f} t/yr (field recovery x effective"
  f" days x cycle rate; P50 {q50:,.0f}; other inputs mid)")
P(f"   3x needs >= {solve(lambda q: ratio_at_Q(q), 3000.0, 5e6, target=3.0):,.0f} t/yr per rig at LHV 4.25 Gcal/t, or"
  f" {solve(lambda q: ratio_at_Q(q, 5.0), 3000.0, 5e6, target=3.0):,.0f} t/yr at LHV 5.0 (review cap 38-68 kt at"
  f" 100 d and 62% recovery)")
LHV_thr = solve(lambda x: chain1_det(LHV=x)[0], 2.0, 6.0)
P(f"   THRESHOLD: chain < 2x when the seam's LHV < {LHV_thr:.2f} Gcal/t (other inputs mid)")
now_thr = solve(lambda x: chain1_det(now_t=x)[0], 5000.0, 40000.0)
P(f"   THRESHOLD: chain < 2x where today's delivered price is below {now_thr:,.0f} RUB/t at the boiler"
  f" (river-bank villages at 7,100-11,600 RUB/t: {chain1_det(now_t=7100)[0]:.2f}-{chain1_det(now_t=11600)[0]:.2f}x)")
for cv in (0.4, 0.6):
    n_h = stats.sample_size_mean(cv, 0.10)
    P(f"   pilot to measure the decisive unknown: per-hole tonnage CV {cv} -> {n_h:.0f} holes for +/-10% (95%) ="
      f" {n_h * 5.0 / 24:.0f}-{n_h * 9.1 / 24:.0f} rig-days at 5.0-9.1 h/hole: one season answers it")
pit_mid = 3250.0 + 225.0
Q_par = solve(lambda q: pit_mid - ((61e6 + 10.5e6) / q + 1030 * 0.62 / 0.40) + 2.0, 3000.0, 5e6)
P(f"   P5 matches the bank pit (3,475 RUB/t incl. loading) only above {Q_par:,.0f} t/yr per rig at 40% recovery")
# pit cost vs bluff height, linear through P5's own 20 m -> 2,800 and 30 m -> 3,700 (est. extrapolation)
p5_mid = p3(R1['mine_t'])[1] - 0.015 * NOW_T
H_cross = 20 + (p5_mid - 225 - 2800) / 90.0
P(f"   P5 (P50 {p5_mid:,.0f} RUB/t) beats a bank pit only under bluffs higher than ~{H_cross:.0f} m (pit cost linear in"
  " height through P5's 20 m/2,800 and 30 m/3,700 - est.), where bluff-collapse risk is worst (P5 MAJOR 5)")

# =====================================================================================================
P()
P("=" * 100)
P("4. CHAIN 2: chain-1 coal; the shuttle hulls winter loaded round a P6 1-MWe ORC CHP barge in a protected backwater")
P("   (district centre).  Product: the winter (194 d) energy bundle = heat into the network + electricity at busbar")
P("=" * 100)
WIN_H = 194 * 24.0


def run_chain2():
    R = {k: [] for k in ("r_now", "r_bca", "r_now_nostandby", "now", "ch", "bca", "E", "coal_t", "hulls", "extra",
                         "ash_ok", "capex", "links_now", "links_ch", "elec_cost", "heat_now_share", "Qok")}
    for _ in range(N):
        o = sample_coal_chain("P5", "bunker_chp")
        a = sample_coal_chain("PIT", "shore")
        r = o['r']
        lf = U(0.8, 1.0)
        E = 1.0 * lf * WIN_H                         # MWh_e, heat-led winter running
        fuel = E / (0.80 * 0.16)                     # MWh fuel (P6: thermal-oil boiler 80%, ORC 16% net)
        loss_kw = U(148.0, 250.0)                    # moat + hold (P6: 104 + 44 kW at 0.3 MWe) - larger hull, est.
        heat = fuel * 0.80 * (1 - 0.16) - loss_kw / 1000.0 * WIN_H * lf
        # NOW: same heat from the shore boiler-house (65%) on imported coal + diesel electricity
        lhv_now = U(5.1, 5.4)
        c_heat_now = heat / 0.65 * GCAL_PER_MWH / lhv_now * NOW_T
        fuel_av = U(18.0, 55.0)                      # avoided diesel fuel RUB/kWh (P6 review MAJOR 1)
        varom = U(1.0, 3.0)                          # avoided variable O&M (est.)
        nonfuel = U(15.0, 30.0)                      # diesel plant kept for summer/standby: same in both (est.)
        c_el_now = E * 1000 * (fuel_av + varom)
        c_standby = E * 1000 * nonfuel
        now = c_heat_now + c_el_now + c_standby
        # CHAIN: local coal in the shuttle hulls (bunker) burned in the CHP barge
        g = o['LHV'] * o['eta_rel']
        coal_t = fuel * GCAL_PER_MWH / g
        need = math.ceil(coal_t / o['payload'])
        extra = max(0, need - o['n_hulls'])          # hulls beyond the shuttle fleet: one cargo a year each
        c_extra = extra * econ.annualised_capex(U(15e6, 50e6), r, 15, 0.03)
        c_coal = coal_t * o['total_t'] + c_extra
        capex = econ.six_tenths_scaling(U(132e6, 237e6), 0.3, 1.0, U(0.6, 0.7))
        c_cap = econ.annualised_capex(capex, r, 15, 0.03)
        staff = 13.5e6                               # P6 review MAJOR 5 (9 staff x 1.5 M RUB/yr)
        ch = c_coal + c_cap + staff + c_standby
        # BEST COMPETENT ALTERNATIVE: pit coal through a shore pile, (i) shore ORC CHP at the boiler-house (no hull,
        # no moat/hold loss, same staff) or (ii) pit coal in the old boiler + diesel as today; take the cheaper
        a_t = pit_alt_per_t(o, a)
        heat_b = fuel * 0.80 * (1 - 0.16)
        fuel_b = fuel * heat / heat_b
        bca_chp = fuel_b * GCAL_PER_MWH / g * a_t + econ.annualised_capex(capex * U(0.85, 1.05), r, 15, 0.03) \
            + staff + c_standby + E * 1000 * 0.0
        bca_old = heat / 0.65 * GCAL_PER_MWH / g * a_t + c_el_now + c_standby
        bca = min(bca_chp, bca_old)
        bundle = heat + E
        R['r_now'].append(now / ch); R['r_bca'].append(bca / ch)
        R['r_now_nostandby'].append((now - c_standby) / (ch - c_standby))
        R['now'].append(now / bundle); R['ch'].append(ch / bundle); R['bca'].append(bca / bundle)
        R['E'].append(E); R['coal_t'].append(coal_t); R['hulls'].append(coal_t / o['payload']); R['extra'].append(extra)
        R['ash_ok'].append((coal_t / U(0.85, 0.95)) / (coal_t * U(0.12, 0.20) / 0.7))
        R['capex'].append(capex)
        R['links_now'].append((c_heat_now / bundle, c_el_now / bundle, c_standby / bundle))
        R['links_ch'].append((c_coal / bundle, (c_cap + staff) / bundle, c_standby / bundle))
        R['elec_cost'].append((c_cap + staff) / (E * 1000))
        R['heat_now_share'].append(c_heat_now / now)
        R['Qok'].append(o['Q'] / coal_t)
    return R


R2 = run_chain2()
ln = [p3([x[i] for x in R2['links_now']])[1] for i in range(3)]
lc = [p3([x[i] for x in R2['links_ch']])[1] for i in range(3)]
P(f"  winter electricity {fmt3(R2['E'])} MWh; coal {fmt3(R2['coal_t'])} t = {fmt3(R2['hulls'], 1)} hull-loads"
  f" moored round the CHP (fixes P6 MAJOR 4); extra one-cargo hulls beyond the shuttle fleet: {fmt3(R2['extra'], 1)}")
P(f"  P5 output / CHP coal = {fmt3(R2['Qok'], 1)} (the rig also supplies the surrounding villages)")
P(f"  CHP capex at 1 MWe (P6 0.3 MWe 132-237 M RUB scaled ^0.6-0.7): {fmt3([c / 1e6 for c in R2['capex']])} M RUB")
P(f"  CHP electricity cost (capex + 3% O&M + staff; net extra fuel ~0, heat-led): {fmt3(R2['elec_cost'], 1)} RUB/kWh"
  " vs avoided diesel fuel 18-55 RUB/kWh")
P(f"  coupling (heat): the CHP's 148-250 kW of hull losses keep the moat and the bunker holds unfrozen, so no slot"
  f" cutting; coupling (waste stream): freed hold volume / ash volume = {fmt3(R2['ash_ok'], 1)} -> ash rides back in"
  " the hulls for the spring trip")
P()
P("  LINK TABLE (RUB per MWh of bundle = heat + electricity, P50)")
P(f"  1-4 coal to the heat plant   | now: imported coal, shore boiler 65% {ln[0]:7,.0f} | chain: P5 + P7 local coal in"
  f" bunker hulls {lc[0]:7,.0f} | P5, P7")
P(f"  5 electricity conversion     | now: diesel fuel + variable O&M      {ln[1]:7,.0f} | chain: P6 CHP barge capex"
  f" + staff   {lc[1]:7,.0f} | P6 + review")
P(f"  6 diesel plant kept standby  | now (untouched share, est.)         {ln[2]:7,.0f} | chain: same"
  f"                       {lc[2]:7,.0f} | est.")
P(f"  TOTAL                        | now {fmt3(R2['now'])} | chain {fmt3(R2['ch'])} | best alternative {fmt3(R2['bca'])}")
P(f"  CHAIN RATIO vs current practice: {fmt3(R2['r_now'], 2)}  P(>=2x) {share_ge(R2['r_now'], 2):.0%}"
  f"  P(>=3x) {share_ge(R2['r_now'], 3):.0%}   (without the standby share, an upper bound:"
  f" {fmt3(R2['r_now_nostandby'], 2)})")
P(f"  CHAIN RATIO vs best competent alternative (pit coal + shore ORC CHP, or pit coal + old boiler + diesel):"
  f" {fmt3(R2['r_bca'], 2)}")
P(f"  -> DROPPED (P50 < 2x): electricity at {p3(R2['elec_cost'])[1]:.0f} RUB/kWh vs 18-55 avoided is ~1x, and it"
  " dilutes the coal gain")

# =====================================================================================================
P()
P("=" * 100)
P("5. CHAIN 3: P4 channel-talik seam dredge -> pumped into P7 hopper hulls (water drains in the hold) -> bunker + shore")
P("=" * 100)


def run_chain3():
    R = dict(r_now=[], r_bca=[], ch=[], mine=[], Q=[], LHV=[])
    for _ in range(N):
        o = sample_coal_chain("P4", "bunker_mix")
        a = sample_coal_chain("PIT_B", "shore")
        g = o['LHV'] * o['eta_rel']
        ch = o['total_t'] / g
        lhv_pit = o['LHV'] * U(1.08, 1.25)          # dry-mined at bed moisture vs slurried + screened (est.)
        base = a['mine'] + a['load'] + a['other'] + o['haul']
        a_t = base + U(300.0, 600.0) + a['loss_shore'] * base
        bca = a_t / (lhv_pit * a['eta_rel'])
        nw = now_per_gcal()
        R['r_now'].append(nw / ch); R['r_bca'].append(bca / ch); R['ch'].append(ch)
        R['mine'].append(o['mine']); R['Q'].append(o['Q']); R['LHV'].append(o['LHV'])
    return R


R3 = run_chain3()
P(f"  dredge output per season {fmt3(R3['Q'])} t (13.3 t/h, 45-61 d) = 1-1.5 bends; dredge cost {fmt3(R3['mine'])} RUB/t"
  " (P4's own season cost, spread over 1 bend instead of 4)")
P(f"  chain {fmt3(R3['ch'])} RUB/Gcal; RATIO vs current {fmt3(R3['r_now'], 2)} (P>=2x {share_ge(R3['r_now'], 2):.0%});"
  f" vs bank pit {fmt3(R3['r_bca'], 2)}")
mr = hydro.fines_release_rate(13.3 / 1.25, 1.25, 0.25, 0.005)
mr5 = hydro.fines_release_rate(13.3 / 1.25, 1.25, 0.25, 0.05)
P(f"  turbidity: cutter (0.5% escape) needs {hydro.dilution_flow_required(mr):.0f} m3/s of full mixing, screen water"
  f" returned (5%) {hydro.dilution_flow_required(mr5):.0f} m3/s, vs +0.25 mg/L judged near the source -> settle in the"
  " hold (coupling with P7), not costed. Wet 37-49% coal freezes solid in a bunker hold.  -> DROPPED (P50 < 2x)")

# =====================================================================================================
P()
P("=" * 100)
P("6. CHAIN 4 (gold, deep thin placer): P2 jet undercut caving + P8 floating power/wash plant in P2's recycle pond,")
P("   power-house reject heat into the jet water.  Product: gold at the refinery, RUB/g")
P("=" * 100)
el_load = hydro.hydro_elevator_power(0.28, 20.0, 1300.0, 0.25) / 1e3 + hydro.pumping_power(0.25, 80.0, 0.75) / 1e3
rej = el_load * 1.35                                  # genset jacket + exhaust heat ~1.2-1.5 x electric (est.)
dT_add = rej * 1e3 / (0.25 * data.C_W_VOL)
P(f"  coupling: electric load (hydro-elevator 20 m lift + monitors 80 m head) ~{el_load:.0f} kW -> reject heat"
  f" ~{rej:.0f} kW vs 3,300 kW thaw demand: +{dT_add:.2f} K on 0.25 m3/s; heat delivered/needed at 4 C water"
  f" 1.27 -> {1.27 * (4 + dT_add) / 4:.2f}")


def run_chain4():
    R = dict(r_now=[], r_bca=[])
    for _ in range(N):
        touch = U(0.52, 0.65)          # earthmoving/mining share of delivered cost (ledger A ~52%; deep placers more)
        base = U(1100.0, 2650.0)       # cheaper of open-cut and drill-blast underground (P2)
        c = U(556.0, 965.0)            # RUB/m3 of pay (P2 sensitivity, review MAJOR 3)
        loss = U(0.07, 0.50)           # bedrock gold left behind (review MAJOR 6)
        p2 = 620.0 * c / 650.0 / (1 - loss)
        r2 = base / p2
        p8 = U(0.0, 0.07)              # P8 delivered-cost gain: 0% cold permafrost .. 7% niche (review)
        frac = 1 - touch * (1 - 1 / r2) - p8
        R['r_now'].append(1 / frac)
        R['r_bca'].append(1 / frac)    # direct competitor (borehole hydraulic mining) not costed: upper bound
    return R


R4 = run_chain4()
P(f"  RATIO vs current practice {fmt3(R4['r_now'], 2)}; P(>=2x) {share_ge(R4['r_now'], 2):.0%};"
  " vs borehole hydraulic mining (not costed) at most the same.  Ceiling with free earthmoving 2.08x -> DROPPED")
r1s = []
for _ in range(N):
    strip_share = U(0.21, 0.44)
    r1 = U(1.1, 2.5)                    # P1 stripping link after carry-forward (review MAJOR 2)
    p8 = U(0.0, 0.07)
    r1s.append(1 / (1 - strip_share * (1 - 1 / r1) - p8))
P(f"  (P1 thaw-face stripping + P8 instead: {fmt3(r1s, 2)}; vs hydraulic stripping ~1x -> DROPPED)")

# =====================================================================================================
P()
P("=" * 100)
P("7. SUMMARY")
P("=" * 100)
for name, R in (("Chain 1 P5+P7 heat", R1), ("Chain 2 P5+P7+P6 CHP", R2), ("Chain 3 P4+P7 heat", R3),
                ("Chain 4 P2+P8 gold", R4)):
    P(f"  {name:24s} vs now {fmt3(R['r_now'], 2):20s} vs best competent {fmt3(R['r_bca'], 2):20s}"
      f" P(now>=2x) {share_ge(R['r_now'], 2):4.0%} P(now>=3x) {share_ge(R['r_now'], 3):4.0%}")
P(f"  Local bank pit + shallow hulls + shore pile (no piece) vs now: {fmt3(R1['r_bca_now'], 2)}"
  f"  P(>=3x) {share_ge(R1['r_bca_now'], 3):.0%}")
m1 = q50 / Q_thr
P(f"  gate (econ.gate_verdict, margin = P50 rig output / 2x-threshold output = {m1:.2f}):"
  f" chain 1 {econ.gate_verdict(m1, p3(R1['r_now'])[1])} vs now,"
  f" {econ.gate_verdict(m1, p3(R1['r_bca'])[1])} vs the best competent alternative")

with open('/home/user/SomeRepository/engine/runs/permafrost/genius/compose/chains_out.txt', 'w') as fh:
    fh.write("\n".join(out) + "\n")
