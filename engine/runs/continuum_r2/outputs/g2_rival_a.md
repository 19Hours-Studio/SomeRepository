Continuum targets frontier training and MoE inference in existing data-center halls. Archetype B, frontier training, has the most room: hardware is 44% of cost, with a 1.66× ceiling if that term falls 10×. Archetype A, MoE inference, has no room for 3×, so I claim only about 1.2× there.

**Metrics:**
- **Training:** $ per useful training FLOP, counting goodput.
- **Inference:** $ per million tokens at at least 100 tok/s/user, and deployability in 40 kW air-cooled halls.

**Facts used:**
- HBM is 45% of B200 BOM and packaging 17%.
- CoWoS and HBM are sold out to about 2028.
- At N3E, 1 GiB of SRAM takes about 258 mm².

**Key check for Idea 1 (my arithmetic):**
- An FP8 GEMM with M=16K and N=K=8192 reaches about 6,600 FLOP/B. A die with 1 TB/s of LPDDR6 and 2 PFLOPS FP8 needs 2,000 FLOP/B, so this GEMM clears the ridge.
- Activation checkpoints (layer inputs only, with recompute) reach about 300K FLOP/B.
- FSDP weight gathers at 16K tokens per chip need about 125 GB/s per chip, which fits 2×800G Ethernet.
- So the design only fails if activation and normalization traffic leaves the chip. The earlier HBM-lean trainer died for exactly that reason.

**Losses, stated honestly:**
- Per-chip decode latency is worse than Groq or Cerebras.
- Peak FLOPS per package is about 2× lower than Rubin.
- None of the three ideas lowers staff cost. Idea 2 does not cut vendor margin.

**Falsification tests:**
- **Idea 1:** a cycle-level simulation of a 70B training step and a DeepSeek-V3-class MoE step using torch.compile graphs. It is dead if more than 15% of step time is LPDDR-bound.
- **Idea 2:** measure link pJ/bit and $/Gbps for co-packaged optics against copper. It is dead if all-to-all takes more than 20% of decode-step time.
- **Idea 3:** replay Llama-3-scale interruption logs, which show 419 failures in 54 days. It is dead if goodput gains less than 5 points.

=== IDEAS ===
IDEA 1
NAME: Fusion-enforced LPDDR training die
MECHANISM: A reticle-sized N3 die (about 2 PFLOPS FP8, about 600 W, air-cooled) carries 512 MB of on-die SRAM and 256 GB of LPDDR6 at about 1 TB/s on an organic substrate, with no HBM or CoWoS. The compiler takes torch.compile graphs and rejects any schedule where norms, activations, attention softmax or optimizer steps spill to DRAM. It keeps them fused in SRAM epilogues, so only GEMM operands, layer-input checkpoints and FSDP shards leave the chip. The closest earlier attempts are the HBM-lean trainer, which died on memory-bound non-GEMM time (fusion removes that traffic), and Graphcore, which died on software (this design accepts unmodified PyTorch). The deciding quantity is off-chip bytes per FLOP over a full training step, which must stay below 1/2000; that needs at least 2K tokens per expert per pass.
VALUE: Removing HBM and CoWoS, about 62% of today's BOM, cuts the cost per training FLOP by about 1.5–2× (estimate) and frees training from the HBM and CoWoS supply limits.

IDEA 2
NAME: Optically spread air-cooled scale-up
MECHANISM: Co-packaged optics at about 5 pJ/bit stretch one 72-chip MoE expert-parallel domain across three 40 kW air-cooled racks, instead of one 130 kW liquid-cooled rack. A switch keeps all-to-all latency under 2 µs. The closest earlier attempts are Google's optical-switched pods, which are captive and still use HBM and CoWoS, and NVL72 copper, whose reach limit forces the 130 kW density. The deciding quantity is all-to-all time as a share of decode-step time, which must stay below 20%.
VALUE: Frontier MoE models can be served in existing halls without liquid retrofits, for about 1.2× lower TCO (estimate).

IDEA 3
NAME: Peer-mirrored state for goodput
MECHANISM: Each chip mirrors its FSDP shard and optimizer delta into a neighbour's LPDDR every step over spare link bandwidth, and hot spares join the job in seconds. On-die checks of GEMM checksums flag silent data corruption before a bad state is mirrored. The closest earlier attempt is periodic checkpointing to storage, which loses minutes per failure and misses silent corruption. The deciding quantity is the mirroring traffic per step relative to spare link bandwidth.
VALUE: Training goodput rises from about 90% to about 98% at 100K-chip scale, which is about 9% off per-run hardware cost.