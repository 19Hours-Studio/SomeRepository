**Continuum: three candidate architectures for AI accelerators**

**Scope.** Target: data-center MoE inference and training. Metrics: tokens/J, $ per token, and BOM $ per delivered TB/s and per PFLOP. By the ceiling table, A has no room for a 3x gain. D and B have room, and C is tight. So I claim BOM and energy gains, not "3x TCO".

**The 8 first answers.** Bigger HBM4 GPU, more CoWoS area, FP4 everywhere, larger NVLink domain, wafer-scale SRAM, SRAM dataflow farm, photonic or analog matrix units, and transformer-only ASIC. **Shared paradigm:** weights and KV live in an off-die memory reached through a scarce interposer, and the effort goes into compute.

**Reference points (reported, unverified)**

| Chip | Memory | Bandwidth | Compute |
|---|---|---|---|
| Rubin | 288 GB HBM4 | ~22 TB/s | ~50 PF NVFP4 |
| Ironwood | 192 GB | 7.4 TB/s | 4.6 PF FP8 |
| WSE-3 | 44 GB SRAM | n/a | n/a |
| Groq | 230 MB per chip | n/a | n/a |

**Estimates and risks (mine, not sourced)**
- **Bonded DRAM (Idea 1).**
  - DRAM density is ~0.35 Gb/mm². Four bonded layers over 800 mm² give ~140 GB.
  - At 9 µm pitch and 2 Gb/s per pad, 10% pad use gives ≥20 TB/s.
  - It loses on peak FLOPS to Rubin (~0.5x, thermal cap) and on single-model capacity to a whole NVL72.
  - It kills: DRAM retention above 0.5 W/mm² of logic.
- **LPDDR training (Idea 2).**
  - 4096² FP8 tiles reach ~4k FLOP/B. So 2 PF needs ~0.5 TB/s, which a 512-bit LPDDR5X interface provides (~680 GB/s) for ~$4/GB, against HBM at ~$15–20/GB.
  - It loses on attention and optimizer phases, which are bandwidth-bound.
  - Staff cost caps the gain at ≤1.6x per run.
- **Attention PIM (Idea 3).** Off-package HBM costs ~5–7 pJ/bit against ~1 pJ/bit in-bank. At 128K context, KV is the majority of decode bytes. Realistic gain is 1.3–1.8x tokens/J. That is not 3x.

**Falsification**
- Thermal and refresh test on a bonded DRAM-on-logic test vehicle.
- Roofline simulation of a full Llama/DeepSeek training step on a 0.5 TB/s model.
- Measured joules per token for PIM attention against an H100 baseline at 16K and 128K, with bit-exact outputs.

**Software.** Unmodified PyTorch through a torch.compile/Triton backend. Attention PIM is exposed as one FlashAttention-compatible op. Software is the first risk: it killed Gaudi and Graphcore.

=== IDEAS ===
IDEA 1
NAME: Continuum-B bonded DRAM stack
MECHANISM: Four commodity DRAM layers are hybrid-bonded directly onto the compute die, with no interposer, HBM or CoWoS. This gives an estimated ~140 GB at ≥20 TB/s, holding MoE weights plus KV. Logic power density is capped near 0.5 W/mm² so DRAM retention holds, trading peak FLOPS for bandwidth. The closest earlier attempts are HBM-PIM, which failed on programmability, and Cerebras, which failed on capacity. This design adds no in-memory logic and keeps DRAM-class capacity, so neither reason applies. The deciding quantity is DRAM refresh rate at the junction temperature over the logic.
VALUE: Removes roughly 60% of BOM, the HBM and packaging share, and the CoWoS supply limit, while matching HBM-class decode bandwidth.

IDEA 2
NAME: Continuum-T LPDDR training chip
MECHANISM: The chip has 256 MB of SRAM holding 4096² GEMM tiles, raising arithmetic intensity to ~4k FLOP/B. A 512-bit LPDDR5X interface (~0.68 TB/s) can then feed ~2 PF FP8. FSDP sharding keeps per-chip optimizer state small. The closest earlier attempt is Dojo, which failed on memory capacity. Here, commodity LPDDR gives cheap capacity, and the large tiles remove the need for HBM bandwidth. The deciding quantity is the fraction of step time in bandwidth-bound attention and optimizer phases.
VALUE: Estimated ~2x lower accelerator $ per training PFLOP using unconstrained memory supply.

IDEA 3
NAME: Continuum-K exact attention PIM
MECHANISM: The KV cache sits in LPDDR-PIM modules whose banks compute one fixed primitive: QKᵀ, online softmax and the V sum. Only query vectors and partial outputs cross the link. The closest earlier attempt is Samsung HBM-PIM, which stalled on general programmability. Exposing a single FlashAttention-compatible operator removes that need. Outputs are exact, with no eviction. The deciding quantity is KV's share of decode bytes at the target context length.
VALUE: An estimated 1.3–1.8x more tokens per joule for long-context decode, with no accuracy change.