# Continuum: three candidate architectures for 2027–28

**Scope.** "Best" here means delivered tokens (or training FLOPs) per binding scarce input: per HBM stack, per CoWoS wafer, and per facility kW. Inference archetypes A and C hold most of the cost an architecture can touch. In training (B), staff cost is a floor of about 33%, so a better chip can save at most about 2–2.5x there.

**Facts versus estimates.** These are treated as established:
- SRAM costs about 0.1 pJ/bit to read.
- HBM costs about 3–5 pJ/bit.
- Cerebras gets about 1 MB/mm² of wafer SRAM.

The decode share is not established. ARCHETYPE C's 50% is the asker's own estimate and is unverified. All Continuum figures below are my estimates.

**Software.** Every option ships as a vLLM/SGLang and torch.compile backend, so existing checkpoints run unmodified. That is the lesson from Gaudi and Graphcore.

**Falsification.** Each idea names one deciding quantity, and that quantity can be measured before tape-out.

=== IDEAS ===

IDEA 1
NAME: Continuum-D: SRAM weights, LPDDR KV
MECHANISM: A FP4 671B-parameter MoE (about 335 GB) sits resident in SRAM across about 340 standard-packaged, CoWoS-free dies of about 800 mm² each, with roughly 1 GB per die. Weight reads cost no HBM and about 40x less energy. The KV cache, which is about 2.2 GB per 32K-token MLA user, lives in commodity LPDDR6 at about 1 TB/s per die. The closest earlier attempt is Groq, which needed 576 chips for one 70B model because it put everything in SRAM. Continuum-D avoids this because the weights are shared across a large MoE batch, and the per-user KV goes to cheap, abundant DRAM instead of SRAM. The deciding quantity is SRAM cost per GB of resident weights versus HBM-rack cost per GB/s of weight traffic. It fails if 340 dies cost more than about $1.5M.

VALUE: It delivers high tok/s per user on frontier MoE models with zero HBM stacks and zero CoWoS wafers, which bypasses the 2026–28 supply limits that cap every GPU and TPU.

IDEA 2
NAME: Continuum-T: HBM-lean training die
MECHANISM: A training die carries 4 HBM4 stacks instead of 8 and adds 3D-stacked SRAM (SoIC) for GEMM tiles. Optimizer state and activations are sharded over the fabric in ZeRO style. The bet is that large training GEMMs exceed about 560 FLOP/B, so they do not need B200-class HBM bandwidth. The closest earlier attempt is TPU Ironwood, which still provisions 8 stacks. The deciding quantity is achieved MFU when HBM bandwidth per FLOP is halved. This can be tested today by down-clocking HBM on B200s during a 10B+ parameter run.

VALUE: It gives about 1.6–2x the training throughput per HBM stack, which makes it the best FLOP-per-scarce-input design if MFU falls by less than 15%.

IDEA 3
NAME: Continuum-K: attention on HBM base-die
MECHANISM: Fixed-function attention units on the custom HBM4 base die read the KV cache over TSVs. Only the query vectors in and the attention outputs back cross the PHY, which is kilobytes instead of gigabytes per step. The closest earlier attempts are Samsung HBM-PIM and UPMEM, which died on general programmability. Continuum-K exposes exactly one kernel that the compiler emits, so programmability is not required. The deciding quantity is the PHY's share of HBM read energy. If it is about 50%, decode energy falls only about 1.3x.

VALUE: It cuts long-context decode joules per token and lifts the KV-limited batch per facility kW, but the gain is likely about 1.2–1.5x, not several-fold.