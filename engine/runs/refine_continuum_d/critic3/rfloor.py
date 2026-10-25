import sys
sys.path.insert(0, "/home/user/SomeRepository/engine/runs/refine_continuum_d/round3")
import model10 as c
q, e8 = c.q, c.e8
C = {q.C128: [62.0, 62.0, 60.0, 59.1, 55.6], q.C1M: [18.5] * 5}
for ctx in (q.C128, q.C1M):
    for nm, keep in (("all V (base)", None), ("Rubin floor 0.65 V", ("0.75V", "0.65V", "MaxQ")), ("Rubin vendor points only (0.75V, MaxQ)", ("0.75V", "MaxQ"))):
        pr = e8.rubin_prof(150); pr = [p for p in pr if keep is None or p[0] in keep]
        R = e8.gpu_env(pr, ctx)
        print(f"{ctx//1024}K {nm:<40} Rubin {e8.fmt(R)}  C10/Rubin " + " ".join(f"{a/R[t][0]:.2f}" for a, t in zip(C[ctx], q.T)))
