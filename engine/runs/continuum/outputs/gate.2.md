=== GATE ===
IDEA 1: Attention in HBM4 base die
KILLER | KV-read energy saved per bit by skipping the PHY and interposer (the TSV, row-activation and in-die movement energy is still paid) | required 2.4 pJ/b saved (the idea's 3.9 → 1.5) | available ~0.5 pJ/b (modeled HBM3e: I/O 0.25 pJ/b of 3.44 total, plus an assumed equal 0.25 on the host-side PHY) (arXiv 2602.18568, an analytical model checked against the reported 3.44 pJ/b) | MARGIN 0.21
CHAIN | GQA decode on HBM GPUs with an FP8/NVFP4 KV cache (Archetype C) | now 1.00 energy/token | with idea ~0.956 (15% saving × an estimated 30% KV share of decode energy at 16K) | RATIO 1.05
VERDICT | DEAD | Most of the cost of reading a bit is spent inside the DRAM stack, so skipping the interface saves ~15%, not the claimed 2×. The idea also adds 16 W of logic under a 12–16-high stack, and no source gives a thermal budget for that.
NEW FACT | Modeled HBM3e energy split: row activation 0.18 pJ/b (streaming), TSV 0.148 pJ/b per layer, I/O 0.25 pJ/b, 3.44 pJ/b total | https://arxiv.org/pdf/2602.18568
NEW FACT | Samsung's custom HBM (Hot Chips 2026) already replaces the HBM PHY with a logic die-to-die interface, so the cheap part of this saving is already being taken by vendors | https://www.servethehome.com/samsung-evolving-hbm-base-die-at-hot-chips-2026/

IDEA 2: Continuum-D: SRAM weights, LPDDR KV
KILLER | All-in hardware cost of 340 dies of 800 mm² at N3 with resident SRAM and 1 TB/s LPDDR each | required ≤ $1.5M | available ~$0.77M estimated (N3 wafer ~$19.5–20k, Silicon Analysts; ~65 gross dies at 75% yield gives ~$410/die; LPDDR at ~$12/GB from the Q2-2026 contract price of $145.9 per 12 GB, Utmel; package and system share assumed at $1.65k/die) | MARGIN 1.9
CHAIN | GB200 NVL72, disaggregated, DeepSeek-class model at ~100 tok/s/user (Archetype A) | now ~467k tok/s per rack, derived from the ledger's $0.06/Mtok at an assumed $1.4/GPU-hr owned TCO, against a rack BOM of ~$1.06M (72 × $6.4k plus an estimated $0.6M) | with idea ~800k tok/s at 8.5K context, KV-bandwidth-bound (35.1 KB/token MLA FP8 KV, 70% of 340 TB/s); hardware cost per throughput 0.42×, power per throughput 0.53× | RATIO 1.9
VERDICT | ALIVE | The numbers close with room to spare. 1 GiB of SRAM takes 258 mm² at N3E (31.8 Mib/mm²), and each die needs ~510 TFLOPS FP8 (MLA attention runs at ~484 FLOP/B), which fits in the remaining area. The open risks need a simulator or a real build: 1 TB/s of LPDDR shoreline per die (2× Grace), whole-instance failure when one die dies, the 2026 LPDDR shortage, and throughput falling ~4× at 32K context (~207k tok/s).
NEW FACT | N3E high-density SRAM bitcell is 0.021 µm², about 31.8 Mib/mm², with no shrink from N5. N2 reaches about 38 Mb/mm² | https://www.tomshardware.com/news/no-sram-scaling-implies-on-more-expensive-cpus-and-gpus
NEW FACT | LPDDR5X contract prices rose about 90% quarter on quarter in 1Q26, and part of the cause is Nvidia's own Grace/Vera LPDDR use. "Abundant commodity DRAM" is not a safe assumption | https://evertiq.com/news/2026-02-02-drampocalypse-memory-price-projections-skyrocket-for-1q26
NEW FACT | GB200 NVL72 rack price: about $3.1M alone, $3.9M all-in (SemiAnalysis, August 2025); Wolfe Research says ~$3M | https://www.wing.vc/content/how-much-does-an-nvidia-nvl72-cost

IDEA 3: Memory-light prefill compute die
KILLER | Prefill arithmetic intensity against the die's ridge point. The idea's 300 FLOP/B threshold is ~100× too low: a 30 PF FP4 die on 1 TB/s of LPDDR has a ridge of 30,000 FLOP/B | required ≥30,000 FLOP/B | available ~65,000 FLOP/B, but only with 16K-token chunks per die across 32-way expert parallelism (FP4 weights give 4 × tokens per expert); 8K-token single prompts give far less (Rubin CPX 30 PF NVFP4, The Register; the batch arithmetic is mine) | MARGIN 2.2 (conditional on very large prefill batches, which cost time-to-first-token)
CHAIN | Disaggregated HBM prefill on GB200 (Archetype A). Best near-term practice is Rubin CPX with GDDR7 | now 1.00 cost/token | with idea 0.80 (prefill ~30% of the fleet at 2–3× cheaper per FLOP; the claimed halving of HBM demand needs a prefill share of ≥50%, and Dynamo recipes show 1:1 worker ratios only in some configurations) | RATIO 1.2 against HBM prefill, ~1.0–1.05 against Rubin CPX
VERDICT | WOUNDED | It works physically if prefill runs in huge batches, but Rubin CPX already takes most of the gain, and the threshold the idea itself names is wrong by 100×.
NEW FACT | Rubin CPX: 30 PFLOPS NVFP4, 128 GB GDDR7 on a monolithic die, ~1.7–1.8 TB/s (inferred, not official), launching late 2026 in the Vera Rubin NVL144 CPX rack | https://www.theregister.com/2025/09/10/nvidia_rubin_cpx/
NEW FACT | Dynamo's DeepSeek V3.2 NVFP4 recipe on GB200 uses 2 prefill and 2 decode workers (DEP8, 32 GPUs) | https://docs.dynamo.nvidia.com/dynamo/recipes/deepseek-v3-2-nvfp4

IDEA 4: Continuum-T: HBM-lean training die
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