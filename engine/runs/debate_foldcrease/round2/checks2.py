"""Round-2 side checks: glass stress incl. central tension (edges), surface-flaw thresholds, finger/backstop,
gravity sag, tension hardware, glass-anelasticity budget, reference-glass waviness slope."""
import numpy as np, math
E=72e9
def ct(CS,DOL,t): return CS*DOL/(t-2*DOL)
print("A. Max net tension through the glass cross-section (what an edge flaw sees), linear CS profile + uniform CT")
def edge_max(zin,zout,R,CS,DOL,t):
    z=np.linspace(zin,zout,4001); a=np.minimum(z-zin,zout-z)            # depth from nearer surface
    res=np.where(a<DOL,-CS*(1-a/DOL),ct(CS,DOL,t)); s=E*z/R+res; i=s.argmax(); return s[i]/1e6,(zout-z[i])*1e6
for CS,DOL in ((450e6,6e-6),(700e6,3e-6),(800e6,2.5e-6)):
    t=20e-6; sw=edge_max(18e-6,38e-6,5.5e-3,CS,DOL,t)
    sh=[edge_max(0,15e-6,R,CS,DOL,30e-6) for R in (1.5e-3,2.0e-3)]
    print(f"  CS {CS/1e6:.0f} DOL {DOL*1e6:.1f}: CT(20um) {ct(CS,DOL,20e-6)/1e6:.0f} MPa -> sandwich bottom sheet R5.5 max {sw[0]:.0f} MPa ;"
          f" CT(30um) {ct(CS,DOL,30e-6)/1e6:.0f} -> single 30um UTG R1.5 {sh[0][0]:.0f} / R2.0 {sh[1][0]:.0f} MPa")
print("\nB. Surface-flaw depth reaching K_th 0.3 / K_IC 0.7 MPa sqrt(m) (CT added beyond DOL)")
def acrit(c,R,CS,DOL,t,Kt):
    a=np.linspace(0.02e-6,9e-6,9000); sb=E*(c-a)/R; res=np.where(a<DOL,-CS*(1-a/DOL),ct(CS,DOL,t))
    K=1.12*np.clip(sb+res,0,None)*np.sqrt(np.pi*a); j=np.argmax(K>=Kt*1e6); return a[j]*1e6 if K[j]>=Kt*1e6 else float('nan')
for CS,DOL in ((700e6,3e-6),(800e6,2.5e-6)):
    for name,c,R,t in (("sandwich bulb inner face R5.5",38e-6,5.5e-3,20e-6),("sandwich neck user face Rn20",38e-6,20e-3,20e-6),
                       ("single 30um UTG R1.5",15e-6,1.5e-3,30e-6),("single 30um UTG R2.0",15e-6,2.0e-3,30e-6)):
        print(f"  CS {CS/1e6:.0f}/DOL {DOL*1e6:.1f} {name:32s} applied {E*c/R/1e6:4.0f} MPa: {acrit(c,R,CS,DOL,t,0.3):.2f} / {acrit(c,R,CS,DOL,t,0.7):.2f} um")
print("\nC. Finger on tensioned span (membrane estimate F/(2 pi T) ln(L/2 / r0), r0=4 mm contact) + gravity sag")
EA=2*E*20e-6+6e9*30e-6; q=(2500*40e-6+1400*36e-6)*9.81; L=76e-3
for T in (1000,2000,3000):
    d=1/(2*math.pi*T)*math.log((L/2)/4e-3)
    print(f"  T={T}: 1 N finger -> {d*1e6:.0f} um; lands on 60/100 um backstop at {60e-6/d:.2f}/{100e-6/d:.2f} N;"
          f" gravity sag {q*L**2/8/T*1e6:.2f} um, end slope {q*L/2/T*1e3:.3f} mrad, curvature radius {T/q:.0f} m;"
          f" membrane strain {T/EA*1e6:.0f} ue, glass {T/EA*E/1e6:.0f} MPa, force on 150 mm {T*0.15:.0f} N, stroke over 70 mm {T/EA*70:.0f} um")
print("\nD. Spring sizing for +-20% force over 35 K Al-vs-glass mismatch on 140 mm")
mis=(23e-6-8.5e-6)*35*0.14
for T in (2000,3000): F=T*0.15; k=0.2*F/(mis*1e3); print(f"  T={T}: F={F:.0f} N, rate <= {k:.0f} N/mm, preload deflection >= {F/k:.2f} mm; opening work ~ {F*T/EA*70e-3*1e3:.1f} mJ")
print("\nE. Glass-anelasticity budget, 30 um panel, 15/15 mm ramps (kappa' = (1/5.5+1/20.1)/15 mm), slope ~ sum(phi D)*kappa'/T")
Dg=2.355e-3; kp=(1/5.5e-3+1/20.1e-3)/15e-3
for ps,Dpoly in (("0.05/0.02",0.05*0.0057*2.372e-3+0.02*0.0021*2.372e-3),("0.2/0.1",0.2*0.0057*2.372e-3+0.1*0.0021*2.372e-3)):
    for T in (2000,3000):
        pg=(0.024e-3*T/kp-Dpoly)/Dg; print(f"  polymer {ps}, T={T}: slope<=0.024 mrad needs phi_g <= {pg:.1e}")
    print(f"  polymer {ps}, T=3000, phi_g 1e-2 (Zerodur-like saturation): slope {(Dpoly+Dg*1e-2)*kp/3000*1e3:.3f} mrad")
print("\nF. Reference: display-glass waviness WCA (0.8-8 mm band) as sinusoid, A = pi/2*WCA")
for W in (0.03e-6,0.1e-6,0.15e-6):
    for lam in (8e-3,4e-3): print(f"  WCA {W*1e6:.2f} um, lambda {lam*1e3:.0f} mm: slope amplitude {2*math.pi*(math.pi/2*W)/lam*1e3:.3f} mrad")
