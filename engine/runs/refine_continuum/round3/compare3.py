"""Round-3 comparison: equal tau for GPU/TPU/Continuum; speculation depth k in {0,1,5}; drafter cost.
Usage: python3 compare3.py > compare3.txt"""
import sys, importlib
TIERS = (100, 200, 500, 800, 1000, 1500, 2000)
def load(ctx, k, p=0.8):
    sys.argv = ['x', str(ctx), str(k), str(p)]
    import model3 as m; importlib.reload(m); m.TIERS = TIERS; return m
def rows(m, tau):
    C = dict(m.CONT, F4=32e15, F8=16e15, P=2450)
    return [(f"Rubin35 {tau*1e6:.0f}us", m.gpu_points(m.SYS['Rubin NVL72'], tau)),
            (f"Rubin50 {tau*1e6:.0f}us", m.gpu_points(m.SYS['Rubin (50PF dense)'], tau)),
            (f"MI455X {tau*1e6:.0f}us", m.gpu_points(m.SYS['MI455X x72'], tau)),
            (f"TPU8i {tau*1e6:.0f}us", m.gpu_points(m.SYS['TPU 8i x128'], tau)),
            (f"Ironwood {tau*1e6:.0f}us", m.gpu_points(m.SYS['Ironwood x128'], tau)),
            ("Rubin+LPX 4us", m.afd_points(4e-6)),
            ("CS-4 3us", m.pipe_points(m.WSE, 3e-6, True)),
            (f"Continuum {tau*1e6:.0f}us", m.pipe_points(C, tau, gmin=3))]
for ctx in (8192, 131072, 1048576):
    for k, p in ((0, 0.8), (1, 0.8), (5, 0.8), (5, 0.6)):
        if ctx != 131072 and (k, p) in ((0, 0.8), (5, 0.6)): continue
        for tau in (8e-6, 5e-6):
            m = load(ctx, k, p)
            print(f"\n== ctx {ctx:,} draft k={k} p={p} (tok/step {m.TOK:.2f}) tau(GPU/TPU/Cont)={tau*1e6:.0f}us: output tok/s per prov. MW (M)")
            print(f"{'system':<16}" + "".join(f"{t:>7}" for t in TIERS) + "    max")
            res = {}
            for n, pts in rows(m, tau):
                b = m.best(pts); res[n] = b
                print(f"{n:<16}" + "".join(f"{x[1]/1e6:7.1f}" if x else f"{'--':>7}" for x in b) + f"  {max(q[0] for q in pts):6,.0f}")
            c = res[f"Continuum {tau*1e6:.0f}us"]
            for ref in (f"Rubin35 {tau*1e6:.0f}us", f"Rubin50 {tau*1e6:.0f}us"):
                print(f"{'ratio vs '+ref:<24}" + "".join(f"{a[1]/r[1]:6.2f}" if a and r else f"{'--':>6}" for a, r in zip(c, res[ref])))
