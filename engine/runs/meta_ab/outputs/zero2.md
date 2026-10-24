# Continuum: an AI accelerator for frontier LLM decode

**Note:** The CONTEXT block was not attached. The figures below are my own recollection of reported values and may conflict with your list.

## What "best" means here

- **Workload:** Frontier-scale LLM inference, specifically autoregressive decode with long context. This is where the money and the bottleneck are.
- **Metric:** Joules per token and dollars per million tokens, measured at a fixed latency target of ≥100 tokens/s per user.
- **Out of scope:** Training. Continuum is deliberately not the best training chip.

## Why the incumbents lose on this metric

Decode is limited by memory bandwidth, not FLOPs. Every weight byte is moved once per token batch.

| Design | Strength | Limit for this metric |
|---|---|---|
| Rubin (HBM4, ~20 TB/s reported) | Bandwidth | Pays ~3–5 pJ/bit for every weight fetch |
| Ironwood (~7.4 TB/s, 192 GB) | Capacity | Pays the same per-bit cost |
| WSE-3 (44 GB SRAM) / Groq (~230 MB/chip) | ~0.1 pJ/bit SRAM | Capacity is costly; SRAM bitcells stopped shrinking around N3 (~0.02 µm²), so capacity costs wafers |

Continuum attacks the cost of the bytes rather than adding more of them.

## Architecture

**Compute**
- Reticle-limited dies of ~800 mm² on N2.
- Each die carries 3× more MAC area than its power budget can light at once (see idea 2).

**Memory**
- Weights are stored as generator seeds plus small corrections, and are expanded on-die (see idea 1).
- HBM holds only the KV cache.
- SRAM holds the seeds and the hot KV entries.

**Numerics**
- Precision is set per tile at runtime against an error budget (see idea 3).

**Interconnect**
- Pipeline stages are linked by co-packaged optics.
- Weight traffic drops out, so links carry only activations and KV state, which is far less than weight traffic.

**Programming model**
- The compiler takes a model plus an accuracy SLA, not a fixed dtype.
- It emits seeds, a heat-rotation schedule and an error budget.

**Packaging and power**
- CoWoS-L, which is the throughput bottleneck since TSMC capacity is constrained.
- Direct liquid cooling at roughly 1–1.5 W/mm² steady state.

## What must be true for this to work

- Seed compression must reach about 1.5 effective bits per weight at frontier quality with fine-tuning. Published SeedLM-class results are at about 3–4 bits.
- The thermal time constants of silicon plus cold plate (~ms) must allow 3× local sprinting without electromigration failure.
- Customers must accept accuracy SLAs instead of bit-exact outputs.

=== IDEAS ===
IDEA 1
NAME: Procedural Weights From Seeds
MECHANISM: Each weight block is stored as a pseudo-random generator seed plus a few low-precision projection coefficients, found offline by search and fine-tuning. On-die hardware generators regenerate the full block next to the MAC arrays each time it is needed, at femtojoules per bit. HBM and SRAM therefore hold kilobytes where they would otherwise hold megabytes. The compiler re-searches seeds whenever the model is updated.
VALUE: It turns the memory-bandwidth wall of LLM decode into cheap local compute, cutting energy per token by several times.

IDEA 2
NAME: Heat-Rotating Oversubscribed Silicon
MECHANISM: The die has about three times more compute tiles than its steady-state power budget can run. A scheduler runs a subset of tiles at high voltage and frequency and moves work to cold regions before local temperature crosses its limit. On-die thermal sensors close the control loop every millisecond. Pipeline stages follow the moving hot spot.
VALUE: It delivers sustained throughput above the cooling limit for a fixed area by spending cheap silicon instead of scarce power and cooling capacity.

IDEA 3
NAME: Error-Budgeted Adaptive Precision Hardware
MECHANISM: Every tensor tile carries a precision tag and a running error estimate, computed by sparse high-precision shadow MACs that sample the low-precision results. A controller lowers a tile's precision, from 8-bit down to 2-bit logarithmic, until the accumulated error approaches an accuracy budget set per request. When drift is detected, it raises precision again.
VALUE: It lets each token use the minimum arithmetic needed for a guaranteed output quality, instead of a worst-case fixed datatype.