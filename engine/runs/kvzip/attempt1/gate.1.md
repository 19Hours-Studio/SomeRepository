I ran all four ideas through the gate. Every one comes out **DEAD**: each fails its own deciding number on published data, and against NVFP4 on the decode-heavy workload (archetype B) none reaches the 1.5× system ratio. The only numbers measured here are on synthetic, Hadamard-rotated data, because real KV tensors can't be downloaded. The script reproduced the known Lloyd-Max error values to within 0.0002 before I used it. Anything marked "needs real-model run" is open.

How the CHAIN ratios were computed: archetype B shares (KV reads 50, weight reads 36, fixed 14), with NVFP4 KV (4.5 b/value) as the current best practice. Each ratio is given as a range. The low end assumes a fixed batch. The high end assumes batch size is limited by KV memory, so weight reads per request also fall with stored bits.

=== GATE ===
IDEA 1: Entropy-measured per-head bit allocation
KILLER | Largest share of heads that can sit at K4V4 and still average 2.1 b/value. Per-value cost with 0.25 b of scale/zero metadata: K2V1 = 1.75, K4V4 = 4.25 | required ≤14% of heads at K4V4 (≤19% with 0.125 b metadata, ≤4% with 0.5 b) | available: about 50% of heads must keep full precision on GQA to stay close to full attention on NIAH (DuoAttention, arXiv 2410.10819, Fig. 6). With 50% at K4V4 the floor is 3.0 b/value, or 5.3×, not 7.5×. Measured relative RMS error of 1-bit values is 0.60 (4.4 dB) | MARGIN 0.28
CHAIN | NVFP4 KV, 4.5 b | now 4.5 b/value, cost index 64.1 (fixed batch) / 38.2 (memory-limited batch) | with idea 2.1 b, index 56.6 / 25.3. At the realistic 3.0 b: about 1.08 / 1.3 | RATIO 1.13–1.51 (best case)
VERDICT | DEAD | The 2.1 b average only holds if about 14% or fewer of GQA heads are retrieval heads, but DuoAttention measured about 50%, so the realistic result is about 3 b. The Spearman ≥0.9 head-ranking stability it relies on needs a real-model run.
NEW FACT | DuoAttention needs 25% full-attention heads on MHA and 50% on GQA to stay close to full attention on NIAH. Its GQA memory saving is 1.67× | arXiv 2410.10819
NEW FACT | On R1-Distill-Llama-8B, AIME 2024–25: BF16 41.67, KIVI-4 35.00, KIVI-2 31.67, KVQuant-2 0 | arXiv 2512.19206 (MixKVQ)

IDEA 2: Progressive bit-plane attention
KILLER | Attention mass covered by the top 2% of pages during long CoT decoding | required ≥99% at a 2% budget | available: about 10% of tokens give about 95% of the softmax output in Kascade's example (arXiv 2512.16391). SeerAttention-R's oracle sparse attention needed about a 2k-token budget for lossless AIME at 11–18k average output length, which is 11–18% of tokens (arXiv 2506.08889). So 99% mass needs ≥10% of tokens. Per-head mass curves on R1-Distill need a real-model run | MARGIN ≈0.2 (2% / ≥10%)
CHAIN | NVFP4 KV | now 4.5 b read and 4.5 b stored, index 64.1 / 38.2 | with idea 2.19 b read (2.15 base + 2% refinement), 4.3 b stored, +12.5% two-pass kernel cost: index 57.8 / 31.4 | RATIO 1.11–1.22
VERDICT | DEAD | The top 2% is far short of 99% of attention mass. Storage stays at 4.3 b, so capacity barely beats NVFP4. Moving refinement planes to the host adds about 9 ms/step of PCIe traffic at batch 40, against 14 ms of HBM KV reads, which wipes out the read savings.
NEW FACT | Quest did not reach lossless AIME even at an 8k budget. SeerAttention-R (which needs a trained gate) got there at about 4k | arXiv 2506.08889
NEW FACT | Measured on rotated Gaussians: the top 2 planes of a 4-bit uniform code have 0.326 relative error (9.7 dB SQNR), against 0.095 (20.4 dB) for NVFP4 | gate.py measurement

