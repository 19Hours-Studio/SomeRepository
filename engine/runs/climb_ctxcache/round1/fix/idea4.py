# Idea 4: break-even reuse interval per model = (own recompute $/token, incl. attention) / (own KV storage $/token-hour).
# Same H100 price/MFU for both models (assumptions: $2/h, 45% of 989 TFLOP/s BF16 dense).
GPU, FL = 2.0, 0.45 * 989e12
TIER = {"HBM": 2 / 80, "DRAM": 0.005, "NVMe": 0.0002}          # $/GB-h (assumptions, as in baseline)
models = {
  # name: (active params, KV bytes/token, attention FLOPs per (token, context position))
  "Llama-3-70B, BF16 KV": (70e9, 2*80*8*128*2, 4*80*8192),
  "Llama-3-70B, FP8 KV":  (70e9, 2*80*8*128*1, 4*80*8192),
  # DeepSeek-V3 MLA, prefill in non-absorbed form: per layer 128 heads x (QK over 192 dims + AV over 128 dims) x 2 FLOPs
  "DeepSeek-V3, BF16 MLA": (37e9, 61*576*2, 61*128*(192+128)*2),
}
for m, (P, b, af) in models.items():
    for ctx in (8_000, 32_000, 100_000):
        flops = 2*P + af*ctx/2                                   # causal prefill: mean context ctx/2
        usd = flops / FL * GPU / 3600                            # $ per token recomputed
        row = "  ".join(f"{t} {60*usd/(c*b/1e9):6.1f} min" for t, c in TIER.items())
        print(f"{m:22s} ctx={ctx:>6}: recompute ${usd*1e6:.3f}/M tok | break-even reuse interval: {row}")
