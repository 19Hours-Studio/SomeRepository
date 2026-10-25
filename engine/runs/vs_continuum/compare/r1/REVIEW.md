=== REVIEW ===
IDEA 1: Layer-pipelined LPDDR prefill dies
DEFECT | MAJOR | The 1.27× cost lead holds only while each die gets at least about 45K tokens per pass. Below that, weight streaming sets the pace, because one pass over a die's 7.6 layers takes about 36 ms whatever the batch size. | A die's ridge is 20 PF / 1.37 TB/s = 14,600 FLOP/B. One layer's weights take 4.74 ms to read. At 8K tokens per pass the die is about 20% utilized, and at 36K it is 80% (1.27 × 0.8 ≈ 1.0). So the lead disappears unless about 44 prompts of 8K are always queued.
DEFECT | MAJOR | The cost lead cannot come from the memory itself. Swapping HBM for LPDDR saves about $1–4K per Rubin-equivalent of compute, and 2026 LPDDR prices are eroding that. | 2.5 dies × 64 GB × $10–20/GB = $1.6–3.2K, against 288 GB HBM4 × $15–20 = $4.3–5.8K. LPDDR5X rose 58–63% QoQ in Q1 2026 and about 89% in Q2 (TrendForce/Utmel). The rest of the 1.27× is an assumed markup.
DEFECT | MINOR | Energy per FLOP is worse than Rubin if Rubin delivers its rated 50 PF NVFP4. | 59 W/PF for Continuum against 46 W/PF for Rubin (2.3 kW / 50 PF). It is only better if Rubin's dense figure is 35 PF (66 W/PF).
DEFECT | MINOR | 61 layers do not split evenly over 8 dies, so stages have 7 or 8 layers and the pipeline loses about 5%. | 8 / 7.625 = 1.049.
SURVIVES | 910 FLOP/B at 256 tokens per expert. Break-even of about 41–57K tokens at 50–70% MFU. 1.37 TB/s from 1024 bits × 10.7 Gb/s. Activations at about 15 GB/s and KV egress at about 4.7 GB/s per die (FP8). TTFT ≤0.69 s (I get 0.33 s). The HBM4 Rubin CPX revival is real: Kuo reports 168 GB HBM4 at 2,300 W.
RATIO | 1.05 | The capex saving is mostly markup. A thin margin depends on utilization, and the LPDDR price trend works against it.
KNOWN | yes | The original Rubin CPX (Sept 2025): a monolithic die, 30 PF NVFP4, 128 GB GDDR7, no HBM, no CoWoS, built for prefill. Per Kuo, Nvidia later moved it to HBM4, and German press reported it was "internally considered a failure". That is a negative signal for the no-HBM prefill premise.
NEW FACT | The revived CPX has 168 GB HBM4, 2,300 W, production 1Q27, and a standalone rack of 64–256 GPUs | technews.tw / overclocking.com (Kuo, Sept 2026)

IDEA 2: SRAM-stacked weights, HBM4 only for KV
DEFECT | MAJOR | 10 GB of SRAM cannot fit under two 800 mm² compute dies. If the base dies are wider than the compute dies, the design needs CoWoS-L/SoIC carriers of about 2,500 mm² of SRAM. | 1,600 mm² × 31.8 Mb/mm² = 6.36 GB at 100% macro fill, and realistically about 5 GB after power-TSV keep-out. 10 GB needs 2,516 mm². With 5–6.4 GB per package, the 377 GB of weights needs about 60–76 packages before any replication or slack, against the claimed 64. The rack power and HBM-stack savings shrink by up to about 20%.
DEFECT | MAJOR | "5,300 users at 128K" only works at about 70–79 tok/s per user, well under the design's own target of ≥200. | Reading a full 13.8 TB of KV each step at 960 TB/s gives 69.6 tok/s per user. The attention-compute ceiling is 417K tok/s / 5,300 = 79 tok/s.
DEFECT | MINOR | tok/J and tok/s/kW use different power boundaries, so "1.2× per J" and "1.5× per kW" are not two separate results. | 892,800 tok/s / 144 kW = 6.2 tok/J (not 7.75). Rubin: 875K / 207 kW = 4.23 tok/J (not 6.5).
DEFECT | MINOR | The claim that the cell has "stayed 0.021 µm² from N5 to N2" is wrong. | The N2 HD cell is 0.0175 µm² and about 38 Mb/mm² (TSMC IEDM 2024), so an N5 base die costs about 17–20% more area per bit.
SURVIVES | 2.59 GB per user at 128K and 0.648 GB at 32K (61 × 576 × 4.5 bit). 13.8 TB. 2,325 against 1,519 tok/s per stack. Groq 3 holds 500 MB per chip, so about 5 LPUs per user.
RATIO | 1.1 | Per kW, after correcting the SRAM capacity (more packages) and putting both designs on the same power boundary.
KNOWN | partly | Nvidia's Groq 3 LPX (500 MB SRAM per chip, 256 chips per rack) paired with Vera Rubin HBM. Logic-on-cache stacking: AMD X3D and MI300 (compute dies on top of base dies).

