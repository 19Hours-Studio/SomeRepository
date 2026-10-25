"""Kill-criterion sensitivity for Continuum g=3 (design B), 128K, MTP. Ratios vs Rubin35@8us."""
import sys; sys.argv = ['x', '131072', '1']
import model2 as m
m.TIERS = (200, 500, 800, 1000)
C = dict(m.CONT, F4=32e15, F8=16e15, P=2450)
R = m.best(m.gpu_points(m.SYS['Rubin NVL72'], 8e-6))
def row(tag, s, tau=5e-6, g=3):
    b = m.best(m.pipe_points(s, tau, gmin=g))
    print(f"{tag:<40}" + "".join(f"{x[1]/1e6:6.1f}M ({x[1]/r[1]:4.2f}x)" if x and r else f"{'--':>16}" for x, r in zip(b, R)))
print(f"{'variant (Rubin35 tau8 ref)':<40}" + "".join(f"{t:>16}" for t in m.TIERS))
print(f"{'Rubin35 tau8':<40}" + "".join(f"{r[1]/1e6:6.1f}M         " for r in R))
row("base: tau5, 256TB/s, 32PF, 2.45kW", C)
for t in (8e-6, 12e-6, 20e-6): row(f"tau {t*1e6:.0f}us", C, t)
row("W-Tier 128 TB/s", dict(C, srambw=128e12))
row("W-Tier 180 TB/s", dict(C, srambw=180e12))
row("compute eff 0.45 (=24PF at 0.6)", dict(C, F4=24e15, F8=12e15))
row("slot power 3.0 kW", dict(C, P=3000))
row("2 HBM4 stacks (72GB, 5TB/s, 2.3kW)", dict(C, hbm=72, hbmbw=5e12, P=2300))
row("derate 0.70 (vs 0.85 for GPUs)", dict(C, P=2450 * 0.85 / 0.70))
row("g=4 (245 pkgs)", C, g=4)
