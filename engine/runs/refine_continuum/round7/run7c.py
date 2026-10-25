"""Round 7: C7 operating points, Vmin floor 0.60 V, and power breakdown. Usage: python3 run7c.py > run7c.txt"""
import model7 as q, model5 as m
for ctx in (q.C128, q.C1M):
    R = q.gpu_env(q.RUBIN_PROF(), ctx)
    E = q.pipe_env(q.cont_prof(q.C7, q.C7_PARTS), ctx, gs=(1, 2, 3, 4, 6))
    print(f"== {ctx//1024}K operating points")
    for t in q.T:
        v, lab, (val, k, spd, pt) = E[t]
        d = pt[4]
        print(f" C7 >={t}: {v:.1f} tok/s/W {lab} k={k} b={pt[2]} m={pt[3][1]} pkgs={pt[3][0]} {spd:,.0f} tok/s/user users {d['users']:,} | "
              f"us/microbatch: sram {d['sram']*1e6:.1f} kv {d['kv']*1e6:.1f} comp {d['comp']*1e6:.1f} link {d['link']*1e6:.1f} c {d['c']*1e6:.1f} T {d['T']*1e6:.1f}")
        v, lab, (val, k, spd, pt) = R[t]; d = pt[4]
        print(f" Rubin >={t}: {v:.1f} {lab} k={k} B={pt[2]} (t,m)={pt[3]} {spd:,.0f} tok/s/user | mem {d['mem']*1e6/62:.1f} comp {d['comp']*1e6/62:.1f} T {d['T']*1e6:.1f}")
    old = q.VMENU; q.VMENU = (0.75, 0.65, 0.60)
    R6 = q.gpu_env(q.RUBIN_PROF(), ctx); E6 = q.pipe_env(q.cont_prof(q.C7, q.C7_PARTS), ctx, gs=(1, 2, 3, 4, 6))
    print(" Vmin floor 0.60 V for all:  C7/Rubin " + q.ratio(E6, R6))
    q.VMENU = (0.75,)
    R0 = q.gpu_env(q.RUBIN_PROF(), ctx); E0 = q.pipe_env(q.cont_prof(q.C7, q.C7_PARTS), ctx, gs=(1, 2, 3, 4, 6))
    print(" vendor Max-P/Max-Q only for all: C7/Rubin " + q.ratio(E0, R0))
    q.VMENU = old
P = q.C7_PARTS
for V in (0.75, 0.55):
    f, e = q.fr(V), q.er(V); ws = f if V < 0.75 else 1
    parts = dict(compute=P["comp_w"] * f * e, leakage=P["leak_w"] * V / 0.75, wtier=P["wt_w"] * ws, hbm=320, links=288)
    pk = sum(parts.values())
    print(f"C7 at {V} V: " + ", ".join(f"{k} {v:.0f}" for k, v in parts.items()) + f" -> package {pk:.0f} W; +14.6% conv/cool {0.146*pk:.0f}; host/NIC/switch 230 -> slot {pk*1.146+230:.0f} W; dense FP4 {64*f:.1f} PF")
