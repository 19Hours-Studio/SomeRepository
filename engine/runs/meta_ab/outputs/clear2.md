# Continuum: an inference accelerator for frontier MoE and long-context serving

No CONTEXT block came with the question, so the figures below are widely reported vendor or press numbers, marked "reported".

**Target and metrics.** The workload is data-center decode for frontier mixture-of-experts (MoE) models with 128K+ token contexts. Training is secondary. "Best" means the most tokens per joule and the lowest $/M tokens at ≥100 tokens/s per user.

**Why leading designs stall:**
- **HBM energy.** HBM costs about 3–5 pJ/bit. Rubin reportedly has 288 GB of HBM4; Ironwood reportedly has 192 GB at about 7.4 TB/s.
- **SRAM capacity.** SRAM is about 0.1–0.3 pJ/bit, but bitcell area has nearly stopped shrinking (about 0.021 µm² from N3 to N2). A 1T-parameter FP4 model (about 500 GB) would need roughly 2,200 Groq LPUs (about 230 MB each) or about 12 Cerebras WSE-3 wafers (44 GB each).
- **Weight traffic.** With 37B active parameters at FP4, each decode step reads 18.5 GB of weights. At 4 pJ/bit that is about 0.6 J per step, but batching shares it across users.
- **KV-cache traffic, the binding cost.** The KV cache is not shared. At about 70 KB per token, 128K tokens of context is about 9 GB per user, or about 0.29 J per generated token. That cost is per user and stays at every batch size.

**Architecture.** Logic chiplets (N2-class, about 4 reticles of silicon) sit on a substrate with 8 HBM4 stacks. HBM4 base dies are built on a logic process. Optics are co-packaged at about 1–2 pJ/bit, versus about 5 pJ/bit for electrical SerDes. Power is about 2 kW per package, cooled by direct liquid. Numerics use 4-bit codebooks. The programming model is a compiler that maps graphs into three tiers: attention, expert GEMM and broadcast streams.

**What must be true:**
- Each HBM4 base die can absorb about 3–5 W of attention logic without causing DRAM refresh or thermal derating.
- Codebook quantization stays within 0.5% of FP8 accuracy.
- A 1:16 optical split (about 12 dB of loss plus about 2 dB of excess loss) still closes the link budget with commodity lasers.
- Throughput holds even though the network is deterministic only per step, not per cycle.

**Risks.** The design depends on HBM vendors opening the base die to customer logic, and gives up flexibility for training.

=== IDEAS ===
IDEA 1
NAME: Attention inside HBM base die
MECHANISM: Each HBM4 stack's logic base die holds that stack's KV-cache slices and computes the attention scores, softmax partials and value sums locally. Only query vectors and partial outputs (a few KB per head) cross the PHY, not gigabytes of KV. A host-side merge combines the partial softmaxes from all stacks exactly, and the cache is re-sharded as sequences grow.
VALUE: Long-context decode energy no longer scales with interface bandwidth, cutting the roughly 0.29 J per token of KV traffic by an order of magnitude.

IDEA 2
NAME: Codebook-gather arithmetic
MECHANISM: Weights are stored as 4-bit indices into 16-entry codebooks fitted per channel group. For each activation, the chip computes 16 products once and keeps them in SRAM. Every multiply-accumulate then becomes a table lookup plus an add. Codebooks are refit offline per layer, and the hardware can switch between 8- and 16-entry tables.
VALUE: Removes multiplier area and energy from expert GEMMs while keeping FP4-level storage at near-FP8 accuracy.

IDEA 3
NAME: Optical weight broadcast fabric
MECHANISM: Each package holds 1/16 of the expert weights. Weights are read from HBM once and sent through passive 1:16 optical splitters to 16 packages at the same time. Each package keeps different users' KV caches and activations. The compiler schedules one weight stream per layer and lets each receiving package consume it in batch.
VALUE: Divides HBM weight-read energy per token by about 16 without SRAM-scale chip counts, making frontier MoE serving cheaper than either HBM-bound GPUs or SRAM-bound wafers.