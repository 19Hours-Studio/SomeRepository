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
ideas otherwise and do not improve them. Work only in `/home/user/SomeRepository/engine/runs/v6_continuum/eval_g1_re/r1/`: write files only there, do not commit.

Facts collected for this question (data; check a decisive one before relying on it):
(a slice: all 0 HARD facts and the 12 of 19 other facts that bear most on these candidates, sources omitted; the full ledger with sources is /home/user/SomeRepository/engine/runs/v6_continuum/evidence.md - read it if you need a source or a fact that is not here)
FACT 3: imec's 3D HBM-on-GPU study measured a 141.7 °C peak against 69.1 °C for the 2.5D layout. Halving the GPU clock was needed to get below 100 °C and cost 28% of training speed. | NEW from eval_g0, check before relying on it
FACT 6: vLLM's FP8 MLA KV layout for DeepSeek-V3.2 is 656 bytes per token per layer, and the indexer K-cache is a separate buffer; top-k = 2048 in the released code | NEW from eval_g0, check before relying on it
FACT 7: imec IEDM 2025: 4 stacks of 12-high hybrid-bonded HBM placed on a GPU push the GPU peak from 141.7 °C down to 70.8 °C only with mitigations | NEW from eval_g0, check before relying on it
FACT 8: UniIC VLSI 2023: "135 GBps/Gbit, 0.66 pJ/bit stacked embedded DRAM with multilayer arrays by fine-pitch hybrid bonding and mini-TSV", 2048 I/Os per Gbit at 541 Mbps; the IEDM 2020 generation gave 34 GB/s/Gb at 0.88 pJ/b, and two SoCs on it are in mass production | NEW from eval_g0, check before relying on it
FACT 9: Rubin CPX is a single monolithic die, not the Rubin compute die, with 128 GB GDDR7 and 30 PF NVFP4. The NVL144 CPX rack is rated at 8 EF, 100 TB of fast memory and 1.7 PB/s | NEW from eval_g0, check before relying on it
FACT 12: Rubin GPU HBM4 is reported at up to 22 TB/s per GPU, with a ~2,300 W TDP from analyst estimates that Nvidia has not confirmed; one source warns that initial bandwidth may fall below 22 TB/s | NEW from eval_g0, check before relying on it
FACT 13: HBM3E access energy is ~3.44 pJ/bit in one model and ~5.74 pJ/bit including I/O in another; HBM4 has no primary pJ/bit figure | NEW from eval_g0, check before relying on it
FACT 14: The only measured areal density found for hybrid-bonded logic-to-DRAM is 64 Mb/mm² ("184QPS/W 64Mb/mm² 3D Logic-to-DRAM Hybrid Bonding…", Niu et al., Alibaba, ISSCC 2022) | NEW from eval_g1, check before relying on it
FACT 16: Micron HBM3E is 24 GB 8-high in an 11×11 mm package, so a 24Gb core die is ≤121 mm², i.e. ≥0.198 Gb/mm² with TSVs | NEW from eval_g1, check before relying on it
FACT 17: Llama 3.3 70B output list prices are Groq $0.79/Mtok and Cerebras $1.20/Mtok; one April 2026 source gives Cerebras ~$0.60 | NEW from eval_g1, check before relying on it
FACT 18: My arithmetic: at 8K context and 300 tok/s/user, a 288 GB / 22 TB/s package runs out of bandwidth at about 201 users but could hold about 855 by capacity. Capacity is 4.3× more than needed, so decode is bandwidth-bound. | NEW from eval_g1, check before relying on it
FACT 19: Spreading 545 GB of weights over 72 packages puts only 7.6 GB on each, about 0.34 ms of HBM time per step against the 3.33 ms step at 300 tok/s/user. Weights in SRAM therefore give at most a 1/(1 − 0.103) = 1.115× gain at both 8K and 128K. | NEW from eval_g1, check before relying on it

Final answer (text only), one line per idea in the order given:
=== RECHECK ===
IDEA 1: <quantity> | required <number unit> (<source>) | available <number unit> (<source>) | MARGIN <available / required, a number>
(same for the other ideas)

