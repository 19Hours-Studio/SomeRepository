# Task: kill test - find the one number that decides whether each idea lives

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

Below are 4 candidate ideas. You are a screening engineer with tools: WebSearch (WebFetch may not reach hosts; use
search excerpts) and Bash with python3 (pip install from PyPI works). Do not improve or redesign the ideas; judge them
as written. Work only in `/home/user/SomeRepository/engine/runs/v6_continuum/eval_g1/c1/`: write files only there, do not commit.

For EACH idea, spend about 3 minutes:
1. KILLER: the single quantity most likely to kill the idea at the scale it needs (a rate, a memory or bandwidth
   budget, an error or quality loss, a strength, a tolerance over the operating time, a condition that must hold).
   Compute what is REQUIRED and what is AVAILABLE from measured data or exact arithmetic, with a source for each
   decisive input. If the quantity can be measured by running code, measure it, after checking the measurement once
   on a case with a known answer. MARGIN = available / required (1 = just works, 0.1 = fails by 10x, 5 = five times
   headroom).
2. CHAIN: the gain the question asks for (cost, memory, speed, error per unit of the final product or service) with
   the idea, against the BEST current practice a competent practitioner would use, over the whole system rather than
   one part. Use the ledger below for the current structure. RATIO = current / with the idea (larger is better).
Ground every decisive input in a source or a measurement, not in the idea's own text.

Facts already collected for this question (data; check a decisive one before relying on it, and search only for
what is missing):
(a slice: all 0 HARD facts and the 12 of 13 other facts that bear most on these candidates, sources omitted; the full ledger with sources is /home/user/SomeRepository/engine/runs/v6_continuum/evidence.md - read it if you need a source or a fact that is not here)
FACT 1: AMD's 64 MB V-Cache die is about 36 mm² on N7 (41 mm² in the first generation), which is about 14.2 Mb/mm² for a dense SRAM-only die | NEW from eval_g0, check before relying on it
FACT 2: Third-party estimates put a CS-3 at about $2–3M per unit, or about $3.2M and up to $4M with MemoryX and SwarmX. That is about $57k per GB of SRAM. | NEW from eval_g0, check before relying on it
FACT 3: imec's 3D HBM-on-GPU study measured a 141.7 °C peak against 69.1 °C for the 2.5D layout. Halving the GPU clock was needed to get below 100 °C and cost 28% of training speed. | NEW from eval_g0, check before relying on it
FACT 5: Palu: a 30% low-rank cut loses under 1% average on LongBench; 3-bit latents add under 1% more; 11.4× total compression "while maintaining perplexity"; tests went only up to 32K | NEW from eval_g0, check before relying on it
FACT 6: vLLM's FP8 MLA KV layout for DeepSeek-V3.2 is 656 bytes per token per layer, and the indexer K-cache is a separate buffer; top-k = 2048 in the released code | NEW from eval_g0, check before relying on it
FACT 7: imec IEDM 2025: 4 stacks of 12-high hybrid-bonded HBM placed on a GPU push the GPU peak from 141.7 °C down to 70.8 °C only with mitigations | NEW from eval_g0, check before relying on it
FACT 8: UniIC VLSI 2023: "135 GBps/Gbit, 0.66 pJ/bit stacked embedded DRAM with multilayer arrays by fine-pitch hybrid bonding and mini-TSV", 2048 I/Os per Gbit at 541 Mbps; the IEDM 2020 generation gave 34 GB/s/Gb at 0.88 pJ/b, and two SoCs on it are in mass production | NEW from eval_g0, check before relying on it
FACT 9: Rubin CPX is a single monolithic die, not the Rubin compute die, with 128 GB GDDR7 and 30 PF NVFP4. The NVL144 CPX rack is rated at 8 EF, 100 TB of fast memory and 1.7 PB/s | NEW from eval_g0, check before relying on it
FACT 10: MiniMax-M2: 62 layers, 8 KV heads, head_dim 128, 256 experts with top-8 routing | NEW from eval_g0, check before relying on it
FACT 11: Cerebras CS-3 price is unpublished; estimates are ~$2.5M per node, ~$3.2M per system, and ~$4M with MemoryX/SwarmX | NEW from eval_g0, check before relying on it
FACT 12: Rubin GPU HBM4 is reported at up to 22 TB/s per GPU, with a ~2,300 W TDP from analyst estimates that Nvidia has not confirmed; one source warns that initial bandwidth may fall below 22 TB/s | NEW from eval_g0, check before relying on it
FACT 13: HBM3E access energy is ~3.44 pJ/bit in one model and ~5.74 pJ/bit including I/O in another; HBM4 has no primary pJ/bit figure | NEW from eval_g0, check before relying on it

