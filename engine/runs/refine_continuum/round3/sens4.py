"""Kill-criterion sensitivity under the best-k envelope, 128K. Reference: Rubin35 and Rubin50 at tau=8us.
Usage: python3 sens4.py > sens4.txt"""
import envelope3 as e
TI = (200, 500, 800, 1000, 1500, 2000)
idx = [e.TIERS.index(t) for t in TI]
def cont_env(ctx, p, tau, mod):
    env = {}
    for k in e.KS:
        m = e.load(ctx, k, p)
        C = mod(dict(m.CONT, F4=32e15, F8=16e15, P=2450))
        g = C.pop('g', 3)
        for i, x in enumerate(m.best(m.pipe_points(C, tau, gmin=g))):
            if x and (i not in env or x[1] > env[i][0]): env[i] = (x[1], k)
    return env
for p in (0.8, 0.6):
    ref = e.envelope(131072, p, 8e-6)
    print(f"\n== 128K, p={p}; Continuum best-k tok/s/MW (M) and ratio vs Rubin35 / Rubin50 (both at tau 8us, best k)")
    print(f"{'variant':<34}" + "".join(f"{t:>18}" for t in TI))
    V = [("base tau8", 8e-6, lambda C: C), ("tau5", 5e-6, lambda C: C), ("tau12", 12e-6, lambda C: C),
         ("tau20", 20e-6, lambda C: C), ("W-Tier 180 TB/s", 8e-6, lambda C: dict(C, srambw=180e12)),
         ("W-Tier 128 TB/s", 8e-6, lambda C: dict(C, srambw=128e12)),
         ("eta 0.45 (=24PF)", 8e-6, lambda C: dict(C, F4=24e15, F8=12e15)),
         ("slot 3.0 kW", 8e-6, lambda C: dict(C, P=3000)), ("slot 2.15 kW (0.03pJ/FLOP)", 8e-6, lambda C: dict(C, P=2150)),
         ("derate 0.70", 8e-6, lambda C: dict(C, P=2450 * 0.85 / 0.70)),
         ("1 tier/C-die, g=4", 8e-6, lambda C: dict(C, sram=4.6, srambw=128e12, P=2350, g=4)),
         ("2 HBM stacks", 8e-6, lambda C: dict(C, hbm=72, hbmbw=5e12, P=2300))]
    for n, tau, mod in V:
        c = cont_env(131072, p, tau, mod)
        print(f"{n:<34}" + "".join(f"{c[i][0]/1e6:5.1f} {c[i][0]/ref[('Rubin35',i)][0]:4.2f}/{c[i][0]/ref[('Rubin50',i)][0]:4.2f}  " if i in c else f"{'--':>18}" for i in idx))
