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
as written. Work only in `/home/user/SomeRepository/engine/runs/rival_ab/gate/c2/`: write files only there, do not commit.

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
ARCHETYPE A: Data-center inference of a large MoE model (GLM, DeepSeek or Kimi class) on owned GB200 NV | untouchable 5.0% -> ceiling 20.0x | 10x cut of one term: accelerator vendor margin 1.34x; facility power, cooling and building 1.22x; electricity 1.16x; network 1.11x; accelerator silicon, hbm and packaging 1.08x; cpu, server and other hardware 1.08x; ops and software 1.05x | 3x needs: accelerator vendor margin, facility power, cooling and building, electricity, network, accelerator silicon, hbm and packaging | NO ROOM
ARCHETYPE B: Frontier pretraining on a rented or owned GPU cluster (H100/B200 class), with FP8/BF16 mix | untouchable 6.0% -> ceiling 16.7x | 10x cut of one term: accelerator chips and servers 1.66x; r&d staff including equity 1.42x; cluster networking 1.13x; energy 1.04x | 3x needs: accelerator chips and servers, r&d staff including equity | ROOM
ARCHETYPE C: Long-context decode on HBM GPUs (GQA model, batch-limited, KV cache streamed from HBM ever | untouchable 5.0% -> ceiling 20.0x | 10x cut of one term: hbm streaming of weights and kv cache 1.82x; static, idle and uncore power 1.19x; tensor-core compute 1.16x; scale-up and scale-out interconnect 1.07x; cooling and power-conversion overhead 1.05x | 3x needs: hbm streaming of weights and kv cache, static, idle and uncore power, tensor-core compute | TIGHT
ARCHETYPE D: Manufacturing one flagship accelerator: B200-class, TSMC 4NP logic dies, 8 HBM3E stacks, C | untouchable 5.0% -> ceiling 20.0x | 10x cut of one term: hbm 1.68x; logic dies, substrate, test and other 1.42x; advanced packaging 1.18x | 3x needs: hbm, logic dies, substrate, test and other | ROOM

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
NAME: Base-die FP4 KV attention
MECHANISM: Fixed-function GQA/MLA attention units sit in custom HBM4 base dies and read KV stored as FP4 with per-16-element scales over the TSVs. Only queries and outputs cross the PHY. Bytes per step fall 4x and energy per bit about 1.5x (est.), so 16K-context attention falls from about 168 mJ to about 28 mJ per token. The closest earlier attempt, HBM-PIM, stalled on programmability. Restricting the logic to one fixed attention kernel behind a vLLM operator avoids that problem. The deciding quantity is the accuracy loss from FP4 KV at 128K context.
VALUE: An estimated 5–6x lower long-context decode energy, attacking the cost term that dominates decode energy.

IDEA 2
NAME: Attention in HBM4 base die
MECHANISM: A custom HBM4 logic base die runs one fixed kernel: exact flash-decode partial attention over the KV resident in that stack. Only per-head partial sums and softmax maxima leave the stack, so output is unchanged. The closest attempt is HBM-PIM, which died on general programmability; this exposes a single vLLM attention op and nothing else. The deciding quantity is the base die's internal TSV bandwidth and pJ/B relative to the PHY-plus-interposer path.
VALUE: It roughly doubles KV bytes/s and halves KV energy per token at 32K+ context without changing model outputs.

IDEA 3
NAME: Half-HBM training die
MECHANISM: Pair about 4.5 PF FP8 with only 4 HBM stacks instead of 8. This raises the compute-to-bandwidth ridge from about 560 to 1,100 FLOP/B (est.). About 400 MB of on-die SRAM tiles the GEMMs, and ZeRO sharding covers the lost capacity. Ironwood and B200 stop short because they spend 8 stacks per die on flexibility that training GEMMs rarely use. The deciding quantity is the share of step time spent in ops below 1,100 FLOP/B (norms, attention backward, MoE dispatch, optimizer); above about 15%, the gain disappears.
VALUE: Roughly 2x training FLOP per HBM stack and per CoWoS wafer, and about 1.3x lower chip BOM (est.).

IDEA 4
NAME: Attention inside memory base
MECHANISM: Each HBM4 stack gets a custom logic base die that holds its slice of the KV cache. The die computes the attention scores, softmax and weighted sum locally, so only queries go in and per-head outputs come out. Link traffic falls about 1000x at 16K context. Unlike general PIM, which stalled on programmability, this is one fixed operation called as a library kernel, so no address translation or coherence is needed. The deciding quantity is the base-die joules per KV bit (target ≤1 pJ). At that level, decode energy at 16K falls from 242 to about 150 mJ/token, roughly 1.6x. Base-die thermal budget under the DRAM stack is the main risk. A cycle-accurate model run against measured H100 traces would falsify the design if the result exceeds 1.3 pJ/bit.
VALUE: Long-context decode at roughly 1.6x lower energy per token, with no change to model outputs.

