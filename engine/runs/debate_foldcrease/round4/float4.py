"""Round-4: floating tensioned display. The sandwich is NOT bonded anywhere in the active area. Tension enters at the
two outer edges through two-face (mid-plane-symmetric) clamps under the side bezels; the open display hovers over a
vented, grooved air gap h above the backing (wing plates + rising bridge). With no shear or normal coupling to the
backing, the open shape is: straight chord between the clamps + uniform-pressure parabola + material-set crease.
A  crease options (R, ramps, T, phi_g, polymer set) on the full clamp-to-clamp span; raw max slope and slope after
   (uniform tilt/curvature, e.g. the gravity parabola, appear identically in the non-fold reference zone).
B  every v3 clamp-line term re-expressed for the floating design (what transfers to the glass shape, what only eats gap).
C  edge-clamp tail into the active area (two-face clamp with bond asymmetry), FD model in the critic's form.
D  gap budget (h = 30 um), touch, squeeze film, lift-off time, drum mode, stylus stress.
E  folded-state retention (electroadhesive strips): peel length and lifted-region curvature.
F  visibility thresholds (vernier 3/5/10 arcsec, source-distance factor) and the like-for-like comparison."""
import numpy as np, math, sys
sys.dont_write_bytecode = True
import scipy.sparse as sp, scipy.sparse.linalg as spl
from scipy.linalg import solve_banded
from design2 import shares
from design3 import solve
tp = 30e-6; Dt, Dg, Dp, Da, zt = shares(tp); E = 72e9; c = zt/2
mA = 2500*40e-6 + 1400*36e-6; q = mA*9.81; ARC = 206265.0
HALF = 75e-3                                          # clamp-to-clamp half span (open display ~150 mm across the fold)
EA = 2*E*20e-6 + 6e9*30e-6

def open_theta(kres_s, s, a, T, N=30001):
    x = np.linspace(-a, a, N); dx = x[1]-x[0]; kr = np.interp(x, s, kres_s, left=0, right=0)
    n = N-2; ab = np.zeros((3, n)); ab[0, 1:] = Dt/dx**2; ab[1, :] = -2*Dt/dx**2-T; ab[2, :-1] = Dt/dx**2
    th = np.concatenate([[0], solve_banded((1, 1), ab, Dt*np.gradient(kr, dx)[1:-1]), [0]])
    w = np.concatenate([[0], np.cumsum((th[1:]+th[:-1])/2)*dx]); return x, th, w
def crease(R, L1, L2, T, phig, ps=0.2, pa=0.1):
    g = solve(R, L1, L2); eff = (Dp*ps+Da*pa+Dg*phig)/Dt
    x, th, w = open_theta(eff*g['k'], g['s'], HALF, T)
    return g, np.abs(th).max(), w.max()-w.min(), x, th

