**Scope.** Continuum is a data-center family for frontier MoE inference, with training as a secondary target. "Best" is measured by four numbers at matched model quality:
- tokens/J at 32K context
- $/M tokens at ≥100 tok/s/user
- BOM per chip
- time-to-loss for training

**Facts and estimates are kept apart.** Sourced (CONTEXT, not checked this session):
- B200 BOM ≈$6.4k, of which HBM 45% and CoWoS 17%.
- Decode energy is 107→242 mJ/token from 4K to 16K context.
- A 32K-token request needs 8.6 GB of KV.

Everything else below is a design estimate.

**Ceilings.** In inference TCO, vendor margin (28%) cannot be engineered away, so silicon alone cannot deliver 3× cheaper. Tokens/J and BOM are where physics has room.

**Software.** PyTorch → torch.compile → Triton/MLIR backend, with vLLM/SGLang plugins. Existing checkpoints run unmodified at FP8 or NVFP4. Graphcore and Gaudi died on software, so this ships before the silicon.

**Kill tests.**
- Cycle-accurate decode simulation of DeepSeek-class models at 32K, compared against measured H100 and B200 energy.
- Prefill model-FLOP utilization (MFU) on an FPGA or emulator.
- 70B FP4 training against FP8.

**Honest losses.**
- Groq and Cerebras win on single-user latency for small models.
- Rubin keeps CUDA and NVLink maturity.
- Ironwood keeps OCS pod scale.

=== IDEAS ===
IDEA 1
NAME: Continuum-D 3D-DRAM decode
MECHANISM: A logic die is hybrid-bonded under 4 DRAM stacks (est. 64 GB, 16 TB/s, ~0.5 pJ/bit, versus ~4 pJ/bit for HBM3E). Each chip holds its expert shard plus the KV of its own users, so no byte crosses a PHY. Roofline: at 4 pJ/bit, reading 8.6 GB of KV per token costs ~275 mJ; at 0.5 pJ/bit it costs ~34 mJ. If HBM streaming is ~50% of decode energy (est.), total energy/token falls ~1.8×. The closest earlier attempt is HBM-PIM, which stalled on programmability; here the DRAM is plain addressable memory with no in-DRAM logic. The deciding quantity is delivered pJ/bit at ≥60% of peak bandwidth (H100 reached only 27%).
VALUE: About 1.8× more tokens per joule at long context, with no HBM supply dependence.

IDEA 2
NAME: Continuum-P LPDDR prefill die
MECHANISM: A reticle-sized FP4/FP8 compute die (est. 10 PFLOPS) sits with 256 GB of LPDDR6 (~1 TB/s) on an organic substrate, with no CoWoS and no HBM. An 8K-token prefill chunk does ~16K FLOP per weight byte, which is above the 10K FLOP/B ridge point, so cheap memory does not throttle it. Estimated BOM is ~$2.5k against $6.4k. The closest earlier attempt is Rubin CPX on GDDR7; Continuum is open-licensed rather than tied to one vendor's margin. The deciding quantity is sustained prefill MFU ≥50%, given the LPDDR bandwidth.
VALUE: About 2.5× lower BOM per prefill FLOP, built from uncontended supply chains.

IDEA 3
NAME: Continuum-T FP4 training mode
MECHANISM: The tensor cores run NVFP4 with per-block FP8 fallback, chosen per layer by a hardware overflow and stochastic-rounding monitor that promotes unstable layers and the final phase of training. This doubles throughput per mm² over FP8. The closest earlier attempt is NVFP4, which is proven only to 12B and lost on code benchmarks; the automatic promotion bounds that loss. The deciding quantity is tokens-to-target-loss at ≥70B within 10% of FP8. Hardware is 44% of training cost, so the gain is ≈1.3× cost, not 3×.
VALUE: Frontier training about 1.3× cheaper, and the design is falsifiable on a single 70B run.