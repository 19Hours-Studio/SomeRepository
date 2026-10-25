# Rough per-unit arithmetic used in answer.md (assumptions in comments)
rub_usd=80
# Idea 1: diesel vs nuclear/grid power
diesel_rub_t=90000        # delivered diesel at remote Chukotka/Yakutia site, RUB/t (43-66k at depots per EUROSOLAR + winter-road haul) - assumption
sfc=0.22                  # kg/kWh, large mine gensets (village DES 0.231-0.46)
fuel=diesel_rub_t/1000*sfc
diesel_total=fuel*1.3     # +30% O&M, genset capex
fnpp=6*1.6                # RUB6/kWh 2020 (Atomflot) indexed ~60% CPI to 2026 - assumption
mwh_per_tcu=300*8000/250000   # 300 MW, 8000 h, ~250 kt Cu/yr Baimskaya (MWh/t)
print("diesel fuel RUB/kWh",round(fuel,1),"all-in",round(diesel_total,1),"FNPP",fnpp)
print("MWh per t Cu",round(mwh_per_tcu,1))
print("saving USD/t Cu",round((diesel_total-fnpp)*mwh_per_tcu*1000/rub_usd))
# hybrid for gold mine 20 MW
for share in (0.1,0.3):
    print("hybrid diesel share saved",share,"RUB/kWh saved",round(fuel*share,1))
# Idea 3: pre-concentration
rej=0.5   # mass rejected (tests up to 0.70), conservative
print("mill energy per unit metal falls to",1-rej,"(if 95% metal kept ->",round((1-rej)/0.95,2),")")
# Idea 4: value density vs NSR/rail freight ~ 30 USD/t
freight=30
for name,val in [("thermal coal",90),("coking coal",170),("crude",450),("LNG",450),("Cu conc 25%",2300),("Cu cathode",9800)]:
    print(name,"freight share %",round(100*freight/val,1))
