"""Idea 2 round 3: strongest regime = most weight bytes per package (1T-class MoE in one NVL72), high tok/s/user."""
import math
def run(name, P_TOT, P_ACT, LAYERS, MOE_L, HEADS, ctx=32768, kvbits=4.5, bw=22e12, fp8=16e15, mfu=0.6, pkgs=72):
    W = P_TOT * 4.5 / 8; ws = W / pkgs
    kvb = (512 + 64) * LAYERS * ctx * kvbits / 8
    fl = 2 * HEADS * 1088 * ctx * LAYERS + 2 * P_ACT
    print(f"\n{name}: weights/pkg {ws/1e9:.1f} GB (stack cap 13.7 GB) -> HBM read {ws/bw*1e3:.2f} ms/step; KV/user {kvb/1e9:.2f} GB")
    print(" tps a2a | Rubin   Stacked  gain | stacked HBM-bound?")
    for tps in (300, 500, 750, 1000):
        for a2a in (2, 5):
            t = 1 / tps; tc = 2 * MOE_L * a2a * 1e-6
            def thr(tw):
                if t - tc - tw <= 0: return 0, ''
                Bm = (t - tc - tw) * bw / kvb; Bc = fp8 * mfu * (t - tc) / fl; Bk = (288e9 - (ws if tw else 0)) / kvb
                B = min(Bm, Bc, Bk); return B * tps * pkgs, ['mem', 'cmp', 'cap'][[Bm, Bc, Bk].index(B)]
            r, rb = thr(ws / bw); s, sb = thr(0)
            g = f"{s/r:4.2f}x" if r else ("inf" if s else "n/a")
            print(f"{tps:4d} {a2a:3d} | {r/1e3:5.0f}k {s/1e3:6.0f}k {g:>6} | Rubin:{rb} Stk:{sb}")
run("DeepSeek-V3 671B/37B", 671e9, 37e9, 61, 58, 128)
run("Kimi-K2 1.04T/32B (64 heads)", 1.04e12, 32e9, 61, 60, 64)
run("Kimi-K2, FP8 attention MFU 0.35 (realistic decode)", 1.04e12, 32e9, 61, 60, 64, mfu=0.35)
run("Kimi-K2 on half-Rubin pkg (11 TB/s, 8 PF) x72", 1.04e12, 32e9, 61, 60, 64, bw=11e12, fp8=8e15)
