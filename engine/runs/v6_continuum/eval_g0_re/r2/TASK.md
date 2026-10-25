# Task: check the deciding numbers independently

QUESTION: Propose a new architecture for an AI accelerator chip, named "Continuum", that could credibly be called the best in the world. The asker has not said which workloads count: training, inference, or both. They have not said what "best" is measured by, or which kind of target (data center, edge, or other) the chip is for. A good answer therefore has to state its own target workloads and metrics, then defend the architecture against the current leading designs. Those designs include GPUs such as the Nvidia Rubin class, Google TPUs such as Ironwood, and SRAM-centric dataflow chips such as Cerebras WSE-3 and Groq LPU. The architecture should cover compute, memory hierarchy, interconnect, numerics, programming model, packaging and power. It should cite known physical, economic and manufacturing limits, and say what would need to be true for it to work. Reported 2026 reference points are listed in CONTEXT. Many are vendor or blog figures, and the sources disagree on some numbers.
A good answer: 
- The answer states explicit target workloads and a metric set. Examples are tokens/s per user, tokens per joule, cost per token, and training throughput. It says why those metrics define "best".
- It describes a coherent architecture with named blocks and quantified estimates. Estimates cover compute, on-chip and off-chip memory capacity and bandwidth, interconnect, power and die or package size. They are sanity-checked against roofline or bandwidth arithmetic.
- It compares quantitatively against at least three current designs (GPU, TPU, SRAM/wafer-scale) and says where Continuum wins, where it loses, and by how much.
- It names the main risks and the physical, process or supply limits (HBM supply, CoWoS packaging, power density, yield). It gives a falsifiable test or simulation plan that could prove the design wrong.
- It covers the software stack and programming model, and says what happens to existing models and frameworks.
- It separates established facts from the design's own assumptions and estimates.
- "Best in the world" is not asserted without evidence. Trade-offs are stated honestly.
Constraints: 
- The name is "Continuum".
- The answer is an architecture for an AI chip.
- Nothing else was specified. The answer must be a real, physically plausible design, not marketing text.

For each idea below, an earlier check named the one quantity most likely to decide whether it works. Estimate that
quantity yourself, independently: what the idea REQUIRES at the scale it claims, and what is AVAILABLE, from measured
data or exact arithmetic, each with a source. You are not shown the earlier numbers on purpose. Tools: WebSearch
(WebFetch does not reach hosts here; use excerpts) and Bash with python3. About 3 searches per idea. Do not judge the
ideas otherwise and do not improve them. Work only in `/home/user/SomeRepository/engine/runs/v6_continuum/eval_g0_re/r2/`: write files only there, do not commit.

Facts collected for this question (data; check a decisive one before relying on it):
(a slice: all 0 HARD facts and the 12 of 13 other facts that bear most on these candidates, sources omitted; the full ledger with sources is /home/user/SomeRepository/engine/runs/v6_continuum/evidence.md - read it if you need a source or a fact that is not here)
FACT 1: AMD's 64 MB V-Cache die is about 36 mm² on N7 (41 mm² in the first generation), which is about 14.2 Mb/mm² for a dense SRAM-only die | NEW from eval_g0, check before relying on it
FACT 3: imec's 3D HBM-on-GPU study measured a 141.7 °C peak against 69.1 °C for the 2.5D layout. Halving the GPU clock was needed to get below 100 °C and cost 28% of training speed. | NEW from eval_g0, check before relying on it
FACT 4: On 2-bit Llama-2-70B, WikiText-2 perplexity is 3.78 for QTIP and 3.91 for QuIP#, against 3.12 for FP16 | NEW from eval_g0, check before relying on it
FACT 5: Palu: a 30% low-rank cut loses under 1% average on LongBench; 3-bit latents add under 1% more; 11.4× total compression "while maintaining perplexity"; tests went only up to 32K | NEW from eval_g0, check before relying on it
FACT 6: vLLM's FP8 MLA KV layout for DeepSeek-V3.2 is 656 bytes per token per layer, and the indexer K-cache is a separate buffer; top-k = 2048 in the released code | NEW from eval_g0, check before relying on it
FACT 7: imec IEDM 2025: 4 stacks of 12-high hybrid-bonded HBM placed on a GPU push the GPU peak from 141.7 °C down to 70.8 °C only with mitigations | NEW from eval_g0, check before relying on it
FACT 8: UniIC VLSI 2023: "135 GBps/Gbit, 0.66 pJ/bit stacked embedded DRAM with multilayer arrays by fine-pitch hybrid bonding and mini-TSV", 2048 I/Os per Gbit at 541 Mbps; the IEDM 2020 generation gave 34 GB/s/Gb at 0.88 pJ/b, and two SoCs on it are in mass production | NEW from eval_g0, check before relying on it
FACT 9: Rubin CPX is a single monolithic die, not the Rubin compute die, with 128 GB GDDR7 and 30 PF NVFP4. The NVL144 CPX rack is rated at 8 EF, 100 TB of fast memory and 1.7 PB/s | NEW from eval_g0, check before relying on it
FACT 10: MiniMax-M2: 62 layers, 8 KV heads, head_dim 128, 256 experts with top-8 routing | NEW from eval_g0, check before relying on it
FACT 11: Cerebras CS-3 price is unpublished; estimates are ~$2.5M per node, ~$3.2M per system, and ~$4M with MemoryX/SwarmX | NEW from eval_g0, check before relying on it
FACT 12: Rubin GPU HBM4 is reported at up to 22 TB/s per GPU, with a ~2,300 W TDP from analyst estimates that Nvidia has not confirmed; one source warns that initial bandwidth may fall below 22 TB/s | NEW from eval_g0, check before relying on it
FACT 13: HBM3E access energy is ~3.44 pJ/bit in one model and ~5.74 pJ/bit including I/O in another; HBM4 has no primary pJ/bit figure | NEW from eval_g0, check before relying on it

