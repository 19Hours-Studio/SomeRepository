# Task: adversarial review - find what would make these ideas fail or overstate their value

QUESTION: Which architecture for compressing the LLM KV cache (the stored attention keys and values) is best if it has to be much more aggressive than FP8, which is 8 bits per value or about 2× smaller than FP16/BF16? It has to work as a drop-in replacement for the cache storage format in an existing pretrained transformer model, with no retraining, fine-tuning or architecture change, and with almost no loss of quality. The cache may be compressed along any axis: numeric precision, the number of stored tokens, channels or heads, redundancy across layers, or entropy coding. The asker calls this a "super-zip" for the KV cache. The answer should be a concrete architecture, covering what is stored, how it is encoded and decoded, and how attention reads it. It should also give the expected compression ratio and quality loss on standard long-context and reasoning benchmarks, and say what runtime cost the design adds.
A good answer: 
- It gives a specific, implementable design. Naming a family of methods is not enough.
- It states the effective bits per value or the compression ratio vs FP16, counting all metadata (scales, zero-points, indices, codebooks).
- Quality loss is stated against the FP16 cache on named benchmarks and models, for example LongBench, RULER, needle-in-a-haystack, GSM8K or MATH-style reasoning, and perplexity. "Almost no loss" is given a number, for example ≤1% relative drop.
- It is checked against the failure modes below: outlier channels in keys, RoPE, attention sinks, GQA/MLA models, long contexts, multi-turn or multi-query reuse, and reasoning-model chains of thought.
- It estimates decode and prefill latency and throughput, including dequantization or decompression cost and compatibility with FlashAttention-style fused kernels.
- It shows how it beats or complements the current state of the art (see CONTEXT), and says what is new.
- It names a cheap experiment that could falsify it.
Constraints: 
- No training, fine-tuning or distillation of the base model. The asker said "without retraining". Whether a one-time offline calibration pass on a small data sample counts is UNCLEAR.
- It must apply to any ready-made model by changing the cache storage format only.
- Compression must be far beyond FP8. This is stated as "much stronger" with no numeric target.
- Quality must drop almost not at all.

Below are 4 ideas, already repaired once against reality by a researcher. Your job is to be the toughest competent
outside reviewer: an engineer who will lose money if any of these claims is wrong. You do NOT fix or improve the
ideas; you find their defects, prove each one with a number, and rank them.

You have tools: WebSearch/WebFetch and Bash with python3 (check every claim in real code). Work only in
`/home/user/SomeRepository/engine/runs/kvzip/audit_final/`: read no other files in the repository, do not modify other files, do not commit.

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
NAME: Folded online KLT water-filling
MECHANISM: Anchor kept: each request accumulates its own covariance during prefill, takes a KLT basis from it, and allocates bits per component by reverse water-filling, with no calibration data. The fatal step was rebuilding every key (819 FLOP/B against a 295 FLOP/B ridge). That is removed by computing the KLT on post-RoPE keys, so attention scores from the stored coefficients using q′ = Uᵀq, and by folding the value basis into the output (o = U_v·Σp·c). This adds +0.39% decode FLOPs at 32k. The distortion is weighted by the request's own prefill query covariance. The basis is refreshed every 32k generated tokens. Prompts under 1,024 tokens fall back to Hadamard. The corrected basis overhead is 0.0625 b/value per FP16 basis at 32k, not "<0.01". Total is about 2.74 b at 32k (5.8×). The model's decisive number is that the post-RoPE KLT gains only 0.0–0.3 b over plain RoPE-band energy allocation on RoPE keys. On stores with no RoPE it gains 0.17–1.6 b over Hadamard: values, MLA latents c_KV (folded into the absorbed W_UK/W_UV) and NoPE layers. So the design is retargeted at those stores.
VALUE: For MLA models (DeepSeek-V3/R1, Kimi-K2) and NoPE/iRoPE layers, it is a calibration-free way to read a compressed cache directly in HBM. If the real-tensor gain is ≥0.5 b, it would be about 1.2× cheaper per served token than Hadamard/TurboQuant at the same quality. On ordinary RoPE keys it is about equal to Block-GTQ (≈1.0×).

