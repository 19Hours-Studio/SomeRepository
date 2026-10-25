"""Round-6 scenarios on top of round-5 model (model5.py unchanged). Usage: python3 run6.py > run6.txt
New levers, each applied with the same rules to competitors:
  * DVFS parity: Continuum gets a Max-Q profile defined exactly like Rubin's (compute x0.92; chip saving = 29% of
    compute power; rack sees 0.83 of chip saving, as Rubin 2.3->1.8 kW chip vs 220->190 kW rack).
  * layer-group width g in {3,4,6} chosen per tier (mapping choice, no hardware change).
  * Continuum-G: KV in GDDR7 (768-bit clamshell, 48 x 4 GB = 192 GB, 32 Gbps -> 3.07 TB/s), no HBM.
  * Rubin Ultra (calendar rival, provisional): 144 pkgs, 100 PF FP4 w/ zero-skip (70 dense), 32 TB/s, 768 GB,
    link 3.6 TB/s/dir (assumed), slot 600 kW/144 = 4.17 kW or 820 kW/144 = 5.69 kW.
"""
import model5 as m, run5 as r
m.OPT["dense_rep"] = True   # round 6: attention is data-parallel, so each package reads all dense weights
T = r.T; C128, C1M = r.C128, r.C1M
CONT5 = r.CONT5
def maxq_cont(s, comp_w=1320, leak_w=250):
    save = 0.83 * (0.29 * comp_w + 0.10 * leak_w)
    return dict(s, F4=s["F4"] * 0.92, F8=s["F8"] * 0.92, P=s["P"] - save)
CG = dict(CONT5, hbm=192, hbmbw=3.07e12, P=2780 - 240 + 200)
def cont(s, tau=10e-6, ctx=C128, p=0.8, M=m.V4, gs=(3,), dvfs=False):
    es = []
    for g in gs:
        for ss in ([s, maxq_cont(s)] if dvfs else [s]):
            es.append(m.envelope(lambda k: m.pipe_points(ss, tau, ctx, k, p, M=M, gmin=g), T))
    return r.best(*es)
def ultra(P):
    return dict(N=144, F4=70e15, F8=35e15, hbm=768, hbmbw=32e12, link=3.6e12, P=P, s=1.43, imb=r.IMB_G)
rub = r.rub; rat = r.rat; fmt = r.fmt; H = r.H
if __name__ == "__main__":
    print("== A6. Round-6 steps, V4-Pro, p=0.8, equal tau 10 us: Continuum / best Rubin (tok/s per provisioned W)")
    for ctx in (C128, C1M):
        R = rub(1.43, 10e-6, ctx=ctx)
        print(f"-- ctx {ctx//1024}K"); print(H)
        c0 = cont(CONT5, ctx=ctx); print(f"{'Continuum-5 (round 5)':<44}" + rat(c0, R))
        c1 = cont(CONT5, ctx=ctx, dvfs=True); print(f"{'+ Max-Q parity':<44}" + rat(c1, R))
        c2 = cont(CONT5, ctx=ctx, dvfs=True, gs=(3, 4, 6)); print(f"{'+ g in {3,4,6} per tier':<44}" + rat(c2, R))
        c3 = cont(CG, ctx=ctx, dvfs=True, gs=(3, 4, 6)); print(f"{'Continuum-G (GDDR7 KV, zero HBM)':<44}" + rat(c3, R))
        print(f"{'  Rubin best':<44}" + fmt(R)); print(f"{'  Continuum-6 (HBM)':<44}" + fmt(c2)); print(f"{'  Continuum-G':<44}" + fmt(c3))
        for t in (1000, 1500, 2000):
            if t in c2: q = c2[t][3]; print(f"    C6 >={t}: k={c2[t][1]} b={q[2]} (Npk,m)={q[3]} g={q[4]['g']} P={'maxq' if q[1]*0+1 else ''}")
    print("\n== B6. p=0.6 and 6.2T, equal tau 10")
    print(H)
    for M, lab in ((m.V4, "1.6T"), (dict(m.V4, n_exp=1536), "6.2T")):
        for ctx in (C128, C1M):
            for p in (0.8, 0.6):
                R = rub(1.43, 10e-6, ctx=ctx, p=p, M=M)
                c = cont(CONT5, ctx=ctx, p=p, M=M, dvfs=True, gs=(3, 4, 6))
                print(f"{lab+' '+str(ctx//1024)+'K p'+str(p):<44}" + rat(c, R))
    print("\n== C6. Rubin Ultra (provisional) vs Continuum-6, 128K/1M p=0.8, tau 10")
    for ctx in (C128, C1M):
        print(f"-- ctx {ctx//1024}K"); print(H)
        c = cont(CONT5, ctx=ctx, dvfs=True, gs=(3, 4, 6))
        for P in (600e3 / 144, 820e3 / 144):
            U = r.gpu(ultra(P), 10e-6, ctx=ctx)
            print(f"{'Ultra slot %.2f kW' % (P/1e3):<44}" + fmt(U))
            print(f"{'  Continuum-6 / Ultra':<44}" + rat(c, U))
    print("\n== D6. Supply: tok/s per HBM stack and per DDR-equivalent GB (HBM 3x wafer/bit, GDDR7 1.2x), 128K")
    R = rub(1.43, 10e-6); c = cont(CONT5, dvfs=True, gs=(3, 4, 6)); g = cont(CG, dvfs=True, gs=(3, 4, 6))
    for t in (200, 1000, 1500):
        rs = R[t][0] * R[t][3][1] and R[t][0]
        pr = R[t][0]; pc = c[t][0]; pg = g[t][0]
        # tok/s per slot = tok/s/W * P_slot; use Max-Q basis for Rubin (190 kW/72) to be generous on per-stack
        ts_r = pr * 190e3 / 72; ts_c = pc * 2780; ts_g = pg * CG["P"]
        print(f">={t}: tok/s/W Rubin {pr:.1f} C6 {pc:.1f} CG {pg:.1f} | per stack Rubin {ts_r/8:,.0f} C6 {ts_c/3:,.0f}"
              f" | per DDR-eq GB Rubin {ts_r/(288*3):.0f} C6 {ts_c/(144*3):.0f} CG {ts_g/(192*1.2):.0f}"
              f" -> C6 {ts_c/(144*3)/(ts_r/864):.2f}x CG {ts_g/(192*1.2)/(ts_r/864):.2f}x")
