"""Round-2 model. Same physics as round1/sandwich.py (bonded neutral-plane sandwich, residual curvature
kres = sum(phi_i D_i)/D * kappa_fold(s), open span clamped flat at +-a, optional membrane tension T), plus:
 - smoothed teardrop: linear curvature ramps of length Lr at every transition, geometry re-solved so the fold
   still closes (end tangents antiparallel, half-gap g/2) -> zone length and bulb width are honest;
 - glass anelastic set phi_g (delayed elasticity), panel thickness 22/30/40 um;
 - outputs depth, max slope, max curvature (mirror power, mdpt = 2000*kappa), reflected deviation in arcsec."""
import numpy as np, math, sys
from scipy.optimize import fsolve
from scipy.linalg import solve_banded
sys.path.insert(0, "../round1")
from sandwich import stack

def kappa_profile(R, Rn, Lr, Lb2, Ln, n=1):
    # half curve from apex outward: bulb plateau, ramp, neck plateau, ramp to 0
    pts = [(0, 1/R), (Lb2, 1/R), (Lb2+Lr, -1/Rn), (Lb2+Lr+Ln, -1/Rn), (Lb2+2*Lr+Ln, 0.0)]
    return pts
def half_curve(R, Rn, Lr, Lb2, Ln, m=4000):
    pts = kappa_profile(R, Rn, Lr, Lb2, Ln)
    s = np.linspace(0, pts[-1][0], m); k = np.interp(s, [p[0] for p in pts], [p[1] for p in pts])
    psi = np.concatenate([[0], np.cumsum((k[1:]+k[:-1])/2*np.diff(s))])   # tangent angle from +x
    x = np.concatenate([[0], np.cumsum(np.cos((psi[1:]+psi[:-1])/2)*np.diff(s))])
    # apex at x=0 is the outer tip; x measured along the gap direction? use y as lateral: lateral = int sin(psi)
    y = np.concatenate([[0], np.cumsum(np.sin((psi[1:]+psi[:-1])/2)*np.diff(s))])
    return s, k, psi, x, y
def solve_teardrop(R, Rn, Lr, g=0.4e-3):
    # apex tangent along +x (lateral, across the gap); end tangent along -y... we need psi_end = pi/2 (turned 90 deg)
    # and lateral position x_end = g/2 back near the centreline. Bulb bulges to x_max.
    def F(v):
        Lb2, Ln = v
        s, k, psi, x, y = half_curve(R, Rn, Lr, abs(Lb2), abs(Ln))
        return [psi[-1]-math.pi/2, (x[-1]-g/2)/R]
    best = None
    for guess in ((R*1.2, Rn*0.9), (R*0.8, Rn*0.5), (R*1.5, Rn*1.2)):
        sol, info, ier, msg = fsolve(F, guess, full_output=True)
        if ier == 1 and min(sol) > 0: best = sol; break
    Lb2, Ln = best
    s, k, psi, x, y = half_curve(R, Rn, Lr, Lb2, Ln)
    half = s[-1]
    return dict(Lb2=Lb2, Ln=Ln, half=half, zone=2*half, width=2*x.max(), height=-y.min() if y.min()<0 else y.max(),
                s=np.concatenate([-s[::-1], s[1:]]), k=np.concatenate([k[::-1], k[1:]]))

def open_shape(kres_s, s, a, T, Dt, N=6001):
    x = np.linspace(-a, a, N); kr = np.interp(x, s, kres_s, left=0, right=0); dx = x[1]-x[0]
    if T == 0:
        th = np.concatenate([[0], np.cumsum(((kr-kr.mean())[1:]+(kr-kr.mean())[:-1])/2)*dx])
    else:
        n = N-2; ab = np.zeros((3, n))
        ab[0, 1:] = Dt/dx**2; ab[1, :] = -2*Dt/dx**2-T; ab[2, :-1] = Dt/dx**2
        rhs = Dt*np.gradient(kr, dx)[1:-1]
        th = np.concatenate([[0], solve_banded((1, 1), ab, rhs), [0]])
    w = np.concatenate([[0], np.cumsum((th[1:]+th[:-1])/2)*dx])
    curv = np.gradient(th, dx)
    return w.max()-w.min(), np.abs(th).max(), np.abs(curv).max()

