import math
eps0=8.854e-12; g=9.81
# --- max charge
for rho,lab in ((3150,'spodumene'),(2650,'quartz')):
    d=300e-6; Emax=3e6
    q=eps0*Emax*math.pi*d**2; m=rho*math.pi*d**3/6
    print("%s 300um: q/m max %.0f uC/kg ; 5%% = %.1f uC/kg"%(lab,q/m*1e6,0.05*q/m*1e6))
qm=10e-6; h=1.5; V=45e3
# --- vacuum drift, from rest
t=math.sqrt(2*h/g)
for gap in (1.0,0.5,0.26,0.2):
    E=V/gap; d=0.5*qm*E*t**2
    print("gap %.2f m: E=%.0f kV/m drift %.3f m (vacuum, from rest)"%(gap,E/1e3,d))
for d in (0.3,0.6):
    print("drift %.1f m needs E=%.0f kV/m and (gap>=drift) V>=%.0f kV"%(d,d*g/(qm*h)/1e3,d*d*g/(qm*h)/1e3))
print("max drift at 45 kV (gap = drift): %.3f m"%math.sqrt(V*qm*h/g))
# --- with air drag (300 um sphere, rho 2900, air at 0 C)
def simulate(E,rho=2900,d=300e-6,v0=0.0,qm=10e-6):
    mu=1.72e-5; rhoa=1.29; m=rho*math.pi*d**3/6; A=math.pi*d**2/4
    x=y=0.0; vx=0.0; vy=v0; dt=1e-4; tt=0
    while y<h:
        v=math.hypot(vx,vy); Re=rhoa*v*d/mu+1e-9
        Cd=24/Re*(1+0.15*Re**0.687)
        F=0.5*rhoa*Cd*A*v
        ax=qm*E - F*vx/m; ay=g - F*vy/m
        vx+=ax*dt; vy+=ay*dt; x+=vx*dt; y+=vy*dt; tt+=dt
    return x,tt,vy
for gap in (0.26,0.5,1.0):
    for v0 in (0.0,1.5):
        x,tt,vy=simulate(V/gap,v0=v0)
        print("with drag: gap %.2f m E=%.0f kV/m v0=%.1f: drift %.3f m, fall time %.2f s, exit v %.2f m/s"%(gap,V/gap/1e3,v0,x,tt,vy))
# --- self-charging time
for C in (60e-12,150e-12,300e-12):
    Q=C*V
    I=Q/1.4
    print("C=%.0f pF: charge %.1f uC; in 1.4 s needs net current %.1f uA = %.2f kg/s of grains delivering 10 uC/kg"%(C*1e12,Q*1e6,I*1e6,I/qm))
print("leakage at 1e10 ohm, 45 kV: %.1f uA"%(V/1e10*1e6))
# --- space charge of the separated streams (each stream is a charged sheet)
for E_app in (100e3,180e3):
    for frac in (0.1,0.3):
        sigma=frac*E_app*eps0
        v=3.0
        mdot=sigma*v/qm  # kg/s per m width per stream
        print("applied %.0f kV/m, counter-field <=%.0f%%: max %.3f kg/s per m per stream -> total %.2f t/h per m width"%(E_app/1e3,frac*100,mdot,2*mdot*3.6))
# plant throughput
for Mt in (0.5,1.0):
    tph=Mt*1e6/8000
    print("%.1f Mt/yr ore = %.0f t/h; x7.2 circulating = %.0f t/h of stage throughput"%(Mt,tph,tph*7.2))
# --- humidity / mill heat / ore moisture
def psat_ice(T): return 611.15*math.exp(22.452*(T-273.15)/(T-0.61))
def psat_w(T): return 611.21*math.exp((18.678-(T-273.15)/234.5)*((T-273.15)/(257.14+T-273.15)))
pv=0.9*psat_ice(233.15)
print("vapour p at -40C, 90%% RH(ice): %.1f Pa ; RH at 0C = %.2f%%"%(pv,100*pv/psat_w(273.15)))
Vair=690.0; rho0=101325/(287*273.15); m_air=Vair*rho0
print("690 m3 (0C) = %.0f kg air; heating 40 K needs %.1f MJ/t = %.1f kWh/t"%(m_air,m_air*1.005*40/1e3,m_air*1.005*40/3600))
w_in=0.622*pv/(101325-pv)
for RH in (0.019,0.05,1.0):
    w_cap=0.622*RH*psat_w(273.15)/(101325-RH*psat_w(273.15))
    print("air at 0C, RH %.1f%%: can absorb %.3f kg water per t ore (%.4f%% moisture)"%(RH*100,(w_cap-w_in)*m_air,(w_cap-w_in)*m_air/10))
for moist in (0.005,0.01,0.03):
    print("ore moisture %.1f%%: %.0f kg water/t; latent %.0f MJ/t (= %.1f kWh/t)"%(moist*100,moist*1000,moist*1000*2.83,moist*1000*2.83/3.6))
# Bond energy to grind to 300 um
for Wi in (10,14):
    for F80 in (6000,10000):
        W=10*Wi*(1/math.sqrt(300)-1/math.sqrt(F80))
        print("Bond Wi=%d, F80=%d um -> P80 300 um: %.1f kWh/t (dry x1.3 = %.1f)"%(Wi,F80,W,1.3*W))
