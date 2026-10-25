"""Round 8c: (1) speed-tier layout search for Continuum-7 (more packages per layer, deeper interleave);
(2) end-to-end output tok/MW with prefill energy charged, prefill on GPUs or on the Continuum pod.
Usage: python3 run8c.py > run8c.txt"""
import model8 as e, model5 as m, model7 as q
C7P = q.cont_prof(q.C7T, q.C7T_PARTS)
H = " " * 40 + " ".join(f"{t:>6}" for t in q.T)
print("== (1) Continuum-7 layout search, 128K, p=0.8, symmetric tau"); print(H)
for gs in ((1, 2, 3, 4, 6), (8,), (12,), (1, 2, 3, 4, 6, 8, 12)):
    A = e.pipe_env_tau(C7P, e.tau_sym, gs=gs)
    print(f"{'g in ' + str(gs):<40}" + q.vals(A))
    if len(gs) > 2:
        for t in (1500, 2000): print(f"     >={t}: {A[t][1]} k={A[t][2][1]} m={A[t][2][3][3][1]} pkgs={A[t][2][3][3][0]}")
print("\n== (2) prefill energy, J per uncached prompt token (compute-bound; avg attention context ctx/2)")
for ctx in (q.C128, q.C1M):
    rows = []
    for lab, s, f in q.RUBIN_PROF(): rows.append(("Rubin " + lab, e.prefill_J_per_tok(s, ctx)))
    for lab, s, f in C7P: rows.append(("C7 " + lab, e.prefill_J_per_tok(s, ctx)))
    best_r = min(v for k, v in rows if k.startswith("Rubin")); best_c = min(v for k, v in rows if k.startswith("C7"))
    print(f"  {ctx//1024}K: best Rubin {best_r*1e3:.2f} mJ/tok, best C7 {best_c*1e3:.2f} mJ/tok, ratio {best_r/best_c:.2f}")
    # same-node C7 prefill
    sn = min(e.prefill_J_per_tok(s, ctx) for lab, s, f in q.cont_prof(q.C7T, dict(q.C7T_PARTS, comp_w=3300)))
    print(f"        same-node C7 {sn*1e3:.2f} mJ/tok, ratio {best_r/sn:.2f}")
    A = e.pipe_env_tau(C7P, e.tau_sym, ctx=ctx)
    for t0 in (10, 140):
        R = e.gpu_env_tau(q.RUBIN_PROF(), e.tau_gpu(t0), ctx=ctx)
        for n_in in (0, 1, 3):
            out = []
            for t in q.T:
                if t not in A: out.append("    --"); continue
                Ec = 1 / A[t][0]
                if t not in R: out.append(f"{'cap':>6}/{'cap':<6}"); continue
                Er = 1 / R[t][0]
                gpu_pre = (Er + n_in * best_r) / (Ec + n_in * best_r)
                own_pre = (Er + n_in * best_r) / (Ec + n_in * best_c)
                out.append(f"{gpu_pre:6.2f}/{own_pre:<6.2f}")
            print(f"   GPU tau0 {t0:3d} us, {n_in} uncached prompt tok per output tok: " + " ".join(out)
                  + "   (prefill on GPU / prefill on Continuum)")
