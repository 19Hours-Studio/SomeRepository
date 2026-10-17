# Gate 7 kill test - numeric checks for 8 ideas (python3 -I calc.py)
# Every decisive input carries a source tag; "assume" = engineering assumption stated explicitly.
import math

G = 6.674e-11
RUB_USD = 84.0          # ledger
out = {}

# ---------------------------------------------------------------- IDEA 1
# Coal micro-pits: KILLER = gravity-gradient (Tzz) signal of a one-winter coal lens
# vs the CAP-5 gradiometer's demonstrated 20 E statistical uncertainty
# (Stray et al., Nature 602, 590 (2022): 20 E, 0.5 m spacing, 2 m tunnel at SNR 8, stationary points).
def prism_gz(x1, x2, y1, y2, z1, z2, rho):
    """Vertical attraction (m/s2, +down) at origin of prism; z positive down (Plouff/Nagy)."""
    s = 0.0
    for i, x in enumerate((x1, x2)):
        for j, y in enumerate((y1, y2)):
            for k, z in enumerate((z1, z2)):
                mu = (-1) ** (i + j + k)
                r = math.sqrt(x * x + y * y + z * z)
                s += mu * (z * math.atan2(x * y, z * r) - x * math.log(r + y) - y * math.log(r + x))
    return -G * rho * s

# sanity: wide thin slab -> 2*pi*G*rho*t
slab = prism_gz(-1e5, 1e5, -1e5, 1e5, 10, 13, 1000.0)
assert abs(abs(slab) / (2 * math.pi * G * 1000 * 3) - 1) < 0.01, slab

def lens_tzz(mass_t, rho_coal, thick, ztop, drho, h_lo=0.5, h_hi=1.5):
    area = mass_t / rho_coal / thick
    s = math.sqrt(area) / 2
    g_lo = prism_gz(-s, s, -s, s, ztop + h_lo, ztop + thick + h_lo, drho)
    g_hi = prism_gz(-s, s, -s, s, ztop + h_hi, ztop + thick + h_hi, drho)
    return abs(g_lo - g_hi) / (h_hi - h_lo) / 1e-9, 2 * s   # Eotvos, side length m

noise_E = 20.0                         # Stray 2022, stationary
need_E = 3 * noise_E                   # SNR 3 (tunnel paper needed SNR 8 to localise)
cases = {}
for label, m, drho, zt in [("one-winter lens, idea's own contrast (host 2.70)", 3000, -1350, 3.0),
                           ("one-winter lens, Lena-basin sandstone host 2.30", 3000, -950, 3.0),
                           ("3-winter lens 10 kt, host 2.30", 10000, -950, 3.0),
                           ("one-winter lens at 6 m, host 2.30", 3000, -950, 6.0)]:
    tzz, side = lens_tzz(m, 1.35, 3.0, zt, drho)
    cases[label] = (round(tzz, 1), round(side, 1), round(tzz / need_E, 2))
out["1_killer"] = cases

# CHAIN idea 1 (ledger C settlement 23,000 rub/t at boiler, outbound 85%)
now1 = 23000.0
t_yr = 3000.0                                      # "a few thousand tonnes each winter"
exc_capex = 45e6                                   # assume: 30-t arctic excavator + hammer + autonomy/vision kit (~$540k)
crf = 0.12 / (1 - 1.12 ** -8)                      # 12%, 8 yr
c = {}
c["excavator capital"] = exc_capex * crf / t_yr
c["fuel 20 l/h x 1500 h @130 rub/l"] = 20 * 1500 * 130 / t_yr     # ledger remote diesel 120-150 rub/l
c["repairs/wear 15%/yr of capex"] = 0.15 * exc_capex / t_yr
c["tech visits 2 x 5/12 x 5 M rub"] = 2 * 5 / 12 * 5e6 / t_yr       # ledger FIFO 5 M rub/worker-yr
c["gravity survey share"] = 1.5e6 / t_yr
c["short winter haul 20 km x 20 rub/t-km + loading"] = 20 * 20 + 100   # ledger winter road 20 rub/t-km
c["moves, licence, ash tests"] = 300
c["MET/other (ledger 1.5%)"] = 0.015 * now1
sub = sum(c.values())
with1 = sub * 1.10                                  # assume +10% tonnes for unwashed higher-ash coal
out["1_chain"] = {k: round(v) for k, v in c.items()}
out["1_chain_total"] = (round(with1), round(now1 / with1, 2))

