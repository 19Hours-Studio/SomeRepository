# Kill-test calculations for the 6 ideas (gate_r1_1). All money in USD unless noted.
# (src) = sourced input, (ledger) = TASK.md value ledger, (est) = screening estimate, (idea) = as written.
import math

RUB = 84.0                      # RUB/USD (ledger)
G_OZ = 31.1035
CRF = lambda r, n: r / (1 - (1 + r) ** -n)
crf7 = CRF(0.15, 7)             # small/mobile kit, 15 %/yr, 7 yr (est)
crf15 = CRF(0.15, 15)           # dredge hull, 15 yr (est)
POST = 2 * 60_000               # $/post-yr: ~$60k per worker-yr, ~2 workers per post (ledger)
P_KWH = 0.49                    # $/kWh mine-scale diesel power (ledger)
DIESEL = 1.6                    # $/l remote-site diesel (ledger 1.4-1.8)

# ---------- Archetype A placer split (ledger) ----------
A_OZ = 2550.0
A_G = A_OZ / G_OZ                                  # 81.98 $/g
T = 0.22 * A_G                                     # MET/taxes/other, unchanged by any idea
E = (2 / 3) * (1 - 0.22) * A_G                     # earthmoving (diesel, fleet, operators) ~2/3 of physical
W = (1 - 0.22) * A_G - E                           # washing, camp, admin, other physical
L_PER_G = 11.0                                     # diesel l/g (ledger)
L_PER_M3 = 1.5                                     # (est) whole-cycle diesel per m3 moved, frozen open cut
V_OC = L_PER_G / L_PER_M3                          # m3 moved per g
C_OC = E / V_OC                                    # $/m3 moved (earthmoving)
SR = 18.0                                          # mid of 6-30 stripping ratio (idea 1 text)
OC_PER_M3_PAY = (SR + 1) * C_OC
print(f"A: {A_G:.2f} $/g = E {E:.2f} + W {W:.2f} + T {T:.2f}; open cut {C_OC:.2f} $/m3 moved, "
      f"{OC_PER_M3_PAY:.1f} $/m3 pay; implied pay grade {(SR+1)/V_OC:.2f} g/m3")

def ratio(new_g):
    return A_G / new_g

# ---------- IDEA 1 Borehole bell ----------
print("\nIDEA 1")
A_bell = math.pi * 7.5 ** 2
t_pay, rho = 2.0, 2.1                              # m pay (est), t/m3 frozen gravel (est)
V_pay = A_bell * t_pay
tons = V_pay * rho
hole = math.pi * 0.3 ** 2 * 40                     # 0.6 m x 40 m (mid of 20-60) (idea)
print(f" bell {V_pay:.0f} m3 pay ({tons:.0f} t); hole/pay volume {hole/V_pay:.3f} (idea claims ~0.04)")
rate_avail = 9.0                                   # t/h, USBM/NIOSH TN-460 prototype, -4 C permafrost (src)
avail = 0.85
fixed = 6 * POST + 3.5e6 * (crf7 + 0.10)           # 6 posts; rig+cutter+airlift+compressors $3.5M (est)
hourly = fixed / (8760 * avail) + 340 * P_KWH      # 340 kW (est)
t_fixed = 40 / 3.0 + 12                            # drill 3 m/h + move/deploy 12 h (est)
bits = 40 * 100
cost_bell = (t_fixed + tons / rate_avail) * hourly + bits
bell_m3 = cost_bell / V_pay
E1 = E * bell_m3 / OC_PER_M3_PAY
new1 = E1 + W + T
budget = OC_PER_M3_PAY * V_pay - bits
rate_req = tons / (budget / hourly - t_fixed)
print(f" spread {hourly:.0f} $/h; bell {cost_bell/1e3:.1f} k$ = {bell_m3:.0f} $/m3 pay vs open cut {OC_PER_M3_PAY:.0f}")
print(f" KILLER rate required {rate_req:.1f} t/h, available {rate_avail} -> MARGIN {rate_avail/rate_req:.2f}")
print(f" CHAIN now {A_OZ:.0f} $/oz, idea {new1*G_OZ:.0f} $/oz -> RATIO {ratio(new1):.2f}")
print(f" halving claim needs E' <= {A_G/2 - W - T:.1f} $/g; fixed drill/move alone = "
      f"{(t_fixed*hourly+bits)/V_pay*E/OC_PER_M3_PAY:.1f} $/g")

