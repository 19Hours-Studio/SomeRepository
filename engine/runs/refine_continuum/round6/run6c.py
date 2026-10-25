"""Round-6 fairness checks: (1) Rubin with expert parallelism across 2 or 4 NVL72 racks over scale-out
(ConnectX-9 1.6 Tb/s = 0.2 TB/s per GPU; cross-rack share of all-to-all traffic (R-1)/R), tau 10/15/20 us;
(2) all-system table with Continuum-6. Usage: python3 run6c.py > run6c.txt"""
import model5 as m, run5 as r, run6b as b
m.OPT["dense_rep"] = True
T = r.T
for ctx in (r.C128, r.C1M):
    print(f"== ctx {ctx//1024}K p=0.8: best Rubin tok/s/W, single NVL72 vs multi-rack EP; Continuum-6 ratio vs best of all")
    print(" " * 40 + " ".join(f"{t:>6}" for t in T))
    R1 = b.envs_r(ctx); C6 = b.envs_c(b.C6, ctx)
    allR = list(R1)
    print(f"{'Rubin NVL72 (tau 10)':<40}" + " ".join(f"{b.pick(R1,t)[0][0]:6.1f}" if b.pick(R1,t) else "    --" for t in T))
    for R in (2, 4):
        lk = 1 / ((1 / R) / 1.8e12 + ((R - 1) / R) / 0.2e12)
        for tau in (10e-6, 15e-6, 20e-6):
            es = []
            for mq in (False, True):
                ss = dict(m.rubin(1.43, mq), imb=r.IMB_G, N=72 * R, link=lk)
                es.append((ss, r.gpu(ss, tau, ctx=ctx)))
            allR += es
            print(f"{f'Rubin EP over {R} racks, tau {tau*1e6:.0f}':<40}" + " ".join(f"{b.pick(es,t)[0][0]:6.1f}" if b.pick(es,t) else "    --" for t in T))
    b.row("Continuum-6 / best of all Rubin configs", C6, allR, 3)
    print()
print("== All systems with Continuum-6 (128K / 1M, p=0.8, equal tau 10; LPX 8, CS-4 9)")
for ctx in (r.C128, r.C1M):
    C6 = b.envs_c(b.C6, ctx)
    E = {"MI455X": r.gpu(dict(m.SYS["MI455X"], imb=r.IMB_G), 10e-6, ctx=ctx),
         "TPU8i": r.gpu(dict(m.SYS["TPU8i"], imb=r.IMB_G), 10e-6, ctx=ctx),
         "Ironwood": r.gpu(dict(m.SYS["Ironwood"], imb=r.IMB_G), 10e-6, ctx=ctx),
         "Rubin+LPX": r.env(lambda k: m.afd_points(8e-6, ctx, k, 0.8)),
         "CS-4": r.env(lambda k: m.pipe_points(m.WSE, 9e-6, ctx, k, 0.8, kv_in_sram=True))}
    print(f"-- {ctx//1024}K"); print(" " * 40 + " ".join(f"{t:>6}" for t in T))
    for n, e in E.items():
        print(f"{'C6 / '+n:<40}" + " ".join(f"{b.pick(C6,t)[0][0]/e[t][0]:6.2f}" if t in e else "   cap" for t in T) + f"   {n} max {e['max']:.0f}")
