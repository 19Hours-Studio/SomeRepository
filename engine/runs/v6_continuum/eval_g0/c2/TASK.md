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
as written. Work only in `/home/user/SomeRepository/engine/runs/v6_continuum/eval_g0/c2/`: write files only there, do not commit.

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
(none recorded)

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
NAME: Latent KV With Outlier Sidecar
MECHANISM: Keys and values are cached as per-head low-rank latents at 3–4 bits, with per-block scales. The few outlier channels go to a small FP16 sidebuffer. Expansion happens inside the attention unit, so full-width KV never crosses memory. The closest earlier attempt is FP8 KV, which saves only 2× and still grows linearly with full width. The deciding quantity is accuracy retained at 128k context.
VALUE: KV bytes per token fall about 6–8×, so long-context serving no longer sets the chip count.

IDEA 2
NAME: Near-HBM sparse-KV gather attention engine
MECHANISM: Attention units sit beside each HBM4 controller. The KV cache is stored as 4.5-bit NVFP4 rows (324 B per token per layer for MLA) and read with a hardware top-k gather, in the style of DeepSeek's sparse attention (top 2,048 tokens plus a 128-dim FP4 index). At 128K context this cuts KV traffic per user-token from 2.59 GB to 0.62 GB. Dense MLA decode needs 1.18 TFLOP per user-token at 128K, about 450 FLOP per byte at FP4 KV. So the HBM-side attention units are sized at about 10 PF FP8 (≈22 TB/s × 450) rather than relying on the main arrays. With sparse attention, Continuum gets 9.39 Mtok/s/MW against Rubin's 5.74 (1.64×) and Ironwood's 7.04 (1.33×). The model assumes the gather sustains at least 80% of HBM peak at 324 B granularity; only a DRAM simulator or silicon can confirm that.
VALUE: Long-context throughput per MW rises about 3.7× over dense attention on the same hardware, and Continuum keeps a 1.3–1.6× lead over incumbents running the same sparse model.

IDEA 3
NAME: Hybrid-bonded DRAM-on-logic decode package
MECHANISM: Continuum targets one workload: decode for frontier sparse-MoE LLMs (1T total / 32B active parameters) at 8K–128K context. The main metric is tokens/s per kW at a per-user speed target (100, 400 or 1000 tok/s/user), with tokens per joule second. Peak FLOPS is not a metric. Serving revenue comes from throughput at an interactivity target, and running cost comes from joules. The package has four ~400 mm² N2-class logic chiplets. Each sits on top of a 4-high custom DRAM stack, bonded die to die at ≤9 µm pitch (hybrid bonding). That gives 160 GB at 64 TB/s per package, at about 0.8 pJ/bit. HBM is around 3 pJ/bit (my estimate), and a published 3D-DRAM estimate gives 0.66–0.88. Compute is 40 PF dense FP4 and 20 PF FP8, in a ~2.0 kW package. Stacked-DRAM power is 64 TB/s × 8 × 0.8 pJ = 410 W. FP8 at full rate would be about 1.6 kW, so the 2 kW budget is shared and the memory and FP8 cannot both run flat out. The package has no HBM. My model found that adding an HBM tier lowered tokens/s per kW, because each decode step reads all resident bytes and the slow tier sets the step time. On the same 4.5-bit weight and KV format, the roofline/energy model compares it with Rubin (288 GB, 22 TB/s, ~1.8 kW). For GQA models, Continuum gets 2.2–2.7× the tokens/s per kW and 2.3–2.5× the tokens/J, at both 8K and 128K. For dense-MLA models it gets only 1.08–1.29×, because MLA decode at 128K costs about 1.1 TFLOP per token in attention and is compute-bound.
VALUE: In my model, Continuum gives about 2.2–2.7× more decode tokens per kW than Rubin on GQA models (2.8–3.8× vs Ironwood, 4–18× vs Groq LP30 and WSE-3). That is a modeled result, not a measured one, and it hinges on the stacked DRAM really reaching ≤1 pJ/bit and 64 TB/s.

IDEA 4
NAME: One compute die, two phase-split SKUs
MECHANISM: Prefill and training are compute-bound, so the SRAM base die adds cost there without adding speed. A "C" SKU uses the same compute die on a plain interposer with HBM only, while the "D" SKU described above handles decode. They are mixed at a measured prefill-to-decode ratio, like Nvidia's CPX/Rubin pairing at 1:1. Training on the C SKU sits at about 0.86–1.0× Rubin per package (30 vs 35 PF FP4) because the compute die and HBM are the same class. I make no claim that it wins at training.
VALUE: It avoids the roughly 10–15% SRAM cost on compute-bound work and shares one tape-out between both SKUs. Training is at parity, not best.

