# IDEA 2: Frozen-roof jet adits. Heat balance, roof thaw, adit advance, cost vs baselines.
import math
L=334e3
print("=== R1: thaw energy of frozen pay ===")
for ice in (200,300,400):        # kg ice per m3 pay (ice content 10-20% of dry mass, rho_d 1.9-2.0 t/m3)
    q=ice*L+(1900*800+ice*2100)*3
    print(f" ice {ice} kg/m3 -> {q/1e6:.0f} MJ/m3 = {q/3.6e6:.1f} kWh/m3")
q_base=300*L+(1900*800+300*2100)*3
print("=== R1: creek heat (parent: 100 L/s cooled 9 K, 30% use) vs realistic low-order creek ===")
for Tin,Tout in ((9,0),(6,1),(5,1.5)):
    for eta in (0.15,0.3,0.5):
        P=100*4190*(Tin-Tout)  # W
        rate=P*eta*3600/q_base
        print(f" Tin={Tin} Tout={Tout} eta={eta}: heat {P/1e6:.2f} MW -> {rate:.0f} m3/h pay")
print("=== R1: roof thaw if adit FLOODS with 6C water vs air-filled unventilated ===")
Lv=300*L  # J per m3 of roof to thaw
for name,h,dT in (("flooded, flowing water h=500",500,5),("flooded h=1000",1000,5),("splash zone h=200",200,4),("air-filled unventilated h=8+4.5rad",12.5,2.5)):
    qf=h*dT; v=qf/Lv*86400
    print(f" {name}: q={qf:.0f} W/m2 -> roof thaw {v*100:.1f} cm/day")
print("=== R2: advance rate and exposure time ===")
for rate in (20,35):
    for w,hh in ((3,1.8),):
        adv=rate/(w*hh)
        print(f" pay rate {rate} m3/h, adit {w}x{hh} m -> advance {adv:.1f} m/h; 80 m adit in {80/adv:.0f} h; with pillar retreat total roof life ~{2*80/adv:.0f} h -> air-filled thaw {12.5*2.5/Lv*3600*2*80/adv*100:.1f} cm")
print("=== R2: roof/pillar mechanics (frozen gravel; strength drops >3x from -18 to -1 C) ===")
rho=2000; g=9.81
for H in (10,20,30):
    for wp in (3,4):
        sv=rho*g*H; sp=sv*(3+wp)/wp
        print(f" cover {H} m pillar {wp} m: pillar stress {sp/1e6:.2f} MPa (vs frozen gravel long-term compressive ~1-2 MPa at -2..-4C, short-term 3-6 MPa; life < 2 days)")
t=1.0; span=3
print(f" roof beam self-weight bending stress (t={t} m span {span} m): {rho*g*span**2/(2*t)/1e3:.0f} kPa vs long-term tensile 100-300 kPa")
print("=== R2: water balance (no flooding) ===")
jet=360; melt=35*0.3
print(f" water in = jet {jet} + ice melt {melt:.0f} m3/h; hydro-elevator design 1.3x = {1.3*(jet+melt):.0f} m3/h; adits driven UP-gradient (valley 0.5-2%) so overflow drains out portal by gravity")
print("=== R3: costs per m3 pay and per gram ===")
GOLD=12088
def jetadit(rate=30,days=60,hours=20,crew=12,pd=25000,equip=10e6,access=5e6,kW=260,fuel=22,wash=300,rec=0.72):
    V=rate*days*hours
    c=(crew*(days+15)*pd+equip+access)/V + kW/rate*fuel + wash
    return V,c,rec
def openpit(H,hp=1.8,cs=None,wash=300,mine=100,rec=0.87):
    if cs is None: cs=150 if H<=15 else 250   # bulldozer ripping frozen vs excavator-truck (estimate)
    SR=H/hp*1.15                                # +15% for side slopes in wide valley
    return SR,SR*cs+mine+wash,rec
def underground(c=3000,rec=0.80): return c,rec   # winter drill/blast or roadheader, LHD, stockpile, summer wash (estimate 2,500-4,000 rub/m3)
gp=3.0  # g/m3 pay typical of placers worth underground mining
for rate in (20,30):
    V,c,r=jetadit(rate=rate)
    print(f" jet adit {rate} m3/h: season {V:.0f} m3, {c:.0f} rub/m3 pay -> {c/(gp*r):,.0f} rub/g")
for H in (10,20,30):
    SR,c,r=openpit(H); print(f" open pit H={H} m SR={SR:.1f}: {c:,.0f} rub/m3 -> {c/(gp*r):,.0f} rub/g")
for cu in (2500,4000):
    c,r=underground(cu); print(f" underground winter mining {cu} rub/m3 -> {c/(gp*r):,.0f} rub/g")
V,c,r=jetadit(rate=30); ja=c/(gp*r)
for H in (20,30):
    SR,co,ro=openpit(H); ug=2500/(gp*0.8)
    print(f" H={H}: best baseline {min(co/(gp*ro),ug):,.0f} rub/g vs jet adit {ja:,.0f} -> {min(co/(gp*ro),ug)/ja:.1f}x")
