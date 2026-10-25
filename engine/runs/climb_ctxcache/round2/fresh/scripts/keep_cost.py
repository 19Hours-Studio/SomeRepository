# Is 1-h retention worth it for the provider? Compare the prefill compute it saves against the
# memory-time it costs, on the Bailian traces, for two KV formats. Storage-time counted: for every
# cached block, the time it sits beyond the 5-min window (until reuse, or 1 h after last use).
# H100 at $2/h, 45% of 989 dense TFLOP/s; DRAM $0.0066/GB-h (cloud memory-optimised VM price per GB);
# NVMe $0.00014/GB-h ($0.10/GB-month). Models: dense 72B (Qwen2.5-72B: 80 layers, 8 KV heads, d 128,
# BF16 KV = 320 KiB/token, 144 GFLOP/token) and MoE 30B-A3B (Qwen3-30B-A3B: 48 layers, 4 KV heads,
# BF16 KV = 96 KiB/token, 6.6 GFLOP/token). Attention FLOPs are ignored (they favour keeping a bit).
import json, sys
GPU = 2.0 / 3600 / (0.45 * 989e12)                  # $ per FLOP
TIERS = {"DRAM": 0.0066, "NVMe": 0.00014}           # $ per GB-hour
MODELS = {"dense 72B": (327680, 144e9), "MoE 30B-A3B": (98304, 6.6e9)}
for fn in sys.argv[1:]:
    last = {}; saved = 0; tok_all = 0.0; tok_reused = 0.0
    for line in open(fn):
        r = json.loads(line); t = r["timestamp"]; k = 0; k5 = k60 = 0; alive5 = alive60 = True
        for b in r["hash_ids"]:
            k = hash((k, b)); lu = last.get(k); age = t - lu if lu is not None else None
            alive5 = alive5 and age is not None and age <= 300; alive60 = alive60 and age is not None and age <= 3600
            k5 += alive5; k60 += alive60
            if age is not None:
                extra = 16 * max(0.0, min(age, 3600) - 300); tok_all += extra
                if age <= 3600: tok_reused += extra          # interval that ends in a reuse (oracle keeps only these)
            last[k] = t
        saved += 16 * (k60 - k5)
    t_end = t
    for lu in last.values(): tok_all += 16 * max(0.0, min(t_end - lu, 3600) - 300)
    print(f"{fn.split('/')[-1]}: prefill tokens saved by 1-h vs 5-min retention {saved/1e6:.1f}M; extra storage {tok_all/3600/1e6:.1f}M token-hours (keep-everything), {tok_reused/3600/1e6:.1f}M (oracle keeps only blocks that come back)")
    for mn, (kvb, fl) in MODELS.items():
        gain = saved * fl * GPU
        s = "  ".join(f"{tn}: cost/benefit {tok_all/3600*kvb/1e9*p/gain:6.2f} (oracle {tok_reused/3600*kvb/1e9*p/gain:5.2f})" for tn, p in TIERS.items())
        print(f"   {mn:12s} recompute avoided ${gain:6.2f}   {s}")