# ---------- IDEA 2 Borehole slurry coal ----------
print("\nIDEA 2")
r_req, r_av = 17.5, 8 * 0.3048                     # 15-20 m (idea); 8 ft rotating jet in coal, RI 8095 (src)
rho_c = 1.3
h_seam = 5000 / (math.pi * r_req ** 2 * rho_c)     # seam implied by "150 m hole yields ~5,000 t"
y_av = math.pi * r_av ** 2 * h_seam * rho_c
print(f" implied seam {h_seam:.1f} m; yield at {r_av:.2f} m = {y_av:.0f} t; drilled m/t {150/y_av:.2f} vs 0.03")
print(f" KILLER MARGIN {r_av/r_req:.2f}")
Q = 20_000                                         # t/yr settlement demand (est)
drill_rub_m = 20_000                               # rub/m, ~300 mm hole, remote Yakutia (est)
def coal_cost(m_per_t):
    drill = m_per_t * drill_rub_m
    energy = 25 * 41                               # 25 kWh/t jet+airlift+dewater (est) x 41 rub/kWh (ledger)
    labour = 5 * 2 * 5e6 / Q                       # 5 posts x 2 x 5 M rub (ledger)
    capex = 250e6 * (crf7 + 0.10) / Q              # rig, HP pump, compressor, dewatering 250 M rub (est)
    dry = 500                                      # fines drying/handling (est)
    kept = (0.03 + 0.015) * 23_000                 # boiler-side processing + other (ledger shares)
    return drill + energy + labour + capex + dry + kept
c2 = coal_cost(0.03)
c2a = coal_cost(150 / y_av)
print(f" CHAIN now 23000 rub/t, idea {c2:.0f} rub/t -> RATIO {23000/c2:.2f}; at available radius {c2a:.0f} -> {23000/c2a:.2f}")

# ---------- IDEA 3 Under-ice regold ----------
print("\nIDEA 3")
g_av = 0.19                                        # g/m3 free gold, Far-East dredge tailings, 83% <0.5 mm (src)
rec = 0.65                                         # centrifugal concentrator recovery on fine gold (est)
Qm3 = 100 * 7000                                   # 100 m3/h x 7000 h/yr year-round (est)
plant = (350 * P_KWH * 7000 + 4 * POST + 2.5e6 * (crf7 + 0.10)) / Qm3   # 350 kW incl. heating (est)
W3 = W / 2                                         # washing done on board; camp/admin/logistics kept
new3 = plant / (g_av * rec) + W3 + T
g_req = plant / (A_G - W3 - T) / rec
print(f" plant {plant:.2f} $/m3; KILLER grade required {g_req:.3f} g/m3, available {g_av} -> MARGIN {g_av/g_req:.2f}")
print(f" CHAIN idea {new3*G_OZ:.0f} $/oz -> RATIO {ratio(new3):.2f}")
for r_ in (0.55, 0.75):
    print(f"  recovery {r_}: RATIO {ratio(plant/(g_av*r_)+W3+T):.2f}")

# ---------- IDEA 4 Basal-slot robots ----------
print("\nIDEA 4")
hg, hb, s = 0.91, 0.38, 0.2                        # paying gravel 3 ft + bedrock 1.25 ft (Yukon report) (src)
f_g = (3 * s - s * s / hg) / (3 * hg - hg)         # linear 3:1 enrichment toward the contact (est)
f_b = (3 * s - s * s / hb) / (3 * hb - hb)
share_uniform = 0.4 / (hg + hb)
share = 0.75 * f_g + 0.25 * f_b                    # 75 % of gold in gravel, 25 % in bedrock (est)
print(f" share uniform {share_uniform:.2f}, enriched {share:.2f}; KILLER MARGIN {share/0.60:.2f} (req 0.60)")
rob_m3 = ((6 * 0.8e6 + 1.5e6 + 2.0e6) * (crf7 + 0.10) + 8 * POST) / 100_000 + 10 * P_KWH   # (est)
fall = 16.5                                        # volume per g falls 13-20x (idea)
E4 = E * (rob_m3 / C_OC) / fall
new4 = E4 + W + T
E4a = E4 * 0.70 / share
print(f" robots {rob_m3:.1f} $/m3; CHAIN idea {new4*G_OZ:.0f} $/oz -> RATIO {ratio(new4):.2f}; "
      f"at available share {ratio(E4a+W+T):.2f}")

