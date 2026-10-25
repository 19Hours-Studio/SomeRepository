=== GATE ===
IDEA 1: N6 SRAM-chiplet pipeline packages
KILLER | delivered system $ per GB of SRAM, which depends on how many MB fit on a ~100 mm² N6 die | required ≤1,500 $/GB. The idea's own plan of 112 GB on 512 dies needs 17.5 Mb/mm² over the whole die. | available ≈1,580 $/GB owner-built. The best shipped pure-SRAM die is AMD V-Cache on N7 at 14.2 Mb/mm², so the design needs about 700 dies in 22 packages. The silicon costs about $17 per die, assuming a $10k wafer, 640 dies per wafer and 90% yield. Per package I estimated about $7.5k for substrate, assembly, board, VRM, cooling and a share of host and network; that figure is mine, not sourced. A 2x vendor markup would raise this to about $3k/GB. (AMD V-Cache 64 MB in 36 mm², per WikiChip/TechPowerUp; wafer price from TSMC N3/N4 reporting scaled down to N6; my bottom-up estimate) | MARGIN 0.95
CHAIN | Cerebras CS-3 serving 70B at about 2,000 tok/s/user, owner cost. I assumed 4 CS-3 at about $2.5M each and about 30 concurrent users at 8K context. | now ≈1.4 $/Mtok | with idea ≈0.05–0.08 $/Mtok. That assumes about 31 users at 8K context with FP8 KV, at 1,000 tok/s/user. | RATIO ≈20. Against GB300 at 50 tok/s the ratio is about 1, but the idea is 20x faster per user.
VERDICT | WOUNDED | The economics are sound if built at cost, but the claim relies on SRAM density about 25% above any shipped pure-SRAM die, and a vendor markup would push it past the $1.5k/GB limit.
NEW FACT | AMD's 64 MB V-Cache die is about 36 mm² on N7 (41 mm² in the first generation), which is about 14.2 Mb/mm² for a dense SRAM-only die | https://www.techpowerup.com/292256/amd-details-its-3d-v-cache-design-at-isscc
NEW FACT | Third-party estimates put a CS-3 at about $2–3M per unit, or about $3.2M and up to $4M with MemoryX and SwarmX. That is about $57k per GB of SRAM. | https://www.nextplatform.com/2024/03/14/cerebras-goes-hyperscale-with-third-gen-waferscale-supercomputers/
IDEA 2: 4.5-bit numerics, compiler-placed memory, kill gates
KILLER | peak temperature of DRAM stacked on a roughly 2 kW logic die. The idea's own gate is DRAM ≤95 °C. | required temperature rise ≤60 °C above 35 °C coolant | available: imec measured 141.7 °C for a baseline 3D HBM-on-GPU stack, which is a 106.7 °C rise. Mitigation reached 70.8 °C only with measures that included halving the clock, which cost about 28% of training speed. (imec, IEDM 2025) | MARGIN 0.56
CHAIN | Blackwell/Rubin already serve with NVFP4 weights and KV, FP8 activations and FP32 accumulation through vLLM/SGLang | now 1.0 (relative cost per token) | with idea ≈1.0. The numerics and software stack are current practice, and any gain depends on the stacked DRAM that fails the thermal limit. | RATIO ≈1.0
VERDICT | DEAD | The parts that work are what incumbents already do, and the one new part, logic-on-DRAM at 2 kW, fails its own 95 °C gate by about 2x in rise above coolant.
NEW FACT | imec's 3D HBM-on-GPU study measured a 141.7 °C peak against 69.1 °C for the 2.5D layout. Halving the GPU clock was needed to get below 100 °C and cost 28% of training speed. | https://imec-publications.be/handle/20.500.12860/60081 ; https://www.eenewseurope.com/en/imec-tackles-thermal-limits-in-3d-hbm-on-gpu-architectures
IDEA 3: Hash-Regenerated Trellis Weight Decoder
KILLER | quality loss at about 2 bits per weight. The idea's stated deciding quantity was decode energy; I chose quality instead because it fails first at the scale the idea needs. | required WikiText-2 perplexity gap ≤ about 2%, which is the loss level of NVFP4/FP8 deployment. | available: QTIP 2-bit on Llama-2-70B scores 3.78 against 3.12 for FP16, a 21% gap. That is the best published trellis result, and Llama-3-class models quantize worse. (third-party table, arXiv 2510.20984) | MARGIN ≈0.1
CHAIN | NVFP4 weights at 4.5 bits, which is current practice, not the FP8 the idea compares against | now 1.0 | with idea: decode is 1.24x faster on HBM, assuming weight reads are 36% of decode time and bits fall from 4.5 to 2.1. On SRAM-resident systems, silicon cost falls about 1.47x. The claimed 4x only holds against FP8. | RATIO ≈1.25–1.47
VERDICT | DEAD | At 2 bits per weight, quality falls about 10x below what production serving accepts. Measured against FP4 rather than FP8, the gain is under 1.5x. QTIP's own computed codes already regenerate the codebook without storing a table.
NEW FACT | On 2-bit Llama-2-70B, WikiText-2 perplexity is 3.78 for QTIP and 3.91 for QuIP#, against 3.12 for FP16 | https://arxiv.org/pdf/2510.20984
IDEA 4: Stacked-SRAM weights, HBM-only KV package
KILLER | SRAM capacity per package for pinning 545 GB of weights in a 144-package domain | required ≥3.8 GB per package (545 GB / 144) | available ≈2.1 GB per package. That uses the best shipped hybrid-bonded SRAM, AMD V-Cache at 14.2 Mb/mm², not the 30 Mb/mm² the idea assumes, with 75% array efficiency over 2×800 mm². The weights would then need 256 packages, not 136. (AMD V-Cache density, as for Idea 1) | MARGIN 0.56
CHAIN | Rubin NVL72/144 cost per token at interactive speeds | now 1.0 | with idea: the idea's own throughput-per-MW ratios of 1.12–1.58x, divided by the 10–15% higher capex it admits, give a net 1.0–1.4x. That is before the capacity shortfall forces more packages. | RATIO ≈1.2
VERDICT | WOUNDED | The bandwidth split is a sound idea, but SRAM density is about 2x short. That breaks the 144-package fit and leaves at most 1.2x net cost gain.

