import math
dens = 1.35  # t/m3 in-situ coal [E]
# ---- recovery per hole: seam thickness t, auger dia d, web w
def hole(d, t, w, L):
    area_frac = (math.pi*d*d/4)/((d+w)*t)
    tonnes = math.pi*d*d/4*L*dens
    return area_frac, tonnes
for d,t,w in ((1.5,1.5,0.4),(1.0,1.2,0.3),(1.5,2.5,0.4)):
    f,tn = hole(d,t,w,80); print(f"auger {d} m in {t} m seam, web {w}: face recovery {f*100:.0f}%, {tn:.0f} t per 80 m hole (incl. weathered zone)")
# weathered/thawed first 10-15 m of hole: dilution with ice/oxidized coal [E]
weathered = 12/80
# ---- production rate: historical 21.5 t/h two-man auger [S Pike County]; highwall miner 27-36 t/man-h x3-4 crew [S Terex]
for rate in (25, 60, 120):
    print(f"rate {rate} t/h: 20 kt in {20000/rate/20:.0f} days at 20 h/d; full 100-day season = {rate*20*100*0.7/1e3:.0f} kt (70% avail)")
# ---- face length consumed per year
_,tn = hole(1.5,1.5,0.4,80)
for Q in (20e3, 80e3):
    holes = Q/(tn*(1-weathered*0.5)); print(f"{Q/1e3:.0f} kt/yr -> {holes:.0f} holes -> {holes*1.9:.0f} m of bluff per year")
# ---- spud/thrust check: thrust 150-300 kN, torque 150-400 kNm [E for 1.5 m augers]
spuds, spud_lat = 3, 120e3  # N lateral capacity each in gravel [E]
print(f"spud lateral capacity {spuds*spud_lat/1e3:.0f} kN vs thrust 150-300 kN -> needs face-anchored reaction frame (rock bolts) for margin")
# ---- water level drift: low-water stage change 0.05-0.15 m/day [E Lena/Kolyma Aug-Sep]; campaign 20 d
for dh in (0.05,0.15):
    print(f"stage change {dh} m/d over 20 d = {dh*20:.1f} m vs auger frame vertical travel needed (seam 1.5 m)")
# ---- cost per tonne delivered (100-150 km)
def cost(Q, rate, capex, crew_n, tow_days, label):
    days = Q/(rate*20*0.7)
    crf=0.15
    fuel = 0.25*600*20*days*90   # 600 kW auger+pontoon power, 90 rub/L
    crew = crew_n*2.2e6*min(1,(days+20)/365)*1.3
    tow = tow_days*450e3          # pusher-tug charter 450k rub/day [E]
    maint = 0.08*capex
    ann = capex*crf+fuel+crew+tow+maint
    print(f"{label:52s} {Q/1e3:4.0f} kt, {days:4.0f} auger-days -> {ann/Q:6,.0f} rub/t at village bank")
    return ann/Q
capex = 150e6 + 40e6 + 2*30e6   # auger rig (used/import-substitute), pontoon+spuds+frame, 2 used 1,500 t hopper barges [E]
c20 = cost(20e3, 40, capex, 10, 25, "R1 as proposed: 20 kt, 5-8 villages")
c80 = cost(80e3, 40, capex+2*30e6, 12, 70, "R2 whole season, river-basin supply 80 kt")
# ---- baselines: (a) central mine + long river haul; (b) micro open pit + winter road; (c) existing small pit on bank + barge
# mine gate 2,500-4,000 rub/t [E]; river freight 2-4 rub/t-km [E]; Dzhebariki-Khaya -> Arctic Yakutia 2,000-3,000 km [S: Dzh-Kh on Aldan; LORP 178 kt Arctic coal 2026]
for gate, rate, km in ((2500,2.0,2000),(3500,3.0,2500)):
    print(f"baseline central mine + river: {gate + rate*km + 600:,.0f} rub/t (incl. 600 transshipment)")
# micro open pit: strip ratio 6-10 m3/t at 150-250 rub/m3 + mining 300 + winter road 150 km at 15-25 rub/t-km [E]
for sr, sc, wr in ((6,150,15),(10,250,25)):
    print(f"baseline micro pit + winter road 150 km: {sr*sc+300+wr*150+400:,.0f} rub/t")
# small bank pit loading barges directly (no winter road): strip + mine + 150 km barge 3 rub/t-km
for sr, sc in ((6,150),(10,250)):
    print(f"baseline small bank pit + barge 150 km: {sr*sc+300+3*150+300:,.0f} rub/t")
