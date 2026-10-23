**Target choice.** Archetype B (long chain-of-thought decode) is the right target. Decode KV reads are about 50% of cost there, and the ceiling is 12.5×. In Archetype A a KV format mainly buys batch capacity. All three designs below need no calibration data. The rotations are random Hadamard transforms with a fixed seed. The sink tokens (first 4) and the last 256 tokens stay in FP8.

**Status of the numbers.** The quality figures are projections, not measurements, and each design comes with a falsification test. The bar to beat is NVFP4: about 4.5 bits per value, 3.6× vs FP16, under 1% loss (a vendor claim).

**Runtime.** All three designs fuse into FlashDecoding-style split-K kernels: unpack, then an FP16 MMA (matrix multiply).
- Dequantization costs about 5–10% of decode kernel time.
- Prefill is unchanged. Quantization runs at cache write.
- The expected net decode throughput gain at 32k is 1.5–2×, mostly from larger batches.

**Shared checks.**
- **MLA:** quantize the latent and keep the decoupled RoPE part in FP8. This is untested.
- **Multi-turn reuse:** no design drops tokens, so reuse is safe.

**Falsification.** Run AIME24 with R1-Distill-8B at 32k on three seeds. A drop of more than 2 points against FP16 kills a design.

=== IDEAS ===
IDEA 1
NAME: Asymmetric dithered key-value codes
MECHANISM: Keys are rotated before RoPE and stored at 3 bits per channel group, plus one FP16 scale per 128 values, which is 3.125 bits. Values are stored at 2 bits per token group with dither subtracted from a shared seed, so the dither needs no stored metadata. That is 2.125 bits, for an average of about 2.65 bits, or 6.0× vs FP16. The reasoning is that score error is exponentiated, while value error averages out over the attended tokens. The closest earlier attempt is KIVI K2V2, which lost 13 points on AIME. Its 2-bit keys broke sharp attention and its error was deterministic and biased; this design keeps keys at 3 bits and makes value error unbiased. The deciding quantity is the effective number of attended tokens in retrieval heads. If it is below about 4, the value noise does not average out.
VALUE: 6× KV capacity with projected loss of ≤1% on RULER-64k and GSM8K and ≤2 points on AIME, and no calibration.

IDEA 2
NAME: Bound-driven progressive bit-plane reads
MECHANISM: Rotated keys and values are stored as 6-bit codes split into bit-planes. The top 2 planes plus scales, about 2.2 bits, stay in HBM, which is 7.3×. The lower 4 planes go to CPU memory. On each decode step the kernel computes an interval for every token's score from the coarse planes. It fetches finer planes only for tokens whose upper bound could carry more than ε=10⁻³ of the attention mass, so the error is provably bounded. The closest earlier attempts are Quest and ShadowKV, which use approximate page-level selection and skip tokens. This design never skips a token; it refines precision. The deciding quantity is the fraction of tokens refined per step. It must stay below about 2% at 128k to fit in PCIe bandwidth.
VALUE: 7× HBM savings with a guaranteed attention-error bound, which makes it safe for chains of thought and reuse.

IDEA 3
NAME: Entropy-measured per-head bit allocation
MECHANISM: During prefill, compute each KV head's attention entropy over the prompt's own queries. Assign bit widths from that: broad heads get K2V1, middle heads K3V2, and sharp retrieval heads K4V4. Every token is kept, and the bits average about 2.1 including scales, or 7.5×. The closest earlier attempts are RazorAttention and DuoAttention. They evicted tokens in non-retrieval heads and saved only 1.67× on GQA. This design only lowers precision, which works on already-shared GQA heads and keeps multi-turn reuse safe. The deciding quantity is how stable head entropy rankings are across prompts and decode phases, measured by a Spearman rank correlation of at least 0.9.
VALUE: About 7.5× compression without calibration data, adapting per prompt to any GQA model.