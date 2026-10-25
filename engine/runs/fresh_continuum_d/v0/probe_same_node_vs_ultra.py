import sys; sys.path.insert(0, "/home/user/SomeRepository/engine/runs/refine_continuum/round7"); sys.path.insert(0, "/home/user/SomeRepository/engine/runs/refine_continuum/round6")
import model7 as q, model5 as m, run7 as r7
GS=(1,2,3,4,6)
def env(base, parts, ctx): return q.pipe_env(q.cont_prof(base, parts), ctx, gs=GS)
for ctx in (q.C128, q.C1M):
    R = q.gpu_env(q.RUBIN_PROF(), ctx); U = q.gpu_env(r7.ultra_prof(), ctx)
    base = env(q.C7T, q.C7T_PARTS, ctx)
    sn = env(q.C7T, dict(q.C7T_PARTS, comp_w=3300), ctx)
    sn_eta = env(dict(q.C7T, F4=q.C7T['F4']*5/6, F8=q.C7T['F8']*5/6), dict(q.C7T_PARTS, comp_w=3300), ctx)
    print(f"--- {ctx//1024}K", " ".join(f"{t:>6}" for t in q.T))
    for lab, e in (("base", base), ("same node", sn), ("same node + eta0.5", sn_eta)):
        print(f"{lab:<22} vs Rubin {q.ratio(e,R)} | vs Ultra bottom-up {q.ratio(e,U)}")
    # Ultra bottom-up chosen voltage
    print("  Ultra picks", [U[t][1] for t in q.T], "Rubin picks", [R[t][1] for t in q.T])
