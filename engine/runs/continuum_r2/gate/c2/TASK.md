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
as written. Work only in `/home/user/SomeRepository/engine/runs/continuum/gate/c2/`: write files only there, do not commit.

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

Value ledger (data):
Some shares below are my own estimates built from sourced anchors. Each is marked "est."

**ARCHETYPE A:** Data-center inference of a large MoE model (GLM, DeepSeek or Kimi class) on owned GB200 NVL72 racks with disaggregated prefill/decode serving. | cost about $0.04–0.08 per million tokens at 85–195 tok/s/user (SemiAnalysis InferenceX, owning-hyperscaler TCO model) | rental price $1.86 per chip-hr for GB200 NVL72 (SemiAnalysis, July 2026)
SHARES (est., from the capex split plus an electricity share of TCO): accelerator silicon, HBM and packaging 8 | accelerator vendor margin 28 | CPU, server and other hardware 8 | network 11 | facility power, cooling and building 20 | electricity 15 | ops and software 5 | other (taxes, land, fees) 5
Anchors for these shares:
- Bernstein puts GPUs at 39% of a roughly $35B/GW build, networking at 13%, and mechanical/electrical plus building at about one third.
- Epoch puts B200 BOM at about $6.4k against a $30–40k price.
- Electricity is about 15–30% of owned-cluster cost per GPU-hour at $0.12–0.14/kWh.
LARGEST: vendor margin on the accelerator, 28%. A 10x cut removes 25% of the cost. Facility power, cooling and building (20%) is the largest term that physical design can change. A 10x cut of that removes 18%.

**ARCHETYPE B:** Frontier pretraining on a rented or owned GPU cluster (H100/B200 class), with FP8/BF16 mixed precision and large 3D-parallel runs. | cost about $30–40M per run for GPT-4 and Gemini Ultra (Epoch, 2023 era). A third-party dashboard on Epoch data says frontier runs have grown about 10x since. Epoch's trend is 2.4x per year, with runs above $1B expected by 2027. | no price or target
SHARES (Epoch ranges, midpoints normalized to 100): accelerator chips and servers 44 | cluster networking 13 (Epoch adds 23% overhead for it) | R&D staff including equity 33 | energy 4 | other (facility, cloud margin, failed runs) 6
Epoch's raw ranges are hardware 47–67%, staff 29–49% and energy 2–6%.
LARGEST: accelerator hardware, 44%. A 10x cut removes about 40%. Staff cost (33%) does not fall when chips get cheaper, so it caps what a better chip can save.

**ARCHETYPE C:** Long-context decode on HBM GPUs (GQA model, batch-limited, KV cache streamed from HBM every step). | cost about 107 mJ/token at 4K context and 242 mJ/token at 16K (arXiv 2605.11999, a measurement study) | no target
SHARES (est.; no source gives this breakdown): HBM streaming of weights and KV cache 50 | tensor-core compute 15 | static, idle and uncore power 18 | scale-up and scale-out interconnect 7 | cooling and power-conversion overhead 5 | other (workload-fixed algorithmic minimum) 5
Source support is qualitative:
- Decode is memory-bound.
- Off-chip DRAM access costs 100–1000x the energy of an on-chip FLOP.
- Energy per token rises 2.26x from 4K to 16K context because the KV cache grows.
- One measurement found H100 reaching only 27% of peak HBM bandwidth on this workload, so the simple bandwidth model is not exact.
LARGEST: HBM data movement, about 50% (est.). A 10x cut removes about 45%. This is the term an architecture can attack most directly.

**ARCHETYPE D:** Manufacturing one flagship accelerator: B200-class, TSMC 4NP logic dies, 8 HBM3E stacks, CoWoS-L packaging. | cost about $6,400 per chip (Epoch range $5.7–7.3k; Silicon Analysts $6.75k) | price $30–40k, an estimated 82–84% chip-level gross margin
SHARES of BOM: HBM 45 (about $2,900) | advanced packaging 17 (about $1,100) | logic dies, substrate, test and other 33 (est., the remainder) | other (yield loss, royalties, fees) 5 (est.)
Note that CoWoS capacity is a supply limit as well as a cost. Silicon Analysts projects 120–130k wafers per month by end-2026, up from 13k at end-2023. Figures for B200 packaging cost are about 47% above H100 (Silicon Analysts).
LARGEST: HBM, 45%. A 10x cut removes about 40%. HBM plus packaging is roughly two thirds of BOM.

**Reading across the four archetypes (my synthesis):**
- Memory and packaging dominate chip BOM (D).
- Memory movement dominates decode energy (C).
- Chip margin plus facility power and cooling dominate inference TCO (A).
- Chips are about 45% of training cost, and staff cost is a floor that chips cannot reduce (B).
- A new chip can move A through C, but it cannot touch staff cost or the margin of whoever sells the chip.

**Caveats:**
- Sources disagree. Rental and TCO figures are vendor or blog numbers.
- Cloudrift and Spheron differ by about 2.5x on depreciation per GPU-hour because of node-versus-GPU unit confusion, so I did not use either as a direct input.
- The Bernstein, Morgan Stanley and Epoch capex splits use different definitions. GPU share runs from 39% up to about 60%.
- I found no measured breakdown of decode energy by component. The C shares are my estimates and should be checked before use.
- I did not look at edge workloads. The archetypes are all data-center.

