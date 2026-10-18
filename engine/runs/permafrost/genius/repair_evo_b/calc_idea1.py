"""IDEA 1 - Brine-thawed shelf tin dredging.  Anchor: seawater/salt keeps shelf placer unfrozen ->
dredge it with no thawing, stripping or roads.

Sources (WebSearch summaries, 2026-10-18):
 S1 Overduin et al. (AWI, Buor-Khaya Bay, central Laptev): 52 m borehole 800 m offshore, ice-bonded permafrost
    (IBPF) at 28 m b.s.l.; mean IBPF degradation ~3 (3-4) cm/yr; coastal retreat 1-2 m/yr.
 S2 goarctic.ru "Gornodobyvayushchaya promyshlennost arkticheskoy Yakutii": late 1970s RED 'Sevmorolovo' in Vankina
    Bay worked the Chokurdakh coastal-marine tin placer with dredge-lighter 'Gornyak' + onboard concentrator and
    accommodation ship 'Petrodvorets'; summer only (open water); reserves ~19 kt Sn; "first experience unsuccessful".
 S3 drive2.ru eyewitness: work stopped because sea waves disturbed the onboard gravity concentration.
 S4 BIMA bucket-ladder dredge, Nome AK 1986-1990: 36,400 oz first full season (UPI 1988), ~130 koz life, unprofitable.
 S5 ITRI: PT Timah delivered cost $13,708/t Sn (Q1 2010), $22,266/t (2010 avg); Timah deposits 400-500 g/m3,
    dredging+concentrating benchmark < $1.10/m3 (MRT Tasmania EL322001 appendix).
 S6 metalcharts/World Bank: tin 2024 average $30,066/t.
 S7 AWI fast-ice study 1999-2013: SE Laptev has the most extensive landfast ice in the Arctic; breakup Jul.
 K  (textbook values, flagged): winter open-water heat loss 400-700 W/m2 at -30 C (Maykut 1978 leads);
    Tiksi freezing index ~5,500 C*day; Stefan ice growth coefficient 0.027 m/sqrt(C*day) snow-free.
"""
import math

print("=== 1a. Depth to ice-bonded permafrost vs offshore distance (S1 scaling) ===")
rate = 0.035          # m/yr IBPF degradation after inundation (S1: 3-4 cm/yr)
for retreat in (1.0, 2.0):
    for x in (100, 200, 400, 800, 1500, 3000):
        t_inund = x / retreat
        # degradation slows with time (diffusive); use sqrt scaling anchored at S1 point (28 m at 800 m, 1 m/yr)
        z_lin = rate * t_inund
        z_sqrt = 28.0 * math.sqrt(t_inund / 800.0)
        print(f"retreat {retreat} m/yr  x={x:5d} m  inundated {t_inund:6.0f} yr  IBPF linear {z_lin:5.1f} m  sqrt {z_sqrt:5.1f} m")
pay_bottom = 15 + 2   # m below seabed (pay 5-15 m + 2 m dredge overdig)
for retreat in (1.0, 2.0):
    x_lin = pay_bottom / rate * retreat
    x_sqrt = 800 * (pay_bottom / 28.0) ** 2 * retreat
    print(f"min distance offshore for IBPF > {pay_bottom} m (retreat {retreat}): linear {x_lin:.0f} m, sqrt {x_sqrt:.0f} m")

print("\n=== 1b. Season / production: open-water only vs under-landfast-ice ===")
def tin_output(q_m3h, days, grade_kg_m3, rec=0.85, sn_in_cass=0.75):
    vol = q_m3h * 24 * days
    return vol, vol * grade_kg_m3 * rec * sn_in_cass / 1000.0  # t Sn

# open water 80-100 d (idea), storms/waves: BIMA & Sevmorolovo show heavy weather downtime -> 65% availability
ow_days = 90 * 0.65
# under fast ice: ice >= 0.8 m (safe working platform) from ~Dec 1 to fast-ice decay ~Jun 15 = ~195 d; 80% availability
FI_rate = 5500 / 240.0   # C*day per day of freezing season
t_08 = (0.8 / 0.027) ** 2 / FI_rate
print(f"days of freezing to reach 0.8 m sea ice (Stefan, 0.027): {t_08:.0f} d -> start ~mid-Nov/early Dec")
ui_days = 195 * 0.80
print(f"effective days: open water {ow_days:.0f}, under ice {ui_days:.0f}, both {ow_days+ui_days:.0f}")

