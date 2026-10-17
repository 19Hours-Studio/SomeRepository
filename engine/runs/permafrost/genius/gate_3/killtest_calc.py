#!/usr/bin/env python3
"""Gate 3 kill test: KILLER margin and CHAIN ratio for the 8 permafrost ideas.

Every decisive input carries its source; '(est.)' marks screening assumptions
where no measured figure was found (web search budget ran out mid-task).
Ledger = value ledger in TASK.md.
"""
import math

RUB_USD = 84.0  # ledger
OZ_PER_T = 32150.7466

# ---------------- ledger archetypes (shares of delivered cost) ----------------
A = dict(cost=2550.0, energy=.10, labour=.20, inbound=.12, outbound=.002,
         processing=.20, capital=.15, other=.22)            # $/oz, placer
B = dict(cost=8500.0, energy=.11, labour=.11, inbound=.03, outbound=.05,
         processing=.15, capital=.41, other=.14)            # $/t Cu CIF China gross
CS = dict(cost=23000.0, energy=.03, labour=.04, inbound=.015, outbound=.85,
          processing=.03, capital=.02, other=.015)          # rub/t at boiler, settlement coal

def phys(x):
    return sum(v for k, v in x.items() if k not in ("cost", "other"))

def manning_Q(b, h, S, n):
    area = b * h
    R = area / (b + 2 * h)
    return (1.0 / n) * area * R ** (2.0 / 3.0) * S ** 0.5

def crf(i, n):
    return i / (1 - (1 + i) ** -n)

out = {}

# ============ shared LNG-carrier inputs (ideas 1 and 8) ============
DWT_ICE = 80200.0     # t at 11.8 m loaded draft (Rosmorport pilotage notice; ship-technology)
LNG_CARGO = 74000.0   # t typical Yamal LNG cargo (CHNL, Jan-May 2025 overview)
ARC7_VOY = 241        # Arc7 laden voyages from Sabetta, 2025 (CHNL AIS 2025 overview)
spare_voy = DWT_ICE - LNG_CARGO                 # before fuel, water, stores -> upper bound
spare_fleet = spare_voy * ARC7_VOY              # t/yr of laden-leg "free" tonnage

# ============ IDEA 1: whole-ore ballast swap (archetype B) ============
ORE_REQ = 70e6        # t/yr ore, Baimskaya design (ledger B)
CU_TPY = 300e3        # t Cu/yr first 10 yrs (KAZ Minerals BFS 2021)
m1 = spare_fleet / ORE_REQ
ore_per_cu = ORE_REQ / CU_TPY                   # t ore per t Cu
barge_usd_t = 3.0 * 1000.0 / RUB_USD            # ledger LORP low end 3 rub/t-km x 1,000 km (est.)
removed = B["processing"] + 0.7 * B["energy"] + 0.5 * B["capital"] + B["outbound"]
left = B["cost"] * (1 - removed)
barge = ore_per_cu * barge_usd_t
port_opex = 0.5 * (B["processing"] + 0.7 * B["energy"]) * B["cost"]   # warm-port mill at half Arctic cost (est.)
port_capex = 0.5 * B["capital"] * B["cost"] / 2.5                      # ledger: Far North builds 2-3x
handling = ore_per_cu * 2 * 2.0                                       # 2 extra handlings x $2/t (est.)
w1 = left + barge + port_opex + port_capex + handling
out[1] = dict(req=ORE_REQ, avail=spare_fleet, margin=m1, now=B["cost"], w=w1,
              ratio=B["cost"] / w1, extra=dict(ore_per_cu=ore_per_cu, barge=barge, left=left,
                                               port_opex=port_opex, port_capex=port_capex, handling=handling))

# ============ IDEA 2: robot-built self-dredging rivers (archetype C settlement) ============
Q_req2 = manning_Q(12.0, 1.0, 0.0005, 0.035)   # 0.8 m draft + 0.2 m keel, 12 m lane, lowland slope (est.)
RUNOFF_MM = 80.0      # wettest of 19 Central-Yakutia basins, mm/yr (EGU2018-16001); 1,270-8,290 km2 basins 1-15 mm/yr (EGU2020-1095)
AREA2 = 1000.0        # km2 at the upstream (deposit/settlement) end (est.)
Q_av2 = AREA2 * 1e6 * RUNOFF_MM / 1000.0 / (365.25 * 86400)
m2 = Q_av2 / Q_req2
logi = CS["outbound"] * CS["cost"]              # 19,550 rub/t
remainder = logi - 8000.0                        # minus LORP seasonal haul (ledger) = winter road + handling
wr_km = remainder / 20.0                         # ledger winter road 20 rub/t-km
idea_leg = wr_km * 4.0                           # ledger LORP 3-5 rub/t-km on the trained tributary
w2 = CS["cost"] - remainder + idea_leg           # robot works costed at zero -> upper bound
out[2] = dict(req=Q_req2, avail=Q_av2, margin=m2, now=CS["cost"], w=w2, ratio=CS["cost"] / w2,
              extra=dict(remainder=remainder, wr_km=wr_km, idea_leg=idea_leg))