# ---------------------------------------------------------------- IDEA 2
# Thaw-bowl leach: KILLER = annual flush water vs water needed to carry the copper out in a mine life
P = 0.346            # m/yr precipitation, Anadyr basin (bigenc.ru) - all of it counted, rain too
fence = 2.0          # assume generous drift-capture multiplier, zero sublimation/evaporation
avail2 = P * fence
D, rho_r, grade, rec, life = 30.0, 2.7, 0.004, 0.60, 25.0   # "tens of metres"; 0.4% Cu porphyry-type; 60% leach rec.
Cu_m2 = D * rho_r * 1000 * grade * rec        # kg recoverable Cu per m2
res2 = {}
for C in (1.0, 3.0, 8.0):                      # PLS g/L = kg/m3; dump/heap range 0.5-8 g/L (911metallurgist SX training)
    req = Cu_m2 / life / C
    res2[C] = (round(req, 2), round(avail2 / req, 2))
out["2_killer"] = {"Cu_kg_m2": round(Cu_m2), "avail_m_yr": avail2, "req_m_yr,margin by PLS g/L": res2}

# CHAIN idea 2 at the water-limited rate (3 g/L)
rate = avail2 * 3.0                             # kg Cu/m2/yr
years = Cu_m2 / rate
db = D * rho_r * 0.6                            # $/m2 drill&blast in place, assume $0.6/t (Arctic x2 of ~$0.3)
ann = 0.10 / (1 - 1.10 ** -years)               # capital recovery at 10% over the leach life
c2 = {}
c2["blasting capital"] = db * ann / rate * 1000
c2["geotextile+fences $0.5/m2/yr"] = 0.5 / rate * 1000
c2["scrap iron 2 t/t Cu x ($350 + NSR 16k rub/t + 200 km road)"] = 2 * (350 + 16000 / RUB_USD + 200 * 0.24)
c2["seasonal crew 20 workers/km2"] = 20 * 60000 / (rate * 1e6) * 1000
c2["ship cement Cu (concentrate outbound $425/t / 3.4)"] = 0.05 * 8500 / 3.4
c2["smelt/refine cement copper"] = 400
c2["other/MET (ledger 14%)"] = 0.14 * 8500
w2 = sum(c2.values())
out["2_chain"] = {k: round(v) for k, v in c2.items()}
out["2_chain_total"] = (round(w2), round(8500 / w2, 2), round(years), round(2500 / w2, 2))

# ---------------------------------------------------------------- IDEA 3
# Floating concentrator: KILLER = module draft vs guaranteed depth of the waterway to the deposit
tph = 10e6 / (8760 * 0.92)
slurry_m3h = tph / 0.35 / 1.30
mass = {
    "mills shells+drives (3 x 1200 t)": 3600,
    "SAG charge (576 m3 x 0.30 x 4.0)": 576 * 0.30 * 4.0,
    "2 ball-mill charges (485 m3 x 0.35 x 4.6)": 2 * 485 * 0.35 * 4.6,
    "flotation slurry (0.5 h x 1.2 / 0.85 holdup)": slurry_m3h * 0.5 * 1.2 / 0.85 * 1.3,
    "flotation cell steel": 1000,
    "pumps, crushers, conveyors, regrind": 3000,
    "enclosed heated superstructure steel": 6000,
}
payload = sum(mass.values())
displ = payload / 0.65                                 # hull lightship ~35% of displacement (assume)
draft_30 = displ / (150 * 30 * 1.0)                    # Lomonosov-like 30 m beam, 150 m long
draft_40 = displ / (150 * 40 * 1.0)
lomonosov = 21500 / (144.4 * 30)                       # 21,500 t, 144.4 x 30 m, draft 5.6 m (Wikipedia/WNN)
req3 = 5.6 + 0.4                                       # Lomonosov-class draft + 0.4 m under-keel
avail3 = 2.5                                           # guaranteed depth ~2.0-3.0 m on Siberian river reaches (Mintrans 2025: 230 cm = guaranteed +30 cm)
out["3_killer"] = {"tph": round(tph), "payload_t": round(payload), "displ_t": round(displ),
                   "draft_30m_beam": round(draft_30, 1), "draft_40m_beam": round(draft_40, 1),
                   "Lomonosov block-draft check": round(lomonosov, 2),
                   "required_m": req3, "available_m": avail3, "margin": round(avail3 / req3, 2)}
