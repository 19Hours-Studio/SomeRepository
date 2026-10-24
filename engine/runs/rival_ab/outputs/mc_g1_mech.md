# Continuum: three candidate architectures

**Target and metrics.** The target is the data center, not the edge. Three metrics define "best":
- **Decode energy:** joules per token at 16K+ context.
- **Packaging cost:** BOM per unit of delivered bandwidth.
- **Training cost:** cost per training FLOP that does not depend on HBM or CoWoS supply.

I chose these because the ledger leaves room only here. BOM (D) and training hardware (B) have room. Decode energy (C) is tight. Inference TCO (A) has no room, so I make no TCO claim for it.

**Facts versus my estimates.** The comparison figures below are vendor or reported numbers, not independently checked:

| Chip | Memory | Bandwidth | Compute |
|---|---|---|---|
| Rubin | 288 GB HBM4 | ~22 TB/s | ~50 PF FP4 |
| Ironwood | 192 GB HBM | 7.4 TB/s | 4.6 PF FP8 |
| WSE-3 | 44 GB SRAM | ~21 PB/s on-wafer | — |
| Groq LPU | 230 MB SRAM | — | — |

The energy figures (pJ/bit) and LPDDR prices are my assumptions.

**Sanity check (C).** 121 mJ is 50% of 242 mJ/token at 16K context. That matches about 4.3 GB per token read at about 3.5 pJ/bit from HBM. This is my estimate, but it hangs together.

**Where it loses.** All three designs still lose on these points:
- Peak FLOPs per package versus Rubin.
- Ecosystem maturity. Graphcore and Gaudi died on software.
- Single-user latency versus Groq and Cerebras when the weights fit in SRAM.

**Software.** Unmodified PyTorch runs through a `torch.compile` backend. Fixed operations are exposed as library kernels. Models need no retraining.

=== IDEAS ===
IDEA 1
NAME: Attention inside memory base
MECHANISM: Each HBM4 stack gets a custom logic base die that holds its slice of the KV cache. The die computes the attention scores, softmax and weighted sum locally, so only queries go in and per-head outputs come out. Link traffic falls about 1000x at 16K context. Unlike general PIM, which stalled on programmability, this is one fixed operation called as a library kernel, so no address translation or coherence is needed. The deciding quantity is the base-die joules per KV bit (target ≤1 pJ). At that level, decode energy at 16K falls from 242 to about 150 mJ/token, roughly 1.6x. Base-die thermal budget under the DRAM stack is the main risk. A cycle-accurate model run against measured H100 traces would falsify the design if the result exceeds 1.3 pJ/bit.
VALUE: Long-context decode at roughly 1.6x lower energy per token, with no change to model outputs.

IDEA 2
NAME: Bonded DRAM decode tile
MECHANISM: Weights and KV live in DRAM layers hybrid-bonded directly onto the compute die, with no PHY and no interposer. The assumed figures are 0.5–0.8 pJ/bit and about 30 TB/s per 16–24 GB tile. Ninety-six tiles hold a 1T-parameter FP4 MoE plus its KV. Groq needed 576 chips because SRAM holds megabytes; this design holds gigabytes per tile. The deciding quantity is the yield of known-good bonded stacks, which must be ≥85% for the cost to close. A pilot-line yield test on 1,000 stacks would falsify it.
VALUE: Removes HBM and CoWoS from the decode path, which is about 62% of the flagship BOM.

IDEA 3
NAME: Commodity-memory training slab
MECHANISM: Compute sits on a standard organic package with 1 GB of SRAM tiles and 256 GB of LPDDR5X at about 1.1 TB/s. Large on-chip GEMM tiles raise reuse so that FP8 matmuls stay compute-bound at 0.0003 B/FLOP. Optimizer state and checkpoints live in LPDDR. Dojo died on wafer yield; this design uses reticle-sized dies. The deciding quantity is the share of training-step time that is memory-bound on B200 traces after fusion; it must be under 15%, or the bandwidth deficit, about 7x below B200, dominates. HBM ($2.9k) and CoWoS ($1.1k) are replaced by LPDDR ($1–2k at an assumed $4–8/GB). The net BOM saving is $2–3k, about 1.4x.
VALUE: Training capacity that HBM and CoWoS sell-outs cannot block, at about 1.4x lower BOM.