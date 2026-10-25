"""Round-3 side checks: glass stress (open-state membrane + CT, folded bulb/neck), flaw thresholds; spring at 600 N;
finger/backstop with 5 um gap; particle embedding in skin; seal-leak and piezo stroke for the servo; Hertz at the seat;
strip test (edge-on) signal; opening work."""
import numpy as np, math
E=72e9; tg=20e-6; c=38e-6; R=5.5e-3; Rn=16.7e-3; T=4000; W=0.15; EA=2*E*tg+6e9*30e-6
def ct(CS,DOL,t): return CS*DOL/(t-2*DOL)
def acrit(cz,Rb,CS,DOL,t,Kt,mem=0.0):
    a=np.linspace(0.02e-6,9e-6,9000); sb=E*(cz-a)/Rb+mem; res=np.where(a<DOL,-CS*(1-a/DOL),ct(CS,DOL,t))
    K=1.12*np.clip(sb+res,0,None)*np.sqrt(np.pi*a); j=np.argmax(K>=Kt*1e6); return a[j]*1e6 if K[j]>=Kt*1e6 else float('nan')
sm=T/EA*E
print(f"A. open state T={T} N/m: membrane strain {T/EA*1e2:.3f}%, glass membrane {sm/1e6:.0f} MPa, frame load {T*W:.0f} N")
for CS,DOL in ((700e6,3e-6),(700e6,2.5e-6),(800e6,2.5e-6)):
    print(f"  CS {CS/1e6:.0f}/DOL {DOL*1e6:.1f}: CT {ct(CS,DOL,tg)/1e6:.0f} MPa, sustained core tension open {ct(CS,DOL,tg)/1e6+sm/1e6:.0f} MPa;"
          f" folded: bulb inner face {E*c/R/1e6:.0f} MPa flaw K_th/K_IC {acrit(c,R,CS,DOL,tg,0.3):.2f}/{acrit(c,R,CS,DOL,tg,0.7):.2f} um;"
          f" neck user face {E*c/Rn/1e6:.0f} MPa {acrit(c,Rn,CS,DOL,tg,0.3):.2f}/{acrit(c,Rn,CS,DOL,tg,0.7):.2f} um;"
          f" open user face (membrane only) {acrit(0,1e9,CS,DOL,tg,0.3,mem=sm):.2f} um")
print("\nB. tension spring (flexure carriage), AlSiC/Ti housing")
F=T*W
for k in (800.0,1200.0):
    pre=F/k; mis=(0.5e-6)*35*0.083; print(f"  rate {k:.0f} N/mm: preload deflection {pre:.2f} mm; 35 K x 0.5 ppm/K mismatch over 83 mm = {mis*1e6:.1f} um -> dF {k*mis*1e3:.1f} N ({k*mis*1e3/F*100:.2f}%)")
st=T/EA*0.083; print(f"  glass stretch over 83 mm free span {st*1e6:.0f} um; stored energy 0.5*F*stretch = {0.5*F*st*1e3:.0f} mJ; cam work to release/apply ~F*stretch = {F*st*1e3:.0f} mJ")
print(f"  5% spring stress relaxation over life: crease and pressure terms scale x1.05; bow term in budget uses dF")
print("\nC. finger and backstop (gap h)")
for h in (5e-6,8e-6):
    d1=1/(2*math.pi*T)*math.log((0.0417)/4e-3); print(f"  h {h*1e6:.0f} um: 1 N on tensioned span ~{d1*1e6:.0f} um/N -> lands on skin at {h/d1:.3f} N")
Es=1e6; t_s=0.2e-3; p=1/(math.pi*(4e-3)**2); print(f"  1 N over r=4 mm on 0.2 mm skin E=1 MPa (confined, x3): {p/(3*Es)*t_s*1e6:.1f} um extra -> total give ~h+{p/(3*Es)*t_s*1e6:.0f} um at 1 N")
for hp in (5e-6,10e-6,20e-6):
    Ft=2*math.pi*T*hp/math.log(0.0417/5e-6); Est=Es/(1-0.25); rr=hp/2
    dd=(9*Ft**2/(16*Est**2*rr))**(1/3)
    print(f"  particle {hp*1e6:.0f} um proud: tent force {Ft*1e3:.1f} mN; Hertz sink into 1 MPa skin {dd*1e6:.0f} um (>= particle size -> embeds)")
print("\nD. servo/gas cushion budget")
m1=1.372e-7; A=0.083*W; P0=101.3e3
for tau_h in (8,):
    dV=2e-6*A; Q=dV/(tau_h*3600); print(f"  leak spec: hold +1.5 Pa for {tau_h} h with <=2 um piezo stroke -> R_leak >= {1.5/Q:.1e} Pa s/m3 (leak <= {Q*1e9*3600:.2f} mm3/h)")
print(f"  stroke needs: thermal (gas+structure) 0.017 um/K x 20 K = 0.34 um; barometric 3600 Pa -> {3600/(P0/5e-6)*1e6:.2f} um; gravity flip 2q -> {2*1.475*m1*1e6:.2f} um")
print(f"  capacitive mean-gap sensor: C = eps0 A/h = {8.85e-12*A/5e-6*1e9:.0f} nF; 1 nm of gap = {1e-9/5e-6*1e6:.0f} ppm of C = {1e-9/m1:.4f} Pa")
print("\nE. kinematic seat contacts: 600 N over 3 contacts, Si3N4 on WC")
Es=1/((1-0.27**2)/310e9+(1-0.22**2)/600e9)
for Rb in (2e-3,10e-3,20e-3):
    Fc=200; p=(6*Fc*Es**2/(math.pi**3*Rb**2))**(1/3); print(f"  ball R {Rb*1e3:.0f} mm: Hertz peak {p/1e9:.1f} GPa")
print("\nF. strip test (phi_g), strip held edge-on (bending plane horizontal, gravity in-plane) vs horizontal")
for name,EI,m in (("bare 20 um UTG",E*tg**3/12,2500*tg*9.81),("sandwich 76 um",2.372e-3,(2500*40e-6+1400*36e-6)*9.81)):
    L=30e-3; sag=m*L**4/(8*EI); print(f"  {name}: horizontal 30 mm tail self-sag {sag*1e6:.0f} um; edge-on: 0 (in-plane stiffness); "
                                      f"signal at phi_g 6e-4, R 5.5 mm: {6e-4/5.5e-3*L**2/2*1e6:.0f} um, at 1e-4: {1e-4/5.5e-3*L**2/2*1e6:.1f} um")
