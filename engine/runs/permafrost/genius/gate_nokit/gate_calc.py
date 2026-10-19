"""Kill-test screening calculations for the 8 permafrost ideas (KILLER margin + CHAIN ratio)."""
import math

RUB_USD = 84.0
OZ = 31.1035
print("=" * 70)

# ---------- shared gold chain (Archetype A ledger) ----------
A_DELIV = 6900.0            # rub/g delivered (ledger)
OTHER = 0.22                # MET/taxes/other share
STEP_SHARE = (2 / 3) * (1 - OTHER)   # earthmoving+washing ~2/3 of physical cost
S_LEDGER = A_DELIV * STEP_SHARE
N_GOLD = A_DELIV - S_LEDGER          # non-mining chain cost (taxes, camp, logistics, G&A...)
print(f"Gold: step share {STEP_SHARE:.3f}, step {S_LEDGER:.0f} rub/g, non-step N {N_GOLD:.0f} rub/g")
price_rub_g = 4150 / OZ * RUB_USD
met = 0.06 * price_rub_g + 0.10 * (4150 - 1900) / OZ * RUB_USD
print(f"  check: Au price {price_rub_g:.0f} rub/g, MET+NDD-like {met:.0f} rub/g (ledger other 22% = {0.22*A_DELIV:.0f})")


def gold_chain(name, idea_step, alt_step):
    now = N_GOLD + alt_step
    w = N_GOLD + idea_step
    print(f"  {name}: now {now:.0f} rub/g, with idea {w:.0f} rub/g, RATIO {now/w:.2f}")
    return now, w, now / w


# ================= IDEA 1: under-ice talik crawler =================
print("\nIDEA 1 - fines containment under ice")
fines_t_d = 540.0
V_water = 160e3                 # m3 under ice (idea)
print(f"  idea check: {fines_t_d*1e6/V_water:.0f} mg/L per day uncontained")
# Stokes settling of clay (2 um) in 1 C water
g, drho, mu = 9.81, 1650.0, 1.73e-3
d = 2e-6
vs = g * drho * d**2 / (18 * mu)
H = 3.0                         # m water under ice (lake must be >2 m to have talik)
tau = H / vs / 86400
f_clay = 0.10                   # <2 um share of fines (conservative)
C_per_leak = fines_t_d * 1e6 * f_clay * tau / V_water   # mg/L at 100% leak, steady state
limit = 25.0                    # mg/L EU Freshwater Fish Directive guide value (RU fishery norm is +0.25-0.75 mg/L)
leak_allowed = limit / C_per_leak
leak_actual = 0.20              # 80% curtain efficiency (HK EPD target, ERDC: poorly documented)
print(f"  clay vs {vs*86400:.2f} m/d, residence {tau:.1f} d, C at full leak {C_per_leak:.0f} mg/L")
print(f"  allowed leak {leak_allowed*100:.2f}%  actual {leak_actual*100:.0f}%  MARGIN {leak_allowed/leak_actual:.3f}")
print(f"  steady TSS with 80% curtain: {C_per_leak*leak_actual:.0f} mg/L")
gold_chain("chain", 1600, 1930)

# ================= IDEA 2: wintering coal CHP barge =================
print("\nIDEA 2 - CHP barge")
Pe = 0.3; eta_orc = 0.16; eta_b = 0.80
Q_orc = Pe / eta_orc; fuel = Q_orc / eta_b
reject = Q_orc - Pe
to_village = 1.54 - 0.104 - 0.044
displaced = to_village / 0.65
extra = fuel - displaced
LHV_MWh_t = 5000 * 4.1868e-3 / 3.6     # 5000 kcal/kg -> MWh/t
hours = 1780 * LHV_MWh_t / fuel
print(f"  fuel {fuel:.3f} MW, reject {reject:.3f} MW, to village {to_village:.3f} MW, displaced boiler fuel {displaced:.3f} MW")
print(f"  net extra fuel {extra:.3f} MW = {extra/Pe:.2f} kWh_f/kWh_e; 1780 t lasts {hours:.0f} h ({hours/24:.0f} d)")
coal_rub_t = 23000.0            # ledger settlement coal at boiler
fuel_cost = extra / Pe * coal_rub_t / (LHV_MWh_t * 1000)
print(f"  net extra fuel cost {fuel_cost:.2f} rub/kWh_e (at ledger 23k rub/t)")
print(f"  electric-only fuel at 10k rub/t: {fuel/Pe*10000/(LHV_MWh_t*1000):.1f} rub/kWh (idea says 12.7)")
# killer: ORC net efficiency in CHP (district-heating condensing) mode
eta_avail = 0.17               # AHDB biomass ORC CHP ~17%; 17.24% at 520.9 kWe (community study)
print(f"  KILLER ORC eff required {eta_orc:.2f} available {eta_avail:.2f} MARGIN {eta_avail/eta_orc:.2f}")
# capex sanity vs AHDB UK prices (500 kWe 2.5 MGBP, 1 MWe 4 MGBP)
b = math.log(4 / 2.5) / math.log(2)
capex_gbp = 2.5e6 * (0.3 / 0.5) ** b
print(f"  AHDB-scaled 0.3 MWe capex {capex_gbp/1e6:.2f} MGBP = {capex_gbp*1.33*RUB_USD/1e6:.0f} M rub (idea 132-237)")
crf = 0.171
for cap in (132e6, 237e6):
    print(f"   capex {cap/1e6:.0f} M rub -> {cap*crf/(Pe*1000*hours):.1f} rub/kWh at CRF {crf}")