if __name__ == "__main__":
    print(f"stack {zt*1e6:.0f} um, D {Dt:.3e} N m, q {q:.3f} Pa, tension length l = sqrt(D/T) = {math.sqrt(Dt/4000)*1e3:.2f} mm at T=4000")
    print("\nA. material-set crease on the clamp-to-clamp span (max |slope| mrad, depth um)")
    geos = [("R5.5 25/9 (v3)", 5.5e-3, 25e-3, 9e-3), ("R5.5 28/12", 5.5e-3, 28e-3, 12e-3), ("R6.0 30/12", 6e-3, 30e-3, 12e-3), ("R7.0 35/12", 7e-3, 35e-3, 12e-3)]
    res = {}
    for name, R, L1, L2 in geos:
        for T in (4000, 5000):
            row = []
            for pg in (0, 5e-4, 1e-3, 3e-3):
                g, sl, d, xx, th = crease(R, L1, L2, T, pg); res[(name, T, pg)] = sl; row.append(f"g{pg:.0e} {sl*1e3:.4f} ({d*1e6:.2f} um)")
            g2, slp, *_ = crease(R, L1, L2, T, 1e-3, 0.5, 0.3); res[(name, T, 'pess')] = slp
            print(f"  {name:15s} T{T}: zone {g['zone']*1e3:.0f} bulb {g['width']*1e3:.1f} Rn {g['Rn']*1e3:.1f} mm | " + " | ".join(row) + f" | pess(0.5/0.3, g1e-3) {slp*1e3:.4f}")
    print("  check vs round-3 wing-clamped span (R5.5 25/9, T4000, g0): round-3 budget3 0.0074 mrad")

    print("\nB. v3 clamp-line terms in the floating design: transfer to glass shape vs gap consumed (h = 30 um)")
    T = 4000.0; L = 2*HALF
    sag = q*L**2/(8*T)
    print(f"  uniform net pressure p (gravity q, vent residual): parabola w = p(a^2-x^2)/2T, curvature p/T = {q/T:.2e} 1/m at p=q"
          f" (R = {T/q/1e3:.1f} km); identical in fold and non-fold zones (no line feature); gravity sag {sag*1e6:.2f} um")
    print("  bond moment c*tau (critic 0.82-0.87 mrad): no bond under the active area -> 0; tension enters at the outer clamps (C)")
    print("  seat kink delta/2 + dh/2a, frame bow, thermal bow, hinge gravity torque: the backing moves, the glass chord does not ->"
          " 0 in shape; each consumes gap (D)")
    print("  servo bridge reference (critic 7 nm): no servo; vented gap -> 0 in shape")

    print("\nC. edge-clamp tail: two-face clamp, jaw bonds 20 um epoxy each face, shear asymmetry eps -> moment eps*c*tau; jaw angle error")
    def clamp_tail(eps, ta=20e-6, Ea=2e9, Lj=3e-3, Lf=40e-3, dx=2e-6, T=4000.0):
        Ga = Ea/2.6; lam = math.sqrt(EA*ta/(2*Ga)); kf = 2*Ea/(1-0.4**2)/ta
        x = np.arange(0, Lf+Lj+dx/2, dx); n = len(x); u = x-Lf             # x<Lf free span (active side), x>Lf inside jaws
        N = np.where(u <= 0, T, T*np.exp(-np.clip(u, 0, None)/lam)); kk = np.where(u > 0, kf, 0.0)
        tau = np.where(u > 0, T/lam*np.exp(-np.clip(u, 0, None)/lam), 0.0); m = eps*c*tau
        D2 = sp.diags([1., -2., 1.], [0, 1, 2], shape=(n-2, n))/dx**2; D1 = sp.diags([-1., 1.], [0, 1], shape=(n-1, n))/dx
        Nm = 0.5*(N[1:]+N[:-1]); mm = 0.5*(m[1:]+m[:-1])
        K = Dt*D2.T@D2*dx + D1.T@sp.diags(Nm)@D1*dx + sp.diags(kk*dx); K = K.tolil(); K[0, :] = 0; K[0, 0] = 1
        f = D1.T@(mm*dx); f[0] = 0
        w = spl.spsolve(K.tocsc(), f); j = np.argmin(np.abs(x-Lf)); th = np.gradient(w, dx)-w[j]/Lf   # relative to chord
        return x, th, Lf
    for eps in (0.05, 0.2):
        x, th, Lf = clamp_tail(eps); mouth = np.abs(th[np.abs(x-Lf) < 0.3e-3]).max()
        o = [f"{d*1e3:.0f} mm: {np.abs(th[np.argmin(np.abs(x-(Lf-d)))])*1e3:.5f}" for d in (1e-3, 2e-3, 3e-3, 4e-3, 5e-3)]
        print(f"  asymmetry {eps:.2f}: slope at mouth {mouth*1e3:.3f} mrad; at distance into active side " + ", ".join(o) + " mrad")
    l = math.sqrt(Dt/4000)
    for d in (3e-3, 4e-3, 5e-3):
        print(f"  jaw angle error 0.2 mrad (hinge deflection, worst) decays e^(-d/l): d {d*1e3:.0f} mm -> {0.2*math.exp(-d/l):.5f} mrad")

    print("\nD. gap budget, h = 30 um (closures, worst sign); backing = lapped AlSiC wings + bridge")
    P0 = 101.3e3; h = 30e-6; M_half = 0.120*9.81*0.040; qb = 0.240*9.81/0.15
    fixed = [("glass gravity sag toward backing", sag), ("wing/bridge flatness (lapped, assumed)", 2e-6),
             ("wing-bridge seam step (coarse, assumed)", 3e-6), ("hinge angular repeat 2 um/30 mm tongue x 37.5 mm", 2e-6/30e-3*37.5e-3),
             ("thermal bow of backing, AlSiC, 300 W/m2", 8e-6/180*300*0.15**2/8)]
    fx = sum(v for _, v in fixed)
    for n_, v in fixed: print(f"  fixed: {n_:52s} {v*1e6:5.2f} um")
    print(f"  fixed sum {fx*1e6:.1f} um; load cases (EI of open body across the fold / hinge k_theta):")
    for EI, kt, lab in ((10.0, 1000.0, "nominal EI 10, k 1000"), (5.0, 300.0, "pessimistic EI 5, k 300")):
        cases = [("on a table / held flat", 0.0),
                 ("held by one half, other cantilevered", M_half/kt*37.5e-3 + 0.120*9.81/0.075*0.075**4/(8*EI)*0),
                 ("held by both outer edges, face-down", 5*qb*0.15**4/(384*EI) + qb*0.15**2/8/kt*37.5e-3),
                 ("held at centre from behind", qb/2*0.075**4/(8*EI) + qb*0.15**2/8/kt*37.5e-3)]
        for cn, v in cases:
            tot = fx+v; print(f"    {lab:24s} {cn:38s}: load {v*1e6:5.1f} + fixed {fx*1e6:4.1f} = {tot*1e6:5.1f} um -> h=30 um margin {30-tot*1e6:5.1f} um")
        print(f"    {lab:24s} extra hand moment across the hinge that closes the remaining gap (nominal hold): "
              f"{(30e-6-fx)/(37.5e-3/kt + 0.15**2/(8*EI))/1:.2f} N m")
    print("  slow-vent cushion (sealed on handling time scales, vent tau ~1 min): glass mean follows backing mean (gas/membrane stiffness")
    a_ = HALF; xg = np.linspace(-a_, a_, 3001); m1 = (2/3)*a_**2/(2*T); print(f"    ratio {P0/h*m1:.0f}); gap used = max(backing - mean-matched parabola) as a fraction of the vented case:")
    shapes = {"self-weight, held by edges (quartic)": (5*a_**4-6*a_**2*xg**2+xg**4),
              "uniform moment (parabola)": a_**2-xg**2, "hinge kink (triangle)": a_-np.abs(xg)}
    for nm, b_ in shapes.items():
        b_ = b_/b_.max(); par = (a_**2-xg**2)/a_**2; par = par*b_.mean()/par.mean(); print(f"    {nm:40s}: {np.max(b_-par)/1:.2f}")
    print("  touch (membrane point load, finger r 4 mm, clamp span 75 mm):")
    for h in (10e-6, 30e-6):
        F = 2*math.pi*T*h/math.log(75e-3/4e-3); print(f"    h {h*1e6:.0f} um: glass lands on backing at {F:.2f} N, then rigid (no foam layer)")
    mu = 1.8e-5; h = 30e-6
    for wg in (1e-3, 5e-3):
        cdamp = mu*wg**2/h**3; kd = T/(10e-3)**2; kfull = 8*T/L**2
        hi = 1e-6; tlift = mu*wg**2/(2*hi**2*kfull*h)
        print(f"    groove pitch {wg*1e3:.0f} mm: squeeze damping {cdamp:.2e} Pa s/m; dimple time {cdamp/kd*1e3:.2f} ms; "
              f"full-span lift-off after tensioning (from 1 um texture) ~{tlift:.2f} s")
    f1 = math.sqrt(T/mA)/(2*L); cd = mu*(5e-3)**2/h**3; print(f"    drum mode f1 {f1:.0f} Hz; damping ratio with 5 mm grooves {cd/(2*mA*2*math.pi*f1):.1f} (overdamped, no buzz)")
    Fs = 3.0; b = math.sqrt(16*math.pi*Dt*h/Fs); kap = 2*h/b**2
    print(f"    stylus 3 N: dimple radius {b*1e3:.2f} mm, curvature ~{kap:.0f} 1/m -> bending {E*c*kap/1e6:.0f} MPa + membrane {T/EA*E/1e6:.0f} MPa on bottom face (CS 700)")

    print("\nE. folded-state retention: glass slack, held on the wings by electroadhesive strips (energised only while folded)")
    for R, Rn, L2 in ((5.5e-3, 20.2e-3, 12e-3), (7e-3, 22.4e-3, 12e-3)):
        V = Dt/(Rn*L2)
        for p in (2e3, 5e3, 20e3):
            ell = 2*V/p; kap = V**2/(2*p)/Dt
            print(f"  R{R*1e3:.1f}: edge shear V = D/(Rn*Lr2) = {V:.1f} N/m; hold {p/1e3:.0f} kPa -> lift-off {ell*1e3:.1f} mm, peak curvature {kap:.1f} 1/m (neck {1/Rn:.0f} 1/m)")
    for Vv, d in ((100, 3e-6), (200, 5e-6)):
        print(f"  ideal parallel-plate electroadhesion {Vv} V across {d*1e6:.0f} um (eps_r 3.5): {8.85e-12*3.5*Vv**2/(2*d**2)/1e3:.0f} kPa (measured conductive targets: 1-100 kPa at 400 V)")

    print("\nF. thresholds and comparison")
    for arcs in (10, 5, 3):
        th_inf = arcs/2/ARC; th_2m = arcs/ARC/(2*2.0/2.3)
        print(f"  {arcs:2d}\" vernier -> surface slope {th_inf*1e3:.4f} mrad (source at infinity), {th_2m*1e3:.4f} mrad (lamp 2 m, eye 0.3 m)")
    print("  worst line feature at the fold (crease; edge tails are a separate location, max 0.0036 mrad at 4 mm, see C):")
    fl = lambda k: res[k]*1e3
    for name, T_ in (("R5.5 25/9 (v3)", 4000), ("R5.5 28/12", 4000), ("R5.5 28/12", 5000), ("R7.0 35/12", 4000), ("R7.0 35/12", 5000)):
        print(f"    v4 {name:15s} T{T_}: phi_g 0 {fl((name,T_,0)):.4f}, 5e-4 {fl((name,T_,5e-4)):.4f}, 1e-3 {fl((name,T_,1e-3)):.4f},"
              f" 3e-3 {fl((name,T_,3e-3)):.4f}, pess polymer 0.5/0.3 + g1e-3 {fl((name,T_,'pess')):.4f}")
    print(f"    v3 as re-budgeted by the critic: 0.047-0.058 nominal; v3 pessimistic {0.123} + critic terms")
    print(f"    shipping iPhone Duo after 3000 folds (HTX, 1.24 deg): {math.radians(1.24)*1e3:.1f} mrad; new (<0.1 deg): <{math.radians(0.1)*1e3:.2f} mrad")

    print("\nG. side checks: Poisson-free clamps, tension hardware, glass stress")
    eps = 4000/EA; print(f"  membrane strain {eps*100:.3f}%: Poisson contraction (nu 0.22) over 150 mm width {0.22*eps*0.15*1e6:.0f} um -> jaws must allow +-{0.22*eps*0.075*1e6:.0f} um in y (flexure comb), else hindered contraction -> transverse compression -> wrinkling risk")
    for T_ in (4000, 5000):
        st = T_/EA*0.15; F = T_*0.15
        print(f"  T {T_}: frame load {F:.0f} N; stretch over 150 mm {st*1e6:.0f} um; cam work ~F*stretch {F*st*1e3:.0f} mJ per opening; "
              f"glass membrane {T_/EA*E/1e6:.0f} MPa, sustained core {150+T_/EA*E/1e6:.0f} MPa; jaw bond shear (3 mm, two faces) {T_/(2*3e-3)/1e6:.2f} MPa")
    print("\nH. like-for-like ratios (same crease model, same polymer/glass set assumptions)")
    for lab, v3, v4 in (("nominal, v3 geometry R5.5 25/9 T4000, phi_g 0", (0.047, 0.058), res[("R5.5 25/9 (v3)", 4000, 0)]*1e3),
                        ("nominal, v4 geometry R5.5 28/12 T4000, phi_g 0", (0.047, 0.058), res[("R5.5 28/12", 4000, 0)]*1e3),
                        ("critic's improved v3 (R7, shape servo, dF 0.5%, k 2e3-1e4) vs v4 R7 35/12 T4000", (0.020, 0.029), res[("R7.0 35/12", 4000, 0)]*1e3)):
        print(f"  {lab:80s}: {v3[0]}-{v3[1]} -> {v4:.4f} mrad = {v3[0]/v4:.1f}-{v3[1]/v4:.1f}x")
    for lab, T_, nm in (("R5.5 28/12", 4000, "R5.5 28/12"), ("R5.5 28/12", 5000, "R5.5 28/12"), ("R7.0 35/12", 4000, "R7.0 35/12"), ("R7.0 35/12", 5000, "R7.0 35/12")):
        s0 = res[(nm, T_, 0)]; s1 = res[(nm, T_, 1e-3)]; k = (s1-s0)/1e-3
        print(f"  {lab} T{T_}: tolerable phi_g for 5\" (0.0121) {max(0,(0.0121e-3-s0)/k):.2e}, for 3\" (0.0073) {max(0,(0.0073e-3-s0)/k):.2e}")
