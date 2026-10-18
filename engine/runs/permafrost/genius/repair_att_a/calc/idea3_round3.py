# R3: rate 60 t/h (between 2-man auger 21.5 t/h [S] and highwall miner ~100-140 t/h [S]); season 100 d navigation;
# competitor = small bank pit under the same bluff, strip ratio set by bluff height
dens=1.35
def auger_cost(Q, rate, capex, crew_n, tow_days):
    days=Q/(rate*20*0.7); ann=capex*0.15+0.25*600*20*days*90+crew_n*2.2e6*min(1,(days+20)/365)*1.3+tow_days*450e3+0.08*capex
    return ann/Q, days
capex=150e6+40e6+4*30e6
for Q in (40e3,80e3):
    c,d=auger_cost(Q,60,capex,12,int(Q/80e3*70)+10); print(f"auger 60 t/h, {Q/1e3:.0f} kt: {d:.0f} auger-days (season 100) -> {c:,.0f} rub/t")
c80,_=auger_cost(80e3,60,capex,12,80)
for bluff in (10,20,30):
    sr = bluff/1.5/dens   # m3 overburden per t coal
    pit = sr*180 + 300 + 3*150 + 300
    print(f"bluff {bluff} m: strip ratio {sr:.1f} m3/t -> bank pit + barge {pit:,.0f} rub/t ; auger/pit = {c80/pit:.2f}")
print(f"vs central mine + 2,000-2,500 km river haul 7,100-11,600 rub/t: ratio {c80/7100:.2f}-{c80/11600:.2f}")
