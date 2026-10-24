=== CALIBRATION ===

P | 1 | 42% | It has no FATAL defect, and its sizing arithmetic (SRAM area, LPDDR bandwidth, hop ceiling, KV per user) reproduces. However, the energy figure is about 1.5× worse than claimed (0.283 J/token), and the 2.8× cost edge shrinks to about 1.5× once LPDDR is priced at $10–21/GB. The edge also depends on unsourced Rubin and LPX baselines.

P | 2 | 18% | It has no FATAL defect, and the SPHBM4 mount and the 8,000:1 byte ratio check out. But it uses 1.57× more HBM per token/s, which undercuts its main selling point. Its edge mostly disappears against sparse or latent attention baselines, and NIC fan-in saturates ConnectX-9. The re-priced ratio is 1.0–1.2.

P | 3 | 5% | It has an unanswered FATAL defect. The design budgets no SRAM, so activation traffic caps routed experts at 28–42% utilization. The ratio falls below 1, and it relies on a rumoured CPX baseline.

P | 4 | 4% | It has an unanswered FATAL defect. HBM is priced 4–6× above 2026 contract, so package cost rises. Throughput halves at FlashMLA-class MFU and on all GQA models, and the multi-layer SoIC stack under a 1 kW die has not been demonstrated.

P | none | 31% | Every survivor's re-priced advantage is 1.0–1.5×. That is within the error of the baseline assumptions and well short of "best in the world." A hybrid could beat all four: for example, Idea 1 with right-sized LPDDR, or an LPX-class product.

WEAKEST LINK: Idea 1's advantage is measured against a Rubin NVL72 wide-EP cost of $0.214/Mtok at ≥1000 tok/s/user on a 671B MoE. That figure is unsourced, and published Blackwell-class records only reach hundreds of tok/s/user. If the baseline is cheaper, or cannot reach that tier at all, the ratio moves sharply in either direction.

FLIP TEST: Measure or simulate DeepSeek-V3 decode at 32K context and ≥1000 tok/s/user, comparing Rubin NVL72 (wide EP plus speculative decoding) and a 3-rack Groq 3 LPX against Continuum-D. Continuum-D should be costed at its full BOM with LPDDR at $20/GB and its 0.283 J/token energy. If the best baseline reaches ≤1.2× of Continuum-D's all-in $/Mtok, Idea 1 loses the lead and "none" becomes the most likely outcome. If the baseline cannot reach the tier at all, Idea 1 rises above 60%.

UNKNOWN: Even if Idea 1 is right, it is unclear whether a market for ≥1000 tok/s/user on frontier MoE models is large enough to define "best." It is also unclear whether 333-die SRAM residency survives the next model-size jump (1T+), or whether die failures and stragglers at that scale erase the yield and cost edge.