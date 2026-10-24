# Continuum: three decode-first architectures

**Target and metric.** The target is data-center inference of large MoE models. The metrics are joules per token and dollars per million tokens, both measured at 50 tok/s per user or more. These terms carry most of the cost: in the estimated shares, HBM movement is about 50% of decode energy and HBM plus packaging is about 62% of chip BOM. Training is out of scope, because staff cost (33%) caps what any chip can save there.

**The 8 conventional answers.** These are what I and most experts would propose first:
1. More HBM4 stacks.
2. A bigger CoWoS interposer.
3. FP4 tensor cores.
4. Larger SRAM.
5. Wafer-scale integration.
6. NVL-style rack scale-up.
7. Optical scale-out.
8. A transformer-only ASIC.

They share one paradigm: keep weights and KV in an external memory tier and buy more bandwidth or compute to stream them faster.

**Facts vs. assumptions.** Established facts are decode being memory-bound, HBM and CoWoS supply limits, and 107 mJ/token at 4K context. My assumptions are tagged (A).

## Roofline checks

**DRAM-on-logic (Idea 1).**
- Half of 107 mJ is about 53 mJ of memory movement.
- A 4x lower pJ/bit (A) saves about 40 mJ, giving 67 mJ/token. That is about **1.6x better**, not 10x.

**Commodity-DRAM decode (Idea 2).**
- A 32B-active MoE at FP4 reads about 16 GB per step.
- Eight chips at 0.5 TB/s each (A) give 4 TB/s, or about 250 steps/s. That supports 250 tok/s per user, and batching does not lower it.
- Against an HBM GPU at about 8 TB/s per chip, Continuum loses about 16x per chip on bandwidth.
- It wins on capacity per dollar and on not needing HBM or CoWoS.
- A 2x cost gain is within reach: the facility (20%) plus the silicon, HBM and packaging share (8%) leave the room.

**Where it loses.** It is worse than GPUs at pretraining. It is worse than Groq or Cerebras on single-user latency for models that fit in SRAM. Ironwood and Rubin specifications are unverified, so no head-to-head claim is made against them.

**Falsification plan.**
- Build a trace-driven simulator from measured vLLM decode traces and validate it first against H100's reported 27%-of-peak bandwidth result.
- Kill Idea 1 if bonded DRAM exceeds 1.5 pJ/bit, or if DRAM at the junction temperature needs more than 2x refresh.
- Kill Idea 2 if the all-to-all at 64 KB/token/layer exceeds 30% of link time.

**Software.** PyTorch runs through torch.compile, with a single MLIR backend shared by all dies. Existing models run unmodified. Kernels are vendor-written, which matters because software is what killed Gaudi and Graphcore.

=== IDEAS ===
IDEA 1
NAME: Hybrid-bonded DRAM-over-MAC decode die
MECHANISM: DRAM layers are hybrid-bonded directly over a logic die, so weights and KV stay stationary within micrometres of the GEMV units, and the compiler sees the bank-edge matmul as an ordinary tensor op. The closest earlier attempt is HBM-PIM, which stalled on programmability and DRAM-process logic. Here the logic sits on a logic-process die and is exposed only through a standard compiler path. The deciding quantity is delivered pJ/bit at the junction temperature, including refresh.
VALUE: About 1.6x lower decode energy per token without any HBM supply.

IDEA 2
NAME: Commodity-DRAM air-cooled MoE decoder
MECHANISM: Each chip carries about 512 GB of LPDDR-class DRAM (A) on an organic substrate, holds fixed experts locally, and moves activations instead of weights. The rack stays at or below 40 kW, which allows air cooling. The closest earlier attempts are Groq and Cerebras, whose SRAM capacity forced hundreds of chips or off-wafer streaming; capacity here comes from commodity DRAM. The deciding quantity is all-to-all link time per token relative to DRAM read time.
VALUE: MoE decode on standard packaging in existing air-cooled halls, at an estimated 2x lower cost per token.

IDEA 3
NAME: Memory-light prefill compute die
MECHANISM: A dense FP4/FP8 compute die with only LPDDR runs the compute-bound prefill phase. It hands KV to the decode tier over a fabric and shares an ISA and compiler with that tier. The closest earlier attempt is Nvidia's Rubin CPX, which uses a separate GDDR7 stack. This design avoids GDDR shortages and keeps a single toolchain across both phases. The deciding quantity is prefill FLOP/byte, which must stay above about 300.
VALUE: Takes prefill off scarce HBM and CoWoS, roughly halving HBM demand per served token (A).