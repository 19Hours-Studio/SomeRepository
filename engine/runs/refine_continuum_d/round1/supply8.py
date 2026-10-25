"""Supply, silicon and BOM per unit of output, Continuum-8 vs Rubin (host-trimmed 150 W), 128K, p=0.8.
Usage: python3 supply8.py > supply8.txt"""
import model8 as e8
q, m = e8.q, e8.m
ctx = q.C128
A = e8.c8_env(e8.C8, e8.C8_PARTS, ctx, labels=("0.55V wt", "0.60V wt", "0.55V"))
RP = e8.rubin_prof(150); R = e8.gpu_env(RP, ctx)
good = 46                                     # good 750 mm2 C-dies per N2 wafer (round 7)
for t in (200, 1000, 2000):
    d = A[t][1]; effc = A[t][0]; npk, st, W = d["npk"], d["stacks"], d["W"]
    effr, labr = R[t][0], R[t][1]; Pr = [x for l, x, f in RP if l == labr][0]["P"]
    tc = effc * W / npk                        # output tok/s per C8 package
    tr = effr * Pr                             # per Rubin GPU
    per = 1e6                                  # per 1M output tok/s
    pk_c, pk_r = per / tc, per / tr
    print(f"\n>={t}: C8 {effc:.1f} tok/s/W, {tc:,.0f} tok/s/pkg, {st/npk:.2f} stacks/pkg | Rubin {effr:.1f} ({labr}, {Pr:.0f} W) {tr:,.0f} tok/s/GPU")
    print(f"  per 1M out tok/s: packages C8 {pk_c:,.0f} vs Rubin {pk_r:,.0f}")
    hc, hr = pk_c * st / npk, pk_r * 8
    print(f"  HBM stacks       C8 {hc:,.0f} (16-high, 48 GB) vs Rubin {hr:,.0f} (12-high, 36 GB): tokens/stack {hr/hc:.1f}x, tokens/GB {hr*36/(hc*48):.1f}x")
    n2, n4, n3 = pk_c * 30, pk_c * 60, pk_r * 16.5
    print(f"  logic cm2        C8 N2 {n2:,.0f} + N4 SRAM tiers {n4:,.0f} = {n2+n4:,.0f} vs Rubin N3P {n3:,.0f}: leading-edge {n2/n3:.2f}x, all silicon {(n2+n4)/n3:.2f}x")
    soic = pk_c * 4 * 2 / good                 # SoIC bonding passes (wafer-level, 2 tiers per C-die)
    print(f"  SoIC passes      {soic:,.0f} wafers per 1M tok/s")
    # BOM: C8 = 4 N2 dies 2.6-3.1k + 8 N4 tiers 2.5k + HBM 16-high 0.9-1.95k/stack + CoWoS-L/SoIC/test 2.5k ; Rubin 7.6-13k
    lo = 2.6 + 2.5 + 0.9 * st / npk + 2.5; hi = 3.1 + 2.5 + 1.95 * st / npk + 2.5; mid = (lo + hi) / 2
    rl, rh = 7.6, 13.0; rm = (rl + rh) / 2
    f = lambda c, r: (tc / c) / (tr / r)
    print(f"  BOM/pkg C8 ${lo:.1f}-{hi:.1f}k (mid {mid:.1f}k) vs Rubin ${rl}-{rh}k (mid {rm:.1f}k): tok/s per BOM$ ratio centre {f(mid, rm):.2f}, "
          f"crossed range {f(hi, rl):.2f}-{f(lo, rh):.2f}")
    print(f"  power per 1M tok/s: C8 {per/effc/1e3:.1f} kW vs Rubin {per/effr/1e3:.1f} kW")
