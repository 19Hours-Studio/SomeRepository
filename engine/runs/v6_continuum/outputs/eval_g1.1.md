=== GATE ===
IDEA 1: Stacked-eDRAM pipeline chiplet packages
KILLER | Bandwidth per user while layers are pipelined. Each pipeline stage can only read its own bits, so the 42 TB/s total equals per-user bandwidth only if every chiplet works on every layer. "Package links" means at least 2 stages. At the measured 0.064 Gb/mm², 312 Gb needs 4,875 mm², or 1.5 packages of 3,200 mm². | required 40.1 TB/s (39.4 GB of NVFP4 weights plus 0.75 GB of KV at 8K, × 1,000 tok/s) | available 21 TB/s per stage with 2 stages (UniIC VLSI 2023: 135 GB/s/Gb × 312 Gb ÷ 2; ISSCC 2022 Niu et al.: 64 Mb/mm² hybrid-bonded logic-DRAM). The best case, a single stage, gives a 1.08 margin before any DRAM efficiency loss. The 312 Gb also leaves no room for KV. | MARGIN 0.52
CHAIN | SRAM dataflow serving of 70B at roughly 300–750 tok/s/user (Groq list price) | now $0.79/Mtok (a list price that includes vendor margin) | with idea ≈$0.05–0.2/Mtok (my rough TCO estimate: N6 + eDRAM wafers + bonding, 4-year amortisation, a few users per pipeline; not measured) | RATIO ~5
VERDICT | WOUNDED | Stacked eDRAM is cheap, but the 1,000 tok/s/user claim treats total bandwidth as per-user bandwidth, which layer pipelining does not give, so it delivers about 500 tok/s/user unless all chiplets are tensor-parallel on every layer.
NEW FACT | The only measured areal density found for hybrid-bonded logic-to-DRAM is 64 Mb/mm² ("184QPS/W 64Mb/mm² 3D Logic-to-DRAM Hybrid Bonding…", Niu et al., Alibaba, ISSCC 2022) | https://arxiv.org/pdf/2412.19275 ; https://www.jos.ac.cn/article/doi/10.1088/1674-4926/24050004

IDEA 2: Half-size DRAM-on-logic pipeline packages
KILLER | DRAM areal density for 80 GB on 2 chiplets × 4 layers. Chiplet area is not stated; I took about 400 mm² from the sibling design. | required 0.20 Gb/mm² while also fitting wide-I/O periphery and power TSVs | available 0.064 Gb/mm² measured for hybrid-bonded logic-DRAM (ISSCC 2022). For comparison, an HBM3E core die is ≥0.198 Gb/mm² (Micron: 24 GB 8-high in 11×11 mm), but that leaves no area for kA-class power TSVs. | MARGIN 0.32
CHAIN | Rubin HBM4 decode, tokens/s per kW | now 9.6 TB/s/kW (22 TB/s ÷ ~2.3 kW, analyst estimate) | with idea 32 TB/s/kW. The raw ratio is 3.35×, and the idea's own model gives 2.2–2.7× tokens/kW. Cost per token is not established, because package $/kW is unknown and energy is only ~9% of TCO. | RATIO ~2.2
VERDICT | WOUNDED | It needs the same 0.20 Gb/mm² "no room left" density that idea 3 had to drop, which is ~3× the measured hybrid-bonded density. Its current claim is also internally off by 2×: 1 kW at 0.75 V across 2 stacks is ~667 A per stack, not 340 A.
NEW FACT | Commodity D1b 16Gb DRAM is 0.431–0.447 Gb/mm² (Samsung LPDDR5X 36.68 mm², 446.7 Mb/mm²) | https://www.techinsights.com/ko/node/59204

