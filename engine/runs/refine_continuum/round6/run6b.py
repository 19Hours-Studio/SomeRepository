"""Round-6 detail: operating points, per-stack accounting with the chosen power profile, HBM-light g=6 SKUs,
4-C-die package, A16 and tile-efficiency sensitivities. Usage: python3 run6b.py > run6b.txt"""
import model5 as m, run5 as r, run6 as s6
m.OPT["dense_rep"] = True
T = r.T; C128, C1M = r.C128, r.C1M
def envs_c(s, ctx=C128, p=0.8, gs=(3, 4, 6), M=m.V4, tau=10e-6):
    out = []
    for g in gs:
        for ss in (s, s6.maxq_cont(s, comp_w=s.get("cw", 1320), leak_w=s.get("lw", 250))):
            out.append((ss, m.envelope(lambda k: m.pipe_points(ss, tau, ctx, k, p, M=M, gmin=g), T)))
    return out
def envs_r(ctx=C128, p=0.8, M=m.V4):
    out = []
    for mq in (False, True):
        ss = dict(m.rubin(1.43, mq), imb=r.IMB_G)
        out.append((ss, r.gpu(ss, 10e-6, ctx=ctx, p=p, M=M)))
    return out
def pick(envs, t):
    c = [(e[t], ss) for ss, e in envs if t in e]
    return max(c, key=lambda q: q[0][0]) if c else None
def row(lab, envs, R, stacks, ts=T):
    cells, ps = [], []
    for t in ts:
        a, b = pick(envs, t), pick(R, t)
        if not a: cells.append("    --"); continue
        if not b: cells.append("   cap"); continue
        cells.append(f"{a[0][0]/b[0][0]:6.2f}")
        ps.append(f"{t}:{a[0][0]*a[1]['P']/stacks/(b[0][0]*b[1]['P']/8):.1f}x")
    print(f"{lab:<40}" + " ".join(cells) + "   per-stack vs ref " + " ".join(ps))
H = " " * 40 + " ".join(f"{t:>6}" for t in T)
C6 = r.CONT5
C6_2 = dict(r.CONT5, hbm=96, hbmbw=5e12, P=2780 - 80)
C6_1 = dict(r.CONT5, hbm=48, hbmbw=2.5e12, P=2780 - 160)
# 4 C-dies, 8 W-tiers, 4 HBM4 16-high, 128 lanes/dir; slot = package 4362 W + host 100 + NIC 100 + switch 30 + 14.6% conv/cool
pk4 = 2640 + 614 + 320 + 288 + 500
C6X = dict(r.CONT5, F4=64e15, F8=32e15, sram=18.4, srambw=512e12, hbm=192, hbmbw=10e12, link=3.6e12 * 0.85,
           P=pk4 + 230 + 0.146 * pk4, cw=2640, lw=500)
A16 = lambda s: dict(s, P=s["P"] - 0.83 * 0.18 * s.get("cw", 1320) - 0.146 * 0.18 * s.get("cw", 1320))
ETA_C = lambda s, e: dict(s, F4=s["F4"] * e / 0.6, F8=s["F8"] * e / 0.6)
if __name__ == "__main__":
    print(f"C6X slot Max-P {C6X['P']:.0f} W, Max-Q {s6.maxq_cont(C6X, 2640, 500)['P']:.0f} W; C6 Max-Q {s6.maxq_cont(C6)['P']:.0f} W")
    for ctx in (C128, C1M):
        R = envs_r(ctx)
        print(f"\n== ctx {ctx//1024}K p=0.8 tau 10: tok/s/W ratio vs best Rubin; per-stack ratio uses each side's chosen slot power")
        print(H)
        row("C5 (g=3, no Max-Q)", [(C6, m.envelope(lambda k: m.pipe_points(C6, 10e-6, ctx, k, 0.8, gmin=3), T))], R, 3)
        row("C6: 3 stacks, Max-Q, g 3/4/6", envs_c(C6, ctx), R, 3)
        row("C6-2: 2 x 48 GB", envs_c(C6_2, ctx), R, 2)
        row("C6-1: 1 x 48 GB", envs_c(C6_1, ctx), R, 1)
        row("C6 eta 0.5 (tiles at 32 cols)", envs_c(ETA_C(C6, 0.5), ctx), R, 3)
        row("C6 eta 0.45", envs_c(ETA_C(C6, 0.45), ctx), R, 3)
        row("C6 imbalance 1.25", envs_c(dict(C6, imb=1.25), ctx), R, 3)
        row("C6 g=6 tau 15 (6-way collectives)", envs_c(C6, ctx, gs=(6,), tau=15e-6) + envs_c(C6, ctx, gs=(3,)), R, 3)
        row("C6 compute 0.050 pJ (=Rubin)", envs_c(dict(C6, P=C6["P"] + 1.146 * 0.25 * 1320 * 0.83), ctx), R, 3)
        row("C6X: 4 C-dies, 4 stacks", envs_c(C6X, ctx, gs=(1, 2, 3, 4, 6)), R, 4)
        row("C6X on A16 (-18% compute power)", envs_c(A16(C6X), ctx, gs=(1, 2, 3, 4, 6)), R, 4)
        for t in (200, 1000, 1500, 2000):
            a = pick(envs_c(C6, ctx), t); q = a[0][3]; d = q[4]
            print(f"  C6 >={t}: {a[0][0]:.1f} tok/s/W k={a[0][1]} b={q[2]} m={q[3][1]} g={d['g']} pkgs={q[3][0]} P={a[1]['P']:.0f} "
                  f"{q[0]:,.0f} tok/s/user users {d['users']:,} | us sram {d['sram']*1e6:.1f} kv {d['kv']*1e6:.1f} comp {d['comp']*1e6:.1f} link {d['link']*1e6:.1f} T {d['T']*1e6:.1f}")
            b = pick(R, t); q = b[0][3]; d = q[4]
            print(f"  Rubin >={t}: {b[0][0]:.1f} k={b[0][1]} B={q[2]} (t,m)={q[3]} P={b[1]['P']:.0f} {q[0]:,.0f} tok/s/user T {d['T']*1e6:.1f}")
    print("\n== p=0.6, 6.2T (C6 vs best Rubin)")
    print(H)
    for M, lab in ((m.V4, "1.6T"), (dict(m.V4, n_exp=1536), "6.2T")):
        for ctx in (C128, C1M):
            for p in (0.8, 0.6):
                row(f"{lab} {ctx//1024}K p{p}", envs_c(C6, ctx, p, M=M), envs_r(ctx, p, M), 3)
    print("\n== Rubin Ultra (provisional) vs C6 and C6X-A16")
    for ctx in (C128, C1M):
        for P in (600e3 / 144, 820e3 / 144):
            U = [(s6.ultra(P), r.gpu(s6.ultra(P), 10e-6, ctx=ctx))]
            print(f"-- {ctx//1024}K Ultra slot {P/1e3:.2f} kW (per-stack ratio: Ultra 16 stacks)")
            print(H)
            row("C6 / Ultra", envs_c(C6, ctx), [(a, b) for a, b in U], 3 * 8 / 16)
            row("C6X / Ultra", envs_c(C6X, ctx, gs=(1, 2, 3, 4, 6)), U, 4 * 8 / 16)
            row("C6X-A16 / Ultra", envs_c(A16(C6X), ctx, gs=(1, 2, 3, 4, 6)), U, 4 * 8 / 16)