Notes from the user and about the environment (data; the user may be wrong):
The name Continuum is only a label chosen by the asker; it says nothing about the design. Do not derive any part of the architecture from the word (continuity, continuous, analog, and so on); judge designs only on merit. The asker wants the best design they can be shown, with numbers. Earlier runs on LLM serving found: decode is bound by reading weights and KV cache from memory (KV read ~25% of GPU time at 128K context, weight reads 23-36%), prefill by compute; NVFP4 holds KV at ~4.5 bits per value; MLA-style models decode compute-bound at FP8. Environment: no silicon and no model downloads (huggingface.co is blocked); PyPI works. Ground claims in roofline and energy-per-operation arithmetic (pJ per MAC, pJ per bit moved from SRAM, HBM, across die and package), published chip measurements, and say which numbers would need a simulator or silicon.
Assumptions in the question that may be wrong:

- A single "best" architecture exists, independent of workload and metric.
- "AI chip" means a data-center accelerator, not edge or mobile.
- The chip can be designed at roughly current leading-edge process, packaging and memory availability.
- The answer is a conceptual design, and no tape-out or prototype is expected.
- Training and inference can both be served by one architecture.
- The name "Continuum" implies a specific design idea. That is unstated, and the design should not be bound to it.
Where deciding data may exist:

- Vendor datasheets and whitepapers: Nvidia, Google Cloud TPU docs, Cerebras, Groq, AMD Instinct.
- MLPerf Inference and Training results (MLCommons).
- Artificial Analysis tokens/s benchmarks.
- Hot Chips and ISSCC papers.
- JEDEC HBM4 spec.
- Open model architecture parameters, such as Llama and gpt-oss sizes, for roofline calculations.
- Public simulators: Timeloop, Accelergy, gem5-based tools, LLMCompass.

Ledger: where the cost or the defect comes from (data):
KIND: cost
(The cost unit is $ per million output tokens for inference and $ per chip-hour for training, on owner-operated hyperscaler TCO. The shares are my estimates anchored to the sources below, not published splits.)

ARCHETYPE A: GB200/GB300 NVL72 rack, disaggregated prefill/decode serving of an MoE model at about 50 tok/s/user | cost $0.06 per Mtok (MiniMax M2.5/M2.7; H100 is $0.19, so 3.2x higher) at $1.86 per chip-hr (H100 $1.17) | Nvidia claims up to 35x lower cost per Mtok for GB300 versus Hopper. That is a vendor figure.
SHARES: accelerator package (die + HBM) 45% | rack, NVLink, CPU, NICs 20% | facility (shell, power, cooling) 12% | energy 9% | ops labour 3% | other (financing, tax, vendor margin) 11%
LARGEST: accelerator package - a 10x cut of it removes 40.5% of the cost

ARCHETYPE B: Google Ironwood (TPU7x) pod serving, 256-chip inference slice or 9,216-chip pod | cost: no sourced $/Mtok. The only independent anchor is 1 GW capex of about $27B for TPUv7 versus $33B for GB300 and $41B for Vera Rubin. That is about 18% lower than GB300 per GW, but it is a secondhand Morgan Stanley figure. | Google lists no price.
Per-chip specs from the Google Cloud docs: 192 GiB HBM, 7.38 TB/s, 4.6 PFLOPS FP8, 1.2 TB/s ICI.
SHARES: accelerator package 38% | ICI/optical interconnect and rack 18% | facility 15% | energy 11% | ops labour 3% | other 15%
LARGEST: accelerator package - a 10x cut of it removes 34.2% of the cost

