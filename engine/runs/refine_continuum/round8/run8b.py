"""Round 8b: Continuum-7 vs GPUs with the GPU-class per-layer latency swept from the symmetric 10 us (never
demonstrated) to the measured 140-150 us floor (DeepSeek-R1, 8xB200, concurrency 1, no MTP: 111 tok/s/user,
TensorRT-LLM blog => 1/(111*61) = 148 us per layer, of which ~5 us is the HBM weight-read floor).
Continuum keeps the symmetric tau (7+3/f us), which the LPX/Cerebras measurements bound at <=5-22 us (run8a).
Usage: python3 run8b.py > run8b.txt"""
import model8 as e, model5 as m, model7 as q, run7 as r7
C7P = q.cont_prof(q.C7T, q.C7T_PARTS)
TAUS = (10, 20, 40, 80, 140)
H = " " * 40 + " ".join(f"{t:>6}" for t in q.T)
for ctx in (q.C128, q.C1M):
    A = e.pipe_env_tau(C7P, e.tau_sym, ctx=ctx)
    A20 = e.pipe_env_tau(C7P, lambda f: 20e-6, ctx=ctx)            # Continuum at a Cerebras-like 20 us, any clock
    print(f"\n== {ctx//1024}K, p=0.8. tok/s/W. 'cap' = GPU cannot reach the tier"); print(H)
    print(f"{'Continuum-7 (tau 7+3/f)':<40}" + q.vals(A))
    print(f"{'Continuum-7 (tau 20 us fixed)':<40}" + q.vals(A20))
    for t0 in TAUS:
        R = e.gpu_env_tau(q.RUBIN_PROF(), e.tau_gpu(t0), ctx=ctx)
        U = e.gpu_env_tau(r7.ultra_prof(), e.tau_gpu(t0), ctx=ctx)
        U6 = e.gpu_env_tau(r7.ultra_vendor600(), e.tau_gpu(t0), ctx=ctx)
        MI = e.gpu_env_tau(r7.sys_prof("MI455X"), e.tau_gpu(t0), ctx=ctx)
        print(f"-- GPU tau0 = {t0} us"); print(f"{'  Rubin best':<40}" + q.vals(R))
        print(f"{'  C7 / Rubin':<40}" + q.ratio(A, R)); print(f"{'  C7(tau20) / Rubin':<40}" + q.ratio(A20, R))
        print(f"{'  C7 / Ultra bottom-up':<40}" + q.ratio(A, U)); print(f"{'  C7 / Ultra 600 kW @100 PF':<40}" + q.ratio(A, U6))
        print(f"{'  C7 / MI455X':<40}" + q.ratio(A, MI))
        if t0 in (40, 140):
            for t in q.T:
                if t in R: print(f"     Rubin >={t}: {R[t][0]:.1f} tok/s/W at {R[t][2][2]:.0f} tok/s/user, k={R[t][2][1]}, {R[t][1]}")
