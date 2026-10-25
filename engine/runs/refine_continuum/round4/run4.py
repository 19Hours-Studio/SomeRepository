"""Round-4 scenarios. Usage: python3 run4.py > run4.txt"""
import model4 as m
T = (200, 500, 800, 1000, 1500, 2000)
C128 = 131072
def gpu(name, tau, ctx=C128, p=0.8, comm=True):
    return m.envelope(lambda k: m.gpu_points(m.SYS[name], tau, ctx, k, p, comm), T)
def cont(tau, ctx=C128, p=0.8, comm=True, **kw):
    return m.envelope(lambda k: m.pipe_points(dict(m.CONT, **kw), tau, ctx, k, p, gmin=kw.get('g', 3), comm=comm), T)
def fmt(e): return "".join(f"{e[t][0]:7.1f}[{e[t][1]}]" if t in e else f"{'--':>10}" for t in T) + f"  max {e['max']:6,.0f}"
def rat(a, b): return "".join(f"{a[t][0]/b[t][0]:10.2f}" if t in a and t in b else f"{'--':>10}" for t in T)
hdr = f"{'':<26}" + "".join(f"{t:>10}" for t in T)

print("== A. round-3 reproduction (no link-bandwidth terms, equal tau 8us, 128K, p=0.8): tok/s per prov. W")
print(hdr)
c0, r0, r50 = cont(8e-6, comm=False), gpu("Rubin35", 8e-6, comm=False), gpu("Rubin50", 8e-6, comm=False)
for n, e in (("Continuum", c0), ("Rubin35", r0), ("Rubin50", r50)): print(f"{n:<26}" + fmt(e))
print(f"{'Cont/Rubin35':<26}" + rat(c0, r0)); print(f"{'Cont/Rubin50':<26}" + rat(c0, r50))

print("\n== B. + scale-up link bandwidth terms (equal tau 8us)")
c1, r1, r51 = cont(8e-6), gpu("Rubin35", 8e-6), gpu("Rubin50", 8e-6)
for n, e in (("Continuum", c1), ("Rubin35", r1), ("Rubin50", r51)): print(f"{n:<26}" + fmt(e))
print(f"{'Cont/Rubin35':<26}" + rat(c1, r1)); print(f"{'Cont/Rubin50':<26}" + rat(c1, r51))
q = r1[1000][3]; print("Rubin35 >=1000 op point: B", q[2], "k", r1[1000][1], {a: round(v*1e3, 2) for a, v in q[4].items()}, "ms")
q = c1[1000][3]; print("Cont >=1000 op point: b", q[2], "k", c1[1000][1], {a: round(v*1e6, 1) for a, v in q[4].items() if a != 'g'}, "us")

print("\n== C. tau matrix, 128K. cell = Continuum / Rubin35 , Continuum / Rubin50 at tiers >=200 | >=1000 | >=1500")
for p in (0.8, 0.6):
    print(f"-- p={p}")
    G = {tg: (gpu("Rubin35", tg*1e-6, p=p), gpu("Rubin50", tg*1e-6, p=p)) for tg in (8, 15, 20, 30, 45)}
    print(f"{'tau_C \\ tau_GPU':<16}" + "".join(f"{tg:>27}" for tg in G))
    for tc in (5, 8, 10, 12, 20):
        c = cont(tc*1e-6, p=p)
        cells = []
        for tg, (a, b) in G.items():
            s = "|".join(f"{c[t][0]/a[t][0]:.2f}/{c[t][0]/b[t][0]:.2f}" if t in c and t in a and t in b else "--" for t in (200, 1000, 1500))
            cells.append(f"{s:>27}")
        print(f"{tc:<16}" + "".join(cells))