# ============ IDEA 3: supply drones survey while flying (archetype A, exploration) ============
REQ_DENS = 1 / 0.100   # line-km/km2: 1:10,000 kimberlite aeromag survey = 100 m lines (journals.vsu.ru)
A_YAK = 3083523.0      # km2 (Gavrileva, ieie.su)
NODES = 3 * 586        # 586 rural settlements (Gavrileva, 2015), tripled for camps (est., generous)
spacing = math.sqrt(A_YAK / NODES)               # km between nodes ~ one corridor of this length per node
avail_dens = 1.0 / spacing
m3 = avail_dens / REQ_DENS
EXPL = 6.15e9          # $ gold exploration budget 2025 (S&P World Exploration Trends 2026)
GOLD_T = 3672.0        # t mine output 2025 (WGC Gold Demand Trends FY2025)
expl_oz = EXPL / (GOLD_T * OZ_PER_T)
w3 = A["cost"] - expl_oz                        # exploration made free
out[3] = dict(req=REQ_DENS, avail=avail_dens, margin=m3, now=A["cost"], w=w3, ratio=A["cost"] / w3,
              extra=dict(spacing_km=spacing, expl_per_oz=expl_oz))

# ============ IDEA 4: village coal-slurry wells (archetype C settlement) ============
REACH = 15 * 0.3048    # m effective jet reach in coal, USBM borehole-mining tool (8 t/h from 88 ft)
SEAM, RHO, REC = 3.0, 1.35, 0.8                 # m, t/m3, recovery inside reach (est.)
t_hole = math.pi * REACH ** 2 * SEAM * RHO * REC
HOLE_RUB = 1.0e6       # rub per 100-m cased 250-300 mm hole in permafrost (est.: casing ~0.55 M + rig/crew/consumables)
req_hole = HOLE_RUB / logi                       # t/hole for drilling to break even with the haulage it removes
m4 = t_hole / req_hole
DEMAND = 5000.0        # t/yr, ~1,500-person settlement boiler (est.)
labour4 = 2 * 2 * 5.0e6                          # 2 posts x 2 workers x 5 M rub (ledger FIFO)
energy4 = 75.0 * 41.0 * DEMAND                   # 75 kWh/t jet+airlift+milling (est.) x 41 rub/kWh (ledger)
drill4 = DEMAND / t_hole * HOLE_RUB
capex4 = 150e6 * crf(0.10, 10)                   # BHM pumps, compressor, CWF mill/thickener, burner retrofit (est.)
cons4 = 500.0 * DEMAND                           # plasticiser, spares (est.)
water_per_coal = 0.38 / 0.62                     # CWF 62 % coal
loss = water_per_coal * 2.5 + 10 * 4.186e-3 * 15 * 0.5   # GJ/t coal: evaporate CWF water + half-recovered jet heating
penalty4 = 1 / (1 - loss / 23.0)                 # 5,500 kcal/kg = 23 GJ/t (ledger coal spec)
w4 = (labour4 + energy4 + drill4 + capex4 + cons4) / DEMAND * penalty4
out[4] = dict(req=req_hole, avail=t_hole, margin=m4, now=CS["cost"], w=w4, ratio=CS["cost"] / w4,
              extra=dict(holes_per_yr=DEMAND / t_hole, labour=labour4 / DEMAND, energy=energy4 / DEMAND,
                         drill=drill4 / DEMAND, capex=capex4 / DEMAND, penalty=penalty4))

# ============ IDEA 5: pulse-sorting weir staircase (archetype A) ============
def mpm_ratio(S, D, n, h):
    theta = h * S / (1.65 * D)
    if theta <= 0.047:
        return float("inf")
    qs = 8 * (theta - 0.047) ** 1.5 * math.sqrt(1.65 * 9.81 * D ** 3)   # Meyer-Peter-Mueller bedload
    qw = (1 / n) * h ** (5.0 / 3.0) * S ** 0.5                          # wide-channel Manning
    return qw / qs