Final answer (text only), one line per idea in the order given:
=== RECHECK ===
IDEA 1: <quantity> | required <number unit> (<source>) | available <number unit> (<source>) | MARGIN <available / required, a number>
(same for the other ideas)

THE 10 IDEAS:
IDEA 1
NAME: N6 SRAM-chiplet pipeline packages
MECHANISM: Weights and KV cache live in about 112 GB of SRAM spread over many dies of about 100 mm² on N6. That node is chosen because SRAM stopped shrinking, so SRAM bytes cost about half as much there as on N3. Thirty-two dies sit on each organic package, and 16 packages hold one 70B model. A compiler pipelines the layers so that only about 8 KB of activations per token crosses the organic links. Closest earlier attempt is the Groq LPU, where 576 chips on 14 nm cards made capacity cost too high. Here SRAM is bought at roughly $0.1/MB on dense, cheap packages instead. The deciding quantity is delivered system cost per GB of SRAM, which must stay at or below about $1.5k/GB.
VALUE: It serves a 70B model at about 1,000 tok/s/user for about $0.07/Mtok, which is GB300's cost at 20x the speed, using no HBM and no CoWoS.
DECIDING QUANTITY: delivered system $ per GB of SRAM, which depends on how many MB fit on a ~100 mm² N6 die

IDEA 2
NAME: 4.5-bit numerics, compiler-placed memory, kill gates
MECHANISM: Weights and KV are stored as NVFP4/MXFP4 at about 4.5 bits, activations are FP8, and accumulation is FP32. Existing checkpoints run after post-training quantization; they do not need retraining. The software stack is PyTorch/JAX → torch.export/StableHLO → MLIR, with Triton-style tile kernels and vLLM/SGLang backends. The compiler places experts statically in stacked DRAM and pages the KV cache. CUDA-only kernels need porting, which is the adoption cost. Five tests could kill the design: 1. Recalibrate the model against MLPerf and Artificial Analysis. Drop the design if the GQA-128K lead is below 1.5×. 2. Run 3D thermal and power simulation (3D-ICE/HotSpot plus a power-integrity tool). It fails if DRAM runs above 95 °C, or if IR drop exceeds 5% while delivering about 2,700 A at 0.75 V through the DRAM stack. 3. Model the DRAM in CACTI-3DD/Accelergy. It fails above 1.5 pJ/bit or below 40 TB/s per package. 4. Simulate in LLMCompass with real expert-routing traces. 5. Run RULER at 128K with NVFP4 KV. The numerics plan fails if it loses more than 1 point against BF16.
VALUE: Models and frameworks carry over with quantization only, and every headline ratio has a test that can prove it wrong before tape-out.
DECIDING QUANTITY: peak temperature of DRAM stacked on a roughly 2 kW logic die. The idea's own gate is DRAM ≤95 °C.

IDEA 3
NAME: Hash-Regenerated Trellis Weight Decoder
MECHANISM: Weights are stored as about 2-bit trellis codes with per-block scales. A small hash circuit at each SRAM or HBM read port regenerates the codebook values, so no table is stored. The circuit emits FP8 operands straight into the MACs. The closest earlier attempt is QTIP-style decoding in software on GPUs, which steals ALU cycles at large batch; fixed logic at the port removes that cost. The deciding quantity is decode energy per weight, which must be ≤0.1 pJ.
VALUE: A 70B model needs 4× fewer SRAM bytes, so it fits on one wafer or about 35 LPUs, and batch-1 HBM decode is 4× faster.
DECIDING QUANTITY: quality loss at about 2 bits per weight. The idea's stated deciding quantity was decode energy; I chose quality instead because it fails first at the scale the idea needs.

