# Idea 3: self-charging (Kelvin-dropper-like) free-fall tribo separator cascade - repair rounds
import numpy as np, math
eps0=8.854e-12; g=9.81
mu=1.6e-5; rho_air=1.29   # air at ~0 C
def drift(E, qm, d=300e-6, rho_p=2900, H=1.5, v0=1.0, dt=1e-4):
    m=rho_p*math.pi*d**3/6
    x=y=0; vx=0; vy=v0
    while y<H:
        vrel=math.hypot(vx,vy); Re=rho_air*vrel*d/mu+1e-9
        Cd=24/Re*(1+0.15*Re**0.687)
        Fd=0.5*rho_air*Cd*math.pi*d**2/4*vrel
        ax=qm*E - Fd*vx/m; ay=g - Fd*vy/m
        vx+=ax*dt; vy+=ay*dt; x+=vx*dt; y+=vy*dt
    return x, vy
print("R1 drift (one side) for qm=10 uC/kg, 300 um, 1.5 m fall:")
for E in (45e3,100e3,150e3,200e3,300e3):
    for v0 in (0.0,1.5):
        x,vy=drift(E,1e-5,v0=v0)
        print(f"  E {E/1e3:.0f} kV/m v0 {v0}: drift {x*100:.1f} cm, exit speed {vy:.2f} m/s")
# design: E=200 kV/m, gap 0.5 m (100 kV), product split needs +/-10 cm separation of opposite-sign streams each side
x,vy=drift(200e3,1e-5,v0=0.5); print(f"design E 200 kV/m gap 0.5 m V=100 kV: drift {x*100:.1f} cm each way -> streams {2*x*100:.0f} cm apart; fits in 25 cm half-gap: {x<0.25}")
print(f"  air breakdown ~3 MV/m; design field is {200e3/3e6*100:.0f}% of it")
# ---- R2 self-excitation current balance at V = 100 kV
V=100e3
for tph_per_m in (0.3,0.5,1.0):
    mdot=tph_per_m/3.6    # kg/s per m width
    I_avail=1e-5*mdot*0.5  # only the net charge sorted to the cross-wired bins; assume half effective
    for Rleak in (1e10,1e11,1e12):
        print(f"  {tph_per_m} t/h/m: charging current {I_avail*1e6:.1f} uA/m vs leakage {V/Rleak*1e6:.2f} uA (R={Rleak:.0e}) -> {'OK' if I_avail>2*V/Rleak else 'FAIL'}")
# energy: gravity supplies charge-lift work
print(f"  charge-lift work qm*V = {1e-5*V:.1f} J/kg vs gravity over 1.5 m {g*1.5:.1f} J/kg (KE at exit ~ {0.5*vy**2:.1f})")
# ---- R3 space charge throughput: separated sheets +/-sigma -> counterfield sigma/eps0 <= f*E
for f in (0.1,0.3):
    for E in (200e3,):
        sigma=f*E*eps0
        vfall=3.5
        mdot=sigma*vfall/1e-5   # kg/s per m width
        print(f"  counterfield <= {f*100:.0f}% of {E/1e3:.0f} kV/m: {mdot*3.6:.2f} t/h per m of plate width")
# ---- R4 cascade with uncertain per-stage split: find stages for >=6% Li2O
def cascade(N, pv, pw, feed_stage, g_feed=0.012, mineral_frac=0.08):  # spodumene ~7.5-8% Li2O pure; 1.2% ore -> 15-16% spodumene
    # steady state counter-current: stage i forward stream (toward concentrate) -> i+1, rejects -> i-1
    xs=g_feed/ mineral_frac  # mass fraction valuable mineral in feed
    F={'v':xs,'w':1-xs}
    out={}
    for comp,p in (('v',pv),('w',pw)):
        # solve linear system: L_i = feed_i + p*L_{i-1} + (1-p)*L_{i+1}
        A=np.zeros((N,N)); b=np.zeros(N)
        for i in range(N):
            A[i,i]=1
            if i>0: A[i,i-1]=-p
            if i<N-1: A[i,i+1]=-(1-p)
        b[feed_stage]=F[comp]
        L=np.linalg.solve(A,b)
        out[comp]=(p*L[-1], (1-p)*L[0], L.sum())
    conc_v,conc_w=out['v'][0],out['w'][0]
    grade=conc_v/(conc_v+conc_w)*mineral_frac
    rec=conc_v/F['v']
    load=(out['v'][2]+out['w'][2])
    return grade,rec,(conc_v+conc_w),load
for pv,pw in ((0.85,0.45),(0.80,0.50),(0.75,0.55)):
    best=None
    for N in range(4,40):
        for fs in range(0,N):
            gr,rec,mass,load=cascade(N,pv,pw,fs)
            if gr>=0.06 and rec>=0.75:
                if best is None or load<best[4]: best=(N,fs,gr,rec,load,mass)
        if best: break
    if best:
        N,fs,gr,rec,load,mass=best
        print(f"split {pv}/{pw}: {N} stages (feed at {fs}) -> {gr*100:.1f}% Li2O, rec {rec*100:.0f}%, mass {mass*100:.1f}%, stage load sum {load:.1f}x feed")
    else: print(f"split {pv}/{pw}: no N<40 reaches 6%/75%")
# ---- R5 moisture: closed air loop through cold trap (outdoor coil at -30 C), heat from genset waste heat
def psat_ice_gm3(Tc):  # g/m3 saturation over ice/water (Magnus)
    T=Tc+273.15
    es = 6.112*math.exp(22.46*Tc/(272.62+Tc)) if Tc<0 else 6.112*math.exp(17.62*Tc/(243.12+Tc))
    return es*100*0.018015/(8.314*T)*1000
for ice_wt in (0.2,0.4,1.0,3.0):
    w=ice_wt*10   # kg/t
    cap=psat_ice_gm3(20)*0.5-psat_ice_gm3(-30)   # g/m3 carried per pass
    V=w*1000/cap
    sens=V*1.2*1.005*50/1000*(1-0.75)   # MJ/t net sensible with 75% recuperator
    lat=w*2.83
    print(f"ore ice {ice_wt}%: water {w:.0f} kg/t, loop air {V:.0f} m3/t, heat {lat+sens:.0f} MJ/t (latent {lat:.0f}); mill heat 21-31 MJ/t; genset waste heat ~{15*1.8*3.6:.0f} MJ/t at 15 kWh/t")
print(f"separator air RH after reheat to +20 C from -30 C trap: {psat_ice_gm3(-30)/psat_ice_gm3(20)*100:.1f}%")
# ---- R6 economics per t Li2O in concentrate at railhead (700 km winter road, $0.15/t-km)
haul=105  # $/t of material
ore_g=0.012
for name,proc,rec,cg in (("A haul raw ore",0,1.0,ore_g),("B DMS+flotation Arctic",45,0.78,0.06),("C XRT sort+DMS (dry-ish)",30,0.70,0.055),("D self-charging cascade",14,0.78,0.06)):
    for capex in ((0,) if name.startswith("A") else (8,16)):
        mass=ore_g*rec/cg
        cost=proc+capex+mass*haul
        print(f"  {name}: proc {proc}+capex {capex} + haul {mass*haul:.1f} = {cost:.0f} $/t ore -> {cost/(ore_g*rec):,.0f} $/t Li2O recovered")