# CHAIN idea 3 (ledger B: $8,500/t Cu gross, capital 41%)
cap = 0.41 * 8500
conc_share = 0.40          # assume generous: concentrator+its civils 40% of capex (TSF, pit, power, road, port, camp excluded)
cut = 6.5                  # idea's claimed 5-8x on the concentrator
saving = cap * conc_share * (1 - 1 / cut)
added = 0.01 * 8500        # assume: dredged basin, towing, ice/open-water ops, marine crew ~1%
w3 = 8500 - saving + added
out["3_chain"] = (round(saving), round(w3), round(8500 / w3, 2))

# ---------------------------------------------------------------- IDEA 4
# Under-ice packets: KILLER = packet drift speed vs claimed 25-50 km/day
req4 = 25e3 / 86400                       # m/s lower bound of claim
rho_w, Cd, A = 1000.0, 1.0, 1.0           # 1 t sack ~1 m3 bluff body
Nb = 0.01 * 1000 * 9.81 * 1.0             # "slightly lighter": 1% net buoyancy pressed on ice
res4 = {}
for label, u, mu, f in [("main channel 0.15 m/s (0.12-0.18), mu 0.03, near-ice 0.8", 0.15, 0.03, 0.8),
                        ("main channel 0.15, mu 0.01, near-ice 0.8", 0.15, 0.01, 0.8),
                        ("best channel 0.25 (Bykovskaya), mu 0.01, no shear loss", 0.25, 0.01, 1.0),
                        ("water itself, main channel, zero friction", 0.15, 0.0, 1.0)]:
    slip = math.sqrt(2 * mu * Nb / (rho_w * Cd * A))
    v = max(0.0, u * f - slip)
    res4[label] = (round(v, 3), round(v * 86.4, 1), round(v / req4, 2))
out["4_killer"] = {"required_m_s": round(req4, 3), "cases(v m/s, km/day, margin)": res4}
# CHAIN idea 4 (ledger C settlement: barge leg ~8,000 rub/t replaced; winter-road last miles run on small
# rivers that freeze to the bed, so they stay)
pk = {"sack+bladder+sensor+valve $150 / 5 trips": 30, "gas cartridges": 10, "bagging": 5,
      "ice slots in/out + net": 5, "lift 1-t wet sacks at -40C": 10, "unbag": 3, "return empties": 4, "losses": 5}
pk_rub = sum(pk.values()) * RUB_USD
w4 = 23000 - 8000 + pk_rub
w4b = 23000 - 8000 - 6000 + pk_rub          # generous: also replaces a 300-km river-ice winter road
out["4_chain"] = (round(pk_rub), round(w4), round(23000 / w4, 2), round(23000 / w4b, 2))

