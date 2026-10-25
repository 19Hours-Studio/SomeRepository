# Synthesis model: Part 1 (Baimskaya diesel bridge, corrected) + Part 3 (Norilsk spares pooling, corrected).
# Part 2 contributes no change (both ideas RATIO 1.0 vs current practice). All $ nominal 2026.
import itertools, statistics as st

KWH_T = 46.7          # kWh/t ore, Part 1 (consistent with 44.6 full plan)
SFC   = (0.20,0.225,0.25)   # kg diesel/kWh, leased gensets (review MAJOR 1)
HEAD  = 250e3/(60e6*0.876)    # Cu head implied by PFS: 250 kt Cu at 60 Mt/y, 87.6% rec -> 0.476%
REC   = 0.876-0.04      # coarse-grind penalty -4 pt (review MAJOR 3)
AU_REC_OZ_T = 400e3/60e6*0.95   # recovered oz/t ore, scaled from PFS, 5% grind penalty
CONC_CU = 0.24; MOIST=0.09

def bridge(avg_MW, sfc, cu=9500, au=3500, haul_km=600, haul_usd_tkm=0.18,
           opex_t=10.0, lease_kwh=0.04, diesel_port=1100, tank_capex=None, years=1.0):
    gwh = avg_MW*8.76
    ore = gwh*1e6/KWH_T                      # t/y
    cu_t = ore*HEAD*REC
    au_oz = ore*AU_REC_OZ_T
    diesel_power = gwh*1e6*sfc/1000          # t/y
    diesel_mine  = ore*1.5/1000              # t/y, mining fleet ~1.5 kg/t ore (assumed)
    diesel = diesel_power+diesel_mine
    conc_wmt = cu_t/CONC_CU/(1-MOIST)
    cons = 50e3*ore/15e6                     # reagents/balls/explosives, review: ~50 kt at 15 Mt/y
    loads = diesel/38 + conc_wmt/38 + cons/38   # separate loads, 38 t payload (TCWR 36.7)
    diesel_site = diesel_port + haul_km*haul_usd_tkm
    power_cost = gwh*1e6*(sfc/1000*diesel_site + lease_kwh)
    rev = cu_t*cu*0.87 + au_oz*au*0.92       # NSR payability net of TC/RC (assumed)
    log = conc_wmt*(haul_km*haul_usd_tkm + 15 + 60)   # road + port + sea Pevek->China
    opex = ore*opex_t + power_cost + log + cons*haul_km*haul_usd_tkm + diesel_mine*haul_km*haul_usd_tkm
    tank_m3 = diesel*0.9/0.84*1.1            # 9 months cover, density 0.84, 10% ullage
    tank = tank_capex if tank_capex is not None else tank_m3*1000   # $1,000/m3 installed on cooled piles (assumed)
    net_cash_per_tCu = (opex - au_oz*au*0.92)/cu_t
    margin = rev-opex
    return dict(MW=avg_MW, ore_Mt=ore/1e6, cu_kt=cu_t/1e3, au_koz=au_oz/1e3, diesel_kt=diesel/1e3,
                tank_km3=tank_m3/1e3, tank_musd=tank/1e6, loads=loads, loads_day_allseason=loads/330,
                loads_day_winter=loads/130, usd_kwh=power_cost/(gwh*1e6), net_cash_usd_tCu=net_cash_per_tCu,
                margin_musd_y=margin/1e6, net_first_year=(margin*years-tank)/1e6)

print("=== Part 1 bridge, corrected ===")
for MW in (40,65,80):
    for sfc in SFC:
        for (cu,au) in ((9500,3500),(8000,2800)):
            r=bridge(MW,sfc,cu,au)
            if sfc==0.225 or (cu==9500):
                print({k:round(v,2) for k,v in r.items()}, "prices",cu,au,"sfc",sfc)