THE 6 IDEAS:
IDEA 1
NAME: Stacked-eDRAM pipeline chiplet packages
MECHANISM: Each ~100 mm² N6 logic chiplet carries a hybrid-bonded multilayer embedded-DRAM stack instead of on-die SRAM. The stack delivers ~135 GB/s per Gbit at ~0.66 pJ/bit, and its density is about 7–14× that of dense SRAM. Thirty-two chiplets sit on each organic package. A compiler pipelines the layers so that only ~8 KB of activations per token crosses the package links. Weights and KV cache stay resident in the stacked DRAM. For a 70B model, 39 GB of weights spread over 312 Gbit yields ~42 TB/s, against ~39 TB/s needed for 1,000 tok/s/user.
VALUE: It serves a 70B model at ~1,000 tok/s/user with no HBM and no CoWoS. Its cost per GB no longer depends on an SRAM density that no one has shipped.
DECIDING QUANTITY: Bandwidth per user while layers are pipelined. Each pipeline stage can only read its own bits, so the 42 TB/s total equals per-user bandwidth only if every chiplet works on every layer. "Package links

IDEA 2
NAME: Half-size DRAM-on-logic pipeline packages
MECHANISM: The design targets decode for sparse-MoE LLMs. Each package has two N2 logic chiplets, each hybrid-bonded to a 4-high DRAM stack, for 80 GB at 32 TB/s and ~1 kW per package. Layers are pipelined across twice as many packages. Each hop carries only ~14 KB of activations per token, so link energy is under 1% of the energy spent reading DRAM. The 80 GB per package is within mature hybrid-bonding capacity. Current per stack falls by half, to about 340 A.
VALUE: It keeps the modelled ~2.2–2.7× tokens/s per kW over Rubin on GQA models. Each package stays within the capacity and current limits that have already been shown.
DECIDING QUANTITY: DRAM areal density for 80 GB on 2 chiplets × 4 layers. Chiplet area is not stated; I took about 400 mm² from the sibling design.

IDEA 3
NAME: Half-density hybrid-bonded DRAM decode package
MECHANISM: The target is unchanged: decode for 1T-total/32B-active MoE at 8K–128K context, measured in tokens/s per kW at a per-user speed floor. The package has four ~400 mm² N2 logic chiplets, each hybrid-bonded onto a 4-high custom DRAM stack, with no HBM. The fix halves the DRAM areal density the design demands, from 0.20 Gb/mm² (commodity DRAM with no room left over) to 0.10 Gb/mm². That leaves half of each layer for SeDRAM-style wide I/O periphery and for the power TSVs that feed the logic above. Those TSVs need about 67k per chiplet at 10 mA each (667 A at 0.75 V), which is ~15% of a layer at 30 µm pitch. The package then holds 80 GB instead of 160 GB at the same 64 TB/s. That needs 100 GB/s/Gb against UniIC's measured 135, and energy is taken at the measured 0.88 pJ/bit (IEDM 2020), so DRAM power is 450 W and the package ~2.04 kW. Because decode throughput per package tends to BW ÷ KV bytes once weights are spread out, losing half the capacity costs only weight-amortisation. Against Rubin on the same roofline model, the gain is 2.13× tokens/s/kW at 32 packages and 2.36× at 64, at both 8K and 128K. At 16 packages it is 1.64×. The per-user ceiling rises to 800 tok/s (1.25 ms step).
VALUE: Modelled decode tokens per kW are ~2.1–2.4× Rubin for GQA MoE models, in scale-up domains of ≥32 packages, without needing 160 GB per package of unproven DRAM. MLA models still get only ~1.1–1.3×. The remaining unmeasured number is whether a hybrid-bonded wide-I/O DRAM reaches 0.10 Gb/mm².
DECIDING QUANTITY: Wide-I/O hybrid-bonded DRAM areal density per layer