now = 41.0                      # ledger mine-scale diesel rub/kWh
w = (19 + 32) / 2 + fuel_cost
print(f"  chain 0.3 MWe: now {now} rub/kWh, with {w:.1f}, RATIO {now/w:.2f}")
w1 = 14 + fuel_cost
print(f"  chain 1 MWe: with {w1:.1f}, RATIO {now/w1:.2f}")

# ================= IDEA 3: ice-deck borehole talik mining =================
print("\nIDEA 3 - jet reach")
R_req = 9.0
# Rajaratnam & Beltaos erosion parameter Ec = (u0 d / x) / sqrt(g * (rho_s-rho)/rho * D); scour negligible below ~0.35
u0 = math.sqrt(2 * 6.0e6 / 1000)      # 6 MPa nozzle
dn = 0.025
for D in (0.02, 0.05):
    x_thresh = u0 * dn / (0.35 * math.sqrt(9.81 * 1.65 * D))
    x_eff = u0 * dn / (1.0 * math.sqrt(9.81 * 1.65 * D))
    uc9 = 6.2 * u0 * dn / 9.0
    print(f"  D={D*100:.0f} cm: threshold reach {x_thresh:.1f} m, effective (Ec=1) {x_eff:.1f} m, centreline u at 9 m {uc9:.2f} m/s")
R_avail = 7.5 / 2                      # NIOSH borehole placer miners paired 7.5 m apart
print(f"  available {R_avail} m MARGIN {R_avail/R_req:.2f}; coverage at 18 m grid {math.pi*R_avail**2/324:.2f} vs {math.pi*81/324:.2f}")
gold_chain("chain", (3000 + 4800) / 2, 8800)

# ================= IDEA 4: frozen-roof jet adits =================
print("\nIDEA 4 - face thaw")
E = 107e6                               # J/m3 of pay (idea)
for v in (3.7, 8.0):
    print(f"  advance {v} m/h -> face flux {v/3600*E/1e3:.0f} kW/m2")
nu, Pr, rhocp = 1.6e-6, 11.4, 4.2e6
for U in (3.0, 5.0):
    Re = U * 2.0 / nu
    St = 0.0296 * Re ** -0.2 * Pr ** (-2 / 3)
    h = St * rhocp * U * 3          # x3 roughness (Douglas et al. 2023)
    q = h * 6.0
    print(f"  U={U} m/s: h {h:.0f} W/m2K, q {q/1e3:.0f} kW/m2, thaw {q/E*3600:.2f} m/h")
req_per_m3w = (35 / 360, 45 / 360)
surin = (2.8 / 90, 3.6 / 90)
khrulev = 18 / 360
print(f"  required {req_per_m3w[0]:.3f}-{req_per_m3w[1]:.3f} m3 pay per m3 water; field Surin {surin[0]:.3f}-{surin[1]:.3f}, Khrulev {khrulev:.3f}")
mid_req = sum(req_per_m3w) / 2
print(f"  MARGIN Surin {sum(surin)/2/mid_req:.2f}, Khrulev {khrulev/mid_req:.2f}")
gold_chain("chain", (550 + 660) / 2, (1040 + 1670) / 2)

