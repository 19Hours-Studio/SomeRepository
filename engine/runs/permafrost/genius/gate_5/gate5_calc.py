"""Gate 5 kill test: KILLER margin and CHAIN ratio for 8 ideas.
Sources are noted next to each decisive input. Run: python3 -I gate5_calc.py
"""
import math

g = 9.81
RUB_USD = 84.0  # ledger

def line(*a):
    print(*a)

# ---------------------------------------------------------------- ledger
A_now = 2550.0               # $/oz placer delivered (ledger A)
A_sh = dict(energy=.10, labour=.20, inbound=.12, outbound=.002, processing=.20, capital=.15, other=.22)
B_now = 8500.0               # $/t Cu CIF China gross (ledger B)
B_out = 0.05; B_cap = 0.41
C_now = 83.0                 # $/t FOB export coal (ledger C)
C_out = 0.55
C_settle = 23000 / RUB_USD   # $/t at boiler, settlement (ledger C)
D_now = 10200.0              # $/t LCE (ledger D)

# Baimskaya concentrate per t Cu, from ledger: gold credit = (8500-2500)*Cu_t
au_credit = 490e3 * 4150.0
cu_t = au_credit / (B_now - 2500.0)
conc_per_cu = 1.4e6 / cu_t

print("=" * 70)
print("IDEA 1  Plume-Assay Needle Drilling")
# KILLER: gold particles per sample (Clifton et al. 1969, USGS PP 625-C:
#   ~20 particles needed for +/-50% precision at 95%, per SMEDG note).
d_hole = 0.02                       # m, 'finger-thin'
V_1m = math.pi * (d_hole / 2) ** 2 * 1.0      # m3 per 1-m composite
V_5cm = math.pi * (d_hole / 2) ** 2 * 0.05    # 'every few centimetres'
grade = 1.75e-3                     # kg/m3 = 1.75 g/m3, Topky placer, Kolyma (Mindat) - rich case
flake = 0.5e-3 * 0.5e-3 * 0.1e-3    # m3, fine 0.5 mm flake (generous: smaller -> more particles)
m_flake = 19300 * flake
n_m3 = grade / m_flake
n_1m = n_m3 * V_1m
n_5cm = n_m3 * V_5cm
req_particles = 20
M1 = n_1m / req_particles
line(f"  flake mass {m_flake*1e6:.3f} mg; particles/m3 {n_m3:.0f}; per 1-m composite {n_1m:.2f}; per 5-cm reading {n_5cm:.3f}")
line(f"  MARGIN = {n_1m:.2f}/{req_particles} = {M1:.3f}")
# side check: vaporisation energy is NOT the killer (Woskov MIT 2009 report ~26 kJ/cm3)
E_m = 26e3 * V_1m * 1e6             # J per metre (26 kJ/cm3)
line(f"  (side check: {E_m/1e6:.1f} MJ/m -> {100e3/E_m*3600:.0f} m/h at 100 kW, not limiting)")
# CHAIN: MinEx discovery cost $62/oz-eq (2009-2018, June-2019 $); CPI x1.30 to 2026
disc = 62 * 1.30
expl_total = 2 * disc               # + equal resource-definition spend (generous)
saving = 0.9 * expl_total           # idea cuts it 90%
A_idea1 = A_now - saving
R1 = A_now / A_idea1
line(f"  exploration+definition ~${expl_total:.0f}/oz; saving ${saving:.0f}/oz; with idea ${A_idea1:.0f}/oz; RATIO {R1:.3f}")