The QTIP 3.78 and FP16 3.12 numbers come from a third-party table, and I did not check that both used the same context length. I also found no N6/N7 wafer price, so the $10k figure comes from scaling down the N3/N4 reports.

Sources:
- [imec IEDM 2025 abstract](https://imec-publications.be/handle/20.500.12860/60081)
- [eeNews Europe on imec 3D HBM-on-GPU](https://www.eenewseurope.com/en/imec-tackles-thermal-limits-in-3d-hbm-on-gpu-architectures)
- [GLVQ paper, arXiv 2510.20984](https://arxiv.org/pdf/2510.20984)
- [QTIP, arXiv 2406.11235](https://arxiv.org/pdf/2406.11235)
- [TechPowerUp ISSCC V-Cache](https://www.techpowerup.com/292256/amd-details-its-3d-v-cache-design-at-isscc)
- [WikiChip on AMD 3D SRAM](https://fuse.wikichip.org/?p=5531)
- [Next Platform CS-3](https://www.nextplatform.com/2024/03/14/cerebras-goes-hyperscale-with-third-gen-waferscale-supercomputers/)
- [Notebookcheck 3nm wafer cost](https://www.notebookcheck.net/TSMC-3nm-wafer-costs-surge-to-18-000.943017.0.html)
- [TechNode 2nm wafer price](https://technode.com/2025/10/09/tsmc-sets-2nm-wafer-price-at-30000-far-below-earlier-50-increase-speculation/)
- [Next Platform on Groq 576-chip system](https://www.nextplatform.com/2023/11/27/groq-says-it-can-deploy-1-million-ai-inference-chips-in-two-years/)
IDEA 5: Latent KV With Outlier Sidecar
KILLER | KV compression versus FP16 reached at ≤1% accuracy loss at 128K context | required 6–8× (7× midpoint) | available ≈6.2× at <1–2% LongBench loss, tested only up to 32K. This combines Palu's 30% low-rank cut and 3-bit latents with a 1% FP16 outlier sidecar; at a 50% rank cut Palu "struggles" on accuracy. No 128K data exists (Palu, ICLR 2025, arXiv 2407.21118; my arithmetic) | MARGIN 0.89
CHAIN | NVFP4 KV at 4.5 bits (3.56× vs FP16) on a Blackwell/Rubin GPU, with KV reads at 25–35% of decode time at 128K | now 1.00 step time | with idea 0.86–0.89 step time (KV only 1.73× smaller than NVFP4). On MLA models, whose KV is already a latent, the gain is about 0 | RATIO 1.14
VERDICT | WOUNDED | It is physically fine, but it buys only 1.7× on KV over NVFP4, which is about 1.12–1.17× on the whole system, and its accuracy at 128K has never been measured.
NEW FACT | Palu: a 30% low-rank cut loses under 1% average on LongBench; 3-bit latents add under 1% more; 11.4× total compression "while maintaining perplexity"; tests went only up to 32K | https://arxiv.org/html/2407.21118v2
IDEA 6: Near-HBM sparse-KV gather attention engine
KILLER | heat from about 10 PF FP8 of logic in the HBM4 base dies, which sit under the DRAM | required ≈2.2 kW in total, ≈278 W per stack × 8 stacks. This uses 0.22 pJ/FLOP, taken from B200's 4.5 PF dense FP8 at about 1 kW | available ≈60 W per base die. That is my estimate: about 0.5 W/mm² × about 120 mm². imec found that GPU-class logic under 12-high hybrid-bonded HBM reached 141.7 °C, and getting it to 70.8 °C took removing the base die, double-sided cooling and frequency scaling (imec, IEDM 2025) | MARGIN 0.22
CHAIN | Rubin running the same DeepSeek-style sparse attention (DSA) model on its main arrays. Sparse decode needs only 166 GFLOP per user-token on 0.62 GB, about 269 FLOP/B, so 5.9 PF at 22 TB/s, and Rubin's main compute covers that. The traffic is 93% sequential index scan and only 6.6% gather, so the gather risk does not matter. Both chips are bound by the same HBM bandwidth. The only gain left is the interposer-hop energy, and energy is about 9% of TCO | now 1.00 $/Mtok | with idea ≈0.95 $/Mtok | RATIO 1.05
VERDICT | DEAD | The 3.7× comes from the sparse model, which incumbents also run. The near-HBM engine is sized for dense intensity (450 FLOP/B) and cannot be cooled under DRAM, and with the bandwidth unchanged it barely changes $/Mtok.
NEW FACT | vLLM's FP8 MLA KV layout for DeepSeek-V3.2 is 656 bytes per token per layer, and the indexer K-cache is a separate buffer; top-k = 2048 in the released code | https://vllm.ai/blog/2025-09-29-deepseek-v3-2
NEW FACT | imec IEDM 2025: 4 stacks of 12-high hybrid-bonded HBM placed on a GPU push the GPU peak from 141.7 °C down to 70.8 °C only with mitigations | https://bits-chips.com/article/imec-halves-peak-temperatures-in-3d-hbm-on-gpu-ai-chips/
IDEA 7: Hybrid-bonded DRAM-on-logic decode package
KILLER | hybrid-bonded DRAM capacity per package at 64 TB/s, which needs 0.20 Gb/mm² per DRAM die and 50 GB/s/Gb | required 160 GB at 64 TB/s and ≤1 pJ/bit | available ≥80 GB from 4-layer stacks, which Helios' industry collaborators call mature (arXiv 2603.04797). Bandwidth is not the limit: SeDRAM shows 135 GB/s/Gb at 0.66 pJ/b (UniIC, VLSI 2023), 2.7× the need. But 0.66–0.88 pJ/b is the interface figure, not the whole access. At 1.5–2 pJ/b the DRAM would draw 770–1,020 W of the 2 kW budget | MARGIN 0.5
CHAIN | Rubin, 288 GB at 22 TB/s and about 1.8 kW, serving a 1T/32B GQA MoE at 128K with NVFP4 weights and KV, bandwidth-bound with memory full. My roofline gives 1,184 tok/s/kW for Rubin against 2,756 for Continuum at N=16 (2.33×; 1.94× at N=8, 2.48× at N=32), and a 2.5 ms step against 13.1 ms. In $/Mtok I assume the custom package costs about 30% more than Rubin's | now 1.00 $/Mtok | with idea ≈0.5 $/Mtok | RATIO 2.0
VERDICT | WOUNDED | The roofline gain is real, about 2.3× per kW and about 2.6× per package. But it depends on 160 GB of hybrid-bonded DRAM per package, about 2× what is claimed as mature, and on a full-access energy no one has measured. Delivering about 2.7 kA up through the DRAM stack to the logic is also an open problem.
NEW FACT | UniIC VLSI 2023: "135 GBps/Gbit, 0.66 pJ/bit stacked embedded DRAM with multilayer arrays by fine-pitch hybrid bonding and mini-TSV", 2048 I/Os per Gbit at 541 Mbps; the IEDM 2020 generation gave 34 GB/s/Gb at 0.88 pJ/b, and two SoCs on it are in mass production | https://chinaflashmarket.com/a/179680 ; https://xmcwh.com/en/site/details/300?details=1
IDEA 8: One compute die, two phase-split SKUs
KILLER | C-SKU training throughput per package compared with Rubin | required ≥1.0× to be competitive | available 30/35 PF FP4 = 0.86× (the idea's own numbers, using the same compute-die class) | MARGIN 0.86
CHAIN | Rubin for training, plus Rubin CPX, a separate monolithic die with 128 GB GDDR7 and 30 PF NVFP4, for prefill. Saving 10–15% of package cost on compute-bound work, with the package at 45% of TCO, gives a 1.05–1.07× cost ratio. Training is at 0.86–1.0×. The "SRAM base-die D SKU" it builds on is not described in any of the ideas: Idea 3 uses DRAM | now 1.00 | with idea 0.95 | RATIO 1.05
VERDICT | DEAD | A product-line choice that gives at most about 5–7% on prefill and loses or ties on training is not a lead.
NEW FACT | Rubin CPX is a single monolithic die, not the Rubin compute die, with 128 GB GDDR7 and 30 PF NVFP4. The NVL144 CPX rack is rated at 8 EF, 100 TB of fast memory and 1.7 PB/s | https://investor.nvidia.com/news/press-release-details/2025/NVIDIA-Unveils-Rubin-CPX-A-New-Class-of-GPU-Designed-for-Massive-Context-Inference/default.aspx

Notes on method:
- **What I calculated vs. what I estimated:** All the arithmetic is in `/home/user/SomeRepository/engine/runs/v6_continuum/eval_g0/c2/gate_arith.py`. As a check, it reproduces Idea 2's 324 B per row, 2.59 GB dense and 0.62 GB sparse figures. Three inputs are my own estimates with no source behind them: the base-die heat budget of about 60 W, the +30% cost of the Idea 3 package, and the ~1% outlier share in Idea 1.
- **Inputs I couldn't confirm:** The DeepSeek indexer's 64 heads × 128 dims came from memory of the config file and is not confirmed. I found no source giving watts per HBM4 stack.

Sources:
- [Palu (arXiv 2407.21118)](https://arxiv.org/html/2407.21118v2)
- [Helios (arXiv 2603.04797)](https://arxiv.org/pdf/2603.04797)
- [3D-DRAM evaluation infrastructure (arXiv 2604.08044)](https://arxiv.org/pdf/2604.08044)
- [UniIC VLSI 2023 report](https://chinaflashmarket.com/a/179680)
- [XMC SeDRAM](https://xmcwh.com/en/site/details/300?details=1)
- [imec HBM-on-GPU (Bits&Chips)](https://bits-chips.com/article/imec-halves-peak-temperatures-in-3d-hbm-on-gpu-ai-chips/)
- [IEEE Spectrum on imec](https://spectrum.ieee.org/hbm-on-gpu-imec-iedm)
- [vLLM DeepSeek-V3.2](https://vllm.ai/blog/2025-09-29-deepseek-v3-2)
- [DeepSeek-V3.2 paper](https://arxiv.org/pdf/2512.02556)
- [Nvidia Rubin CPX press release](https://investor.nvidia.com/news/press-release-details/2025/NVIDIA-Unveils-Rubin-CPX-A-New-Class-of-GPU-Designed-for-Massive-Context-Inference/default.aspx)
- [Synopsys HBM4 PHY datasheet](https://www.synopsys.com/content/dam/synopsys/resources/dw/hbm4-phy-datasheet.pdf)
- [JESD270-4 summary](https://www.storagenewsletter.com/2025/04/17/jedec-and-industry-leaders-collaborate-to-release-jesd270-4-hbm4-standard/)
IDEA 9: SRAM-resident MoE expert farm
KILLER | SRAM left for KV cache after the weights, measured as concurrent users at 500 tok/s on 8k-in/1k-out traffic (~9k-token context; MiniMax-M2 has 62 layers × 8 KV heads × head dim 128, so KV is 127 KB/token at FP8 and 71 KB at NVFP4). To get near GB300's $/Mtok, a 3-wafer system at ~$571/hr TCO (3 × ~$3M CS-3-class wafers over 4 years, with the package taken as 45% of TCO) has to sell ~2.64M tok/s | required ~5,300 users | available 61 users (FP8 weights and KV, 70 GB free) to 265 users (FP4 weights and NVFP4 KV, 171 GB free) out of 300 GB SRAM (config: HF MiniMax-M2/M2.5 config.json; price: Next Platform/AIM CS-3 $2–4M; arithmetic in gate_calc.py, with the KV formula checked against Llama-3-70B's known 320 KiB/token) | MARGIN 0.05 (0.012 at FP8)
CHAIN | GB300 NVL72 disaggregated serving of MiniMax M2.5/M2.7 | now $0.06 /Mtok | with idea ~$1.2–5.2 /Mtok | RATIO 0.012–0.05
VERDICT | DEAD | Keeping all 230B parameters in SRAM leaves almost no room for KV cache, so the batch is roughly 20–90× too small to amortise wafer-class silicon; also, 300 GB in "2.5–3 wafers" needs ~100–120 GB per wafer, against WSE-3's 44 GB (≈6.8 wafers at WSE-3 density).
NEW FACT | MiniMax-M2: 62 layers, 8 KV heads, head_dim 128, 256 experts with top-8 routing | https://huggingface.co/MiniMaxAI/MiniMax-M2/blob/refs%2Fpr%2F57/config.json
NEW FACT | Cerebras CS-3 price is unpublished; estimates are ~$2.5M per node, ~$3.2M per system, and ~$4M with MemoryX/SwarmX | https://www.nextplatform.com/2024/03/14/cerebras-goes-hyperscale-with-third-gen-waferscale-supercomputers/
IDEA 10: Decode-only part, disaggregated prefill/training
KILLER | Decode power per package at Rubin-class 22 TB/s. "2× tokens per kW" needs ≤ half of Rubin's decode draw (taken as 0.8 × ~2.3 kW TDP, an analyst estimate). The floor is HBM read at 3.44–5.74 pJ/bit, plus 3.6 TB/s scale-up SerDes at ~5 pJ/bit, plus on-die movement at ~1 pJ/bit, plus ~100 W for compute and leakage | required ≤920 W | available floor 1,025–1,430 W (HBM pJ/bit: arXiv 2602.18568 and 2607.26491; Rubin 22 TB/s and ~2.3 kW: spheron/introl secondary sources) | MARGIN 0.64–0.9
CHAIN | Rubin NVL72 + CPX disaggregated serving, $/Mtok on owner TCO | now 1.0 (normalised) | with idea 0.76–0.89 (2× tok/kW halves energy at 9% and power-provisioned facility at 12%; the upper end also assumes a generous 30% cut in package cost from dropping training FLOPs, but HBM dominates the BOM) | RATIO 1.12–1.32
VERDICT | WOUNDED | The trade-offs are stated honestly and the design is physically plausible, but HBM access energy alone takes most of the claimed 2× power budget, and energy is only ~9% of TCO, so even a full 2× tok/kW cuts cost per token by about 1.1–1.3×, short of 1.5×.
NEW FACT | Rubin GPU HBM4 is reported at up to 22 TB/s per GPU, with a ~2,300 W TDP from analyst estimates that Nvidia has not confirmed; one source warns that initial bandwidth may fall below 22 TB/s | https://www.spheron.network/blog/nvidia-vera-rubin-nvl72-guide/ ; https://introl.com/blog/nvidia-vera-rubin-platform-8-exaflops-infrastructure
NEW FACT | HBM3E access energy is ~3.44 pJ/bit in one model and ~5.74 pJ/bit including I/O in another; HBM4 has no primary pJ/bit figure | https://arxiv.org/pdf/2602.18568 ; https://arxiv.org/pdf/2607.26491

The script is `/home/user/SomeRepository/engine/runs/v6_continuum/eval_g0/c3/gate_calc.py`, not committed. Several decisive inputs are my own assumptions, not sourced: TCO/hr from the 45% package share, Rubin drawing 80% of TDP during decode, ~5 pJ/bit SerDes and ~1 pJ/bit on-die movement, and the 30% package-cost cut.

Sources:
- [MiniMax-M2 config](https://huggingface.co/MiniMaxAI/MiniMax-M2/blob/refs%2Fpr%2F57/config.json)
- [MiniMax-M2.5 config](https://huggingface.co/MiniMaxAI/MiniMax-M2.5/blob/refs%2Fpr%2F40/config.json)
- [Next Platform CS-3](https://www.nextplatform.com/2024/03/14/cerebras-goes-hyperscale-with-third-gen-waferscale-supercomputers/)
- [AIM Research CS-3](https://aimresearch.co/?p=12750)
- [Spheron Vera Rubin guide](https://www.spheron.network/blog/nvidia-vera-rubin-nvl72-guide/)
- [Introl Vera Rubin](https://introl.com/blog/nvidia-vera-rubin-platform-8-exaflops-infrastructure)
- [arXiv 2602.18568](https://arxiv.org/pdf/2602.18568)
- [arXiv 2607.26491](https://arxiv.org/pdf/2607.26491)
