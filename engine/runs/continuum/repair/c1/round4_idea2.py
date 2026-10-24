"""Idea 2 round 4: HBM-halved expert-stationary package (4 HBM4 stacks for KV only + 4 SRAM layers/die for experts)
vs full Rubin (8 HBM4 stacks, weights+KV in HBM). Same compute (16 PF FP8 dense [E]), 72 pkgs."""
HBM_STACK_USD = 0.26 * 7.8e6 / (72 * 8)   # [S] memory 26% of $7.8M (Morgan Stanley via digitalcitizen) -> upper bound per stack
STACK_ADD = 4279                           # from model.py (SRAM dies + bonding, BOM)
def thr(P, Pact, heads, moe_l, tps, a2a, bw, cap, w_in_sram, ctx=32768, mfu=0.6, fp8=16e15, L=61):
    ws = P * 4.5 / 8 / 72; kvb = 576 * L * ctx * 4.5 / 8; fl = 2 * heads * 1088 * ctx * L + 2 * Pact
    t = 1 / tps; tc = 2 * moe_l * a2a * 1e-6; tw = 0 if w_in_sram else ws / bw
    if t - tc - tw <= 0: return 0
    B = min((t - tc - tw) * bw / kvb, fp8 * mfu * (t - tc) / fl, (cap - (0 if w_in_sram else ws)) / kvb)
    return B * tps * 72
print(f"HBM4 stack cost (upper bound) ${HBM_STACK_USD:.0f}; 4 stacks saved ${4*HBM_STACK_USD:.0f} vs SRAM stack +${STACK_ADD}")
d_bom = -4 * HBM_STACK_USD + STACK_ADD
price_ratio = (7.8e6 + 72 * d_bom * 3) / 7.8e6    # BOM delta x3 markup
print(f"Package BOM delta {d_bom:+.0f}$; rack price ratio {price_ratio:.3f}")
for name, P, Pa, h, ml in (("DeepSeek-V3", 671e9, 37e9, 128, 58), ("Kimi-K2 1T", 1.04e12, 32e9, 64, 60)):
    print(f"\n{name}  tps a2a | Rubin8stk  Exp-stat4stk | thr ratio  $/tok ratio(lower=better for Exp-stat)")
    for mfu in (0.6, 0.35):
        for tps in (100, 300, 500, 1000):
            for a2a in (2, 5):
                r = thr(P, Pa, h, ml, tps, a2a, 22e12, 288e9, False, mfu=mfu)
                s = thr(P, Pa, h, ml, tps, a2a, 11e12, 144e9, True, mfu=mfu)
                rr = s / r if r else float('inf')
                cr = price_ratio / rr if rr else float('inf')
                print(f"  mfu{mfu} {tps:5d} {a2a:2d} | {r/1e3:6.0f}k {s/1e3:6.0f}k | {rr:5.2f} {cr:5.2f}")
