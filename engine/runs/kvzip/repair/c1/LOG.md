# LOG — repair c1 (kvzip)

| round | idea | change | decisive number | result |
|---|---|---|---|---|
| 0 | I1 Hadamard-E8 | novelty check | arXiv 2610.15384 (E8 k2v2, Oct 2026) + NexusQuant already publish uniform Hadamard+E8 KV | original = KNOWN |
| 1 | I1 | measured E8 vs scalar (e8sim.py) | E8 2b MSE 0.091 vs Lloyd-Max-2b 0.118 vs KIVI-style INT2 g128 0.25; E8 3b 0.030 vs LM 0.035; E8 4b 0.0091 ≈ NVFP4 0.0089 | E8 gain is 1.1 dB at 2b, 0.7 dB at 3b and about 0 at 4b, so the anchor is strongest at 2 b (values) |
| 2 | I1 | SOTA check | Block-GTQ (2606.24033): uniform-rotation TQ-MSE K3V2 collapses to 0.0 on AIME24 (R1-Distill-Qwen-7B); RoPE-block bit allocation K3V2 reaches 51.7 vs 54.2 FP16 | a global Hadamard with a uniform rate is the failure mode, so allocation is needed |
| 3 | I1 | rotate WITHIN RoPE-energy-ranked 8-dim bands, give E8 rates 4/3/2 b per band (keys mean 3.0 b), values E8 2b (alloc.py) | band allocation saves 0.07–1.0 b vs global Hadamard at equal logit-MSE (flat to outlier-heavy heads) | keeps the anchor and is not yet published; prediction is to beat Block-GTQ at equal bits |
| 4 | I1 | bit budget (budget.py) | 2.62 b/value at 32k (6.1x vs FP16), 2.58 at 128k, 3.0 at 4k | ok |
| 5 | I1 | kernel + cost | decode 12.5 op/B < 20 op/B CUDA-core ridge (H100); $5.06 vs Block-GTQ $5.17 per 1k correct AIME answers (predicted) | NICHE/WORKS-if-AIME holds |
| 6 | I1 | falsifier power | AIME24 needs ~340 samples/problem for a 2-pt diff at 3σ (9 H100-h/arm); "2 GPU-h" claim underpowered | use teacher-forced KL on FP16 CoT traces first |
| 0 | I2 online KLT | killer reproduced | pre-RoPE reconstruct 819 FLOP/B vs 295 ridge | original FAILS on decode |
| 1 | I2 | KLT on POST-RoPE keys, basis folded into q (U^T q) and into output for V | +0.39% decode FLOPs at 32k (was compute-bound) | killer removed |
| 2 | I2 | cost of the post-RoPE gain (alloc.py) | post-RoPE KLT saves 0.04–1.2 b vs Hadamard, only 0.0–0.3 b over band-energy allocation; pre-RoPE/NoPE saves 0.17–1.6 b | gain on RoPE keys is marginal |
| 3 | I2 | fix basis overhead claim | 128x128 FP16 basis = 0.0625 b/value at 32k (not <0.01); 0.5 b at 4k | need prompt ≥8k or FP8 basis |
| 4 | I2 | novelty | SVDq (pre-RoPE, reconstructs, post-RoPE "degrades"), KVTC (offline PCA+DP+DEFLATE, storage only) | online + folded + query-weighted is new |
| 5 | I2 | regime search | strongest where stored vector has no RoPE: values, MLA latent c_KV (absorbed W_UK/W_UV), NoPE layers (Llama-4 iRoPE, SmolLM3) | NICHE |
