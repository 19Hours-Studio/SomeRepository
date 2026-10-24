# Continuum: a decode-first accelerator for data-center inference

**Note:** No CONTEXT block was attached, so the figures below are approximate public numbers (±30%).

## Target and metric

Continuum targets frontier-scale data-center **inference**: MoE models with 1M-token contexts, including RL rollouts. It is judged on two system-level metrics:
- **Joules per token**
- **Tokens/s per user at a fixed $/token**

It is not judged on peak FLOPS. Decode has an arithmetic intensity near 1–10 FLOP/byte, so peak FLOPS mostly sit idle.

## How the leading designs fail on this metric

- **Rubin-class GPUs** (~288 GB HBM4, ~20 TB/s, ~50 PF FP4): every token re-reads weights and KV cache at roughly 3–4 pJ/bit.
- **Ironwood** (192 GB, ~7.4 TB/s) has the same bottleneck. Its strength is the optical-switched pod.
- **WSE-3** (44 GB SRAM, ~21 PB/s) and **Groq** (~230 MB/chip) avoid the HBM cost. But SRAM bitcells stopped shrinking at N3/N2 (~0.02 µm²), so capacity per dollar is poor and very large models need hundreds of chips or wafers.

## Physical limits Continuum is built around

| Limit | Value |
|---|---|
| Reticle size | ~858 mm² (halves under High-NA) |
| HBM4 bandwidth | ~2 TB/s per stack |
| Off-package electrical I/O | ~5 pJ/bit |
| On-die SRAM access | ~0.1–0.5 pJ/bit |
| FP8 MAC | ~0.1–0.2 pJ |
| Package power | ~1.5–2 kW with liquid cooling |
| CoWoS capacity | Tight supply |

## Architecture

- **Compute:** Modest dense FP8/FP4 tile arrays.
- **Memory:** The novelty is in the memory hierarchy (Ideas 1 and 2).
- **Interconnect:** The novelty is in the interconnect (Idea 3).
- **Packaging:** 2.5D package with 8 HBM4 stacks, using custom logic base dies, and co-packaged optics. Target ~1.2 kW.
- **Programming model:** A compiler with three explicit placement scopes: stack-local attention, codec-resident weights, and broadcast layers. It exposes a JAX/PyTorch front end, so model code does not change.

## What must be true

1. Memory vendors sell HBM4 base dies built on a custom N3 logic process.
2. Trellis-coded weights at ~2.5 bits per weight match FP8 quality on frontier MoE models.
3. Optical splitter loss plus laser power stays below ~1 pJ/bit at 1:16 fan-out.
4. Serving operators accept batch-synchronous scheduling across chips.

If all four hold, I estimate **~5–10× lower joules per token** than Rubin-class GPUs on long-context decode. That figure is an estimate, not a measurement.

=== IDEAS ===
IDEA 1
NAME: Attention Inside HBM Base-Die
MECHANISM: Each HBM4 stack's logic base die stores its share of the KV cache and runs two steps locally: approximate top-k block retrieval, then exact flash-decoding partial attention. Only small partial results (softmax numerators, denominators and max values) leave the stack, not the KV data itself. A retrieval index in the base die is updated as tokens are appended. The die adjusts how many blocks it selects based on the entropy of the attention scores.
VALUE: Million-token decode no longer needs to pull KV bandwidth off the stack, which cuts long-context attention energy by roughly an order of magnitude.

IDEA 2
NAME: Codec-Native Tensor Datapath
MECHANISM: Weights are stored only in a learned trellis/codebook compressed form at about 2–3 bits per weight. A decoder sits directly beside each MAC array and expands the weights in-line, so uncompressed weights are never written to memory. Codebooks are trained per layer and can be swapped at runtime by a small resident manager. The manager switches to finer codes for layers whose activation outliers grow.
VALUE: Each HBM byte delivers about 3× more weights at near-FP8 accuracy, so both capacity and bandwidth effectively triple.

IDEA 3
NAME: Optical Weight-Broadcast Fabric
MECHANISM: A layer's weights are read from memory once and sent through passive photonic splitters to as many as 16 chips at the same time. Each chip holds activations and KV cache for a different set of users, so the chips are token-stationary while the weights stream past. A scheduler aligns layer timing across the group and changes the fan-out to match load.
VALUE: The cost of the HBM weight read is shared across many chips, which breaks the per-chip decode bandwidth limit without needing wafer-scale SRAM.