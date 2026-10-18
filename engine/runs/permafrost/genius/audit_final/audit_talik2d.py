"""Idea 1: steady talik geometry under a circular lake (disk source on a half-space).
T(r,z) = Tg + G z + (Tb - Tg) * Omega(r,z)/(2 pi), Omega = solid angle of the lake disk seen from (r,z).
Checks (1) whether 36-67 m under a 200-m lake is reachable with parameters that give 15-22 m under a 100-m lake,
(2) what fraction of the lake area has the talik reaching the 15.5-16 m soil column the dredge must dig."""
import math

def omega_frac(r, z, R, n_t=720, _unused=None):
    # exact reduction for a point above the disk interior (r < R): inner radial integral is analytic,
    # Omega/(2 pi) = (1/2pi) * int_0^{2pi} [1 - z / sqrt(rho_max(t)^2 + z^2)] dt,
    # rho_max(t) = -r cos t + sqrt(R^2 - r^2 sin^2 t)
    tot = 0.0
    dt = 2 * math.pi / n_t
    for i in range(n_t):
        t = (i + 0.5) * dt
        rho = -r * math.cos(t) + math.sqrt(R * R - (r * math.sin(t)) ** 2)
        tot += 1 - z / math.sqrt(rho * rho + z * z)
    return tot * dt / (2 * math.pi)

def first_zero(f, zmax, step=0.25):
    # scan down from the lake bed; first crossing from thawed (>0) to frozen (<=0)
    z = 0.01
    if f(z) <= 0:
        return 0.0
    while z < zmax:
        z2 = z + step
        if f(z2) <= 0:
            lo, hi = z, z2
            for _ in range(50):
                m = 0.5 * (lo + hi)
                lo, hi = (m, hi) if f(m) > 0 else (lo, m)
            return 0.5 * (lo + hi)
        z = z2
    return float('inf')          # no frozen ground above permafrost base -> through-talik

def zc_axis(R, Tg, Tb, G):
    f = lambda z: Tg + G * z + (Tb - Tg) * (1 - z / math.sqrt(z * z + R * R))
    return first_zero(f, -Tg / G + 1.0)

# (1) widened grid
best = None
hits = []
for Tg10 in range(-120, -4, 5):          # -12 ... -0.5 C
    Tg = Tg10 / 10
    for Tb10 in range(5, 81, 5):         # +0.5 ... +8 C
        Tb = Tb10 / 10
        for G in (0.01, 0.02, 0.03, 0.04, 0.05, 0.06):
            z50 = zc_axis(50, Tg, Tb, G)
            if 15 <= z50 <= 22:
                z100 = zc_axis(100, Tg, Tb, G)
                pf = -Tg / G                       # permafrost base far from lake
                hits.append((z50, z100, Tg, Tb, G, pf))
fin = [h for h in hits if math.isfinite(h[1])]
pr = print
pr(f"widened grid: {len(hits)} sets give 15-22 m under a 100-m lake")
pr(f"  under a 200-m lake: finite {min(h[1] for h in fin):.0f}-{max(h[1] for h in fin):.0f} m; through-taliks: {len(hits)-len(fin)}")
big = [h for h in fin if h[1] >= 60]
for h in big[:5]:
    pr(f"  z50={h[0]:.1f} z100={h[1]:.1f} Tg={h[2]} Tb={h[3]} G={h[4]} permafrost base={h[5]:.0f} m")
pr(f"  sets with z100>=60 m: {len(big)}; all of them have permafrost base <= {max([h[5] for h in big], default=float('nan')):.0f} m")

# (2) area fraction with talik >= 15.5 m below lake bottom, R=50 m, for the central sets
def zc_r(r, R, Tg, Tb, G):
    f = lambda z: Tg + G * z + (Tb - Tg) * omega_frac(r, z, R)
    return first_zero(f, -Tg / G + 1.0, step=0.5)

for Tg, Tb, G in ((-8.0, 4.0, 0.02), (-6.0, 3.0, 0.02), (-4.0, 2.0, 0.03), (-10.0, 5.0, 0.02)):
    z0 = zc_axis(50, Tg, Tb, G)
    rs = [0, 10, 20, 30, 40, 45, 49]
    prof = [(r, zc_r(r, 50, Tg, Tb, G)) for r in rs]
    # area fraction where z >= 15.5 (linear interp of radius)
    rcrit = None
    for (r1, z1), (r2, z2) in zip(prof, prof[1:]):
        if z1 >= 15.5 > z2:
            rcrit = r1 + (z1 - 15.5) * (r2 - r1) / (z1 - z2)
    frac = (rcrit / 50) ** 2 if rcrit is not None else (1.0 if prof[-1][1] >= 15.5 else 0.0)
    s = ", ".join(f"r{r}:{z:.1f}" for r, z in prof)
    pr(f"Tg={Tg} Tb={Tb} G={G}: z(0)={z0:.1f} m | {s} | area with talik>=15.5 m: {frac*100:.0f}%")
