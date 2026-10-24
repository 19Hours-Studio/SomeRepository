# Continuum: proposals for a long-context MoE decode accelerator

**Target and metrics.** The target is data-center decode of a GQA-class MoE model (about 670B total parameters, about 37B active, FP4 weights) at 128K context. The service floor is ≥100 tok/s/user. "Best" means the lowest J/token and $/token per rack at that floor. Training and edge are out of scope, so I claim no win there. Ceilings matter: decode energy is TIGHT for a 3x gain and TCO has NO ROOM for 3x. I therefore claim 1.5–2x, not "several times".

**The deciding arithmetic** (my estimates, using standard GQA shapes):

- **KV cache size.** 8 KV heads × 128 dimensions × K and V × 92 layers × FP8 gives about 188 KB/token. At 128K context that is about 24 GB per user.
- **KV bandwidth.** At 100 tok/s, each user needs about 2.4 TB/s. That is several times the weight traffic per token at batch 64.
- **Required ratio.** Every KV byte is read once per token, so the memory needs a bandwidth-to-capacity ratio of 100 per second.
- **What supplies that ratio.** HBM3E offers about 33/s (1.2 TB/s over 36 GB). GDDR7 offers about 43/s. LPDDR5X offers about 5/s. Only SRAM exceeds 100/s, and SRAM has too little capacity. The workload therefore buys bandwidth and gets capacity for free. The decisive figures are **$/(GB/s) and pJ/byte**, not $/GB.

**Comparison at 128K context and 100 tok/s/user:**

| Design | Reported spec | Users served at 128K, 100 tok/s |
|---|---|---|
| GB300 NVL72 | 576 TB/s, about 20 TB HBM | ≤240 if all bandwidth goes to KV |
| Ironwood | 7.4 TB/s, 192 GB per chip | About 3 per chip |
| Cerebras WSE-3 | 44 GB on-wafer | About 1.8 users' KV fits; off-wafer I/O (~150 GB/s) cannot feed it |
| Groq | 230 MB per chip | About 100 chips per user, for KV alone |

On this workload, SRAM-centric designs lose outright. Continuum's realistic opponent is the HBM GPU, and its edge over that GPU is the 1.5–2x stated above. It loses on prefill FLOP density, on short-context work, and on training.

**Main risks:**

- Thermal derating of DRAM stacked on logic.
- GDDR7 energy of about 6–7 pJ/bit, versus about 4 pJ/bit for HBM3E.
- Hybrid-bonding supply.
- Software. Graphcore and Gaudi died here.

**Software plan.** Ship a PyTorch/vLLM backend and a Triton kernel path that accept unmodified checkpoints. Use an attention-disaggregation API, so models need no retraining.

**Falsification test.** Build a cycle-level simulation plus an FPGA memory testbed. Calibrate it first against measured H100 numbers: 107 and 242 mJ/token at 4K and 16K context, with 27% HBM utilization. If it cannot reproduce those, its Continuum predictions are not trusted.

**What is fact and what is assumed.** Device specs are vendor figures. The energy-per-bit values, prices and shares are estimates that need checking.

=== IDEAS ===
IDEA 1
NAME: DRAM-on-logic attention tiles
MECHANISM: Hybrid-bond 8-high DRAM directly onto the attention-compute die, with no interposer and no CoWoS. Size it at about 48 GB and 4–6 TB/s per tile, and stream the KV over vertical links at an assumed 1 pJ/bit instead of HBM's roughly 4. Experts stay on separate FP4 chips. The closest earlier attempt is HBM-PIM, which stalled on programmability. That problem does not apply here, because compute stays in normal logic with ordinary kernels. The deciding quantity is the delivered pJ/byte after thermal derating of DRAM that sits over hot logic.
VALUE: If HBM streaming is about half of decode energy, it gives roughly 1.5–1.6x tokens per joule at 128K context and 100 tok/s/user, against GB300-class racks.

IDEA 2
NAME: GDDR7 disaggregated attention rack
MECHANISM: Attention chips on standard PCB hold the KV in GDDR7 at an estimated $0.23 per GB/s, against about $0.48 for HBM3E. Expert chips keep the weights in HBM, since weight traffic is amortized over the batch. Only the query and attention-output vectors cross the link, a few KB per layer. The closest earlier attempt is CXL or host offload, which failed because the KV had to travel back over a slow link. Here the KV never moves. The deciding quantity is $/(GB/s) at a 100/s bandwidth-to-capacity ratio, net of GDDR7's higher pJ/bit.
VALUE: It roughly halves the cost of KV bandwidth and sidesteps HBM and CoWoS scarcity, for an estimated 1.3–1.7x lower $/token on long-context decode.

IDEA 3
NAME: Lossless KV entropy coding
MECHANISM: Memory controllers entropy-code FP8 KV exponents and signs on write and decode them in-line on read, using per-head tables refit every few thousand tokens. Model outputs stay bit-identical. The closest earlier attempt is lossy KV quantization or eviction, which fails requirements that the same model give the same outputs. Lossless coding meets them. The deciding quantity is the measured entropy of real KV caches; the gain is worthwhile only if it exceeds about 1.15x.
VALUE: Any KV-bandwidth-bound decode gets an estimated 1.1–1.3x more users per rack at zero accuracy cost, and the gain stacks with any memory technology.