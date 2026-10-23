# Repair notes c1 — consistency tables (scripts: e8sim.py, alloc.py, budget.py; outputs *.out, power.out)

## Idea 1 — band-allocated Hadamard-E8
| limit / window | value relied on | computed | margin | status |
|---|---|---|---|---|
| E8 codebook ball (2^16 pts, r²≤12) vs post-Hadamard Gaussian tail | overload rare | MSE 0.091 incl. overload (e8sim) | — | ok |
| CUDA-core ridge H100 (67 TF / 3.35 TB/s ≈ 20 op/B) | decode-side dequant | 12.5 op/B (dot on tensor cores) | 1.6x | ok; MHA with CUDA-core dot 18.8 op/B is tight |
| shared-memory table | 256 x 8 B = 2 KB | 228 KB/SM | >100x | ok |
| band energies stable over 32k CoT | RoPE preserves pair norm; semantic drift not | re-rank every 4k tokens, 384 b permutation | — | unmeasured |
| bits at short context | ≤3 b | 3.0 b at 4k (5.3x) | — | ok |
| FP8 E4M3 per-token scale range (2^-9..448) | relative to per-head FP16 scale | — | — | ok |
| AIME falsifier power | 2-pt diff at 3σ | ~340 samples/problem, ~9 H100-h/arm | — | the "2 GPU-h" in the original was underpowered |

## Idea 2 — online post-RoPE KLT, folded
| limit / window | value relied on | computed | margin | status |
|---|---|---|---|---|
| decode compute | basis transforms on q and o only | +0.39% FLOPs at 32k, +3.1% at 4k | — | ok (was 819 vs 295 FLOP/B) |
| basis metadata | ≤0.13 b | 0.0625 b per basis at 32k; 0.5 b at 4k | — | original "<0.01 b" was wrong; need prompt ≥8k or FP8 basis |
| covariance sample size | N/d ≥ 8 (N≥1024) | chunked prefill with 2048 tokens: rel. eig error ≈ sqrt(d/N) = 0.25, about 0.16 b misallocation | — | Hadamard fallback below 1024 tokens |
| prefill overhead | covariance accumulation | +0.15% (70B, 32k) | — | ok |
| coding gain, RoPE keys | ≥0.3 b over band-energy allocation | 0.0–0.3 b (model) | ≤1x | FAILS as the main lever |
| coding gain, no-RoPE stores (V, MLA c_KV, NoPE layers) | ≥0.3 b over Hadamard | 0.17–1.6 b (model, pre-RoPE proxy) | — | unmeasured on real tensors |