# ---------------------------------------------------------------- IDEA 5
# Freeze cascade: KILLER = net cooling flux at the eutectic vs flux to freeze a shallow tray in one night
h, c0, kB = 6.626e-34, 2.998e8, 1.381e-23
def band(T, l1=8e-6, l2=13e-6, n=4000):
    s = 0.0
    dl = (l2 - l1) / n
    for i in range(n):
        l = l1 + (i + 0.5) * dl
        s += 2 * h * c0 ** 2 / l ** 5 / (math.exp(h * c0 / (l * kB * T)) - 1) * dl
    return math.pi * s        # W/m2 hemispherical
Tt, Ta = 273.15 - 52, 273.15 - 45          # tray just past eutectic (-49.8 C), air mid of idea's -40..-50
tau = 0.85                                  # assume PE-type IR windshield transmittance in 8-13 um
eps_w = 0.10                                # assume very dry winter sky window emissivity (upper-bound case 0)
h_par = 2.0                                 # assume W/m2K residual air coupling through windshield
emit = tau * band(Tt)
shield = (1 - tau) * band(Ta)
sky = tau * eps_w * band(Ta)
par = h_par * (Ta - Tt)
avail5_ub = emit - shield                   # perfect sky, no parasitic gain
avail5 = emit - shield - sky - par
dH = 0.412 * 223e3 + 0.588 * 150e3          # J/kg eutectic solid: ice 41.2% + CaCl2.6H2O 58.8% (29.8 wt% CaCl2 eutectic)
rho_b = 1280.0
layer, night = 0.01, 16 * 3600
req5 = layer * rho_b * dH / night
out["5_killer"] = {"band(221K)": round(band(Tt), 1), "sigmaT4(221K)": round(5.67e-8 * Tt ** 4, 1),
                   "avail_upper_bound": round(avail5_ub, 1), "avail_realistic": round(avail5, 1),
                   "dH_kJ_kg": round(dH / 1e3), "req_W_m2_1cm_16h": round(req5, 1),
                   "margin_realistic": round(avail5 / req5, 2), "margin_upper_bound": round(avail5_ub / req5, 2)}
# CHAIN idea 5 (ledger D: $10,200/t LCE)
cold_h = 500                                # assume generous hours/yr with air <= -45 C on the Siberian Platform
for flux in (avail5, avail5_ub):
    q_m2 = flux * cold_h * 3600             # J/m2/yr
    brine = q_m2 / (rho_b * dH)             # m3/m2/yr
    lce = brine * 0.30 * 5.323 * 0.5        # kg LCE/m2/yr: 0.3 g/L Li, 50% recovery (crust entrainment)
    m2_per_t = 1000 / lce
    cost = m2_per_t * (11 * 0.15 + 1.0)     # $11/m2 capex @15%/yr + $1/m2/yr windshield replacement
    cost += 0.6 * 10200                     # downstream Li plant + rest of chain (capital/processing/other ~60% of D)
    out.setdefault("5_chain", []).append((round(flux, 1), round(m2_per_t), round(cost), round(10200 / cost, 3)))

# ---------------------------------------------------------------- IDEA 6
# Winter railway: KILLER = river-ice capacity for the lightest mainline diesel vs available ice
A_safe = 3.5            # kg/cm2, Gold (1971) P = A h^2 lower (safe) value; 7 = short-term upper
P_loco = 2 * 138e3      # kg, 2TE116 two-section diesel, 2 x 138 t, 23 t/axle
h_nat = 130             # cm, mean end-of-winter natural ice, Lena at Tabaga 1.2-1.4 m (MSU Lomonosov-2017)
h_flood = 100           # cm, assume generous flooded layer
h_eff = h_nat + 0.65 * h_flood            # Russian ice-crossing rule h = h_est + 0.65 h_nal
h_req = math.sqrt(P_loco / A_safe)
out["6_killer"] = {"h_req_cm(A=3.5)": round(h_req), "h_req_cm(A=7)": round(math.sqrt(P_loco / 7)),
                   "h_eff_cm": h_eff, "margin(A=3.5)": round(A_safe * h_eff ** 2 / P_loco, 2),
                   "margin(A=7)": round(7 * h_eff ** 2 / P_loco, 2),
                   "margin season start 80 cm natural": round(A_safe * 80 ** 2 / P_loco, 2)}