print("=" * 70)
print("IDEA 2  Spray-Ice Drift Pods")
# KILLER: share of Laptev-launched floes reaching Fram Strait (Krumpen et al. 2019 Sci Rep / AWI):
#   'up to 50% of FYI entered the Transpolar Drift' pre-2000; 'rarely more than 20% survived' now.
req_arrive = 0.90
avail_arrive = 0.50
M2 = avail_arrive / req_arrive
line(f"  MARGIN = {avail_arrive}/{req_arrive} = {M2:.2f}  (with today's 0.20 survival: {0.20/req_arrive:.2f})")
# CHAIN vs ledger C export ($83/t FOB): keep the non-logistics 45%
non_log = C_now * (1 - C_out)
bag = 10.25                          # $/bag 1 t FIBC, 215+ lot (Palmetto Industries)
ice_m3_t = 3.0; spray_ratio = 2.0    # m3 ice per t; sprayed/frozen
E_spray = ice_m3_t * spray_ratio * 1.0e6 / 0.7 / 3.6e6   # kWh/t at 1 MPa, 70% pump
spray = E_spray * 0.49               # $0.49/kWh mine-scale diesel (ledger)
launch_cost = non_log + bag + spray
carry = launch_cost * (1.14 ** 2 - 1) # 2 yr at CBR key rate 14% (Sep 2026)
pickup_gen = 20.0                    # generous; ledger NSR general cargo 15-17k rub/t = ~$190/t
pickup_led = 16000 / RUB_USD
C_idea2_gen = launch_cost + carry + pickup_gen
C_idea2_led = launch_cost + carry + pickup_led
R2 = C_now / C_idea2_gen
line(f"  non-log ${non_log:.2f} + bag ${bag} + spray ${spray:.2f} ({E_spray:.1f} kWh/t) + carry ${carry:.1f} + pickup ${pickup_gen}")
line(f"  with idea ${C_idea2_gen:.1f}/t (generous) -> RATIO {R2:.2f}; with ledger NSR bag-cargo rate ${C_idea2_led:.0f}/t -> {C_now/C_idea2_led:.2f}")
line(f"  with 50% arrival the launch-side cost doubles: ${ (launch_cost+carry)/0.5 + pickup_gen:.0f}/t")

print("=" * 70)
print("IDEA 3  Self-Sorting Wave-and-Ice Pond")
# KILLER: near-bed wave orbital velocity vs threshold for 0.5 mm sand.
# Wave growth: USACE Coastal Engineering Manual EM 1110-2-1100 Part II-2 (fetch-limited):
#   gHm0/u*^2 = 4.13e-2 (gF/u*^2)^0.5 ; gTp/u* = 0.651 (gF/u*^2)^(1/3) ; Cd = 0.001(1.1+0.035U10)
# Threshold: Soulsby (1997) theta_cr; wave friction f_w = max(1.39(A/z0)^-0.52, 2 Re^-0.5)
def waves(U10, F):
    Cd = 0.001 * (1.1 + 0.035 * U10)
    us = U10 * math.sqrt(Cd)
    X = g * F / us ** 2
    Hm0 = 4.13e-2 * X ** 0.5 * us ** 2 / g
    Tp = 0.651 * X ** (1 / 3) * us / g
    return Hm0, Tp

def wavenumber(T, h):
    w = 2 * math.pi / T
    k = w * w / g
    for _ in range(200):
        k = w * w / (g * math.tanh(k * h))
    return k

def ub(H, T, h):
    k = wavenumber(T, h)
    return math.pi * H / (T * math.sinh(k * h))

nu = 1.5e-6; rho = 1000.0; rhos = 2650.0
def u_crit(D, T):
    s = rhos / rho
    Dst = D * (g * (s - 1) / nu ** 2) ** (1 / 3)
    th = 0.30 / (1 + 1.2 * Dst) + 0.055 * (1 - math.exp(-0.020 * Dst))
    tau_cr = th * g * (rhos - rho) * D
    lo, hi = 1e-4, 5.0
    for _ in range(100):
        U = 0.5 * (lo + hi)
        A = U * T / (2 * math.pi)
        z0 = D / 12
        fr = 1.39 * (A / z0) ** -0.52
        fl = 2 * (U * A / nu) ** -0.5
        tau = 0.5 * rho * max(fr, fl) * U * U
        if tau > tau_cr:
            hi = U
        else:
            lo = U
    return U

U10 = 10.0; F = 1000.0   # upper-bound summer wind (typical 1-5 m/s, yr.no Susuman) and long fetch
H, T = waves(U10, F)
for h in (0.5, 1.0, 1.5):
    u = ub(H, T, h)
    line(f"  U10 {U10} m/s, F {F:.0f} m: Hm0 {H:.3f} m, Tp {T:.2f} s; depth {h} m -> u_bed {u:.4f} m/s")
u_b = ub(H, T, 1.0)
uc_sand = u_crit(0.5e-3, T)
uc_grav = u_crit(20e-3, T)
M3 = u_b / uc_sand
line(f"  u_crit 0.5-mm sand {uc_sand:.3f} m/s; 20-mm gravel {uc_grav:.3f} m/s")
line(f"  MARGIN (sand, h=1.0 m) = {u_b:.4f}/{uc_sand:.3f} = {M3:.2f}; (gravel) {u_b/uc_grav:.3f}")
# CHAIN vs ledger A, as if it worked: earthmoving+washing ~2/3 of physical cost cut to 5%
phys = A_now * (1 - A_sh['other'])
earth = phys * 2 / 3
A_idea3 = A_now * A_sh['other'] + phys / 3 + 0.05 * earth + 50.0   # +$50/oz pond works (est.)
R3 = A_now / A_idea3
line(f"  with idea ${A_idea3:.0f}/oz; RATIO {R3:.2f}")

