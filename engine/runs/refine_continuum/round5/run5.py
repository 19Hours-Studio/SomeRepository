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

if __name__ != "__main__": raise SystemExit
print("== A. Fairness waterfall, V4-Pro 128K p=0.8: Continuum / best Rubin, tok/s per provisioned W")
print(H)
steps = []
m.OPT["idx_fp4"] = False
r = rub(1.43, 20e-6, 1.0, False, ms=(1,)); c = cont(dict(m.CONT, P=2450), ms=(1,))
print(f"{'0 round-4 central (Rubin50, tau 20/10)':<44}" + rat(c, r))
m.OPT["idx_fp4"] = True
r = rub(1.43, 20e-6, 1.0, False, ms=(1,)); c = cont(dict(m.CONT, P=2450), ms=(1,))
print(f"{'1 + indexer at FP4 rate (all)':<44}" + rat(c, r))
c = cont(dict(m.CONT, P=2800), ms=(1,)); print(f"{'2 + Continuum slot 2.45 -> 2.80 kW':<44}" + rat(c, r))
r = rub(1.43, 20e-6, 1.0, True, ms=(1,)); print(f"{'3 + Rubin best of Max-P / Max-Q':<44}" + rat(c, r))
r = rub(1.43, 20e-6, IMB_G, True, ms=(1,)); c = cont(dict(m.CONT, P=2800, imb=IMB_C), ms=(1,))
print(f"{'4 + MoE load imbalance (GPU 1.07, tiles 1.12)':<44}" + rat(c, r))
r = rub(1.43, 20e-6); c = cont(dict(m.CONT, P=2800, imb=IMB_C))
print(f"{'5 + microbatch overlap m<=4 (all)':<44}" + rat(c, r))
r = rub(1.43, 10e-6); print(f"{'6 + equal tau 10 us':<44}" + rat(c, r))
c = cont(BASE4); print(f"{'7 DESIGN: Continuum zero-skip, slot 2.85 kW':<44}" + rat(c, r))
r35 = rub(1.0, 10e-6); c1 = cont(dict(BASE4, s=1.0, P=2800)); print(f"{'7b same, both without zero-skip (35 PF)':<44}" + rat(c1, r35))
c = cont(CONT5); print(f"{'8 DESIGN: 3 x 48 GB 16-high HBM4 (primary)':<44}" + rat(c, r))
print("absolute:"); print(f"{'  Rubin best (50 PF eff.)':<44}" + fmt(r)); print(f"{'  Continuum-5':<44}" + fmt(c))

print("\n== B. Regimes at EQUAL tau (10 us all), Continuum-5 / best Rubin; 'cap' = Rubin cannot reach tier")
print(H)
for M, lab in ((m.V4, "1.6T"), (dict(m.V4, n_exp=768), "3.1T"), (dict(m.V4, n_exp=1536), "6.2T")):
    for ctx in (C128, C1M):
        for p in (0.8, 0.6):
            r = rub(1.43, 10e-6, ctx=ctx, p=p, M=M); c = cont(CONT5, ctx=ctx, p=p, M=M)
            print(f"{lab+' '+str(ctx//1024)+'K p'+str(p):<44}" + rat(c, r))

print("\n== C. tau sensitivity (V4-Pro 128K and 1M, p=0.8): Continuum-5 at tau_C / Rubin at tau_G")
for ctx in (C128, C1M):
    print(f"-- ctx {ctx//1024}K" ); print(H)
    for tg in (10, 20, 45):
        r = rub(1.43, tg * 1e-6, ctx=ctx)
        for tc in (5, 10, 20):
            c = cont(CONT5, tc * 1e-6, ctx=ctx)
            print(f"{f'tau_G {tg} / tau_C {tc}':<44}" + rat(c, r))

print("\n== D. Design variants (equal tau 10, p=0.8): tok/s/W and ratio vs best Rubin; tok/s per HBM stack at >=1000")
for kvfp4 in (False, True):
    m.OPT["kv_fp4"] = kvfp4
    print(f"-- KV latent {'NVFP4 (all systems)' if kvfp4 else 'FP8'}"); print(H)
    for ctx in (C128, C1M):
        r = rub(1.43, 10e-6, ctx=ctx)
        print(f"{'Rubin best '+str(ctx//1024)+'K':<44}" + fmt(r))
        for n, s, st in (("Continuum-5 (3x48GB 16-high)", CONT5, 3), ("3x36GB 12-high", C5_12H, 3), ("2x48GB", C5_2S, 2),
                         ("4x36GB (round-4 package)", BASE4, 4), ("4x48GB", LC, 4)):
            c = cont(s, ctx=ctx)
            tps = lambda e, P, n: e[1000][0] * P / n if 1000 in e else 0
            print(f"{'  '+n:<44}" + rat(c, r) + f"   tok/s/stack@1000: {tps(c, s['P'], st):6,.0f} vs Rubin(Max-Q basis) {tps(r, 190e3/72, 8):6,.0f}")
m.OPT["kv_fp4"] = False

print("\n== E. All systems, V4-Pro 128K and 1M, p=0.8; GPUs/TPUs at tau 10 (equal) and 20; LPX 8, CS-4 9; tok/s/W")
for ctx in (C128, C1M):
    for tg in (10, 20):
        print(f"-- ctx {ctx//1024}K, GPU/TPU tau {tg}"); print(H)
        E = {"Rubin best": rub(1.43, tg * 1e-6, ctx=ctx)}
        for n in ("MI455X", "TPU8i", "Ironwood"): E[n] = gpu(dict(m.SYS[n], imb=IMB_G), tg * 1e-6, ctx=ctx)
        E["Rubin+LPX"] = env(lambda k: m.afd_points(8e-6, ctx, k, 0.8))
        E["CS-4"] = env(lambda k: m.pipe_points(m.WSE, 9e-6, ctx, k, 0.8, kv_in_sram=True))
        E["Continuum-5"] = cont(CONT5, ctx=ctx)
        for n, e in E.items(): print(f"{n:<20}" + " " * 24 + fmt(e))
        for n in E:
            if n != "Continuum-5": print(f"{'  Cont-5 / '+n:<44}" + rat(E["Continuum-5"], E[n]))

print("\n== F. Operating points, V4-Pro 128K p=0.8 equal tau 10")
for t in (200, 1000, 1500):
    c = cont(CONT5); q = c[t][3]; d = q[4]
    print(f">={t} Cont-5: k={c[t][1]} b={q[2]} m={q[3][1]} users/pod {d['users']:,} {q[0]:,.0f} tok/s/user {c[t][0]*CONT5['P']:,.0f} tok/s/pkg |"
          f" c us: sram {d['sram']*1e6:.1f} kv {d['kv']*1e6:.1f} comp {d['comp']*1e6:.1f} link {d['link']*1e6:.1f} T {d['T']*1e6:.1f}")
    r = rub(1.43, 10e-6); q = r[t][3]; d = q[4]
    print(f">={t} Rubin: k={r[t][1]} B={q[2]} (t,m)={q[3]} {q[0]:,.0f} tok/s/user | per-layer us: mem {d['mem']/62*1e6:.1f} comp {d['comp']/62*1e6:.1f} link {d['link']/62*1e6:.1f} T {d['T']*1e6:.1f}")