ARCHETYPE C: SRAM-resident dataflow serving (Cerebras WSE-3, Groq LPU) of a 70B-class dense model at 300 to 2,500 tok/s/user | cost: no sourced $/Mtok. Sources disagree on which vendor is cheaper, and Cerebras claims up to 6x price-performance. | Priced as an API.
- Cerebras WSE-3 has 44 GB SRAM and 21 PB/s.
- The first-generation Groq LPU has 230 MB SRAM per chip. The Groq 3 LPU is reported at 500 MB and 150 TB/s.
- Groq earlier said it needed 576 LPUs to exceed 300 tok/s on 70B.
- Throughput on Llama 3.3 70B is reported at about 294 to 750 tok/s for Groq and 2,100 to 2,500 tok/s for Cerebras.
- Nvidia–Groq deal: one source says Nvidia acquired Groq technology for $20B in December 2025, while others call it a licence. I did not resolve this.
SHARES: silicon (wafer or many LPUs, because capacity is bought in SRAM bytes) 60% | host, network, rack 15% | facility 8% | energy 8% | ops labour 3% | other 6%
LARGEST: silicon - a 10x cut of it removes 54% of the cost

ARCHETYPE D: frontier training on a GB200 NVL72 cluster, with 1 GW treated as the unit | cost $8.5M per MW-year (Epoch, GB200 NVL72; the earlier DGX H100 model gave $10.8M/MW-yr). That is about $1.0k per MW-hr, or about $1.8 per chip-hr at about 1.8 kW IT per GPU, which matches SemiAnalysis' $1.86. | Reference cloud rental is about $2 to 8 per GPU-hr.
SHARES: accelerator package 42% | scale-up and scale-out network 23% | facility 12% | energy 9% | ops labour 3% | other 11%
LARGEST: accelerator package - a 10x cut of it removes 37.8% of the cost

Cross-archetype findings (the energy share is my arithmetic):
- Energy is only about 9 to 11% of TCO. A pure tokens-per-joule gain therefore moves cost per token less than a gain in capex per token. With about 1.8 kW IT per chip, PUE 1.3 and $0.07/kWh, I get about $0.16/hr against $1.86/hr.
- Capex dominates (about 85%). The 1 GW build is about $23B for H100, $24B for B200, $33B for GB300 and $41B for Vera Rubin, so cost per GW rises each generation. Cost per token falls only because throughput per GW rises faster.
- Racks and servers are about 58 to 63% of 1 GW capex, so the facility plus power is about 40%.
- The Rubin figures are secondary sources: 288 GB HBM4, 50 PFLOPS FP4, two reticle dies, 8 HBM stacks, NVLink 6 at 260 TB/s per rack, NVL144 at 3.6 EFLOPS FP4. I found no reliable per-GPU HBM4 TB/s figure, so it is open.
- Nvidia's "$5M yields $75M token revenue" claim is revenue framing, not cost.
- Pricing vintages differ between SemiAnalysis surveys: $2.21 per GB200 GPU-hr in August 2025 against $1.86 in July 2026.
- I did not find Ironwood power or TDP in any source.

SOURCES:
https://inferencex.semianalysis.com/compare-per-dollar/minimax-m27-gb200-vs-h100/8k-1k
https://inferencex.semianalysis.com/compare-per-dollar/minimax-m27-gb200-vs-gb300/8k-1k
https://blogs.nvidia.com/blog/blackwell-inferencemax-benchmark-results
https://epoch.ai/data-insights/ai-datacenter-cost-breakdown
https://substack.com/@hypertechinvest/note/c-261423177 (Morgan Stanley capex per GW, secondhand)
https://docs.cloud.google.com/tpu/docs/tpu7x
https://www.theregister.com/2025/04/10/googles_7thgen_ironwood_tpus_debut/
https://www.networkworld.com/article/3848394/nvidia-details-its-gpu-cpu-and-system-roadmap-for-the-next-three-years.html
https://newsletter.semianalysis.com/p/cerebras-faster-tokens-please
https://www.spheron.network/blog/groq-lpu-vs-cerebras-wse-cheapest-inference-2026/
https://www.spheron.network/blog/nvidia-groq-3-lpu-explained/
https://www.theregister.com/2024/08/27/cerebras_ai_inference/