IDEA 3: Deterministic, compiler-scheduled low-latency scale-up fabric
DEFECT | MAJOR | "Bandwidth is not the hard part at batch 4096" is false. Within a 6 µs layer window, the all-to-all saturates the 1.8 TB/s link. | At batch 4096 a package sends 7.2–10.8 MB per layer, which is 1.2–1.8 TB/s peak in 6 µs and 0.44–0.66 TB/s on average (4–7× the stated 0.1 TB/s). Batch 4096 at 1000 tok/s per user and 32K context would need 2,585 PF of attention compute against 960 PF available. The claimed 573K tok/s implies a batch of about 573.
DEFECT | MAJOR | Fixed MoE slots have to be sized for the worst package in every layer and every step. Otherwise tokens are dropped, which changes the model's outputs. | Monte Carlo with uniform top-8 routing at batch 573: package load max/mean is 1.27 (median) and 1.44 (p99), and 1 − 0.99^61 = 46% of steps exceed p99 in at least one layer. Real DeepSeek routing is skewed (that is why EPLB exists). Slots therefore need about 1.5×+ overprovision, which adds to the 6 µs budget.
DEFECT | MAJOR | The GPU latency baseline is the wrong one. DeepEP's 77–369 µs figures are for H800 over CX7 InfiniBand with 128 tokens, not NVL72 NVLink. "No Rubin reaches 1000" also ignores MTP/speculative decoding, which helps every platform. | DeepEP README test setup. B200 already reached 250+ tok/s per user on 671B R1 and over 1000 on Llama-4 Maverick (Nvidia blog).
DEFECT | MINOR | Cerebras's "10 µs per layer" comes from smaller models, not the 671B model. | 2,500 tok/s on a 36-layer model works out to 11 µs per layer, so the comparison is not like for like.
SURVIVES | Per-user ceilings: 2,732 at 6 µs, 1,366 at 12 µs, and below 1000 (820) at 20 µs, all consistent.
RATIO | 1.5 | Against Groq 3 LPX after slot overprovision. The LPX per-chip power is still a guess, and the ≤6 µs figure is unproven.
KNOWN | yes | Groq LPU (static, compiler-scheduled chip-to-chip) and TPU ICI, both cited by the idea itself.

IDEA 4: Ridge point matched to MLA decode
DEFECT | MAJOR | The current DeepSeek line (V3.2, with DSA) moves decode attention from compute-bound to memory-bound, so 15 PF matched to 15 TB/s leaves compute idle. | At 128K with an indexer of 64 heads × 128 dims in FP8 plus top-2048 selection: 166 GFLOP over 1.10 GB, about 151 FLOP/B, against 2,228 GFLOP over 2.59 GB dense. That is 13× less compute and 2.4× fewer bytes.
DEFECT | MAJOR | 860 FLOP/B assumes the KV cache is stored in NVFP4. With FP8 KV (as V3.2 stores it, 656 B per token per layer) the intensity halves, which puts it under Continuum's 1,000 ridge. | 17e6 / (61 × 656) = 425 FLOP/B.
DEFECT | MINOR | The decisive 0.1 pJ per FP8 FLOP is assumed. A plausible range of 0.05–0.15 pJ moves attention energy from 28 to 84 mJ, which swamps the claimed 1.08×. | 557 GFLOP × 0.05–0.15 pJ.
SURVIVES | 17.0 MFLOP and 19.76 KB per context token. Ridge points of 1,000, about 800 (Rubin) and 624 (Ironwood). 56 mJ against 21 mJ (implying about 4 pJ/bit for HBM). The idea's own "not best at long context" disclaimer stands.
RATIO | 1.0 | 1.08× is inside the energy uncertainty. On DSA models it may be below 1.
KNOWN | partly | FlashMLA (compute-bound MLA decode on H800). DeepSeek-V3.2 DSA.

