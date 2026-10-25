=== REVIEW ===
IDEA 1: N6 SRAM-chiplet pipeline packages
DEFECT | FATAL | The SRAM won't fit on the die. 112 GB over 512 dies is 219 MB per 100 mm² die, which takes 118 mm² of SRAM alone at the measured V-Cache density, leaving no room for logic. | 112e9/(32×16) = 218.75 MB; at 14.2 Mib/mm², that is 117.5 mm². At the 124 MB per die that Idea 6 corrects to, the build needs about 903 dies and 28 packages, so silicon and package cost rise 1.76×.
DEFECT | MAJOR | "GB300's cost at 20× the speed" does not hold. The researcher's own repair (Idea 6) finds $0.14–0.23/Mtok, which is 2–4× more per token than GB300 at 50 tok/s. $0.07 only works as BOM cost at 100% utilisation. | My calculation for 32 users × 1,000 tok/s and a $168k system over 3 years at 100% utilisation gives $0.055/Mtok for capex alone, before markup, host, facility or energy.
DEFECT | MAJOR | 1,000 tok/s/user is not reachable with a die-by-die pipeline. The hop count alone uses about half the 1 ms token budget, and the researcher's previous check found that per-user speed halves. | 512 stage hops × about 1 µs on organic links is about 0.5 ms, against a budget of 1 ms per token.
DEFECT | MINOR | KV room is tiny: 42 GB serves only about 31 users at 8K context with FP8 KV. | 80 layers × 8 heads × 128 × 2 = 160 KB per token; 42 GB / (160 KB × 8,192) = 31 users.
SURVIVES | 8 KB per token of activations (8,192 × FP8) is correct, and $0.1/MB for N6 SRAM is about right.
RATIO | ~1.5 | After correcting to Idea 6's cost, compared with the Cerebras/Groq price for 70B at ≥1,000 tok/s. Against GB300 at normal speed it is 0.3–0.5.
KNOWN | partly | The Groq LPU, and d-Matrix Corsair, which puts SRAM chiplets on an organic package.

IDEA 2: SRAM-stacked weights, HBM4 only for KV
DEFECT | FATAL | 10 GB of SRAM in two base dies per 800 mm² compute die (about 1,600 mm² per package) needs 53.7 Mb/mm², more than a 0.021 µm² bitcell gives even at 100% array efficiency. At realistic macro density a package holds about 4.7 GB, so 64 packages give about 300 GB, not 640 GB, and cannot hold the 377 GB of weights. | 1/0.021 µm² = 47.6 Mb/mm² as the ceiling. TSMC's N2 macro reaches 38.1 Mb/mm² at ISSCC; 31.8 Mib × 0.7 × 1,600 mm² = 4.67 GB. Holding the weights needs at least 81 packages, 27% more power and HBM.
DEFECT | MAJOR | The tok/J and tok/s/kW figures must be equal (1 kW = 1,000 J/s), but they disagree by 1.25× for Continuum and 1.54× for Rubin. The headline "1.2× per J, 1.5× per kW" split is therefore an artifact of mixing power bases. | 6,200 tok/s/kW = 6.2 tok/J, not 7.75; 4,227 tok/s/kW = 4.23 tok/J, not 6.5.
DEFECT | MAJOR | 2.6 GB per user at 128K assumes 4.5-bit MLA KV. The production FlashMLA format is 656 B per token per layer, about 2× more, so capacity is about 2,600 users, not 5,300. | 576 × 61 × 4.5/8 = 19.8 KB per token, against 656 × 61 = 40 KB (FlashMLA README).
DEFECT | MAJOR | The "HBM per stack" metric hides that the package still needs CoWoS-L for 6 HBM4 stacks, plus SoIC hybrid bonding for 4 large base dies. That is two scarce packaging flows, not fewer. | 2 × 800 mm² logic + 4 base dies + 6 HBM4 is larger than a Rubin package.
DEFECT | MINOR | 893k tok/s at 32K requires about 59% utilisation of the rack's FP8 compute on attention, which the design does not state. | 631 GFLOP per token × 893k tok/s = 563 PF, against 960 PF.
SURVIVES | 377 GB at 4.5 bits, 36 GB HBM4 stacks, 307 W for SRAM at 0.3 pJ/bit, and 2,325 tok/s per stack (as stated).
RATIO | ~1.1 | Per-kW lead after resizing to ≥81 packages and using the real KV format.
KNOWN | partly | AMD 3D V-Cache (SoIC); Nvidia's pairing of Groq 3 LPX SRAM racks with Rubin for decode.

