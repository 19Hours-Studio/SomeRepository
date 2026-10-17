#!/usr/bin/env python3
"""Gate 8 kill test: KILLER (margin) and CHAIN (ratio) for 8 ideas.
Every decisive input carries a source tag; see SOURCES at the bottom.
Assumptions that are not sourced are marked ASSUMPTION and set in the idea's favour where possible.
"""
import math

g = 9.81
RHO_W = 1000.0
RUB_PER_USD = 84.0          # ledger
DAY = 86400.0

def verdict(m, r):
    if m < 0.3 or r < 1.1:
        return "DEAD"
    if m >= 1 and r >= 1.5:
        return "ALIVE"
    return "WOUNDED"

out = []
def p(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    out.append(s)

# ---------------------------------------------------------------------------
# Shared: measured under-ice depth-mean velocities, Lena delta, April 2019 [S1]
U_BYKOV = (0.20, 0.25)      # Bykovskaya channel (best measured)
U_MAIN = (0.12, 0.18)       # main channel near Samoilov
U_OLEN = (0.05, 0.11)       # Olenekskaya channel
U_TYP = sum(U_MAIN) / 2     # 0.15 m/s typical
U_BEST = U_BYKOV[1]         # 0.25 m/s best
MU_K = 0.05                 # kinetic friction, wet ice on coated steel/plastic; [S4] range 0.02-0.47 -> favourable pick
F_BUOY = 0.01               # ASSUMPTION: +1 % net buoyancy = "slightly buoyant" (minimum to float reliably)
Z0 = 0.01                   # ASSUMPTION: ice-underside roughness length (m) for log-law profile
H_ICE_LAYER = 5.0           # ASSUMPTION: ice-influenced half-depth (m) of a ~10 m deep channel

def loglaw_factor(h_pod):
    """mean velocity over a pod of height h_pod hugging the ice / depth-mean of ice-side layer"""
    return (math.log(h_pod / Z0) - 1) / (math.log(H_ICE_LAYER / Z0) - 1)

def slide_threshold(V, A, Cd, mu=MU_K, f=F_BUOY):
    """current speed relative to pod at which drag = mu * net buoyancy"""
    B = f * RHO_W * g * V
    return math.sqrt(2 * mu * B / (RHO_W * Cd * A))

# ===========================================================================
p("=" * 78)
p("IDEA 1  One-pass snow-berm ice lane")
# KILLER: depth-mean under-ice velocity needed to slide a +1% buoyant 1 m3 pod
# along the (granted smooth) channel ceiling AND cover 500 km in a 120-day window.
V1, D1 = 1.0, 1.0
A1 = math.pi / 4 * D1 ** 2
Cd1 = 0.85                   # short cylinder end-on (bluff), favourable (high drag)
u_thr1 = slide_threshold(V1, A1, Cd1)
dist1, window = 500e3, 120 * DAY   # ASSUMPTION: mine->plant 500 km, usable ice window 120 d
u_drift1 = dist1 / window
fac1 = loglaw_factor(1.0)          # recess sheltering ignored (favourable)
req1 = (u_thr1 + u_drift1) / fac1
m1 = U_TYP / req1
p(f"  slide threshold {u_thr1:.3f} m/s + drift {u_drift1:.3f} m/s; near-ice factor {fac1:.2f}")
p(f"  required depth-mean {req1:.3f} m/s ; available {U_TYP:.2f} (main ch.) best {U_BEST:.2f} [S1]")
p(f"  MARGIN typical {m1:.2f}  best {U_BEST/req1:.2f}  (mu=0.1 -> {U_TYP/((slide_threshold(V1,A1,Cd1,mu=0.1)+u_drift1)/fac1):.2f})")
# CHAIN: riverside high-grade ore to an existing plant. Best practice = summer barge of ore.
grade = 10.0                        # g/t, ASSUMPTION "high-grade"
t_per_oz = 31.1035 / grade
deliv_A = 2550.0                    # $/oz delivered, archetype A (ledger) as remote-gold proxy
barge_tkm = 4.0                     # rub/t-km, ledger 3-5 rub/t-km
barge = barge_tkm * 500 / RUB_PER_USD          # $/t ore for 500 km
barge_hi = 8000 / RUB_PER_USD                  # ledger 8,000 rub/t per seasonal haul
pod_price = (55.0, 120.0)           # $ per 1 m3 sealed IBC-type pod [S5]
# central: pod reused 5x, returned by summer barge at half the forward rate (bulky empties)
pod_c = pod_price[0] / 5 + 0.5 * barge
cost_now = deliv_A
cost_idea_c = deliv_A - barge * t_per_oz + pod_c * t_per_oz
r1 = cost_now / cost_idea_c
r1_lo = deliv_A / (deliv_A - barge * t_per_oz + pod_price[0] * t_per_oz)     # single-use pods
r1_hi = deliv_A / (deliv_A - barge_hi * t_per_oz + pod_price[0] / 5 * t_per_oz)  # long haul, free return
p(f"  barge {barge:.1f} $/t ore ({barge*t_per_oz:.0f} $/oz); pod cost central {pod_c:.1f} $/t")
p(f"  CHAIN now {cost_now:.0f} $/oz, with idea {cost_idea_c:.0f} $/oz -> RATIO {r1:.3f} (range {r1_lo:.2f}-{r1_hi:.2f})")
p("  VERDICT", verdict(m1, r1))

# ===========================================================================
p("=" * 78)
p("IDEA 2  Cold-sealed rolling snow-log pods")
# KILLER: velocity to roll a 1.6 m log (+750 kg) over 5-20 cm ice keels. Idea's own numbers 0.62-0.95 m/s;
# reproduce: wheel-over-step force F = B*sqrt(2Rk-k^2)/(R-k), drag F = 0.5 rho Cd D L u^2.
R2, B2 = 0.8, 750 * g
for L in (6.0, 9.0):
    for k in (0.05, 0.20):
        F = B2 * math.sqrt(2 * R2 * k - k * k) / (R2 - k)
        u = math.sqrt(2 * F / (RHO_W * 1.0 * 2 * R2 * L))
        p(f"  log L={L:.0f} m keel {k*100:.0f} cm -> F {F:.0f} N, u_req {u:.2f} m/s")
req2 = 0.62                          # idea's own minimum (5 cm keels)
m2 = U_TYP / req2
p(f"  required >= {req2} m/s ; available {U_TYP} typical, {U_BEST} best [S1]; Kolyma winter Q only 61-127 m3/s [S3]")
p(f"  MARGIN typical {m2:.2f}  best {U_BEST/req2:.2f}")
# CHAIN: archetype C settlement coal, delivered ~275 $/t, outbound logistics 85 %.
deliv_C = 23000 / RUB_PER_USD
barge_C = 8000 / RUB_PER_USD        # river barge leg replaced by pods
pod2 = 6.8                          # idea's own pod cost $/t
r2 = deliv_C / (deliv_C - barge_C + pod2)
r2_hi = deliv_C / (deliv_C - 0.85 * deliv_C + pod2)
p(f"  CHAIN now {deliv_C:.0f} $/t, with idea {deliv_C-barge_C+pod2:.0f} $/t -> RATIO {r2:.2f} (if last mile also replaced {r2_hi:.1f})")
p("  VERDICT", verdict(m2, r2))

# ===========================================================================
p("=" * 78)
p("IDEA 3  Under-ice river drift pods (torpedo, slightly buoyant)")
D3, L3 = 0.5, 2.5
A3 = math.pi / 4 * D3 ** 2
V3 = 0.7 * A3 * L3                   # torpedo fineness factor 0.7
Cd3 = 0.2                            # streamlined body of revolution incl. wall proximity (favourable side)
u_thr3 = slide_threshold(V3, A3, Cd3)
dist3 = 1000e3                       # ASSUMPTION: riverside mine -> Arctic port ~1,000 km (lower Lena reach alone ~600 km [S2])
u_drift3 = dist3 / window
fac3 = loglaw_factor(D3)
req3 = (u_thr3 + u_drift3) / fac3
m3 = U_TYP / req3
p(f"  V {V3:.2f} m3, slide threshold {u_thr3:.3f} m/s (smooth ice granted, no keels), drift {u_drift3:.3f} m/s, factor {fac3:.2f}")
p(f"  required depth-mean {req3:.2f} m/s ; MARGIN typical {m3:.2f} best {U_BEST/req3:.2f}")
# CHAIN: concentrate (archetype B structure): 8,500 $/t Cu, 1.4 Mt conc / 300 kt Cu [S16]
deliv_B = 8500.0
conc_per_cu = 1.4e6 / 300e3
barge3 = 4.0 * 1000 / RUB_PER_USD    # ledger 3-5 rub/t-km x 1,000 km
pod3 = pod_price[0] / 5 + 0.5 * barge3
cost3 = deliv_B - (barge3 - pod3) * conc_per_cu
r3 = deliv_B / cost3
r3_hi = deliv_B / (deliv_B - (8000 / RUB_PER_USD) * conc_per_cu)   # pods free, long haul
p(f"  barge {barge3:.1f} $/t conc vs pods {pod3:.1f} $/t; CHAIN now {deliv_B:.0f} with idea {cost3:.0f} $/t Cu -> RATIO {r3:.3f} (max if pods free {r3_hi:.3f})")
p("  VERDICT", verdict(m3, r3))

# ===========================================================================
p("=" * 78)
p("IDEA 4  Midnight-sun salt-gradient power pond (Yakutsk 62.0 N)")
H = {5: 565.6, 6: 632.7, 7: 603.4, 8: 444.1, 9: 276.5}   # MJ/m2 global horizontal, ice-free months [S6]
k_w = 0.60                  # W/m K brine/water [S8]
UCZ = 0.2                   # m, ASSUMPTION thin upper zone (favourable)
T_lcz = 70.0
lat = math.radians(62.0)
def zenith_weighted_cos(month):
    decl = math.radians(23.44 * math.sin(math.radians(360 / 365 * (30.4 * month - 15 - 81))))
    num = den = 0.0
    for i in range(1440):
        h = math.radians((i / 1440) * 360 - 180)
        cz = math.sin(lat) * math.sin(decl) + math.cos(lat) * math.cos(decl) * math.cos(h)
        if cz > 0:
            sz = math.sqrt(1 - cz * cz)
            cr = math.sqrt(1 - (sz / 1.333) ** 2)
            num += cz * cr; den += cz
    return num / den           # irradiance-weighted cos(refraction angle)
cosr = {m: zenith_weighted_cos(m) for m in H}
def tau(x):                    # Bryant & Colbeck [S7]
    return 0.36 - 0.08 * math.log(x)
def absorbed(L):
    return sum(H[m] * 0.95 * tau((UCZ + L) / cosr[m]) for m in H)      # MJ/m2/yr, 5 % surface reflection
days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
T_ucz = [0, 0, 0, 0, 5, 12, 15, 12, 5, 0, 0, 0]   # under ice Oct-Apr = 0 C; summer ASSUMPTION
def top_loss(L, T=T_lcz):
    return sum(k_w * (T - T_ucz[i]) / L * days[i] * DAY for i in range(12)) / 1e6
ground = 5.0 * 365 * DAY / 1e6        # ASSUMPTION 5 W/m2 through heavy insulation over permafrost
L_std = 1.18                          # upper end of optimum NCZ found in [S9]
a, l = absorbed(L_std), top_loss(L_std) + ground
m4 = a / l
p(f"  NCZ {L_std} m: absorbed {a:.0f} MJ/m2/yr vs losses at 70 C {l:.0f} (top {top_loss(L_std):.0f} + ground {ground:.0f}) -> MARGIN {m4:.2f}")
best = max(((absorbed(L) / (top_loss(L) + ground), L) for L in [0.5 + 0.1 * i for i in range(40)]))
p(f"  best NCZ thickness {best[1]:.1f} m gives margin {best[0]:.2f} with ZERO heat extraction")
# electric yield: optimise NCZ thickness (and LCZ temperature), ORC at 0.5 Carnot to -30 C winter sink
def best_yield(Tmin, Tmax):
    best_e = (0, 0, 0)
    for L in [0.5 + 0.1 * i for i in range(46)]:
        for T in range(Tmin, Tmax + 1, 2):
            q = absorbed(L) - top_loss(L, T) - 5.0 * (T / 70) * 365 * DAY / 1e6
            if q <= 0:
                continue
            eta = 0.5 * (1 - 243.15 / (T + 273.15))
            e = q * eta / 3.6     # kWh_e/m2/yr
            if e > best_e[0]:
                best_e = (e, L, T)
    return best_e
be = best_yield(60, 80)        # as written: storage layer held at 60-80 C
bg = best_yield(10, 90)        # generous: any storage temperature
p(f"  max electric yield as written (60-80 C) {be[0]:.1f} kWh_e/m2/yr at NCZ {be[1]:.1f} m, LCZ {be[2]} C")
p(f"  (unconstrained bound {bg[0]:.1f} kWh_e/m2/yr at LCZ {bg[2]} C, NCZ {bg[1]:.1f} m)")
capex_m2 = 35.0 * 2.0          # lowest sourced pond cost [S10] x low-end Far North premium 2x (ledger)
c_diesel = 0.49                 # ledger mine-scale diesel
share_E = 0.10                  # archetype A energy share, assume pond replaces ALL of it (generous)
c_pond = 0.10 * capex_m2 / be[0]   # $/kWh, 10 %/yr capital charge, ORC capex & O&M excluded
c_pond_g = 0.10 * capex_m2 / bg[0]
r4 = 1 / (1 - share_E + share_E * c_pond / c_diesel)
r4_g = 1 / (1 - share_E + share_E * c_pond_g / c_diesel)
p(f"  pond electricity {c_pond:.2f} $/kWh vs diesel {c_diesel} -> CHAIN RATIO {r4:.2f} (unconstrained bound {c_pond_g:.2f} $/kWh -> {r4_g:.2f}; free power cap {1/(1-share_E):.2f})")
p("  VERDICT", verdict(m4, r4))

# ===========================================================================
p("=" * 78)
p("IDEA 5  Superconducting rotating-field grinding pipe")
feed_emm = 1.0            # mm, largest feed demonstrated in electromagnetic (needle) mill [S12]
feed_req_crushed = 16.0   # mm, fully crushed SAG-feed scenario F80 [S13]
feed_req_sag = 152.4      # mm, SAG feed F80 that the grinding block actually takes [S13]
m5 = feed_emm / feed_req_crushed
p(f"  feed size: available {feed_emm} mm vs required {feed_req_crushed} mm (crushed) / {feed_req_sag} mm (SAG duty)")
# supporting energy check: 1x10 mm steel needle at 10 m/s vs breaking a 16 mm ore particle at 0.25 kWh/t (ASSUMPTION, JK t10~10 %)
m_needle = math.pi / 4 * 1e-3 ** 2 * 10e-3 * 7850
ke = 0.5 * m_needle * 10 ** 2
m_part = math.pi / 6 * 0.016 ** 3 * 2700
e_break = 0.25 * 3.6e6 / 1000 * m_part
p(f"  needle KE {ke*1e3:.2f} mJ vs ~{e_break:.1f} J to break a 16 mm particle -> energy ratio {ke/e_break:.1e}")
p(f"  MARGIN {m5:.3f} (size, lenient crushed-feed case); {feed_emm/feed_req_sag:.4f} for SAG duty")
cap_share = 0.41          # ledger B
plant_frac, comm_frac, grind_frac = 0.45, 0.50, 0.70   # plant share ASSUMPTION; comminution 50 % of plant at 20 Mt/a [S14]
grind_capex = plant_frac * comm_frac * grind_frac
r5 = 1 / (1 - cap_share * grind_capex * 0.9)
r5_hi = 1 / (1 - cap_share * 0.81 * 0.50 * 0.70)    # plant+infra 81 % of capex [S15], grinding free
p(f"  grinding = {grind_capex:.3f} of capex; 10x lighter -> CHAIN RATIO {r5:.3f} (upper bound, grinding free & plant 81 %: {r5_hi:.3f})")
p("  VERDICT", verdict(m5, r5))

# ===========================================================================
p("=" * 78)
p("IDEA 6  Self-feeding ore-ice dam")
E_ice = 101.0               # MJ/m3 thaw energy of ice-cemented gravel (idea-7 figure; 0.33 porosity x 917 x 0.3335)
E_chk = 0.33 * 917 * 0.3335
cw = 4.19                   # MJ/m3 K
T_basin = 10.0              # C, sun-warmed basin in July; Kolyma main stem 10-15 C [S18]
R6 = E_ice / (cw * T_basin)           # m3 water per m3 gravel delivered to the chute (100 % heat use)
req_water = math.sqrt(3.2 * 9.9)      # geometric mid of US plants 3.2-9.9 m3/m3 [S17]; Russian T:L 1:10-1:20 is higher
m6 = R6 / req_water
p(f"  thaw energy {E_ice} (check {E_chk:.0f}) MJ/m3; water ratio at {T_basin} C = {R6:.2f} m3/m3 vs sluice need {req_water:.1f}")
p(f"  MARGIN {m6:.2f} (at 7 C: {E_ice/(cw*7)/req_water:.2f}; at 15 C: {E_ice/(cw*15)/req_water:.2f})")
deliv_g = 6900 / RUB_PER_USD          # $/g, archetype A (ledger)
wash_now = 4.65 / 0.684               # $/g: idea-7 bottom-up current washing link ($4.65/m3, 0.684 g/m3 recovered)
wash_idea6 = 2.0 / 0.684              # ASSUMPTION: dam laying + winter spraying + peat ~ same as idea-7 passive cost
r6 = deliv_g / (deliv_g - wash_now + wash_idea6)
r6_hi = deliv_g / (deliv_g - wash_now)
p(f"  washing link {wash_now:.2f} $/g of {deliv_g:.1f} $/g ({wash_now/deliv_g*100:.1f} %) -> CHAIN RATIO {r6:.3f} (if washing free {r6_hi:.3f})")
p("  VERDICT", verdict(m6, r6))

# ===========================================================================
p("=" * 78)
p("IDEA 7  Self-feeding ore-ice buttress dam")
E_loose = 52.5              # MJ/m3 (idea: 50-55)
R7 = (2.2, 3.2)             # idea's own design water ratio; check:
p(f"  check: {E_loose}/(4.19*7)={E_loose/(cw*7):.2f}, /(4.19*5)={E_loose/(cw*5):.2f} m3/m3 (idea says 2.2-3.2)")
m7 = (sum(R7) / 2) / req_water
p(f"  design ratio {sum(R7)/2:.1f} m3/m3 vs sluice need {req_water:.1f} (US 3.2-9.9; RU 10-20) -> MARGIN {m7:.2f}")
p(f"  (face thaw 70 m/day vs 0.8 needed -> {70/0.8:.0f}x headroom, not the killer)")
wash_idea7 = 2.0 / 0.684
r7 = deliv_g / (deliv_g - wash_now + wash_idea7)
p(f"  CHAIN now {deliv_g:.1f} $/g with idea {deliv_g-wash_now+wash_idea7:.1f} $/g -> RATIO {r7:.3f}")
p("  VERDICT", verdict(m7, r7))

# ===========================================================================
p("=" * 78)
p("IDEA 8  Gun-launched gliding freight shuttle")
shell, mv, charge, life = 517.0, 762.0, 124.7, 344      # 12"/50 Mk 8 [S19]
ke8 = 0.5 * 500 * 700 ** 2
p(f"  analog 12in/50 Mk8: {shell} kg at {mv} m/s, KE {0.5*shell*mv**2/1e6:.0f} MJ; idea 0.5 t at 0.7 km/s KE {ke8/1e6:.0f} MJ")
conc = 1.4e6                          # t/yr, archetype B
shots = conc / 0.5                    # payload 0.5 t per shot (generous: casing mass ignored)
m8 = life / shots
m8_small = life / (50e3 / 0.5)
p(f"  shots/yr {shots:.2e} vs barrel life {life} -> MARGIN {m8:.1e} (small 50 kt/yr mine: {m8_small:.1e}); a barrel every {life/shots*365*24:.2f} h")
nc_floor = 3.18 / 0.4536 / 1.67       # $/kg propellant: cotton-linter cost [S20] / NC mass yield 1.67 (stoichiometry)
prop_t = charge / shell * nc_floor * 1000   # $/t payload, propellant raw-material floor only
out_B = 0.05 * deliv_B; in_B = 0.03 * deliv_B
cost8 = deliv_B - out_B - in_B + prop_t * conc_per_cu
r8 = deliv_B / cost8
# generous alternative: diesel-fired launcher at 30 % muzzle efficiency, 40 % genset, remote diesel 1.9 $/kg, no wear
dies_shot = ke8 / 0.3 / 0.4 / 43e6
dies_t = dies_shot * 1.9 / 0.5
r8_alt = deliv_B / (deliv_B - out_B - in_B + dies_t * conc_per_cu * 1.3)
p(f"  propellant floor {nc_floor:.2f} $/kg -> {prop_t:.0f} $/t payload; CHAIN with idea {cost8:.0f} $/t Cu -> RATIO {r8:.2f}")
p(f"  (generous diesel-fired, zero barrel/casing wear: {dies_shot:.1f} kg diesel/shot, {dies_t:.0f} $/t -> RATIO {r8_alt:.2f})")
p("  VERDICT", verdict(m8, r8))

p("=" * 78)
p("SUMMARY (per-unit chain costs)")
p(f"  cos(refraction) May-Sep: " + ", ".join(f"{m}:{cosr[m]:.2f}" for m in H))
rows = [
    (1, m1, r1, f"{cost_now:.0f} -> {cost_idea_c:.0f} $/oz"),
    (2, m2, r2, f"{deliv_C:.0f} -> {deliv_C-barge_C+pod2:.0f} $/t coal"),
    (3, m3, r3, f"{deliv_B:.0f} -> {cost3:.0f} $/t Cu"),
    (4, m4, r4, f"{deliv_A:.0f} -> {deliv_A/r4:.0f} $/oz"),
    (5, m5, r5, f"{deliv_B:.0f} -> {deliv_B/r5:.0f} $/t Cu"),
    (6, m6, r6, f"{deliv_g:.1f} -> {deliv_g/r6:.1f} $/g ({deliv_A:.0f} -> {deliv_A/r6:.0f} $/oz)"),
    (7, m7, r7, f"{deliv_g:.1f} -> {deliv_g/r7:.1f} $/g ({deliv_A:.0f} -> {deliv_A/r7:.0f} $/oz)"),
    (8, m8, r8, f"{deliv_B:.0f} -> {cost8:.0f} $/t Cu"),
]
for i, m, r, c in rows:
    p(f"  IDEA {i}: MARGIN {m:.3g}  RATIO {r:.3f}  chain {c}  -> {verdict(m, r)}")

with open(__file__.replace("gate8_checks.py", "gate8_results.txt"), "w") as fh:
    fh.write("\n".join(out) + "\n")

SOURCES = """
S1  Fedorova, Zdorovennov, Zdorovennova, Aksenov 2020, E3S Web Conf 163:05003, https://www.e3s-conferences.org/10.1051/e3sconf/202016305003
S2  Kaab et al. 2013, HESS 17:4671, https://hess.copernicus.org/articles/17/4671/2013/
S3  GRDC Srednekolymsk monthly means, https://www.compositerunoff.sr.unh.edu/html/Polygons/P2998500.html
S4  Vance 1980 Katmai Bay ice-hull friction 0.02-0.47 (via MDPI Lubricants 11(8):314, https://www.mdpi.com/2075-4442/11/8/314)
S5  IBC tote prices, https://www.repackify.com/listing/new-275-gallon-1000l-ibc-totes-orem-ut-84057
S6  SNiP climatology Table 17 (Yakutsk Q), https://dnaop.com/html/66253_7.html
S7  Bryant & Colbeck formula, https://www.e3s-conferences.org/articles/e3sconf/pdf/2024/54/e3sconf_apecvii2024_02016.pdf
S8  https://www.engineeringtoolbox.com/water-liquid-gas-thermal-conductivity-temperature-pressure-d_2012.html
S9  https://research.uaeu.ac.ae/en/publications/effect-of-energy-extraction-on-solar-pond-performance/
S10 https://portal.arid.my/0/Publications/Details/3882 ; https://www.osti.gov/biblio/109854 ; https://trid.trb.org/View/275350
S11 https://www.jewishvirtuallibrary.org/jsource/Environment/Solar.html
S12 Wolosiewicz-Glab et al. 2018, Appl Sci 8(8):1322, https://www.mdpi.com/2076-3417/8/8/1322
S13 https://cdn-web-content.srk.com/upload/user/image/ADance_FeedSizeEffects_SME2022 Panel(secured)20220304140711951.pdf ; https://onemine.org/documents/optimizing-sag-mill-product-stze-in-sag-mill-ball-mill-circuits-
S14 https://www.scribd.com/doc/269557894/Crushing-and-Grinding-Circuit-Design
S15 https://www.sec.gov/Archives/edgar/data/1364125/000106299323020061/exhibit99-2.htm
S16 https://www.globalminingreview.com/exploration-development/29092021/kaz-minerals-completes-baimskaya-bankable-feasibility-study
S17 https://www.911metallurgist.com/blog/gravity-gold-process-water-requirements/ ; https://trud.igduran.ru/index.php/psu/article/view/559
S18 https://dic.academic.ru/dic.nsf/bse/97148/
S19 https://navweaps.com/Weapons/WNUS_12-50_mk8.php ; https://www.navygeneralboard.com/?p=4121
S20 https://defence-blog.com/?p=88032
S21 Value ledger in TASK.md (archetype costs, shares, freight, diesel, power)
"""
