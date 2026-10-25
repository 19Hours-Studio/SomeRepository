"""SKU comparison at central taus (Continuum 10us, Rubin 20us), 128K and 1M, p=0.8 and 0.6.
Usage: python3 sku4.py > sku4.txt"""
import model4 as m
T = (200, 500, 800, 1000, 1500, 2000)
SK = {"2-tier g=3 (192 pkg)": (dict(), 4), "1-tier g=4": (dict(sram=4.6, srambw=128e12, P=2350, g=4), 4),
      "1-tier g=4, 3 HBM": (dict(sram=4.6, srambw=128e12, hbm=108, hbmbw=7.5e12, P=2270, g=4), 3)}
for ctx in (131072, 1048576):
    for p in (0.8, 0.6):
        R = {n: m.envelope(lambda k: m.gpu_points(m.SYS[n], 20e-6, ctx, k, p), T) for n in ("Rubin35", "Rubin50")}
        print(f"\n== ctx {ctx:,} p={p}: tok/s/W ; tok/s per HBM stack (k) ; ratio vs R35/R50 ; packages")
        for n, (kw, st) in list(SK.items()) + [("Rubin35", (None, 8)), ("Rubin50", (None, 8))]:
            if kw is None:
                e, P = R[n], m.SYS[n]["P"]
            else:
                C = dict(m.CONT, **kw); g = C.pop("g", 3); P = C["P"]
                e = m.envelope(lambda k: m.pipe_points(C, 10e-6, ctx, k, p, gmin=g), T)
            cells = []
            for t in T:
                if t not in e: cells.append(f"{'--':>26}"); continue
                v, k, u, q = e[t]
                r = f"{v/R['Rubin35'][t][0]:.2f}/{v/R['Rubin50'][t][0]:.2f}" if kw is not None and t in R['Rubin35'] else ""
                cells.append(f"{v:5.1f} {v*P/st/1e3:5.1f}k[{k}] {r:>9}")
            npk = e[1000][3][3] if kw is not None and 1000 in e else ""
            print(f"{n:<22}" + "".join(cells) + f"  N={npk}")
