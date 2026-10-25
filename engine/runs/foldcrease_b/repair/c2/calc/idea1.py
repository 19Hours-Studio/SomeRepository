# Idea 1: centre-pinned, capillary-wrung fluid laminate (repair of the unbonded sliding bend zone)
import numpy as np
pi=np.pi
E_g,nu_g=72e9,0.22        # alkali-aluminosilicate UTG
E_pi=5e9                  # PI/OLED panel effective modulus (approx)
def D(E,t,nu=0.3): return E*t**3/(12*(1-nu**2))
R=3.5e-3                  # waterdrop bend radius chosen (round 2)
t_cg,t_oled,t_bg,h=50e-6,25e-6,30e-6,3e-6
print("== per-layer bending strain t/2R (each layer about own neutral axis)")
for n,t,lim in [("cover UTG",t_cg,None),("OLED-on-PI",t_oled,0.005),("back UTG",t_bg,None)]:
    e=t/(2*R); print(f"{n:12s} t={t*1e6:.0f}um strain={e*100:.2f}%", f"stress={E_g*e/1e6:.0f}MPa" if lim is None else f"(CPI zero-residual threshold ~{lim*100:.1f}%, Korean CPI study R_crit~5mm)")
# bonded-stack comparison: OLED offset from composite neutral axis by ~100um in a ~250um stack
print("bonded-stack OLED strain if 100um off neutral axis at R=2mm:",f"{100e-6/2e-3*100:.1f}%")
print("\n== round1 killer: both-ends bonded mismatch  pi*d/L")
d=t_cg/2+h+t_oled/2; L=15e-3
print(f"d={d*1e6:.0f}um mismatch={pi*d/L*100:.2f}% vs clamped Euler pi^2 t^2/(3L^2)={pi**2*t_oled**2/(3*L**2)*100:.5f}%  -> buckles (killer confirmed)")
print("\n== round2 fix: every layer pinned only at the fold axis (tabs at short-edge bezel), outer long edges free in a reservoir groove")
for n,dd in [("cover-OLED",t_cg/2+h+t_oled/2),("cover-backUTG",t_cg/2+h+t_oled+h+t_bg/2)]:
    print(f"{n}: edge slip per side pi*d/2 = {pi*dd/2*1e6:.0f} um (reservoir groove 500 um)")
dT=60; print(f"thermal slip glass vs Al frame over 70 mm half-width, dT=60K: {(23e-6-8.5e-6)*dT*0.07*1e6:.0f} um (free, no stress)")
gam=0.021  # phenylmethyl silicone surface tension ~21 mN/m
p=2*gam/h; print(f"\n== capillary clamp p=2g/h = {p/1e3:.1f} kPa (open meniscus, fully wetting)")
# set-layer lift height between two glasses: delta ~ 0.5*D*k0^2/p (one-sided couple model, coefficient from beam couple a=sqrt(2M/p))
Do=D(E_pi,t_oled)
for f in [0.01,0.05,0.10,0.20]:
    k0=f/R; dl=0.5*Do*k0**2/p
    print(f"OLED residual fraction f={f:.2f}: k0={k0:.1f}/m lift={dl*1e9:.0f} nm")
# viscous drag during fold -> compressive force in OLED
eta=0.125; slip=pi*(t_cg/2+h+t_oled/2)/2; tf=0.3
tau=eta*(slip/tf)/h; F=2*tau*0.07
Ncr=pi**2*Do/(4*0.07**2)
print(f"\n== drag: eta={eta}Pa s, v={slip/tf*1e3:.2f}mm/s, tau={tau:.1f}Pa, N={F:.2f}N/m (x5 at -20C: {5*F:.1f}) vs free Euler {Ncr:.4f}N/m -> needs the 3um two-sided sandwich constraint (max buckle amplitude 3um, fluid must flow out)")
# squeeze-film time for a buckle of width w to open by dh against p
w=2e-3; ts=eta*w**2/(h**2*p)
print(f"Reynolds time to open a {w*1e3:.0f}mm buckle in a {h*1e6:.0f}um film against {p/1e3:.0f}kPa ~ {ts:.1f}s >> fold transient {tf}s")
print("\n== optics (Fresnel at interfaces)")
def Rf(a,b): return ((a-b)/(a+b))**2
for n,a,b in [("UTG/fluid(DC550 1.49)",1.51,1.49),("UTG/fluid(DC710 1.533)",1.51,1.533),("fluid/TFE SiNx",1.49,1.85),("OCA/TFE SiNx (baseline)",1.48,1.85),("air gap (if dewets)",1.51,1.0)]:
    print(f"{n:26s} R={Rf(a,b)*100:.4f}%")
print("\n== geometric crease from hinge (floating sandwich over non-contact bend-zone plates)")
Dt=D(E_g,t_cg,nu_g)+D(E_g,t_bg,nu_g)+Do
Ls=15e-3
q=2500*9.81*(t_cg+t_bg)+1400*9.81*t_oled
print(f"D_total={Dt:.2e} N m; self-weight sag over {Ls*1e3:.0f}mm clamped = {q*Ls**4/(384*Dt)*1e9:.0f} nm")
P=1.0; print(f"1 N touch -> free deflection {P*Ls**2/(192*Dt)*1e3:.2f} mm, so it bottoms on plates at clearance; force to close 20um gap = {20e-6*192*Dt/Ls**2*1e3:.0f} mN")
s_t=np.deg2rad(0.02)
print(f"slope target 0.02deg={s_t*1e3:.2f} mrad -> wing dihedral error <= {np.rad2deg(s_t):.3f} deg; wing height offset <= {s_t*Ls/1.5*1e6:.1f} um; hard-stop face tolerance over 5mm lever <= {s_t*5e-3*1e6:.2f} um")
# Archard wear on hard stops over 2000 cycles
k=1e-15; F=5; s=0.2e-3*2000; A=2e-6
print(f"hard-stop wear (k=1e-15 m3/Nm, 5N, 0.2mm slide/cycle, 2000 cyc) depth={k*F*s/A*1e9:.2f} nm")
# fluid inventory
A=0.15*0.14; V=2*A*h; print(f"\nfluid volume 2 films = {V*1e6:.3f} mL, mass {V*1070*1e3:.2f} g; back UTG mass {A*t_bg*2450*1e3:.2f} g")
# thickness vs Fold-type bonded stack (PET50+OCA25 adh+UTG30+OCA50+pol-free OLED30+OCA25+PI back film50)
base=50+25+30+50+30+25+50; new=50+3+25+3+30
print(f"active stack thickness: bonded ~{base} um vs wrung {new} um")
