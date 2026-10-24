# Idea 1: liquid-coupled slip stack. All SI units.
import numpy as np
pi=np.pi
def D(E,t,nu): return E*t**3/(12*(1-nu**2))
# --- materials (sources in NOTES.md)
E_g,nu_g=72e9,0.22      # UTG (aluminosilicate)
E_p,nu_p=10e9,0.35      # OLED-on-PI panel effective (PI 6-8 GPa + SiNx/TFT stiffening) -- assumption
t_g=30e-6; t_p=30e-6
Dg=D(E_g,t_g,nu_g); Dp=D(E_p,t_p,nu_p)
print(f"D_UTG={Dg:.2e} N m, D_panel={Dp:.2e} N m, ratio p/(p+g)={Dp/(Dp+Dg):.3f}")

print("\n== R1 original: fluid strip bonded both sides ==")
d=50e-6; slip=pi*d; t_oca=25e-6
print(f"slip pi*d={slip*1e6:.0f} um -> OCA shear gamma={slip/t_oca:.1f} (quoted foldable OCA design range 2.5-4)")
R=2e-3
print(f"if both ends bonded, mismatch spread over arc pi*R: membrane strain={slip/(pi*R)*100:.2f}%  -> FAIL")

print("\n== R2: decouple only UTG/panel, R=3 mm, run slip to perimeter (no bonded edge in view area) ==")
R=3e-3; h=10e-6
for name,t in [("UTG",t_g),("panel",t_p)]:
    print(f"  own-NA bending strain {name}: {t/(2*R)*100:.2f}%")
print(f"  UTG stress {E_g*t_g/(2*R)/1e6:.0f} MPa")
# bonded reference stack ~150 um at R=3mm, fully bonded outer fibre
print(f"  fully bonded 150 um stack outer fibre @R=3mm: {75e-6/R*100:.1f}%")
# sub-stack = panel(30)+PSA(15)+Ti plate(30); NA ~ plate-dominated
z_sub=30e-6+15e-6+15e-6  # panel top to plate mid
d=t_g/2+h+z_sub
edge=pi/2*d
print(f"  d={d*1e6:.0f} um, slip per outer edge (anchor by symmetry at fold line)={edge*1e6:.0f} um, total={2*edge*1e6:.0f} um")
# seal options
G_el,width,height=0.3e6,0.8e-3,20e-6
print(f"  elastomer seal of gap height: gamma={edge/height:.1f} -> FAIL")
height=0.5e-3; G_el=0.05e6; w=0.3e-3
tau=G_el*edge/height; print(f"  tall gel bead: gamma={edge/height:.2f}, line force={tau*w:.2f} N/m")
Ncr=pi**2*Dg/0.07**2; print(f"  UTG Euler N_cr over 70 mm half (no foundation)={Ncr:.2f} N/m  -> gel bead too stiff")
# thin PI loop bellows: cantilever of length Lb, thickness tb
E_pi=3e9; tb=5e-6; Lb=0.5e-3
k=3*E_pi*(tb**3/12)/Lb**3
print(f"  5um PI loop bellows: line force={k*edge:.1e} N/m  (<< N_cr OK)")

print("\n== fluid choice: leveling vs stylus vs fold transient ==")
def tau_level(mu,h,lam): k=2*pi/lam; return 12*mu/(h**3*Dg*k**6)
for mu in [0.1,1,10,100]:
    for h in [10e-6,20e-6]:
        lv=[tau_level(mu,h,l) for l in (1e-3,6e-3,20e-3)]
        v=edge/0.5  # slip in 0.5 s fold
        Ffold=mu*v/h*0.07   # viscous shear x 70 mm flap length -> in-plane line force on UTG
        r=0.5e-3;F=2.0
        tsq=3*mu*pi*r**4/(4*F)*(1/(h/2)**2-1/h**2)
        print(f"  mu={mu:>5} Pa s h={h*1e6:.0f}um: level tau(1/6/20mm)={lv[0]:.1e}/{lv[1]:.1e}/{lv[2]:.1e} s; fold line force={Ffold:.2f} N/m; stylus half-squeeze={tsq*1e3:.2f} ms")
print(f"  stylus bottom-out curvature F/(8 pi D)={2/(8*pi*Dg):.0f} 1/m -> UTG strain {t_g/2*2/(8*pi*Dg)*100:.2f}% (independent of gap)")

print("\n== optics: index match ==")
for nf in [1.40,1.49,1.51]:
    Rf=((1.51-nf)/(1.51+nf))**2
    print(f"  fluid n={nf}: R per interface={Rf:.1e}, fringe amplitude ~2*sqrt(R1R2)={2*Rf:.1e} (vs 4% first surface)")
print(f"  coherence: optical path 2nh(10um)={2*1.51*10:.0f} um vs white-light coherence ~1-2 um")

print("\n== thermal: fluid volume ==")
beta=9.6e-4  # PDMS volumetric CTE /K
for dT in [40,60]: print(f"  dT={dT}K: fluid volume change {beta*dT*100:.1f}% -> {beta*dT*h*1e6:.2f} um uniform gap change at h=10um (needs bellows reservoir)")

print("\n== set budget: sub-stack (panel+PSA+plate) set must stay inside gap ==")
a=pi*R  # set length
for hgap in [10e-6,20e-6]:
    margin=0.5*hgap
    kmax=32*margin/a**2
    print(f"  h={hgap*1e6:.0f}um: allowed sub-stack set depth {margin*1e6:.0f} um -> kappa_res<={kmax:.2f}/m = {kmax*R*100:.2f}% of fold curvature")
# today's phones: ~60 um 'good' crease over ~6 mm at R~1.5 mm
k_now=32*60e-6/(6e-3)**2; print(f"  reference: 60um/6mm crease => kappa={k_now:.0f}/m = {k_now*1.5e-3*100:.0f}% of 1/1.5mm")
# if fluid leveling fails (rigid coupling), UTG follows fraction
Dsub=D(E_p,t_p,nu_p)+D(110e9*0.3,30e-6,0.33)  # Ti plate patterned ~30% effective E
f=Dsub/(Dsub+Dg); print(f"  rigid-coupling worst case: UTG carries {f*100:.0f}% of sub-stack set curvature")
