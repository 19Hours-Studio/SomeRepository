"""Critic round 3: independent checks of the round-3 answer.
A analytic crease vs solver; B bond-eccentricity moment at clamp lines (new term); C servo reference error;
D gravity torque on hinge seat; E strip-test tension length; F visibility threshold sensitivity; G gas coupling of a press."""
import sys, math, numpy as np
sys.path.insert(0, "../round3"); sys.dont_write_bytecode = True
import scipy.sparse as sp, scipy.sparse.linalg as spl
from budget3 import budget, base3, pess3, Dt, Dg, Dp, Da, q
from design3 import solve
E = 72e9; T = 4000.0
print("A. analytic crease (slope ~ eff*D*max|k'|/T, depth ~ eff*D*dk/T) vs solver, 25/9 ramps R=5.5")
g = solve(5.5e-3, 25e-3, 9e-3); kp = np.abs(np.gradient(g['k'], g['s'])).max()
for pg in (0, 1e-3, 3e-3):
    eff = (Dp*0.2 + Da*0.1 + Dg*pg)/Dt; o = budget(dict(base3, phig=pg))
    print(f"  phi_g {pg:.0e}: eff {eff:.2e}  analytic slope {eff*Dt*kp/T*1e3:.4f} mrad (solver {o['crease']*1e3:.4f}); "
          f"analytic depth {eff*Dt*(1/5.5e-3+1/g['Rn'])/T*1e6:.2f} um (solver {o['depth']*1e6:.2f})")
print(f"  max|k'| = {kp:.0f} 1/m^2, Rn = {g['Rn']*1e3:.1f} mm, l = {math.sqrt(Dt/T)*1e3:.2f} mm")

print("\nB. load enters the stack through its bottom face (wing bond) -> distributed moment c*tau at each clamp line")
def clamp_feature(Ta, ta, Ea, c=38e-6, a=41.7e-3, Lb=6e-3, dx=4e-6):
    Ga = Ea/2.6; EA = 2*E*20e-6 + 6e9*30e-6; lam = math.sqrt(EA*ta/Ga); kf = Ea/(1-0.4**2)/ta
    x = np.arange(-a-Lb, a+Lb+dx/2, dx); n = len(x); u = np.abs(x) - a
    N = np.where(u <= 0, Ta, Ta*np.exp(-np.clip(u, 0, None)/lam))
    kk = np.where(u > 0, kf, 0.0); tau = np.where(u > 0, Ta/lam*np.exp(-np.clip(u, 0, None)/lam), 0.0)
    m = c*tau*np.sign(x)                                   # moment per length, antisymmetric
    # energy sum D/2 w''^2 + N/2 w'^2 + k/2 w^2 - m w'  (FD, w=0 at both far ends, w'=0 via ghost)
    D2 = sp.diags([1, -2, 1], [0, 1, 2], shape=(n-2, n))/dx**2
    D1 = sp.diags([-1, 1], [0, 1], shape=(n-1, n))/dx
    Nm = 0.5*(N[1:]+N[:-1]); mm = 0.5*(m[1:]+m[:-1])
    K = Dt*D2.T@D2*dx + D1.T@sp.diags(Nm)@D1*dx + sp.diags(kk*dx)
    f = D1.T@(mm*dx)
    w = spl.spsolve(K.tocsc(), f); th = np.gradient(w, dx)
    free = np.abs(x) < a - 3*math.sqrt(Dt/Ta)
    return np.abs(th[np.abs(x) < a+Lb-1e-3]).max(), np.abs(w).max(), lam, (kf/(4*Dt))**-0.25
for ta, Ea, name in ((3e-6, 3e9, "thin glassy bond 3 um"), (20e-6, 2e9, "structural epoxy 20 um"), (100e-6, 1e9, "gap-filling wedge 100 um")):
    s0, w0, lam, ib = clamp_feature(T, ta, Ea); s1, w1, *_ = clamp_feature(T*1.025, ta, Ea)
    print(f"  {name:26s}: shear-lag {lam*1e3:.2f} mm, 1/beta {ib*1e3:.3f} mm | static kink {s0*1e3:.3f} mrad, lift {w0*1e6:.2f} um"
          f" | change for dF 2.5%: {abs(s1-s0)*1e3:.4f} mrad  (target 0.024)")
