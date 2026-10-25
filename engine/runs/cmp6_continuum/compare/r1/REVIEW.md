=== REVIEW ===
IDEA 1: Same die, separate training/prefill SKU
DEFECT | MAJOR | The decode package has 6 HBM4 stacks across 2 dies, which is 3 PHYs per die. Continuum-T needs 8, which is 4 per die. A die built to take power and weights through hybrid-bonded SRAM base dies also cannot simply "drop the base dies". So this is a second die or a second base/interposer design, not the "same die". | 6/2 = 3 vs 8/2 = 4 HBM4 PHYs per die. Without base dies, roughly 1,400 A per die (1 kW at 0.7 V) needs a new power-delivery path.
DEFECT | MAJOR | With its SRAM gone, the compute die has little on-chip buffer for training GEMM tiles. Its ridge point is high, so 0.6–0.85× Rubin is an assumption, not a result. | 30 PF FP4 / (8 × 2.75 TB/s) = 1,364 FLOP/B, against Rubin's 35 PF dense / 22 TB/s ≈ 1,590 FLOP/B. Rubin gets there with large L2 and shared memory that this die lacks. No simulation is cited.
DEFECT | MINOR | The baseline mixes sparse and dense figures. Several sources list Rubin's 50 PF NVFP4 as sparse and 35 PF as dense. Which one the 0.6–0.85× uses decides whether it is 0.6 or 0.85. | barrack.ai and guru3d Rubin spec pages.
DEFECT | MINOR | "Prefill on Rubin CPX" rests on a single analyst report. CPX was dropped from the roadmap in March 2026 and reportedly revived with HBM4 in August 2026. | technews.tw 2026-09-02 (Ming-Chi Kuo); rutab.net 2026-03-17.
SURVIVES | Shared torch.export/StableHLO flow, honest "no lead in training" claim; NVFP4 PTQ of DeepSeek-class checkpoints with about 1% loss is established practice.
RATIO | 0.7 | Training cost/throughput at 0.6–0.85× Rubin, plus a second package NRE. The value is purely defensive.
KNOWN | yes | AWS Trainium/Inferentia (one Neuron SDK, two SKUs). Nvidia Rubin + Rubin CPX (same CUDA stack, split prefill/decode).

IDEA 2: SRAM-stacked weights, HBM4 only for KV
DEFECT | FATAL | 10 GB of SRAM does not fit in four base dies under two ~800 mm² compute dies. The rack then holds 182–407 GB, not 640 GB. At realistic density that is below the 377 GB of weights. | 10 GB needs 2,516 mm² at 31.8 Mib/mm² (100% array), 3,594 mm² at 70% array efficiency, or 5,634 mm² at the measured V-Cache density of 14.2 Mb/mm². The available footprint is about 1,600 mm², giving 2.8–6.4 GB per package.
DEFECT | MAJOR | The "5,300 users at 128K" capacity cannot be used at the target speed. When HBM is full, each decode step must read all of it. | 64 × 15 TB/s = 960 TB/s. 5,327 × 2.59 GB gives 69.6 tok/s/user. At 200 tok/s/user only 1,853 users fit.
DEFECT | MAJOR | tok/J and tok/s/kW use different power denominators, so "1.2× per J vs 1.5× per kW" contradicts itself. Both ratios must match on the same power. | Continuum: 6,200 × 144 kW = 892.8k tok/s, which implies 115 kW at 7.75 tok/J. Rubin: 875k tok/s implies 134.6 kW at 6.5 tok/J. The overhead is 29 kW for Continuum against 72 kW for Rubin, and that asymmetry is not explained.
DEFECT | MAJOR | Each 1 kW+ N2 die is powered through hybrid-bonded SRAM base dies, about 10× the power of the 9800X3D precedent. There is also no cost line for four ~400 mm² base dies plus SoIC bonding. | About 1,400 A per die through base-die TSVs, against ~120 W X3D parts.
DEFECT | MINOR | The Rubin "best case" at 25 µs/layer is a modelled number with no source. | No measurement is cited.
SURVIVES | 377 GB at 4.5 bits; 2.59 GB/user MLA KV at 128K (NVFP4); 216 GB/15 TB/s HBM; 384 vs 576 stacks; 2,325 vs 1,519 tok/s per stack; 32K at 200 tok/s/user is bandwidth-feasible (580 of 960 TB/s).
RATIO | 0.9 | Holding 377 GB at realistic density takes about 85–135 packages, not 64. HBM stacks and power rise 1.3–2.1×, which erases the 1.2× per-joule lead.
KNOWN | partly | Nvidia Rubin NVL72 + Groq 3 LPX (weights in SRAM, KV on GPU HBM), storagereview.com "nvidia groq 3 lpx everything we know". d-Matrix 3D-stacked DRAM roadmap.
NEW FACT | Groq 3 LPU: 500 MB SRAM and 150 TB/s per chip; 256 LPUs and about 128 GB per LPX rack | https://www.3dtested.com/tech-industry/semiconductors/nvidias-20-billion-groq-deal-produces-its-first-chip

