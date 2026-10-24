Continuum is a family of three dies. Each one targets whatever is scarce for its workload: HBM stacks, CoWoS wafers, or facility kW.

**Metrics**
- Decode: tokens/s/user ≥100 and tokens per joule.
- Training: FP8 model-FLOPs per dollar.
- Both: throughput per scarce input.

**Why these define "best"**
- HBM is about 45% of accelerator BOM, and HBM plus packaging is about two thirds.
- HBM streaming is about 50% of decode energy. That figure is my estimate.
- Facility cost is about 20% of inference TCO.

**Baselines**
- GB200/Rubin: HBM, CoWoS and 120 kW racks.
- Ironwood: also HBM and CoWoS.
- Groq and Cerebras: too little capacity (230 MB per chip; 44 GB per wafer with 150 GB/s off-wafer I/O).

**Where Continuum loses**
- About 3–8x less raw bandwidth per chip than HBM parts.
- About 0.4–2x the per-chip peak, depending on die.
- A new compiler that must reach PyTorch/vLLM parity through Triton/MLIR lowering. Gaudi and Graphcore failed on exactly this.

**What is fact and what is estimate**
- Facts: B200 BOM and its shares, rack power, and the capacities and I/O of Groq and Cerebras listed above.
- My estimates: all Continuum figures below.

=== IDEAS ===
IDEA 1
NAME: Continuum-V speculative-verify LPDDR decoder
MECHANISM: An FP4 die (est. 2 PFLOPS) sits with 16 LPDDR6 packages, about 0.9 TB/s and 256 GB, on an organic substrate with no HBM and no CoWoS. An on-die SRAM draft head of about 125 MB proposes token trees, and the die verifies 6 candidates per pass using exact rejection sampling, so outputs match the target model's distribution. Each weight byte and KV byte read is therefore amortized over the accepted tokens. At 37B active parameters in FP4 (18.5 GB per pass), 54 passes/s × 3.5 accepted gives about 190 tok/s/user, versus about 8 TB/s HBM parts running without speculation. The closest earlier attempt is EAGLE/Medusa on GPUs, whose gains collapse at large batch because the GPU's FLOP-to-byte ratio saturates. This die is provisioned at about 2,000 FLOP/B, so batch × tree still fits. The deciding quantity is mean accepted tokens per verify pass at sampling temperature >0 and production batch size, which must be ≥3.
VALUE: Delivers HBM-class decode speed for each user at an est. 3–4x lower memory BOM, with zero HBM stacks or CoWoS wafers consumed.

IDEA 2
NAME: Continuum-T HBM-free tiled trainer
MECHANISM: A reticle-sized FP8 die (est. 5 PFLOPS) carries 512 MB of hybrid-bonded stacked SRAM and 32 LPDDR6 channels (about 2 TB/s, 512 GB). The compiler holds 8K×8K output tiles on chip, giving about 8,000 FLOP/B on GEMMs. It fuses norms and elementwise ops into the tile pass, so peak/bandwidth, about 2,500 FLOP/B, is met everywhere. The closest earlier attempt is Cerebras MemoryX weight streaming, which was starved at about 150 GB/s off-wafer. This die gets about 13x that bandwidth per die from commodity DRAM. The deciding quantity is achieved FLOP/B over a whole training step, including attention backward and the optimizer, which must stay ≥2,500. A simulator replaying real Llama/MoE traces can falsify it.
VALUE: Frontier-scale training throughput per dollar with no HBM or CoWoS dependency, attacking the 44% hardware share of training cost.

IDEA 3
NAME: Continuum-X optical air-cooled scale-up
MECHANISM: Co-packaged optics at an est. ≤5 pJ/bit stretch a 72-chip all-to-all domain across three air-cooled racks of about 30 kW each. At 14.4 Tb/s per chip this adds about 72 W to a 1 kW chip budget. The closest earlier attempt is Google's optical-circuit-switched TPU pods, which keep electrical scale-up inside liquid-cooled cubes. Continuum-X makes the scale-up domain itself optical, so density no longer sets the domain size. The deciding quantity is the laser and module failure rate (FIT) at that bandwidth, which must cost less domain availability than copper NVL72 does.
VALUE: Allows NVL72-class MoE serving and training in existing 30–40 kW air-cooled halls, without the liquid-cooling retrofit that 120 kW racks need.