print("=" * 70)
print("IDEA 4  Stored Meltwater Barge Pulse")
# KILLER: seasonal release volume to float B-scale tonnage vs snowmelt of a small-creek basin.
# Kinematic wave: crest celerity 5/3 V (Manning, wide channel) > barge drift ~V, so the
# full-draft flow must last until the release tail catches the barges: x* = 2.5 V T
# -> prism volume per pulse = 0.4 W d L; plus water moving with each barge slot W d s.
W = 20.0; d = 0.8; L = 100e3
barge_L, gap = 30.0, 100.0; payload = 75.0      # 30x6 m flat barge, 0.6 m draft
s = barge_L + gap
w_per_t = W * d * s / payload
tonnage = 1.4e6
V_req = 0.4 * W * d * L + tonnage * w_per_t
# Kolyma: 123 km3/yr over 643,000 km2 (BSE) = ~190 mm; snow-fed 47% -> ~90 mm snowmelt
runoff = 123e9 / 643e9 * 0.47
V_av = 100e6 * runoff                 # 100 km2 'small creek' basin (generous)
M4 = V_av / V_req
line(f"  water/t {w_per_t:.1f} m3; required {V_req/1e6:.1f} Mm3; snowmelt {runoff*1000:.0f} mm -> available {V_av/1e6:.1f} Mm3")
line(f"  MARGIN {M4:.2f}")
B_idea4 = B_now * (1 - B_out)          # even if ALL outbound logistics became free
R4 = B_now / B_idea4
line(f"  with idea >= ${B_idea4:.0f}/t Cu; RATIO <= {R4:.3f}")

print("=" * 70)
print("IDEA 5  Self-Charging Frost Separator Cascade")
x = 0.41; E = 3.0e5; fall = 1.5
t = math.sqrt(2 * fall / g)
qm_req = 2 * x / (E * t * t)
qm_av = 4.30e-6      # C/kg = 4.30 nC/g feldspar (quartz 6.05) after 1.5 m tribocharging (onemine ilmenite-ore study)
M5 = qm_av / qm_req
line(f"  fall time {t:.3f} s; q/m required {qm_req*1e6:.2f} uC/kg; available {qm_av*1e6:.2f} (feldspar) / 6.05 (quartz)")
line(f"  MARGIN {M5:.2f} (quartz {6.05e-6/qm_req:.2f})")
# CHAIN: idea's own $3,994 vs $4,588 per t Li2O; Li2CO3/Li2O = 73.89/29.88; chem recovery 0.88 (est.)
sav_li2o = 4588 - 3994
li2o_per_lce = 1 / (73.89 / 29.88) / 0.88
D_idea5 = D_now - sav_li2o * li2o_per_lce
R5 = D_now / D_idea5
line(f"  Li2O per t LCE {li2o_per_lce:.3f}; saving ${sav_li2o*li2o_per_lce:.0f}/t LCE; with idea ${D_idea5:.0f}; RATIO {R5:.3f}")

print("=" * 70)
print("IDEA 6  Woven pressure-shell concentrator")
P_burst = 77 * 6894.76               # Pa, Sierra Space full-scale LIFE UBP (77 psi)
R_life = 27 * 0.3048 / 2             # m, 27 ft diameter
T_av = P_burst * R_life
rho_sl = 0.8e5 / (g * 6.0)           # idea: 6 m of slurry = 0.8 bar
R_thick = 30.0                       # m, 60-m tailings thickener (TAKRAF/DELKOR Talabre units)
SF = 4.0                             # NASA softgoods factor (60.8 psi = 4 x 15.2 psi MOP)
T_req = SF * rho_sl * g * 6.0 * R_thick
M6 = T_av / T_req
T_cell = SF * 0.8e5 * 5.0
line(f"  demonstrated hoop capacity {T_av/1e6:.2f} MN/m; thickener needs {T_req/1e6:.2f} MN/m (SF4); MARGIN {M6:.2f}")
line(f"  (10-m flotation cell needs {T_cell/1e6:.2f} MN/m -> {T_av/T_cell:.2f}, passes)")
# CHAIN: concentrator <=50% of capex (generous); of plant cost, shells address half
# (Ausenco: equipment / bulk materials / labour / indirects ~ four equal parts)
addr = 0.50 * (0.25 * 0.75 + 0.25 * 0.75 + 0.25 * 0.5)
cut = 0.9 * addr
B_idea6 = B_now - B_now * B_cap * cut
R6 = B_now / B_idea6
line(f"  addressable capex share {addr:.3f}; delivered-cost cut {B_cap*cut*100:.1f}%; with idea ${B_idea6:.0f}; RATIO {R6:.3f}")

