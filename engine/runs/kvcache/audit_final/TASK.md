# Task: adversarial review - find what would make these ideas fail or overstate their value

QUESTION: Which KV-cache design (storage layout, compression, eviction, quantization, offloading or reuse) can be swapped into an existing pretrained transformer LLM with no retraining and no fine-tuning, so that the same model gives the same outputs with a smaller, faster or cheaper cache? The asker wants to take any model and replace one component with another. This design should be the best across memory, speed and quality. "Best" is not defined. The answer should say which metric or workload it is best for, and where it stops working. Plausible workloads are long-context single requests, multi-user serving, multi-turn chat and prefix reuse. The asker did not give a model family, hardware, context length or serving stack. The answer may be a ranking of existing approaches, a new combination of them, or a new idea. Each claim must be checkable against published benchmarks or an experiment that can be run.
A good answer: 
- It names the criteria that define "best" (memory saved, throughput or latency, accuracy loss, calibration cost) and the workload each applies to.
- It checks "no training, any model" against published evidence: which models and architectures it was tested on, and what happens on an architecture it was not tested on.
- It gives numbers (compression ratio, accuracy change on benchmarks such as RULER, LongBench or multi-turn tasks, throughput) with sources.
- It states the conditions under which it fails, including a compression level, a task type and a model type.
- If it proposes something new, it gives a test that could show the idea is wrong.
Constraints: 
- No retraining and no fine-tuning of the model weights.
- It should be near plug-and-play and work on "any" model. See ASSUMPTIONS on whether that is possible.

Below are 4 ideas, already repaired once against reality by a researcher. Your job is to be the toughest competent
outside reviewer: an engineer who will lose money if any of these claims is wrong. You do NOT fix or improve the
ideas; you find their defects, prove each one with a number, and rank them.

You have tools: WebSearch/WebFetch and Bash with python3 (check every claim in real code). Work only in
`/home/user/SomeRepository/engine/runs/kvcache/audit_final/`: read no other files in the repository, do not modify other files, do not commit.

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
NAME: Audited exact-prefix agentic KV tier
MECHANISM: The anchor stays: KV is reused only on an exact token-prefix match and kept in the deployment's own KV dtype, so the result is lossless by construction. In the repaired design, the CPU DRAM of all 8 GPUs in a node is pooled into one cache (about 1.6 TB). NVMe is written only for blocks that have already been hit twice. Each block gets a hash, and a 1% sample of cache hits is recomputed from scratch. That sample is checked against the server's own run-to-run noise. This replaces the claim that outputs are bit-identical, which would need batch-invariant kernels that cost 34–56% of throughput. The design is aimed at agentic or long multi-turn sessions whose working set is 4–40× larger than GPU memory. For a 30–60K-token context on Llama-3.1-8B, loading a 95% hit takes 0.15–0.30 s, against 1.4–3.8 s of prefill. That gives 2.04–2.19× less GPU time per request than prefix caching on the GPU alone. PCIe is busy 11–13% of the time and the audit adds about 1.4%.
VALUE: In agentic or multi-turn serving where the working set is larger than GPU memory, it needs about 2.0–2.2× less GPU time per request than vLLM prefix caching on the GPU alone. On chat traces like Mooncake the gain is only about 1.17–1.24×: $228 → $196 per 1M requests.

IDEA 2
NAME: Two-arm probe-gated FP8 layers
MECHANISM: The anchor stays: a cheap per-model probe compares BF16 KV with FP8 KV and picks which layers keep BF16. Everything else uses the stock vLLM FP8 kernels and the `--kv-cache-dtype-skip-layers` flag. The repaired probe runs three arms over 100 prompts of 32K tokens each, plus 512 decode tokens per prompt: BF16, the stock FP8 kernel, and a simulated FP8 rounding with BF16 attention. If the stock kernel fails but the simulated rounding does not, the problem is the kernel (as in vLLM's 128K NIAH drop from 91% to 13%). The answer is then to fix the kernel, not to gate layers. Gating is used only when the error sits in a few layers. NVIDIA's docs trace Qwen2.5-7B's FP8 loss to very large values in its last layer, and R1-Distill-Qwen-7B uses the same architecture. With 1 of 28 layers in BF16, R1-Distill gets 1.93× the KV capacity and decode tokens/s of BF16 at 32K. That is 96.5% of what FP8 everywhere would give. The probe costs about 9 GPU-minutes (about $0.38).
VALUE: On models where FP8 fails, it gives about 1.9× the throughput per request of the usual BF16 fallback, for $0.38 of probing. On models where FP8 already works, it changes nothing and only certifies FP8. On Gemma-3-1B it drops to 1.0–1.5×.

IDEA 3
NAME: Turn-granular reversible KV eviction
MECHANISM: Anchor kept: a query-agnostic score in the style of KVzip decides which ~30% of the FP8 KV stays on the GPU, and the evicted pages stay in CPU memory where they can be recalled, not deleted. The repair moves recall from every decode step to once per user turn. When a new message arrives, its query vectors are scored against page summaries (min/max keys, about 1% of HBM) and the top 10% of offloaded pages are fetched in one ~8 ms burst that overlaps the message's prefill. A per-step Quest-style "valve" is capped at ≤0.36% of the context per step. This cuts PCIe load from 25.8× the step time (the killed design) to 0.08×. At 32K context that is 64 vs 26 active users per H100 and 2.49× decode tokens/s over FP8-full. Turn-start reload from CPU drops from 84 to 34 ms. The binding quantity is the residency-scoring cost: the design only pays if scoring costs ≤0.29× prefill on trace-average turns (7.6K new tokens), or the turns are short follow-ups on a shared context. So the residency score has to be cheap (an observation window or KVzip's static head-level score), not KVzip's full context-reconstruction pass.
VALUE: In multi-turn shared-context chat (≈500 new tokens per turn) it costs 0.49–0.61× the GPU-seconds per request of FP8-full; on document-heavy turns with full KVzip scoring it costs 1.5–2.2× and loses.

IDEA 4
NAME: FLOP-per-byte bounded-tier admission
MECHANISM: Anchor kept: score cached prefixes by (expected reuses × recompute FLOPs) ÷ bytes, with exact reuse only. The repair applies the score only where capacity or writes are actually bounded, since the replay confirmed it gives 0% at ≥25M tokens. The first place is the HBM-only prefix cache, as leaf-only eviction with a 180 s reuse half-life. On replayed Mooncake traces at 0.5–1M tokens it saves 43–75% more prefill FLOPs than LRU for Llama-8B and 156–207% more for DeepSeek-V3 (MLA), and it is never more than 5% worse at any capacity. The second place is SSD admission under an endurance budget. There the score must cover the whole prefix chain, because per-block admission keeps deep blocks whose ancestors are missing and gets about zero value. For DeepSeek-V3 it keeps 37–95% more SSD-hit FLOPs per byte written than random admission at a 10–35% write budget. In $ form the score gives the threshold directly: admit if P(reuse) ≥ $wear/byte ÷ $recompute/byte, which is 0.04 for DSv3 and 0.21 for 8B.
VALUE: For MLA-class models in a capacity-short or write-capped last tier it doubles or triples useful hits per byte. For dense 8B models, or any tier above about 5M tokens, it is worth ≤3% of node cost, because write-all SSD wear costs only $17 per day against $576 per day for the GPU node.

