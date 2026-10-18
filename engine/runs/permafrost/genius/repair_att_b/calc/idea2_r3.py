# IDEA 2 round 3: heat from black-lined recirculating settling pond (sun) + creek; sourced stripping costs
L=334e3; q=300*L+(1900*800+300*2100)*3      # 107 MJ/m3 pay
GOLD=12088; gp=3.0
def heat(pond_ha, net_Wm2, creek_MW=2.1): return creek_MW*1e6 + pond_ha*1e4*net_Wm2
for ha in (0,1,2,3):
    for net in (80,150):
        P=heat(ha,net); r=P*0.3*3600/q
        # pond steady state: return water 1C, flow 100 L/s -> pond temp rise needed
        dT=P/(100*4190)
        print(f" pond {ha} ha net {net} W/m2: heat {P/1e6:.1f} MW -> {r:.0f} m3/h pay (eta 0.3); loop dT={dT:.1f} K (supply ~{1+dT:.0f} C)")
# sourced stripping: bulldozer 80-90 rub/m3, dragline 27-29 (zolotodb.ru, undated ~2015-20); washing+mining ~3x stripping/m3.
infl=1.5   # to 2026 prices (assumption)
bull=85*infl; wash=3*85*infl
def openpit(H,hp=1.8,rec=0.87):
    cs=bull if H<=15 else bull*1.8          # beyond bulldozer economic push distance 50-100 m (mgri) -> excavator-truck (assumed 1.8x)
    SR=H/hp*1.15
    c=SR*cs+wash
    return SR,c,c/(gp*rec)
def jetadit(rate,days,crew=12,pd=25000,equip=12e6,access=5e6,pond=6e6,kW=280,fuel=22,rec=0.72):
    V=rate*days*20
    c=(crew*(days+15)*pd+equip+access+pond)/V + kW/rate*fuel + wash
    return V,c,c/(gp*rec)
for rate,days in ((21,60),(35,90),(45,90)):
    V,c,cg=jetadit(rate,days)
    print(f" jet adit {rate} m3/h x {days} d: {V:.0f} m3/season, {c:,.0f} rub/m3 -> {cg:,.0f} rub/g")
ug=(2500/(gp*0.8),4000/(gp*0.8))
for H in (10,15,20,30,40):
    SR,c,cg=openpit(H)
    V,cj,cgj=jetadit(35,90)
    best=min(cg,ug[0])
    print(f" H={H}: open pit SR={SR:.1f} {c:,.0f} rub/m3 = {cg:,.0f} rub/g; underground(est) {ug[0]:,.0f}-{ug[1]:,.0f}; jet adit {cgj:,.0f} -> {best/cgj:.1f}x vs best")
