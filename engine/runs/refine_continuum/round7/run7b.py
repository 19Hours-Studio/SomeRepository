"""Round 7 detail: C7 sensitivities, silicon/HBM per token, A16, Ultra scenarios. Usage: python3 run7b.py > run7b.txt"""
import model7 as q, model5 as m, run7 as r7
def c7(parts=q.C7_PARTS, base=q.C7, gs=(1, 2, 3, 4, 6), ctx=q.C128, p=0.8, M=m.V4):
    return q.pipe_env(q.cont_prof(base, parts), ctx, p=p, M=M, gs=gs)
def law(vt=None, alpha=None):
    old = (q.VT, q.ALPHA)
    if vt: q.VT = vt
    if alpha: q.ALPHA = alpha
    return old
H = " " * 44 + " ".join(f"{t:>6}" for t in q.T)
for ctx in (q.C128, q.C1M):
    R = q.gpu_env(q.RUBIN_PROF(), ctx)
    print(f"\n== {ctx//1024}K p0.8: ratio to best Rubin (all V)"); print(H)
    rows = [("C7 base (g 1-6)", c7(ctx=ctx)),
            ("C7 g<=3 only (~C6-g6 silicon per pod)", c7(gs=(1, 2, 3), ctx=ctx)),
            ("C7 eta 0.5", c7(base=dict(q.C7, F4=q.C7['F4'] * 5 / 6, F8=q.C7['F8'] * 5 / 6), ctx=ctx)),
            ("C7 imbalance 1.25", c7(base=dict(q.C7, imb=1.25), ctx=ctx)),
            ("C7 compute at N3P energy (x1.25)", c7(parts=dict(q.C7_PARTS, comp_w=2640 * 1.25), ctx=ctx)),
            ("C7 no zero-skip on either side", None),
            ("C7 leakage 2x", c7(parts=dict(q.C7_PARTS, leak_w=1000), ctx=ctx)),
            ("C7 on A16 (compute power -18%)", c7(parts=dict(q.C7_PARTS, comp_w=2640 * 0.82), ctx=ctx))]
    for lab, e in rows:
        if e is None:
            Rn = q.gpu_env([(a, dict(s, s=1.0), f) for a, s, f in q.RUBIN_PROF()], ctx)
            e = q.pipe_env([(a, dict(s, s=1.0), f) for a, s, f in q.cont_prof(q.C7, q.C7_PARTS)], ctx, gs=(1, 2, 3, 4, 6))
            print(f"{lab:<44}" + q.ratio(e, Rn)); continue
        print(f"{lab:<44}" + q.ratio(e, R))
    for vt, al, lab in ((0.35, 1.3, "law Vt 0.35 (steeper f-V)"), (0.25, 1.3, "law Vt 0.25"), (0.30, 1.6, "law alpha 1.6")):
        old = law(vt, al)
        Rl = q.gpu_env(q.RUBIN_PROF(), ctx); e = c7(ctx=ctx)
        print(f"{lab:<44}" + q.ratio(e, Rl))
        q.VT, q.ALPHA = old
    for tau0, lab in ((10, "collectives 10 us (tau 13 at f0) for C7 only"), (14, "collectives 14 us for C7 only")):
        oldt = q.tau_f
        q.tau_f = lambda f, t0=tau0: (t0 + 3 / f) * 1e-6
        e = c7(ctx=ctx); q.tau_f = oldt
        print(f"{lab:<44}" + q.ratio(e, R))
    # per-stack, C-die area per token
    e = c7(ctx=ctx); e3 = c7(gs=(1, 2, 3), ctx=ctx)
    C6 = q.pipe_env(q.cont_prof(q.C6, q.C6_PARTS), ctx)
    print("  tier | tok/s per HBM stack: Rubin / C7 / C7(g<=3) / C6 | tok/s per cm2 of leading-edge logic: Rubin / C7 / C7(g<=3) / C6")
    for t in q.T:
        def slot(env, sysP): return env[t][0] * sysP
        # recover chosen slot power from label
        def P_of(env, profs):
            lab = env[t][1].split(" g")[0]
            return [s for a, s, f in profs if a == lab][0]["P"]
        pr = P_of(R, q.RUBIN_PROF()); pc = P_of(e, q.cont_prof(q.C7, q.C7_PARTS)); p3 = P_of(e3, q.cont_prof(q.C7, q.C7_PARTS))
        p6 = P_of(C6, q.cont_prof(q.C6, q.C6_PARTS))
        tr, tc, t3, t6 = R[t][0] * pr, e[t][0] * pc, e3[t][0] * p3, C6[t][0] * p6
        print(f"  {t:>5} | {tr/8:7,.0f} {tc/4:7,.0f} {t3/4:7,.0f} {t6/3:7,.0f} ({tc/4/(tr/8):.1f}x, {t3/4/(tr/8):.1f}x)"
              f" | {tr/16.5:6,.0f} {tc/30:6,.0f} {t3/30:6,.0f} {t6/15:6,.0f}   [C7 {e[t][1]}, {e[t][2][3][3][0]} pkgs; g<=3 {e3[t][1]}]")
    U = q.gpu_env(r7.ultra_prof(), ctx); U6 = q.gpu_env(r7.ultra_vendor600(), ctx)
    A16 = c7(parts=dict(q.C7_PARTS, comp_w=2640 * 0.82), ctx=ctx)
    print(f"{'C7-A16 / Ultra bottom-up':<44}" + q.ratio(A16, U))
    print(f"{'C7-A16 / Ultra vendor-600 @100 PF':<44}" + q.ratio(A16, U6))
print("\n== p=0.6 and 6.2T (C7 / best Rubin)"); print(H)
for M, lab in ((m.V4, "1.6T"), (dict(m.V4, n_exp=1536), "6.2T")):
    for ctx in (q.C128, q.C1M):
        for p in (0.8, 0.6):
            print(f"{lab+' '+str(ctx//1024)+'K p'+str(p):<44}" + q.ratio(c7(ctx=ctx, p=p, M=M), q.gpu_env(q.RUBIN_PROF(), ctx, p=p, M=M)))
