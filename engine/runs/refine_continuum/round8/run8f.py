"""Round 8f: single-assumption sensitivities of C7 / best Rubin under the calibrated GPU tau (140 us) and at 40 us.
Usage: python3 run8f.py > run8f.txt"""
import model8 as e, model5 as m, model7 as q
P = q.C7T_PARTS
cases = [("base", q.C7T, P), ("same node (C-die energy x1.25)", q.C7T, dict(P, comp_w=3300)),
         ("eta 0.5 on Continuum only", dict(q.C7T, F4=q.C7T['F4'] * 5 / 6, F8=q.C7T['F8'] * 5 / 6), P),
         ("W-tier 0.30 pJ/bit", q.C7T, dict(P, wt_w=1228)), ("leakage x2", q.C7T, dict(P, leak_w=1000)),
         ("tile imbalance 1.25", dict(q.C7T, imb=1.25), P)]
for ctx in (q.C128, q.C1M):
    for t0 in (40, 140):
        R = e.gpu_env_tau(q.RUBIN_PROF(), e.tau_gpu(t0), ctx=ctx)
        print(f"\n== {ctx//1024}K, GPU tau {t0} us"); print(" " * 40 + " ".join(f"{t:>6}" for t in q.T))
        for lab, base, parts in cases:
            A = e.pipe_env_tau(q.cont_prof(base, parts), e.tau_sym, ctx=ctx)
            print(f"{lab:<40}" + q.ratio(A, R))
        A = e.pipe_env_tau(q.cont_prof(q.C7T, P), lambda f: 20e-6, ctx=ctx)
        print(f"{'Continuum tau 20 us (Cerebras-like)':<40}" + q.ratio(A, R))
        if 200 in R: print(f"  Rubin >=200 point: {R[200][0]:.1f} tok/s/W, {R[200][2][2]:.0f} tok/s/user, k={R[200][2][1]}, {R[200][1]}, per-stack {R[200][0]*[x for a,x,f in q.RUBIN_PROF() if a==R[200][1]][0]['P']/8:,.0f} tok/s")