best_ratio, best_h = min((mpm_ratio(0.01, 0.03, 0.035, h / 100.0), h / 100.0) for h in range(5, 400))
# the water-optimal depth (~2.3 m) would need ~117 m3/s through a 10 m lane; use a realistic
# side-lane pulse of q = 1.5 m2/s (15 m3/s over 10 m, est.) -> depth from Manning, then MPM ratio
lane_h = (1.5 * 0.035 / 0.01 ** 0.5) ** 0.6
lane_ratio = mpm_ratio(0.01, 0.03, 0.035, lane_h)
water_per_bulk = lane_ratio * 0.65               # 35 % porosity
Q_CREEK = 100.0 * 10.0 / 1000.0                  # 100 km2 placer creek (est.) x 10 L/s/km2 (Chukotka low-water, Lomonosov Geogr. J. 2023)
N_WEIRS = 5                                      # water reused at each step (est.)
avail5 = Q_CREEK * 3600 / water_per_bulk * N_WEIRS
REQ5 = 100.0                                     # m3/h sands, one SB-100 washing plant (SB RAS, sibran.ru)
m5 = avail5 / REQ5
earth = 2.0 / 3.0 * phys(A)                      # ledger: earthmoving ~2/3 of physical cost
removed5 = 0.5 * A["processing"] + 0.10 * A["energy"] + 0.15 * A["capital"]   # washing plant, pumps, plant capital (est.)
w5 = A["cost"] * (1 - removed5)
out[5] = dict(req=REQ5, avail=avail5, margin=m5, now=A["cost"], w=w5, ratio=A["cost"] / w5,
              extra=dict(best_ratio_solid=best_ratio, best_h=best_h, lane_h=lane_h, lane_ratio=lane_ratio,
                         water_per_bulk=water_per_bulk,
                         earthmoving_share=earth, removed=removed5))

# ============ IDEA 6: relay flood-pulse ore barges (archetype B) ============
Q_IN6 = 1000.0 * 10.0 / 1000.0                   # 1,000 km2 tributary (est.) x 10 L/s/km2 (Chukotka, Lomonosov 2023)
Q_PULSE = manning_Q(40.0, 1.2, 0.001, 0.035)     # 1.2 m over a 40 m natural shoal (est.) for 1.0 m draft barges
DUR = 2 * 2000.0 / 1.0                           # s: twice the transit of a 2 km shoal at ~1 m/s (est.)
pulses_day = Q_IN6 * 86400 / (Q_PULSE * DUR)    # mean outflow = inflow
t_pulse = 4 * 500.0                              # 4 barges x 500 t (est.)
SEASON = 100.0                                   # open-water days (est.)
avail6 = pulses_day * t_pulse * SEASON
REQ6 = 1.4e6                                     # t/yr concentrate (ledger B)
m6 = avail6 / REQ6
road_usd = (44e3 - 28e3) / 3 * CU_TPY            # road = 1/3 of state road/port/NPP (ledger $16k/t-yr; split est.)
road_tcu = road_usd * crf(0.10, 30) / CU_TPY
truck_tcu = 0.5 * B["outbound"] * B["cost"]      # trucking ~ half of outbound (est.)
now6 = B["cost"] + road_tcu
w6 = now6 - road_tcu - truck_tcu                 # relay system costed at zero -> upper bound
out[6] = dict(req=REQ6, avail=avail6, margin=m6, now=now6, w=w6, ratio=now6 / w6,
              extra=dict(Q_pulse=Q_PULSE, pulses_day=pulses_day, road_tcu=road_tcu, truck_tcu=truck_tcu))

# ============ IDEA 7: highwall-mined frozen paystreaks (archetype A) ============
T, W, H, h, e = 18.0, 100.0, 10.0, 1.5, 0.6      # HW300 min bench 18 m (Coal Age); pay-streak 100 m (generous vs 11-12 m
                                                 # Yukon Marten Creek, YGS 2001-039); overburden/pay (est.); web-pillar extraction (est.)
open_cut = (H + h) / h
idea7 = (T * (H + h) + (W - T) * h * e) / (T * h + (W - T) * h * e)
factor = open_cut / idea7
m7 = factor / 8.0                                # idea claims 8-10x
hwm_oz = 25e6 * crf(0.12, 7) / (0.5 * OZ_PER_T)  # $25 M HW300 system (est.), 0.5 t/yr site (est.)
nonearth = phys(A) - earth
w7 = A["cost"] * (earth / factor + nonearth + A["other"]) + hwm_oz
out[7] = dict(req=8.0, avail=factor, margin=m7, now=A["cost"], w=w7, ratio=A["cost"] / w7,
              extra=dict(max_factor_infinite_width=open_cut, hwm_per_oz=hwm_oz))

# ============ IDEA 8: paid ore ballast on LNG carriers (archetype B) ============
m8 = spare_fleet / REQ6
w8 = B["cost"] * (1 - B["outbound"])             # all outbound logistics made free -> upper bound
out[8] = dict(req=REQ6, avail=spare_fleet, margin=m8, now=B["cost"], w=w8, ratio=B["cost"] / w8,
              extra=dict(spare_per_voyage=spare_voy))

def verdict(m, r):
    if m < 0.3 or r < 1.1:
        return "DEAD"
    if m >= 1 and r >= 1.5:
        return "ALIVE"
    return "WOUNDED"

for k in sorted(out):
    o = out[k]
    print(f"IDEA {k}: req={o['req']:.4g} avail={o['avail']:.4g} MARGIN={o['margin']:.3g} | "
          f"now={o['now']:.5g} with={o['w']:.5g} RATIO={o['ratio']:.3g} -> {verdict(o['margin'], o['ratio'])}")
    print("   ", {kk: round(vv, 4) for kk, vv in o["extra"].items()})
