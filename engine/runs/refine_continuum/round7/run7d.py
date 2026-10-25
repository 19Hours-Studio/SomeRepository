"""Round 7 final tables (symmetric V/f law and slot-saving rule for every system).
Usage: python3 run7d.py > run7d.txt"""
import model7 as q, model5 as m, run7 as r7
GS = (1, 2, 3, 4, 6)
def env(base, parts, ctx, p=0.8, M=m.V4, gs=GS): return q.pipe_env(q.cont_prof(base, parts), ctx, p=p, M=M, gs=gs)
def rub(ctx, p=0.8, M=m.V4, s=1.43): return q.gpu_env([(a, dict(x, s=s), f) for a, x, f in q.RUBIN_PROF()], ctx, p=p, M=M)
H = " " * 46 + " ".join(f"{t:>6}" for t in q.T)
for kvfp4 in (False, True):
    m.OPT["kv_fp4"] = kvfp4
    for ctx in (q.C128, q.C1M):
        R = rub(ctx); U = q.gpu_env(r7.ultra_prof(), ctx); U6 = q.gpu_env(r7.ultra_vendor600(), ctx)
        A = env(q.C7T, q.C7T_PARTS, ctx)
        print(f"\n== {ctx//1024}K p=0.8 KV {'NVFP4' if kvfp4 else 'FP8'} (all systems)"); print(H)
        print(f"{'Rubin best (tok/s/W)':<46}" + q.vals(R))
        print(f"{'Continuum-7 (tok/s/W)':<46}" + q.vals(A))
        print(f"{'C7 / Rubin':<46}" + q.ratio(A, R))
        print(f"{'C7 / Ultra bottom-up (5.69 kW full clock)':<46}" + q.ratio(A, U))
        print(f"{'C7 / Ultra vendor 600 kW at 100 PF':<46}" + q.ratio(A, U6))
        if kvfp4: continue
        print(f"{'  C6 (round 6 package) / Rubin':<46}" + q.ratio(env(q.C6, q.C6_PARTS, ctx, gs=(3, 4, 6)), R))
        print(f"{'  C7 untrimmed / Rubin':<46}" + q.ratio(env(q.C7, q.C7_PARTS, ctx), R))
        sens = [("same node: C-die compute energy x1.25 (N3P)", env(q.C7T, dict(q.C7T_PARTS, comp_w=3300), ctx)),
                ("eta 0.5 on Continuum only", env(dict(q.C7T, F4=q.C7T['F4'] * 5 / 6, F8=q.C7T['F8'] * 5 / 6), q.C7T_PARTS, ctx)),
                ("tile imbalance 1.25", env(dict(q.C7T, imb=1.25), q.C7T_PARTS, ctx)),
                ("leakage 2x (SRAM tiers leak more)", env(q.C7T, dict(q.C7T_PARTS, leak_w=1000), ctx)),
                ("W-tier 0.30 pJ/bit", env(q.C7T, dict(q.C7T_PARTS, wt_w=1228), ctx)),
                ("g <= 3 only (187-package pod)", env(q.C7T, q.C7T_PARTS, ctx, gs=(1, 2, 3))),
                ("A16 C-dies (compute power -18%)", env(q.C7T, dict(q.C7T_PARTS, comp_w=2640 * 0.82), ctx))]
        for lab, e in sens: print(f"{'  ' + lab:<46}" + q.ratio(e, R))
        Rn = rub(ctx, s=1.0); An = q.pipe_env([(a, dict(x, s=1.0), f) for a, x, f in q.cont_prof(q.C7T, q.C7T_PARTS)], ctx, gs=GS)
        print(f"{'  no zero-skip on either side':<46}" + q.ratio(An, Rn))
        oldt = q.tau_f; q.tau_f = lambda f: (12 + 3 / f) * 1e-6
        e = env(q.C7T, q.C7T_PARTS, ctx); q.tau_f = oldt
        print(f"{'  Continuum collectives 12 us (tau 15 at f0)':<46}" + q.ratio(e, R))
        oldv = q.VMENU; q.VMENU = (0.75, 0.65, 0.60)
        print(f"{'  Vmin floor 0.60 V for all':<46}" + q.ratio(env(q.C7T, q.C7T_PARTS, ctx), rub(ctx)))
        q.VMENU = (0.75,)
        print(f"{'  vendor Max-P/Max-Q only for all':<46}" + q.ratio(env(q.C7T, q.C7T_PARTS, ctx), rub(ctx)))
        q.VMENU = oldv
        A16 = env(q.C7T, dict(q.C7T_PARTS, comp_w=2640 * 0.82), ctx)
        print(f"{'  C7-A16 / Ultra bottom-up':<46}" + q.ratio(A16, U))
        print(f"{'  C7-A16 / Ultra vendor 600 kW':<46}" + q.ratio(A16, U6))
        print("  operating points:")
        for t in q.T:
            v, lab, (val, k, spd, pt) = A[t]; d = pt[4]
            Pc = [x for a, x, f in q.cont_prof(q.C7T, q.C7T_PARTS) if a == lab.split(" g")[0]][0]["P"]
            v2, lab2, (_, k2, spd2, pt2) = R[t]
            Pr = [x for a, x, f in q.RUBIN_PROF() if a == lab2][0]["P"]
            print(f"   >={t}: C7 {v:.1f} {lab} slot {Pc:.0f} W k={k} b={pt[2]} m={pt[3][1]} pkgs={pt[3][0]} {spd:,.0f} tok/s/user users {d['users']:,}"
                  f" | us sram {d['sram']*1e6:.1f} kv {d['kv']*1e6:.1f} comp {d['comp']*1e6:.1f} link {d['link']*1e6:.1f} T {d['T']*1e6:.1f}"
                  f" || Rubin {v2:.1f} {lab2} slot {Pr:.0f} W k={k2} B={pt2[2]} (t,m)={pt2[3]} {spd2:,.0f} tok/s/user"
                  f" || per HBM stack C7 {v*Pc/4:,.0f} Rubin {v2*Pr/8:,.0f} ({v*Pc/4/(v2*Pr/8):.1f}x)")
m.OPT["kv_fp4"] = False
print("\n== p=0.6 and 6.2T: C7 / best Rubin"); print(H)
for M, lab in ((m.V4, "1.6T"), (dict(m.V4, n_exp=1536), "6.2T")):
    for ctx in (q.C128, q.C1M):
        for p in (0.8, 0.6):
            print(f"{lab+' '+str(ctx//1024)+'K p'+str(p):<46}" + q.ratio(env(q.C7T, q.C7T_PARTS, ctx, p=p, M=M), rub(ctx, p=p, M=M)))
print("\n== all systems, 128K / 1M, p 0.8 (C7 / X)")
for ctx in (q.C128, q.C1M):
    A = env(q.C7T, q.C7T_PARTS, ctx); print(f"-- {ctx//1024}K  C7 max tok/s/user {A['max']:.0f}"); print(H)
    E = {n: q.gpu_env(r7.sys_prof(n), ctx) for n in ("MI455X", "TPU8i", "Ironwood")}
    E["Rubin+LPX (LP30 FP8)"] = q.afd_env(ctx)
    E["CS-4"] = q.best_over([("w", m.envelope(lambda k: m.pipe_points(m.WSE, 9e-6, ctx, k, 0.8, kv_in_sram=True), q.T))])
    for n, e in E.items(): print(f"{'C7 / ' + n:<46}" + q.ratio(A, e) + f"   max {e['max']:.0f}")
