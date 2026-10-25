import sys; sys.path.insert(0, '/home/user/SomeRepository/engine')
from kit import econ, data
fx = data.get('price.fx_rub_usd'); wr = data.get('price.winter_road_rub_tkm')/fx  # $/t-km
pdz = data.get('price.power_mine_diesel'); crf = econ.crf(0.14, 25)
cu = 14441.0   # LME 21 Oct 2026 (Cochilco via redimin.cl)
gold = data.get('price.gold'); G = data.G_PER_OZ
print('crf', round(crf,3), 'winter road $/tkm', round(wr,3))

print('\n== IDEA 1 Tomtor raw ore ==')
# leg costs per t ore: winter road 300 km, barge 1000 km, NSR, rail 3000 km to Krasnokamensk (SRK route)
ore = 300*data.get('price.winter_road_rub_tkm') + 1000*4 + 16000 + 3000*data.get('price.rail_rzd_rub_tkm')
for g in (0.10, 0.125):
    print(f' grade {g}: freight ${ore/fx:.0f}/t ore -> ${ore/fx/g/0.85:,.0f}/t REO recovered (85% assumed)')
print(' existing plant able to leach Tomtor ore: 0 (Krasnokamensk "still to be built") -> margin 0')
print(' ratio vs ThreeArc 2010s raw-ore plan (same chain):', econ.ratio_vs_baseline(1.0, 1.0))

print('\n== IDEA 2 diesel starter ==')
kwh_t = 27e3*8760*0.85/6e6
print(' fuel kt/yr', round(27e3*8760*0.85*0.27*0.84/1e6,1), ' kWh/t ore', round(kwh_t,1))
for g in (0.50, 0.39):
    cu_t = g/100*0.88*1000  # kg Cu per t ore
    en = kwh_t*pdz/cu_t*1000; haul = (1/0.25)*800*wr
    print(f' grade {g}%: energy ${en:,.0f}/t Cu + conc haul ${haul:,.0f} = ${en+haul:,.0f}; allowed 30%*Cu ${0.3*cu:,.0f}; margin {0.3*cu/(en+haul):.2f}')
cut = 6e6*0.005*0.88
road = 48e3 + 6e6*0.005*0.88/0.25 + 18e6*0.4*0.84/1000 + 10e3   # fuel, conc, mine fuel, reagents/supplies
kupol_road = 60e3 + 25e3   # 2008 Kupol winter road season (Wikipedia, Kinross)
print(f' winter-road tonnage needed {road/1e3:.0f} kt vs demonstrated {kupol_road/1e3:.0f} kt -> margin {kupol_road/road:.2f}')
plant = econ.six_tenths_scaling(8e9-1.9e9, 70, 6)
print(' starter plant capex $bn', round(plant/1e9,2))
cap_t = plant*crf/cut
base = data.get('price.copper_conc_delivered_cost')
other = base*(0.12+0.10+0.07+0.10)*1.3   # processing, labour, inbound, other; +30% small-scale penalty
en = kwh_t*pdz/(5*0.88)*1000; haul = 4*800*wr
new = cap_t + en + haul + other
print(f' starter $/t Cu: capital {cap_t:,.0f} energy {en:,.0f} haul {haul:,.0f} other {other:,.0f} = {new:,.0f}; base {base}; ratio {econ.ratio_vs_baseline(base,new):.2f}')

print('\n== IDEA 3 mine-first ==')
L = 24e6/0.84
for lpt in (0.11, 0.5):
    print(f' {lpt} L/t -> {L/lpt/1e6:.0f} Mt moved/yr')
print(' fuel by winter road: demonstrated 25 kt diesel/season at Kupol -> margin', round(25/24,2))
af = sum(1/1.14**t for t in range(1,26))
ratio3 = af/(af-0.5*econ.delay_pv_factor(0.14,1))
pre = 50e6*2.0; extra = econ.carry_forward_cost(pre,0.14,2)-pre
print(f' ramp-year gain ratio {ratio3:.3f}; carry-forward penalty ${extra/1e6:.0f}M vs ~${base*300e3/1e9:.1f}bn/yr cost')

print('\n== IDEA 4 Kupol hub ==')
haul_t = 300*data.get('price.winter_road_rub_tkm')/fx
rec = 0.93
for g in (6, 9.5):
    oz = g*rec/G
    print(f' {g} g/t: haul ${haul_t:.0f}/t -> ${haul_t/oz:.0f}/oz; margin vs $250 target {250/(haul_t/oz):.2f}')
print(' idea assumed $45/t =', round(45/300,3), '$/tkm vs kit', round(wr,3))
print(' window margin (feed 365 kt/yr in ~100 d at Kupol 2008 850 t/d):', round(econ.window_margin(100, 365e3, 85e3/100),2))
kupol_cos = 304.5e6/511e3
mill_cap = 200e6*crf/(300e3*6*rec/G)
oz = 6*rec/G
std = kupol_cos + mill_cap; hub = kupol_cos + haul_t/oz
print(f' Kupol CoS ${kupol_cos:.0f}/oz; standalone {std:.0f} vs hub {hub:.0f}; ratio {std/hub:.2f}')
for m,r in [(0.0,1.0),(0.47,0.55),(1.04,1.06),(0.63,1.18)]: print(econ.gate_verdict(m,r))
