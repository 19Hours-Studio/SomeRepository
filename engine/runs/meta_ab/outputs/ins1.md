No CONTEXT block came through, so the figures below are approximate public numbers. Treat them as order-of-magnitude.

## Target and metric

**Target:** Data-center inference for frontier models, specifically long-context decode. That is where the money is going and where current designs waste the most energy.

**Metric:** Joules per output token at a fixed interactivity floor (≥100 tok/s/user, 128k context), then $/token.

Training is secondary. A chip that wins decode energy can still train, but not the other way round.

## Why current designs lose

- **Rubin-class GPUs and Ironwood** are HBM-bound during decode. Moving a byte off-package costs about 3–5 pJ, while an FP8 MAC costs about 0.1 pJ, so most of the energy goes to fetching weights and KV, not to compute.
- **WSE-3 (about 44 GB SRAM) and Groq (about 230 MB per chip)** avoid the HBM cost. But SRAM bitcell scaling has largely stalled since N5. Holding a 2T-parameter model plus its KV cache therefore takes wafers or racks of silicon.
- **Packaging:** the reticle limit is about 858 mm², and CoWoS and HBM supply are the real constraints. Any design that needs more HBM stacks than competitors loses on economics.

## Continuum in brief

- **Compute:** logic dies hybrid-bonded directly beneath DRAM.
- **Numerics:** MSB-first bit-plane arithmetic.
- **Interconnect:** optical circuit switching.
- **Programming model:** a layer-pipelined dataflow graph with error budgets stated per operation. Programmers do not choose dtypes.
- **Power:** about 600 W per package, liquid-cooled. The thermal budget is limited by the DRAM retention-temperature ceiling of roughly 85–95 °C.

## What must be true for this to work

1. Hybrid bonding of logic to DRAM yields above about 90% at volume. Memory makers are working toward this for HBM4E and later generations.
2. Thermal limits under the DRAM can be met, which requires backside power delivery and microfluidic cooling.
3. Model quality holds under bounded-error arithmetic and approximate attention, within about 0.5% on long-context evaluations.
4. Optical switches can reconfigure in microseconds or less, with insertion loss low enough for direct-detect links. Google's OCS shows feasibility at millisecond reconfiguration timescales.

=== IDEAS ===
IDEA 1
NAME: Near-Bank Associative Attention
MECHANISM: The KV cache lives in DRAM that is stacked over logic and stored as product-quantized codes, with small comparator arrays at each bank. A query is broadcast to every bank. Each bank scores its keys locally and returns only the top-k candidates plus a residual bound, so the full KV cache never crosses the memory interface. Codebooks are periodically re-fit on chip as the context grows.
VALUE: Long-context decode energy becomes nearly independent of context length, rather than scaling linearly with it.

IDEA 2
NAME: MSB-First Anytime Arithmetic
MECHANISM: Multipliers process operands one bit-plane at a time, starting from the most significant bit, and track a running worst-case bound on the remaining error. Each dot product stops as soon as its bound falls below the error budget the compiler assigned to that tensor. Hardware counters record the average depth reached per layer, and the compiler adjusts budgets from that feedback.
VALUE: Precision is spent only where it changes the output, which saves an estimated 2–4× in energy compared with fixed FP4/FP8 formats.

IDEA 3
NAME: Optically Rewired Weight-Stationary Pipeline
MECHANISM: Each package keeps one model slice permanently resident in its stacked DRAM. Only activations move between packages, over co-packaged optics routed through microsecond-scale optical circuit switches. The switch fabric is reconfigured per batch phase, such as prefill versus decode or between mixture-of-experts routing patterns, to match the dataflow graph. Expert placement migrates according to observed routing statistics.
VALUE: Weights are never refetched, and the network topology tracks the workload instead of forcing the workload to fit a fixed topology.