SOURCES:
- https://inferencex.semianalysis.com/compare-per-dollar/glm-5-3-gb200-vs-gb300
- https://inferencex.semianalysis.com/compare-per-dollar/deepseek-r1-gb200-vs-gb300
- https://www.investing.com/news/stock-market-news/how-much-does-a-gw-of-data-center-capacity-actually-cost-4314046
- https://www.trendforce.com/research/download/RP251016DL
- https://epoch.ai/blog/how-much-does-it-cost-to-train-frontier-ai-models
- https://arxiv.org/abs/2405.21015
- https://epoch.ai/data-insights/b200-cost-breakdown
- https://siliconanalysts.com/analysis/nvidia-b200-blackwell-cost-breakdown
- https://www.spheron.network/blog/ai-inference-power-electricity-cost-2026/
- https://www.cloudrift.ai/blog/the-true-cost-of-gpu-ownership
- https://pytorchtoatoms.substack.com/p/metas-24k-h100-cluster-capextco-and
- https://arxiv.org/pdf/2605.11999
- https://arxiv.org/pdf/2605.30571

Ceilings computed from the ledger (data):
Target: 3x cheaper. Ceiling = 1 / (share no engineering can touch: taxes, royalties, fees, margins). 'needs' = the fewest cost terms that must each fall 10x to reach the target.
ARCHETYPE B: Frontier pretraining on a rented or owned GPU cluster (H100/B200 class), with FP8/BF16 mix | untouchable 0.0% -> ceiling infx | 10x cut of one term: cluster networking 13 (epoch adds 10.00x | 3x needs: cluster networking 13 (epoch adds | ROOM (shares summed to 23%)

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
NAME: Attention in HBM4 base die
MECHANISM: Each HBM4 stack's custom logic base die runs GQA decode attention (QKᵀ, softmax, AV at FP8) on KV read through the TSVs, skipping the PHY and interposer, and sends only the partial outputs to the main die. The closest attempt, HBM-PIM, stalled on general programmability. Here a single fixed compiler op with a small vector unit avoids that. The deciding quantity is attention intensity × in-stack bandwidth against the base-die thermal budget: about 16 FLOP/B × 2 TB/s ≈ 32 TFLOPS ≈ 16 W per stack, which I estimate is tolerable. MLA, at about 480 FLOP/B, falls outside it.
VALUE: Cuts KV-movement energy about 2× (est. ~1.5 vs ~3.9 pJ/bit) for long-context GQA decode, the largest term in decode energy.

IDEA 2
NAME: Continuum-D: SRAM weights, LPDDR KV
MECHANISM: A FP4 671B-parameter MoE (about 335 GB) sits resident in SRAM across about 340 standard-packaged, CoWoS-free dies of about 800 mm² each, with roughly 1 GB per die. Weight reads cost no HBM and about 40x less energy. The KV cache, which is about 2.2 GB per 32K-token MLA user, lives in commodity LPDDR6 at about 1 TB/s per die. The closest earlier attempt is Groq, which needed 576 chips for one 70B model because it put everything in SRAM. Continuum-D avoids this because the weights are shared across a large MoE batch, and the per-user KV goes to cheap, abundant DRAM instead of SRAM. The deciding quantity is SRAM cost per GB of resident weights versus HBM-rack cost per GB/s of weight traffic. It fails if 340 dies cost more than about $1.5M.
VALUE: It delivers high tok/s per user on frontier MoE models with zero HBM stacks and zero CoWoS wafers, which bypasses the 2026–28 supply limits that cap every GPU and TPU.

IDEA 3
NAME: Memory-light prefill compute die
MECHANISM: A dense FP4/FP8 compute die with only LPDDR runs the compute-bound prefill phase. It hands KV to the decode tier over a fabric and shares an ISA and compiler with that tier. The closest earlier attempt is Nvidia's Rubin CPX, which uses a separate GDDR7 stack. This design avoids GDDR shortages and keeps a single toolchain across both phases. The deciding quantity is prefill FLOP/byte, which must stay above about 300.
VALUE: Takes prefill off scarce HBM and CoWoS, roughly halving HBM demand per served token (A).

IDEA 4
NAME: Continuum-T: HBM-lean training die
MECHANISM: A training die carries 4 HBM4 stacks instead of 8 and adds 3D-stacked SRAM (SoIC) for GEMM tiles. Optimizer state and activations are sharded over the fabric in ZeRO style. The bet is that large training GEMMs exceed about 560 FLOP/B, so they do not need B200-class HBM bandwidth. The closest earlier attempt is TPU Ironwood, which still provisions 8 stacks. The deciding quantity is achieved MFU when HBM bandwidth per FLOP is halved. This can be tested today by down-clocking HBM on B200s during a 10B+ parameter run.
VALUE: It gives about 1.6–2x the training throughput per HBM stack, which makes it the best FLOP-per-scarce-input design if MFU falls by less than 15%.

