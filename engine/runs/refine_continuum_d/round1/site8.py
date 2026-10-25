"""Site-level tok/s per W including prefill (critic point E). r = fresh (uncached) prompt tokens per output token.
Prefill is compute-bound on both systems: J per prompt token = comp_time(mean ctx = ctx/2) x slot W / DERATE,
same eta 0.6, zero-skip 1.43, imbalance 1.07 for both. Each system uses its most FLOP/W-efficient profile.
(a) Rubin prefill + Rubin decode (b) Rubin prefill + C8 decode (c) C8 prefill on the C8 pod + C8 decode.
Usage: python3 site8.py > site8.txt"""
import model8 as e8
q, m = e8.q, e8.m
def prefill_J(profs, ctx):
    return min((m.comp_time(m.V4, dict(s, imb=1.07, s=1.43), 1, 61, ctx // 2) * s["P"] / m.DERATE, lab) for lab, s, f in profs)
for ctx in (q.C128, q.C1M):
    Jr, lr = prefill_J(e8.rubin_prof(150), ctx)
    # C8 pod-average slot: weight 371-pkg mix at 0.55 V wt (CSA h=3, HCA h=0) -> use profiles per h
    pr3 = e8.c8_profiles(e8.C8, e8.C8_PARTS, 3); pr0 = e8.c8_profiles(e8.C8, e8.C8_PARTS, 0)
    cands = []
    for lab in pr3:
        s3, s0 = pr3[lab][0], pr0[lab][0]
        P = (210 * s3["P"] + 161 * s0["P"]) / 371
        cands.append((m.comp_time(m.V4, dict(s3, imb=1.07), 1, 61, ctx // 2) * P / m.DERATE, lab))
    Jc, lc = min(cands)
    Jc_sn = Jc * (1 + 0.25 * 902 / 2332)   # same node: compute energy x1.25 on the 902 W compute share (approx)
    R = e8.gpu_env(e8.rubin_prof(150), ctx)
    A = e8.c8_env(e8.C8, e8.C8_PARTS, ctx, labels=("0.55V wt", "0.60V wt", "0.55V"))
    print(f"== {ctx//1024}K: prefill mJ per prompt token: Rubin {Jr*1e3:.1f} ({lr}), C8 {Jc*1e3:.1f} ({lc}); ratio {Jr/Jc:.2f}"
          f" (same node ~{Jr/Jc_sn:.2f})")
    print("   r     (b) GPU-prefill+C8 decode: >=200 >=1000 >=2000 | (c) all-Continuum: >=200 >=1000 >=2000")
    for r in (0, 0.25, 1, 4, 16, 64, 1e9):
        b_ = [(1 / R[t][0] + r * Jr) / (1 / A[t][0] + r * Jr) for t in (200, 1000, 2000)]
        c_ = [(1 / R[t][0] + r * Jr) / (1 / A[t][0] + r * Jc) for t in (200, 1000, 2000)]
        print(f"   {('inf' if r > 1e6 else r):<6}" + " " * 31 + " ".join(f"{x:5.2f}" for x in b_) + " |" + " " * 20 + " ".join(f"{x:5.2f}" for x in c_))
