=== GATE ===
IDEA 1: Continuum-P LPDDR prefill die
KILLER | Arithmetic intensity on expert weights during an 8K-token prefill chunk of a DeepSeek-class MoE (256 experts, top-8), measured against the die's roofline ridge. Each expert sees about 256 tokens per chunk, not 8K. The idea's figure of 16K FLOP/B holds only for dense models. | required 10,000 FLOP/B (10 PFLOPS ÷ 1 TB/s) | available 1,024 FLOP/B at FP4 and 512 at FP8 (exact arithmetic from the public DeepSeek-V3 routing config; the dense case reproduces the idea's 16,384 as a check) | MARGIN 0.10
CHAIN | GB200/Rubin-class disaggregated serving with Rubin CPX (30 PF NVFP4, 128 GB GDDR7, no CoWoS) as the prefill tier | now $711/PF of BOM (B200 at $6.4k for about 9 PF dense FP4; CPX is cheaper per PF still) | with idea about $386/PF (LPDDR at $10/GB means 256 GB costs $2,560, which alone exceeds the claimed $2.5k BOM; logic die and substrate add about $1.3k, est.). Accelerator BOM is only 8% of TCO, so the system gain is 1.04× against B200 and below 1 against CPX | RATIO 1.04
VERDICT | DEAD | On MoE models the 8K chunk sits 10× below the ridge, so 50% MFU needs about 51K-token prefill batches. The cheap memory now costs more than the whole claimed BOM, and Rubin CPX already ships the same no-CoWoS idea with 3× the compute.
NEW FACT | LPDDR5 contract prices were about $10/GB in mid-2026, roughly 3× Q1 2025. Long-term agreements run $7.8–21/GB. | https://wccftech.com/mobile-dram-prices-expected-to-increase-by-100-quarter-over-quarter-as-long-term-agreements-now-getting-signed-at-prices-as-high-as-21-gb/amp/
NEW FACT | Rubin CPX: 30 PF NVFP4 and 128 GB GDDR7 on a monolithic die, built for prefill. Per-chip bandwidth of about 1.8–2 TB/s is a third-party estimate, not a spec. | https://futurumgroup.com/insights/nvidias-new-rubin-cpx-targets-future-of-large-scale-inference/

IDEA 2: Continuum-T FP4 training mode
KILLER | Tokens-to-target-loss for NVFP4 against FP8 at 70B or more | required ≤1.10× FP8 tokens | available: no NVFP4 pretraining run above 12B is published. At 12B and 10T tokens the loss gap without promotion grows to about 1.5% at the end of training. On a Chinchilla fit that equals about 2.61× the tokens. With late-phase high precision the paper reports the gap mostly closes, but only at 12B (arXiv 2509.25149) | MARGIN 0.42 (unpromoted, 12B); about 1 with promotion at 12B, unmeasured at 70B
CHAIN | Frontier pretraining on Blackwell using the published NVFP4 recipe: about 16% of layers kept in BF16, late-phase switch to higher precision, hardware FP4 at 2× FP8 already in B200/B300 | now 1.00 (against plain FP8 the idea would reach 1.19×: GEMM time 0.656, step 1.32× faster, with staff's 33% fixed) | with idea about 1.00. The 2×-per-mm² gain already ships, and the hardware monitor only automates what the software recipe already does | RATIO 1.0
VERDICT | DEAD | Its throughput gain is already in shipping Blackwell silicon and recipes. The only new piece is automatic promotion, which adds about nothing to cost, and no evidence exists at 70B or more. Even against FP8 alone the ceiling is about 1.19×.
NEW FACT | The NVFP4 12B/10T run scored 62.58% on MMLU-Pro against 62.62% for FP8. Relative loss error is under 1% in the stable phase and above 1.5% during LR decay. The model is a hybrid Mamba-Transformer, not a plain transformer. | https://arxiv.org/html/2509.25149v2

IDEA 3: Expert-stationary stacked SRAM
KILLER | Rack SRAM capacity against the resident size of all expert weights. Assumes 64 chips × 4 layers × 800 mm² at AMD V-Cache density of 64 MB/36 mm² ≈ 1.78 MB/mm². | required 377 GB (DeepSeek-V3 671B at NVFP4, 4.5 bits/value) or 585 GB (Kimi K2 1.04T). The idea's 178 GB figure is too small for its stated model class. | available 364 GB (WikiChip V-Cache die area; the idea's 7 GB/chip needs about 2.2 MB/mm², which is not sourced) | MARGIN 0.96 (DeepSeek), 0.62 (Kimi K2)
CHAIN | GB200 NVL72 disaggregated MoE decode, where weight reads take 23–36% of decode time (earlier runs) | now 1.00 cost per token | with idea: decode time falls to 1/1.30–1/1.56. Prefill gains nothing, so with decode at about 70% of cost (est.) system cost falls to about 0.79. SRAM at $170/GB × 377 GB ≈ $64k per rack, about 2× the idea's $30k but still small | RATIO 1.27
VERDICT | WOUNDED | Capacity fits DeepSeek-V3 only with no headroom and misses trillion-parameter models by 1.6×. Even if every weight read is removed, the ceiling is about 1.27–1.34× system-wide, below the 1.5× bar. Thermal effects of 4-high stacking on a hot compute die and SoIC supply still need a simulator or silicon.
NEW FACT | AMD's 64 MB V-Cache die is 36 mm² (6×6 mm), hybrid-bonded with TSMC SoIC, with 15× the interconnect density of microbumps. | https://fuse.wikichip.org/?p=5531

IDEA 4: Commodity-DRAM air-cooled MoE decoder
KILLER | Memory cost per unit of bandwidth. Decode is bandwidth-bound, and 512 GB of LPDDR per chip forces you to pay for capacity in order to get bandwidth. Benchmark is Vera at 1.2 TB/s per 512 GB-class configuration. | required ≤$362 per TB/s (HBM3E: $2,900 for 8 TB/s, ledger D) | available $4,267 per TB/s (512 GB × $10/GB ÷ 1.2 TB/s; Vera bandwidth from Nvidia, price from SemiAnalysis via wccftech) | MARGIN 0.085
CHAIN | GB200 NVL72 MoE decode at 85–195 tok/s/user | now about $65k 4-year TCO per GPU (from $1.86/chip-hr) | with idea about $92k per HBM-bandwidth-equivalent. Air cooling is credited at 30% of the facility share. LPDDR at 3.65 pJ/bit (Vera: 30–40 W for 1.2 TB/s) saves no energy against HBM3E at 3.44 pJ/bit | RATIO 0.70
VERDICT | DEAD | Commodity DRAM is cheap per GB but about 12× dearer per TB/s, which is what decode buys. Energy per bit is the same as HBM. The idea's own deciding quantity, all-to-all time, is fine (about 0.16 ms against a 10 ms step) and does not rescue it.
NEW FACT | Vera supports up to 1.5 TB of LPDDR5X (8 SOCAMM2 modules, 9600 MT/s) at 1.2 TB/s, with the full memory subsystem drawing 30–40 W, which works out to about 3.6 pJ/bit. | https://www.digitalcitizen.life/nvidia-reveals-vera-cpu-architecture-with-88-olympus-cores-and-high-bandwidth-lpddr5x-memory/
NEW FACT | Reported HBM3E energy is 3.44 pJ/bit (RPU paper validation point); LLMET lists 5.74 pJ/bit. | https://arxiv.org/pdf/2602.18568

The arithmetic is in `/home/user/SomeRepository/engine/runs/continuum/gate/c1/gate_calc.py`, with output in `gate_calc.out` in the same folder. Nothing was committed.

Sources:
- [Futurum – Rubin CPX](https://futurumgroup.com/insights/nvidias-new-rubin-cpx-targets-future-of-large-scale-inference/)
- [TechRadar – Rubin CPX 128GB GDDR7](https://www.techradar.com/pro/nvidia-has-launched-a-gpu-with-128gb-of-gddr7-ram-but-yeah-theres-no-way-it-will-sell-one-to-us-to-run-games)
- [arXiv 2509.25149 – Pretraining LLMs with NVFP4](https://arxiv.org/html/2509.25149v2)
- [WikiChip – AMD 3D-stacked SRAM](https://fuse.wikichip.org/?p=5531)
- [Tom's Hardware – V-Cache at Hot Chips](https://tomshardware.com/news/amd-unveils-more-ryzen-3d-packaging-and-v-cache-details-at-hot-chips)
- [Power Systems Design – LPDDR6 bandwidth](https://www.powersystemsdesign.com/articles/lpddr6-bandwidth-math-what-you-gain-what-you-pay-what-you-measure/22/23664)
- [wccftech – mobile DRAM prices](https://wccftech.com/mobile-dram-prices-expected-to-increase-by-100-quarter-over-quarter-as-long-term-agreements-now-getting-signed-at-prices-as-high-as-21-gb/amp/)
- [Digital Citizen – Vera CPU LPDDR5X](https://www.digitalcitizen.life/nvidia-reveals-vera-cpu-architecture-with-88-olympus-cores-and-high-bandwidth-lpddr5x-memory/)
- [RPU paper arXiv 2602.18568](https://arxiv.org/pdf/2602.18568)
- [LLMET arXiv 2607.26491](https://arxiv.org/pdf/2607.26491)