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
`/home/user/SomeRepository/engine/runs/continuum_r2/audit_final/`: read no other files in the repository, do not modify other files, do not commit.

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
NAME: Continuum-D: SRAM experts, LPDDR sparse-KV
MECHANISM: The anchor survives: a 671B MoE (DeepSeek-V3.2 class) sits fully resident in SRAM across standard-packaged dies with no HBM and no CoWoS, and the KV cache goes to commodity LPDDR. The repair changes three things. First, SRAM area is recomputed at a realistic 55% of N3E bitcell density, so 1 GB takes 436 mm² rather than 258 mm². That gives 36 experts per die and one 8+1-die stage per MoE layer, so all-to-all traffic stays inside a stage. The system grows to 527 dies costing $1.44M, under the $1.5M kill line. Second, the target changes from dense-MLA attention to sparse-attention (DSA) MoE models at 32K–128K context. The binding quantity is "drain time": how long a memory takes to be read end to end. Sparse KV at 128K needs about 55 ms at 100 tok/s per user, and LPDDR drains in about 62 ms. HBM4 drains in 13 ms, so it strands bandwidth or runs out of capacity. Dense MLA needs 10 ms, and there the design only ties GPUs ($0.138 vs $0.135–0.157 per million tokens). Third, the system is decode-only: prefill runs on separate GPUs and arrives as about 1.5 GB/s per die of KV writes.
VALUE: At 128K context, sparse attention and 200–400 tok/s per user, it costs about $0.095 per million tokens. The best Vera Rubin NVL72 setup (HBM only, or with CPU-memory KV offload) costs $0.127–0.136, so Continuum-D is 1.34–1.44× cheaper. Against LPX+Rubin it is about 2.9× cheaper, but that figure depends on an estimated LPX price. It is one of the few options above 1,000 tok/s per user.

IDEA 2
NAME: Touch-rate-split DSA KV tier
MECHANISM: The anchor is kept. The model's own lightning indexer picks the top-2,048 entries, and a hardware engine gathers exactly those 656-B MLA latents from on-package LPDDR6. The 132-B FP8 indexer keys stay in HBM and are scanned in full every step. The repair drops the bandwidth and energy claim, which was false: against FlashMLA-sparse, HBM bytes per step fall only 1.137→1.055 GB (1.08×), and memory energy is 31.3 vs 31.7 mJ per token, so no gain. The design is restated as a capacity split by touch rate. The indexer needs about 100 reads per second of its own capacity, which nearly matches HBM4's 76 per second, while the latent is touched at only 2,048/L. Each byte class therefore goes to the memory whose bandwidth-to-capacity ratio fits it. The decode die (Continuum-D) has 4 HBM4 stacks, 4 LPDDR6 modules (512 GB, ~0.7 TB/s), a hardware per-layer top-k unit and an LRU hot-buffer tag directory in HBM. At 128K context and 100 tok/s it serves 74 users, or 18.4 per HBM stack, against 5.0 per stack for an all-HBM Rubin. That is 3.9×, and the limit is HBM bandwidth spent on the indexer scan. LPDDR miss traffic (79 GB/s) and gather latency (37 of 164 µs per layer) both have headroom down to a hot-buffer hit rate of about 0.4.
VALUE: Cost per 128K user slot is 1.0× (2026 prices) to 1.0× (2027) that of the best practice, Rubin+Vera with HiSparse offload ($86–100 vs $102 per user slot). The win is 1.9× users per HBM stack when top-k locality is low (hit ≤0.4), and 1.8–3.4× users per chip on accelerators that lack a large coherent host memory, such as Ironwood-class chips (47.7–89.5 vs 26.6 users).

IDEA 3
NAME: Node-scale expert-stationary SRAM stacks
MECHANISM: The anchor survives: hybrid-bonded multi-layer SRAM stacked under each compute die holds all expert weights, so HBM carries only KV. Capacity is repaired by putting the stacks on 2-die Rubin-class packages using N5 SRAM dies (est. 2.29 MB/mm²). Three layers give 790 GB per rack, a margin of 1.38 on Kimi K2 and 2.15 on V3; the original design had 0.96. But removing weight reads can save at most W/(N·BW) per step, which is 0.40–0.62 ms on an EP72 rack. Rack-scale gain is therefore only 1.19–1.33×, which fails the 1.5× bar. The repair moves the design to where that term is large: an 8-GPU node, without a 72-GPU NVLink rack (NVL72), serving MoE models of 120B parameters or less (gpt-oss-120b). Four layers give 117 GB per node, a 1.86 capacity margin. Gain is 1.39× at 500 tok/s per user and 1.86× at 800, and above 1,000 tok/s per user the stacked node keeps working where the baseline node cannot reach that speed. The SRAM adds about $24k to a ~$0.95M node.
VALUE: At 500–800 tok/s per user on 8-GPU nodes, cost falls from $0.024–0.032 to $0.017 per million tokens (1.4–1.9× cheaper). Against the same model spread across a full NVL72 rack, the gain is only about 1.06×.

IDEA 4
NAME: SRAM-tiled LPDDR prefill die
MECHANISM: The anchor is kept: a prefill die with no HBM, sharing an ISA with the decode tier and passing it KV (132 B to decode-tier HBM, 656 B to its LPDDR, 1.8 GB/s per die). The original threshold was wrong. The die's ridge is 12,500 FLOP/B (17.5 PF ÷ 1.4 TB/s), not 300. MoE expert-stationary streaming is also capped at about 2·F_expert = 4,096 FLOP/B whatever the batch, so an LPDDR-only die with 256 MB of SRAM reaches only 34% of its compute at 128K. Two changes fix this. First, each package holds a full NVFP4 replica of the model (377 GB in 512 GB LPDDR6), so there is no expert-parallel all-to-all. Second, a hybrid-bonded SRAM token-tile buffer (≥0.75 GB per die at 128K, ≥1.0 GB at 32K; 1.45 GB planned) keeps tiles of 31–65K tokens resident while weights stream past. The package then becomes compute-bound at 76.5k tok/s at 128K, the same as Rubin. A CPX-like part that needs EP3 over a 200 GB/s NIC is network-bound at 30k tok/s. The price is at least 64K tokens per pass, which means about 1–2 s of batching latency.
VALUE: Prefill throughput per FLOP matches Rubin with zero HBM stacks. BOM per ktok/s is 1.0× Rubin at 2026 HBM prices ($115 vs $114) and 1.6× cheaper at 2027 prices ($115 vs $187). Energy per token is the same (23.8 vs 24.2 mJ).