IDEA 4
NAME: N6 SRAM-chiplet pipeline, NVFP4-sized
MECHANISM: Weights and KV cache stay entirely in SRAM, on ~100 mm² N6 chiplets with 32 per organic package, and a compiler pipelines layers across them. Only ~8 KB of activations per token crosses package links. The fix sizes the design to the measured 14.2 Mb/mm² of AMD's V-Cache die and applies it only to an 80 mm² SRAM region, with 20 mm² left for logic. That gives 142 MB per die. The design also stores 70B weights and KV in NVFP4 (4.5 bits), which is current Blackwell/Rubin practice, instead of FP8. Capacity needed drops from 111.6 GB to 62.8 GB for 31 users at 8K context, so the build is 448 dies in 14 packages, not 512 dies on an unshipped 17.5 Mb/mm². Compute is 6.8 PF FP8 against the 5.0 PF needed for 31×1,000 tok/s (margin 1.35). Under a 2× vendor markup the system price is ~$226k, or ~$3.5k/GB. That fails the old $/GB test, but that test was a stand-in for cost per token. The deciding number is now $/Mtok, which comes to ≈$0.068 including energy (14.6 kW).
VALUE: At measured SRAM density and a 2× vendor markup, it serves 70B at ~1,000 tok/s/user for ≈$0.068/Mtok. That is about GB300's ~$0.07/Mtok cost at ~20× the per-user speed, with no HBM or CoWoS. The cost margin is only ~1.03×, and it assumes 4-year, fully utilised amortisation.
DECIDING QUANTITY: Per-user speed when SRAM-resident weights are pipelined layer by layer. Only the dies that hold layer ℓ can compute it, so a token's time per step is L·F/P_total. My script reproduces the idea's own 6

IDEA 5
NAME: Wider-pipeline SRAM-weight HBM-KV domain
MECHANISM: Each compute die sits face-to-face on an SRAM base die at a realistic ~14 Mb/mm², which gives ~1.4 GB per die and ~2.8 GB per package. The 545 GB of model weights are pinned across a 192-package pipeline instead of 144, with ~14 KB of activations crossing each hop. Each package's HBM holds only KV cache. The 33% larger HBM pool raises the number of concurrent users, which offsets the cost of the extra packages.
VALUE: The weight-in-SRAM, KV-in-HBM split fits at shipped SRAM densities. It keeps a ~1.1–1.4× per-MW advantage at interactive speeds, but only if the extra KV capacity is filled with users.
DECIDING QUANTITY: how much of each Rubin package's HBM time per decode step goes to reading weights, at ≥300 tok/s/user, with the 545 GB of weights spread across all 72 NVL72 packages. Moving weights into SRAM can only

IDEA 6
NAME: Stacked-SRAM weights, 224-package interactive tier
MECHANISM: Each compute die sits on an 800 mm² hybrid-bonded SRAM base die, and HBM4 (288 GB, 22 TB/s) carries only KV cache. The fix accepts the measured 14.2 Mb/mm² instead of 30 Mb/mm²: 2.84 GB raw per package, 2.56 GB after 10% for TSVs. The 545 GB of weights therefore need 213 packages, and the domain grows from 144 to 224. Per-package decode throughput is set by HBM bandwidth ÷ KV bytes, not by where the weights sit. So tokens/s per MW is unchanged by the larger domain. MoE all-to-all is ~14 MB per token, ≈0.6 TB/s per package, well under NVLink-6-class ~3.6 TB/s. The design is offered only for the ≥300 tok/s/user tier. There the per-MW gain of 1.41× (8K) and 1.58× (128K) still survives a 5–15% capex premium (base-die silicon is only ~$370 per package), giving 1.23–1.34× at 8K and 1.37–1.50× at 128K. At ≥100 tok/s/user the net is 0.97–1.09×, which is not a win, so that tier is dropped.
VALUE: It gives a modelled ~1.2–1.5× lower cost per token than Rubin NVL72 for interactive serving at ≥300 tok/s/user, at shipped SRAM density. The cost is a 224-package scale-up domain, still ~4.8× fewer packages than Groq LP30's 1,064. This is the smallest honest version: it does not beat Rubin at ≥100 tok/s/user.
DECIDING QUANTITY: the same weight-read share of Rubin's HBM time per decode step at 300 tok/s/user. The claimed per-MW gain of 1.41× at 8K needs that share to be 1 − 1/1.41.