IDEA 3: Detached attention-stack memory nodes
DEFECT | MAJOR | The baseline is a Llama-70B-style GQA model with dense 128K attention. A competent operator uses MLA or sparse-attention models, which shrink KV and attention 10–17×. That removes most of the market for these nodes. | DeepSeek KV is 19.8 KB/token vs 160 KB (GQA-70B FP8), about 8×. The DSA indexer costs about 1.0 MFLOP vs 17 MFLOP per context token. DeepSeek reports 128K decode cost falling from about $2.4 to $0.8 per Mtok (arXiv 2512.02556).
DEFECT | MAJOR | The 0.2 GB/s per node adds up to the whole GPU NIC on the Rubin side. | 1,500 users × 49 tok/s × 2.79 MB (BF16 q/o, 80 layers) = 205 GB/s, about 100% of a 1.6 Tb/s ConnectX-9. FP8 q/o still uses 50%.
DEFECT | MAJOR | Node power is understated. The 13–19 W covers only the base die, and DRAM core reads at 2.5 TB/s add more on top. The cost of each standalone node (board, NIC, PSU, enclosure) is not in the $0.177. | 2.5 TB/s × 8 × 2–3 pJ/bit = 40–60 W more per stack. 750 such nodes go with every Rubin.
DEFECT | MINOR | The per-layer chain is serial (q out → attention on 750 nodes → GPU FFN), with tail latency across 750 nodes. | Per layer per user the budget is 255 µs. KV read takes 107–215 µs, and FFN for a batch of 1,500 takes about 75 µs at 35 PF dense, so 49 tok/s/user leaves less than 0–70 µs of slack.
SURVIVES | 21.5 GB/user at 128K FP8 (GQA-70B); 2 users/stack at about 58 tok/s peak (49 realistic); KV:link ratio of about 7,700:1; the 33% (not 2×) energy correction; SPHBM4 exists (JESD330-4, 13 July 2026, verified).
RATIO | 1.2 | Against an MLA/sparse-attention model or host-memory KV offload rather than Rubin-only GQA; the 2.6× "market price" figure is markup avoided.
KNOWN | partly | Lamina, attention offloading to memory devices (arXiv 2405.01814). Samsung HBM-PIM and SK hynix AiM.
NEW FACT | SPHBM4 = JESD330-4, 512 data signals at 4:1 serialization, 22.4–46 GT/s, organic substrate | https://www.tomshardware.com/pc-components/dram/jedec-releases-new-sphbm4-standard-to-slash-ai-memory-costs-narrow-512-bit-interface-enables-dropping-expensive-interposers-for-organic-substrates