IDEA 3: Half-density hybrid-bonded DRAM decode package
KILLER | Wide-I/O hybrid-bonded DRAM areal density per layer | required 0.10 Gb/mm² at 100 GB/s/Gb | available 0.064 Gb/mm² measured hybrid-bonded (ISSCC 2022). The path to more is credible: HBM3E with TSVs reaches ≥0.198 and commodity DRAM 0.44 (TechInsights). Separately, the idea's premise that 0.20 Gb/mm² is commodity DRAM "with no room left" is wrong, since commodity is ~0.44. | MARGIN 0.64
CHAIN | Rubin HBM4 decode, GQA MoE at 8K–128K, tokens/s per kW | now 9.6 TB/s/kW (Rubin estimate) | with idea 31.4 TB/s/kW nominal. At the measured density, capacity is 410 Gb, bandwidth 55 TB/s and package power 1.97 kW, which takes the modelled 2.13× down to ~1.9× tokens/kW at 32 packages. The gain on MLA models is only 1.1–1.3×, and cost per token is unproven. | RATIO ~1.9
VERDICT | WOUNDED | The physics adds up (DRAM power 450 W checks out, and bandwidth per bit is under the measured 135 GB/s/Gb), but the one deciding density has only been shown at 64% of what is needed. Heat from the logic die on DRAM is a second open risk, since imec's 3D layout reached 141.7 °C without mitigations.
NEW FACT | Micron HBM3E is 24 GB 8-high in an 11×11 mm package, so a 24Gb core die is ≤121 mm², i.e. ≥0.198 Gb/mm² with TSVs | https://micron.net/content/dam/micron/global/public/documents/products/product-flyer/hbm3e-product-brief.pdf

IDEA 4: N6 SRAM-chiplet pipeline, NVFP4-sized
KILLER | Per-user speed when SRAM-resident weights are pipelined layer by layer. Only the dies that hold layer ℓ can compute it, so a token's time per step is L·F/P_total. My script reproduces the idea's own 62.8 GB and 5.0 PF as a known-answer check. | required 1,000 tok/s/user | available ≤526 tok/s/user (6.8 PF ÷ (80 layers × 161 GFLOP/token)). This is an upper bound, because link and all-reduce latency come on top. Groq needed 576 LPUs for 300 tok/s, far below its total compute, which agrees with this bound. | MARGIN 0.53
CHAIN | SRAM dataflow serving of 70B (Groq list price) | now $0.79/Mtok | with idea ≈$0.17/Mtok. That is the idea's $0.068 rescaled to the reachable 16.3k tok/s total (31 users × 526) instead of 31k, then divided by the ~75% of TCO that its hardware-plus-energy figure covers. Capacity is full (63.6 vs 62.8 GB), so users can't be added. It compares a cost estimate against a price that includes margin. | RATIO ~4.6
VERDICT | WOUNDED | The density, capacity and compute totals check out, but layer-serial pipelining limits it to about half of the claimed 1,000 tok/s/user. Its $0.068 claim also rests on full pipeline utilisation that 31 users across 80 stages cannot provide, and it leaves out facility and network costs.
NEW FACT | Llama 3.3 70B output list prices are Groq $0.79/Mtok and Cerebras $1.20/Mtok; one April 2026 source gives Cerebras ~$0.60 | https://cloudprice.net/models/cerebras/llama-3.3-70b ; https://www.morphllm.com/cerebras-pricing ; https://deploybase.ai/articles/groq-vs-cerebras-pricing-speed-and-benchmark-comparison

The arithmetic is in `gate_calc.py` and `gate_calc.out`, with a summary in `gate_notes.md`, all in the `c1` folder. I didn't commit anything.

Sources:
- [ISSCC 2022 HB-PNM, via arXiv 2412.19275](https://arxiv.org/pdf/2412.19275)
- [J. Semicond. 2024 reference list](https://www.jos.ac.cn/article/doi/10.1088/1674-4926/24050004)
- [SeDRAM MDPI](https://www.mdpi.com/2079-9292/12/5/1077)
- [IEDM 2020 SeDRAM](https://www.semanticscholar.org/paper/A-Stacked-Embedded-DRAM-Array-for-LPDDR4-4X-using-s-Fujun-Jiang/020b5921a95195c1ff6741604e6bfeb3c84d06ee)
- [TechInsights D1b](https://www.techinsights.com/ko/node/59204)
- [Micron HBM3E brief](https://micron.net/content/dam/micron/global/public/documents/products/product-flyer/hbm3e-product-brief.pdf)
- [cloudprice Cerebras](https://cloudprice.net/models/cerebras/llama-3.3-70b)
- [Morph Cerebras pricing](https://www.morphllm.com/cerebras-pricing)
- [DeployBase Groq vs Cerebras](https://deploybase.ai/articles/groq-vs-cerebras-pricing-speed-and-benchmark-comparison)