# CHAIN idea 6 (ledger C export; best practice for a remote deposit = own all-season railway + own port,
# Elga ~$12/t vs $46/t RZD -> delivered 83-46+12 = $49/t FOB)
now6 = 83 - 46 + 12
own = {"rail capital": 7.2, "port": 3.0, "rail ops": 1.8}           # assume split of the $12/t
win = {"rail capital /4": 7.2 / 4, "re-level+snow $30k/km/yr, 531 km, 30 Mt": 30e3 * 531 / 30e6,
       "ops+fleet x1.6 (same tonnage in 5.5 months)": 1.8 * 1.6, "6-7 month stockpiles, double handling": 1.5,
       "port": 3.0}
w6 = now6 - sum(own.values()) + sum(win.values())
out["6_chain"] = (now6, round(sum(win.values()), 2), round(w6, 1), round(now6 / w6, 2))

# ---------------------------------------------------------------- IDEA 7
# Kimberlite magnet: KILLER = ore throughput one open-gradient coil can treat vs a pit's ore stream
req7 = 4.0e6 / 7000                  # t/h; Lomonosov GOK plant 1 + 3 Mt/yr modules (Rapaport/IDEX)
per_m = 30.0                         # t/h per metre of magnet length, theoretical, no plant experience (IIR record 9379)
L = 3.0                              # assume generous usable length of one 20-T coil face
avail7 = per_m * L
out["7_killer"] = {"required_t_h": round(req7), "available_t_h": avail7, "margin": round(avail7 / req7, 2)}
# CHAIN idea 7: on-mine split mining 67 / processing 27 / G&A 6 (Lace FS, Engineering News 2015);
# assume on-mine opex = 75% of delivered cost; ore haul = 15% of mining; crushing = 30% of processing (still needed)
onmine = 0.75
proc, haul = 0.27 * onmine, 0.67 * 0.15 * onmine
shrink = 3.0                         # "several-fold"
saving7 = proc * 0.70 * (1 - 1 / shrink) + haul * (1 - 1 / shrink)
add7 = 0.03                          # assume: coils, cryocoolers, X-ray counters, pit-rim dry crushing station
w7 = 1 - saving7 + add7
out["7_chain"] = (round(saving7, 3), round(w7, 3), round(1 / w7, 2))

# ---------------------------------------------------------------- IDEA 8
# Pressure-cell mats: KILLER = thaw settlement under a heated building on grade over its life vs cell stroke
def thaw_depth(years, R=5.2, k=1.4, dT=20.0, ice=0.40, Tg=4.0):
    Lv = ice * 917 * 334e3 + 2.0e6 * Tg          # J/m3: latent of pore/excess ice + warming frozen ground 4 K
    t = years * 3.156e7
    return k * (-R + math.sqrt(R * R + 2 * dT * t / (Lv * k)))
res8 = {}
for R in (5.2, 10.2):                    # floor R ~5 m2K/W (northern code level, assume) + 0.2 air cells; 10 = super-insulated
    X = thaw_depth(20, R=R)
    res8[R] = (round(X, 1), round(0.2 * X, 2), round(1.0 / (0.2 * X), 2))   # thaw strain 0.2 (ice-rich), stroke 1.0 m
out["8_killer"] = res8
# CHAIN idea 8 (ledger B): zero-cycle >=40% of construction cost (Ekspozitsiya Neft Gaz via runeft.ru);
# assume buildings & structures 35% of capex, idea saves 70% of zero cycle (mill/crusher plinths still needed)
s8 = 0.41 * 0.35 * 0.40 * 0.70
sched = 0.41 * 0.05                       # assume faster build trims 5% of capital (IDC)
w8 = 1 - s8 - sched
out["8_chain"] = (round(s8, 3), round(w8, 3), round(1 / w8, 2))

for k, v in out.items():
    print(k, "=>", v)
