Claims below are design predictions anchored on cited results, not measurements. Every design is **calibration-free**: it uses fixed Hadamard rotations and fixed Gaussian codebooks. That sidesteps the question of whether one-time calibration counts as retraining.

**Shared accounting**
- The first 4 sink tokens and a 128-token recent window stay in FP8. At 32k tokens this adds less than 0.03 bits per value.
- Each 128-dim post-RoPE key and value vector is multiplied by a fixed randomized Hadamard matrix. This spreads outlier channels across all dimensions.
- The query is rotated once per step, since q·k equals (Hq)·(Hk). The attention output is un-rotated once per head. Neither cost scales with context length.
- Encoding runs in the prefill epilogue, adding roughly 2% to prefill time. Prefill is mostly attention and linear layers, so the cache format barely changes prefill speed.
- Scoring, by usage pattern:
  - Reasoning chains of thought: KV reads are about 50% of decode cost.
  - Long-document QA: the gain is capacity and batch size.
  - Prefix reuse: the gain is cache density and hit rate.

**Falsifying experiment (a few GPU-hours)**
- Model: R1-Distill-Llama-8B.
- Benchmarks: AIME24, MATH-500 at 32k tokens, and multi-query RULER-128k, each against BF16.
- The design fails if the drop is more than 1 point, or if fused decode is slower than FP8 at batch 10.
- For MLA models: compress the 512-dim latent and keep the decoupled 64-dim RoPE part in FP8. This is untested.

=== IDEAS ===
IDEA 1
NAME: Rotated 3-bit fixed-codebook cache
MECHANISM: Keys and values are rotated with a fixed Hadamard matrix after RoPE. Each value is then coded with a fixed 3-bit Lloyd-Max Gaussian codebook, plus one FP8 scale per 64 values, for 3.125 bits per value or about 5.1× versus FP16. Sinks and the recent window stay in FP8, and a FlashAttention kernel dequantizes through an 8-entry lookup table in registers. The closest earlier attempt is TurboQuant, whose QJL residual added attention noise; this design drops QJL and spends that bit budget on the code itself. Anchors are KVQuant (<0.1 perplexity loss at 3 bits) and TurboQuant (neutral at 3.5 bits). The deciding quantity is the AIME accuracy gap at 32k tokens, which must be ≤1 point.
VALUE: A safe ~5× cache, against NVFP4's ~4×, with a predicted ≤1% drop on RULER and LongBench and no calibration.

IDEA 2
NAME: Progressive residual, score-guided refinement
MECHANISM: Each 16-token page stores a 2-bit rotated base code in HBM, plus a 2-bit residual in cold HBM or CPU memory, so no token is ever evicted. At decode, attention scores are computed from the base keys. For the pages holding the top ~5% of softmax mass, the residual is fetched and those pages are recomputed at 4 bits. The closest earlier attempts are KIVI-2bit, which loses about 13 AIME points because errors land on high-attention tokens, and Quest, which keeps full precision. Here only the high-attention tokens are refined. Hot storage is about 2.25 bits, roughly 7× versus FP16. The deciding quantity is the true softmax mass captured by the 2-bit top-k, which must be ≥0.99.
VALUE: About 7× HBM reduction that stays query-agnostic under multi-turn reuse and long chains of thought, cutting decode KV reads roughly 3.5× versus FP8.

IDEA 3
NAME: E8 lattice 2-bit KV
MECHANISM: Each group of 8 rotated values is coded as one 16-bit E8P lattice codeword, a fixed QuIP#-style codebook needing no calibration. One FP16 scale is stored per 128 values, giving about 2.13 bits per value, or 7.5× versus FP16. The kernel decodes from a 1 KB shared-memory table using sign flips. The closest earlier attempts are 2-bit scalar schemes such as KIVI and MILLION, which break on long chains of thought. E8's granular and shaping gain lowers distortion by about 0.2 bits' worth compared with scalar 2-bit codes. The deciding quantity is the key mean-squared error relative to scalar 3-bit codes, which must be ≤1.3×.
VALUE: If the AIME gap stays ≤2 points, it gives a near-8× drop-in cache that roughly doubles reasoning-serving batch size over NVFP4.