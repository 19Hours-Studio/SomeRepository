"""Idea 2 - self-feeding ore-ice buttress dam. Binding quantities: thaw energy per m3 vs heat carried by
creek water (sets feed = Q*rho*c*dT/E), watertightness of a hoisted frozen pile, face heat transfer, breach peak, cost.
Sources: sluicing water 3 m3/m3 (kuzstu 2023 conf.), plant 1118-1458 m3/d (igduran trud 52/50); D375 new 96-156 Mrub,
operator 230 krub/month (drom.ru, hh.ru 2024-25); Froehlich (1995) breach peak; Samokhvalov & Ukhov: order I-II
streams 4.7-5.9 C colder than order VI-VII rivers (Kolyma basin)."""
import math
rho_i, L, cw = 917, 334e3, 4.186e6
def E_thaw(ice, T0, C=1.8e6):  # J/m3 bulk
    return ice*rho_i*L + C*(0-T0)
cases = {
 "ice-cemented pile (original, ice 0.30, -5C)": (0.30, -5),
 "loose hoisted frozen lumps (ice 0.15 bulk, -5C)": (0.15, -5),
 "loose lumps, summer-tempered (ice 0.15, -2C)": (0.15, -2),
 "sprayed upstream skin (ice 0.15+0.33 pores, -8C)": (0.48, -8),
}
print("thaw energy and water needed (water cooled from Tw to 0.5 C, 85% heat use)")
for k, (ice, T0) in cases.items():
    E = E_thaw(ice, T0)
    for Tw in (4, 6, 8, 10):
        w = E/(cw*(Tw-0.5)*0.85)
        print(f" {k:50s} E={E/1e6:5.1f} MJ/m3  Tw={Tw:2d}C -> {w:4.1f} m3 water per m3 ore")
print("sluice needs ~2.2-3 m3 water per m3 (kuzstu 2023: 3 m3/m3)")

# face heat transfer: sheet flow down a 10 m face
Q = 0.047; width = 60; Hf = 10; slope = math.radians(35)
q = Q/width
nu = 1.8e-6; k_w = 0.56
# film thickness laminar/turbulent sheet on rough gravel: use Manning n=0.04
S = math.sin(slope); n = 0.04
h = (q*n/math.sqrt(S))**0.6
V = q/h
Re = V*h/nu
tc = Hf/S/V
alpha_w = k_w/cw
t_mix = h**2/alpha_w
print(f"\nsheet flow: depth {h*1000:.1f} mm, V {V:.2f} m/s, Re {Re:.0f}, contact {tc:.0f} s, conductive mixing time {t_mix:.0f} s"
      f" -> water leaves at ~0 C if contact >> mixing: {tc/t_mix:.1f}x")
hcoef = 0.023*k_w/h*max(Re,2300)**0.8*13**0.4  # rough upper bound (Dittus-Boelter, Pr 13)
print(f" h ~ {hcoef:.0f} W/m2K -> thaw rate at 6C: {hcoef*6/E_thaw(0.15,-5)*86400:.2f} m/d (needed 0.8 m/d)")

# feed rate
for Tw in (5, 6, 8):
    for ice, T0 in ((0.15, -5), (0.30, -5)):
        feed = Q*cw*(Tw-0.5)*0.85/E_thaw(ice, T0)
        print(f" Q=47 L/s Tw={Tw}C ice {ice}: feed {feed*3600:5.1f} m3/h = {feed*86400:6.0f} m3/d -> 60,000 m3 in {60000/(feed*86400):5.1f} d")

# watertightness of a loose frozen pile: refreeze capacity of infiltrating water
for Tpile in (-3, -6, -10):
    refreeze = 1.6e6*(-Tpile)/(rho_i*L)
    print(f" loose pile at {Tpile}C: cold content refreezes {refreeze:.3f} m3 water per m3 vs air voids 0.30-0.35 -> self-seal {refreeze/0.33*100:.0f}% : LEAKS")
# winter spray-sealing an upstream skin, lift by lift
for Ta in (-20, -30, -40):
    lift = 0.4; water = 0.33*lift
    qloss = 25*(0-Ta) + 80     # W/m2 convective (wind 3 m/s) + LW
    t = water*rho_i*L/qloss/3600
    print(f" spray-seal 0.4 m lift at {Ta}C: {water:.2f} m3/m2 water freezes in {t:.0f} h")
skin_t, skin_h, skin_w = 3.0, 8.0, 80.0
print(f" sealed skin {skin_t} m x {skin_h} m x {skin_w} m = {skin_t*skin_h*skin_w:.0f} m3 of ore (thawed last, needs {E_thaw(0.48,-8)/E_thaw(0.15,-5):.1f}x energy)")

# Froehlich 1995 breach peak
for V_, H_ in ((60000, 6), (8000, 3), (3000, 2)):
    Qp = 0.607*V_**0.295*H_**1.24
    print(f" breach peak V={V_} m3 H={H_} m -> {Qp:.0f} m3/s")

# forebay solar warming
for dT in (2, 3, 4):
    P = Q*cw*dT
    A = P/90.0   # net 90 W/m2 into a shallow dark forebay in July (absorbed SW ~200 minus LW/evap/sensible)
    print(f" forebay warming +{dT} K at 47 L/s needs {A:,.0f} m2 (~{A/1e4:.2f} ha) shallow pond")

# temperature-stability window: feed rises/falls with Tw; sluice tolerates +-30% feed
for Tw in (3, 5, 7, 9, 11):
    feed = Q*cw*(Tw-0.5)*0.85/E_thaw(0.15, -3)*3600
    ratio = Q*3600/feed
    print(f" Tw {Tw:2d}C: feed {feed:5.1f} m3/h, water ratio {ratio:4.1f} m3/m3 {'OK' if 2.0<=ratio<=6 else 'OUT'}")

# ---- cost per m3 and per g ----
usd = 85.0
D375 = (120e6/usd)/30000 + 55*0.95 + 45 + (230e3*1.6/usd)/300  # $/h depreciation + fuel 55 L/h @0.95 + maint + crew
loader = 0.45*D375
plant_h = 60.0      # sluice/scrubber plant ownership + 2 crew, $/h
pump_h = 35.0       # diesel pump for water supply (baseline only)
print(f"\nhourly: D375-class ${D375:.0f}/h, loader ${loader:.0f}/h")
V = 60000
# Baseline A: natural thaw + dozer ripping/stacking layer by layer + loader feed + sluice (pumped water), 70 m3/h
hA = V/70
cA = hA*(D375 + loader + plant_h + pump_h)
# Baseline B: hydraulic monitor (water cannon) breaking/thawing + hydroelevator/gravel pump to sluice, 50 m3/h, diesel pumps 400 kW
hB = V/50
cB = hB*(plant_h + 400*0.25*0.95 + 30 + 0.3*D375)   # 0.25 L/kWh diesel
# New: forebay + header + sluice; dozer only 15% of time for tailings/cleanup; feed 70 m3/h at 6 C
hN = V/70
build = 25000 + 15000   # forebay dyke + header pipe, per season
cN = hN*(plant_h + 0.15*D375 + 10) + build
for lab, c in (("A natural thaw+dozer rip+loader+sluice", cA), ("B hydromonitor+gravel pump+sluice", cB), ("NEW self-feeding buttress", cN)):
    print(f" {lab:42s} ${c/V:5.2f}/m3 ; at 0.8 g/m3, 85% recovery: ${c/V/(0.8*0.85):5.2f}/g")
print(f" ratio vs A {cA/cN:.1f}x, vs B {cB/cN:.1f}x")
