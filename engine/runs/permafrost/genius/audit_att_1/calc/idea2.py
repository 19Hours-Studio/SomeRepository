import math
print("annual volume 270d*24h*150:",270*24*150/1e6,"Mm3; util implied for 0.6:",0.6e6/(270*24*150))
print("area for 0.6 Mm3 at 7 m:",0.6e6/7/1e4,"ha; for 0.972:",0.972e6/7/1e4)
print("fines conc per day mg/L:",540e9/160000/1000)  # mg / L
# Stefan with Yakutsk monthly means (1991-2020 approx)
T={'Oct':-7.5,'Nov':-27.0,'Dec':-37.6,'Jan':-38.6,'Feb':-33.8,'Mar':-20.1,'Apr':-4.8}
days={'Oct':31,'Nov':30,'Dec':31,'Jan':31,'Feb':28,'Mar':31,'Apr':30}
# Freeze-up assume Oct 15; use Oct 15-31 avg -11
fdd=0; dates=[]
seq=[('Oct',17,-11.0),('Nov',30,-27.0),('Dec',31,-37.6),('Jan',31,-38.6),('Feb',28,-33.8),('Mar',31,-20.1),('Apr',20,-8.0)]
for a in [2.0,2.4,2.7]:
    fdd=0; reached=None
    for m,n,t in seq:
        for d in range(n):
            fdd+=-t
            h=a*math.sqrt(fdd)
            if reached is None and h>=110: reached=(m,d+1 if m!='Oct' else d+15)
    print(f"a={a}: FDD end season {fdd:.0f}, max ice {a*math.sqrt(fdd):.0f} cm; 1.1 m reached {reached}")
# Gold formula
for A in [3.5,7.0]:
    for h in [50,84.5,110,180]:
        print(f"Gold A={A} h={h} cm -> {A*h*h/1000:.1f} t")
# moon pool heat loss
def openwater(Ta,v=2.0,Tw=0.0):
    h=5.7+3.8*v
    qs=h*(Tw-Ta)
    sig=5.67e-8
    Lw_up=0.97*sig*(273.15+Tw)**4
    # clear sky downwelling approx Brutsaert-like: eps ~0.6 at very cold dry
    Lw_dn=0.65*sig*(273.15+Ta)**4
    ql=Lw_up-Lw_dn
    es=lambda T:611*math.exp(21.87*T/(T+265.5)) if T<0 else 611*math.exp(17.27*T/(T+237.3))
    qe=h*(2.5e6/1005)*0.622/101325*(es(Tw)-0.8*es(Ta))
    return qs+ql+qe,qs,ql,qe
for Ta in [-20,-40,-50]:
    tot,qs,ql,qe=openwater(Ta)
    print(f"open water Ta={Ta}: {tot:.0f} W/m2 (sens {qs:.0f}, LW {ql:.0f}, evap {qe:.0f}); 2 m2 -> {2*tot/1e3:.1f} kW; 2+1.96 m2 -> {3.96*tot/1e3:.1f} kW")
# turbidity: norms 0.25 / 0.75 mg/L increment
for leak in [0.001,0.01,0.1,0.2]:
    per_day=540e9*leak/160000/1000
    print(f"curtain leakage {leak*100}%: +{per_day:.1f} mg/L per day; days to exceed 0.75 mg/L: {0.75/per_day:.3f}; over 150 d {per_day*150:.0f} mg/L (no settling)")
req=1-0.75/3375
print("containment needed to stay under 0.75 mg/L for ONE day:",req)
# crawler ground pressure
W=40; sub=W*(1-1/7.85*1.0)  # steel-dominated submerged weight
for A in [8,12,20]:
    print(f"track area {A} m2: submerged ground pressure {sub*9.81/A:.0f} kPa; dry {W*9.81/A:.0f} kPa")
for su in [3,5,10]:
    print(f"su={su} kPa: bearing capacity 5.14*su = {5.14*su:.0f} kPa")
# jig area: primary jig capacity 15-25 m3/h per m2
for c in [15,25]:
    print("jig area m2 for 150 m3/h:",150/c)
# cost ratio margin
for err in [0.2,0.35,0.5]:
    print(f"capex/opex +{err*100:.0f}%: 1600 -> {1600*(1+err):.0f} rub/g vs 1930/2140")
