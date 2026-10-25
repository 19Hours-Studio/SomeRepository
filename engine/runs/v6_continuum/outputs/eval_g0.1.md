I wrote the arithmetic to `gate_calc.py` and its output to `gate_calc.out`, both in the working directory, and committed nothing. To check the method on a known case, the script reproduces Groq v1's density from published figures (230 MB on 725 mm² ≈ 2.5 Mb/mm²) and AMD V-Cache's (512 Mb in 36 mm² ≈ 14.2 Mb/mm²). I could not measure energy or quality by running code, because there is no silicon and no model downloads here. Those inputs come from published figures.

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