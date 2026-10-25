# Own-stack (operator) cost of the REAL trace workload, using round-2 replay3 constants (70B GQA, BF16 KV 320 KB/token,
# H100 $2/h, 45% MFU, 3.35 TB/s). Real per-request prompt/new/output tokens and real inter-request gaps.
# Usage: python3 -I own4.py <trajs_dir>
import sys, glob, statistics as st
sys.path.insert(0, ".")
import trace4 as T, replay3 as R
LIN, ATT, KVB, GPU_S, FL, HBM = R.LIN, R.ATT, R.KVB, R.GPU_S, R.FLOPS, R.HBM
HBM_GBS, DRAM_GBS = 2 / 80 / 3600, 0.005 / 3600
tot = dict(new_prefill=0.0, att_over_cache=0.0, decode_kv=0.0, hold_pin=0.0, hold_swap=0.0, recompute_prefix=0.0)
for f in sorted(glob.glob(sys.argv[1] + "/*.json")):
    st_, _ = T.load(f)
    for j, s in enumerate(st_):
        L = s["L"]; c = st_[j - 1]["L"] if j else 0; m = L - c
        tot["new_prefill"] += (LIN * m + ATT * m * m / 2) / FL * GPU_S
        tot["att_over_cache"] += ATT * m * c / FL * GPU_S              # new tokens attending to cached prefix
        tot["decode_kv"] += s["out"] * L * KVB / HBM * GPU_S
        tot["recompute_prefix"] += (LIN * c + ATT * c * c / 2) / FL * GPU_S   # what a miss would add
        if j + 1 < len(st_) and st_[j + 1]["ts"] and s["ts"]:
            g = max(0.0, st_[j + 1]["ts"] - s["ts"]); gb = L * KVB / 1e9
            tot["hold_pin"] += gb * HBM_GBS * g
            tot["hold_swap"] += gb * DRAM_GBS * g + max(0, gb / 50 - 0.05) * GPU_S * 0  # reload hidden (see tiers3) -> 0 stall
base = tot["new_prefill"] + tot["att_over_cache"] + tot["decode_kv"]
print(f"operator $ for 441 tasks (cache hits, KV pinned in HBM over real gaps): {base + tot['hold_pin']:.2f}")
for k, v in tot.items(): print(f"  {k:17s} ${v:8.2f}  ({v/(base + tot['hold_pin']):.1%} of hit-path total)")
hit = tot["att_over_cache"] + min(tot["hold_pin"], tot["hold_swap"])
print(f"true marginal cost of the cache hits = attention over cached prefix + holding = ${hit:.2f}"
      f" = {hit/tot['recompute_prefix']:.1%} of recomputing those prefixes (API price: 10%)")
print(f"pin vs swap over real gaps (median 2.2 s): pin ${tot['hold_pin']:.2f}, swap ${tot['hold_swap']:.2f}")
print(f"decode KV reads are {tot['decode_kv']/(base+tot['hold_pin']):.1%} of operator cost: FP8 KV -> -{tot['decode_kv']/2/(base+tot['hold_pin']):.1%},"
      f" MLA-class 4.7x smaller KV -> -{tot['decode_kv']*(1-1/4.7)/(base+tot['hold_pin']):.1%} (prior art, architecture-dependent)")