IDEA 4
NAME: Stacked-SRAM weights, HBM-only KV package
MECHANISM: Each package has two compute dies of about 800 mm² each on N2/N3, rated at about 30 PF dense FP4 and 15 PF FP8. Each compute die sits face-to-face on an 800 mm² SRAM base die. Older-node SRAM at about 30 Mb/mm² gives about 2.25 GB per die, so roughly 4 GB per package. At about 14k bonds/mm² across 40 mm² of signal area, each die gets about 210 TB/s, so about 300 TB/s per package at about 0.12 pJ/bit. Eight HBM4 stacks add 288 GB at 22 TB/s, which is about 3 pJ/bit. The model's 545 GB of weights are pinned across the SRAM of a 144-package domain (136 packages minimum). HBM then carries only KV cache, so weight reads and KV reads no longer compete for the same bandwidth. Earlier runs found weight reads take 23–36% of GPU HBM time. Power at full load is about 288 W (SRAM) + 528 W (HBM) + 900 W (compute at 0.12 pJ per FP8 multiply-accumulate) + about 250 W of I/O, roughly 2.0 kW, inside a 2.3 kW package. That is the same class as Rubin's reported 1.8–2.3 kW. The package needs CoWoS-L at about 4.5× reticle, like Rubin, plus TSMC's SoIC hybrid bonding. The model gives these per-MW results against the best incumbent: - **8K context:** 18.6 vs 16.5 Mtok/s/MW at ≥100 tok/s/user (1.12×); 18.6 vs 13.2 at ≥300 (1.41×). - **128K context:** 2.55 vs 2.23 at ≥100 (1.14×); 2.38 vs 1.51 at ≥300 (1.58×). - **Losses:** prefill FLOPs per watt are about 0.91× Rubin, and capex is about 10–15% higher (my estimate) for the SRAM dies and bonding.
VALUE: Cost per token comes out about 1.1–1.6× lower than Rubin NVL72 at interactive speeds (an estimate). It needs about 8× fewer SRAM chips than Groq LP30 (136 vs 1,064) and, unlike Cerebras, it doesn't cap concurrency: the modelled CS-3 cluster fits only about 15 users at 128K context.
DECIDING QUANTITY: SRAM capacity per package for pinning 545 GB of weights in a 144-package domain

IDEA 5
NAME: Latent KV With Outlier Sidecar
MECHANISM: Keys and values are cached as per-head low-rank latents at 3–4 bits, with per-block scales. The few outlier channels go to a small FP16 sidebuffer. Expansion happens inside the attention unit, so full-width KV never crosses memory. The closest earlier attempt is FP8 KV, which saves only 2× and still grows linearly with full width. The deciding quantity is accuracy retained at 128k context.
VALUE: KV bytes per token fall about 6–8×, so long-context serving no longer sets the chip count.
DECIDING QUANTITY: KV compression versus FP16 reached at ≤1% accuracy loss at 128K context

IDEA 6
NAME: Near-HBM sparse-KV gather attention engine
MECHANISM: Attention units sit beside each HBM4 controller. The KV cache is stored as 4.5-bit NVFP4 rows (324 B per token per layer for MLA) and read with a hardware top-k gather, in the style of DeepSeek's sparse attention (top 2,048 tokens plus a 128-dim FP4 index). At 128K context this cuts KV traffic per user-token from 2.59 GB to 0.62 GB. Dense MLA decode needs 1.18 TFLOP per user-token at 128K, about 450 FLOP per byte at FP4 KV. So the HBM-side attention units are sized at about 10 PF FP8 (≈22 TB/s × 450) rather than relying on the main arrays. With sparse attention, Continuum gets 9.39 Mtok/s/MW against Rubin's 5.74 (1.64×) and Ironwood's 7.04 (1.33×). The model assumes the gather sustains at least 80% of HBM peak at 324 B granularity; only a DRAM simulator or silicon can confirm that.
VALUE: Long-context throughput per MW rises about 3.7× over dense attention on the same hardware, and Continuum keeps a 1.3–1.6× lead over incumbents running the same sparse model.
DECIDING QUANTITY: heat from about 10 PF FP8 of logic in the HBM4 base dies, which sit under the DRAM

