**Targets and metrics.** The design targets two workloads. The first is low-latency decode at 200–500 tok/s/user, measured as $/Mtok at a fixed tok/s/user (Archetype C has a 16.7× ceiling). The second is training, measured as $/useful-PFLOP-hour (Archetype D is tight at 9.1×). Capex is about 85% of TCO and energy only about 10%, so tokens/J is a secondary metric.

**Deciding economics (my estimates, not sourced).** On capacity, LPDDR5X costs about $5/GB against about $18/GB for HBM. On bandwidth the comparison reverses: LPDDR5X is about $1.9 per GB/s, and an HBM4 stack is about $0.3 per GB/s. A capacity tier therefore wins only when SRAM reuse R (bytes delivered to compute ÷ external bytes) is at least about 6. Continuum cannot claim to be "best" overall. Its claim is to match HBM-class throughput without CoWoS or HBM supply, where R allows it.

**Candidates**
1. HBM4 + bigger L2, i.e. a Rubin clone | P 0.45
2. Wafer-scale SRAM with external weight store | P 0.25
3. LPDDR/CXL capacity tier with an SRAM double-buffered layer stream | P 0.20
4. HBF (high-bandwidth flash) weights tier | P 0.12
5. Router-lookahead MoE expert prefetch into SRAM | P 0.08
6. Tensor-parallel LPDDR "bandwidth-by-count" decode, no CoWoS | P 0.07
7. HBM-free training chip with SRAM-tiled GEMM and offloaded optimizer state | P 0.05
8. Analog CIM weights tier | P 0.04

I develop candidates 5, 6 and 7.

**Checks**
- **Candidate 6.**
  - Each Continuum die has 24 × 32 GB LPDDR5X on organic substrate, giving about 2 TB/s and 768 GB.
  - Spreading a 70B FP8 model (70 GB) across 9 dies means each die streams 7.8 GB per token in 3.9 ms. That is about 256 tok/s/user, with 18 TB/s aggregate. Groq used 576 chips for about 300 tok/s.
  - KV cache is about 160 KB/token. At 8k context that is 1.3 GB/user, which fits in LPDDR. KV reads of 1.3 GB/9 dies per token cut the batch headroom.
  - It loses to Cerebras on single-user speed (about 2,100+ tok/s) and to Rubin on bandwidth per dollar.
- **Candidate 5.** A 37B-active MoE at FP8 needs about 37 GB per token. Fetched at 2 TB/s, a mispredicted expert stalls a layer by more than 1 ms.
- **Candidate 7.**
  - At 4 PFLOPS and 2 TB/s, the chip needs about 2,000 FLOP/B.
  - A 256 MB SRAM GEMM tile gives about 5,000 FLOP/B (√S-scaling estimate).
  - Optimizer state for 100M params/chip × 16 B is 1.6 GB per step, which is trivial.

**Falsification plan.** Run a cycle-level simulation of Llama-3-70B and DeepSeek-V3 traces. Measure:
- R per layer
- expert-prediction hit rate
- achieved FLOP/B on attention and collectives

The design is killed if R < 6, hit rate < 85%, or training MFU < 40%.

**Software.** PyTorch/XLA compiles through a StableHLO backend, and existing checkpoints load unchanged. Prefetch is compiler-inserted, and the hardware predictor is transparent to the model.

=== IDEAS ===
IDEA 1
NAME: Router-lookahead expert prefetch
MECHANISM: A small on-die predictor reads each layer's hidden state and predicts the next layer's top-k experts one to two layers ahead. It then issues DMA from LPDDR5X into SRAM, while frequency counters keep hot experts pinned in SRAM. The closest earlier attempts are Pre-gated MoE and MoE-Infinity, which were stalled by PCIe offload at about 64 GB/s; on-package LPDDR at about 2 TB/s removes that link. The deciding quantity is the prediction hit rate multiplied by lead time, set against the per-expert fetch time; it needs at least 85% hits.
VALUE: Frontier MoE models can be served from about $5/GB DRAM instead of HBM, with no CoWoS allocation needed.

IDEA 2
NAME: Bandwidth-by-count LPDDR decode
MECHANISM: Nine dies, each with 24 LPDDR5X packages (about 2 TB/s and 768 GB each), hold one tensor-parallel shard of a 70B FP8 model plus its KV slice. Each die streams 7.8 GB per token through double-buffered SRAM, for about 256 tok/s/user. The closest earlier attempt is Groq, whose chip count (576) was set by SRAM capacity; here capacity is DRAM, so the count is set by bandwidth alone. The deciding quantity is the SRAM reuse ratio, which must be at least about 6 to beat HBM on dollars per GB/s.
VALUE: It delivers SRAM-dataflow-class latency with about 60× fewer chips and no HBM or CoWoS dependency.

IDEA 3
NAME: HBM-free SRAM-tiled training chip
MECHANISM: A 256 MB SRAM tile buffer feeds about 4 PFLOPS FP8 GEMMs at about 5,000 FLOP/byte. Weights, activation checkpoints and optimizer state (16 B/param) sit in LPDDR or CXL DRAM at about 2 TB/s, with hardware-sequenced prefetch. The closest earlier attempts are Dojo and Graphcore, which had SRAM only and no capacity tier, and ZeRO-Infinity, which was PCIe-bound. The deciding quantity is the achieved FLOP/byte on attention and collectives, which must stay above 2,000.
VALUE: It cuts the HBM share of accelerator-package cost in training clusters while staying above 40% MFU.