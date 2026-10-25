# Physical marginal cost of a cache *read* on your own stack (Llama-3-70B, GQA 8 KV heads, BF16 KV, H100 SXM),
# per cached token per call, relative to recomputing that token (linear layers only, 2*70.6e9 FLOP).
L, Hq, d, Hkv = 80, 64, 128, 8
lin = 2 * 70.6e9
n_new = (2.7637e6 - 63 * 8559) / 2068          # mean new tokens per call in the 63 traces (terms.py inputs)
out_per_call = 322e3 / 2068                     # mean output tokens per call
attn = 4 * L * Hq * d * n_new                   # QK^T + AV FLOPs of the new tokens against one cached token
kvB = 2 * L * Hkv * d * 2                       # bytes of KV per token
t_tok = lin / (0.45 * 989e12)                   # GPU-seconds to recompute one token
t_dec = out_per_call * kvB / 3.35e12            # HBM time to stream one cached token's KV for every decoded token
print(f"new tokens/call={n_new:,.0f}  output tokens/call={out_per_call:.0f}  KV bytes/token={kvB/1e3:.0f} kB")
print(f"prefill attention over a cached token = {attn/lin:.3f}x of recompute")
print(f"decode KV streaming of a cached token  = {t_dec/t_tok:.3f}x of recompute (shared across B sessions with cascade attention)")
print("re-billing prior assistant output as read instead of write saves", f"{1.15*322e3/1e6:.2f}M units")