IDEA 7
NAME: Hybrid-bonded DRAM-on-logic decode package
MECHANISM: Continuum targets one workload: decode for frontier sparse-MoE LLMs (1T total / 32B active parameters) at 8K–128K context. The main metric is tokens/s per kW at a per-user speed target (100, 400 or 1000 tok/s/user), with tokens per joule second. Peak FLOPS is not a metric. Serving revenue comes from throughput at an interactivity target, and running cost comes from joules. The package has four ~400 mm² N2-class logic chiplets. Each sits on top of a 4-high custom DRAM stack, bonded die to die at ≤9 µm pitch (hybrid bonding). That gives 160 GB at 64 TB/s per package, at about 0.8 pJ/bit. HBM is around 3 pJ/bit (my estimate), and a published 3D-DRAM estimate gives 0.66–0.88. Compute is 40 PF dense FP4 and 20 PF FP8, in a ~2.0 kW package. Stacked-DRAM power is 64 TB/s × 8 × 0.8 pJ = 410 W. FP8 at full rate would be about 1.6 kW, so the 2 kW budget is shared and the memory and FP8 cannot both run flat out. The package has no HBM. My model found that adding an HBM tier lowered tokens/s per kW, because each decode step reads all resident bytes and the slow tier sets the step time. On the same 4.5-bit weight and KV format, the roofline/energy model compares it with Rubin (288 GB, 22 TB/s, ~1.8 kW). For GQA models, Continuum gets 2.2–2.7× the tokens/s per kW and 2.3–2.5× the tokens/J, at both 8K and 128K. For dense-MLA models it gets only 1.08–1.29×, because MLA decode at 128K costs about 1.1 TFLOP per token in attention and is compute-bound.
VALUE: In my model, Continuum gives about 2.2–2.7× more decode tokens per kW than Rubin on GQA models (2.8–3.8× vs Ironwood, 4–18× vs Groq LP30 and WSE-3). That is a modeled result, not a measured one, and it hinges on the stacked DRAM really reaching ≤1 pJ/bit and 64 TB/s.
DECIDING QUANTITY: hybrid-bonded DRAM capacity per package at 64 TB/s, which needs 0.20 Gb/mm² per DRAM die and 50 GB/s/Gb

IDEA 8
NAME: One compute die, two phase-split SKUs
MECHANISM: Prefill and training are compute-bound, so the SRAM base die adds cost there without adding speed. A "C" SKU uses the same compute die on a plain interposer with HBM only, while the "D" SKU described above handles decode. They are mixed at a measured prefill-to-decode ratio, like Nvidia's CPX/Rubin pairing at 1:1. Training on the C SKU sits at about 0.86–1.0× Rubin per package (30 vs 35 PF FP4) because the compute die and HBM are the same class. I make no claim that it wins at training.
VALUE: It avoids the roughly 10–15% SRAM cost on compute-bound work and shares one tape-out between both SKUs. Training is at parity, not best.
DECIDING QUANTITY: C-SKU training throughput per package compared with Rubin

IDEA 9
NAME: SRAM-resident MoE expert farm
MECHANISM: All experts of a model with about 230B total and 10B active parameters stay resident in about 300 GB of N6 SRAM chiplets, roughly 2.5 to 3 wafers. A deterministic all-to-all over organic links moves only a few tens of KB per token per layer. The compiler replicates hot experts based on measured routing statistics. Closest earlier attempt is Cerebras streaming weights from MemoryX, which was bandwidth-bound off-wafer. Here nothing streams. The deciding quantity is the capacity needed to replicate hot experts, which must stay under 30%.
VALUE: It runs frontier MoE models at more than 500 tok/s/user near GB300's $/Mtok.
DECIDING QUANTITY: SRAM left for KV cache after the weights, measured as concurrent users at 500 tok/s on 8k-in/1k-out traffic (~9k-token context; MiniMax-M2 has 62 layers × 8 KV heads × head dim 128, so KV is 127 KB/to

IDEA 10
NAME: Decode-only part, disaggregated prefill/training
MECHANISM: I reject the premise that one chip should be best at training and inference. Prefill and training are compute-bound and need capacity: optimizer states, and prompts that use GDDR or HBM well, as Rubin CPX shows with 30 PF NVFP4 and 128 GB GDDR7. Continuum has 160 GB per package against Rubin's 288 GB, so it needs about 1.6–2× more packages for pools with very large KV caches. It also does not beat Rubin on training. The system therefore pairs Continuum decode racks with HBM or GDDR prefill/training parts, linked by KV transfer. Each package has 3.6 TB/s of NVLink-6-class scale-up, in 72-package copper racks. On maximum single-user speed it loses. Expert-parallel all-to-alls (120 per token × ~3 µs) cap it at about 2.8k tok/s/user, the same as Rubin. SRAM chips model at about 8k (Groq) and measure about 2.2k (Cerebras on gpt-oss-120B). Matching them would need about 1.5 µs collectives, which is unproven.
VALUE: Continuum is aimed at the bulk serving market, about 2× tokens per kW against Rubin + CPX-style disaggregation. It concedes ultra-low-latency single-user speed to Groq LPX and Cerebras, and training to Rubin and TPU.
DECIDING QUANTITY: Decode power per package at Rubin-class 22 TB/s. "2× tokens per kW" needs ≤ half of Rubin's decode draw (taken as 0.8 × ~2.3 kW TDP, an analyst estimate). The floor is HBM read at 3.44–5.74 pJ/bit, pl

