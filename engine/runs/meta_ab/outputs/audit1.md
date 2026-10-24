**Note:** No CONTEXT block came with the request. The figures below are widely reported vendor numbers, rounded and marked "≈". Check them against your own sources.

## Target and metric

- **Workload:** data-center inference for frontier-scale mixture-of-experts (MoE) models with long context. Training is secondary.
- **Metric:** tokens/s per watt and $/token, measured at a fixed per-user latency target (for example, ≥100 tok/s per stream).

## Why the incumbents fall short

- **Decode is limited by memory bandwidth.** A 1T-parameter model at 4 bits is 500 GB of weights. At Rubin's claimed ≈22 TB/s HBM4, one batch-1 pass takes 500/22,000 ≈ 23 ms. That caps a stream at ≈44 tok/s before batching.
- **HBM chips (Rubin, Ironwood) pay for every byte moved.** Ironwood offers ≈7.4 TB/s and ≈192 GB.
- **SRAM chips are fast but small.**
  - Cerebras WSE-3 has ≈44 GB of SRAM at ≈21 PB/s. A 500 GB model needs about 12 wafers.
  - Groq LPU has ≈230 MB per chip. The same model needs about 2,200 chips.
- **Physical limits:**
  - A single chip cannot exceed the ≈858 mm² reticle.
  - Off-package traffic costs several pJ/bit, versus well under 1 pJ/bit on-die.
  - HBM supply and advanced packaging (CoWoS-class) capacity limit how many units can ship.

## Continuum architecture

- **Compute:** chiplets of codebook lookup-accumulate tiles instead of FP multiply-accumulate arrays.
- **Memory:**
  - KV cache sits in DRAM stacks that contain their own attention logic.
  - Weights sit in compressed codebook form on HBM, staged through SRAM.
- **Interconnect:** co-packaged silicon-photonic switches. The network topology is rewired for each MoE routing step.
- **Numerics:**
  - Weights are 2–3-bit indices into learned per-block codebooks.
  - Accumulation is FP16.
  - KV cache uses compressed FP8.
- **Programming model:** a compiler takes graphs in the JAX/PyTorch style. It emits three things: codebooks, attention-offload kernels, and topology schedules.
- **Packaging and power:**
  - 2.5D interposer with backside power delivery.
  - Liquid cooling, budgeted at roughly 1.5–2 kW per package.

## What must be true for it to work

1. Codebook quantization at 2–3 bits must stay within about 1% of FP8 quality on frontier MoE models.
2. Attention logic must be added to DRAM dies without unacceptable yield or thermal penalties.
3. Photonic switches must reconfigure in under about 10 µs, at a cost competitive with copper.
4. A software stack must make all of this invisible to model authors. This is historically the factor that decides whether new accelerators succeed.

If any one of these fails, Continuum falls back to a conventional HBM accelerator design.

=== IDEAS ===
IDEA 1
NAME: Attention Inside the Memory
MECHANISM: Each DRAM stack holding the KV cache gets a logic layer that computes query-key scores, softmax and the value-weighted sum next to the stored keys and values. Only query vectors go into the stack and only attention outputs come back. Cache pages are compressed and evicted in place according to accumulated attention scores.
VALUE: KV-cache traffic stops crossing the memory bus, so long-context decode is no longer limited by memory bandwidth.

IDEA 2
NAME: Codebook-Native Lookup Compute
MECHANISM: Weights are stored as 2–3-bit indices into small learned codebooks, one per block. Tiles precompute products of activations with codebook entries and then accumulate by table lookup instead of multiplying. Codebooks are periodically re-fit to the activation statistics seen in deployment.
VALUE: Weights take roughly half the bytes of 4-bit formats, which roughly doubles bandwidth-limited decode throughput per watt.

IDEA 3
NAME: Routing-Shaped Photonic Fabric
MECHANISM: Co-packaged silicon-photonic switches rewire the connections between chips at microsecond timescales. Each rewiring follows the expert-routing histogram that the MoE gate predicts for the next batch. Experts that are used heavily get direct optical links, and rarely used experts share links over multiple hops.
VALUE: The physical network matches the shifting traffic pattern of MoE expert routing, which reduces all-to-all communication bottlenecks at cluster scale.