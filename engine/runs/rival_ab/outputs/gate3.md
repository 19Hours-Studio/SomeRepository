=== GATE ===
IDEA 1: Continuum on-die speculative tree verifier
KILLER | accepted tokens per verify pass at T=1 on a frontier MoE target, with an EAGLE-3-class tree drafter | required 3.0 tokens/pass (the idea's own threshold for about 3x tok/s/user) | available 2.96 for Qwen3-235B-A22B, 2.53 for GPT-OSS-120B, 3.39 for Llama-3.1 with a KL-trained drafter (arXiv 2602.23881, MT-Bench, T=1, bs=1) | MARGIN 0.99 for the MoE case (0.84 for GPT-OSS-120B)
CHAIN | EAGLE-3 tree speculation already running on GPUs in SGLang/TRT-LLM, T=1 | now 1.84x speedup at τ=2.96 (Qwen3-235B, same source) | with idea at most about 2.7x: τ divided by about 1.1 for draft cost, with verify and sampling overhead set to zero by hardwiring. This is an upper bound and gets smaller at batch scale, where verifying 32–64 nodes makes decode compute-bound | RATIO 1.3 on tok/s/user (1.46 is the ceiling); less on whole-system $/token
VERDICT | WOUNDED | At T=1 acceptance only just reaches the required 3 tokens/pass, and today's GPU EAGLE-3 already gets most of the gain, so the hardware can recover only the overhead, not the claimed 3x.
NEW FACT | At T=1, EAGLE-3 speedups on large MoE targets are only 1.2–1.84x (GPT-OSS-120B 1.20x, Qwen3-235B 1.84x) | https://arxiv.org/pdf/2602.23881

IDEA 2: Continuum-T HBM-free tiled trainer
KILLER | whole-step FLOP/B needed to keep 5 PFLOPS FP8 fed from 32 LPDDR6 channels | required 4,069 FLOP/B. The idea's "2 TB/s" assumes about 64 GB/s per channel, but LPDDR6 delivers 38.4 GB/s per 24-bit channel at 14.4 Gbps, so 32 channels give 1.23 TB/s (SK Hynix, ISSCC 2026, via 36kr/hothardware) | available: expert-FFN fwd+dgrad+wgrad intensity for DeepSeek-V3 shapes (d=7168, f=2048), computed with 8K output tiles held on chip, is 4,001 FLOP/B at 8K or more tokens per expert per die and 2,688 at 2K. Wgrad is capped at 2df/(d+f)≈3,186 at any batch size. The tiling model returns exactly 8,192 on a square 8K GEMM (known-answer check passed) (gate_calc.py) | MARGIN 0.66 at realistic tokens per expert (0.98 at best), before counting attention-bwd, norm and optimizer traffic
CHAIN | B200/Rubin-class GPU with HBM and CoWoS, cost per effective FP8 PFLOP | now about $1.4k BOM per PF (B200: $6.4k / 4.5 PF, Epoch) | with idea about $1.5k per PF at peak and about $2.3k per PF at 0.66 utilization. Build-up: 512 GB LPDDR at about $10/GB (SemiAnalysis via wccftech) is $5.1k, more than B200's whole $2.9k of HBM; logic die plus SRAM stack plus substrate about $2.5k (est.). Hardware is 44% of the run and vendor margin sits on top, so the run-level change is about 1x | RATIO 0.6–1.0
VERDICT | DEAD | LPDDR6 delivers about 60% of the bandwidth the idea assumes, MoE GEMM intensity falls below what the die needs, and 2026 LPDDR prices make 512 GB of it cost more than the HBM it replaces.
NEW FACT | LPDDR6 is 38.4 GB/s usable per 24-bit chip at 14.4 Gbps (43.2 GB/s raw) | https://eu.36kr.com/en/p/3856607395959810
NEW FACT | LPDDR5 contract price is about $10/GB after a 3x rise since Q1 2025; long-term agreement bands run $7.8–21/GB | https://wccftech.com/mobile-dram-prices-expected-to-increase-by-100-quarter-over-quarter-as-long-term-agreements-now-getting-signed-at-prices-as-high-as-21-gb/amp/

IDEA 3: Two-tier exact sparse-KV decode
KILLER | LPDDR efficiency on random 656-B row gathers at 150 users per chip | required 61.5% (150 users × 4.1 GB/s ÷ 1 TB/s, from the idea's own numbers; the 40% threshold the idea states is too lax) | available about 93% from a bank-timing model (tRCD/tRP 18 ns, tFAW 20 ns, 16 banks, 5% refresh). The model reproduces the analytic tFAW bound for 32-B random reads (0.316 vs 0.317). A real controller would land at an estimated 75–90% (lpddr_gather.py) | MARGIN 1.5 (about 1.2 conservative). The tighter term is HBM: index keys use 7.8 of 8 TB/s, leaving about 0.2 TB/s for weights, which caps it at about 145 users
CHAIN | GB300 plus Grace LPDDR5X offload of the latent cache, with the indexer kept on the GPU. ESS (Baidu) does this for DeepSeek-V3.2 and reports +123% decode throughput at 128K, in simulation | now about 94 users per GPU at 128K (47 from HBM plus 240 GB of Grace memory ÷ 5.1 GB, needing about 193 GB/s of C2C) | with idea about 145 users per chip, with about $7.7k of extra LPDDR BOM per chip (about 10% more per-chip cost, est.) | RATIO 1.4
VERDICT | WOUNDED | The physics works with headroom, but Grace offload on today's GB300 already gets about 2x, so the dedicated silicon adds only about 1.4x, and the HBM bandwidth spent on index keys is nearly saturated.
NEW FACT | ESS already offloads the DeepSeek-V3.2 latent cache to CPU memory and reports +69.4% throughput at 32K and +123% at 128K (simulated) | https://arxiv.org/abs/2512.10576

IDEA 4: Weight-stationary stacked-SRAM tiles
KILLER | decode tokens per facility kW at 8K context, which the 80-tile LPDDR6 KV bandwidth limits. MLA KV is 656 B × 61 layers × 8K = 328 MB read per token, so 10⁵ tok/s already needs about 0.41 TB/s of LPDDR per tile | required about 20,000 tok/s/kW for the claimed 3x | available 3,125 tok/s/kW (10⁵ tok/s ÷ 32 kW, the idea's own figures and chip power only), against GB300 NVL72 at 6,685 tok/s/kW (12,534 tok/s/chip × 72 ÷ about 135 kW, DeepSeek-R1 FP4 8K/1K disaggregated at 93 tok/s/user, InferenceX via Packet.ai) | MARGIN 0.16
CHAIN | GB300 NVL72 disaggregated serving of DeepSeek-R1 FP4 at 8K/1K, energy per token | now 0.150 J/token (1/6,685 per kW) | with idea 0.32 J/token | RATIO 0.47
VERDICT | DEAD | Moving the KV cache from HBM (about 576 TB/s per NVL72) to LPDDR (about 40 TB/s for 80 tiles) caps throughput below today's GPU racks, so the claimed 1.5–3x per joule or per kW is actually about a 2x loss. Stacked-SRAM cost per GB doesn't matter until this is fixed.
NEW FACT | GB300 NVL72 runs DeepSeek-R1 FP4 8K/1K disaggregated at 12,534 tok/s/chip at 93 tok/s/user and 5,394 at 162 tok/s/user (interpolated InferenceX data) | https://packet.ai/blog/gb300-vs-gb200-nvl72
NEW FACT | TSMC SoIC capacity is about 10–15k wafers/month in 2026, at an estimated $6.8–7.0B of capex per 10k wafers/month, more than CoWoS | https://www.trendforce.com/news/?p=54678

The scripts `gate_calc.py` and `lpddr_gather.py` are in `/home/user/SomeRepository/engine/runs/rival_ab/gate/c3/`; nothing was committed. Three inputs here are my own estimates, and a simulator or silicon would be needed to pin them down: the real LPDDR controller efficiency, the die and SRAM-stack BOM, and the 135 kW GB300 rack power.

Sources:
- [LK Losses, arXiv 2602.23881](https://arxiv.org/pdf/2602.23881)
- [36kr on LPDDR6](https://eu.36kr.com/en/p/3856607395959810)
- [HotHardware on JEDEC LPDDR6](https://hothardware.com/news/jedec-ddr6-lpddr6-revealed)
- [wccftech on LPDDR pricing](https://wccftech.com/mobile-dram-prices-expected-to-increase-by-100-quarter-over-quarter-as-long-term-agreements-now-getting-signed-at-prices-as-high-as-21-gb/amp/)
- [ESS, arXiv 2512.10576](https://arxiv.org/abs/2512.10576)
- [TensorRT-LLM DeepSeek-V3.2 blog](https://nvidia.github.io/TensorRT-LLM/1.2.1/blogs/tech_blog/blog15_Optimizing_DeepSeek_V32_on_NVIDIA_Blackwell_GPUs.html)
- [Packet.ai, GB300 vs GB200](https://packet.ai/blog/gb300-vs-gb200-nvl72)
- [InferenceX, GB300 vs MI355X](https://inferencex.semianalysis.com/compare/deepseek-r1-gb300-vs-mi355x)
- [TrendForce on SoIC](https://www.trendforce.com/news/?p=54678)
- [Tom's Hardware on hybrid bonding](https://tomshardware.com/tech-industry/semiconductors/hybrid-bonding-roadmap-examined)