print("\n=== 1c. Under-ice slot heat balance ===")
# dredge 300 m3/h class: hull ~80 x 20 m; open slot to keep: bucket ladder well + face 40 x 25 m; rest insulated cover
A_open = 40 * 25
A_cov = 120 * 30 - A_open
q_open, q_cov = 550.0, 40.0   # W/m2 (K); insulated floating cover ~40 W/m2
P_heat = A_open * q_open + A_cov * q_cov
P_inst = 3.0e6               # W installed diesel-electric for a 300 m3/h BLD + plant (Timah-class scaled)
waste = P_inst * 0.6 / 0.4 * 0.5   # diesel at 40% eff, 50% recoverable of waste heat at 60% load
print(f"heat needed to hold slot open: {P_heat/1e6:.2f} MW; recoverable diesel waste heat: {waste/1e6:.2f} MW")
# advance: face 40 m wide x (water 6 m + dig 12 m) -> advance per hour
adv = 300 / (40 * 12)
ice_vol_per_m3 = 2.0 * 40 * adv / 300
print(f"advance {adv*24:.1f} m/day; ice to cut ahead {ice_vol_per_m3:.3f} m3 ice per m3 ground "
      f"= {300*ice_vol_per_m3:.0f} m3/h ice (mechanical saw + lift, not melting)")
melt_MJ = ice_vol_per_m3 * 917 * 334e3 / 1e6
print(f"if melted instead: {melt_MJ:.1f} MJ/m3 ground = {melt_MJ*300/3.6:.0f} kW -> {melt_MJ*300/3.6/1000:.1f} MW (> waste heat => saw blocks)")

print("\n=== 1d. Cost per tonne Sn delivered vs best practice ===")
def cost_case(name, q, days, grade, capex, crew, crew_cost, fuel_l_per_m3=1.2, diesel=1.3, extra=0.0, crf=0.147):
    vol, sn = tin_output(q, days, grade)
    cap = capex * crf
    om = 0.05 * capex
    labour = crew * crew_cost
    fuel = vol * fuel_l_per_m3 * diesel
    ship = sn / 0.7 * 400          # $/t concentrate to smelter (Novosibirsk) via Tiksi + rail
    tot = cap + om + labour + fuel + ship + extra
    print(f"{name:42s} vol {vol/1e6:5.2f} Mm3  Sn {sn:6.0f} t  cost ${tot/1e6:5.1f}M/yr  -> ${tot/sn:8,.0f}/t Sn")
    return tot / sn

for grade in (0.2, 0.35, 0.5, 0.8):
    print(f"-- grade {grade} kg/m3 cassiterite --")
    a = cost_case("open-water only 300 m3/h (Sevmorolovo/BIMA mode)", 300, ow_days, grade, 50e6, 70, 90e3)
    b = cost_case("open water + under fast ice 300 m3/h", 300, ow_days + ui_days, grade, 58e6, 110, 90e3, extra=1.5e6)
    c = cost_case("open water + under ice 600 m3/h", 600, ow_days + ui_days, grade, 85e6, 130, 90e3, extra=2.5e6)
print("baseline: PT Timah delivered $13.7-22.3k/t (S5); tin price ~$30k/t (S6)")

# break-even grade for <= $22k/t and <= $30k/t, both modes
def be(q, days, capex, crew, extra, target):
    lo, hi = 0.05, 5.0
    for _ in range(60):
        g = (lo + hi) / 2
        vol, sn = tin_output(q, days, g)
        tot = capex*0.147 + 0.05*capex + crew*90e3 + vol*1.2*1.3 + sn/0.7*400 + extra
        if tot/sn > target: lo = g
        else: hi = g
    return g
for tgt in (22e3, 30e3):
    print(f"break-even grade for ${tgt/1e3:.0f}k/t: open-water 300 m3/h {be(300, ow_days, 50e6, 70, 0, tgt):.2f} kg/m3; "
          f"year-round 300 {be(300, ow_days+ui_days, 58e6, 110, 1.5e6, tgt):.2f}; year-round 600 {be(600, ow_days+ui_days, 85e6, 130, 2.5e6, tgt):.2f}")

print("\n=== 1e. Reserve life check: 19 kt Sn (S2) ===")
for q, d in ((300, ow_days), (300, ow_days+ui_days), (600, ow_days+ui_days)):
    _, sn = tin_output(q, d, 0.5)
    print(f"{q} m3/h, {d:.0f} d at 0.5 kg/m3 -> {sn:.0f} t/yr -> life {19000/sn:.0f} yr")

print("\n=== 1f. Ice platform check (only ice saw/crane on ice; plant on hull) ===")
for h in (0.8, 1.2, 1.8):
    P = 3.5 * (h*100)**2 / 1000   # Gold's formula, A=3.5 kgf/cm2 (conservative, sea ice) -> tonnes
    print(f"sea ice {h} m: allowable moving load ~{P:.0f} t (Gold A=3.5); parked loads x0.5")
