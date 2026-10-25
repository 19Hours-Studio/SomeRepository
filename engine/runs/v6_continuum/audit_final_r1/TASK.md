# Task: adversarial review - find what would make these ideas fail or overstate their value

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

Below are 4 ideas, already repaired once against reality by a researcher. Your job is to be the toughest competent
outside reviewer: an engineer who will lose money if any of these claims is wrong. You do NOT fix or improve the
ideas; you find their defects, prove each one with a number, and rank them.

You have tools: WebSearch/WebFetch and Bash with python3 (check every claim in real code). Work only in
`/home/user/SomeRepository/engine/runs/v6_continuum/audit_final_r1/`: read no other files in the repository, do not modify other files, do not commit.

For each idea, attack in this order:
1. Recompute every number the text states (arithmetic, units, mass, energy or memory balances). Flag any that do not reproduce.
2. Consistency: list every tolerance, margin and window the design relies on, and check every rate in the design
   against it over the whole operating time (rate x duration vs window). Check that the conditions assumed really
   hold where the idea is used (site, route, season, workload, hardware) - find measured data.
3. Baseline: is the comparison against the best current practice a competent operator would use, per unit of
   recovered or delivered product or service? Name the real competing alternatives it ignores and recompute the ratio.
4. Assumptions: which decisive numbers (efficiencies, friction, rates, loss fractions, costs) are assumed rather
   than sourced? How far can they move, and does the claim survive the plausible range?
5. Evidence and statistics: are the proposed tests able to show what is claimed (sample sizes, confidence bounds)?
6. Hazards and showstoppers not mentioned (safety, environment, regulation, logistics, scale-up).
Facts marked NEW were found by earlier checks in this run and are not yet verified: do not count them toward FIT,
and do not base a FATAL or MAJOR defect on a NEW fact alone unless you have verified it yourself (its source and,
for measurements, which object and which hole, face or item each number belongs to).
Do not pad: a defect needs a mechanism and a number. If a claim survives your check, say so in one line.

Final answer (text only), exactly this format:
=== REVIEW ===
IDEA 1: <name>
DEFECT | <FATAL/MAJOR/MINOR> | <one sentence: what is wrong> | <the number or source that shows it>
(as many DEFECT lines as needed, most severe first)
SURVIVES | <claims that held up under your check, one line>
RATIO | <whole-chain cost ratio against the best current practice after your corrections: current cost / cost with the idea, one number> | <one line basis>
KNOWN | <yes / partly / no: is this already done or seriously proposed?> | <the closest existing system, project or proposal, with source>
NEW FACT | <any hard fact you found that the material did not contain> | <source> (optional, any number)
(same for the other ideas, in the same order as below)

THE 4 IDEAS:
IDEA 1
NAME: N6 SRAM chiplets, package-wide tensor stages
MECHANISM: Weights and KV cache for Llama-3.3-70B are stored in NVFP4 (4.5 bits) and live entirely in SRAM on 100 mm² N6 chiplets, 32 per organic package. The fix has two parts. First, each die is sized to the measured 14.2 Mb/mm² of AMD's V-Cache die, not 17.5. A die has 70 mm² of SRAM (124 MB) and 30 mm² of logic, which gives 22.7 TF FP8 at A100's whole-die 0.755 TOPS/mm² on N7. Second, layers are no longer pipelined die by die, which had halved per-user speed in the last check. Each package is instead one tensor-parallel stage across its 32 dies. For 32 users at 8K context the model needs 67 GB, which is 544 dies in 17 stages running 16 micro-batches. Each stage takes 37.7 µs of compute plus 11.4 µs of collectives, assuming a 1 µs all-reduce across 32 dies, which still needs a simulator. That gives 1,198 tok/s/user, or 916 at 50% MAC efficiency. Full cost of ownership (2× vendor markup, host and network, facility, energy, 60% utilisation) comes to $0.23/Mtok with $7.5k package overhead, or $0.14 with $3k.
VALUE: At measured SRAM density it serves 70B at about 1,000–1,200 tok/s/user for about $0.14–0.23/Mtok. That is 2.6–5.6× below the Groq ($0.79) and Cerebras ($0.60–1.20) list prices, which include their margins, and capex per GB of SRAM is 13× below CS-3. The "GB300 cost at 20× speed" claim is dropped: this costs 2–4× more per token than GB300 at 50 tok/s, and it is slower per user than Cerebras (2,100–2,500 tok/s).

