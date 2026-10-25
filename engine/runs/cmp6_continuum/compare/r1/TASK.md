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

Below are 10 ideas, already repaired once against reality by a researcher. Your job is to be the toughest competent
outside reviewer: an engineer who will lose money if any of these claims is wrong. You do NOT fix or improve the
ideas; you find their defects, prove each one with a number, and rank them.

You have tools: WebSearch/WebFetch and Bash with python3 (check every claim in real code). Work only in
`/home/user/SomeRepository/engine/runs/cmp6_continuum/compare/r1/`: read no other files in the repository, do not modify other files, do not commit.

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

THE 10 IDEAS:
IDEA 1
NAME: Same die, separate training/prefill SKU
MECHANISM: Prefill and training are compute- and HBM-bound and do not benefit from SRAM-resident weights. A Continuum-T package would reuse the same N2 compute die and toolchain, drop the SRAM base dies and take 8 HBM4 stacks. Serving would then be split: prefill on Continuum-T (or on GPUs or Rubin CPX), decode on Continuum. The software path is PyTorch or JAX, exported through torch.export/StableHLO to a compiler that places experts in the SRAM, emits the fixed fabric schedules and pages KV into HBM, with a plugin for vLLM/SGLang. Existing checkpoints run after post-training quantization to NVFP4 with no retraining. Custom CUDA kernels do not port, and dynamic shapes have to be padded into fixed buckets.
VALUE: This keeps one design flow and one compiler for both roles, but I estimate Continuum-T at only about 0.6–0.85× Rubin for training. It is a defensive product, and the design claims no lead in training.

IDEA 2
NAME: SRAM-stacked weights, HBM4 only for KV
MECHANISM: I target decode-heavy serving of frontier MoE models (DeepSeek-V3 class: 671B total parameters, 37B active, 32K–128K context). "Best" here means tokens/J and tokens/s per kW, both measured at a required tokens/s per user, plus tokens/s per HBM stack, because HBM is sold out for 2026. Each Continuum package has two ~800 mm² N2 compute dies, 30 PF dense FP4 in total. Each compute die sits on top of two hybrid-bonded SRAM-only base dies made on an N5-class node; that is the cheap node, because the dense SRAM cell has stayed at about 0.021 µm² from N5 to N2. The four base dies give about 10 GB of SRAM per package at about 128 TB/s and about 0.3 pJ/bit; the compute die is on top, next to the cooler, as in AMD's 9800X3D. Six HBM4 stacks give 216 GB at 15 TB/s and hold only KV cache, so no HBM bandwidth is spent on weights. A 64-package rack has 640 GB of SRAM, which holds the model's 377 GB of 4.5-bit weights, and 13.8 TB of HBM for KV. That is about 5,300 users at 128K context, where each user needs 2.6 GB that would otherwise take about 5 Groq-3 LPUs. The rack draws about 144 kW and uses 384 HBM stacks, against about 207 kW and 576 stacks for Rubin NVL72.
VALUE: At ≥200 tok/s/user and 32K context, my model gives 7.75 tok/J and 6,200 tok/s/kW. The best Rubin NVL72 case, which assumes software reaching 25 µs per layer, gives 6.5 tok/J and 4,227 tok/s/kW, so Continuum is about 1.2× better per joule and 1.5× per kW. Rubin with today's measured software cannot reach this speed at all. Per HBM stack Continuum is about 1.5× better (2,325 vs 1,519). It loses about 2× on tokens per cm² of silicon at ≤100 tok/s/user, and its lead shrinks to about 1.08× at 128K context, where attention compute dominates on every chip.

IDEA 3
NAME: Detached attention-stack memory nodes
MECHANISM: The anchor is kept: the custom HBM4 logic base die runs GQA decode attention (QKᵀ, softmax, AV at FP8) on KV read through the TSVs, and only partial outputs leave the stack. The repair takes the stack off the GPU interposer. It uses a JEDEC SPHBM4-style organic-substrate mount (standard published July 2026), with a narrow link in place of the 2048-bit host bus. Each 48 GB, 2.5 TB/s stack becomes a separate KV node with a 13–19 W attention base die. It serves 2 users at 128K context (FP8 KV) at 49 tok/s each and needs only 0.2 GB/s of decode link, because KV bytes read outnumber link bytes about 8,000 to 1 (plus ~2 GB/s to load KV after prefill). The claimed 2× energy saving does not hold: counting the GPU-side NoC, L2 and shared-memory path, it is 33% (5.34 → 3.58 pJ/bit). The real gain is that KV capacity and bandwidth grow without CoWoS or GPU silicon: one Rubin handles weights and FFN for about 1,200–1,500 users while 400–760 stacks hold their KV.
VALUE: Long-context (128K) GQA decode costs about 1.7× less per million tokens than the best baseline (Rubin-only: $0.177 vs $0.304 at cost of goods; 2.6× at market prices), and 1.5× less at 16K context.

