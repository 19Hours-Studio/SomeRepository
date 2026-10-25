"""Fair comparison: each system picks its best speculation depth k (0..7) per tier.
Equal tau for GPU/TPU/Continuum. Usage: python3 envelope3.py > envelope3.txt"""
import sys, importlib
TIERS = (100, 200, 500, 800, 1000, 1500, 2000, 3000)
KS = range(0, 8)
def load(ctx, k, p):
    sys.argv = ['x', str(ctx), str(k), str(p)]
    import model3 as m; importlib.reload(m); m.TIERS = TIERS; return m
def systems(m, tau, cont):
    return {f"Rubin35": m.gpu_points(m.SYS['Rubin NVL72'], tau),
            f"Rubin50": m.gpu_points(m.SYS['Rubin (50PF dense)'], tau),
            f"MI455X": m.gpu_points(m.SYS['MI455X x72'], tau),
            f"TPU8i": m.gpu_points(m.SYS['TPU 8i x128'], tau),
            f"Ironwood": m.gpu_points(m.SYS['Ironwood x128'], tau),
            "Rubin+LPX(4us)": m.afd_points(4e-6),
            "CS-4(3us)": m.pipe_points(m.WSE, 3e-6, True),
            "Continuum": m.pipe_points(cont(m), tau, gmin=3)}
BASE = lambda m: dict(m.CONT, F4=32e15, F8=16e15, P=2450)
def envelope(ctx, p, tau, cont=BASE):
    env = {}
    for k in KS:
        m = load(ctx, k, p)
        for n, pts in systems(m, tau, cont).items():
            for i, x in enumerate(m.best(pts)):
                if x and (n, i) not in env or x and x[1] > env[(n, i)][0]:
                    env[(n, i)] = (x[1], k, x[0])
            env[(n, 'max')] = max(env.get((n, 'max'), 0), max(q[0] for q in pts))
    return env
if __name__ == "__main__":
    names = ["Rubin35", "Rubin50", "MI455X", "TPU8i", "Ironwood", "Rubin+LPX(4us)", "CS-4(3us)", "Continuum"]
    for ctx in (8192, 131072, 1048576):
        for p in (0.8, 0.6):
            for tau in (8e-6, 5e-6):
                env = envelope(ctx, p, tau)
                print(f"\n== ctx {ctx:,} p={p} tau={tau*1e6:.0f}us: best-k output tok/s per prov. MW (M) [k]")
                print(f"{'system':<15}" + "".join(f"{t:>10}" for t in TIERS) + "     max")
                for n in names:
                    print(f"{n:<15}" + "".join(f"{env[(n,i)][0]/1e6:6.1f}[{env[(n,i)][1]}] " if (n, i) in env else f"{'--':>10}" for i in range(len(TIERS))) + f" {env[(n,'max')]:6,.0f}")
                for ref in ("Rubin35", "Rubin50", "MI455X", "TPU8i", "Rubin+LPX(4us)", "CS-4(3us)"):
                    print(f"{'Cont/'+ref:<15}" + "".join(f"{env[('Continuum',i)][0]/env[(ref,i)][0]:10.2f}" if ('Continuum', i) in env and (ref, i) in env else f"{'--':>10}" for i in range(len(TIERS))))
