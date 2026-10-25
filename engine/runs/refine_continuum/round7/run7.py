"""Round 7: V/f-law parity for all systems, Continuum-7 (4 C-dies, wide-and-slow), bottom-up Rubin Ultra,
LP30 at FP8 weights. Usage: python3 run7.py > run7.txt"""
import model7 as q, model5 as m
# Rubin Ultra bottom-up from Rubin per-die figures: 4 dies x (860 W compute + 75 W leak) + 2 x 430 W (HBM, IO)
# = 4.6 kW chip; + ~1.0 kW rack overhead per package -> 5.6-5.7 kW at full clock (matches the 820 kW/144 report).
def ultra_prof(P_maxp=5690):
    return q.profiles(dict(q.ultra(P_maxp), P_maxq=P_maxp), comp_w=3440, leak_w=300, other_w=0, rack_share=0.83, vendor_maxq=False)
def ultra_vendor600():   # Nvidia's 600 kW taken with full 100 PF clocks (upper bound; 47% better PF/kW than Rubin on N3P)
    return [("vendor600", q.ultra(600e3 / 144), 1.0)]
def sys_prof(name, comp_frac=0.56, leak_w=120):
    s = dict(m.SYS[name], imb=q.IMB_G, s=1.0, P_maxq=m.SYS[name]["P"])
    return q.profiles(s, comp_w=comp_frac * s["P"], leak_w=leak_w, other_w=0, rack_share=0.83, vendor_maxq=False)
if __name__ == "__main__":
    for ctx in (q.C128, q.C1M):
        print(f"\n======== ctx {ctx//1024}K, p=0.8, tau(f)=7+3/f us for all; tok/s per provisioned W")
        print(" " * 34 + " ".join(f"{t:>6}" for t in q.T))
        R = q.gpu_env(q.RUBIN_PROF(), ctx)
        Rv = q.gpu_env([p for p in q.RUBIN_PROF() if p[0] in ("0.75V", "MaxQ")], ctx)
        C6 = q.pipe_env(q.cont_prof(q.C6, q.C6_PARTS), ctx)
        C6v = q.pipe_env([p for p in q.cont_prof(q.C6, q.C6_PARTS) if p[0] in ("0.75V", "MaxQ")], ctx)
        C7 = q.pipe_env(q.cont_prof(q.C7, q.C7_PARTS), ctx, gs=(1, 2, 3, 4, 6))
        C7v = q.pipe_env([p for p in q.cont_prof(q.C7, q.C7_PARTS) if p[0] in ("0.75V", "MaxQ")], ctx, gs=(1, 2, 3, 4, 6))
        for lab, e in (("Rubin vendor profiles", Rv), ("Rubin all V (best)", R), ("C6 vendor profiles", C6v),
                       ("C6 all V", C6), ("C7 vendor profiles", C7v), ("C7 all V", C7)):
            print(f"{lab:<34}" + q.vals(e))
        for t in q.T:
            print(f"   >={t}: Rubin {R[t][1]:<8} {R[t][2][1]}k {R[t][2][2]:6.0f} tok/s/user | C6 {C6[t][1]:<12} | C7 {C7[t][1]:<12} k={C7[t][2][1]} {C7[t][2][2]:5.0f} tok/s/user pk={C7[t][2][3][3][0]} m={C7[t][2][3][3][1]}")
        print(f"{'C6 / Rubin':<34}" + q.ratio(C6, R))
        print(f"{'C7 / Rubin':<34}" + q.ratio(C7, R))
        print(f"{'C7 (vendor V only) / Rubin':<34}" + q.ratio(C7v, R))
        for lab, U in (("Ultra bottom-up 5.69 kW, all V", q.gpu_env(ultra_prof(), ctx)),
                       ("Ultra vendor 600 kW @100 PF", q.gpu_env(ultra_vendor600(), ctx))):
            print(f"{lab:<34}" + q.vals(U))
            print(f"{'  C7 / that':<34}" + q.ratio(C7, U))
            if "bottom" in lab:
                for t in (200, 1000): print(f"     Ultra >={t} picks {U[t][1]} slot")
        A = q.afd_env(ctx)
        print(f"{'Rubin+LPX (LP30 FP8 weights)':<34}" + q.vals(A)); print(f"{'  C7 / that':<34}" + q.ratio(C7, A))
        for n in ("MI455X", "TPU8i", "Ironwood"):
            E = q.gpu_env(sys_prof(n), ctx)
            print(f"{'C7 / ' + n + ' (all V)':<34}" + q.ratio(C7, E) + f"   {n} max {E['max']:.0f}")
        W = q.best_over([("cs4", m.envelope(lambda k: m.pipe_points(m.WSE, 9e-6, ctx, k, 0.8, kv_in_sram=True), q.T))])
        print(f"{'C7 / CS-4':<34}" + q.ratio(C7, W) + f"   CS-4 max {W['max']:.0f}")