IDEA 4: Cheap-node HBM decode tier
DEFECT | FATAL | "3 PF FP8 saturates 22 TB/s" holds only for GQA-class decode. MLA decode, which this design's own target workloads use, needs about 6× more compute. On those models the N6 part is compute-bound at about 1/6 of Rubin's throughput. | 858 FLOP/B × 22 TB/s = 18.9 PF needed vs 3 PF. That is $16k/3 PF = $5.3k per PF against $45k/16 PF = $2.8k per PF for Rubin.
DEFECT | MAJOR | The 2.7× formula treats the whole 91% non-energy TCO as package cost. It also halves energy, but N6 uses more energy per FLOP than N3. | Assume 55% package, 30% system/network/facility, 6% ops, and energy ×1.2 instead of ÷2. The result is 1/(0.55/2.8 + 0.30 + 0.108 + 0.06) = 1.5×.
DEFECT | MAJOR | 3 PF FP8 on N6 needs 2,500–4,000 mm² of logic plus 8 HBM4 PHYs. That is 3–5 reticle dies on a CoWoS-L interposer at or above the current ~5.5-reticle limit, so "$2k packaging" is not credible. | 3,000 / 0.755 TF/mm² (A100 N7) = 3,974 mm². At 1.2 TF/mm² it is 2,500 mm².
DEFECT | MINOR | The HBM cost line looks high, not low. It also does nothing for the stated HBM shortage, since the part still uses 8 stacks per package like Rubin. | 8 × ~$550 (SK hynix HBM4, TrendForce Nov 2025) = $4.4k vs $12k assumed ($41.7/GB).
SURVIVES | The admission that the margin is "mostly vendor markup avoided"; for dense GQA decode, memory-bound sizing at about 136 FLOP/B is correct.
RATIO | 1.1 | About 1.5× on GQA decode, below 1 on MLA decode; after corrected TCO shares the blend is about 1.1.
KNOWN | partly | Huawei Ascend 910C (SMIC 7nm-class logic with HBM). AWS Inferentia2.

IDEA 5: N6 SRAM-chiplet pipeline packages
DEFECT | FATAL | 112 GB over 512 dies of 100 mm² needs a whole-die SRAM density above AMD's measured pure-SRAM V-Cache die, with zero area left for compute. | 218.75 MB/die = 17.5 Mb/mm² over the full die vs 14.2 Mb/mm² measured. Idea 9 corrects it to 124 MB/die with 30 mm² of logic.
DEFECT | FATAL | The headline value "GB300 cost at 20× speed" was retracted by this run's own later repair (Idea 9). That repair found 2–4× more cost per token than GB300 and per-user speed halved by die-by-die pipelining. | Idea 9 text: "$0.14–0.23/Mtok ... 2–4× more per token than GB300".
DEFECT | MAJOR | "Half the cost per SRAM byte vs N3" does not reproduce. | Wafer price × bitcell area: (10k × 0.027)/(19k × 0.021) = 0.68, not 0.5.
SURVIVES | Raw N6 silicon at about $0.1–0.15/MB of SRAM ($10k wafer, ~540 good 100 mm² dies, 124 MB each).
RATIO | 0.4 | Cost per token against GB300 at normal interactivity (Idea 9 corrected figures).
KNOWN | yes | d-Matrix Corsair (8 TSMC 6nm chiplets, 2 GB SRAM, 150 TB/s), hc2025.hotchips.org 24_dMatrix_Bhoja_final.pdf. Groq LPU.

IDEA 6: Layer-pipelined LPDDR prefill dies
DEFECT | MAJOR | It ignores the cheapest current prefill: chunked prefill running on decode-tier GPUs' idle FLOPs, which are mostly unused in memory-bound decode, plus prefix caching. Both cut marginal prefill cost well below a dedicated tier. | Decode at about 100–800 FLOP/B on a ~1,590 FLOP/B Rubin leaves more than 50% of compute idle. The vs-CPX figure also relies on a single-analyst report of an HBM4 CPX (technews.tw 2026-09-02).
DEFECT | MINOR | The 45K tokens "compute-bound" threshold holds only at about 75% MFU. At 100% it needs 58K, which lengthens TTFT. | Pass memory time 34.3 ms; 11.8 GFLOP/token/die. Balance at 58.1K (100%) or 29.1K (50%) tokens.
DEFECT | MINOR | A 1024-bit LPDDR5X bus at 10.7 Gbps needs twice Grace's 512-bit beachfront on an 800 mm² die that also carries a NIC and die links. LPDDR prices rose sharply in the 2026 DRAM shortage, and that is not in the cost. | 1024 × 10.7/8 = 1.37 TB/s reproduces. The PHY edge is about 80 of 113 mm of perimeter.
SURVIVES | 910 FLOP/B at 256 tokens/expert; 47 GB/die; activation traffic of about 6–12 GB/s (inside the stated 15–45); no NVLink-class fabric needed for layer pipelining.
RATIO | 1.1 | After crediting the baseline with chunked prefill and prefix caching on an existing fleet.
KNOWN | partly | Nvidia Rubin CPX (GDDR7 prefill part; reportedly revived on HBM4 with 168 GB). Cerebras weight streaming (layer-major).
NEW FACT | Rubin CPX was dropped at GTC March 2026, then reportedly revived with HBM4 (168 GB/GPU, production 1Q27, 1:1 pairing with Rubin), per Kuo; not confirmed by Nvidia | https://technews.tw/2026/09/02/nvidia-rubin-cpx-reenters-roadmap-hbm4-ai-prefill/

