"""Idea 4 - Docked multi-year bunker hull (sealed river hull = coal store + boiler room).
Sources: IMSBC/P&I (West, Britannia): coal is O2-depleting cargo, CO monitoring, avoid ventilation;
storage limits for oxidation-prone coals ~6 months in open stockpiles (enterprise rules citing RD 34.44.101-86);
Dec-2025 coal shortfalls in 6 Yakutian districts (Moscow Times / iStories). [est] = estimate.
"""
import numpy as np
print("=== IDEA 4: bunker hull ===")
# --- capacity vs burn ---
L, B = 130.0, 22.0             # dumb barge hull [est for ~8 kt dwt]
dwt, light = 8000.0, 1500.0
hold_m3 = dwt * 1.15           # m3/t typical river dry-cargo [est]
for rho in (0.80, 0.90):
    cap = min(dwt, hold_m3 * rho)
    print(f"coal bulk {rho} t/m3: capacity {cap:.0f} t -> {cap/3500:.1f}-{cap/2000:.1f} winters at 2,000-3,500 t/yr")
print(f"light draught {light/(L*B*1.0):.2f} m, loaded {(light+dwt)/(L*B*1.0):.2f} m")

# --- Round 1 floating, frozen-in: buoyancy change as coal is burned over winter ---
burn = 3000.0
rise = burn / (L * B)
P = burn * 1e3 * 9.81 / (2 * (L + B))           # N/m along perimeter
h_ice, E = 1.8, 5e9
lc = (E * h_ice**3 / (12 * 0.91 * 1000 * 9.81)) ** 0.25
M = 0.32 * P * lc; sig = 6 * M / h_ice**2
print(f"winter burn {burn:.0f} t -> hull wants to rise {rise:.2f} m; line load {P/1e3:.0f} kN/m; "
      f"ice bending stress {sig/1e6:.1f} MPa vs ice flexural 0.5-0.8 MPa -> ice cracks along hull (no hull damage)")
# thermal ice pressure in confined basin 100-300 kN/m [lit. range] -> moat needed if floating
moat_kW = 0.5 * 2 * (L + B) * 500 / 1e3
boiler_MW = burn * 21e9 * 0.7 / (0.6 * 3.156e7) / 1e6
print(f"open moat 0.5 m wide at 500 W/m2: {moat_kW:.0f} kW = {moat_kW/1e3/boiler_MW*100:.1f} % of mean boiler output {boiler_MW:.1f} MW")

# --- Round 2 dewatered dock: hull rests on gravel pad ---
q = (dwt + light) * 9.81 / (L * B)
print(f"hull on gravel pad: {q:.0f} kPa bearing (thaw-stable gravel allows >200 kPa)")

# --- self-heating: O2 budget of a sealed hold ---
void = 0.40
air = hold_m3 * void + 1000                      # voids + headspace
O2_kg = air * 0.21 * 1.43
heat_total = O2_kg * 13e6                       # J per kg O2 consumed (~400 kJ/mol)
dT_bulk = heat_total / (dwt * 1e3 * 1.2e3)
breathe = 0.057 * air                            # m3/day (10 K diurnal + 2 % baro)
O2_in = breathe * 0.21 * 1.43
print(f"sealed hold: initial O2 {O2_kg/1e3:.1f} t -> if all consumed, bulk heating {dT_bulk:.1f} K")
print(f"breathing ingress {breathe:.0f} m3/day -> {O2_in:.0f} kg O2/day -> {O2_in*13e6/86400/1e3:.0f} kW mean heat")
for O2frac in (0.21, 0.06, 0.01):
    print(f"  make-up gas O2 {O2frac*100:.0f} %: O2 ingress {breathe*O2frac*1.43:.0f} kg/day")
# fresh coal unsealed O2 uptake ~1e-10 mol/g/s at 20-30 C [order of magnitude, lit.] -> would consume
rate = 1e-10 * dwt * 1e6 * 32 / 1000 * 86400
print(f"fresh-coal O2 demand if ventilated ~{rate/1e3:.1f} t O2/day -> sealed hold is O2-limited within ~"
      f"{O2_kg/rate*24:.0f} h")

# --- economics per tonne burned (2025 rub) ---
base = 8080.0  # rub/t delivered chain (from idea; unverified)
removed = {"transshipment barge->shore": (400, 800), "shore stockpile + losses 3-8%": (250, 650),
           "trucking + loader to boiler house": (300, 900)}
lo = sum(v[0] for v in removed.values()); hi = sum(v[1] for v in removed.values())
print(f"\nremoved cost items: {lo}-{hi} rub/t = {lo/base*100:.0f}-{hi/base*100:.0f} % of {base:.0f}")
# freight optimisation: deliver only full loads in high-water years (low water forces 50-70 % loading)
freight = 3500.0
fr_save = (0.10, 0.25)
print(f"freight saving from full-load/high-water-only deliveries: {freight*fr_save[0]:.0f}-{freight*fr_save[1]:.0f} rub/t")
# failure insurance: p(failed delivery) x fraction short x emergency premium
for p in (0.05, 0.15):
    print(f" expected emergency cost avoided p={p}: {p*0.5*25000:.0f} rub/t")
# capital per village
for burn_t, hull, dock, kit in ((3000, 45e6, 30e6, 40e6), (3000, 45e6, 30e6, 0.0), (6000, 45e6, 30e6, 40e6)):
    crf = 0.12 / (1 - 1.12 ** -20)
    ann = (hull + dock + kit) * crf + 3e6
    print(f" burn {burn_t} t/yr, hull {hull/1e6:.0f}+dock {dock/1e6:.0f}+boiler/conveyor {kit/1e6:.0f} M: "
          f"{ann/burn_t:.0f} rub/t annualised (kit=0 means boiler-house rebuild is due anyway)")
# alternative: purpose-built closed coal warehouse for 8 kt in the Arctic [est 150-250 M rub]
for wh in (150e6, 250e6):
    print(f" closed warehouse {wh/1e6:.0f} M -> {wh*crf/3000:.0f} rub/t at 3 kt/yr")
