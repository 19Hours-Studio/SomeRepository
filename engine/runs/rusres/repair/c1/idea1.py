# IDEA 1 numbers-up Arctic Cascade trains: whole-chain per tonne delivered + hull-limited capacity
def crf(r,n): return r*(1+r)**n/((1+r)**n-1)
r=0.12  # nominal rouble-era WACC proxy (key rate 14%, FACT 229), USD-ish
MMBtu_per_t=52.0
# capex per t/y (plant only)
cap={'T1-3 C3MR (imported drives)':1100,'Train4 Arctic Cascade est':500,'small train series target':600,
     'large domestic-drive 6.6Mtpa (AL2-type, plant share)':800}
for k,v in cap.items(): print(f"{k:50s} capex {v} $/t/y -> annualised {v*crf(r,25):6.1f} $/t")
# Arc7 hull productivity
cargo=172600*0.45*0.97/1000  # kt LNG per voyage
modes={'Murmansk/Saam shuttle 12d':12,'NW Europe Zeebrugge 20d (ends 2027, FACT 215)':20,'Asia via NSR east ~40d (summer)':40}
for k,d in modes.items(): print(f"{k:45s} {cargo*365/d/1000:5.2f} Mt/y per hull")
mixed=cargo*(150/40+215/12)/1000
print("mixed (150d east + 215d shuttle) Mt/y/hull",round(mixed,2))
hull=330e6; hull_opex=20e6
ann_hull=hull*crf(r,30)+hull_opex
print("Arc7 hull cost per t (mixed)", round(ann_hull/(mixed*1e6),1), "$/t; shuttle-only", round(ann_hull/(cargo*365/12*1e3),1))
print("hulls per 0.9 Mtpa train (mixed)",round(0.9/mixed,2))
# Installed idle: AL2 T1+T2 13.2 Mtpa; hulls needed to fill
print("hulls to fill AL2 T1+T2 (mixed)", round(13.2/mixed,1))
# hull supply 1.0-2.0/yr from Zvezda (FACT 139,347): year AL2 T1+T2 filled
for rate in (1.0,1.5,2.0):
    yrs=(13.2/mixed-1)/rate   # 1 hull already (Kosygin) + Christophe de Margerie is Yamal fleet
    print(f"hull rate {rate}/yr -> AL2 T1+T2 full ~{2026+yrs:.0f}")
# whole chain per tonne delivered China, both small and large need same ships
gas_field_opex=25; plant_opex_big=30; plant_opex_small=35  # $/t assumptions (small trains slightly higher O&M per t)
onward_conv=2.0*MMBtu_per_t   # $/t conventional Murmansk->Asia (Suez) assumption ~$2/MMBtu
ship=ann_hull/(mixed*1e6)
def chain(capex,opex): return capex*crf(r,25)+opex+gas_field_opex+ship+0.6*onward_conv  # 60% of volume goes via transshipment
big=chain(1100,plant_opex_big); small=chain(600,plant_opex_small); dom_big=chain(800,plant_opex_big)
print(f"chain $/t delivered: T1-3 type {big:.0f}, AL2 domestic big {dom_big:.0f}, small series {small:.0f}, ratio big/small {big/small:.2f}, domestic-big/small {dom_big/small:.2f}")
fill_idle=0*crf(r,25)+plant_opex_big+gas_field_opex+ship+0.6*onward_conv
print(f"fill idle AL2 T1/T2 (sunk plant): {fill_idle:.0f} $/t  -> small train / fill-idle = {small/fill_idle:.2f}")
# lumpiness: big 6.6 Mtpa train completed at once, hulls arrive 1.5/yr -> idle capital
def idle_cost(cap_t, size, rate):
    # fraction of capacity unusable each year until hulls catch up
    hull_need=size/mixed; t=hull_need/rate  # years to get hulls
    avg_idle_frac=0.5  # linear ramp
    return cap_t*size*1e6*r*t*avg_idle_frac/ (size*1e6*25)  # $/t over life, crude
print("idle-capital penalty $/t: 6.6Mtpa big", round(idle_cost(800,6.6,1.5),1), " 0.9 small", round(idle_cost(600,0.9,1.5),1))
# hedge value at Sabetta: lost T1-3 availability
margin=4.5*MMBtu_per_t
for loss in (0.03,0.08,0.15):
    lost=16.5*loss
    trains=lost/0.9
    print(f"T1-3 availability loss {loss:.0%}: {lost:.1f} Mt/y lost, {trains:.1f} small trains to cover, payback {600/margin:.1f} y at margin {margin:.0f}$/t")