# Expected value over FPU slip distribution (years after line-1 readiness Q1 2029)
slip = {0:0.35, 1:0.35, 2:0.20, 3:0.10}   # assumed from 2026->2028 slip history and Lomonosov
print("expected slip yr", sum(k*p for k,p in slip.items()))
for MW in (40,65):
    r=bridge(MW,0.225); rl=bridge(MW,0.225,8000,2800)
    commit = r['tank_musd']*0.6   # 40% of tankage reusable by mine fleet/North delivery after bridge (assumed)
    ev = sum(p*(k*r['margin_musd_y']) for k,p in slip.items()) - commit - 30   # 30 $m genset mobilisation
    evl= sum(p*(k*rl['margin_musd_y']) for k,p in slip.items()) - commit - 30
    be = (commit+30)/r['margin_musd_y']
    print(f"MW {MW}: EV base ${ev:.0f}m, low prices ${evl:.0f}m, break-even slip {be:.2f} yr")
    # time to first metal
    t_no = sum(p*k for k,p in slip.items())
    print(f"   expected years earlier first metal = {t_no:.2f}; P(bridge earns nothing)=0.35")

# Levelised full cost per t Cu over life, with vs without bridge, for slip = 1 yr
def lcu(slip_yr, bridge_on, MW=65, r=0.12, cu=9500, au=3500):
    capex=8000e6; years=range(0,30)
    pv_cost=0; pv_cu=0
    b = bridge(MW,0.225,cu,au)
    for y in years:
        df=(1+r)**-y
        if y<5: pv_cost += capex/5*df; continue          # build 2024-28
        t=y-5                                            # t=0 is 2029
        if t<slip_yr:
            if bridge_on:
                c = (b['cu_kt']*1e3)
                cost = (b['cu_kt']*1e3)*b['net_cash_usd_tCu'] + (b['tank_musd']*1e6*0.6+30e6 if t==0 else 0)
                pv_cost += cost*df; pv_cu += c*df
            else:
                pv_cost += 60e6*df   # care & owner's cost while idle (assumed)
            continue
        tt=t-slip_yr
        cu_kt = 125 if tt==0 else (250 if tt<10 else 170)   # line1 first, line2 next year
        if tt>=25: continue
        cost = cu_kt*1e3*2000                            # Part 1 full-plan net cash $2.0k/t Cu
        pv_cost += cost*df; pv_cu += cu_kt*1e3*df
    return pv_cost/pv_cu
for s in (0,1,2):
    a=lcu(s,False); b_=lcu(s,True)
    print(f"slip {s}: levelised full cost $/t Cu  no-bridge {a:,.0f}  bridge {b_:,.0f}  ratio {b_/a:.3f}")

print("\n=== Part 3 Norilsk spares pooling, corrected ===")
base_kt=806; cash=5.1e9; capex=3.0e9
full=(cash+capex)/(base_kt*1e3)
for add,unit in ((8,9000),(15,5400),(29,2700)):
    new=(cash+capex+add*1e3*unit)/((base_kt+add)*1e3)
    print(f"+{add} kt at ${unit}/t: full cost {full:,.0f} -> {new:,.0f} $/t Ni-eq, change {100*(new/full-1):.2f}%")

print("\n=== Cross-part checks ===")
r=bridge(65,0.225)
print("bridge diesel vs Chukotka 2025 northern delivery 159.2 kt:", round(r['diesel_kt']/159.2,2),"x")
print("tanker calls at 19.5 kt:", round(r['diesel_kt']/19.5,1), " conc ships at 40 kt:", round(r['cu_kt']/CONC_CU/(1-MOIST)/40,1))
print("Nagleynyn design 1.842 Mt/y; bridge conc wmt kt:", round(r['cu_kt']/CONC_CU/(1-MOIST),0))
print("conc storage for 8-month closed season kt:", round(r['cu_kt']/CONC_CU/(1-MOIST)*8/12,0), "(Red Dog holds 950 kt)")
