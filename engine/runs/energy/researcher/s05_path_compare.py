# Compare annual cost of covering Germany's dark-spell deficit (s02/s03 daily system):
# A) electrolysis -> salt cavern H2 -> new H2 turbines (61 GW)
# B) electrolysis -> e-methanol (DAC CO2) -> existing EREV fleet engines (sunk), 11 kW bidirectional chargers
# C) same as A but discharge converter = sunk/idle assets (only an interface cost)
def crf(r,n): return r*(1+r)**n/((1+r)**n-1)
r=0.07
gen_cost=0.045      # $/kWh marginal overbuild energy (wind+solar LCOE)
load=491e9          # kWh/yr (s02 mean)
def overbuild_cost(OVER): return (OVER-1.0)*load*gen_cost
paths={
 # name: OVER needed, deficit kWh, RTE, electrolyser GW (from s03), conv $/kW, conv GW, extra fuel-chain $/kWh_fuel, storage $/kWh_fuel_capacity, store size kWh_fuel
 "A H2 + new turbines":      dict(OVER=1.3, deficit=55e9, rte=0.26, ely_GW=60, conv=900, conv_GW=61, fuel_extra=0.0,  store=0.5,  store_kwh=55e9/0.40*0.6),
 "B e-MeOH + EREV fleet":    dict(OVER=1.5, deficit=40e9, rte=0.18, ely_GW=55, conv=73,  conv_GW=61, fuel_extra=0.035, store=0.02, store_kwh=40e9/0.36*0.6),
 "C H2 + sunk converters":   dict(OVER=1.3, deficit=55e9, rte=0.26, ely_GW=60, conv=150, conv_GW=61, fuel_extra=0.0,  store=0.5,  store_kwh=55e9/0.40*0.6),
}
for k,p in paths.items():
    ob=overbuild_cost(p['OVER'])
    ely=p['ely_GW']*1e6*600*(crf(r,20)+0.02)
    conv=p['conv_GW']*1e6*p['conv']*(crf(r,25)+0.02)
    fuel_in=p['deficit']/p['rte']*p['rte']/ (p['rte']) # placeholder no-op
    fuel_kwh=p['deficit']/ (0.40 if k[0]!='B' else 0.36)
    fx=fuel_kwh*p['fuel_extra']
    st=p['store']*p['store_kwh']*(crf(r,40)+0.01)
    tot=ob+ely+conv+fx+st
    print(f"{k:26s} overbuild {ob/1e9:5.1f}  electrolyser {ely/1e9:5.1f}  converter {conv/1e9:5.1f}  "
          f"fuel-synth {fx/1e9:4.1f}  store {st/1e9:4.1f}  => {tot/1e9:5.1f} B$/yr ; "
          f"{tot/p['deficit']:.3f} $/kWh-deficit")
print("(OVER=1.3 overbuild is common to all; B's extra 0.2 overbuild cost is the price of its low RTE)")