s0, *_ = clamp_feature(T, 20e-6, 2e9)
print(f"  dF that keeps this term <= 0.012 mrad (half budget), 20 um epoxy: {0.012e-3/s0*100:.2f}% of T")

print("\nC. servo reference: capacitor reads glass-to-BRIDGE gap; bridge height vs wing clamp plane is the error")
o = budget(base3); m1 = o['m1']; sl_per_Pa = o['press']/0.05
for eps in (7e-9, 50e-9, 100e-9, 300e-9, 1e-6):
    pe = eps/m1; ob = budget(dict(base3, servo_res=pe))
    print(f"  bridge offset {eps*1e9:6.0f} nm -> {pe:6.3f} Pa equivalent -> pressure term {ob['press']*1e3:.4f} mrad, worst {ob['total']*1e3:.4f} mrad")
print(f"  thermal: 20 K x 8 ppm/K x 2 mm bridge support height = {20*8e-6*2e-3*1e9:.0f} nm; gravity sag mean being cancelled = {q*m1*1e9:.0f} nm")

print("\nD. gravity torque about the hinge (phone held by one half, other half cantilevered)")
Mg = 0.120*9.81*0.040
for kth in (300, 2000, 1e4, 1e5):
    print(f"  joint angular stiffness {kth:8.0f} N m/rad: d(theta) = {Mg/kth*1e3:.4f} mrad -> clamp kink ~{Mg/kth/2*1e3:.4f} mrad")
print(f"  M = {Mg:.3f} N m; kink <= 0.012 mrad needs k_theta >= {Mg/(2*0.012e-3):.0f} N m/rad")
for b, h in ((3e-3, 1e-3), (5e-3, 2e-3), (5e-3, 4e-3)):
    I = b*h**3/12; kt = 3*200e9*I/0.03**3; kth = 2*kt*0.03**2
    print(f"  two 30 mm AlSiC tongues {b*1e3:.0f}x{h*1e3:.0f} mm: tip k {kt/1e6:.2f} N/um, k_theta {kth:.0f} N m/rad -> kink {Mg/kth/2*1e3:.3f} mrad")
print(f"  glass tension as restoring torque: 600 N x eccentricity; for M_g need preload offset >= {Mg/600*1e3:.3f} mm (vs e <= 0.05 mm spec)")

print("\nE. strip test: tension length under self-weight when hung with gravity along the length")
for name, D, w in (("bare 20 um UTG", E*20e-6**3/12, 2500*20e-6*9.81), ("76 um sandwich", Dt, q)):
    Tg = w*0.03; l = math.sqrt(D/Tg); sc = (D/w)**(1/3)
    print(f"  {name}: T at clamp {Tg:.4f} N/m, l = {l*1e3:.3f} mm; free-curling tip length ~{sc*1e3:.2f} mm "
          f"-> tip offset ~{6e-4/5.5e-3*min(sc,0.03)**2/2*1e6:.3f} um (vs 49 um unloaded)")

print("\nF. visibility threshold: reflected deviation = 2*theta; vernier optimum 3-5 arcsec")
ARC = 206265
for arcs in (10, 5, 3):
    th = arcs/2/ARC
    print(f"  {arcs:2d}\" -> theta {th*1e3:.4f} mrad: nominal 0.0197 {'passes' if 0.0197e-3<=th else 'fails x%.1f'%(0.0197e-3/th)},"
          f" R=7/50 mm 0.0152 {'passes' if 0.0152e-3<=th else 'fails x%.1f'%(0.0152e-3/th)}")

print("\nG. press on a sealed 5 um gas film: displaced volume vs gas volume")
A = 0.083*0.15; V = A*5e-6; P0 = 101.3e3
for F in (0.05, 0.5, 1.0):
    Vd = F*0.0417**2/(4*T)           # membrane point-load dimple volume, no gas
    dP = F/A                         # if the gas carries it all (stiff limit), uniform overpressure
    print(f"  F {F:.2f} N: free dimple volume {Vd*1e9:.2f} mm3 = {Vd/V*100:.1f}% of gas -> gas would add {P0*Vd/V:.0f} Pa; "
          f"stiff limit {dP:.0f} Pa uniform -> rest of zone bulges, mean {dP*m1*1e6:.2f} um while pressed")
