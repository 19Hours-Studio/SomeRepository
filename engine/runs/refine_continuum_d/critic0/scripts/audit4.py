"""Critic central estimate: per-layer-type stages (audit3) + HBM-less HCA packages (design fix) + imbalance parity 1.07
(hot-expert replication into idle SRAM) vs Rubin with host/NIC overhead trimmed by X W/slot. Also vs bottom-up Ultra."""
import sys
sys.path.insert(0, "/home/user/SomeRepository/engine/runs/refine_continuum_d/critic0/scripts")
import audit3 as a3
q, m = a3.q, a3.m
import run7 as r7
for ctx in (q.C128, q.C1M):
    profs = [p for p in q.cont_prof(dict(q.C7T, imb=1.07), q.C7T_PARTS) if p[0] in ("0.55V wt", "0.60V wt", "0.55V", "0.60V")]
    A = a3.env(profs, ctx, hca_sram=True, hbm_free_hca=True)
    U = q.gpu_env(r7.ultra_prof(), ctx)
    print(f"== {ctx//1024}K central C7: " + " ".join(f"{A[t][0]:5.1f}" for t in q.T))
    print("   vs Ultra bottom-up       " + " ".join(f"{A[t][0]/U[t][0]:5.2f}" for t in q.T))
    for X in (0, 150, 250):
        R = q.gpu_env([(l, dict(s, P=s["P"] - X), f) for l, s, f in q.RUBIN_PROF()], ctx)
        print(f"   vs Rubin trimmed {X:>3} W   " + " ".join(f"{A[t][0]/R[t][0]:5.2f}" for t in q.T))
