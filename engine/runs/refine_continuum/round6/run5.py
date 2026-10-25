"""Round-5 scenarios. Usage: python3 run5.py > run5.txt"""
import model5 as m
T = (200, 500, 1000, 1500, 2000)
C128, C1M = 131072, 1048576
IMB_G, IMB_C = 1.07, 1.12          # from imbal5.txt (sigma=0.5, GPU with 32 redundant experts; tiles r=16)
BASE4 = dict(m.CONT, s=1.43, imb=IMB_C, P=2850)            # round-4 package + zero-skip: 4 x 36 GB, slot 2.85 kW
CONT5 = dict(BASE4, hbm=144, hbmbw=7.5e12, P=2780)          # Continuum-5 primary: 3 x 48 GB 16-high HBM4, slot 2.78 kW
C5_12H = dict(BASE4, hbm=108, hbmbw=7.5e12, P=2770)         # fallback until 16-high ships: 3 x 36 GB
C5_2S = dict(BASE4, hbm=96, hbmbw=5e12, P=2700)             # 2 x 48 GB
LC = dict(BASE4, hbm=192, hbmbw=10e12, P=2870)              # 4 x 48 GB


def env(fn, ks=range(8)): return m.envelope(fn, T, ks)
def best(*es):
    out = {}
    for t in list(T) + ["max"]:
        c = [e[t] for e in es if t in e]
        if c: out[t] = max(c, key=lambda q: q if t == "max" else q[0])
    return out
def gpu(s, tau, ctx=C128, p=0.8, M=m.V4, ms=m.MS): return env(lambda k: m.gpu_points(s, tau, ctx, k, p, M=M, ms=ms))
def rub(sz=1.43, tau=10e-6, imb=IMB_G, maxq=True, **kw):
    es = [gpu(dict(m.rubin(sz, False), imb=imb), tau, **kw)]
    if maxq: es.append(gpu(dict(m.rubin(sz, True), imb=imb), tau, **kw))
    return best(*es)
def cont(s, tau=10e-6, ctx=C128, p=0.8, M=m.V4, ms=m.MS):
    return env(lambda k: m.pipe_points(s, tau, ctx, k, p, M=M, gmin=3, ms=ms))
def v(e, t): return e[t][0] if t in e else None
def rat(a, b, ts=T): return " ".join(f"{v(a,t)/v(b,t):6.2f}" if v(a, t) and v(b, t) else f"{'cap' if v(a,t) else '--':>6}" for t in ts)
def fmt(e, ts=T): return " ".join(f"{v(e,t):6.1f}" if v(e, t) else f"{'--':>6}" for t in ts) + f"   max {e.get('max', 0):5.0f}"
H = " " * 44 + " ".join(f"{t:>6}" for t in T)

if __name__ == "__main__":
    import runpy; runpy.run_path("../round5/run5.py")
