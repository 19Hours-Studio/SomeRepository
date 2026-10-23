=== IDEAS ===
IDEA 1
NAME: RoPE-band-ranked Hadamard-E8 KV
MECHANISM: Anchor kept: a seeded Hadamard rotation plus an E8 lattice code decoded from a 256-entry shared-memory table. The original design rotated all 128 dimensions globally at one rate, and that is now published work (arXiv 2610.15384, E8 k2v2). It is also the configuration that collapses on reasoning: TurboQuant-MSE K3V2, which uses one rotation and one rate, scores 0.0 on AIME24 (Block-GTQ paper).

In the repaired design, the 64 RoPE pairs are ranked by their prefill energy. RoPE never changes a pair's norm, so the ranking holds during decode. They are grouped into 16 bands of 8 dimensions, with a Hadamard rotation inside each band. Bands are coded at 4, 3 or 2 bits with E8 (2b+2b residual, 2b+1b, 2b), giving keys a 3.0-bit average. Values use E8 at 2 bits, which is where E8 helps most. Simulated MSE is 0.091 for E8 against 0.118 for Lloyd-Max and 0.25 for KIVI-style INT2 g128.

Each token and head stores one FP8 scale. 4 sink tokens and the last 128 tokens stay in FP16. The query gets the same permutation and band rotation, so keys are stored post-RoPE exactly. Total is 2.62 b/value at 32k (6.1× vs FP16) and 3.0 b at 4k (5.3×). Decode dequantization is 12.5 op/B, under the H100 CUDA-core ridge of about 20 op/B. Prefill encode cost is +0.007%.
VALUE: Same 6× memory and about 6.2× the decode throughput of BF16 at 32k as Block-GTQ K3V2. The prediction is that it loses less on AIME (≤2 points vs −2.5). That would be about $5.06 vs $5.17 per 1,000 correct AIME answers, roughly 2% cheaper, which is a small edge.

IDEA 2
NAME: Folded online KLT water-filling
MECHANISM: Anchor kept: each request accumulates its own covariance during prefill, takes a KLT basis from it, and allocates bits per component by reverse water-filling, with no calibration data. The fatal step was rebuilding every key (819 FLOP/B against a 295 FLOP/B ridge). That is removed by computing the KLT on post-RoPE keys, so attention scores from the stored coefficients using q′ = Uᵀq, and by folding the value basis into the output (o = U_v·Σp·c). This adds +0.39% decode FLOPs at 32k.

The distortion is weighted by the request's own prefill query covariance. The basis is refreshed every 32k generated tokens. Prompts under 1,024 tokens fall back to Hadamard.

The corrected basis overhead is 0.0625 b/value per FP16 basis at 32k, not "<0.01". Total is about 2.74 b at 32k (5.8×). The model's decisive number is that the post-RoPE KLT gains only 0.0–0.3 b over plain RoPE-band energy allocation on RoPE keys. On stores with no RoPE it gains 0.17–1.6 b over Hadamard: values, MLA latents c_KV (folded into the absorbed W_UK/W_UV) and NoPE layers. So the design is retargeted at those stores.
VALUE: For MLA models (DeepSeek-V3/R1, Kimi-K2) and NoPE/iRoPE layers, it is a calibration-free way to read a compressed cache directly in HBM. If the real-tensor gain is ≥0.5 b, it would be about 1.2× cheaper per served token than Hadamard/TurboQuant at the same quality. On ordinary RoPE keys it is about equal to Block-GTQ (≈1.0×).

=== NOTES ===
I ran everything in Python: e8sim.py, alloc.py, budget.py and power.out are in the folder, along with LOG.md and NOTES.md. I could not run a real model, so every accuracy figure below is a prediction or a published number.

**Idea 1 — anchor kept? Yes.** The rotation and E8 table are unchanged; only where the rotation applies and how rates are assigned changed.
- **Decisive numbers:**
  - Simulated MSE on a unit Gaussian: E8 2b 0.091, 3b 0.030, 4b 0.0091; Lloyd-Max 2/3/4b 0.118/0.035/0.0095; NVFP4 0.0089. This matches QuIP#'s E8P figure.
  - So E8 beats scalar by about 1.1 dB at 2 bits, about 0.7 dB at 3 bits and about 0 at 4 bits. That is why the 2-bit values are kept.
  - In the synthetic model, band allocation saves 0.07–1.0 b at equal logit MSE, from flat heads to heads with strong outliers.
  - SOTA reference (Block-GTQ, AIME24/25 on R1-Distill-Qwen-7B): FP16 54.2/37.9, Block-GTQ K3V2 51.7/37.5, TurboQuant-MSE with uniform rate 0/0.
