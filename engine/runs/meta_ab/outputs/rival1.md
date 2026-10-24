# Continuum: an inference-first, memory-centred accelerator

**Note:** No CONTEXT block came with the question, so the figures below are approximate public numbers and should be checked.

## Target and metric

Continuum targets **data-centre frontier inference**: long-context, agentic decode with MoE models. Training is a secondary goal.

"Best" means **joules per output token**, and **TCO dollars per million tokens**, measured at a fixed interactivity of ≥100 tokens/s per user and 128K-token context.

## Why the incumbents fall short on this metric

- **GPUs (Rubin, ~288 GB HBM4)** and **TPUs (Ironwood, ~192 GB HBM, ~7.4 TB/s)** are limited by HBM bandwidth during decode. They move the KV cache and weights across a PHY at roughly 3–5 pJ/bit.
- **Cerebras WSE-3 (~44 GB SRAM)** and **Groq (~230 MB SRAM per chip)** get bandwidth from SRAM. But SRAM density has nearly stopped improving since N3, which forces them to use hundreds of chips or a whole wafer for each model.

## Architecture

- **Compute:** Two N2 logic dies hold systolic tiles for dense FFN and MoE work.
- **Memory hierarchy:** 16 HBM4E stacks, each with a custom logic base die that performs attention near the memory (see Idea 1).
- **Interconnect:** Co-packaged optics carry the scale-up domain across 576 chips, with wavelength multicast for weights.
- **Numerics:**
  - FP4 and FP6 computation.
  - FP8 for the KV cache.
  - FP32 accumulation.
  - Bounded-error correction in hardware.
- **Programming model:** A JAX/PyTorch graph compiles to a static, Groq-style dataflow schedule. MoE routing and KV paging are handled by a runtime.
- **Packaging and power:**
  - CoWoS-L-class interposer at about 4 reticles, which is close to the current yield and substrate-warpage limits.
  - About 1.8 kW per package with direct liquid cooling.
  - 48 V delivered to the package, then backside power delivery.

## Physical, economic and manufacturing limits

- DRAM off-stack I/O energy is 3–5 pJ/bit, much higher than on-die access.
- SRAM density is roughly flat from N3 to N2.
- CoWoS and HBM supply are constrained.
- Rack power is limited to about 200 kW or less.
- Optical engines must reach under 5 pJ/bit with field reliability at least as good as copper.

## What must be true for this to work

1. HBM vendors must accept custom base dies, which the HBM4 roadmap suggests they will.
2. Top-k sparse attention must preserve quality at 128K+ context.
3. Thermal limits must allow logic in the HBM base die, within about 5 W per stack.
4. Error-bounded FP4 must hold accuracy within 0.5% of FP8.

If all four hold, joules per token should fall about 3–5× relative to Rubin. That estimate is reasoned, not measured.

=== IDEAS ===
IDEA 1
NAME: Attention Inside the Memory Stack
MECHANISM: Logic on the base die of each HBM stack keeps a learned locality-sensitive hash index over the KV cache stored in that stack. For every query, it scores keys locally and returns only the top-k keys and values, or a partial softmax result, to the compute die. The index is updated as tokens are appended and is retuned per model from attention statistics.
VALUE: Long-context decode no longer depends on HBM-to-compute bandwidth, which could cut attention data movement by more than 10×.

IDEA 2
NAME: Photonic Multicast Weight Streaming
MECHANISM: Each weight shard is read from memory once and broadcast optically on separate wavelengths to every chip in a replica group at the same time. Each chip consumes the weights in lockstep against its own batch of users. A scheduler adjusts group size to match live MoE expert popularity.
VALUE: Weight-read energy is shared across many chips, so large batches no longer require each chip to hold its own copy of the weights.

IDEA 3
NAME: Speculative Precision with Lazy Correction
MECHANISM: Every matrix multiply runs first in FP4, and hardware computes a cheap error bound for each output row from the operands' exponent statistics. Only rows whose bound exceeds a per-layer budget are recomputed in FP8 using a stored residual. The budgets are calibrated online from the drift in downstream logits.
VALUE: Most operations run at FP4 throughput and energy while accuracy stays close to FP8.