IDEA 3: Bit-plane on-demand attention precision
KILLER | Its own bound: mass on coarse-only tokens × their value error ≤1e-3 per head. The measured coarse 2-plane value error is 0.326, so the coarse-only mass must stay ≤0.31% | required ≥99.7% of mass in top 2% + 4 sinks + 64-token window | available: a coarse-only mass of about 5–10% is implied by about 10% of tokens giving about 95% of the output (arXiv 2512.16391; SeerAttention-R oracle budget, arXiv 2506.08889), so the product is 0.016–0.033 | MARGIN 0.03–0.06
CHAIN | NVFP4 KV | now 4.5 b read and 4.5 b stored, index 64.1 / 38.2 | with idea 2.6 b read and 4.5 b stored (no capacity gain), index 58.1 (+0% kernel cost) to 59.5 (+12.5%) | RATIO 1.08–1.18. The claimed 1.5–1.6× is the attention kernel alone (4.5/2.6 = 1.73), not end to end
VERDICT | DEAD | It fails its own error bound by 15–30×. It stores exactly as many bytes as NVFP4, so it gains no batch capacity. End to end it gains about 1.1×.
NEW FACT | An LMDeploy deployment of TurboQuant K4V2 on Qwen3-30B measured 2195.8 tok/s against 2368.8 tok/s baseline, 7.3% slower. Rotated low-bit kernels do not automatically run faster | secondary report via morphllm/photonspark TurboQuant benchmark pages

IDEA 4: Rotated 3-bit fixed-codebook cache
KILLER | AIME accuracy gap against BF16 at long CoT with a 3-bit rotated KV cache | required ≤1 point | available: QuaRot (Hadamard rotation + 3-bit KV) on R1-Distill-Llama-8B, AIME-120: 27.50 vs 34.17, a 6.7-point gap (arXiv 2504.04823). A RoPE-aware K3V2 method lost 2.5 points (51.7 vs 54.2) on R1-Distill-Qwen-7B, and uniform TQ-MSE collapsed to 0 without a recent-token buffer (arXiv 2606.24033, summary only). Measured SQNR of the design is 14.7 dB, against 20.4 dB for NVFP4 | MARGIN 0.15 (0.4 if the 2.5-point result is the right comparison)
CHAIN | NVFP4 KV | now 4.5 b, index 64.1 / 38.2 | with idea 3.125 b read and stored, index 59.8 / 30.8 | RATIO 1.07–1.24
VERDICT | DEAD | The closest published 3-bit rotated result misses the 1-point AIME bar by 2.5–6.7×. Its error is 5.7 dB worse than NVFP4, and it gains at most 1.24× over NVFP4. A 32k AIME run on R1-Distill-8B with the FP8 sink and recent window is the one check that could overturn this.
NEW FACT | On LongBench with Llama-3.1-8B, TurboQuant scores 50.06 at 3.5 b (equal to the full cache) and 49.44 at 2.5 b. NIAH is 0.997 in every setting. This is non-reasoning only | secondary reports of arXiv 2504.19874 (yage.ai, insiderllm)
NEW FACT | Measured relative RMS error: 3-bit Lloyd-Max with an FP8 RMS scale per 64 gives 0.183, NVFP4 0.095, and 4-bit uniform per 32 0.078 | gate.py measurement

Reading across the four: once metadata is counted, every idea that goes below about 3 b/value runs into the same wall. Published results on reasoning models show multi-point AIME losses at 2–3 b. Against NVFP4 the best possible end-to-end gain in the decode-heavy workload is about 1.5×, and only if the format is both lossless and the batch is KV-memory-limited.

The script is `/home/user/SomeRepository/engine/runs/kvzip/gate/c1/gate.py` and its output is in `gate_out.txt` in the same directory. Nothing was committed.

Sources:
- [DuoAttention, arXiv 2410.10819](https://arxiv.org/pdf/2410.10819)
- [PRISM (secondary on DuoAttention ratios), arXiv 2603.21576](https://arxiv.org/pdf/2603.21576)
- [Quantization Hurts Reasoning?, arXiv 2504.04823](https://arxiv.org/pdf/2504.04823)
- [MixKVQ, arXiv 2512.19206](https://arxiv.org/pdf/2512.19206)
- [NSNQuant, arXiv 2505.18231](https://arxiv.org/pdf/2505.18231)
- [RoPE-Aware Bit Allocation, arXiv 2606.24033](https://arxiv.org/pdf/2606.24033)
- [SeerAttention-R, arXiv 2506.08889](https://arxiv.org/pdf/2506.08889)
- [Kascade, arXiv 2512.16391](https://www.arxiv.org/pdf/2512.16391)
- [Top-k attention <2% tokens, arXiv 2502.06766](https://arxiv.org/html/2502.06766v1)
- [Condensate Theorem (mass is insufficient), arXiv 2602.06317](https://arxiv.org/pdf/2602.06317)
- [Twilight, arXiv 2502.02770](https://arxiv.org/html/2502.02770v2)
- [TurboQuant summaries: yage.ai](https://yage.ai/share/turboquant-kv-cache-3-bit-en-20260325.html), [insiderllm](https://insiderllm.com/guides/turboquant-kv-cache-compression-local-ai/), [morphllm](https://www.morphllm.com/turboquant), [photonspark](https://photonspark.com/blog/turboquant-kv-cache-benchmarks)
- [SemKV, arXiv 2608.28911](https://arxiv.org/pdf/2608.28911)