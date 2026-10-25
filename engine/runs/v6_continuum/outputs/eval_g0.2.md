=== GATE ===
IDEA 1: Latent KV With Outlier Sidecar
KILLER | KV compression versus FP16 reached at ≤1% accuracy loss at 128K context | required 6–8× (7× midpoint) | available ≈6.2× at <1–2% LongBench loss, tested only up to 32K. This combines Palu's 30% low-rank cut and 3-bit latents with a 1% FP16 outlier sidecar; at a 50% rank cut Palu "struggles" on accuracy. No 128K data exists (Palu, ICLR 2025, arXiv 2407.21118; my arithmetic) | MARGIN 0.89
CHAIN | NVFP4 KV at 4.5 bits (3.56× vs FP16) on a Blackwell/Rubin GPU, with KV reads at 25–35% of decode time at 128K | now 1.00 step time | with idea 0.86–0.89 step time (KV only 1.73× smaller than NVFP4). On MLA models, whose KV is already a latent, the gain is about 0 | RATIO 1.14
VERDICT | WOUNDED | It is physically fine, but it buys only 1.7× on KV over NVFP4, which is about 1.12–1.17× on the whole system, and its accuracy at 128K has never been measured.
NEW FACT | Palu: a 30% low-rank cut loses under 1% average on LongBench; 3-bit latents add under 1% more; 11.4× total compression "while maintaining perplexity"; tests went only up to 32K | https://arxiv.org/html/2407.21118v2

IDEA 2: Near-HBM sparse-KV gather attention engine
KILLER | heat from about 10 PF FP8 of logic in the HBM4 base dies, which sit under the DRAM | required ≈2.2 kW in total, ≈278 W per stack × 8 stacks. This uses 0.22 pJ/FLOP, taken from B200's 4.5 PF dense FP8 at about 1 kW | available ≈60 W per base die. That is my estimate: about 0.5 W/mm² × about 120 mm². imec found that GPU-class logic under 12-high hybrid-bonded HBM reached 141.7 °C, and getting it to 70.8 °C took removing the base die, double-sided cooling and frequency scaling (imec, IEDM 2025) | MARGIN 0.22
CHAIN | Rubin running the same DeepSeek-style sparse attention (DSA) model on its main arrays. Sparse decode needs only 166 GFLOP per user-token on 0.62 GB, about 269 FLOP/B, so 5.9 PF at 22 TB/s, and Rubin's main compute covers that. The traffic is 93% sequential index scan and only 6.6% gather, so the gather risk does not matter. Both chips are bound by the same HBM bandwidth. The only gain left is the interposer-hop energy, and energy is about 9% of TCO | now 1.00 $/Mtok | with idea ≈0.95 $/Mtok | RATIO 1.05
VERDICT | DEAD | The 3.7× comes from the sparse model, which incumbents also run. The near-HBM engine is sized for dense intensity (450 FLOP/B) and cannot be cooled under DRAM, and with the bandwidth unchanged it barely changes $/Mtok.
NEW FACT | vLLM's FP8 MLA KV layout for DeepSeek-V3.2 is 656 bytes per token per layer, and the indexer K-cache is a separate buffer; top-k = 2048 in the released code | https://vllm.ai/blog/2025-09-29-deepseek-v3-2
NEW FACT | imec IEDM 2025: 4 stacks of 12-high hybrid-bonded HBM placed on a GPU push the GPU peak from 141.7 °C down to 70.8 °C only with mitigations | https://bits-chips.com/article/imec-halves-peak-temperatures-in-3d-hbm-on-gpu-ai-chips/

IDEA 3: Hybrid-bonded DRAM-on-logic decode package
KILLER | hybrid-bonded DRAM capacity per package at 64 TB/s, which needs 0.20 Gb/mm² per DRAM die and 50 GB/s/Gb | required 160 GB at 64 TB/s and ≤1 pJ/bit | available ≥80 GB from 4-layer stacks, which Helios' industry collaborators call mature (arXiv 2603.04797). Bandwidth is not the limit: SeDRAM shows 135 GB/s/Gb at 0.66 pJ/b (UniIC, VLSI 2023), 2.7× the need. But 0.66–0.88 pJ/b is the interface figure, not the whole access. At 1.5–2 pJ/b the DRAM would draw 770–1,020 W of the 2 kW budget | MARGIN 0.5
CHAIN | Rubin, 288 GB at 22 TB/s and about 1.8 kW, serving a 1T/32B GQA MoE at 128K with NVFP4 weights and KV, bandwidth-bound with memory full. My roofline gives 1,184 tok/s/kW for Rubin against 2,756 for Continuum at N=16 (2.33×; 1.94× at N=8, 2.48× at N=32), and a 2.5 ms step against 13.1 ms. In $/Mtok I assume the custom package costs about 30% more than Rubin's | now 1.00 $/Mtok | with idea ≈0.5 $/Mtok | RATIO 2.0
VERDICT | WOUNDED | The roofline gain is real, about 2.3× per kW and about 2.6× per package. But it depends on 160 GB of hybrid-bonded DRAM per package, about 2× what is claimed as mature, and on a full-access energy no one has measured. Delivering about 2.7 kA up through the DRAM stack to the logic is also an open problem.
NEW FACT | UniIC VLSI 2023: "135 GBps/Gbit, 0.66 pJ/bit stacked embedded DRAM with multilayer arrays by fine-pitch hybrid bonding and mini-TSV", 2048 I/Os per Gbit at 541 Mbps; the IEDM 2020 generation gave 34 GB/s/Gb at 0.88 pJ/b, and two SoCs on it are in mass production | https://chinaflashmarket.com/a/179680 ; https://xmcwh.com/en/site/details/300?details=1

IDEA 4: One compute die, two phase-split SKUs
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