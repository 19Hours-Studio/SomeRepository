# Real (own-stack) cost of one cache hit per turn vs recompute; storage tiers on two pricing bases;
# document-order canonicalisation. Llama-3-70B-class, H100 $2/h, 45% MFU, 3.35 TB/s HBM.
LIN, ATT = 2 * 70e9, 4 * 80 * 8192
KV = {"BF16": 2 * 80 * 8 * 128 * 2, "FP8": 2 * 80 * 8 * 128, "MLA-BF16 (DSV3)": 61 * 576 * 2}
FL, S, HBM = 0.45 * 989e12, 2.0 / 3600, 3.35e12
usd_per_M = lambda flop: flop / FL * S * 1e6

print("== recompute cost per token at context position ==")
for pos in (0, 50_000, 100_000):
    print(f"pos {pos:>7,}: ${usd_per_M(LIN + ATT * pos):.3f}/M tok")
print("\n== cost of one cached token for one turn (n_new new tokens attend to it, n_out decoded, gap_s parked) ==")
n_new, n_out, gap = 2300, 300, 30
att = usd_per_M(ATT * n_new)
rec = usd_per_M(LIN + ATT * 60_000)
print(f"prefill attention from {n_new} new tokens: ${att:.4f}/M  = {att/rec:.1%} of recompute at pos 60k (${rec:.3f}/M)")
for name, b in KV.items():
    dec = n_out * b / HBM * S * 1e6
    tiers = {"HBM": 2 / 80 / 3600, "DRAM cloud $0.005/GB-h": 0.005 / 3600, "DRAM capex $4/GB/3y": 4 / (3 * 8760 * 3600)}
    hold = {k: b / 1e9 * v * gap * 1e6 for k, v in tiers.items()}
    print(f"{name:16s} decode KV reads ({n_out} tok): ${dec:.4f}/M ; hold {gap}s: "
          + ", ".join(f"{k} ${v:.4f}/M" for k, v in hold.items())
          + f" ; reload 100k tok over PCIe 50GB/s: {1e5*b/50e9:.2f} s")
print("\n== storage break-even reuse interval (recompute $/M at pos 100k vs hold $/M-h) ==")
b = KV["BF16"]; rc = usd_per_M(LIN + ATT * 100_000) / 2 + usd_per_M(LIN) / 2   # avg over a 0..100k prefill
rc = usd_per_M(LIN + ATT * 50_000)
for tier, gbh in [("HBM $2/h/80GB", 2 / 80), ("DRAM cloud-rental", 0.005), ("DRAM capex 3y", 4 / (3 * 8760)),
                  ("NVMe cloud block", 0.0002), ("NVMe capex 3y", 0.08 / (3 * 8760))]:
    h = gbh * b / 1e9 * 1e6
    print(f"{tier:18s} ${h:.4f}/M-tok-h  break-even interval {rc/h:8.2f} h  (recompute avg over 100k prefill ${rc:.3f}/M)")
print("\n== document set grows by one doc per request: tokens rewritten ==")
import random, statistics
for D, size in [(10, 1000), (50, 500)]:
    rng = random.Random(0); hs = []
    for _ in range(2000):
        keys = sorted(rng.random() for _ in range(D)); newk = rng.random()
        rank = sum(1 for k in keys if k < newk)          # hash-sorted position of the new doc
        hs.append((D - rank + 1) * size)                  # new doc + every doc after it rewritten
    print(f"D={D} docs x {size} tok: hash-sort rewrites {statistics.mean(hs):,.0f} tok/request; first-seen order {size:,}"
          f" (+ rank line ~{5*D} tok)")
