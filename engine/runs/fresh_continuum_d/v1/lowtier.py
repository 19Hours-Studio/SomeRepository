import sys, time
sys.path.insert(0, "/home/user/SomeRepository/engine/runs/refine_continuum_d/round1")
import model8 as e8
q = e8.q
TS = (20, 50, 100, 200, 1000)
q.T = TS
L = ("0.55V wt", "0.60V wt", "0.65V wt", "0.55V", "0.60V")
for ctx in (q.C128,):
    t=time.time()
    R = e8.gpu_env(e8.rubin_prof(150), ctx)
    print("Rubin trim150", e8.fmt(R, TS)); 
    for t_ in TS:
        if t_ in R: print(t_, R[t_][1], R[t_][2][1] if isinstance(R[t_][2],tuple) else '')
    A = e8.c8_env(e8.C8, e8.C8_PARTS, ctx, labels=L, tiers=TS)
    print("C8", e8.fmt(A, TS)); print("ratio", e8.rat(A, R, TS))
    for t_ in TS: print(t_, A[t_][1]['spd'], A[t_][1]['npk'])
    print(time.time()-t)