IDEA 4
NAME: Cheap-node HBM decode tier
MECHANISM: Energy is ~9% of TCO, so this decode-only part competes on capex per TB/s rather than tokens per kW. Decode needs only ~3 PF FP8 to saturate 22 TB/s, so the compute dies move to N6. The design keeps 288 GB of HBM4 and is built at cost. Estimated package cost is ~$16k (HBM ~$12k, N6 logic ~$1.5k, packaging ~$2k), against a ~$45k street Rubin package (also an estimate). Prefill and training stay on HBM or GDDR parts, linked to this tier by KV-cache transfer.
VALUE: Cost per token improves by 1/(0.91/2.8 + 0.09/2) ≈ 2.7×. The 1.5× target holds while the package costs ≤ ~$31k, a ~1.9× margin, though most of that margin is vendor markup avoided rather than physics.

IDEA 5
NAME: N6 SRAM-chiplet pipeline packages
MECHANISM: Weights and KV cache live in about 112 GB of SRAM spread over many dies of about 100 mm² on N6. That node is chosen because SRAM stopped shrinking, so SRAM bytes cost about half as much there as on N3. Thirty-two dies sit on each organic package, and 16 packages hold one 70B model. A compiler pipelines the layers so that only about 8 KB of activations per token crosses the organic links. Closest earlier attempt is the Groq LPU, where 576 chips on 14 nm cards made capacity cost too high. Here SRAM is bought at roughly $0.1/MB on dense, cheap packages instead. The deciding quantity is delivered system cost per GB of SRAM, which must stay at or below about $1.5k/GB.
VALUE: It serves a 70B model at about 1,000 tok/s/user for about $0.07/Mtok, which is GB300's cost at 20x the speed, using no HBM and no CoWoS.

IDEA 6
NAME: Layer-pipelined LPDDR prefill dies
MECHANISM: The anchor is kept: a dense FP4/FP8 compute die with no HBM runs the compute-bound prefill phase, sends the KV to the decode tier over a plain NIC, and uses the same ISA and compiler as that tier. The kill test was right that one die holding a whole MoE model is memory-bound: on DeepSeek-V3 at 8K tokens per pass, each expert sees only 256 tokens, which gives 910 FLOP/B. The repair splits the model's layers across 8 dies. Each die (20 PF dense FP4, 800 mm², ~1.18 kW) keeps 47 GB of the 376 GB of NVFP4 weights in 64 GB of 1024-bit LPDDR5X (1.37 TB/s) and pushes a large batch of tokens through one layer before moving to the next (layer-major mega-batch). That makes a die compute-bound from about 45K tokens per pass. Only activations cross between dies (15–45 GB/s, against the 0.65 TB/s per die that expert-parallel all-to-all would need), so no NVLink-class scale-up fabric is required. KV egress is 2.4–5 GB/s per die, TTFT is 0.69 s at 8K prompts, and the design uses 0 GB of HBM and no CoWoS.
VALUE: All-in cost per prefill token comes out 1.27× cheaper than Rubin, 1.20× cheaper than the revived HBM4 Rubin CPX and 2.7× cheaper than B200, rising to about 1.45× vs Rubin if HBM4 reaches $32/GB. It also removes the ~1.26 GB of HBM Rubin needs per 1K prefill tok/s.

IDEA 7
NAME: Ridge point matched to MLA decode
MECHANISM: In MLA models (DeepSeek-style attention, where all heads share one compressed KV entry), decode attention does about 17 MFLOP per context token while reading only about 19.8 KB of KV at NVFP4's 4.5 bits per value. That is about 860 FLOP per byte, so this attention is compute-bound at FP8 (consistent with the earlier runs). Continuum therefore pairs 15 PF of FP8 attention compute with 15 TB/s of KV bandwidth, a ridge point of about 1,000 FLOP/B. Rubin's is about 800 FLOP/B and Ironwood's about 625 FLOP/B. Linear layers run at FP4 with 4.5-bit weights, accumulators and softmax are FP32, and the router and norms are BF16. The decisive figure is attention energy: at 32K context it is about 56 mJ per token at my assumed 0.1 pJ per FP8 FLOP, against about 21 mJ to read the KV from HBM. So FP8 energy per FLOP decides tokens/J at long context, not SRAM energy. Raising SRAM from 0.3 to 0.6 pJ/bit barely changes the result, while halving compute halves Continuum's lead.
VALUE: With this balance Continuum stays ahead at long context, but only by about 1.08× tok/J against the best Rubin case at 128K. That gap is small enough that I am not claiming "best" at long context; it would need sparse attention in the model or cheaper FP8 compute.

