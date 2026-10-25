import sys; sys.path.insert(0, '/home/user/SomeRepository/engine')
from kit import thermal, econ, geotech

print("== IDEA 1 plant-chilled foundations ==")
# summer heat reaching the frozen ground = heat to thaw the active layer (1.0 m, F85 Norilsk 0.96 m;
# Yamal ALT ~1 m) over ~100 thaw days, ice 35 vol%, from -3 C (F86 warm Yamal permafrost)
E = thermal.thaw_energy_per_m3(0.35, -3)
q_req = E * 1.0 / (100 * 86400)
print("thaw energy MJ/m3", E/1e6, "required summer flux W/m2", q_req, "margin vs 5 W/m2", 5/q_req)
# check: kit reference 30% ice -5C ~101 MJ/m3
print("check", thermal.thaw_energy_per_m3(0.30, -5)/1e6)
print("power at required flux, MW elec (COP 2, 1 km2)", q_req*1e6/2/1e6)
# chain: foundation-related cost share in delivered LNG (est <=1%) removed completely -> ceiling
print("ratio ceiling (1% share)", econ.ceiling_ratio(0.01))

print("== IDEA 2 Murmansk shuttle ==")
nm = 1852.0
def rt_days(ice_nm, open_nm, v_ice=9, v_open=17, port_d=3.0):
    return 2*(ice_nm/v_ice + open_nm/v_open)/24 + port_d
shuttle = rt_days(600, 650)            # Utrenneye/Sabetta - Kola (Saam FSU)
zee = rt_days(600, 650+1400)           # + ~1,400 nm Kola-Zeebrugge open water
print("RT shuttle d", shuttle, "RT Zeebrugge d", zee, "(F138 says ~20 d)", "gain x", zee/shuttle)
cargo_t = 172600*0.45*0.98             # F140 ship size
mt_per_ship = 365/shuttle*cargo_t/1e6
print("Mt/ship-yr shuttle", mt_per_ship)
for avail in (1, 2):                   # F139: Kosygin (+ Margerie, which is Yamal LNG fleet)
    print("T1 6.6 Mt margin", avail*mt_per_ship/6.6, " T1+T2 13.2 Mt margin", avail*mt_per_ship/13.2)
print("ratio (22% share x 25-35% cut)", econ.ceiling_ratio(0.22*0.25), econ.ceiling_ratio(0.22*0.35))

print("== IDEA 3 rock-socketed piles ==")
# SP 25.13330.2020 already prescribes rock-bearing piles where rock <=20 m; Norilsk pits to 20 m
print("depth margin Norilsk 30/20", 30/20)
# adfreeze drag on a thawing layer is the problem the sleeve addresses; warm adfreeze loss
print("adfreeze -0.5 vs -3 C", geotech.adfreeze_strength(-0.5,'clay')/geotech.adfreeze_strength(-3,'clay'))
# chain: Ambarnaya award 146 bn RUB (F262) ~ $1.9bn, spread over 30 yr vs ~$8bn/yr full cost (ledger B)
share = (146e9/78/30)/8e9
print("foundation-failure share/yr", share, "ratio ceiling", econ.ceiling_ratio(share))

print("== IDEA 4 numbers-up Arctic Cascade ==")
# schedule: T4 build ~2017, due end-2019, first LNG early 2021, full mid-2021 -> ~4-4.5 yr
print("time margin 2.5/4.5", 2.5/4.5)
# winter shipping: no spare Arc7 (Yamal fleet of 15 fully used, Arctic LNG 2 has 1-2); summer only Jul-Nov
print("deliverable-year margin (5 of 12 months)", 5/12)
# capital: T1-3 project $1,640/t/y = ~1,100 trains + ~540 field/port/utilities (F43, F174)
cap_now, cap_idea = 1640, 500+540
cut = 1 - cap_idea/cap_now
print("capital cut", cut, "ratio", econ.ceiling_ratio(0.47*cut), " idea's claim 60%:", econ.ceiling_ratio(0.47*0.6))
for m, r in [(5/q_req, 1.01), (2*mt_per_ship/13.2, 1.07), (1.5, 1.01), (5/12, 1.21)]:
    print(econ.gate_verdict(m, r))
