**Recommended format: 2.0-bit KV ("HTQ-KV"), calibration-free.** It is 8× smaller than FP16 and 4× smaller than FP8, counting all metadata.

**Accounting per 128-dimension head vector**
- Payload: 1.875 bits per value.
- One FP16 norm: 0.125 bits per value.
- 4 sink tokens and a 128-token recent window in FP8: about 0.01 bits per value at 128k.
- Total: about 2.0 bits per value.

**Why it should beat earlier 2-bit attempts**
- A random Hadamard rotation makes every head vector close to Gaussian. A fixed trellis codebook then needs no calibration and no outlier sidecar.
- Trellis coding at 2 bits gets within about 1 dB of the Gaussian rate-distortion bound (D = 2⁻⁴ ≈ −12 dB). Scalar Lloyd-Max quantization at 2 bits gives about −9.3 dB (MSE 0.1175).

**Target quality (unverified hypothesis)**
- At most a 1% relative drop on AIME24/25 and MATH-500 with R1-Distill-8B and Qwen3-8B at 32k CoT, and on RULER-128k with Llama-3.1-8B/70B.
- Perplexity rises by no more than 0.05.

**Runtime**
- Prefill: the current chunk runs at BF16 and is encoded when the chunk finishes, adding under 3% to prefill.
- Decode: a FlashDecoding-style kernel decodes the trellis in registers, then applies RoPE and runs the dot product.
- Throughput: in archetype B, the KV-read term falls from 50% to about 12.5% of cost. That is about 1.6× tokens per second at fixed batch, and about 2× once the larger batches the freed capacity allows are counted.
- The ceiling of 12.5× leaves room for this gain.

**Deciding quantity:** the attention-logit error divided by the logit spread of each head. This must stay at or below about 0.1 on long-CoT retrieval heads.

**Cheap falsifier:** simulate the format in PyTorch on R1-Distill-8B with AIME24 (30 problems × 8 samples, about 4 GPU-hours). A drop of more than 1 point kills the design.

=== IDEAS ===
IDEA 1
NAME: Hadamard-trellis 2-bit KV
MECHANISM: Each pre-RoPE key and value head vector is rotated by a fixed random Hadamard matrix and stored as one FP16 norm plus trellis-coded indices at 1.875 bits per value. Four sink tokens and the last 128 tokens stay in FP8. The fused decode kernel decodes the trellis in registers, then applies RoPE and runs attention. The closest earlier attempt is TurboQuant, which lost 18 GSM8K points at 3 bits because its scalar bins plus noisy QJL correction waste about 3 dB. Trellis vector coding recovers about 2 dB of that, and the design has no QJL stage. The deciding quantity is the logit error relative to the per-head logit spread.
VALUE: A drop-in, calibration-free 8× KV cache versus FP16, about 2× smaller than NVFP4, which should give roughly 1.6–2× reasoning decode throughput.

IDEA 2
NAME: Coarse-HBM, refined-host residual
MECHANISM: The HBM holds only 2-bit rotated codes, and every token is still attended. A 2-bit residual for each token sits in host DRAM. At each decode step, approximate scores from the 2-bit codes pick the top 256 tokens per KV head, and only those tokens' residuals are fetched. That costs about 10 MB per step for a 70B model at 128k, roughly 0.2 ms over PCIe 5 or less over NVLink-C2C. The closest earlier attempts are Quest and ShadowKV, which approximate or skip non-selected tokens. Here no token is dropped, so multi-turn reuse is safe. The deciding quantity is the softmax mass that falls outside the top-k set.
VALUE: About 4-bit effective fidelity on the tokens that matter, at a 2-bit HBM footprint and read cost.

IDEA 3
NAME: MLA latent trellis quantization
MECHANISM: The 512-dimension MLA latent is Hadamard-rotated and trellis-coded at 2 bits. The decoupled 64-dimension RoPE key stays in FP8, and one FP16 norm is stored per token. That totals about 2.7 bits per value, roughly 6× smaller than the BF16 MLA cache. The kernel decodes the latent before the absorbed up-projection. The closest earlier attempt is Palu, whose own low-rank projection created latent outliers that hurt low-bit quantization. Rotation flattens those outliers without calibration. The deciding quantity is the latent MSE after the absorbed up-projection.
VALUE: Removes about 25% of DeepSeek-V3-class decode cost and fits about 6× more 128k contexts per GPU.