Ceilings computed from the ledger (data):
Target: 3x cheaper. Ceiling = 1 / (share no engineering can touch: taxes, royalties, fees, margins). 'needs' = the fewest cost terms that must each fall 10x to reach the target.
ARCHETYPE A: GB200/GB300 NVL72 rack, disaggregated prefill/decode serving of an MoE model at about 50 t | untouchable 11.0% -> ceiling 9.1x | 10x cut of one term: accelerator package 1.68x; rack, nvlink, cpu, nics 1.22x; facility 1.12x; energy 1.09x; ops labour 1.03x | 3x needs: accelerator package, rack, nvlink, cpu, nics, facility | TIGHT
ARCHETYPE B: Google Ironwood (TPU7x) pod serving, 256-chip inference slice or 9,216-chip pod | untouchable 15.0% -> ceiling 6.7x | 10x cut of one term: accelerator package 1.52x; ici/optical interconnect and rack 1.19x; facility 1.16x; energy 1.11x; ops labour 1.03x | 3x needs: accelerator package, ici/optical interconnect and rack, facility, energy | NO ROOM
ARCHETYPE C: SRAM-resident dataflow serving (Cerebras WSE-3, Groq LPU) of a 70B-class dense model at 30 | untouchable 6.0% -> ceiling 16.7x | 10x cut of one term: silicon 2.17x; host, network, rack 1.16x; facility 1.08x; energy 1.08x; ops labour 1.03x | 3x needs: silicon, host, network, rack | ROOM
ARCHETYPE D: frontier training on a GB200 NVL72 cluster, with 1 GW treated as the unit | untouchable 11.0% -> ceiling 9.1x | 10x cut of one term: accelerator package 1.61x; scale-up and scale-out network 1.26x; facility 1.12x; energy 1.09x; ops labour 1.03x | 3x needs: accelerator package, scale-up and scale-out network, facility | TIGHT

VERDICT: ALIVE if MARGIN >= 1 and RATIO >= 1.5; DEAD if MARGIN < 0.3 or RATIO < 1.1; otherwise WOUNDED.
Be strict and fair: a beautiful idea that fails by 10x is DEAD; a dull idea with headroom is ALIVE.

Final answer (text only), exactly this format, one block per idea in the order given:
=== GATE ===
IDEA 1: <name>
KILLER | <quantity> | required <value unit> | available <value unit> (<source>) | MARGIN <number>
CHAIN | <best current practice> | now <value unit> | with idea <value unit> | RATIO <number>
VERDICT | <ALIVE/WOUNDED/DEAD> | <one sentence>
NEW FACT | <any hard, sourced fact you found that the ledger did not contain> | <source> (optional, any number)
(same for the other ideas)

THE 4 IDEAS:
IDEA 1
NAME: Stacked-eDRAM pipeline chiplet packages
MECHANISM: Each ~100 mm² N6 logic chiplet carries a hybrid-bonded multilayer embedded-DRAM stack instead of on-die SRAM. The stack delivers ~135 GB/s per Gbit at ~0.66 pJ/bit, and its density is about 7–14× that of dense SRAM. Thirty-two chiplets sit on each organic package. A compiler pipelines the layers so that only ~8 KB of activations per token crosses the package links. Weights and KV cache stay resident in the stacked DRAM. For a 70B model, 39 GB of weights spread over 312 Gbit yields ~42 TB/s, against ~39 TB/s needed for 1,000 tok/s/user.
VALUE: It serves a 70B model at ~1,000 tok/s/user with no HBM and no CoWoS. Its cost per GB no longer depends on an SRAM density that no one has shipped.