print("\n== D. calibration: model max tok/s/user (best k<=7, p=0.8) vs measured")
for name in ("GB300", "Rubin35"):
    for tg in (8, 20, 45, 70):
        e = m.envelope(lambda k: m.gpu_points(m.SYS[name], tg*1e-6, 8192, k, 0.8), (50,))
        e1 = m.envelope(lambda k: m.gpu_points(m.SYS[name], tg*1e-6, 8192, k, 0.8), (50,), ks=(1,))
        print(f"{name:<8} tau {tg:>3}us: max {e['max']:6,.0f} tok/s/user (k<=7), {e1['max']:5,.0f} (k=1 MTP);"
              f" tok/s/GPU at >=50: {e[50][0]*m.SYS[name]['P']:8,.0f}")
for tw in (3, 9, 12):
    e = m.envelope(lambda k: m.pipe_points(m.WSE, tw*1e-6, C128, k, 0.8, kv_in_sram=True), (100,))
    e0 = m.envelope(lambda k: m.pipe_points(m.WSE, tw*1e-6, C128, k, 0.8, kv_in_sram=True), (100,), ks=(0,))
    print(f"CS-4 tau {tw}us: max {e['max']:6,.0f} (k<=7), {e0['max']:6,.0f} (k=0); tok/s/MW at >=100 {e[100][0]*1e6/1e6:.1f}")

print("\n== E. central case: Rubin/MI455X/TPU tau 20us, Continuum 10us, LPX 8us, CS-4 9us; 128K; tok/s per prov. W")
for p in (0.8, 0.6):
    print(f"-- p={p}"); print(hdr)
    E = {n: gpu(n, 20e-6, p=p) for n in ("Rubin35", "Rubin50", "MI455X", "TPU8i", "Ironwood")}
    E["Rubin+LPX"] = m.envelope(lambda k: m.afd_points(8e-6, C128, k, p), T)
    E["CS-4"] = m.envelope(lambda k: m.pipe_points(m.WSE, 9e-6, C128, k, p, kv_in_sram=True), T)
    E["Continuum"] = cont(10e-6, p=p)
    for n, e in E.items(): print(f"{n:<26}" + fmt(e))
    for n in ("Rubin35", "Rubin50", "MI455X", "TPU8i", "Rubin+LPX", "CS-4"): print(f"{'Cont/'+n:<26}" + rat(E["Continuum"], E[n]))

print("\n== F. central case, other contexts (p=0.8): Continuum/Rubin35, Continuum/Rubin50")
for ctx in (8192, 1048576):
    c, a, b = cont(10e-6, ctx=ctx), gpu("Rubin35", 20e-6, ctx=ctx), gpu("Rubin50", 20e-6, ctx=ctx)
    print(f"ctx {ctx:>8,}: Cont {fmt(c)}"); print(f"{'':<16}R35 " + rat(c, a)); print(f"{'':<16}R50 " + rat(c, b))

print("\n== G. Continuum variants at central taus (128K p=0.8), ratio vs Rubin35 / Rubin50 (tau 20)")
a, b = gpu("Rubin35", 20e-6), gpu("Rubin50", 20e-6)
V = [("base", {}), ("2 HBM stacks", dict(hbm=72, hbmbw=5e12, P=2300)), ("slot 3.06 kW (=Rubin)", dict(P=220e3/72)),
     ("eta-equiv 24 PF", dict(F4=24e15, F8=12e15)), ("W-Tier 180 TB/s", dict(srambw=180e12)),
     ("1 tier/C-die g=4", dict(sram=4.6, srambw=128e12, P=2350, g=4))]
print(hdr)
for n, kw in V:
    c = cont(10e-6, **kw); print(f"{n:<26}" + "".join(f"{c[t][0]/a[t][0]:5.2f}/{c[t][0]/b[t][0]:4.2f}" if t in c else f"{'--':>10}" for t in T))
c = cont(10e-6, ctx=1048576, hbm=72, hbmbw=5e12, P=2300); a1 = gpu("Rubin35", 20e-6, ctx=1048576)
print(f"{'2 HBM stacks @1M':<26}" + rat(c, a1))
