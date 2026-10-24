"""Idea 1 round 5: long context, Ironwood comparison, KV-slice replication for die failure."""
import math
N1, PRICE, KW = 333, 2.44e6, 117
HOURS = 4 * 365 * 24 * 0.7
def usd(price, kw, th): return (price + kw * HOURS * 0.13) / (th * HOURS * 3600) * 1e6
kvb = lambda ctx, b=4.5: 576 * 61 * ctx * b / 8
fl = lambda ctx: 2 * 128 * 1088 * ctx * 61 + 74e9
for ctx in (8192, 32768, 131072):
    mem = 1e12 / (kvb(ctx) / N1); cmp_ = 1308e12 * 0.6 / (fl(ctx) / N1)
    th = min(mem, cmp_)
    # Rubin NVL72 at 100 tok/s/user, compute- or memory-bound
    ws = 377e9 / 72; t = 0.01 - 2 * 58 * 5e-6
    rB = min((t - ws / 22e12) * 22e12 / kvb(ctx), 16e15 * 0.6 * t / fl(ctx), (288e9 - ws) / kvb(ctx))
    r = rB * 100 * 72
    # Ironwood: 192 GB, 7.37 TB/s, 4.614 PF FP8 [S Google]; 64-chip slice holds weights (5.9 GB/chip)
    ws_i = 377e9 / 64
    iB = min((t - ws_i / 7.37e12) * 7.37e12 / kvb(ctx), 4.614e15 * 0.6 * t / fl(ctx), (192e9 - ws_i) / kvb(ctx))
    i_chip = iB * 100
    print(f"ctx {ctx:6d}: C-D {th/1e3:6.0f}k tok/s (${usd(PRICE,KW,th):.3f}/Mtok) | Rubin@100tps {r/1e3:6.0f}k (${usd(7.8e6,190,r):.3f}) "
          f"| per-chip: C-D {th/N1:5.0f} tok/s, Ironwood {i_chip:6.0f} tok/s, Rubin pkg {r/72:6.0f}")
# replication: every user's KV is sliced across all dies -> one die loss = all users lose a slice
users = 414e3 / 50
rep_cap = 2 * users * kvb(32768) / N1 / 1e9
wr_bw = 414e3 * kvb(1) / N1 * 2
print(f"KV slice replication at 50 tok/s/user, 32K: {users:.0f} users -> {rep_cap:.1f} GB/die (cap 32) ; extra write BW {wr_bw/1e9:.3f} GB/s/die")
print(f"Capacity margin with replication: {32/rep_cap:.2f}")
# SRAM capacity margin, DeepSeek-V3 NVFP4
print(f"SRAM margin: {N1*1.25/377:.3f} (incl. 10% for replicated dense/attn weights & spares)")