IDEA 3: Layer-pipelined LPDDR prefill dies
DEFECT | MAJOR | The memory-cost advantage is eroding: 2026 LPDDR5X contract prices have roughly doubled to about $10–21/GB, so 64 GB costs $0.6–1.3k per die. | TrendForce and SemiAnalysis via Wccftech: long-term agreements at $500–1,350 per 64 GB.
DEFECT | MINOR | The compute-bound threshold is understated. Reading all weights once per pass needs about 58K tokens, and judged per expert it needs about 131K, not 45K. | Ridge = 20 PF / 1.37 TB/s = 14.6K FLOP/B; 14.6K × 376 GB / 94 GFLOP per token ≈ 58K.
DEFECT | MINOR | The 2.7× win over B200 is against an outdated baseline. The relevant comparisons are Rubin and Rubin CPX. | (none)
SURVIVES | 47 GB per die, 1.37 TB/s from 1024-bit LPDDR5X, 2.3–5 GB/s of KV egress, and a TTFT of about 0.5–0.7 s all reproduce. Power per PF is roughly equal to Rubin's (59 vs 66 W/PF at 2.3 kW).
RATIO | ~1.2 | Against Rubin CPX, after the LPDDR price rise.
KNOWN | yes | Nvidia Rubin CPX (GDDR7 prefill part), plus DistServe/Splitwise disaggregated prefill.

IDEA 4: Detached attention-stack memory nodes
DEFECT | MAJOR | SPHBM4 is a 512-signal serialized host interface on organic substrate, not a networked memory node. Each of the 400–760 nodes per Rubin needs its own board, link and power. That overhead is not costed and could add 15–30% to the KV tier. | JESD330-4 (13 Jul 2026): 512 signals at 22.4–46 GT/s.
DEFECT | MAJOR | Putting 13–19 W of logic in the base die, under 12–16 DRAM dies, roughly doubles stack power. DRAM above about 85–95 °C needs more refresh or fails, and the design gives no thermal budget. | (none)
DEFECT | MAJOR | The Rubin-only baseline is a strawman, since it fits about 10 users at 128K. A competent operator would use NVFP4 KV, MLA, or sparse attention (DSA top-2048), which cut KV bytes read by 2–60×. | 160 KB per token × 131K = 21 GB per user; 288 GB of HBM holds about 10 users after weights.
DEFECT | MINOR | 49 tok/s/user is under a quarter of the ≥200 target set in Idea 2. | 2.5 TB/s / 24 GB = 104 tok/s per stack.
SURVIVES | 2 users per stack, about 0.26 GB/s of link traffic, and about 34 TF of attention per stack at 13–19 W all reproduce.
RATIO | ~1.3 | The claimed 1.7× less node overhead, against an unchanged GQA baseline.
KNOWN | partly | JEDEC SPHBM4, Samsung HBM-PIM, SK hynix AiM, and custom HBM4 base dies.

IDEA 5: Deterministic low-latency scale-up fabric
DEFECT | MAJOR | The DeepEP figures cited as proof of fixed latency are actually bandwidth-limited: 7.3 MB at 98 GB/s takes 75 µs, against 77 µs measured. They do not show that latency per layer is fixed. | DeepEP README: 128 tokens, top-8, 7,168 hidden, about 50 GB/s InfiniBand.
DEFECT | MAJOR | Batch 4,096 at 1,000 tok/s/user is impossible. It needs 2.6 EF against a 960 PF rack. At that batch each package needs an average of 0.67 TB/s, not 0.1 TB/s, and 3.7 MB of dispatch takes 2 µs of the 6 µs per-layer budget. The stated tok/s/kW implies a batch of about 573. | 4.1M tok/s × 631 GFLOP; 64 tokens × 8 × 7,168 B per layer per package; 3,978 × 144 / 1,000 = 573.
DEFECT | MAJOR | The design inherits Idea 2's SRAM overstatement: 64 packages cannot hold the 377 GB of weights. | ~4.7 GB per package
DEFECT | MAJOR | The per-J and per-kW comparison with Groq is inconsistent with itself by 2.9×. On top of that, LPX power is a guess. | 2.15 tok/J against 0.747 tok/J implied by 747 tok/s/kW.
DEFECT | MINOR | Cerebras' 2,500 tok/s on an 80-layer 70B model implies about 5 µs per layer, not 10. | 1/(2,500 × 80) s = 5 µs.
SURVIVES | The 16.4 µs per-layer budget at 1,000 tok/s, the 12 µs and 20 µs feasibility limits, and the Groq-3 chip count (at least 754 chips for weights) all reproduce.
RATIO | ~1.5 | Against Groq 3 LPX, with the power-base inconsistency removed.
KNOWN | yes | NVLink 6 already gives 1.8 TB/s per direction in a single-hop domain; Groq RealScale and TPU ICI already use static scheduling.