- **Baselines, $ per 1,000 correct AIME answers** (H100 at $2.99/h, 32k context, memory-bound decode):

| Format | $ per 1,000 correct |
|---|---|
| BF16 | 30.4 |
| FP8 | 15.4 |
| KIVI-2 | 5.35 |
| Block-GTQ | 5.17 |
| Kitty | 4.47, if its −3.5 points holds |
| This design (predicted) | 5.06 |

- **Consistency table** (in NOTES.md): all limits are met. Arithmetic intensity has 1.6× margin. Stability of the band ranking over a 32k chain of thought is unmeasured; the design re-ranks every 4k tokens, which costs 384 bits.
- **Hazards:** 2-bit values are still the riskiest part for long chain of thought. On MHA models with the dot product on CUDA cores the kernel reaches 18.8 op/B, close to the ridge.
- **Deciding unknown and experiment:** the AIME change against Block-GTQ at equal bits. The "2 GPU-hour" test in the original is underpowered: a 2-point difference at 3σ needs about 340 samples per problem, about 9 H100-hours per arm. The cheap first test is teacher-forced KL and top-1 flip rate on 64 FP16 chain-of-thought traces of 16–32k tokens each, which takes minutes. It falsifies the idea if band-E8 is not below Block-GTQ.
- **Closest work:** arXiv 2610.15384 / NexusQuant (uniform E8), Block-GTQ (scalar RoPE-block allocation), QuIP#.
- **Verdict: NICHE.** It works if the AIME result holds, and its edge over the state of the art is small.

**Idea 2 — anchor kept? Yes.** It is still per-request, online and water-filled; the basis is now applied after RoPE and folded into the query and output.
- **Decisive numbers:**
  - The killer (819 FLOP/B) is replaced by +0.39% decode FLOPs at 32k.
  - Prefill overhead is +0.15% (70B-class model at 32k).
  - The modelled post-RoPE gain over band allocation is only 0.0–0.3 b. This agrees with Loki (post-rotary keys have higher rank) and with SVDq (post-RoPE is worse).
- **Baselines:** Block-GTQ and TurboQuant per served token. It is about equal on RoPE keys and could be about 1.2× better on stores without RoPE.
- **Consistency:** the basis overhead claim was wrong (0.0625 b per basis at 32k, 0.5 b at 4k). With chunked prefill from a 2,048-token first chunk, eigenvalue error is about 25%, which misallocates up to about 0.16 b.
- **Hazards:** short prompts, covariance drift during the chain of thought, and kernels needing several bit-widths at once.
- **Deciding unknown:** the real query-weighted AM/GM gain on MLA c_KV, on values and on NoPE layers. The experiment is one forward pass dumping 8 prompts × 32k tokens from DeepSeek-V2-Lite and Llama-3.1-8B. It is falsified if the median gain is under 0.3 b.
- **Closest work:** SVDq, KVTC (offline PCA with DEFLATE, storage only), Palu.
- **Verdict:** FAILS on RoPE keys; NICHE for MLA, NoPE layers and values.

Sources: [E8 key quantization 2610.15384](https://arxiv.org/abs/2610.15384), [NexusQuant](https://github.com/jagmarques/nexusquant), [Block-GTQ 2606.24033](https://arxiv.org/pdf/2606.24033), [QuIP#](https://arxiv.org/pdf/2402.04396), [SVDq](https://arxiv.org/pdf/2502.15304), [KVTC](https://arxiv.org/pdf/2511.01815), [Loki](https://arxiv.org/pdf/2406.02542), [MixKVQ](https://arxiv.org/pdf/2512.19206), [Kitty](https://arxiv.org/pdf/2511.18643), [TurboQuant summary](https://techinformed.com/?p=38291), [AnchorKV](https://arxiv.org/pdf/2608.02901), [KVQuant](https://arxiv.org/pdf/2401.18079)