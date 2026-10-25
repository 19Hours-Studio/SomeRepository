"""Order-of-magnitude crease model for foldable display stacks.
Assumptions (all flagged in notes): layers decoupled by soft OCA (each bends about its own
mid-plane), glass and metals elastic, glassy polymers keep a set fraction phi of bending strain.
Residual curvature kappa = sum(D_i*phi_i)/R / sum(D_i); depth ~ kappa*L^2/8, L = fold arc."""
import math
def D(E,t): return E*t**3/12
def run(name,R,layers,Lfac=1.5):
    L=math.pi*R*Lfac; Dtot=sum(D(E,t) for _,E,t,_,_ in layers)
    print(f"\n== {name}: R={R*1e3:.1f} mm, fold arc L={L*1e3:.1f} mm")
    num=0
    for n,E,t,phi,lim in layers:
        eps=t/(2*R); d=D(E,t); num+=d*phi
        print(f"{n:28s} t={t*1e6:5.0f}um eps={eps*100:5.2f}%  sigma={E*eps/1e6:6.0f}MPa  limit={lim}  D-share={d/Dtot*100:5.1f}%")
    k=num/R/Dtot; dep=k*L**2/8; slope=4*dep/L
    print(f"residual kappa={k:.3f} 1/m  depth~{dep*1e6:.1f} um  max slope~{slope*1e3:.2f} mrad ({math.degrees(slope):.3f} deg)")
    return dep
GPa=1e9
for phi in (0.02,0.05,0.10):
    print(f"\n######## polymer set fraction phi={phi}")
    run("Current-like (polymer top film, 45um UTG)",2.0e-3,[
     ("top polymer film (PET/TPU)",4*GPa,60e-6,phi,"PET yield ~3%"),
     ("UTG 45um",72*GPa,45e-6,0,"CS~700MPa"),
     ("panel CPI/TFT/OLED/TFE/touch",6*GPa,30e-6,phi/2,"TFT <~1%"),
     ("back PET film",4*GPa,50e-6,phi,""),
     ("SUS lattice plate (eff E)",4*GPa,100e-6,0,"ligaments local")])
    run("Proposed glass-dominated stack",4.0e-3,[
     ("UTG 70um (no polymer above)",72*GPa,70e-6,0,"CS>=750MPa"),
     ("panel CPI/TFT/OLED/TFE/touch",6*GPa,25e-6,phi/2,"TFT <~1%"),
     ("beta-Ti solid foil 40um",100*GPa,40e-6,0,"yield ~1000MPa")])
# OCA shear: slip = s*theta, independent of R
for s,t in ((100e-6,50e-6),(55e-6,25e-6)):
    print(f"\nOCA slip at fold edge for mid-plane separation {s*1e6:.0f}um: {s*math.pi*1e6:.0f}um, shear strain {s*math.pi/t:.1f} (OCA {t*1e6:.0f}um)")
# visibility target
for dep,L in ((1.5e-6,15e-3),(48e-6,15e-3),(167e-6,15e-3)):
    sl=4*dep/L; print(f"depth {dep*1e6:6.1f}um over {L*1e3:.0f}mm -> slope {sl*1e3:.2f} mrad, reflected-ray deviation {2*sl*1e3*3.438:.1f} arcmin, reflection power {2*8*dep/L**2*1e3:.0f} mD")
