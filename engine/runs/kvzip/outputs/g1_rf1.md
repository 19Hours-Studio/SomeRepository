**Scope.** This targets Archetype B, reasoning decode, where KV reads are about 50% of cost. That is the only archetype where a storage format can deliver a several-fold gain. The bar to beat is NVFP4: 4 bits plus an FP8 scale per 16 values, which is 4.5 bits per value, about 3.6× vs FP16, at under 1% loss.

**Working hypothesis.** Sub-3-bit failures in long chains of thought are concentrated. They happen when a query attends *sharply* to a few earlier tokens, such as intermediate results or variable bindings. There, the key error ‖q‖·‖e_k‖ is comparable to the gap between the top attention logit and the runner-up, so the argmax flips. Diffuse attention averages the error away. That gap can be measured online without calibration.

**Accounting** (per value, 32k context, head dim 128):
- 2-bit codes: 2 bits
- FP8 scale per 32 values: 0.25 bits
- FP16 sinks and a 128-token recent window: about 0.06 bits
- Total: about 2.3 bits, or 7× vs FP16 and 1.9× vs NVFP4

**Targets, not measurements.** Within 1% relative on AIME24, MATH500, RULER-64k and LongBench, with perplexity +0.05. Models: R1-Distill-Llama-8B and Qwen3-8B.

**Runtime.** Dequantization fused into FlashDecoding split-K adds an estimated 5–10% to kernel time. Prefill is unchanged.

**Falsifier (one GPU-day).** Run R1-Distill-8B on AIME24 at 32k tokens with five configurations: FP16, NVFP4, plain rotated 2-bit, and each design below. Log every top-1 attention flip. The hypothesis dies if flips are not concentrated in under 5% of query–key pairs, or if a design is not within 1 point of NVFP4.

=== IDEAS ===
IDEA 1
NAME: Margin-flagged key residual promotion
MECHANISM: Each head is rotated with a fixed Hadamard transform, which needs no calibration. Keys are stored at 2 bits pre-RoPE, values at 2 bits per token, and a 2-bit residual for every page is kept in host memory. During decode, the kernel flags any page whose quantized logit lies within ‖q‖·‖e‖max of the top logit. Only flagged pages fetch their residual over PCIe, so they are read at 4 bits. The closest earlier attempt is Kitty's dynamic precision boost, which uses a static importance heuristic and still trails FP16 by 3–4 AIME points. This design promotes exactly the pairs whose argmax can flip. The deciding quantity is the flagged-page fraction, which must stay under about 5% to fit PCIe bandwidth.
VALUE: About 2.3 bits per value in HBM (7× vs FP16) with 4-bit fidelity where reasoning needs it, so batch size roughly doubles over NVFP4.

IDEA 2
NAME: Entropy-gated decision-step recompute
MECHANISM: Decode runs on a 2.3-bit rotated cache. A full FP8 copy is kept on host or SSD, as LMCache already does. When next-token entropy exceeds a threshold τ, the step is a decision point. The model then refetches FP8 pages for the top-attention pages identified in the quantized pass, recomputes that step, and samples from the corrected distribution. The closest earlier attempt is speculative-decoding verification, which rechecks every token at full cost. This design rechecks only uncertain steps, and only on pages that carry attention mass. The deciding quantity is the fraction of steps above τ, which must be under about 10% for the overhead to stay below 15%.
VALUE: It bounds where a 7× cache can change a reasoning chain's tokens, without any offline calibration.

IDEA 3
NAME: Per-request online KLT bit-allocation
MECHANISM: During prefill, the system accumulates each head's pre-RoPE key and value covariance. It stores one 128×128 FP16 basis per head per layer, which is under 0.01 bits per value at 32k. Bits are then allocated by reverse water-filling, about 2.5 on average, and RoPE is applied after dequantization inside the kernel. The closest earlier attempt is Palu, whose offline SVD truncation creates latent outliers and loses accuracy beyond 30% rank reduction. This design truncates nothing and needs no calibration data. The deciding quantity is the eigenvalue arithmetic-to-geometric-mean ratio, which must be at least 4 to save at least 1 bit. That ratio is likely too small on MLA latents.
VALUE: For GQA models it is a calibration-free path to 2.5 bits per value (6.4×) whose quality follows rate-distortion theory rather than heuristics.