# ---------- IDEA 5 Collier ships ----------
print("\nIDEA 5")
draft = 12.2                                       # m, modern Supramax design draft (src)
depth_at_seam = 0.0                                # Amaam North seam 35 km inland; ships anchor ~2 nmi off (src)
print(f" KILLER MARGIN {depth_at_seam/draft:.2f}")
C_FOB, out = 83.0, 0.55 * 83.0                     # ledger
own = 12.0                                         # own short rail/road + port, ledger (Elga) best practice
now5 = C_FOB - out + own
ship = 5 * 20_336 / 50_000                         # 5 days x BSI $20,336/day (31 Jul 2026) (src)
new5 = now5 - own + ship
print(f" CHAIN now {now5:.2f} $/t, idea {new5:.2f} $/t -> RATIO {now5/new5:.2f}; vs RZD chain {C_FOB/new5:.2f}")

# ---------- IDEA 6 Talik dredging ----------
print("\nIDEA 6")
talik = 80.0                                       # m best-estimate (91 m TEM), thermokarst lake (src)
req6 = 40 + 2                                      # deepest claimed pay + 2 m pay (idea, est)
print(f" KILLER MARGIN lakes {talik/req6:.2f}")
X = math.sqrt(2 * 2.0 * 4.0 * 40 * 3.156e7 / (334e3 * 1000 * 0.30))   # Stefan thaw under 40-yr reservoir (est)
mean_depth = 14.56e9 / 441e6                       # Kolyma reservoir volume/area (src)
print(f" reservoir check: thaw {X:.1f} m in 40 yr; mean water depth {mean_depth:.0f} m leaves {45-mean_depth:.0f} m of reach")
# open-water heat loss at -40 C, 5 m/s (bulk formulas)
rho_a, cp, Ch, U, dT = 1.51, 1004, 1.5e-3, 5.0, 40.0
q_s = rho_a * cp * Ch * U * dT
q_l = rho_a * 2.5e6 * Ch * U * (0.622 * 611 / 101300 - 0.622 * 12.8 / 101300)
q_r = 0.97 * 5.67e-8 * 273.15 ** 4 - 0.7 * 5.67e-8 * 233.15 ** 4
q = q_s + q_l + q_r
heat_kwh = 3000 * q * (32 / 40) * 150 * 24 / 1000  # 3000 m2 open water, 150 d at mean -32 C (est)
Qd = 300 * 7000                                    # m3/yr (est)
heat_m3 = heat_kwh / (10 * 0.85) * DIESEL / Qd
dredge = (750 * P_KWH * 7000 + 10 * POST + 25e6 * (crf15 + 0.05)) / Qd + heat_m3   # $25M deep dredge (est)
korzun = 35.82 * 2.5 / RUB + heat_m3               # 35.82 rub/m3 extended-season dredging (src) x2.5 escal. (est)
vol_g = V_OC * (25 - 4 + 2) / 2 / (SR + 1)         # column below 4 m of lake water to 2 m pay at 25 m (est)
new6 = dredge * vol_g + W / 2 + T
print(f" heat loss {q:.0f} W/m2 -> {heat_m3:.2f} $/m3; dredge {dredge:.2f} $/m3 (Korzun-based {korzun:.2f}); {vol_g:.2f} m3/g")
print(f" CHAIN idea {new6*G_OZ:.0f} $/oz -> RATIO {ratio(new6):.2f}; Korzun-based {ratio(korzun*vol_g+W/2+T):.2f}")