IDEA 7: Ridge point matched to MLA decode
DEFECT | MAJOR | The premise that dense attention dominates long-context decode is already outdated for DeepSeek-class models. DeepSeek-V3.2's DSA cuts per-context-token compute about 17× and attends to the top 2,048 tokens. The 1,000 FLOP/B ridge is then tuned to a superseded model. | Indexer 2 × 64 × 128 × 61 = 1.0 MFLOP vs 17.0 MFLOP per context token (arXiv 2512.02556).
DEFECT | MAJOR | The 1.08× lead at 128K sits inside model error and rests on equal assumed pJ/FLOP. Continuum also has less FP8 and less bandwidth per package than Rubin. | 15 PF / 15 TB/s vs Rubin's about 16–17.5 PF / 22 TB/s, which leaves Continuum 1.1–1.5× slower per package at 128K. A ±20% swing in the 0.1 pJ/FLOP assumption flips the sign.
DEFECT | MINOR | With a ridge of 1,000 above the 858 FLOP/B intensity, attention on Continuum is bandwidth-bound, not "compute-bound at FP8". | 17.0e6 / 19.8e3 = 858.
SURVIVES | 17 MFLOP and 19.8 KB per context token; 56 mJ attention compute and 21 mJ KV read at 32K (4 pJ/bit); Ironwood ridge of about 626; Rubin ridge of about 727–795, since Rubin dense FP8 is not published.
RATIO | 1.0 | 1.08× is within error and goes to zero with sparse attention.
KNOWN | partly | Balancing compute and bandwidth for attention is standard practice (FlashMLA; Blackwell Ultra's doubled attention SFU throughput).
NEW FACT | DSA: top-2,048 token selection, FP8 lightning indexer, quality reported near V3.1-Terminus; indexer precision about 60% on 128K HELMET | https://arxiv.org/pdf/2512.03494

IDEA 8: Continuum-D: SRAM weights, LPDDR KV
DEFECT | MAJOR | The energy per token does not reproduce from the stated power and throughput. It is about 45% worse than stated, so "about 9% worse than Rubin" becomes about 55% worse. | 117 kW / 414k tok/s = 0.283 J/token vs the stated 0.19–0.20.
DEFECT | MAJOR | The Rubin baseline at ≥1,000 tok/s/user ($0.214) contradicts Idea 10's "no Rubin setup reaches this speed". The competent baseline is a GPU with speculative decoding, which Continuum would also use. | DGX B200 measured 1,038 tok/s/user on Llama 4 Maverick (400B MoE) with EAGLE-3 (Nvidia/Artificial Analysis, May 2025).
DEFECT | MINOR | The 1 TB/s per die needs top-bin LPDDR6. At launch speeds the LPDDR ceiling falls below the compute-bound rate. | 624 b × 10.7 Gbps = 0.83 TB/s, giving 428k tok/s ceiling. 1 TB/s needs about 12.8 Gbps.
DEFECT | MINOR | Weights are not replicated. With 333 dies, a die failure takes the system down about weekly until reload. | About 4.7e-4 failures per die-day (Llama-3 fleet rate) × 333 ≈ 0.16/day.
SURVIVES | 377 GB; 428 mm² of SRAM per 1.25 GB; 514k tok/s LPDDR ceiling; 686k tok/s at 100% compute (414k ≈ 60% MFU); 11.8k tok/s/user hop ceiling; $0.077/Mtok at 4-year life, 70% utilisation and 3× markup.
RATIO | 1.8 | Against a GPU with speculative decoding at ≥1,000 tok/s/user, after the energy correction. The Rubin $0.214 is unsourced.
KNOWN | partly | d-Matrix Corsair (SRAM + 256 GB LPDDR5 per card); Groq 3 LPX.
NEW FACT | d-Matrix Corsair: 2 GB SRAM at 150 TB/s, 256 GB LPDDR5 at 400 GB/s, 2,400 TFLOPS MXINT8, 8 TSMC 6nm chiplets | https://hc2025.hotchips.org/assets/program/conference/day2/24_dMatrix_Bhoja_final.pdf

IDEA 9: N6 SRAM chiplets, package-wide tensor stages
DEFECT | MAJOR | The cost is quoted only at 8K context and 32 users. KV grows linearly with context and takes most of the SRAM, so cost per token roughly doubles at 32K and grows about 6× at 128K. | 32K needs 136 GB (1,100 dies); 128K needs 426 GB (3,438 dies), against 67 GB (544 dies) at 8K.
DEFECT | MAJOR | It compares cost of goods against Groq and Cerebras list prices, which include margin. The 2.6–5.6× is therefore not like-for-like. | Cerebras Llama-3.3-70B lists at $0.85 in / $1.20 out (cloudprice.net). At a 50% margin, the competitor's cost is about $0.4–0.6.
DEFECT | MINOR | 17 stages with 16 micro-batches leaves the pipeline one stage underfilled. The 1 µs all-reduce across 32 dies is unproven; a ring would take about 3 µs. | 62 ring steps × 50 ns = 3.1 µs, which adds about 20 µs per stage. That gives about 1,000 tok/s/user, not 1,198.
SURVIVES | 124 MB/die; 22.65 TF/die; 39.7 GB weights + 24.2 GB KV = 64 GB; 1/(17 × 49.1 µs) = 1,198 tok/s/user; about 26 µs ideal stage compute (37.7 µs ≈ 70% efficiency); honest retraction of the GB300 claim.
RATIO | 1.5 | Against the competitors' estimated cost (not list price) at 8K. Close to 1 at 32K.
KNOWN | yes | d-Matrix Corsair (6nm SRAM chiplets); Groq LPU.

IDEA 10: Deterministic, compiler-scheduled low-latency scale-up fabric
DEFECT | MAJOR | "No Rubin or Ironwood reaches 1,000 tok/s/user" is false for a comparable MoE once speculative decoding is used. The text then gives a Rubin figure at that speed anyway (639 tok/s/kW). | DGX B200: 1,038 tok/s/user on Llama 4 Maverick with EAGLE-3 (developer.nvidia.com blog).
DEFECT | MAJOR | Fixed all-to-all slots must be sized for the busiest expert. Even with perfectly uniform routing that wastes about 1.7–1.9× of slot capacity at the operating batch, and real routing is more skewed. | Monte Carlo with 256 experts, top-8: max/mean = 1.86 at batch 414 and 1.68 at batch 573.
DEFECT | MAJOR | The bandwidth figure is taken at an inconsistent point. At 1,000 tok/s/user, 64 packages at 144 kW serve only about 573 users. Batch 4096 at 1,000 tok/s/user needs about 6× the stated per-package bandwidth. | 10 MB/token of all-to-all over 58 layers: 0.64 TB/s per package at 4096 × 1,000 tok/s vs 0.09 TB/s at 573k tok/s.
DEFECT | MINOR | Cerebras "implies about 10 µs/layer" does not reproduce without a model and a speculative-decoding correction. | 2,300–2,500 tok/s on 80 layers = 5.0–5.4 µs/layer per token.
DEFECT | MINOR | tok/J and tok/s/kW again use different denominators, as in Idea 2. | 6.35 / 3.978 = 1.60.
SURVIVES | DeepEP 77–194 µs dispatch and 114–369 µs combine (H800, IB, 128 tokens, EP8–256); 1.8 TB/s/direction matches NVLink 6; a ≤1 µs switch traversal is physically plausible.
RATIO | 2.5 | Against Rubin with speculative decoding at about 12 µs/layer (1,785 vs 639 tok/s/kW, minus slot padding). At 20 µs it falls below 1.
KNOWN | yes | Groq RealScale compiler-scheduled chip-to-chip fabric, Groq 3 LPX (640 TB/s scale-up), sdxcentral.com; Google TPU ICI.
NEW FACT | The DeepEP README notes (2025-06-05) that low-latency kernels now use NVLink where possible, so the IB-era 77/114 µs figures overstate GPU per-layer latency | https://gitee.com/wxx213/DeepEP