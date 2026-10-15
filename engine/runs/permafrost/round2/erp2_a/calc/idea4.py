# Idea 4: night-sky radiative trays below CaCl2-ice eutectic (-49.8 C) to lock Ca out of Li brine
import math, random
h=6.626e-34;c=2.998e8;k=1.381e-23;sig=5.670e-8
def band(T,l1=8e-6,l2=13e-6,n=2000):
    s=0
    for i in range(n):
        l=l1+(l2-l1)*(i+0.5)/n
        s+=2*math.pi*h*c*c/l**5/(math.exp(h*c/(l*k*T))-1)
    return s*(l2-l1)/n
for TC in [-40,-50,-52]:
    T=TC+273.15; print(f"{TC} C: 8-13um band {band(T):.1f} W/m2 = {band(T)/(sig*T**4)*100:.0f}% of sigmaT^4")
def net(Ts,Ta,tau=0.85,hc=3.0,eps=0.95):
    # selective emitter in window; atmosphere in window emits (1-tau)*B(Ta-ish); outside window assume emitter reflective
    return eps*(band(Ts)-(1-tau)*band(Ta))-hc*(Ta-Ts)
# stagnation temperature
for Ta in [-35,-40,-45,-50]:
    lo,hi=Ta-30,Ta
    for _ in range(50):
        m=(lo+hi)/2
        if net(m+273.15,Ta+273.15)>0: hi=m
        else: lo=m
    print(f"air {Ta} C: no-load film {lo:.1f} C ({Ta-lo:.1f} K below air); net power at film -52 C: {net(221.15,Ta+273.15):.1f} W/m2")
# Udachny Jan mean ~ -39 C; Nov -30, Dec -37, Feb -36, Mar -26 (approx.), hourly SD 6 K
random.seed(2); E=0; hrs=0
for mu,d in [(-30,30),(-37,31),(-39.4,31),(-36,28),(-26,31)]:
    for i in range(d*24):
        Ta=random.gauss(mu,6)
        p=net(221.15,Ta+273.15)
        if p>0: E+=p*3600; hrs+=1
Lf=260e3  # J/kg brine solidified at eutectic (ice 334 kJ/kg * 0.7 + hexahydrate fusion ~ 170 kJ/kg * 0.3, approx)
print(f"hours with net cooling at -52 C film: {hrs}; energy {E/1e6:.1f} MJ/m2 -> {E/Lf:.0f} kg brine solidified per m2 per winter")
Li=0.147 # g/L Udachnaya average (Novosibirsk study); 0.4 g/L for richer Siberian horizons
for Li_gL in [0.147,0.4]:
    brine_t=188/Li_gL*1.25  # t brine per t LCE (188 kg Li per t LCE; brine density 1.25 t/m3; Li in kg/m3 = g/L)
    area=brine_t*1000*0.8/(E/Lf)  # 80% of brine mass solidified
    print(f"Li {Li_gL} g/L: {brine_t:.0f} t brine per t LCE; trays {area:.0f} m2 per t LCE/yr; at $5/m2/yr -> ${area*5:.0f}/t LCE")
# Above-eutectic, air-only alternative for brines richer than eutectic composition: hexahydrate crystallisation
def hexa_liq(TC): return 29.9+(37.3-29.9)*(TC+49.8)/49.8   # wt% CaCl2 on hexahydrate liquidus (eutectic -49.8/29.9 to 0 C/37.3)
for w0 in [33,36,40]:
    for TC in [-30,-40,-48]:
        we=hexa_liq(TC)/100; w=w0/100
        if w<=we: print(f"brine {w0}% CaCl2 at {TC}: undersaturated"); continue
        x=(w-we)/(1-we*2.0)   # kg CaCl2 crystallised per kg brine (hexahydrate = 1.97 kg per kg CaCl2)
        x=(w-we)/(1-1.973*we)
        left=1-1.973*x
        print(f"brine {w0}% CaCl2 cooled to {TC} C: Ca removed {x/w*100:.0f}%, liquid left {left*100:.0f}% -> Li x{1/left:.2f}")
# Niche: freeze-concentrate Ca-free LiCl eluate with plain -40 C air vs RO + MVR
for el in [0.3,0.6]:
    V=188/el  # m3 eluate per t LCE
    ro_perm=V*(1-el/6.0)  # RO to 6 g/L Li
    evap=V*el/6.0*(1-6/25)
    for p in [0.08,0.30]:
        cost=V*(4*p+0.25) + evap*(30*p+1.0)   # RO 4 kWh/m3 + $0.25/m3 non-energy; MVR 30 kWh/m3 + $1/m3 capex/upkeep
        print(f"eluate {el} g/L Li, power ${p}/kWh: RO+MVR ${cost:.0f}/t LCE  (eluate {V:.0f} m3/t LCE)")
