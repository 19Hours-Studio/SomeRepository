"""Round 8d: numerics lever applied to EVERY system: core attention (QK^T, PV) at the FP4 rate (SageAttention3-style
microscaled FP4), alone and with NVFP4 KV. Usage: python3 run8d.py > run8d.txt"""
import model8 as e, model5 as m, model7 as q
C7P = q.cont_prof(q.C7T, q.C7T_PARTS)
orig = m.attn_flops
def attn_fp4(M, L):
    f8, f4 = orig(M, L); return 0.0, f8 + f4
H = " " * 44 + " ".join(f"{t:>6}" for t in q.T)
for ctx in (q.C128, q.C1M):
    print(f"\n== {ctx//1024}K p=0.8"); print(H)
    for lab, fa, kv in (("base (FP8 attention, FP8 KV)", orig, False), ("FP4 attention", attn_fp4, False),
                        ("FP4 attention + NVFP4 KV", attn_fp4, True)):
        m.attn_flops = fa; m.OPT["kv_fp4"] = kv
        A = e.pipe_env_tau(C7P, e.tau_sym, ctx=ctx)
        for t0 in (10, 140):
            R = e.gpu_env_tau(q.RUBIN_PROF(), e.tau_gpu(t0), ctx=ctx)
            print(f"{lab + f' | GPU tau {t0}':<44}" + q.ratio(A, R) + f"   C7 {A[200][0]:.1f} Rubin {R[200][0]:.1f} tok/s/W at >=200")
    m.attn_flops = orig; m.OPT["kv_fp4"] = False
