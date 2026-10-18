# Idea 1: under-ice crawler talik mining. All numbers: source tag in comment.
# [S] = sourced in this session (web search), [E] = engineering estimate / textbook value (stated range).
import math

# ---- ice growth (Stefan/Lebedev empirical h = a*sqrt(FDD)), Yakutsk monthly means [E: climate normals]
months = [("Oct",-7.6,31),("Nov",-28.0,30),("Dec",-37.6,31),("Jan",-40.4,31),("Feb",-35.8,28),("Mar",-22.2,31),("Apr",-7.0,30)]
a = 2.7  # cm/(degC day)^0.5, snow-covered lake ice [E: Michel/Lebedev range 2.0-3.4]
fdd = 0; print("ice thickness by end of month (cm):")
ice = {}
for m,T,d in months:
    fdd += max(0,-T)*d; h = a*math.sqrt(fdd); ice[m]=h; print(f"  {m}: FDD={fdd:5.0f} h={h:5.0f} cm")
# ---- Gold formula P = A h^2 (kg, cm), A = 3.5 safe moving / 7 short-term [E: Gold 1971]
for load_t in (40, 25, 10):
    print(f"ice needed for {load_t} t (A=3.5): {math.sqrt(load_t*1000/3.5):.0f} cm")
# -> 40 t surface plant needs 107 cm: reached ~early-mid Dec only; crawler cannot pass a 2 m2 hole (1.4x1.4 m)

# ---- moon-pool heat (water 0C to air -40C, wind): h_conv+evap ~ 25 W/m2K [E]
for A in (2.0, 1500.0):
    print(f"open water {A:6.0f} m2 heat loss at dT=40 K: {25*A*40/1e3:8.1f} kW")

# ---- surface wash plant vs submerged concentration
Q_solids = 150.0          # m3/h bank solids [E: cutter-suction / dredge-pump crawler class]
water_ratio = 10.0        # m3 water per m3 sands for sluicing [E: Russian ПГШ 8-15]
Q_w = Q_solids*water_ratio
# surface plant: water arrives at ~1C; sensible heat margin above 0C:
margin_kW = Q_w*1000/3600*4186*1.0/1e3
print(f"surface plant water flow {Q_w:.0f} m3/h, carries only {margin_kW:.0f} kW above 0C; building/ventilation losses ~300-600 kW at -40C [E]")
# submerged: only concentrate lifted (jig concentrate 0.5-2% of feed mass [E])
conc_frac = 0.01
print(f"submerged concentration: lift {Q_solids*conc_frac:.1f} m3/h concentrate instead of {Q_solids:.0f} m3/h slurry solids")

# ---- season production and lake size check
hours = 20*170   # Nov-Apr working under ice (crawler enters in Oct before freeze-up, exits after break-up) [E]
V_season = Q_solids*hours*0.75  # 75% availability
pay_frac = 2.0/7.0  # 2 m pay under 5 m thawed overburden in talik [E typical valley placer]
grade = 0.5   # g/m3 sands [E; Russian placers 0.3-1.0; Topky 1.75 S]
rec_sub, rec_surf = 0.75, 0.88  # recovery submerged jig vs surface sluice [E, deciding unknown]
V_pay = V_season*pay_frac
Au = V_pay*grade*rec_sub/1000
print(f"season dig {V_season:,.0f} m3 (pay {V_pay:,.0f} m3) -> Au {Au:.1f} kg")
# lake needed: dig depth 7 m below lake floor
area_needed = V_season/7.0
print(f"lake floor area needed per season: {area_needed/1e4:.1f} ha (e.g. {math.sqrt(area_needed*2):.0f} x {math.sqrt(area_needed/2):.0f} m)")
# talik depth check: Yakutian lake talik ~25 m [S: SPbU abstract], TEM 80-91 m [S]; Lachenbruch: need water depth > ice (2 m) [S bg-12-5941]
talik = 25.0
print(f"dig depth 7 m (+water 3 m) vs talik {talik} m -> margin {talik-7:.0f} m; lakes <2 m deep freeze to bottom -> no talik")

# ---- cost per g recovered, crawler system
gold_price = 9600  # rub/g [E: ~$3,800/oz at ~80 rub/$]
capex = 60e6 + 50e6 + 40e6   # crawler (amphibious/underwater-dozer class + dredge pump), surface power+camp, concentration module [E]
crf = 0.25                  # short life, high risk
P_kW = 550; fuel_L = 0.26*P_kW*hours*0.75; diesel = 90  # rub/L delivered remote [E]
crew = 14*2.2e6             # 14 people seasonal, fully loaded [E]
maint = 0.10*capex; mob = 15e6  # winter-road mobilisation sled [E]
opex = fuel_L*diesel + crew + maint + mob
annual = capex*crf + opex
cost_g = annual/(Au*1000)
print(f"crawler: annual {annual/1e6:.0f} M rub, fuel {fuel_L/1e3:.0f} kL -> {cost_g:,.0f} rub/g recovered")

# ---- baselines (per g recovered)
# Kommersant [S]: sluice ('промприбор') cash cost ~40% of gold value, dredge ~25%; cutoffs 50 mg/m3 sluice, 30 mg/m3 dredge
print(f"baseline sluice (40% of value): {0.40*gold_price:,.0f} rub/g ; dredge (25%): {0.25*gold_price:,.0f} rub/g")
# bottom-up bulldozer-sluice: strip ratio 2.5 (5 m thawed / 2 m pay) at 80-250 rub/m3, washing 250 rub/m3, other 250 [E]
for strip_cost in (80, 250):
    c = (2.5*strip_cost + 250 + 250)/(grade*rec_surf)
    print(f"bottom-up dozer-sluice, stripping {strip_cost} rub/m3: {c:,.0f} rub/g")
# drain-the-lake baseline: talik stays thawed several summers after drainage -> dozer/sluice on thawed talik, strip at ~80 rub/m3, but summer only
c_drain = (2.5*80 + 250 + 250 + 150)/(grade*rec_surf)   # +150 drainage/water mgmt
print(f"drain-lake-then-sluice (best practice for lake placers): {c_drain:,.0f} rub/g")
print(f"ratio crawler/drain-lake = {cost_g/c_drain:.2f}; crawler/dredge = {cost_g/(0.25*gold_price):.2f}")
# sensitivity on recovery and grade
for g in (0.3,0.5,1.0):
    for r in (0.6,0.75,0.85):
        Au2 = V_pay*g*r/1000; print(f"  grade {g} rec {r}: {annual/(Au2*1000):,.0f} rub/g", end="")
    print()