# ================= IDEA 5: barge auger =================
print("\nIDEA 5 - auger rate")
req = 60.0
avail_1985 = 450 / 8
print(f"  required {req} t/h; 1985 surface auger {avail_1985:.0f} t/h (MARGIN {avail_1985/req:.2f}); Cardox 21.5 t/h (MARGIN {21.5/req:.2f})")
print(f"  hours needed {80000/req:.0f} of {100*24} h season")
handling = (1100 + 3400) / 2      # bank -> boiler transshipment/rehandling/trucking/loss (idea 8 figures)
now = (2800 + 3700) / 2 + handling
w = 1800 + handling
print(f"  chain: now {now:.0f} rub/t at boiler, with {w:.0f}, RATIO {now/w:.2f}")
print(f"  vs long-haul ledger 23000 rub/t at boiler: RATIO {23000/w:.2f}")

# ================= IDEA 6: channel-talik seam dredging =================
print("\nIDEA 6 - cutter rate")
kovin = 4400863 / 66056
kovin_kw = 750
scaled = kovin * 150 / kovin_kw
icr = 0.28 * (150 / 0.7457) * 0.974 ** 6     # Bilgin ICR, P in hp, UCS 6 MPa, RQD 100
req = (46 + 65) / 2
print(f"  Kovin I {kovin:.1f} t/h with {kovin_kw} kW -> {scaled:.1f} t/h at 150 kW; Bilgin ICR {icr:.0f} m3/h")
m1, m2 = scaled / req, icr / req
print(f"  MARGIN Kovin {m1:.2f}, Bilgin {m2:.2f}, geo-mean {math.sqrt(m1*m2):.2f}")
gcal_t = 3.67
idea_g = (730 + 930) / 2
pit_g = idea_g * (1.4 + 2.4) / 2
hand_g = handling / gcal_t
print(f"  chain: now (bank micro-pit) {pit_g+hand_g:.0f} rub/Gcal, with {idea_g+hand_g:.0f}, RATIO {(pit_g+hand_g)/(idea_g+hand_g):.2f}")
print(f"  vs northern delivery ledger 23000 rub/t @5.3 Gcal/t: {23000/5.3:.0f} rub/Gcal, RATIO {23000/5.3/(idea_g+hand_g):.2f}")

# ================= IDEA 7: thermal drift-and-drop =================
print("\nIDEA 7 - water heat balance")
n = 0.30
Q_req = n * 917 * 334e3 + 2.0e6 * 3          # latent + sensible from -3 C
print(f"  required thaw heat {Q_req/1e6:.0f} MJ/m3 pay")
cw = 4.186e6
for W, Tw, eta in ((3, 6, 0.3), (5.5, 8, 0.3), (5.5, 8, 0.5), (8, 10, 0.6)):
    Qa = W * cw * (Tw - 1) * eta
    print(f"  water {W} m3/m3, {Tw} C->1 C, heat use {eta}: {Qa/1e6:.0f} MJ/m3 -> MARGIN {Qa/Q_req:.2f}")
gold_chain("chain", 1930, (2270 + 3980) / 2)

# ================= IDEA 8: wintering barge bunker swap =================
print("\nIDEA 8 - moat + hold heat; chain")
Ta = -38.6                     # Yakutsk January mean
sens = 1.52 * (0 - Ta) ** (1 / 3) * (0 - Ta)     # free convection hot horizontal surface
lw = 0.97 * 5.67e-8 * 273.15 ** 4 - 0.7 * 5.67e-8 * (273.15 + Ta) ** 4
lat = 50.0
q_open = sens + lw + lat
P = 2 * (75 + 14)
moat = 0.3 * P * q_open + P * 2.2 * (-Ta / 2) * 1.5 / 1.0 * 0 + P * 66
hold = 75 * 14 * 1.0 * (2 - Ta)
avail = (2.4 / 0.65) * 0.15 / 3 * 1000        # recoverable 1/3 of ~15% flue loss, kW
req_kw = moat / 1000 + hold / 1000
print(f"  open-water loss {q_open:.0f} W/m2, moat {moat/1e3:.0f} kW, hold {hold/1e3:.0f} kW, required {req_kw:.0f} kW")
print(f"  available recoverable flue heat {avail:.0f} kW, MARGIN {avail/req_kw:.2f}")
now = 23000.0
for avoided in (1100, 2250, 3400):
    w = now - avoided + 1360
    print(f"  avoided {avoided}: with {w:.0f}, RATIO {now/w:.3f}")
