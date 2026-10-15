# Idea 3: self-charging (Kelvin-dropper-like) tribo separator cascade for spodumene, -40 C air warmed by mill heat
import math
eps0=8.854e-12; g=9.81
rho_p=3150.0     # spodumene density kg/m3 (quartz 2650, feldspar 2560)
d=300e-6; r=d/2
# Gauss limit of surface charge (air breakdown ~3 MV/m at STP; x1.2 at -40 C density)
Eb=3.0e6*1.2
qmax=3*eps0*Eb/(r*rho_p)
print(f"Gauss-limit q/m at 300 um: {qmax*1e6:.0f} uC/kg; 5% of it = {0.05*qmax*1e6:.1f} uC/kg")
q=1.0e-5  # C/kg (typical tribo minerals 1-10 uC/kg)
# terminal settling velocity in -40 C air (rho_a 1.51, mu 1.52e-5)
rho_a=1.51; mu=1.52e-5
v=1.0
for _ in range(200):
    Re=rho_a*v*d/mu
    Cd=24/Re*(1+0.15*Re**0.687)+0.42/(1+42500*Re**-1.16)
    v=math.sqrt(4*g*d*(rho_p-rho_a)/(3*rho_a*Cd))
print(f"terminal velocity 300 um spodumene in -40 C air {v:.2f} m/s, Re {rho_a*v*d/mu:.0f}")
# lateral drift: simulate 2D motion with drag
def drift(E,H,q=q,v0=0.5):
    x=0;y=0;vx=0;vy=v0;dt=1e-4;t=0
    m=rho_p*math.pi/6*d**3
    while y<H:
        vrel=math.hypot(vx,vy); Re=max(rho_a*vrel*d/mu,1e-6)
        Cd=24/Re*(1+0.15*Re**0.687)+0.42/(1+42500*Re**-1.16)
        Fd=0.5*rho_a*Cd*math.pi*r*r*vrel
        ax=q*E-Fd*vx/m; ay=g-Fd*vy/m
        vx+=ax*dt; vy+=ay*dt; x+=vx*dt; y+=vy*dt; t+=dt
    return x,t
for E,H in [(3e4,1.5),(3e4,3.0),(3e5,1.5),(3e5,3.0),(2e5,2.0)]:
    x,t=drift(E,H)
    print(f"E={E/1e3:.0f} kV/m H={H} m: lateral drift {x*100:.1f} cm in {t:.2f} s")
# space-charge-limited throughput per m of plate width (unipolar cloud after separation; allow space-charge field 30% of E)
def thru(E,q=q,vfall=None,alpha=0.3):
    vfall=vfall or v
    return 2*alpha*eps0*E*vfall/q  # kg/s per m
for E in [3e4,1e5,3e5]:
    m=thru(E); print(f"E={E/1e3:.0f} kV/m: space-charge-limited feed {m:.3f} kg/s/m = {m*3.6:.2f} t/h per m width")
# plant: 1 Mt/yr ore, 7000 h, circulating load 7.2x -> stage throughput
feed=1e6/7000; stage_total=feed*7.2
for E in [3e4,3e5]:
    w=stage_total/(thru(E)*3.6)
    print(f"E={E/1e3:.0f} kV/m: total plate width needed {w:.0f} m (sum over 9 stages), {w/9:.0f} m per stage")
# self-excitation: charge current vs leakage at operating voltage
for E,gap in [(3e4,1.5),(3e5,0.3)]:
    V=E*gap; I=q*thru(E)  # A per m width (collected charge flux, one polarity)
    Rmin=V/I
    print(f"E={E/1e3:.0f} kV/m gap {gap} m: V={V/1e3:.0f} kV, charging current {I*1e6:.2f} uA/m, leakage must exceed {Rmin:.1e} Ohm per m width")
# charge carried out of HV bin by product if grains equilibrate with bin potential (worst case, conductive grains)
C=4*math.pi*eps0*r; m1=rho_p*math.pi/6*d**3
for V in [45e3,90e3]:
    print(f"bin at {V/1e3:.0f} kV: conductive grain would leave with {min(C*V, qmax*m1)/m1*1e6:.0f} uC/kg (cap at Gauss limit) vs {q*1e6:.0f} uC/kg delivered -> need grain-bin charge exchange < {q/min(C*V/m1,qmax)*100:.1f}% ")
# insulating grain relaxation time at -40 C dry: eps_r 6, bulk/surface resistivity 1e12-1e14 Ohm m
for rho_e in [1e10,1e12,1e14]:
    print(f"grain resistivity {rho_e:.0e} Ohm m -> charge relaxation {6*eps0*rho_e:.1e} s")
# humidity / drying
def esat_ice(T): return 611.2*math.exp(22.46*T/(272.62+T))
def esat_w(T): return 611.2*math.exp(17.62*T/(243.12+T))
e=0.9*esat_ice(-40)
for T in [0,20,40]:
    RH=e/esat_w(T); cap=(esat_w(T)-e)*0.018/(8.314*(T+273.15))*1000  # g/m3 pick-up to saturation
    print(f"-40C air (90%RHi) warmed to {T} C: RH {RH*100:.1f}%, can pick up {cap:.1f} g/m3 -> 690 m3/t removes {cap*690/1000:.1f} kg water/t ore ({cap*690/1e4:.2f}% moisture)")
# drying heat to remove 2% moisture with air heated to 40 C
air=20/ (( esat_w(40)-e)*0.018/(8.314*313.15))/1  # m3 per kg... per 20 kg water
print(f"air to remove 20 kg/t water at 40C saturation: {20/((esat_w(40)-e)*0.018/(8.314*313.15)):.0f} m3/t")
Q=(690*1.45*1.005*80+20*2830)/1000
print(f"heat for 690 m3/t warmed -40->40 C + 20 kg/t sublimation/evap: {Q:.0f} MJ/t ore; dry grinding to 300 um ~12-15 kWh/t = {12*3.6:.0f}-{15*3.6:.0f} MJ/t")
