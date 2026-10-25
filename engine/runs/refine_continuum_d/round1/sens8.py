"""Continuum-8 sensitivities and all-system comparison. Usage: python3 sens8.py > sens8.txt"""
import model8 as e8, run7_shim as r7
q, m = e8.q, e8.m
L = ("0.55V wt", "0.60V wt", "0.65V wt", "0.55V", "0.60V")
H = " " * 50 + " ".join(f"{t:>6}" for t in q.T)
def C(ctx, base=e8.C8, parts=e8.C8_PARTS, **kw): return e8.c8_env(base, parts, ctx, labels=kw.pop("labels", L), **kw)
for ctx in (q.C128, q.C1M):
    R = e8.gpu_env(e8.rubin_prof(150), ctx); A = C(ctx)
    print(f"\n== {ctx//1024}K p=0.8: Continuum-8 / Rubin host-trimmed 150 W"); print(H)
    print(f"{'C8 tok/s/W':<50}" + e8.fmt(A)); print(f"{'base ratio':<50}" + e8.rat(A, R))
    rows = [("same node (C-die compute energy x1.25)", C(ctx, parts=dict(e8.C8_PARTS, comp_w=3300))),
            ("eta 0.5 (Continuum only)", C(ctx, base=dict(e8.C8, F4=e8.C8["F4"] * 5 / 6, F8=e8.C8["F8"] * 5 / 6))),
            ("W-tier 0.30 pJ/bit", C(ctx, parts=dict(e8.C8_PARTS, wt_w=1228))),
            ("leakage x2", C(ctx, parts=dict(e8.C8_PARTS, leak_w=1000))),
            ("no hot-expert replicas (imb 1.12)", C(ctx, imb_fixed=1.12)),
            ("tile imbalance 1.25", C(ctx, imb_fixed=1.25)),
            ("collectives 12 us (Continuum only)", C(ctx, tau_fn=lambda f: (12 + 3 / f) * 1e-6))]
    e8.FILL = 0.8; rows.append(("usable SRAM 80% (not 90%)", C(ctx))); e8.FILL = 0.9
    for lab, e in rows: print(f"{'  ' + lab:<50}" + e8.rat(e, R))
    Rv = e8.gpu_env([p for p in e8.rubin_prof(150) if p[0] in ("0.75V", "0.65V", "0.60V", "MaxQ")], ctx)
    print(f"{'  Vmin floor 0.60 V for both':<50}" + e8.rat(C(ctx, labels=("0.60V wt", "0.65V wt", "0.60V")), Rv))
    R2 = e8.gpu_env(e8.rubin_prof(150), ctx, two_phase=True); A2 = C(ctx, two_phase=True)
    print(f"{'  two-phase (no weight/attention overlap), both':<50}" + e8.rat(A2, R2) + f"   C8 {e8.fmt(A2)} | Rubin {e8.fmt(R2)}")
    print(f"{'  pair: same node + eta 0.5':<50}" + e8.rat(C(ctx, base=dict(e8.C8, F4=e8.C8['F4'] * 5 / 6, F8=e8.C8['F8'] * 5 / 6), parts=dict(e8.C8_PARTS, comp_w=3300)), R))
    print(f"{'  pair: two-phase + no replicas':<50}" + e8.rat(C(ctx, two_phase=True, imb_fixed=1.12), R2))
    print(f"{'  vs Rubin as shipped (no trim)':<50}" + e8.rat(A, e8.gpu_env(e8.rubin_prof(0), ctx)))
    print(f"{'  vs Rubin trimmed 250 W':<50}" + e8.rat(A, e8.gpu_env(e8.rubin_prof(250), ctx)))
    print(f"\n-- {ctx//1024}K all systems (C8 / X)"); print(H)
    sysd = {"Ultra 4-die bottom-up, trimmed 150 W": e8.gpu_env(e8.ultra4_prof(150), ctx),
            "Ultra 4-die at Nvidia 600 kW, 100 PF, no undervolt": e8.gpu_env(r7.ultra_vendor600(), ctx),
            "Ultra 2-die (reported), trimmed 150 W": e8.gpu_env(e8.ultra2_prof(150), ctx)}
    for n in ("MI455X", "TPU8i"): sysd[n] = q.gpu_env(r7.sys_prof(n), ctx)
    sysd["Rubin+LPX (LP30 FP8)"] = q.afd_env(ctx)
    sysd["CS-4"] = q.best_over([("w", m.envelope(lambda k: m.pipe_points(m.WSE, 9e-6, ctx, k, 0.8, kv_in_sram=True), q.T))])
    for n, e in sysd.items(): print(f"{n:<50}" + e8.rat(A, e) + f"   ({e8.fmt(e)}; max {e['max']:.0f})")
    print(f"C8 max tok/s/user {A['max']:.0f}; Rubin {R['max']:.0f}")
# p = 0.6 and NVFP4 KV
for ctx in (q.C128, q.C1M):
    print(f"\n-- {ctx//1024}K p=0.6:  " + e8.rat(C(ctx, p=0.6), e8.gpu_env(e8.rubin_prof(150), ctx, p=0.6)))
m.OPT["kv_fp4"] = True
for ctx in (q.C128, q.C1M):
    print(f"-- {ctx//1024}K NVFP4 KV on both: " + e8.rat(C(ctx), e8.gpu_env(e8.rubin_prof(150), ctx)))
m.OPT["kv_fp4"] = False
