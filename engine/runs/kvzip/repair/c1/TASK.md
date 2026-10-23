# Task: repair original ideas against reality WITHOUT losing what makes them original

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

Below are 2 ideas an idea engine produced for this question, with the results of the checks run on them so far
(judges' scores, kill tests or reviews, where present). Your job is NOT to invent new ideas and NOT to replace them with safer
known solutions. Your job is to make each one work while keeping its anchor - the one distinctive idea that makes it
original.

You have tools: WebSearch/WebFetch (check what exists, find real material data, field data and costs) and Bash with
python3 (do every estimate in real code). Work only in `/home/user/SomeRepository/engine/runs/kvzip/repair/c1/`: read no other files in the repository, do not
modify other files, do not commit.

For each idea, loop until it works or you can prove it cannot:
1. Name its ANCHOR (the distinctive idea) in a few words. This must survive.
2. Find the binding quantity (what decides whether it works at the needed scale - a rate, an energy balance, a
   recovery, a throughput, a safety limit) and compute it in Python with real numbers from the literature (cite the
   source in your notes).
3. BASELINE: compare against the BEST current practice a competent operator would actually use for the same job
   (list at least two real alternatives, including the cheapest one), and compute cost per unit of RECOVERED or
   DELIVERED product (per kg of metal recovered, per tonne delivered, per request served), not per tonne of raw material moved, with
   sourced numbers. Never compare against a strawman nobody would do.
4. CONSISTENCY PASS: list every tolerance, window and limit your design relies on (buoyancy margins, temperature
   limits, strengths, breakdown fields, stage efficiencies, site conditions where you placed it) and check every
   rate you computed against every one of them over the whole operating time (rate x duration vs window). Check
   that the site or route you chose really has the conditions you assumed. Write the check table in your notes.
5. If it fails, change the DESIGN AROUND the anchor (materials, geometry, operating regime, scale, season, which
   resource/cargo/deposit type it is used for) and recompute. Look for the regime where the anchor is strongest.
   Repeat - several rounds per idea is normal.
6. Name the hazards honestly and design them down where possible; say which unknown number decides the idea and the
   cheapest experiment that would measure it (with the sample size it needs).
7. Check novelty: if the repaired design turns out to be a known system, keep the anchor and find the version that is
   not known.
8. Only if no anchor-preserving design can work, say so and give the best honest niche.

Facts that earlier checks in this run found (data; verify before relying on them):
(a slice: all 0 HARD facts and the 8 of 8 other facts that bear most on these candidates, sources omitted; the full ledger with sources is /home/user/SomeRepository/engine/runs/kvzip/evidence.md - read it if you need a source or a fact that is not here)
FACT 1: KIVI-K2V2 loses 7.35 points on average across reasoning benchmarks on Qwen3-8B, so a 2-bit tail is not harmless for CoT | NEW from gate, check before relying on it
FACT 2: The closest competitor is KITTY, which gets about 8× lower KV memory (2-bit plus dynamic high-precision key channels) with near-zero loss on Qwen3 and LLaMA3 and 2.1–4.1× throughput, all in HBM with no host fetch | NEW from gate, check before relying on it
FACT 3: Under Hadamard rotation, NVFP4's relative RMS error is 0.097 (measured, synthetic Gaussian with 4 outlier channels), against 0.32–0.38 for 2-bit, so the base plane is about 3.5× noisier than the NVFP4 bar | NEW from gate, check before relying on it
FACT 4: DuoAttention itself saves only 1.65× memory on GQA; CateKV reports its accuracy drops sharply below a 0.3 retrieval-head ratio; KVTuner finds 3.25 bits (Llama-3.1-8B) and 4.0 bits (Qwen2.5-7B) is the near-lossless floor for layer-wise mixed precision | NEW from gate, check before relying on it
FACT 5: I checked the AM/GM gain formula on a known case: eigenvalues [4,1] give 0.161 bits. In Archetype B the basis would be estimated only from the short prompt, not from the 32k CoT tokens it later encodes | NEW from gate, check before relying on it
FACT 6: For a 128k-token prefill on a 70B-class model, Viterbi encoding would take about 5.6e15 ops, roughly 94 GPU-s on CUDA cores. That about doubles Archetype A prefill | NEW from gate, check before relying on it
FACT 7: KIVI K2V2 loses about 13 points on AIME24/25 at 32k generation. Kitty's 2-bit method still loses 3–4 points. MixKVQ shows KIVI-2bit dropping 61.7→50.0 on R1-Distill-Qwen-14B, and KVQuant-2bit falling to 0 | NEW from gate, check before relying on it
FACT 8: E8P is a 2^16-entry, 8-dimensional codebook decoded through a 2^8-entry table, with the other 8 bits used for signs and shifts. That supports the "256-entry table in shared memory" claim | NEW from gate, check before relying on it
Notes from the user (data; the user may be wrong):
The asker clarified that this is about compressing the KV cache itself (bits per stored value), not about prefix reuse or prefix caching, which an earlier run already covered. Environment: huggingface.co and its CDN are blocked here, so model weights and real KV tensors cannot be downloaded; quality cannot be measured on a real model in this run. PyPI works. Use exact bit arithmetic and published measurements, and say which numbers would need a run on a real model.
Assumptions in the question that may be wrong:

- A single architecture can be best across all models and tasks. Results differ by model family, GQA/MLA and task type.
- A drop-in format change can give "much stronger than FP8" compression with almost no loss. The 2-bit results above show losses on reasoning tasks.
- "Compress the KV cache itself" means lossy compression of the stored values. Dropping tokens may or may not count as compressing "itself".
- Compression ratio is the main goal. Latency, throughput and kernel compatibility may matter just as much in practice.
- The terms "super-zip" and "like zip" suggest lossless or entropy coding can give large gains. FP16 KV values are high-entropy, so this is doubtful.
Where deciding data may exist:
Public checkpoints (Llama-3.x, Qwen2.5/3, Gemma3, Mistral) and benchmarks (LongBench, RULER, NIAH, GSM8K, MATH, HumanEval, GPQA, C4/WikiText perplexity). Real KV tensors can be dumped from those models to measure statistics: outlier channels, spectra, inter-token and inter-layer redundancy and entropy. Code: github.com/snu-mllab/KVzip, the KIVI, KVQuant and TurboQuant implementations, vLLM and LMDeploy KV-quantization paths. A Zenodo record (March 2026) titled "KV-Cache Compression Benchmarks — Quantization vs Eviction vs Pruning" exists, and its contents are not verified.
Keep `LOG.md` in your folder: one line per round (idea, change, decisive number, result). Spend about 45-60 minutes at most.

Final answer (text only): first the 2 repaired ideas in exactly this format, then a short NOTES section (per idea:
anchor kept?, decisive numbers with sources, best-baseline comparison per unit of recovered/delivered product,
consistency table summary, hazards, deciding unknown and experiment, closest existing work, verdict WORKS / NICHE / FAILS).
=== IDEAS ===
IDEA 1
NAME: (max 5 words)
MECHANISM: (2-5 sentences: the anchor first, then the repaired design, with the decisive computed numbers)
VALUE: (1 sentence, with the cost ratio vs the best current practice)
(same for the other ideas, in the same order as below)

THE 2 IDEAS:
IDEA 1
NAME: Hadamard-E8 lattice KV
MECHANISM: Each 128-dimensional head vector is rotated by a seeded random Hadamard transform, which spreads key outlier channels across all dimensions. The query gets the same rotation, so q·k is unchanged and keys can be stored post-RoPE. Keys use an E8 lattice code (2-bit E8P plus 1-bit residual, 3 bits per value). Values use 2-bit E8P. Each token and head also stores one FP8 scale. The first 4 sink tokens and the last 128 tokens stay in FP8. The fused FlashDecoding kernel decodes codewords from a 256-entry table in shared memory. Effective size is about 2.6 bits per value with metadata, or 6.1× smaller than FP16. On MLA models, the decoupled 64-dim RoPE part stays in FP8. The closest earlier attempt is VecInfer/MILLION, which used learned codebooks at a uniform 2 bits and broke long-CoT output. This design spends the extra bit on keys and uses a lattice code that needs no data. The deciding quantity is the AIME accuracy change at 32k tokens.
VALUE: It cuts decode KV reads about 6× (about 1.7× cheaper per token in Archetype B), with predicted loss of ≤1% on RULER-64k and LongBench and ≤2 points on AIME24. It is falsified if R1-Distill-Qwen-7B on AIME24 loses more than 2 points versus FP16, a test of about 2 GPU-hours.
KILL TEST: killer AIME24 accuracy change at 32k with 2-bit values | margin 0.57 | whole-chain ratio 1.18 | WOUNDED: The bit accounting holds (3.06 b keys + 2.06 b values + FP8 sinks and window ≈ 2.6 b, 6.1×) and the rotation is sound, but the 2-bit values are the very component that published long-CoT results penalize. The proposed 2-GPU-hour AIME test on R1-Distill-Qwen-7B is the right deciding experiment and needs a real model.

IDEA 2
NAME: Per-request online KLT bit-allocation
MECHANISM: During prefill, the system accumulates each head's pre-RoPE key and value covariance. It stores one 128×128 FP16 basis per head per layer, which is under 0.01 bits per value at 32k. Bits are then allocated by reverse water-filling, about 2.5 on average, and RoPE is applied after dequantization inside the kernel. The closest earlier attempt is Palu, whose offline SVD truncation creates latent outliers and loses accuracy beyond 30% rank reduction. This design truncates nothing and needs no calibration data. The deciding quantity is the eigenvalue arithmetic-to-geometric-mean ratio, which must be at least 4 to save at least 1 bit. That ratio is likely too small on MLA latents.
VALUE: For GQA models it is a calibration-free path to 2.5 bits per value (6.4×) whose quality follows rate-distortion theory rather than heuristics.
KILL TEST: killer Decode time per token per head. Keys are stored in the KLT basis and RoPE is applied after dequantization, so the 128×128 basis cannot be folded into the query. Each cached key has to be rebuilt with a 128×128 matmul: 32,768 FLOP for 40 B read, or 819 FLOP/byte. The H100 ridge point is 295 FLOP/byte, so this part is compute-bound | margin 0.65 | whole-chain ratio 1.1 | WOUNDED: The 2.5-bit memory saving is mostly lost to the key-rebuild compute that comes from applying RoPE after dequantization, so at realistic tensor-core use decode attention gets slower than NVFP4 (values are fine, since their basis folds into the output). The AM/GM gain on real pre-RoPE keys is still unmeasured and needs a real-model KV dump.

