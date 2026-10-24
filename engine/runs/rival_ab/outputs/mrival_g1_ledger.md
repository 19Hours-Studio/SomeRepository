# Continuum: three variants, each aimed at one cost term

**Metrics:** joules per token at 16K context, tokens/s per user, $ per million tokens, and training time-to-loss at equal cost. Competitor figures below are vendor-reported (R): Rubin ~288 GB HBM4 at ~22 TB/s; Ironwood 192 GB at 7.4 TB/s; WSE-3 44 GB SRAM; Groq 230 MB. Everything else is my estimate (E).

**Software (all variants):** PyTorch through a torch.compile → MLIR/Triton backend. Unmodified checkpoints load via FP8/MXFP4 quantization. The bet is no new language, because software is what stopped Gaudi and Graphcore.

**1. Continuum-D (decode energy, Archetype C).**
- **Design:** DRAM is hybrid-bonded directly on the logic die. That gives 24 GB per chip (E) at about 1.5 pJ/bit, versus about 4–5 pJ/bit for HBM3E (E, literature range).
- **Scale:** 72 chips hold 1.7 TB, enough for a 1T-parameter FP4 model (0.5 TB) plus KV cache.
- **Energy check:** 242 mJ/token (R, 16K context) × 50% data-movement share = 121 mJ. Cutting that 3× saves about 81 mJ, leaving about 161 mJ/token. That is **about 1.5× tokens/J, not 10×.**
- **Where it loses:** it trails on capacity per dollar.
- **Deciding quantity:** retention and refresh power of DRAM sitting above 90 °C logic.

**2. Continuum-L (BOM and supply, Archetype D).**
- **Design:** no HBM and no CoWoS. Each package has LPDDR6 on an organic substrate, 512 GB at about 1.1 TB/s (E), plus 512 MB of SRAM for activations.
- **Cost check:** HBM is about $16–25/GB (E, from $550–600 per stack); LPDDR is about $4/GB (E). That cuts the HBM-plus-packaging share of BOM (62%) by about 3×, for **about 1.7× BOM.**
- **Where it loses:** tokens/s per user is about 20× worse than Rubin, so it is a prefill and high-batch tier only.
- **Overall effect:** it does not move Archetype A total cost of ownership much (silicon is 8%). It moves supply.

**3. Continuum-T (training, Archetype B).**
- **Design:** dense MXFP4/NVFP4 tensor arrays with FP8 fallback per layer, and a 512-chip co-packaged-optics scale-up.
- **Cost check:** a 2× perf/$ gain on the hardware share (44%) gives **1.28× run cost.** Staff cost sets the floor.

**Verdict.** No single variant is "best overall." Continuum-D can credibly lead on tokens/J for long-context decode. Rubin keeps leading on peak throughput per chip and on software maturity.

=== IDEAS ===
IDEA 1
NAME: Bonded-DRAM decode chip
MECHANISM: DRAM layers are hybrid-bonded directly onto a logic die, giving 24 GB per chip at about 1.5 pJ/bit against about 4–5 pJ/bit for HBM. Weights are sharded across 72 chips, and the KV cache stays local, so decode never crosses a PHY. The closest earlier attempt, HBM-PIM, stalled on programmability; this design exposes plain memory, not in-memory logic. The deciding quantity is DRAM refresh power when the DRAM sits above logic hotter than 90 °C.
VALUE: About 1.5× tokens per joule on 16K-context decode, falsified if a test chip measures more than 2.5 pJ/bit end to end.

IDEA 2
NAME: HBM-free LPDDR capacity accelerator
MECHANISM: LPDDR6 (512 GB, about 1.1 TB/s) sits on an organic substrate with no CoWoS, and 512 MB of SRAM holds activations for batched MoE prefill. The closest earlier attempt, Groq, ran out of SRAM capacity; here bulk capacity lives in cheap DRAM. The deciding quantity is whether the batched expert arithmetic intensity stays above about 900 FLOP/B.
VALUE: Roughly 1.7× lower BOM, built from memory and packaging supply that is not sold out.

IDEA 3
NAME: FP4-native optical training pod
MECHANISM: Dense MXFP4/NVFP4 tensor arrays fall back to FP8 for sensitive layers, selected by a per-layer gradient-noise monitor, across 512 chips joined by co-packaged optics. The closest earlier attempt, NVFP4, is proven only to 12B parameters. The deciding test is a 70B model trained on 1T tokens, finishing within 1% of FP8 loss.
VALUE: About 1.28× cheaper frontier runs, falsifiable before tape-out by simulating FP4 numerics on existing GPUs.