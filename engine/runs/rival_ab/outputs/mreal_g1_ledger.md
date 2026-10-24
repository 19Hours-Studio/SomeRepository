# Continuum: a three-tier, HBM-light inference architecture

**Target and metrics.** Continuum targets data-center serving of frontier MoE models (DeepSeek/Kimi class, about 671B parameters, 37B active per token). It is judged on four metrics:
- **$/Mtok** and **J/token**, because they set inference cost (cost ledgers A and C).
- **tok/s/user**, kept at or above 80.
- **Rack power**, kept at or below 40 kW so racks stay air-cooled.

It does not claim to be best at training. A 10x cut in hardware cost saves training runs only about 1.66x, because staff cost does not fall.

**Facts used**
- GB200 NVL72 serves at about $0.04–0.08/Mtok at 85–195 tok/s/user.
- On B200 the BOM is about 45% HBM and 17% packaging.
- 2026 HBM and CoWoS supply is sold out.
- Long-context decode costs about 242 mJ/token at 16K context.

**Estimates (est.)**
- LPDDR costs about $5/GB, against about $16/GB for HBM3E at $550–600 per stack.
- HBM costs about 4 pJ/bit end to end.

**Sanity checks (est.)**
- **Expert tier, bandwidth.** 340 GB of FP4 expert weights over 32 chips is 10.6 GB per chip. At 1.1 TB/s that is about 10 ms per step, or about 95 tok/s per user.
- **Expert tier, compute.** With 2,048 concurrent users, each expert sees 64 tokens per step, which gives 256 FLOP/B. That is below the 2,000 FLOP/B ridge, so the tier is bandwidth-bound and the bandwidth figure above sets the step time.
- **Expert tier, fabric.** Moving activations across the fabric needs about 43 GB/s per chip.
- **Attention tier.** A 16K context in a GQA-70B model reads about 5.2 GB of FP16 KV per token, about 168 mJ at 4 pJ/bit.
  - Storing KV in FP4 cuts bytes 4x.
  - Running attention in the HBM base die avoids the PHY and interposer, cutting energy per bit about 1.5x (est.).
  - Together that is about a 6x reduction, roughly 28 mJ instead of 168 mJ.
- **Prefill tier.** An 8K-token prompt needs 6×10¹⁴ FLOP, about 0.15 s at 10 PFLOPS and 40% utilization. Reading the weights takes only 18 ms, so prefill is compute-bound and LPDDR is enough.

**Versus competitors**
- **Rubin/GB200.** Continuum wins about 2–3x on $/Mtok (est.) and runs at about 15 kW instead of about 120 kW. It loses about 2x on peak tok/s/user.
- **Ironwood.** Ironwood still depends on HBM and CoWoS, and Continuum wins on supply for the same reason. Whether it beats Ironwood on $/Mtok is unverified, because Ironwood specs were not found.
- **Cerebras and Groq.** Continuum holds the full model in about 32 chips rather than hundreds. It loses 5–10x on single-user latency.

**Risks and falsification tests**
- **Fabric tail latency.** Each decode step needs 116 all-to-all exchanges, each within about 50 µs. Test: simulate p99 at 2,048 users.
- **FP4 KV accuracy.** Test: RULER and LongBench at 128K context. Kill the design if accuracy drops by more than 1 point.
- **HBM4 custom base-die access.** This needs vendor cooperation.
- **LPDDR6 price risk.** If LPDDR goes above $10/GB, the cost win falls below 1.5x.

**Software.** Continuum lowers PyTorch through a torch.compile/MLIR backend and adds a vLLM/SGLang disaggregation plugin. Models are not retrained; only post-training FP4 quantization is required. The CUDA ecosystem is the biggest commercial risk.

=== IDEAS ===
IDEA 1
NAME: LPDDR expert-stationary decode tier
MECHANISM: Each chip is a CoWoS-free, organic-substrate die with 256 GB of LPDDR6 at about 1.1 TB/s and about 2 PFLOPS of FP4. It permanently holds a shard of the MoE experts, and routed activations travel to the experts instead of weights travelling to the tokens. Pooling about 2,048 users gives 64 tokens per expert per step, so 32 chips each stream 10.6 GB per step, about 10 ms, or about 95 tok/s per user, at about 15 kW air-cooled. The closest earlier attempt, HBM GPUs, is limited by HBM and CoWoS supply and cost. Weights shared across a batch tolerate cheap bandwidth, so this tier avoids that limit. The deciding quantity is all-to-all p99 latency, which must stay under about 50 µs per layer.
VALUE: FFN decode on frontier MoE at an estimated 2–3x lower $/Mtok with no HBM, no CoWoS and no liquid cooling.

IDEA 2
NAME: Base-die FP4 KV attention
MECHANISM: Fixed-function GQA/MLA attention units sit in custom HBM4 base dies and read KV stored as FP4 with per-16-element scales over the TSVs. Only queries and outputs cross the PHY. Bytes per step fall 4x and energy per bit about 1.5x (est.), so 16K-context attention falls from about 168 mJ to about 28 mJ per token. The closest earlier attempt, HBM-PIM, stalled on programmability. Restricting the logic to one fixed attention kernel behind a vLLM operator avoids that problem. The deciding quantity is the accuracy loss from FP4 KV at 128K context.
VALUE: An estimated 5–6x lower long-context decode energy, attacking the cost term that dominates decode energy.

IDEA 3
NAME: LPDDR-only compute-bound prefill die
MECHANISM: A reticle-sized die with about 10 PFLOPS of FP4/FP8 and 256 GB of LPDDR runs prefill. Prefill is compute-bound: an 8K-token prompt needs 0.15 s of compute but only 18 ms of weight reads. The die then ships the 0.57 GB of KV over a 100 GB/s link to the decode chips in about 6 ms. The closest earlier attempt, GPU prefill, wastes HBM bandwidth that prefill never uses. Removing the HBM cuts roughly 60% of the BOM. The deciding quantity is sustained FP4 utilization above 40%.
VALUE: Prefill FLOPs at an estimated 2x or more lower capex per FLOP using unconstrained packaging and memory supply.