IDEA 2
NAME: Cheap-node HBM decode tier
MECHANISM: Energy is ~9% of TCO, so this decode-only part competes on capex per TB/s rather than tokens per kW. Decode needs only ~3 PF FP8 to saturate 22 TB/s, so the compute dies move to N6. The design keeps 288 GB of HBM4 and is built at cost. Estimated package cost is ~$16k (HBM ~$12k, N6 logic ~$1.5k, packaging ~$2k), against a ~$45k street Rubin package (also an estimate). Prefill and training stay on HBM or GDDR parts, linked to this tier by KV-cache transfer.
VALUE: Cost per token improves by 1/(0.91/2.8 + 0.09/2) ≈ 2.7×. The 1.5× target holds while the package costs ≤ ~$31k, a ~1.9× margin, though most of that margin is vendor markup avoided rather than physics.

IDEA 3
NAME: N6 SRAM-chiplet pipeline packages
MECHANISM: Weights and KV cache live in about 112 GB of SRAM spread over many dies of about 100 mm² on N6. That node is chosen because SRAM stopped shrinking, so SRAM bytes cost about half as much there as on N3. Thirty-two dies sit on each organic package, and 16 packages hold one 70B model. A compiler pipelines the layers so that only about 8 KB of activations per token crosses the organic links. Closest earlier attempt is the Groq LPU, where 576 chips on 14 nm cards made capacity cost too high. Here SRAM is bought at roughly $0.1/MB on dense, cheap packages instead. The deciding quantity is delivered system cost per GB of SRAM, which must stay at or below about $1.5k/GB.
VALUE: It serves a 70B model at about 1,000 tok/s/user for about $0.07/Mtok, which is GB300's cost at 20x the speed, using no HBM and no CoWoS.

IDEA 4
NAME: Hybrid-bonded DRAM-on-logic decode package
MECHANISM: Continuum targets one workload: decode for frontier sparse-MoE LLMs (1T total / 32B active parameters) at 8K–128K context. The main metric is tokens/s per kW at a per-user speed target (100, 400 or 1000 tok/s/user), with tokens per joule second. Peak FLOPS is not a metric. Serving revenue comes from throughput at an interactivity target, and running cost comes from joules. The package has four ~400 mm² N2-class logic chiplets. Each sits on top of a 4-high custom DRAM stack, bonded die to die at ≤9 µm pitch (hybrid bonding). That gives 160 GB at 64 TB/s per package, at about 0.8 pJ/bit. HBM is around 3 pJ/bit (my estimate), and a published 3D-DRAM estimate gives 0.66–0.88. Compute is 40 PF dense FP4 and 20 PF FP8, in a ~2.0 kW package. Stacked-DRAM power is 64 TB/s × 8 × 0.8 pJ = 410 W. FP8 at full rate would be about 1.6 kW, so the 2 kW budget is shared and the memory and FP8 cannot both run flat out. The package has no HBM. My model found that adding an HBM tier lowered tokens/s per kW, because each decode step reads all resident bytes and the slow tier sets the step time. On the same 4.5-bit weight and KV format, the roofline/energy model compares it with Rubin (288 GB, 22 TB/s, ~1.8 kW). For GQA models, Continuum gets 2.2–2.7× the tokens/s per kW and 2.3–2.5× the tokens/J, at both 8K and 128K. For dense-MLA models it gets only 1.08–1.29×, because MLA decode at 128K costs about 1.1 TFLOP per token in attention and is compute-bound.
VALUE: In my model, Continuum gives about 2.2–2.7× more decode tokens per kW than Rubin on GQA models (2.8–3.8× vs Ironwood, 4–18× vs Groq LP30 and WSE-3). That is a modeled result, not a measured one, and it hinges on the stacked DRAM really reaching ≤1 pJ/bit and 64 TB/s.

