# Continuum

**Note:** the CONTEXT block wasn't included. The figures below are approximate public numbers and are marked "~".

## Target and metric

Continuum targets **data-center inference for frontier sparse (MoE) models with long context**. Training is excluded on purpose, because decode is where money and energy now go. Two metrics count:

- **Joules per token** at ≥300 tokens/s per user, on a ~2T-parameter MoE with 1M-token context.
- **$ per token** at that same latency.

## Why the incumbents lose on this metric

- **Rubin class** (~288 GB HBM4, ~20 TB/s): decode is bound by weight and KV-cache bandwidth. HBM costs about 3–5 pJ/bit, so most energy goes to moving bytes, not to math.
- **Ironwood** (~7.4 TB/s HBM, 9,216-chip pods): same bottleneck, plus all-to-all expert traffic across the torus.
- **WSE-3** (~44 GB SRAM) and **Groq LPU** (~230 MB SRAM per chip): very fast, but SRAM density has stalled since N5 (bitcell ~0.021 µm²). Holding 2T parameters takes racks of silicon, so $ per token blows up.

## Architecture

- **Compute and memory:** weights live in stacked non-volatile compute-in-memory tiers. Activations live in SRAM, and the KV cache lives in logic-augmented DRAM.
- **Interconnect:** co-packaged optics. Tokens move between chips; weights never do.
- **Numerics:** 4-bit microscaled weights computed in place, a digital residual-correction pass, and FP8 accumulation.
- **Programming model:** the compiler places experts the way a database places shards, then emits a static token-routing schedule. Users write PyTorch-level graphs.
- **Packaging and power:** 3D hybrid bonding at ~9 µm pitch. Target is ~600 W per package with liquid cooling, versus 1.8 kW or more for the incumbents.

## What must be true for this to work

1. FeFET or RRAM tiers hold 4-bit levels across 85 °C drift, with on-chip recalibration costing under 2% of throughput.
2. Hybrid-bond yield on a 4–8 tier stack exceeds 90%.
3. Approximate top-k attention loses under 0.5% on long-context benchmarks.
4. Optical links reach ≤1 pJ/bit with fast enough circuit reconfiguration.
5. Model churn is slow enough, roughly a weight rewrite per month, that non-volatile endurance (~10⁶ cycles) is irrelevant.

If (1) fails, Continuum falls back to an HBM machine with good routing, which is only incrementally better.

=== IDEAS ===
IDEA 1
NAME: Non-volatile weight-stationary compute stacks
MECHANISM: Model weights are written once into 3D-stacked FeFET compute-in-memory tiers that are hybrid-bonded over logic. Matrix-vector products happen inside the storage array, and a digital pass corrects analog error using stored residuals. Periodic on-die recalibration tracks drift, and new models are loaded by rewriting the arrays in minutes.
VALUE: It removes per-token weight movement, the dominant energy cost of decode, cutting joules per token by an estimated 5–10× versus HBM-fed designs.

IDEA 2
NAME: Associative in-DRAM attention retrieval
MECHANISM: Each stacked DRAM bank stores KV-cache keys alongside locality-sensitive hash signatures and has logic for parallel signature matching. A query is broadcast, banks return only the top-k candidate keys and values, and exact attention is computed on that small set. Hash functions are retuned per layer from observed attention statistics.
VALUE: It makes million-token decode cost scale with the number of retrieved keys instead of context length.

IDEA 3
NAME: Wavelength-addressed expert routing fabric
MECHANISM: Each MoE expert is pinned permanently to one chiplet, and tokens rather than weights travel between chips. The router's choice of expert maps directly onto an optical wavelength channel on co-packaged photonics. A compiler-generated schedule, rebalanced from measured expert popularity, replicates hot experts and reassigns wavelengths between batches.
VALUE: It turns MoE all-to-all from a congestion-bound bottleneck into near-constant-latency, low-pJ/bit point-to-point delivery at rack scale.