IDEA 6: N6 SRAM chiplets, package-wide tensor stages
DEFECT | MAJOR | Cost is quoted only at 8K context. Because KV lives in SRAM, 32 users at 32K need 136 GB (2.1× the dies), so cost is about $0.30–0.48/Mtok and the lead over Groq falls to 1.6–2.6×. At 128K they need 426 GB. | Weights 39.7 GB + 32 × ctx × 90 KB.
DEFECT | MAJOR | The 1 µs all-reduce across 32 dies on an organic package is unproven, and speed rests on it. At the stated 50% MAC efficiency the design is already below its target, at 916 tok/s. | 17 × 49.1 µs = 835 µs gives 1,198 tok/s.
DEFECT | MINOR | The baseline is old Groq pricing. Groq 3 now has 500 MB per chip, more than 2× the original LPU's 230 MB. | Nvidia LPX rack: 256 × 500 MB = 128 GB.
SURVIVES | 124 MB per die, 22.65 TF, 544 dies in 17 stages, 64 GB at 8K, and about 13× lower capex per GB than CS-3 all reproduce.
RATIO | ~1.6 | At 32K context, against Groq/Cerebras list prices (the $0.23 already includes 2× markup).
KNOWN | partly | d-Matrix Corsair and Groq.

IDEA 7: Same die, separate training/prefill SKU
DEFECT | MAJOR | A compute die designed to sit on SRAM base dies has little on-die SRAM. Without them, training GEMM and attention tiling (B200 uses 126 MB of L2) suffers, so the 0.6–0.85× estimate is unsourced and probably optimistic. | (none)
DEFECT | MAJOR | 8 HBM4 stacks mean CoWoS-L, the scarce resource the rest of the design avoids, plus the cost of a second package design for a product admitted to be uncompetitive. | (none)
SURVIVES | Post-training quantization to NVFP4 without retraining is plausible, with about 1% accuracy loss on DeepSeek-R1 FP4. Non-portable CUDA kernels and padded shape buckets are stated honestly.
RATIO | ~0.7 | The design's own range for training.
KNOWN | yes | Rubin CPX alongside Rubin, and Google's TPU v5e/v5p split.

IDEA 8: Continuum-D: SRAM weights, LPDDR KV
DEFECT | MAJOR | The energy figure doesn't reproduce: 117 kW / 414k tok/s = 0.283 J/token, not 0.19–0.20. That makes it about 1.5× worse than Rubin, not 9% worse. | 117e3 / 414e3
DEFECT | MAJOR | The Rubin baseline ($0.214 at ≥1,000 tok/s/user) contradicts Idea 5, which says no Rubin setup reaches that speed. The valid baseline is Groq 3 LPX at an assumed $4M per rack. | (none)
DEFECT | MAJOR | Reliability is not addressed. 333 dies each hold unique weights, so one die failure stops the system; KV mirroring doesn't help. At GPU-like failure rates (Meta's Llama 3 run) the system would fail about every 6 days, plus failures from about 2,000 DRAM packages. | 16,384 × 54 days × 24 h / 419 interruptions ≈ 50.7k h per device; divided by 333 ≈ 152 h.
DEFECT | MINOR | 1 TB/s from 26 × 24-bit LPDDR6 channels needs at least 12.8 Gbps; at the launch speed of 10.667 Gbps it gives 0.83 TB/s. 16 TB of LPDDR at $10–20/GB is $160–320k of a $0.81M BOM. | 26 × 24 × 10.667 / 8
SURVIVES | 377 GB, 428 mm² of SRAM, 514k tok/s from LPDDR, an 85 µs hop floor (11.8k tok/s ceiling), and $0.077 at about 70% utilisation all reproduce.
RATIO | ~1.5 | Against Groq 3 LPX; the LPX price is uncertain.
KNOWN | partly | Groq 3 LPX holds SRAM-resident weights and leaves KV to Rubin.

