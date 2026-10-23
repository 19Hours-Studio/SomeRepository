**Obvious first answers.** These are KIVI-style 2-bit, KVQuant non-uniform codebooks, TurboQuant rotation, NVFP4, H2O/SnapKV eviction, KVzip, Palu low-rank and MiniCache/xKV layer merging. **The paradigm they share:** each layer's KV entry is shrunk once, independently, by a fixed lossy map, and attention reads whatever survived. The three ideas below instead:
- exploit statistical dependence *between* stored entries,
- decide precision *per query at read time*, or
- use sequence-level codes.

All three use a fixed Hadamard rotation (no stored metadata) and need no calibration, which sidesteps the open calibration question.

**Bar to beat:** NVFP4, at ≈4.5 bits per value including one FP8 scale per 16 values. That is 3.6× vs FP16 with <1% loss (vendor claim).

**Where the gain applies:**
- **Archetype B (long reasoning):** KV reads are 50% of cost, so the ceiling is 12.5×.
- **Archetype C (multi-turn reuse):** this is a capacity and hit-rate gain.
- **Archetype A (long-document QA):** dominated by prefill, so I claim only capacity gains there.

**Main caveat.** Every quality number below is a predicted target, not a measurement. The falsification tests are what confirm or kill each idea.

=== IDEAS ===

IDEA 1
NAME: Bit-plane on-demand attention precision
MECHANISM: Keys are stored pre-RoPE and rotated, then quantized to 4-bit codes laid out as bit-planes, at 4.5 bits per value in HBM. A FlashAttention tile reads only the top 2 planes plus scales (2.5 bits per value, 6.4× fewer bytes than FP16) to score every token. It then fetches the low planes only for the ≈2% of tokens whose coarse logit could land in the top softmax mass; the 4 sink tokens and a 64-token recent window always use full planes. The closest earlier attempts are Quest and ShadowKV, which drop the tokens they do not select and so lose them on reused or multi-turn queries; here no token is ever dropped, and the tail is still read at 2 bits. The deciding quantity is the softmax mass that falls on coarse-only tokens multiplied by their value error; it must stay ≤1e-3 per head.

VALUE: About 2.6 bits read per value during decode, against NVFP4's 4.5. This should give a 1.5–1.6× decode speedup in reasoning workloads, with quality bounded by NVFP4 (≤1% drop on AIME24 and RULER-64K for R1-Distill-8B). It is falsified if a one-day PyTorch prototype misses NVFP4 accuracy on AIME24.

IDEA 2
NAME: Cross-layer conditional entropy coding
MECHANISM: Values and pre-RoPE keys are rotated and quantized to NVFP4-grade 4-bit codes. Each token's codes at layer l are then coded losslessly with interleaved rANS, using a small count table conditioned on the same channel's code at layer l−1 and at token t−1. Pages decompress into SRAM inside the attention kernel or on transfer from a CPU or SSD tier. The closest earlier attempts are SplitZip and ZipNN, which code only BF16 exponents and reach about 25%; here the target is low-entropy indices that share the residual stream across layers. The deciding quantity is the conditional entropy H(code_l | code_{l−1}, code_{t−1}), which must be ≤2.5 bits.

VALUE: Output is bit-identical to the 4-bit format, at ≈3.0 bits per value including tables and scales, or 5.3× vs FP16. This raises prefix-cache hit rates and the number of resident requests in LMCache-style deployments. GPU rANS throughput of roughly 300 GB/s (DietGPU class) limits its speed advantage in decode-heavy HBM serving. Measuring that entropy on 1k cached sequences from Llama-3-70B and DeepSeek-V3 latents falsifies it in one hour.

IDEA 3
NAME: Calibration-free trellis-coded KV
MECHANISM: Each rotated 256-value token-channel block is coded with a QTIP-style trellis code over a fixed Gaussian code. This is sequence-level vector quantization at 2 bits plus one FP8 scale per 64 values, 2.13 bits per value or 7.5× vs FP16. A lookup-free decode fuses into the attention tile. The closest earlier attempts are KIVI-2bit and VecInfer, whose scalar or small-codebook error collapses long chains of thought; trellis codes cut MSE about 2× over scalar quantization at equal bits.

VALUE: The deciding quantity is attention-logit MSE relative to 4-bit scalar codes, which must be ≤1.2×. If that holds, the target is ≤1% relative drop on AIME24, GSM8K, RULER-128K and NIAH for Qwen3-8B and Llama-3-70B at 7.5×, with ≈10% decode overhead. A 2-hour logit-MSE sweep falsifies it.