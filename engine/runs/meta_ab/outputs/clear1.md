**Note:** the CONTEXT block was not attached. The figures below are publicly reported vendor numbers from memory, so treat them as approximate.

## Scope and metric

**Target:** data-center inference of frontier MoE LLMs, which is decode-heavy and runs on contexts of 128k tokens or more. Training is a secondary goal.

**Metric:** tokens/s per watt and $ per million tokens, both measured at a fixed interactivity of at least 200 tok/s per user.

Decode is limited by memory traffic, not FLOPs, so "best" here means the fewest joules per byte moved per token.

## Baselines and limits

- **Nvidia Rubin:** about 288 GB of HBM4 at about 22 TB/s. HBM costs roughly 3–4 pJ/bit, while local SRAM costs about 0.1 pJ/bit.
- **Google Ironwood:** 192 GB of HBM3e at 7.4 TB/s, about 4.6 PFLOPS FP8, in pods of 9,216 chips.
- **Groq LPU:** 230 MB of SRAM per chip. Holding the 0.5 TB of weights for a 1T-parameter model at FP4 would take about 2,200 chips.
- **Cerebras WSE-3:** 44 GB of SRAM per wafer, so the same weights need about 12 wafers.
- **Hard limits:**
  - The reticle is about 858 mm², and High-NA lithography halves it.
  - SRAM density has stalled at about 38 Mb/mm² on N2.
  - Attention traffic for the KV cache grows linearly with context length.

## Continuum

### Compute
Bit-plane MAC arrays sit under monolithic BEOL non-volatile weight storage.

### Memory
There are three tiers:
- Resident weights in BEOL storage.
- An HBM4 tier that holds only the KV cache.
- A search array that holds attention keys.

### Interconnect
Co-packaged optics on the package. Only activations move between chips; weights never do.

### Numerics
FP4/FP8 at the interface, with MSB-first internal arithmetic that can stop early.

### Programming model
A compiler built for dataflow. It pins every expert to fixed tiles and emits each layer's error budget.

### Packaging and power
Liquid cooling at about 1.5 kW per package. Weights are non-volatile, so idle tiles can be power-gated with no reload cost.

## What must be true

1. **BEOL non-volatile memory density:** at least about 1 Gb/mm² across stacked layers, which is about 26× the density of N2 SRAM. It must also read at no more than about 0.2 pJ/bit and endure about 10⁴ rewrites, which is enough for model updates.
2. **Analog key search:** it must reach at least 95% top-k recall against exact attention, with the shortlist then rescored digitally.
3. **Early termination:** it must cut average bit-planes by at least 40% with no measurable loss of accuracy.
4. **Packaging yield:** hybrid bonding and BEOL thermal budgets (below about 400 °C) must stay compatible with leading-edge logic.

If any of these fails, Continuum falls back to roughly Rubin-class efficiency.

=== IDEAS ===
IDEA 1
NAME: BEOL Non-Volatile Weight Fabric
MECHANISM: Several layers of ReRAM/FeFET crossbar are built monolithically in the back-end metal stack directly above the MAC arrays. They store model weights permanently, so a weight travels only micrometres from where it is stored to where it is computed. Weights are rewritten only when the model is updated, and idle tiles are power-gated with no reload cost.
VALUE: Frontier-model weights stay resident on the compute at near-SRAM energy, using about 5 reticles instead of roughly 2,200 SRAM chips.

IDEA 2
NAME: In-Memory Attention Key Search
MECHANISM: Attention keys are stored as 4-bit values in a ferroelectric content-addressable array. The array computes every query–key similarity in analog form in place and returns only the indices of the top-k matches. Only the matching values are then fetched from HBM and rescored exactly in digital logic, and k adapts per head to how sharp its attention scores are.
VALUE: Attention traffic for each decoded token becomes nearly independent of context length, so million-token decode stops being limited by memory bandwidth.

IDEA 3
NAME: Early-Terminating MSB-First Arithmetic
MECHANISM: Matrix multiplies process bit-planes starting from the most significant bit and keep a running interval bound on each output. Each output stops computing once its downstream result is mathematically settled, such as the argmax, the router's expert choice, or a saturated activation. The compiler sets a per-layer error budget that controls how early outputs may stop.
VALUE: Average compute and operand traffic fall in proportion to how certain the model is, with a certified error bound instead of blanket quantization.