print("=" * 70)
print("IDEA 7  Fire-controlled ballistic ore transfer")
slug = 0.3                           # t concentrate per round (100-500 kg)
rounds_yr = 1.4e6 / slug
req_life = rounds_yr / 365           # one barrel change per day
av_life = 65                         # Paris Gun: 1,640 m/s, ~106 kg, 130 km; barrel life ~65 rounds
M7 = av_life / req_life
line(f"  rounds/yr {rounds_yr:.3g}; required barrel life {req_life:.0f}; available {av_life}; MARGIN {M7:.4f}")
KE = 0.5 * 1500 ** 2                 # J/kg
payload_frac = 0.7; eff = 0.30
kWh_t = KE * 1000 / payload_frac / eff / 3.6e6
p_npp = 6.45 / RUB_USD               # floating NPP 6.45 rub/kWh (2020 prices, ledger)
gun_cu = kWh_t * p_npp * conc_per_cu
B_idea7 = B_now - B_now * B_out + gun_cu
R7 = B_now / B_idea7
line(f"  Cu output {cu_t/1e3:.0f} kt/yr -> {conc_per_cu:.2f} t conc/t Cu; gun energy {kWh_t:.0f} kWh/t conc = ${gun_cu:.0f}/t Cu vs outbound ${B_now*B_out:.0f}")
line(f"  with idea >= ${B_idea7:.0f}/t Cu (no barrels, casings, catch basin); RATIO {R7:.3f}")

print("=" * 70)
print("IDEA 8  Village Coal Gasified Underfoot")
# KILLER: seam area gasified per well pair. Chinchilla: ~35 kt from 2 gasifiers, 10 m seam, 130 m deep
per_gas = 35000 / 2
foot = per_gas / (1.3 * 10.0 * 0.7)  # m2, 70% sweep (generous)
req_area = 5000 * 3                  # 0.5 ha/yr x 'every few (3) years'
M8 = foot / req_area
line(f"  footprint per pair {foot/1e4:.3f} ha; required {req_area/1e4:.2f} ha; MARGIN {M8:.3f}")
# CHAIN for 10 kt/yr village vs ledger settlement coal ($275/t at boiler)
tpy = 10000
labour = 7 * 2 * 60000               # 7 posts x 2 workers x $60k (ledger FIFO)
plant = 8e6 * 0.92 * 1.45            # Cougar Energy UCG pilot A$8M (2010) -> 2026 US$
crf = 0.14 / (1 - 1.14 ** -15)       # 14% key rate, 15 yr
pairs = 5000 / foot                  # pairs per year at 0.5 ha/yr
wells = pairs * 0.3e6                # $0.3M per directional pair (est.)
compress = 15 * tpy                  # syngas-engine driven compressors (est. $15/t)
monitor = 10 * tpy
cost8 = (labour + plant * crf + wells + compress + monitor) / tpy
cost8_nowell = (labour + plant * crf + compress + monitor) / tpy
R8 = C_settle / cost8
line(f"  labour ${labour/tpy:.0f}/t; plant ${plant*crf/tpy:.0f}/t (capex ${plant/1e6:.1f}M, CRF {crf:.3f}); wells {pairs:.1f} pairs/yr ${wells/tpy:.0f}/t")
line(f"  now ${C_settle:.0f}/t; with idea ${cost8:.0f}/t -> RATIO {R8:.2f}; with free drilling ${cost8_nowell:.0f}/t -> {C_settle/cost8_nowell:.2f}")

print("=" * 70)
def verdict(M, R):
    if M < 0.3 or R < 1.1:
        return "DEAD"
    if M >= 1 and R >= 1.5:
        return "ALIVE"
    return "WOUNDED"
for i, (M, R) in enumerate([(M1, R1), (M2, R2), (M3, R3), (M4, R4), (M5, R5), (M6, R6), (M7, R7), (M8, R8)], 1):
    print(f"IDEA {i}: MARGIN {M:.3g}  RATIO {R:.3g}  -> {verdict(M, R)}")
