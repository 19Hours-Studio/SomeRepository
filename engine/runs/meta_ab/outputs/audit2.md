**Note:** No CONTEXT block was attached. The figures below are widely reported vendor numbers and should be treated as approximate.

## Target and metric

Continuum targets **data-center inference of frontier MoE LLMs (≈1T parameters) in the decode phase**. The metric is **tokens/s per watt and per dollar at ≥100 tok/s per user**. Training is out of scope, because a single chip optimized for both loses to specialists on each.

## Why decode is the battleground

At batch size B, an FP8 weight byte yields about 2B FLOPs. Ridge points (peak FLOPs ÷ memory bandwidth):

| Chip | Peak | Bandwidth | Ridge (FLOP/B) |
|---|---|---|---|
| Rubin | ~50 PFLOPS FP4 | ~22 TB/s HBM4 | ~2,270 |
| Ironwood | 4.6 PFLOPS FP8 | 7.37 TB/s | ~626 |

Low-batch decode sits far below both ridges, so the binding resource is **bytes moved**, not FLOPs.

**Energy cost of HBM.** At about 3.5 pJ/bit, streaming 22 TB/s costs 22e12 × 8 × 3.5e-12 ≈ **616 W** on memory movement alone.

**Capacity cost of SRAM.** SRAM-centric designs avoid the HBM energy cost but hit capacity limits:
- Holding 1 TB of weights needs ≈23 WSE-3 wafers (44 GB each).
- It needs ≈4,350 Groq LPUs (230 MB each).
- SRAM bitcells barely shrank from N5 to N3 (~0.021 µm²), so this gap won't close.

## Continuum

- **Compute:** about 800 mm² logic tiles, held under the ~858 mm² reticle limit for yield.
- **Memory:** DRAM is hybrid-bonded directly over the logic tiles, with an LUT-based numeric format.
- **Interconnect:** co-packaged optics, at roughly 1–2 pJ/bit versus about 5 pJ/bit for electrical SerDes.
- **Programming model:** a static, compiler-scheduled dataflow graph in the style of Groq, but with DRAM capacity.
- **Packaging and power:** about 1 kW per package, liquid-cooled.

At a target of 0.3 pJ/bit, the same 22 TB/s costs about **53 W** instead of 616 W.

## What must be true

1. **DRAM retention.** Hybrid-bonded DRAM must keep acceptable refresh overhead at junction temperatures of 85–95 °C. Retention degrades with heat, and this is the key thermal risk.
2. **Bonding yield.** Logic and DRAM yield at bond pitches of ≤10 µm must be good enough that known-good-die economics hold.
3. **Codebook quality.** Codebook quantization at about 4 bits per weight must stay within roughly 1% of FP8 quality on frontier models.
4. **Compiler.** Static scheduling must handle MoE routing variance, for example through over-provisioned expert replicas.

If (1) fails, Continuum falls back to HBM4 and is only incrementally better than existing designs.

=== IDEAS ===
IDEA 1
NAME: DRAM Carpet Over Logic
MECHANISM: Each compute tile has its own DRAM stack hybrid-bonded directly above it at a fine pitch, giving every tile a private, very wide memory port. Weights are stored where they are consumed, so data travels microns instead of millimeters. The tile's temperature telemetry adapts DRAM refresh rate per bank.
VALUE: It delivers DRAM capacity at near-SRAM energy per bit, removing the memory-movement power that dominates low-batch decode.

IDEA 2
NAME: Codebook Lookup Matrix Engines
MECHANISM: Weights are stored as roughly 4-bit indices into small learned per-block codebooks. Activations are precombined into lookup tables, so a matrix multiply becomes table reads plus additions instead of multiplications. Codebooks are refit per layer at deployment, trading compression against accuracy.
VALUE: It halves bytes per weight relative to FP8 and replaces most multipliers with adders, cutting both bandwidth and compute energy.

IDEA 3
NAME: Attention Executed Where KV Lives
MECHANISM: Long-context KV caches sit in pooled memory modules that contain their own attention engines. Only queries go in and attention outputs come back, so the cache never crosses the network. Hot sequences migrate between modules based on access frequency.
VALUE: Context length scales with pooled memory capacity instead of accelerator-local memory, without paying interconnect bandwidth for KV traffic.