IDEA 2
NAME: Half-size DRAM-on-logic pipeline packages
MECHANISM: The design targets decode for sparse-MoE LLMs. Each package has two N2 logic chiplets, each hybrid-bonded to a 4-high DRAM stack, for 80 GB at 32 TB/s and ~1 kW per package. Layers are pipelined across twice as many packages. Each hop carries only ~14 KB of activations per token, so link energy is under 1% of the energy spent reading DRAM. The 80 GB per package is within mature hybrid-bonding capacity. Current per stack falls by half, to about 340 A.
VALUE: It keeps the modelled ~2.2–2.7× tokens/s per kW over Rubin on GQA models. Each package stays within the capacity and current limits that have already been shown.

IDEA 3
NAME: Half-density hybrid-bonded DRAM decode package
MECHANISM: The target is unchanged: decode for 1T-total/32B-active MoE at 8K–128K context, measured in tokens/s per kW at a per-user speed floor. The package has four ~400 mm² N2 logic chiplets, each hybrid-bonded onto a 4-high custom DRAM stack, with no HBM. The fix halves the DRAM areal density the design demands, from 0.20 Gb/mm² (commodity DRAM with no room left over) to 0.10 Gb/mm². That leaves half of each layer for SeDRAM-style wide I/O periphery and for the power TSVs that feed the logic above. Those TSVs need about 67k per chiplet at 10 mA each (667 A at 0.75 V), which is ~15% of a layer at 30 µm pitch. The package then holds 80 GB instead of 160 GB at the same 64 TB/s. That needs 100 GB/s/Gb against UniIC's measured 135, and energy is taken at the measured 0.88 pJ/bit (IEDM 2020), so DRAM power is 450 W and the package ~2.04 kW. Because decode throughput per package tends to BW ÷ KV bytes once weights are spread out, losing half the capacity costs only weight-amortisation. Against Rubin on the same roofline model, the gain is 2.13× tokens/s/kW at 32 packages and 2.36× at 64, at both 8K and 128K. At 16 packages it is 1.64×. The per-user ceiling rises to 800 tok/s (1.25 ms step).
VALUE: Modelled decode tokens per kW are ~2.1–2.4× Rubin for GQA MoE models, in scale-up domains of ≥32 packages, without needing 160 GB per package of unproven DRAM. MLA models still get only ~1.1–1.3×. The remaining unmeasured number is whether a hybrid-bonded wide-I/O DRAM reaches 0.10 Gb/mm².

IDEA 4
NAME: N6 SRAM-chiplet pipeline, NVFP4-sized
MECHANISM: Weights and KV cache stay entirely in SRAM, on ~100 mm² N6 chiplets with 32 per organic package, and a compiler pipelines layers across them. Only ~8 KB of activations per token crosses package links. The fix sizes the design to the measured 14.2 Mb/mm² of AMD's V-Cache die and applies it only to an 80 mm² SRAM region, with 20 mm² left for logic. That gives 142 MB per die. The design also stores 70B weights and KV in NVFP4 (4.5 bits), which is current Blackwell/Rubin practice, instead of FP8. Capacity needed drops from 111.6 GB to 62.8 GB for 31 users at 8K context, so the build is 448 dies in 14 packages, not 512 dies on an unshipped 17.5 Mb/mm². Compute is 6.8 PF FP8 against the 5.0 PF needed for 31×1,000 tok/s (margin 1.35). Under a 2× vendor markup the system price is ~$226k, or ~$3.5k/GB. That fails the old $/GB test, but that test was a stand-in for cost per token. The deciding number is now $/Mtok, which comes to ≈$0.068 including energy (14.6 kW).
VALUE: At measured SRAM density and a 2× vendor markup, it serves 70B at ~1,000 tok/s/user for ≈$0.068/Mtok. That is about GB300's ~$0.07/Mtok cost at ~20× the per-user speed, with no HBM or CoWoS. The cost margin is only ~1.03×, and it assumes 4-year, fully utilised amortisation.