IDEA 5: Same die, separate training/prefill SKU
DEFECT | MAJOR | Continuum-T uses 8 HBM4 stacks on CoWoS. That is exactly the scarce supply the rest of the design is built to avoid, and it contradicts Idea 1, which shows prefill works without HBM. | 8 stacks is the same as Rubin's 288 GB / 36 GB. The design's own premise is that HBM is sold out for 2026.
DEFECT | MINOR | Padding dynamic shapes into fixed buckets wastes compute. | With power-of-two buckets the average waste is about 25% and the worst case about 50%.
DEFECT | MINOR | Production serving stacks rely on custom kernels (FlashMLA, DeepGEMM, DeepEP), so "a plugin for vLLM/SGLang" is really a full reimplementation.
SURVIVES | It honestly claims no lead in training (0.6–0.85×). NVFP4 PTQ of DeepSeek-R1 is published by Nvidia (I did not re-verify the accuracy myself).
RATIO | 0.7 | The idea's own range of 0.6–0.85× Rubin for training.
KNOWN | yes | Nvidia's Rubin / Rubin CPX split. The Groq, Cerebras and TPU compile flows (StableHLO/XLA).

IDEA 6: Continuum-D: SRAM weights, LPDDR KV
DEFECT | MAJOR | The energy figure does not match the stated power. | 117 kW / 414K tok/s = 0.283 J per token, not 0.19–0.20 (which would imply 81 kW). That makes it about 1.6× worse than Rubin's implied 0.175 J, not 9% worse.
DEFECT | MAJOR | The Rubin baseline contradicts Idea 3. Here, Rubin NVL72 serves at ≥1000 tok/s per user for $0.214/Mtok and about 5.7 tok/J. Idea 3 says no Rubin setup reaches that speed, and gives 0.64 tok/J even at 10 µs per layer. | That is a 9× gap between the two ideas on the same baseline. Either the 2.8× here or the "unreachable" claim in Idea 3 is wrong.
DEFECT | MAJOR | The $0.81M BOM underprices 16 TB of LPDDR6 at 2026 DRAM prices. | 333 × 48 GB = 16 TB. At $10–20/GB that is $0.16–0.32M (20–40% of the BOM), while N3 dies come to only about $0.2M. A BOM about 20% higher brings the 2.8× down to about 2.3×.
DEFECT | MINOR | Weights are not replicated, so a single die failure stops the whole 333-die machine. | Meta's Llama 3 run had 419 unexpected interruptions across 16,384 GPUs in 54 days, which gives about 50,700 h per device and a system MTBF of about 152 h (6 days).
DEFECT | MINOR | LPDDR6 at 26 x24 channels reaches 1 TB/s only at about 12.8 Gb/s per pin. | 832 GB/s at 10.667 Gb/s.
SURVIVES | 377 GB at 4.5 bits. 428 mm² of SRAM. 433 PF available against 261 PF needed. The LPDDR ceiling of 514K tok/s. The cost of about $0.055–0.07/Mtok over 3–4 years of amortization.
RATIO | 2.0 | At ≥1000 tok/s per user only, after the DRAM-price BOM correction and allowing for the unreliable baseline. About 1.0 at ≤500 tok/s per user.
KNOWN | partly | Groq LPU/LPX (SRAM weights over many dies). Cerebras WSE-3 (44 GB SRAM per wafer).

