=== TRIAGE ===

IDEA 1 | I 6 | P 4 | DECIDES: per-head eigenvalue AM/GM ratio of pre-RoPE K/V (≥4 needed to save ≥1 bit) | Valid rate-distortion argument, but 2.5-bit scalar codes sit in the range where TurboQuant and KIVI lost reasoning accuracy; the gain over a fixed Hadamard rotation is likely small.

IDEA 2 | I 7 | P 3 | DECIDES: attention-logit MSE vs 4-bit scalar (≤1.2×) | About 2 dB of trellis gain makes 2.13 bits act like roughly 2.5-bit scalar, still below the ~3-bit reasoning floor; per-token Viterbi encoding during decode adds cost.

IDEA 3 | I 6 | P 4 | DECIDES: effective attended-token count in retrieval heads (≥4) | Asymmetric K3/V2 is sound, but TurboQuant's 3-bit keys already lost GSM8K points; dither removes bias but adds variance.

IDEA 4 | I 2 | P 4 | DECIDES: latent MSE after absorbed up-projection | Archetype D has NO ROOM; latents are already compressed and their AM/GM headroom is small.

IDEA 5 | I 6 | P 3 | DECIDES: Spearman ρ of head-entropy rank across prompts and decode phases (≥0.9) | V1 on "broad" heads is risky; per-prompt entropy measured at prefill may not hold during long CoT.

IDEA 6 | I 7 | P 2 | DECIDES: logit error / per-head logit spread at 1.875 bits | Recovering 2 of TurboQuant's 3 dB still leaves it below the 3-bit point that failed GSM8K.

IDEA 7 | I 7 | P 6 | DECIDES: attention mass in top-2% pages on long CoT (≥99%) | Nested 2+2 planes are clean and reads fall to ~2.2 bits, which targets Archetype B's main term. HBM capacity stays ~4.3 bits unless the planes are offloaded.

IDEA 8 | I 6 | P 3 | DECIDES: PCIe bytes per step × batch | 10 MB per request per step becomes ~0.6 GB at batch 64, with 80 serialized per-layer fetches on the critical path.

IDEA 9 | I 7 | P 5 | DECIDES: ΔAIME24 at 32k on R1-Distill-7B (≤2 pts) | Proven E8P decode, spends bits on keys, handles sinks and window; cheapest decisive test. Close to TurboQuant-3-bit risk.

IDEA 10 | I 3 | P 6 | DECIDES: entropy of rotated 5-bit codes (≤3.5 bits) | ECSQ gain is real, but it only addresses the tier storage term (~1.00×) in TIGHT Archetype C.

IDEA 11 | I 7 | P 6 | DECIDES: coarse-only softmax mass × value error (≤1e-3 per head) | Same strength as 7, with a fidelity ceiling at NVFP4; token-level gather inside tiles is harder than page-level.

IDEA 12 | I 5 | P 3 | DECIDES: fraction of steps with entropy >τ (<10%) | Errors compound on low-entropy steps it never checks; host refetch at batch scale is expensive.

IDEA 13 | I 7 | P 2 | DECIDES: refined-token fraction at 128k (<2%) | 2% of 128k × 80 layers is ~200 MB per request per step over PCIe, so it cannot scale.

IDEA 14 | I 4 | P 3 | DECIDES: H(code_l \| code_{l−1}, code_{t−1}) ≤2.5 bits | Per-layer W_k and W_v make cross-layer code correlation weak. Lossless coding helps mostly the tier, not decode.

IDEA 15 | I 6 | P 3 | DECIDES: flagged-page fraction (<5%) | The ‖q‖·‖e‖max margin is loose and guards only the argmax, not softmax mass. It hits the same PCIe batch limit as 8.