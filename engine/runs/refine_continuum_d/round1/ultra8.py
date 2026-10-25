"""Rubin Ultra bounds: vendor 600 kW (trimmed 150 W like every GPU), and why the 'vendor 600 kW + undervolt law' bound is
rejected (PF/kW implied). Usage: python3 ultra8.py > ultra8.txt"""
import model8 as e8, run7_shim as r7
q, m = e8.q, e8.m
pf = lambda s: s["F4"] * s["s"] / s["P"] / 1e12      # PF per kW (FP4 incl. zero-skip)
rb = {l: pf(s) for l, s, f in e8.rubin_prof(0)}
u6 = q.ultra(600e3 / 144)
uv = {l: pf(s) for l, s, f in q.profiles(dict(u6, P_maxq=u6["P"]), comp_w=3440 * 4167 / 5690, leak_w=300 * 4167 / 5690,
                                         other_w=0, rack_share=1, vendor_maxq=False)}
c8 = {l: pf(s) for l, s, f in q.cont_prof(e8.C8, e8.C8_PARTS)}
print(f"PF/kW  Rubin Max-P {rb['0.75V']:.1f}, Rubin best {max(rb.values()):.1f} | Ultra 600 kW @100 PF {pf(u6):.1f}"
      f" ({pf(u6)/rb['0.75V']:.2f}x Rubin Max-P, same N3P) | Ultra 600 kW + law at 0.55 V {uv['0.55V']:.1f}"
      f" ({uv['0.55V']/max(rb.values()):.2f}x Rubin best) | C8 (4-HBM pkg, N2) 0.55 V wt {c8['0.55V wt']:.1f}")
for ctx in (q.C128, q.C1M):
    A = e8.c8_env(e8.C8, e8.C8_PARTS, ctx, labels=("0.55V wt", "0.60V wt", "0.55V"))
    U = e8.gpu_env([("v600t", dict(u6, P=u6["P"] - 150), 1.0)], ctx)
    print(f"{ctx//1024}K C8 / Ultra vendor 600 kW trimmed 150 W, 100 PF, full clock: {e8.rat(A, U)}")