IDEA 7: Detached attention-stack memory nodes
DEFECT | MAJOR | The 48 GB (16-high) HBM4 stack is not in volume production in 2026. With the 36 GB 12-high stacks that Rubin ships, a stack holds 1 user at 128K, not 2. | 36 / 21.5 GB = 1.68, so 1 user. Micron's 10-K shows 48 GB 16H at the sample stage only. That doubles the node count per user.
DEFECT | MAJOR | The cost comparison is at a lower service level: 49 tok/s per user here against about 76 for Rubin-only. | At a matched 76 tok/s, a stack serves 2.07 TB/s / (76 × 21.5 GB) = 1.27 users, so the KV-node cost per token rises about 57%.
DEFECT | MAJOR | A narrow link sized to the 2 GB/s average makes loading a user's KV after prefill take seconds. A burst-capable NIC on each of 400–760 nodes per Rubin is not in the cost. | 21.5 GB / 2 GB/s = 10.7 s. At about $300–1,000 per port, that adds about $0.12–0.76M per Rubin.
DEFECT | MINOR | Adding a 13–19 W logic die under 12–16 DRAM layers raises stack power by about 50% against DRAM temperature limits of about 85–95 °C.
SURVIVES | 164 KB per token. 2,618 KB of link traffic per token (ratio 8,192). 0.26 GB/s. 33.7 TFLOPS on the base die. The 33% energy saving. SPHBM4 published as JESD330-4 on 13 July 2026.
RATIO | 1.1 | After correcting to 36 GB stacks, matched per-user speed, and NIC/port cost.
KNOWN | yes | AttAcc (ASPLOS 2024, attention in HBM-PIM), Samsung HBM-PIM / SK hynix AiM, and attention-disaggregation systems (Lamina, MegaScale-Infer).

Most severe across the set: Idea 2's SRAM capacity, the Rubin-baseline contradiction between Ideas 3 and 6, Idea 4's dependence on dense attention, and Idea 7's 48 GB stack.

The arithmetic script is at /tmp/claude-0/-home-user-SomeRepository-engine-runs-vs-continuum-compare-r1/86b61a25-826d-5e99-8ce4-43b0688ac74a/scratchpad/chk.py.

Sources:
- [Kuo: Rubin CPX re-enters roadmap with HBM4](https://technews.tw/2026/09/02/nvidia-rubin-cpx-reenters-roadmap-hbm4-ai-prefill/), [overclocking.com](https://overclocking.com/nvidia-rubin-cpx-hbm4-ming-chi-kuo/), [trading-treff (CPX considered failed)](https://trading-treff.de/trading/nvidia-aktie-rubin-cpx-gilt-intern-als-gescheitert), [TechRepublic: original Rubin CPX](https://www.techrepublic.com/article/news-nvidia-vera-rubin-cpx/)
- [Nvidia: Blackwell DeepSeek-R1 record](https://developer.nvidia.com/blog/nvidia-blackwell-delivers-world-record-deepseek-r1-inference-performance), [insideHPC: 1000 TPS/user on Maverick](https://insidehpc.com/tag/tps/)
- [HPCwire: Groq 3 LPU](https://www.hpcwire.com/2026/03/16/nvidia-boasts-7-chips-in-production-for-vera-rubin-platform-including-groq-3-lpu/), [The Register: LPX deep dive](https://www.theregister.com/2026/03/19/nvidia_lpx_deep_dive/)
- [vLLM: DeepSeek-V3.2 sparse attention](https://vllm.ai/blog/2025-09-29-deepseek-v3-2)
- [Tom's Hardware: JEDEC SPHBM4](https://www.tomshardware.com/pc-components/dram/jedec-releases-new-sphbm4-standard-to-slash-ai-memory-costs-narrow-512-bit-interface-enables-dropping-expensive-interposers-for-organic-substrates)
- [wccftech: mobile DRAM prices](https://wccftech.com/mobile-dram-prices-expected-to-increase-by-100-quarter-over-quarter-as-long-term-agreements-now-getting-signed-at-prices-as-high-as-21-gb/amp/), [Utmel: LPDDR5 2026](https://www.utmel.com/blog/categories/memory+chip/lpddr5-memory-2026-lead-times-hbm-impact-and-procurement-strategies)
- [SemiWiki: TSMC N2 SRAM](https://semiwiki.com/forum/threads/sram-scaling-isnt-dead-after-all-%E2%80%94-tsmcs-2nm-process-tech-claims-major-improvements.21363/latest)
- [2CRSI: Rubin NVL72 power](https://2crsi.com/nvidia-from-blackwell-to-rubin-platforms-power-and-cooling), [CUDO: Vera Rubin](https://www.cudocompute.com/products/nvidia-vera-rubin)
- [DeepEP README](https://github.com/deepseek-ai/DeepEP)
- [Micron FY2026 10-K](https://www.sec.gov/Archives/edgar/data/0000723125/000072312526000023/mu-20260903.htm), [Evertiq: Micron HBM4 36GB 12H](https://evertiq.com/news/2026-04-06-micron-begins-volume-shipment-of-hbm4-36gb-12h)