IDEA 8
NAME: Continuum-D: SRAM weights, LPDDR KV
MECHANISM: The anchor is unchanged. Weights of a frontier MoE stay resident in plain 2D SRAM across many standard-packaged dies, with no HBM and no CoWoS, and each user's KV cache lives in LPDDR attached to each die. Repaired sizing: - At NVFP4's 4.5 bits per weight the model is 377 GB, not 335 GB. That takes 333 N3 dies of 800 mm², each with 1.25 GB of SRAM (428 mm² at 31.8 Mib/mm² and 70% array efficiency), about 1.3 PF of FP8, and 48 GB of LPDDR6 at 1 TB/s (26 x24 channels). - The dies form 61 layer-groups that broadcast and then reduce, instead of one 333-stage pipeline. That cuts the hop floor from 233 µs to 85 µs per token, so the per-user ceiling is about 11k tok/s. - Each die keeps a copy of a neighbour's KV slice. Without it, losing one die would erase part of every user's cache. At 32K context with NVFP4 KV the system serves 414k tok/s and is compute-bound (LPDDR could carry 514k). Bill of materials is $0.81M at 117 kW, or $2.44M priced at a 3× markup. Energy is 0.19–0.20 J/token, about 9% worse than Rubin, so the original "40× less energy" claim is dropped.
VALUE: At 32K context and ≥1000 tok/s/user it serves tokens at $0.077/Mtok. That is 2.8× cheaper than Rubin NVL72 with wide expert parallelism ($0.214), about 5× cheaper than Rubin plus Groq 3 LPX (if an LPX rack costs ~$4M), and 10–19× cheaper than Cerebras. At ≤500 tok/s/user it only reaches parity (1.1×).

IDEA 9
NAME: N6 SRAM chiplets, package-wide tensor stages
MECHANISM: Weights and KV cache for Llama-3.3-70B are stored in NVFP4 (4.5 bits) and live entirely in SRAM on 100 mm² N6 chiplets, 32 per organic package. The fix has two parts. First, each die is sized to the measured 14.2 Mb/mm² of AMD's V-Cache die, not 17.5. A die has 70 mm² of SRAM (124 MB) and 30 mm² of logic, which gives 22.7 TF FP8 at A100's whole-die 0.755 TOPS/mm² on N7. Second, layers are no longer pipelined die by die, which had halved per-user speed in the last check. Each package is instead one tensor-parallel stage across its 32 dies. For 32 users at 8K context the model needs 67 GB, which is 544 dies in 17 stages running 16 micro-batches. Each stage takes 37.7 µs of compute plus 11.4 µs of collectives, assuming a 1 µs all-reduce across 32 dies, which still needs a simulator. That gives 1,198 tok/s/user, or 916 at 50% MAC efficiency. Full cost of ownership (2× vendor markup, host and network, facility, energy, 60% utilisation) comes to $0.23/Mtok with $7.5k package overhead, or $0.14 with $3k.
VALUE: At measured SRAM density it serves 70B at about 1,000–1,200 tok/s/user for about $0.14–0.23/Mtok. That is 2.6–5.6× below the Groq ($0.79) and Cerebras ($0.60–1.20) list prices, which include their margins, and capex per GB of SRAM is 13× below CS-3. The "GB300 cost at 20× speed" claim is dropped: this costs 2–4× more per token than GB300 at 50 tok/s, and it is slower per user than Cerebras (2,100–2,500 tok/s).

IDEA 10
NAME: Deterministic, compiler-scheduled low-latency scale-up fabric
MECHANISM: The sensitivity runs show that tokens/s per user is set by a fixed latency cost per layer, not by memory bandwidth. Measured GPU numbers bear this out. DeepEP's dispatch takes 77–194 µs and its combine 114–369 µs per layer over InfiniBand. InferenceMAX shows GB200 NVL72 falling from 1,006 tok/s per GPU at 50 tok/s/user to 194 at 100 tok/s/user. The Cerebras figures (about 2,300–2,700 tok/s/user) imply about 10 µs per layer. Continuum uses a single-hop switched copper domain of 64 packages at 1.8 TB/s per direction. The compiler schedules all traffic statically, Groq/TPU style, and MoE all-to-all uses fixed slots with FP8 activations. The goal is ≤1 µs per traversal and ≤6 µs per layer. Bandwidth is not the hard part: at batch 4096 each package needs only about 0.1 TB/s. This is the assumption the design depends on most. At 12 µs per layer Continuum still reaches 1000 tok/s/user at 1,785 tok/s/kW; at 20 µs it cannot reach 1000 at all.
VALUE: At ≥1000 tok/s/user on the 671B model, the model gives 6.35 tok/J and 3,978 tok/s/kW with 64 packages. Groq-3 LPX needs about 2,300 chips for 2.15 tok/J and 747 tok/s/kW (about 3× worse per joule, 5× per kW; per-chip power is my guess). Cerebras WSE-3 needs 11 wafers for 0.5 tok/J. No Rubin or Ironwood setup reaches this speed, even if Rubin's software gets to 10 µs per layer (639 tok/s/kW).

