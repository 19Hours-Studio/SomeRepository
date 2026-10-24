# Continuum: an inference-first accelerator

**Target and metric.** Continuum is for data-center decode of frontier sparse MoE models with long context (128K to 1M tokens). It is scored on **$/M output tokens at ≥100 tok/s per user, measured at the wall** (J/token included). That is the binding cost today. Training is out of scope.

**Why the incumbents leave room**
- **Rubin-class GPUs and Ironwood.** Decode at large KV sizes is bound by HBM traffic, not FLOPs. HBM costs roughly 3–5 pJ/bit; on-die SRAM costs roughly 0.1 pJ/bit.
- **WSE-3 and Groq.** SRAM-centric designs (Groq ~230 MB per chip; WSE-3 ~44 GB per wafer) fit a 1M-token KV cache for many users only across very many chips or wafers. Their cost per GB of SRAM is about 100× that of HBM.
- **The real limits** are KV bytes per token, reticle size (~858 mm²), CoWoS-class interposer area and yield, ~$30k per N2 wafer, and ~1.5–2 kW per package cooled by liquid.

**Architecture**
- **Compute.** Four N2 compute dies plus eight HBM4 stacks with *custom logic base dies* (HBM4 makes custom base dies possible).
- **Memory.** HBM4 with near-memory logic in the base dies. Weights and KV cache live in separate tiers.
- **Interconnect.** Co-packaged optics.
- **Programming model.** A compiler targeting "token graphs". It schedules weight broadcast windows and per-tile error budgets.
- **Packaging and power.** CoWoS-L class; about 1.8 kW, liquid cooled.

**What must be true for this to work**
1. Codebook KV keeps less than 0.3% perplexity loss on long-context evals. Published product-quantized KV results suggest 4–8× compression is plausible; this is unproven at 1M tokens.
2. Ring resonators hold their wavelength lock within the thermal budget.
3. Escalation rates stay below 5%. Otherwise the 3-bit gain disappears.
4. HBM vendors agree to build custom base-die logic, which is an economic dependency.

If the claims hold, the expected result is about 3–6× lower $/token than Rubin-class GPUs on long-context MoE decode. This is my estimate, not a measurement.

=== IDEAS ===
IDEA 1
NAME: Compressed-domain attention in HBM
MECHANISM: The KV cache is stored as learned product-quantization codes, never as dense values. The HBM base die computes the query-to-codeword dot-product tables once per head. It then scores attention by table lookup and accumulation inside the memory stack, and returns only the top-k scores and a weighted value sum. Codebooks are retrained per layer offline and can be refreshed online when the drift in reconstruction error crosses a threshold.
VALUE: It cuts KV bytes crossing the HBM interface by about 8–20×, so million-token decode stops being memory-bound.

IDEA 2
NAME: Circulating optical weight broadcast
MECHANISM: Expert weights are not replicated per chip. Instead, weight shards circulate on a wavelength-multiplexed co-packaged optical ring. Each chip keeps its users' activations and hot KV stationary in SRAM and computes on weights as they pass, so a single weight read serves every chip in the ring. The scheduler reorders expert broadcast slots each step to match the router's predicted demand.
VALUE: The effective decode batch becomes cluster-wide, so weight-read energy per token falls by roughly the number of chips in the ring.

IDEA 3
NAME: Error-budgeted escalating numerics
MECHANISM: Matmul tiles run at 3-bit, and each tile carries a cheap hardware running bound on its rounding error. A tile whose bound exceeds the compiler-assigned budget for its layer is recomputed at FP8 by deterministic residual correction. The budget per layer is tuned from observed escalation rates and output-sensitivity statistics.
VALUE: It gives near-3-bit throughput and energy with a provable bound on accuracy loss, instead of relying on empirical quantization guesses.