IDEA 2
NAME: Window-mass per-head precision gating
MECHANISM: The anchor stays: each KV head's precision is set per prompt from the prompt's own attention, measured during prefill, and no token is dropped. Four repairs remove the causes of death. First, 1-bit and 2-bit keys are banned; the menu is now K4V4, K4V3 or K3V2. Second, there is an error target instead of a fixed 2.1-bit budget. Third, ranking heads by entropy (which needed Spearman stability across prompts) is replaced by an absolute gate on m_q, the share of attention that falls outside the FP16 sink-plus-recent window. Fourth, every head gets per-block channel-mean centering (0.125 bit). Deterministic error can stay correlated across tokens, but it is still bounded by rel(b)·m_q, so the gate holds without dither. The thresholds are K3V2 if m_q ≤ 0.133, K4V3 if m_q ≤ 0.31, and K4V4 otherwise. A decode-time Σp² watchdog upgrades a head's new 128-token blocks if it turns sharp during chain-of-thought.
VALUE: 3.22–3.80 bits (4.2–5.0×), with error at most 1.2–1.67× that of uniform 4-bit. That is 57–67 vs 50 concurrent requests (+14–34%). It matches the calibrated KVTuner (about 3.5 bits) while needing no calibration, and it beats uniform K3V3 (3.31 bits, about 2.15× error) on error at the same size.

IDEA 3
NAME: Mass-gated dithered value codes
MECHANISM: The anchor stays: keys and values are treated differently. Keys are always deterministic 4-bit (per-channel, 128-token groups, 4.25 bits with scales), because key error is exponentiated in the softmax. Values carry a subtractive dither regenerated from a position hash, so it costs no stored bits. The repair is where the dither matters. It does not reduce error per value (0.50 relative RMS at 2 bits either way), and simple per-block mean-centering beats it on channel-offset data (0.49 vs 1.33). It is, however, the only one of the three schemes that makes errors on repeated content (repeated phrases, code, CoT loops) shrink as more tokens are averaged: at 60 copies, 0.065 vs 0.44–0.52 for the other schemes. That makes a provable gate possible. Each KV head's value precision is chosen from E_h = √Σp² over its quantized tokens: 4-bit above 0.31, 3-bit for 0.133–0.31, 2-bit for 0.046–0.133, and 1-bit dithered at or below 0.046 (about 470 or more tokens effectively attended). At that 1-bit setting the simulated error is 0.025–0.063, under the 0.10 that single-token 4-bit already gives, while deterministic 1-bit stays at 0.38–1.10. Values are Hadamard-rotated and mean-centered, 4 sink tokens plus the last 128 tokens stay FP16, and E_h is accumulated inside the attention kernel (the maximum over the GQA group, 99th percentile over queries).
VALUE: 3.46–3.95 bits (4.1–4.6×), with total attention-output error at most 1.2–1.43× that of uniform 4-bit. That is 55–60 vs 50 concurrent 32k requests on an H100 (+10–20% requests per GPU), with no calibration.

IDEA 4
NAME: RoPE-band-ranked Hadamard-E8 KV
MECHANISM: Anchor kept: a seeded Hadamard rotation plus an E8 lattice code decoded from a 256-entry shared-memory table. The original design rotated all 128 dimensions globally at one rate, and that is now published work (arXiv 2610.15384, E8 k2v2). It is also the configuration that collapses on reasoning: TurboQuant-MSE K3V2, which uses one rotation and one rate, scores 0.0 on AIME24 (Block-GTQ paper). In the repaired design, the 64 RoPE pairs are ranked by their prefill energy. RoPE never changes a pair's norm, so the ranking holds during decode. They are grouped into 16 bands of 8 dimensions, with a Hadamard rotation inside each band. Bands are coded at 4, 3 or 2 bits with E8 (2b+2b residual, 2b+1b, 2b), giving keys a 3.0-bit average. Values use E8 at 2 bits, which is where E8 helps most. Simulated MSE is 0.091 for E8 against 0.118 for Lloyd-Max and 0.25 for KIVI-style INT2 g128. Each token and head stores one FP8 scale. 4 sink tokens and the last 128 tokens stay in FP16. The query gets the same permutation and band rotation, so keys are stored post-RoPE exactly. Total is 2.62 b/value at 32k (6.1× vs FP16) and 3.0 b at 4k (5.3×). Decode dequantization is 12.5 op/B, under the H100 CUDA-core ridge of about 20 op/B. Prefill encode cost is +0.007%.
VALUE: Same 6× memory and about 6.2× the decode throughput of BF16 at 32k as Block-GTQ K3V2. The prediction is that it loses less on AIME (≤2 points vs −2.5). That would be about $5.06 vs $5.17 per 1,000 correct AIME answers, roughly 2% cheaper, which is a small edge.

