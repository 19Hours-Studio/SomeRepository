import numpy as np
E_g,t_g=70e9,45e-6; EA_g=E_g*t_g; W=0.150   # fold-line length (display height) m, assumption ~Fold7 inner display
print("== IDEA 1: UTG-as-tendon ==")
T=2000.0
print(f"T={T} N/m: glass stress {T/t_g/1e6:.1f} MPa, strain {T/EA_g*100:.3f}%, total rail force {T*W:.0f} N, glass stretch over 150mm {T/EA_g*0.15e6:.0f} um")
# shear lag of tension from edge grip to fold through interlayer of modulus G, thickness h; half-width 75 mm
L=0.075
for name,G,h in [("acrylic OCA 60C (FACT1)",5e4,25e-6),("silicone OCA",1e4,25e-6),("silicone optical gel",2e3,50e-6)]:
    ell=np.sqrt(EA_g*h/G); frac=1/np.cosh(L/ell)
    tau=T/ell*np.tanh(L/ell)  # peak shear at grip edge
    print(f" {name:26s} ell={ell*1e3:6.1f} mm  fraction of edge tension reaching fold={frac:.2f}  peak sustained shear {tau/1e3:.1f} kPa (vs G {G/1e3:.0f} kPa -> strain {tau/G*100:.0f}%)")
# static fatigue of glass under sustained tension in open state (stress-corrosion exponent n)
for n in [15,20,30]:
    t_life=3*365*24*3600*0.8; t_ref=10
    print(f" n={n}: required short-term (10 s) strength for {T/t_g/1e6:.0f} MPa over 3 y open = {T/t_g/1e6/(t_ref/t_life)**(1/n):.0f} MPa")
# thermal: Al vs Ti frame, force-controlled spring with stroke s
for frame,a in [("Al",23e-6),("Ti",8.6e-6)]:
    d=abs(a-8e-6)*40*0.15
    print(f" {frame} frame: thermal mismatch over 40K & 150 mm = {d*1e6:.0f} um ; spring stroke for +-10% force = {d/0.1*1e3:.2f} mm")
# cycling: glass sees tension only flat; bending stress at R=3 when folded (tension released)
print(f" UTG bending stress R=3: {E_g*t_g/6e-3/(1-0.22**2)/1e6:.0f} MPa ; R=2: {E_g*t_g/4e-3/(1-.22**2)/1e6:.0f} MPa (shipping range)")
# thickness penalty: teardrop bulb inner diameter ~2R + 2*(stack+plate)
for R in [2,3,4.2,5]:
    print(f" R={R}: hinge spine thickness ~ {2*R+2*(0.25+0.15)+2*0.5:.1f} mm (Fold7 closed 8.9 mm)")
print("\n== IDEA 2: per-layer sub-creep budget ==")
for eps_c in [0.0025,0.003,0.005]:
    for tmax in [25,38,60]:
        print(f" eps_c60={eps_c*100:.2f}% thickest polymer layer {tmax}um -> R_min={tmax*1e-3/(2*eps_c):.1f} mm")
# OCA lock-in shear stress (locked when opened after hold): tau = r*G*gamma, gamma = pi*d/(2h)
d=65e-6
for name,G,r,h in [("acrylic OCA (FACT1)",5e4,0.45,25e-6),("silicone OCA",1e4,0.15,25e-6),("silicone gel",2e3,0.10,50e-6)]:
    g=np.pi*d/2/h; print(f" {name:20s} gamma={g*100:.0f}%  locked shear {r*G*g/1e3:.2f} kPa")
