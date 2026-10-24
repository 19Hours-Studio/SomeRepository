# Continuum: three candidate architectures

**Targets and metrics.** The stated targets are data-center frontier MoE inference and long-context decode, plus frontier pretraining. The metrics are joules per token at a fixed tok/s/user, BOM dollars per GB/s of weight bandwidth, and training cost per run. These metrics define "best" because the ledger shows memory movement and memory plus packaging dominate the terms a chip can change: about 50% of decode energy (C, my estimate) and about 62% of BOM (D). Inference TCO (A) leaves no room for a 3x gain, so it is not the target.

**Conventional answers and their shared paradigm.**
1. Bigger HBM4/4E stacks.
2. More CoWoS area.
3. FP4 training.
4. Larger NVLink-class domains.
5. A wafer-scale SRAM successor.
6. A Groq-style SRAM swarm.
7. Co-packaged optics.
8. A transformer ASIC.

All eight put fast compute on a logic die and buy bandwidth either from scarce stacked memory beside it or from expensive SRAM.

**Reference points (vendor figures).**

| Design | Memory | Bandwidth |
|---|---|---|
| Rubin | 288 GB HBM4 | ~22 TB/s |
| Ironwood | 192 GB | 7.4 TB/s |
| WSE-3 | 44 GB SRAM | 21 PB/s, ~150 GB/s off-wafer |
| Groq | 230 MB SRAM | — |

**My estimates** for Idea 1 per package: 4 commodity-DRAM layers hybrid-bonded onto a ~600 mm² logic die.
- **Capacity:** about 70 GB, from 0.23 Gb/mm² × 600 mm² × 4 layers.
- **Bandwidth:** about 40 TB/s, from 9 µm bond pitch, ~10% of the area used for signals, ~0.5 Gb/s per bond.
- **Energy:** about 0.5 pJ/bit, versus about 4 pJ/bit for HBM.
- **Compute:** logic is capped at about 450 W so the DRAM stays below 95 °C. That gives roughly 4 PFLOP FP8, below Rubin.
- **Where it wins and loses:**
  - It wins on bandwidth per GB and energy per byte, by about 5–8x.
  - It loses about 4x on capacity per package against Rubin.
  - It needs about 3x more packages than Rubin per model shard.
- **Roofline check:** sweeping 70 GB at 40 TB/s takes 1.75 ms per decode step for one shard.

**Software.** All three designs use the standard path: PyTorch to torch.compile to an MLIR backend, with vLLM/SGLang paging and no model changes.

**Falsification tests.**
- Idea 1: a thermal test vehicle measuring DRAM refresh rate at 450 W.
- Idea 2: run attention offload on HBM-PIM silicon with a bit-exactness check against a reference.
- Idea 3: run DiLoCo at 70B or larger against a matched-token synchronous baseline.

=== IDEAS ===
IDEA 1
NAME: DRAM-on-logic hybrid bond
MECHANISM: Commodity DRAM wafers are hybrid-bonded directly onto the compute die, replacing HBM and CoWoS. This gives roughly 70 GB at 40 TB/s for about 0.5 pJ/bit, versus about 4 pJ/bit for HBM (estimate). HBM-PIM stalled because it put logic into the DRAM process and broke programmability. Here the DRAM is plain addressable memory and the accelerator stays conventional. The deciding quantity is DRAM retention and refresh overhead at logic hotspot temperature.
VALUE: Cuts decode memory energy about 7x, about 1.7x per token, and removes HBM and CoWoS from both supply chain and BOM.

IDEA 2
NAME: Fixed attention engine in DRAM
MECHANISM: Each DRAM base die carries one hardwired primitive: a GQA decode-attention dot product with softmax-weighted V accumulation over contiguous KV pages the serving engine already allocates. It needs no address translation and no user programming. PIM previously failed on programmability; this exposes a single library kernel. The deciding quantity is the KV share of decode bytes at 32K tokens or more. It must exceed about 60%, and GQA's ~8 FLOP/B intensity must fit in-die ALUs.
VALUE: Long-context decode stops streaming KV across the memory interface, roughly halving energy per token at 16K–128K context.

IDEA 3
NAME: Low-communication training islands
MECHANISM: Silicon and fabric are sized for DiLoCo-style training: dense copper all-to-all inside air-coolable 40 kW islands, with about 100x thinner links between islands that synchronize outer-optimizer deltas every few hundred steps. Dojo and NVL72 bet on ever-denser scale-up and hit yield and facility walls. This trades bandwidth for algorithmic tolerance instead. The deciding quantity is DiLoCo's extra-token penalty beyond 70B parameters, which must stay below about 10%.
VALUE: Removes most of the 13% scale-out networking cost and lets frontier runs span power-limited sites. The gain is roughly 1.15–1.2x on cost, not several times.