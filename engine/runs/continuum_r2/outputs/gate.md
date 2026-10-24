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
IDEA 5: Attention in HBM4 base die
KILLER | KV-read energy saved per bit by skipping the PHY and interposer (the TSV, row-activation and in-die movement energy is still paid) | required 2.4 pJ/b saved (the idea's 3.9 → 1.5) | available ~0.5 pJ/b (modeled HBM3e: I/O 0.25 pJ/b of 3.44 total, plus an assumed equal 0.25 on the host-side PHY) (arXiv 2602.18568, an analytical model checked against the reported 3.44 pJ/b) | MARGIN 0.21
CHAIN | GQA decode on HBM GPUs with an FP8/NVFP4 KV cache (Archetype C) | now 1.00 energy/token | with idea ~0.956 (15% saving × an estimated 30% KV share of decode energy at 16K) | RATIO 1.05
VERDICT | DEAD | Most of the cost of reading a bit is spent inside the DRAM stack, so skipping the interface saves ~15%, not the claimed 2×. The idea also adds 16 W of logic under a 12–16-high stack, and no source gives a thermal budget for that.
NEW FACT | Modeled HBM3e energy split: row activation 0.18 pJ/b (streaming), TSV 0.148 pJ/b per layer, I/O 0.25 pJ/b, 3.44 pJ/b total | https://arxiv.org/pdf/2602.18568
NEW FACT | Samsung's custom HBM (Hot Chips 2026) already replaces the HBM PHY with a logic die-to-die interface, so the cheap part of this saving is already being taken by vendors | https://www.servethehome.com/samsung-evolving-hbm-base-die-at-hot-chips-2026/
IDEA 6: Continuum-D: SRAM weights, LPDDR KV
KILLER | All-in hardware cost of 340 dies of 800 mm² at N3 with resident SRAM and 1 TB/s LPDDR each | required ≤ $1.5M | available ~$0.77M estimated (N3 wafer ~$19.5–20k, Silicon Analysts; ~65 gross dies at 75% yield gives ~$410/die; LPDDR at ~$12/GB from the Q2-2026 contract price of $145.9 per 12 GB, Utmel; package and system share assumed at $1.65k/die) | MARGIN 1.9
CHAIN | GB200 NVL72, disaggregated, DeepSeek-class model at ~100 tok/s/user (Archetype A) | now ~467k tok/s per rack, derived from the ledger's $0.06/Mtok at an assumed $1.4/GPU-hr owned TCO, against a rack BOM of ~$1.06M (72 × $6.4k plus an estimated $0.6M) | with idea ~800k tok/s at 8.5K context, KV-bandwidth-bound (35.1 KB/token MLA FP8 KV, 70% of 340 TB/s); hardware cost per throughput 0.42×, power per throughput 0.53× | RATIO 1.9
VERDICT | ALIVE | The numbers close with room to spare. 1 GiB of SRAM takes 258 mm² at N3E (31.8 Mib/mm²), and each die needs ~510 TFLOPS FP8 (MLA attention runs at ~484 FLOP/B), which fits in the remaining area. The open risks need a simulator or a real build: 1 TB/s of LPDDR shoreline per die (2× Grace), whole-instance failure when one die dies, the 2026 LPDDR shortage, and throughput falling ~4× at 32K context (~207k tok/s).
NEW FACT | N3E high-density SRAM bitcell is 0.021 µm², about 31.8 Mib/mm², with no shrink from N5. N2 reaches about 38 Mb/mm² | https://www.tomshardware.com/news/no-sram-scaling-implies-on-more-expensive-cpus-and-gpus
NEW FACT | LPDDR5X contract prices rose about 90% quarter on quarter in 1Q26, and part of the cause is Nvidia's own Grace/Vera LPDDR use. "Abundant commodity DRAM" is not a safe assumption | https://evertiq.com/news/2026-02-02-drampocalypse-memory-price-projections-skyrocket-for-1q26
NEW FACT | GB200 NVL72 rack price: about $3.1M alone, $3.9M all-in (SemiAnalysis, August 2025); Wolfe Research says ~$3M | https://www.wing.vc/content/how-much-does-an-nvidia-nvl72-cost
IDEA 7: Memory-light prefill compute die
KILLER | Prefill arithmetic intensity against the die's ridge point. The idea's 300 FLOP/B threshold is ~100× too low: a 30 PF FP4 die on 1 TB/s of LPDDR has a ridge of 30,000 FLOP/B | required ≥30,000 FLOP/B | available ~65,000 FLOP/B, but only with 16K-token chunks per die across 32-way expert parallelism (FP4 weights give 4 × tokens per expert); 8K-token single prompts give far less (Rubin CPX 30 PF NVFP4, The Register; the batch arithmetic is mine) | MARGIN 2.2 (conditional on very large prefill batches, which cost time-to-first-token)
CHAIN | Disaggregated HBM prefill on GB200 (Archetype A). Best near-term practice is Rubin CPX with GDDR7 | now 1.00 cost/token | with idea 0.80 (prefill ~30% of the fleet at 2–3× cheaper per FLOP; the claimed halving of HBM demand needs a prefill share of ≥50%, and Dynamo recipes show 1:1 worker ratios only in some configurations) | RATIO 1.2 against HBM prefill, ~1.0–1.05 against Rubin CPX
VERDICT | WOUNDED | It works physically if prefill runs in huge batches, but Rubin CPX already takes most of the gain, and the threshold the idea itself names is wrong by 100×.
NEW FACT | Rubin CPX: 30 PFLOPS NVFP4, 128 GB GDDR7 on a monolithic die, ~1.7–1.8 TB/s (inferred, not official), launching late 2026 in the Vera Rubin NVL144 CPX rack | https://www.theregister.com/2025/09/10/nvidia_rubin_cpx/
NEW FACT | Dynamo's DeepSeek V3.2 NVFP4 recipe on GB200 uses 2 prefill and 2 decode workers (DEP8, 32 GPUs) | https://docs.dynamo.nvidia.com/dynamo/recipes/deepseek-v3-2-nvfp4
IDEA 8: Continuum-T: HBM-lean training die
KILLER | Training throughput retained when HBM bandwidth per FLOP is halved | required ≥0.85 | available ~0.69 (a power-law fit to a simulation in which 16× more HBM bandwidth gave 4.5× throughput for GPT-1.8T on 8,192 GPUs; this is a model, not a measurement) (arXiv 2506.15006) | MARGIN 0.81
CHAIN | Rubin/B200-class 8-stack FP8/BF16 3D-parallel pretraining (Archetype B) | now 1.00 cost/run | with idea 1.28 at 0.69 retention, 1.10 at 0.85. Halving HBM saves only ~3% of chip price, because BOM is ~18% of price, HBM is 45% of BOM, and SoIC SRAM is added back; staff (33%) and networking get spread over fewer FLOPs | RATIO 0.78 (0.91 even if the 15% MFU target is met)
VERDICT | DEAD | Big GEMMs clear the ridge easily (8192³ at FP8 reaches 5,461 FLOP/B), but the memory-bound non-GEMM time sets the cost. Even at the target MFU, saving HBM cannot pay for lost throughput when HBM is ~8% of what the chip sells for.
NEW FACT | Non-GEMM operators took 40–55% of BERT training time (sources conflict for LLaMA-scale models, where one says <1%). Measurement with Nsight on B200 is needed before trusting either | https://arxiv.org/pdf/2104.08335
NEW FACT | Rubin's 22 TB/s over 8 HBM4 stacks is ~2.75 TB/s per stack, so 4 HBM4 stacks (~11 TB/s) already beat B200's 8 HBM3E stacks (8 TB/s). The idea's "half of B200" baseline is a generation behind | https://www.theregister.com/2025/09/10/nvidia_rubin_cpx/

Several inputs are my own estimates, not sourced:
- the 30% KV share of decode energy (Idea 1);
- the $1.65k per-die package and system share, the 75% SRAM-redundant yield, the $1.4/GPU-hr owned TCO and the $0.6M rest-of-rack BOM (Idea 2);
- the 30–50% prefill fleet share (Idea 3);
- the power-law fit through one simulated point (Idea 4).

The verdicts most sensitive to these are Idea 2's RATIO and Idea 4's MARGIN. Idea 2's verdict depends mainly on the per-die system cost, which needs a real BOM quote; Idea 4's needs the HBM down-clock run the idea itself proposes.

Files are in `/home/user/SomeRepository/engine/runs/continuum/gate/c2/` (nothing committed):
- gate_calc.py
- gate_calc_output.txt

Sources:
- [RPU, arXiv 2602.18568](https://arxiv.org/pdf/2602.18568)
- [ServeTheHome: Samsung HBM base die, Hot Chips 2026](https://www.servethehome.com/samsung-evolving-hbm-base-die-at-hot-chips-2026/)
- [Silicon Analysts wafer pricing](https://siliconanalysts.com/data/wafer-pricing)
- [Tom's Hardware: N3 SRAM](https://www.tomshardware.com/news/no-sram-scaling-implies-on-more-expensive-cpus-and-gpus)
- [Utmel: LPDDR5 2026](https://www.utmel.com/blog/categories/memory%20chip/lpddr5-memory-2026-lead-times-hbm-impact-and-procurement-strategies)
- [Evertiq: DRAM prices 1Q26](https://evertiq.com/news/2026-02-02-drampocalypse-memory-price-projections-skyrocket-for-1q26)
- [Wing VC: NVL72 cost](https://www.wing.vc/content/how-much-does-an-nvidia-nvl72-cost)
- [The Register: Rubin CPX](https://www.theregister.com/2025/09/10/nvidia_rubin_cpx/)
- [Dynamo DeepSeek V3.2 NVFP4 recipe](https://docs.dynamo.nvidia.com/dynamo/recipes/deepseek-v3-2-nvfp4)
- [arXiv 2506.15006](https://arxiv.org/pdf/2506.15006)
- [Demystifying BERT, arXiv 2104.08335](https://arxiv.org/pdf/2104.08335)
