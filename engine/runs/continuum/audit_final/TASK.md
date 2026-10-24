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
`/home/user/SomeRepository/engine/runs/continuum/audit_final/`: read no other files in the repository, do not modify other files, do not commit.

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
NAME: Layer-pipelined LPDDR prefill dies
MECHANISM: The anchor is kept: a dense FP4/FP8 compute die with no HBM runs the compute-bound prefill phase, sends the KV to the decode tier over a plain NIC, and uses the same ISA and compiler as that tier. The kill test was right that one die holding a whole MoE model is memory-bound: on DeepSeek-V3 at 8K tokens per pass, each expert sees only 256 tokens, which gives 910 FLOP/B. The repair splits the model's layers across 8 dies. Each die (20 PF dense FP4, 800 mm², ~1.18 kW) keeps 47 GB of the 376 GB of NVFP4 weights in 64 GB of 1024-bit LPDDR5X (1.37 TB/s) and pushes a large batch of tokens through one layer before moving to the next (layer-major mega-batch). That makes a die compute-bound from about 45K tokens per pass. Only activations cross between dies (15–45 GB/s, against the 0.65 TB/s per die that expert-parallel all-to-all would need), so no NVLink-class scale-up fabric is required. KV egress is 2.4–5 GB/s per die, TTFT is 0.69 s at 8K prompts, and the design uses 0 GB of HBM and no CoWoS.
VALUE: All-in cost per prefill token comes out 1.27× cheaper than Rubin, 1.20× cheaper than the revived HBM4 Rubin CPX and 2.7× cheaper than B200, rising to about 1.45× vs Rubin if HBM4 reaches $32/GB. It also removes the ~1.26 GB of HBM Rubin needs per 1K prefill tok/s.

IDEA 2
NAME: Detached attention-stack memory nodes
MECHANISM: The anchor is kept: the custom HBM4 logic base die runs GQA decode attention (QKᵀ, softmax, AV at FP8) on KV read through the TSVs, and only partial outputs leave the stack. The repair takes the stack off the GPU interposer. It uses a JEDEC SPHBM4-style organic-substrate mount (standard published July 2026), with a narrow link in place of the 2048-bit host bus. Each 48 GB, 2.5 TB/s stack becomes a separate KV node with a 13–19 W attention base die. It serves 2 users at 128K context (FP8 KV) at 49 tok/s each and needs only 0.2 GB/s of decode link, because KV bytes read outnumber link bytes about 8,000 to 1 (plus ~2 GB/s to load KV after prefill). The claimed 2× energy saving does not hold: counting the GPU-side NoC, L2 and shared-memory path, it is 33% (5.34 → 3.58 pJ/bit). The real gain is that KV capacity and bandwidth grow without CoWoS or GPU silicon: one Rubin handles weights and FFN for about 1,200–1,500 users while 400–760 stacks hold their KV.
VALUE: Long-context (128K) GQA decode costs about 1.7× less per million tokens than the best baseline (Rubin-only: $0.177 vs $0.304 at cost of goods; 2.6× at market prices), and 1.5× less at 16K context.

IDEA 3
NAME: HBM-halved expert-stationary stack
MECHANISM: The anchor is unchanged: MoE expert weights stay fixed in hybrid-bonded SRAM layers, and HBM serves only the KV cache. The repair changes the job of the stack. It no longer sits on top of a full-HBM GPU, where it bought only 1.00–1.04×: with wide expert parallelism a Rubin package streams just 5.2 GB of weights per step, about 0.24 ms, which is around 1% of energy per token. Instead the stack replaces half the HBM. The repaired package: - 2 compute dies, each with 2–4 SRAM layers bonded underneath. The compute die sits on top, as in Zen 5 X3D, so heat goes straight to the lid. At the N5 bitcell that is 2.29 MB/mm², 6.9 GB per die with 4 layers, and 987 GB per 72-package rack. - 4 HBM4 stacks per package instead of 8: 11 TB/s and 144 GB, used only for KV. DeepSeek-V3 needs 2 SRAM layers per die and Kimi-K2 (1T) needs 3. In every tier tested for DeepSeek-V3, and for Kimi-K2 at a realistic 0.35 MFU, throughput equals the 8-stack Rubin. The stack adds about $4.3k per package; the 4 HBM4 stacks it saves are worth about $10–14k.
VALUE: Throughput per rack is the same, but the rack costs about 0.73–0.83× as much per token and uses 288 fewer HBM4 stacks (half), and HBM supply is the binding limit for 2026–28. It loses (0.61×) only for 1T-class models at high MFU and ≤300 tok/s/user, where HBM bandwidth for KV becomes the limit again.

IDEA 4
NAME: Continuum-D: SRAM weights, LPDDR KV
MECHANISM: The anchor is unchanged. Weights of a frontier MoE stay resident in plain 2D SRAM across many standard-packaged dies, with no HBM and no CoWoS, and each user's KV cache lives in LPDDR attached to each die. Repaired sizing: - At NVFP4's 4.5 bits per weight the model is 377 GB, not 335 GB. That takes 333 N3 dies of 800 mm², each with 1.25 GB of SRAM (428 mm² at 31.8 Mib/mm² and 70% array efficiency), about 1.3 PF of FP8, and 48 GB of LPDDR6 at 1 TB/s (26 x24 channels). - The dies form 61 layer-groups that broadcast and then reduce, instead of one 333-stage pipeline. That cuts the hop floor from 233 µs to 85 µs per token, so the per-user ceiling is about 11k tok/s. - Each die keeps a copy of a neighbour's KV slice. Without it, losing one die would erase part of every user's cache. At 32K context with NVFP4 KV the system serves 414k tok/s and is compute-bound (LPDDR could carry 514k). Bill of materials is $0.81M at 117 kW, or $2.44M priced at a 3× markup. Energy is 0.19–0.20 J/token, about 9% worse than Rubin, so the original "40× less energy" claim is dropped.
VALUE: At 32K context and ≥1000 tok/s/user it serves tokens at $0.077/Mtok. That is 2.8× cheaper than Rubin NVL72 with wide expert parallelism ($0.214), about 5× cheaper than Rubin plus Groq 3 LPX (if an LPX rack costs ~$4M), and 10–19× cheaper than Cerebras. At ≤500 tok/s/user it only reaches parity (1.1×).

