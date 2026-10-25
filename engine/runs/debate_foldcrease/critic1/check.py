"""Critic-1 independent checks of round-1 sandwich claims. Imports author's model unchanged."""
import sys, math, numpy as np
sys.path.insert(0, '../round1')
from sandwich import stack, teardrop, depth, E_g, E_p, E_a

def shares(tg=20e-6, ta=3e-6, tp=22e-6):
    D, zt, _ = stack(tg, ta, tp); Dt = sum(d for _, d, *_ in D)
    Dp = sum(d for n, d, *_ in D if n == "panel"); Da = sum(d for n, d, *_ in D if n == "adh")
    Dg = Dt - Dp - Da
    return Dt, Dp, Da, Dg, zt

Dt, Dp, Da, Dg, zt = shares()
R, Rn = 5e-3, 8e-3; s, k, al, Lz = teardrop(R, Rn); a = Lz/2 + 3e-3
dk = 1/R + 1/Rn
print("A. Closed form: tensioned depth ~ (sum phi_i D_i)*(1/R+1/Rn)/T, step slope ~ eff*dk*l/2")
for pp, pa in ((0.05, .02), (.2, .1), (.5, .3)):
    for T in (500, 1000):
        eff = (pp*Dp + pa*Da)/Dt; l = math.sqrt(Dt/T)
        dn, sn = depth(eff*k, s, a, T=T, Dt=Dt)
        print(f"  phi {pp}/{pa} T={T}: closed {eff*dk*l*l*1e6:.3f} um / {eff*dk*l/2*1e3:.3f} mrad | numeric {dn*1e6:.3f} um / {sn*1e3:.3f} mrad")

print("\nB. Glass anelasticity phi_g (assumed 0 by author) added to phi 0.2/0.1")
for pg in (0, 1e-4, 3e-4, 1e-3, 3e-3):
    eff = (0.2*Dp + 0.1*Da + pg*Dg)/Dt
    d0, s0 = depth(eff*k, s, a); d1, s1 = depth(eff*k, s, a, T=1000, Dt=Dt)
    print(f"  phi_g={pg:.0e}: T=0 {d0*1e6:6.2f} um/{s0*1e3:5.2f} mrad | T=1000 {d1*1e6:5.2f} um/{s1*1e3:5.3f} mrad")

print("\nC. Lever: smooth curvature transitions (clothoid ramps of length Lr) instead of steps, phi 0.2/0.1, T=1000")
eff = (0.2*Dp + 0.1*Da)/Dt
for Lr in (0, 2e-3, 5e-3, 10e-3):
    if Lr == 0: ks = k
    else:
        n = max(3, int(Lr/(s[1]-s[0]))); ker = np.ones(n)/n; ks = np.convolve(k, ker, mode='same')
    d1, s1 = depth(eff*ks, s, a, T=1000, Dt=Dt); d0, s0 = depth(eff*ks, s, a)
    print(f"  ramp {Lr*1e3:4.1f} mm: T=1000 {d1*1e6:.3f} um / {s1*1e3:.3f} mrad | T=0 {d0*1e6:.2f} um / {s0*1e3:.2f} mrad")

print("\nD. Panel thickness sensitivity (author assumes 22 um incl. CPI+TFT+TFE+CF+touch)")
for tp in (22e-6, 30e-6, 40e-6):
    Dt2, Dp2, Da2, Dg2, zt2 = shares(tp=tp); c = zt2/2
    Rg = E_g*c/490e6
    s2, k2, _, Lz2 = teardrop(Rg, Rg*1.6); eff2 = (0.2*Dp2 + 0.1*Da2)/Dt2
    d1, s1 = depth(eff2*k2, s2, Lz2/2+3e-3, T=1000, Dt=Dt2)
    print(f"  tp={tp*1e6:.0f}: total {zt2*1e6:.0f} um, glass stress @R=5 {E_g*c/5e-3/1e6:.0f} MPa, R for 490 MPa {Rg*1e3:.2f} mm, "
          f"panel strain {tp/2/Rg*100:.2f}%, panel D-share {Dp2/Dt2*100:.2f}% -> T=1000 {d1*1e6:.2f} um/{s1*1e3:.3f} mrad")

print("\nE. Bottom-glass stress incl. central tension (author's flaw check ignores CT)")
def ct(CS, DOL, t): return CS*DOL/(t-2*DOL)   # linear CS profile on both faces
for CS, DOL in ((450, 6), (650, 4), (800, 5)):
    CT20 = ct(CS, DOL, 20); CT30 = ct(CS, DOL, 30)
    # sandwich bottom glass spans z=14..34 um from NA, R=5 mm; peak interior tension at DOL below outer face
    sb = E_g*(34e-6-DOL*1e-6)/5e-3/1e6; si = E_g*(14e-6+DOL*1e-6)/5e-3/1e6
    su = E_g*(15e-6-DOL*1e-6)/1.5e-3/1e6
    print(f"  CS {CS} DOL {DOL}: 20um CT {CT20:.0f} MPa -> sandwich interior tension {si+CT20:.0f}..{sb+CT20:.0f} MPa over full sheet;"
          f" single 30um@R1.5 CT {CT30:.0f} -> {su+CT30:.0f} MPa peak, only on tensile half")

print("\nF. Visibility vs the answer's own vernier argument (reflected deviation = 2*theta)")
for th in (0.04, 0.08, 0.16, 0.2, 0.43):
    print(f"  slope {th:.2f} mrad -> reflected deviation {2*th*1e-3*206265:.0f} arcsec (vernier ~5-10 arcsec)")
print(f"  slope for 10 arcsec deviation: {10/206265/2*1e3:.3f} mrad; 30 arcsec: {30/206265/2*1e3:.3f} mrad")

print("\nG. Backstop gap: 1 N finger on clamped circular plate radius 5-10 mm (no tension)")
for rr in (5e-3, 10e-3):
    print(f"  r={rr*1e3:.0f} mm: deflection {1*rr**2/(16*math.pi*Dt)*1e6:.0f} um vs 10-20 um gap -> glass lands on backstop at "
          f"{10e-6*16*math.pi*Dt/rr**2:.3f}-{20e-6*16*math.pi*Dt/rr**2:.3f} N")
print("  Oppo N6 best shipping hinge height variation 50 um vs required 10-20 um gap (no contact at rest)")

print("\nH. Comparison ratios")
old = (0.67, 20.89); new = (0.10, 0.42, 1.09)
print(f"  matched low/low {old[0]/new[0]:.1f}x, high/high (realistic) {old[1]/new[1]:.0f}x, old-high/new-pessimistic {old[1]/new[2]:.0f}x")
print(f"  vs HTX 167 um: {167/1.09:.0f}-{167/0.10:.0f}x ; slope vs 21.6 mrad aged: {21.64/0.43:.0f}-{21.64/0.04:.0f}x")
print(f"  equivalent glass thickness {(12*Dt/E_g)**(1/3)*1e6:.1f} um; tension length {math.sqrt(Dt/1000)*1e3:.2f} mm")
