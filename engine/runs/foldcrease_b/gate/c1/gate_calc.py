import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve
# layers (t m, E Pa) - typical foldable stack, decoupled by soft OCA (favourable to tension ideas)
L = {'UTG':(30e-6,70e9),'PET_cover':(50e-6,4e9),'panel_PI+TFT':(30e-6,8e9),'backfilm_PET':(50e-6,4e9)}
nu=0.25
D = sum(E*t**3/12/(1-nu**2) for t,E in L.values())
EA = sum(E*t for t,E in L.values())
print(f"D_decoupled={D:.3e} N.m  EA={EA:.3e} N/m")
# crease width from HTX: depth 167um, slope 1.24 deg -> Gaussian sigma
A=167e-6; s=np.tan(np.radians(1.24)); sigma=0.607*A/s
print(f"Gaussian sigma from HTX = {sigma*1e3:.2f} mm")
def flatten(T, sigma, A=167e-6, n=2001, Lx=0.08):
    x=np.linspace(-Lx/2,Lx/2,n); h=x[1]-x[0]
    w0=A*np.exp(-x**2/2/sigma**2)
    d4=diags([1,-4,6,-4,1],[-2,-1,0,1,2],shape=(n,n))/h**4
    d2=diags([1,-2,1],[-1,0,1],shape=(n,n))/h**2
    K=(D*d4 - T*d2).tocsc()
    w=spsolve(K, D*(d4@w0))
    return w.max()-w.min()  # peak-to-valley (approx; ends pinned ~0)
# validation: T=0 must return A
print("check T=0 depth um:", flatten(0,sigma)*1e6)
# validation vs Fourier single-mode analytic: w=w0/(1+T/(D k^2)) for long sinusoid -> test sinusoid
for T in [0,100,1000,3000,10000,20000]:
    print(f"T={T:6d} N/m depth={flatten(T,sigma)*1e6:7.2f} um  glassStress={T*L['UTG'][1]*L['UTG'][0]/EA/L['UTG'][0]/1e6:6.1f} MPa strain={T/EA*100:.3f}%")
from scipy.optimize import brentq
for target in [1,20]:
    T=brentq(lambda T: flatten(T,sigma)*1e6-target, 1, 1e6)
    print(f"T for {target}um: {T:.0f} N/m, glass stress {T*70e9/EA/1e6:.0f} MPa, strain {T/EA*100:.3f}%")
# OCA shear lag: G at 60C 20-45 kPa (patent 11348487 family), h=25um
for G in [20e3,45e3]:
    lam=np.sqrt(EA*25e-6/G); print(f"G={G/1e3:.0f}kPa shear-lag length {lam*1e3:.1f} mm")
# Idea4: 0.1% tension
T4=0.001*EA; lam=np.sqrt(EA*25e-6/30e3)
print(f"Idea4 T=0.1%*EA={T4:.0f} N/m; peak OCA shear ~T/lam={T4/lam/1e3:.0f} kPa; depth under it {flatten(T4,sigma)*1e6:.1f} um")
# sustained OCA shear known: patent creep test 10.5 kPa -> 10-30% creep in 10 min at 60C
Tsus=10.5e3*lam; print(f"T sustainable at 10.5kPa peak: {Tsus:.0f} N/m -> depth {flatten(Tsus,sigma)*1e6:.1f} um (from 167)")
# strain per layer at radius R (each layer about own midplane)
for R in [1.5e-3,3e-3,5e-3]:
    print(f"R={R*1e3}mm", {k:round(t/2/R*100,2) for k,(t,E) in L.items()}, "60um bonded:",round(60e-6/2/R*100,2),"%")
# Idea3: depth from unrecovered fraction f of 180deg bend over arc pi*R: sagitta ~ s*theta/8 (check: circle)
R=5e-3; s=np.pi*R
for f in [0.0032,0.1,0.33]:
    th=np.pi*f; Rc=s/th; sag=Rc*(1-np.cos(th/2)); print(f"f={f}: residual angle {np.degrees(th):.1f} deg, free sagitta {sag*1e6:.0f} um")