def shares(tp, tg=20e-6, ta=3e-6):
    D, zt, zna = stack(tg, ta, tp); Dt = sum(d for _, d, *_ in D)
    Dg = sum(d for n, d, *_ in D if n.startswith("UTG")); Dp = sum(d for n, d, *_ in D if n == "panel")
    Da = sum(d for n, d, *_ in D if n == "adh")
    return Dt, Dg, Dp, Da, zt

ARC = 206265.0
def row(tp, R, Rn, Lr, phis, phig, T, margin=3e-3, geo=None):
    Dt, Dg, Dp, Da, zt = shares(tp)
    geo = geo or solve_teardrop(R, Rn, Lr)
    eff = (Dp*phis[0] + Da*phis[1] + Dg*phig)/Dt
    d, sl, cv = open_shape(eff*geo["k"], geo["s"], geo["half"]+margin, T, Dt)
    return d, sl, cv

if __name__ == "__main__":
    print("Geometry (gap 0.4 mm): R, Rn, ramp -> zone length, bulb width; glass peak stress set by R (68-76 um stack)")
    geos = {}
    for R, Rn in ((5e-3, 8e-3), (5e-3, 12e-3), (6e-3, 12e-3)):
        for Lr in (0.0, 5e-3, 10e-3, 15e-3):
            try:
                g = solve_teardrop(R, Rn, Lr if Lr > 0 else 1e-6); geos[(R, Rn, Lr)] = g
                print(f"  R={R*1e3:.0f} Rn={Rn*1e3:.0f} Lr={Lr*1e3:4.1f} mm: bulb plateau 2x{g['Lb2']*1e3:5.2f} neck {g['Ln']*1e3:5.2f} mm, zone {g['zone']*1e3:5.1f} mm, bulb width {g['width']*1e3:5.2f} mm")
            except Exception as e:
                print(f"  R={R*1e3:.0f} Rn={Rn*1e3:.0f} Lr={Lr*1e3:4.1f}: no closed solution ({e.__class__.__name__})")
    for tp in (22e-6, 30e-6, 40e-6):
        Dt, Dg, Dp, Da, zt = shares(tp)
        print(f"\nPanel {tp*1e6:.0f} um: stack {zt*1e6:.0f} um, D={Dt:.3e}; shares glass {Dg/Dt*100:.2f}% panel {Dp/Dt*100:.2f}% adh {Da/Dt*100:.2f}%; glass stress @R5 {72e9*zt/2/5e-3/1e6:.0f} MPa")
    print("\nResidual open shape, 1 min after worst hold. cols: depth um / max slope mrad / max curvature mdpt / reflected dev arcsec (2*theta*0.85)")
    cases = [((0.05, 0.02), 0), ((0.2, 0.1), 0), ((0.2, 0.1), 1e-3), ((0.2, 0.1), 3e-3), ((0.5, 0.3), 0), ((0.5, 0.3), 3e-3)]
    for tp in (22e-6, 30e-6, 40e-6):
        for (R, Rn, Lr) in ((5e-3, 8e-3, 0.0), (5e-3, 8e-3, 10e-3), (5e-3, 12e-3, 10e-3), (5e-3, 12e-3, 15e-3)):
            if (R, Rn, Lr) not in geos: continue
            g = geos[(R, Rn, Lr)]
            print(f"\n tp={tp*1e6:.0f} R={R*1e3:.0f} Rn={Rn*1e3:.0f} ramp={Lr*1e3:.0f} mm (zone {g['zone']*1e3:.0f} mm)")
            for phis, phig in cases:
                out = []
                for T in (0, 1000, 2000, 3000):
                    d, sl, cv = row(tp, R, Rn, Lr, phis, phig, T, geo=g)
                    out.append(f"T={T:4d}: {d*1e6:6.2f}/{sl*1e3:5.3f}/{cv*2000:5.1f}/{2*sl*0.85*ARC:4.0f}")
                print(f"  phi {phis[0]:.2f}/{phis[1]:.2f} phi_g {phig:.0e} | " + " | ".join(out))