IDEA 9: Ridge point matched to MLA decode
DEFECT | MAJOR | The production MLA KV format is 656 B per token per layer (FP8 NoPE plus scales plus BF16 RoPE), not 324 B. That gives 425 FLOP/B, so on a 1,000 FLOP/B chip decode attention is memory-bound and the "compute decides tok/J" conclusion flips. | FlashMLA README; 278,528 / 656 = 425.
DEFECT | MAJOR | Sparse attention, which the design says it would need, already ships (DeepSeek V3.2 DSA, top-2048). At 128K it cuts attention FLOPs by about 64×, so the 15 PF / 15 TB/s balance is wrong for current frontier models. Speculative decoding (MTP) moves the intensity the other way, by k×. | 131,072 / 2,048 = 64
DEFECT | MINOR | Rubin's ridge (about 800 FLOP/B) is already below 860, so Rubin is compute-bound too. The 1.08× comes only from the assumed 0.1 pJ/FLOP against Rubin's about 0.13. | 2.3 kW / 17.5 PF
SURVIVES | 17.0 MFLOP per context token, 19.8 KB, 860 FLOP/B, 55.7 mJ and 21 mJ at 32K, and Ironwood's ridge of about 625 all reproduce.
RATIO | ~1.0 | No real lead.
KNOWN | partly | DeepSeek FlashMLA and DSA.

IDEA 10: Cheap-node HBM decode tier
DEFECT | FATAL | On the design's own target (MLA MoE at 860 FLOP/B), 3 PF cannot keep 22 TB/s busy; it needs about 19 PF. Per-package throughput at 32K is 4.8k tok/s against Rubin's 27.7k, so cost per tok/s is about 2× worse. | $16k / 4.8k against $45k / 27.7k
DEFECT | MAJOR | 3 PF of FP8 on N6 needs 3,300–4,000 mm² of logic (4–5 reticle-size dies) drawing about 1.65 kW. Energy is therefore not halved, and $2k is too little to package 5 dies with 8 HBM4 stacks on CoWoS-L. | 3,000 / 0.755–0.9 TF/mm²; 3e15 × 0.55 pJ
DEFECT | MAJOR | The baseline compares a street price with cost of goods. If only the package changes (about 60% of capex) and energy stays at parity, the ratio is 1.54, not 2.7. Against Rubin or a TPU at cost, the gain is only the logic saving, about 1.1×. | 1/(0.91 × 0.613 + 0.09) = 1.54
SURVIVES | The $12k for 288 GB of HBM (about $42/GB) is plausible. The idea does work for GQA models, which need only about 16 FLOP/B.
RATIO | ~0.5 | MLA target workload (about 1.1 for GQA at cost).
KNOWN | partly | AWS Inferentia/Trainium and Meta MTIA (cost-node inference ASICs at cost).

NEW FACT | Groq 3 LPU has 500 MB SRAM and 1.2 PF FP8 per chip; an LPX rack has 256 chips and 128 GB | https://developer.nvidia.com/blog/?p=114202 , https://www.eesel.ai/blog/groq-3-lpx
NEW FACT | SPHBM4 is published as JESD330-4 (13 Jul 2026), with 512 data signals at 22.4–46 GT/s on organic substrate | https://www.tomshardware.com/pc-components/dram/jedec-releases-new-sphbm4-standard-to-slash-ai-memory-costs-narrow-512-bit-interface-enables-dropping-expensive-interposers-for-organic-substrates
NEW FACT | The TSMC N2 SRAM macro reaches 38.1 Mb/mm² (ISSCC 2025) | https://spectrum.ieee.org/sram-intel-tsmc
NEW FACT | Rubin is listed at about 17.5 PF dense FP8 and 2.3 kW TDP (secondary sources disagree) | https://www.cudocompute.com/products/nvidia-vera-rubin
NEW FACT | 2026 LPDDR5X long-term agreements run about $7.8–21/GB | https://wccftech.com/mobile-dram-prices-expected-to-increase-by-100-quarter-over-quarter-as-long-term-agreements-now-getting-signed-at-prices-as-high-as-21-gb/amp/
NEW FACT | DeepEP's low-latency benchmark used 128 tokens per batch on 400 Gb/s CX7 InfiniBand (EP8 dispatch 98 GB/s) | https://github.com/coderzc/DeepEP
NEW FACT | FlashMLA's FP8 KV format is 656 B per token per layer, with RoPE kept in BF16 | https://gittrend.io/repo/deepseek-ai/FlashMLA