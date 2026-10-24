=== GATE ===
IDEA 1: Compiler-Scheduled Power Envelope
KILLER | supply-voltage guardband the compiler can remove beyond what adaptive clocking already recovers | required 10% of Vdd (low end of the claim) | available about 5% of Vdd (est.: IBM POWER9's adaptive clocking already halved its droop margin, so only the leftover droop is new; the margin for process, aging and temperature stays because the compiler cannot know those) (Synopsys adaptive-clocking blog; IBM z-series guardband papers) | MARGIN 0.5
CHAIN | GB200 NVL72 disaggregated MoE inference, with adaptive clocking and droop detectors already in the chip | now $0.04–0.08 per million tokens | with idea about 2% lower (a 5% V cut gives about 10% less dynamic chip power; I assume the chip is about 60% of IT power, and only the electricity plus facility shares (35%) scale with it) | RATIO 1.02
VERDICT | DEAD | Even at the full claimed 20% voltage cut, the saving reaches only the power-linked 35% of cost and gives at most 1.08x. That is below the 1.1 line, and running near threshold also needs more area to keep the same throughput, which the idea says it avoids.
NEW FACT | AMD's adaptive clocking already delivered 7–15% better power efficiency, and IBM POWER9 halved its droop margin. Droop-margin recovery is already current practice. | https://www.synopsys.com/blogs/chip-design/dynamic-power-management-demands-adaptive-clocks.html

IDEA 2: Codec-Native Tensor Datapath
KILLER | bits per weight needed at near-FP8 accuracy | required ≤2.67 b/w (needed for 3x over FP8) | available about 3.0 b/w (QTIP is near-lossless at 3 bits; at 2 bits Llama-2-70B Wikitext2 perplexity is 3.78 against 3.12 for FP16, about +21%, which is not near-FP8) (arXiv 2406.11235; GLVQ table arXiv 2510.20984) | MARGIN 0.89
CHAIN | NVFP4 weights on Blackwell/Rubin (4 bits plus an FP8 scale per 16 values = 4.5 b/w; Kimi K2 Thinking ships native INT4), not FP8 | now 4.5 b/w, with weight streaming about 50% of decode step time (est.) | with idea 3.0 b/w, so 1.5x less weight traffic; the KV cache and compute do not shrink | RATIO 1.2
VERDICT | WOUNDED | The codec works at about 3 bits, but the real baseline is FP4, not FP8. Against FP4 the claimed 3x shrinks to about 1.5x on weight traffic and about 1.2x end to end, and the decoder also feeds FP8-rate MACs rather than FP4-rate ones.
NEW FACT | QTIP 2-bit Llama-2-70B gives perplexity 3.78 versus QuIP# 3.91 and FP16 3.12; GLVQ-32D reaches 3.36 at 2 bits, so 2-bit quality is still improving | https://arxiv.org/pdf/2510.20984

IDEA 3: BEOL Non-Volatile Weight Fabric
KILLER | weight storage density in BEOL memory | required 944 Mb/mm² (2,200 chips × 230 MB = 506 GB, packed into 5 reticles of 858 mm²) | available about 40 Mb/mm² per layer from the bitcell alone, before any periphery (TSMC's ISSCC 2024 12nm RRAM has a 0.0249 µm² 1T1R cell; 1T1R needs a front-end transistor, so it does not stack freely in BEOL). Generously assuming 4 stacked layers gives 160 Mb/mm². (TSMC ISSCC 2024 paper 15.7, via TechInsights) | MARGIN 0.04 (one layer) to 0.17 (four layers)
CHAIN | HBM decode (ledger archetype C), where only weight traffic moves into the fabric; the KV cache cannot move because it is rewritten every token and RRAM endurance is about 10k cycles | now 107–242 mJ/token | with idea, weight streaming drops but KV-cache streaming, compute and static power stay, about 1.3x (est.) | RATIO 1.3
VERDICT | DEAD | Density falls short by 6–24x, so "5 reticles" becomes about 30–120. And 10k-cycle endurance rules out holding the KV cache, the part that grows with context.
NEW FACT | TSMC 12nm RRAM: 32 Mb macro, 0.0249 µm² bitcell, 3.2 GB/s read, 10k write cycles, 10-year retention at 105 °C | https://www.eetasia.com/?p=57311

IDEA 4: Compiler-Scheduled Optical Circuits
KILLER | circuit reconfiguration time, against the per-layer switches between expert dispatch, combine and all-reduce in decode | required ≤5.5 µs (10 ms/token, 61 layers, 3 reconfigurations per layer, 10% overhead budget) | available 10–100 ms for 3D-MEMS optical circuit switches (Google Apollo-class; secondary press says seconds); the best fast prototype (Mordia) switches in 11.5 µs (UCSD/Google papers; DCD) | MARGIN 0.0005 (MEMS) to 0.48 (Mordia prototype)
CHAIN | NVL72 copper NVLink scale-up plus packet scale-out (ledger A) | now network about 11% of TCO | with idea, even if the entire network cost disappeared, cost falls 11% at most | RATIO ≤1.12, realistically about 1.05
VERDICT | DEAD | Deployed optical circuit switches reconfigure about 1,000x too slowly for per-layer MoE phase changes. Even a free network could not bring inference cost below 1/1.12 of today's.
NEW FACT | The hardware switching time of 3D-MEMS optical circuit switches (10–100 ms) is one of the two main parts of reconfiguration delay, the control plane is the other, and Google gets around it by reconfiguring rarely | https://leed.sysnet.ucsd.edu/papers/Mordia.pdf

These are estimates, not measurements. I didn't run a quantization test for Idea 2 because it can't be done quickly. Several inputs are my own estimates (marked est.): the chip's ~60% share of IT power, the ~50% weight-streaming share of decode time, and the 10 ms/token decode pace. The arithmetic is saved in `gate_calc.py` in the working directory; nothing was committed.

Sources:
- [Synopsys: Why Dynamic Power Management Demands Adaptive Clocks](https://www.synopsys.com/blogs/chip-design/dynamic-power-management-demands-adaptive-clocks.html)
- [IBM: dynamic guardband features of the IBM z17](https://research.ibm.com/publications/dynamic-guardband-features-of-the-ibm-z17-system)
- [RealWorldTech: Adaptive Clocking in AMD's Steamroller](https://www.realworldtech.com/steamroller-clocking/)
- [QTIP, arXiv 2406.11235](https://arxiv.org/pdf/2406.11235)
- [GLVQ, arXiv 2510.20984](https://arxiv.org/pdf/2510.20984)
- [EE Times Asia / TechInsights: ISSCC 2024 memory day](https://www.eetasia.com/?p=57311)
- [Mordia (UCSD)](https://leed.sysnet.ucsd.edu/papers/Mordia.pdf)
- [DCD: Mission Apollo](https://datacenterdynamics.com/en/analysis/mission-apollo-behind-googles-optical-circuit-switching-revolution-mag)
- [SemiAnalysis: Google Apollo](https://www.semianalysis.com/p/google-apollo-the-3-billion-game)