"""Continuum-9 operating points, all-system comparison, site level (prefill), supply/BOM. Usage: python3 all9.py > all9.txt"""
import model9 as e9, run7_shim as r7
q, e8, m = e9.q, e9.e8, e9.m


def gpu_all(ctx):
    d = {"Rubin trimmed 150 W": e8.gpu_env(e8.rubin_prof(150), ctx),
         "Rubin as shipped": e8.gpu_env(e8.rubin_prof(0), ctx),
         "Ultra 4-die bottom-up, trimmed 150 W": e8.gpu_env(e8.ultra4_prof(150), ctx)}
    u6 = q.ultra(600e3 / 144)
    d["Ultra 4-die 600 kW, 100 PF, full clock, trimmed 150 W"] = e8.gpu_env([("v600t", dict(u6, P=u6["P"] - 150), 1.0)], ctx)
    d["Ultra 2-die (reported), trimmed 150 W"] = e8.gpu_env(e8.ultra2_prof(150), ctx)
    for n in ("MI455X", "TPU8i"): d[n] = q.gpu_env(r7.sys_prof(n), ctx)
    d["Rubin+LPX (LP30 FP8)"] = q.afd_env(ctx)
    d["CS-4"] = q.best_over([("w", m.envelope(lambda k: m.pipe_points(m.WSE, 9e-6, ctx, k, 0.8, kv_in_sram=True), q.T))])
    return d


H = " " * 58 + " ".join(f"{t:>6}" for t in q.T)
for ctx in (q.C128, q.C1M):
    A = e9.env(ctx, **e9.BASE)
    A8 = e9.env(ctx, split="tp", gmax=14, s_static=0, labels=("0.55V wt", "0.60V wt"))
    G = gpu_all(ctx); R = G["Rubin trimmed 150 W"]
    print(f"\n== {ctx//1024}K p=0.8"); print(H)
    print(f"{'C9 tok/s/W':<58}" + e8.fmt(A) + f"   max {A['max']:.0f}")
    print(f"{'C8 tok/s/W (round 1, reproduced)':<58}" + e8.fmt(A8))
    for t in q.T: print(f"   >={t}: " + e9.detail(A[t][1]))
    for n, e in G.items(): print(f"{'C9 / ' + n:<58}" + e8.rat(A, e) + f"   ({e8.fmt(e)}; max {e['max']:.0f})")
    for gm in (20, 10):
        Ag = e9.env(ctx, **dict(e9.BASE, gmax=gm))
        print(f"{'C9 with g <= %d / Rubin trimmed' % gm:<58}" + e8.rat(Ag, R) + "   pkgs at >=1000: %d" % Ag[1000][1]["npk"])
    Acold = e9.env(ctx, **e9.BASE, spares=0.03, spare_mode="cold")
    print(f"{'C9 with 3% cold spares (5% idle power) / Rubin trimmed':<58}" + e8.rat(Acold, R))
    # site level with prefill
    d = A[1000][1]
    pr = {h: e9.design_profiles(h, 0.7, 64, ("0.55V wt",))["0.55V wt"][0] for h in (0, 3)}
    nC = 30 * d["C"][0]; P = d["W"] / d["npk"]
    Jc = m.comp_time(m.V4, dict(pr[3], imb=1.07), 1, 61, ctx // 2) * P / m.DERATE
    Jr = min(m.comp_time(m.V4, dict(s, imb=1.07, s=1.43), 1, 61, ctx // 2) * s["P"] / m.DERATE for l, s, f in e8.rubin_prof(150))
    Jc_sn = Jc * (1 + 0.25 * 902 / P)
    print(f"  prefill mJ/prompt token: Rubin {Jr*1e3:.1f}, C9 {Jc*1e3:.1f} (pod-average slot {P:.0f} W): ratio {Jr/Jc:.2f}, same node ~{Jr/Jc_sn:.2f}")
    print("   r    GPU prefill + C9 decode (>=200 >=1000 >=2000) | all-C9 (>=200 >=1000 >=2000)")
    for r in (0.25, 1, 4, 16, 64):
        b_ = [(1 / R[t][0] + r * Jr) / (1 / A[t][0] + r * Jr) for t in (200, 1000, 2000)]
        c_ = [(1 / R[t][0] + r * Jr) / (1 / A[t][0] + r * Jc) for t in (200, 1000, 2000)]
        print(f"   {r:<5}" + " ".join(f"{x:5.2f}" for x in b_) + "   |  " + " ".join(f"{x:5.2f}" for x in c_))
    if ctx != q.C128: continue
    # supply / BOM
    RP = e8.rubin_prof(150)
    for t in (200, 1000, 2000):
        d = A[t][1]; effc = A[t][0]; npk, st, W = d["npk"], d["stacks"], d["W"]
        effr, labr = R[t][0], R[t][1]; Pr = [x for l, x, f in RP if l == labr][0]["P"]
        tc, tr = effc * W / npk, effr * Pr
        pk_c, pk_r = 1e6 / tc, 1e6 / tr
        hc, hr = pk_c * st / npk, pk_r * 8
        n2, n4, n3 = pk_c * 30, pk_c * 60, pk_r * 16.5
        lo = 2.6 + 2.5 + 0.9 * st / npk + 2.5; hi = 3.1 + 2.5 + 1.95 * st / npk + 2.5; mid = (lo + hi) / 2
        rl, rh = 7.6, 13.0; rm = (rl + rh) / 2
        f = lambda c, r_: (tc / c) / (tr / r_)
        print(f"  supply >={t}: {tc:,.0f} tok/s/pkg vs Rubin {tr:,.0f}/GPU; {st/npk:.2f} stacks/pkg; tokens per HBM GB {hr*36/(hc*48):.1f}x; "
              f"all silicon per token {(n2+n4)/n3:.2f}x (N2 only {n2/n3:.2f}x); SoIC passes per GW "
              f"{1e9 / (W/npk) * 8 / 46 / 1e3:,.0f}k (packages per GW {1e9/(W/npk)/1e3:,.0f}k, stacks per GW {1e9/(W/npk)*st/npk/1e6:.2f}M); BOM ${lo:.1f}-{hi:.1f}k, tok/s per BOM$ centre {f(mid, rm):.2f} crossed {f(hi, rl):.2f}-{f(lo, rh):.2f}; "
              f"with 3% spares centre {f(mid, rm)/1.03:.2f}")
# NVFP4 KV and p = 0.6
m.OPT["kv_fp4"] = True
for ctx in (q.C128, q.C1M):
    print(f"-- {ctx//1024}K NVFP4 KV on both: " + e8.rat(e9.env(ctx, **e9.BASE), e8.gpu_env(e8.rubin_prof(150), ctx)))
m.OPT["kv_fp4"] = False
for ctx in (q.C128, q.C1M):
    print(f"-- {ctx//1024}K p=0.6: " + e8.rat(e9.env(ctx, p=0.6, **e9.BASE), e8.gpu_env(e8.rubin_prof(150), ctx, p=0.6)))
