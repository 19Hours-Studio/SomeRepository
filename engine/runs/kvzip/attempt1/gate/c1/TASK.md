# Task: kill test - find the one number that decides whether each idea lives

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

Below are 4 candidate ideas. You are a screening engineer with tools: WebSearch (WebFetch may not reach hosts; use
search excerpts) and Bash with python3 (pip install from PyPI works). Do not improve or redesign the ideas; judge them
as written. Work only in `/home/user/SomeRepository/engine/runs/kvzip/gate/c1/`: write files only there, do not commit.

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
The asker clarified that this is about compressing the KV cache itself (bits per stored value), not about prefix reuse or prefix caching, which an earlier run already covered. Environment: huggingface.co and its CDN are blocked here, so model weights and real KV tensors cannot be downloaded; quality cannot be measured on a real model in this run. PyPI works. Use exact bit arithmetic and published measurements, and say which numbers would need a run on a real model.
Assumptions in the question that may be wrong:

- A single architecture can be best across all models and tasks. Results differ by model family, GQA/MLA and task type.
- A drop-in format change can give "much stronger than FP8" compression with almost no loss. The 2-bit results above show losses on reasoning tasks.
- "Compress the KV cache itself" means lossy compression of the stored values. Dropping tokens may or may not count as compressing "itself".
- Compression ratio is the main goal. Latency, throughput and kernel compatibility may matter just as much in practice.
- The terms "super-zip" and "like zip" suggest lossless or entropy coding can give large gains. FP16 KV values are high-entropy, so this is doubtful.
Where deciding data may exist:
Public checkpoints (Llama-3.x, Qwen2.5/3, Gemma3, Mistral) and benchmarks (LongBench, RULER, NIAH, GSM8K, MATH, HumanEval, GPQA, C4/WikiText perplexity). Real KV tensors can be dumped from those models to measure statistics: outlier channels, spectra, inter-token and inter-layer redundancy and entropy. Code: github.com/snu-mllab/KVzip, the KIVI, KVQuant and TurboQuant implementations, vLLM and LMDeploy KV-quantization paths. A Zenodo record (March 2026) titled "KV-Cache Compression Benchmarks — Quantization vs Eviction vs Pruning" exists, and its contents are not verified.

Value ledger (data):
Method: the searches gave sourced unit numbers (KV bytes per token, GPU prices, cache prices). The % shares are my own roofline arithmetic from those numbers, with the assumptions stated. They are not published breakdowns. "Other" is an assumed margin/overhead share in every case.

**ARCHETYPE A: long-document QA or RAG, 128k tokens in and about 0.5k out. Llama-3-70B-class model with GQA, FP8 weights and FP8 KV, vLLM with chunked prefill and paged KV, TP8 on H100.** | cost ≈ 21 GB of HBM held per request (327 KB/token at FP16, halved for FP8, × 131k) and ≈ 105 GPU-seconds per request, about $0.07 at $2.5/GPU-h | price: H100 rents for roughly $2–4/GPU-h on specialist clouds, $7–12 on hyperscalers
Assumptions: batch 8, 400 TFLOP/s effective, 3.35 TB/s per GPU. Prefill is about 4e16 FLOPs: 1.8e16 in linear layers plus 2.2e16 in attention.
SHARES: prefill attention 48% | prefill linear layers 39% | decode KV reads 3% | decode weight reads 1% | other 9%
LARGEST: prefill attention. A 10x cut removes about 43% of the cost. A KV storage format barely touches this term. KV compression mainly buys capacity (batch size and context length) and decode speed, not prefill.

**ARCHETYPE B: reasoning-model chain of thought, 32k generated tokens. DeepSeek-R1-Distill-class dense GQA model, FP16 or FP8 KV, vLLM, batch about 10 per GPU.** | cost ≈ 37 GPU-seconds, about $0.025, per 32k-token solution. KV is 4.3 GB at the end for an 8B model at FP16 (128 KB/token). | price: not applicable
Sourced anchor: SkipKV reports that for the 8B model at batch 10 the KV cache is about 2.5× the weights. My calculation gives roughly 2.7×, which is consistent.
SHARES: decode KV reads 50% | decode weight reads 36% | kernel, launch and sampling overhead 5% | prefill 1% | other 8%
LARGEST: decode KV reads. A 10x cut removes about 45%. This is where an aggressive KV format pays most. KV capacity also caps the batch size, so a smaller cache also lowers the weight-read share per request. Prefill-oriented compression methods are reported to fail on long outputs.

**ARCHETYPE C: multi-turn agent or chat with prefix-cache reuse. 100k-token context, 90% hit, 10k new tokens and 1k output per turn, through a commercial API with a cache layer, or LMCache-style CPU/SSD offload.** | cost ≈ $0.08 per turn at Sonnet-class list prices: $0.30/MTok cache read, $3 base input, 1.25× cache write, $15 output | price: this is the list price, so cost and price are conflated
The price shape is cache-read 0.1× and cache-write 1.25× of base input (Anthropic docs). OpenAI is cited at 0.5× and Google at 0.25×, but those figures come from third-party sources. DeepSeek reported 56.3% of its input tokens (342B of 608B) hit its on-disk KV cache.
SHARES: cache-read input 27% | new-input prefill plus cache write 38% | output decode 15% | KV storage and transfer (hidden inside the prices above) 0% (unobserved) | other 20%
LARGEST: new-input prefill and cache write. A 10x cut removes about 34%. The real KV storage and transfer cost is not visible from outside the provider. A denser KV format would mainly raise the hit rate and cut the cache-read price. I have no sourced split for this.

**ARCHETYPE D: MLA model serving (DeepSeek-V3-class), 32k context, large expert-parallel decode.** | cost ≈ 70 KB of KV per token (the sourced figure, against 516 KB for Llama-3.1-405B and 327 KB for Qwen-2.5-72B), so about 2.2 GB of KV read per request per decode step at 32k, and 9.2 GB held at 128k | price: not found. The $87,072/day and 545% margin figures did not appear in the results, so I cite only the 56.3% hit rate.
SHARES (estimate, no sourced breakdown): decode KV latent reads 30% | MoE expert weight reads 25% | attention compute including latent up-projection 15% | all-to-all communication 15% | other 15%
LARGEST: decode KV latent reads. A 10x cut removes about 27%. This share is lower than in A and B because MLA already shrinks the cache about 5–7×. MLA latents are low-rank and RoPE is decoupled, so key-outlier and RoPE tricks designed for GQA may not transfer.

**Reading across the archetypes for the "super-zip" question**
- The gain is concentrated in reasoning and other decode-heavy, high-batch serving. There KV reads are about half the cost (B).
- In prefill-dominated long-document QA, a KV format changes only about 4–5% of GPU time (A). Its value there is fitting more requests per GPU.
- NVIDIA reports NVFP4 KV at up to 50% less memory than FP8, with under 1% accuracy loss on LiveCodeBench, MMLU-PRO, MBPP and RULER-64K. That is about 4 bits per value, or roughly 4× against FP16, which sets the bar to beat.
- Any proposed format should be scored on the decode KV-read share (B), the HBM bytes per request (A), and the cache hit rate (C).

SOURCES:
- https://www.morphllm.com/grouped-query-attention
- https://blogs.vmware.com/cloud-foundation/2024/09/25/llm-inference-sizing-and-performance-guidance/
- https://arxiv.org/pdf/2505.09343
- https://arxiv.org/pdf/2602.20732
- https://developer.nvidia.com/blog/optimizing-inference-for-long-context-and-large-batch-sizes-with-nvfp4-kv-cache/
- https://web.ece.ucsb.edu/~zhengzhang/conf/2026-MLSys-SkipKV.pdf
- https://intuitionlabs.ai/articles/h100-rental-prices-cloud-comparison
- https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching
- https://docs.helicone.ai/gateway/concepts/prompt-caching
- https://gigazine.net/news/20250303-deepseek-ai-cost-profit
- https://pypi.org/project/lmcache-cli/0.5.3.dev0/

Ceilings computed from the ledger (data):
Target: 3x cheaper. Ceiling = 1 / (share no engineering can touch: taxes, royalties, fees, margins). 'needs' = the fewest cost terms that must each fall 10x to reach the target.
ARCHETYPE A: long-document QA or RAG, 128k tokens in and about 0.5k out. Llama-3-70B-class model with G | untouchable 9.0% -> ceiling 11.1x | 10x cut of one term: prefill attention 1.76x; prefill linear layers 1.54x; decode kv reads 1.03x; decode weight reads 1.01x | 3x needs: prefill attention, prefill linear layers | ROOM
ARCHETYPE B: reasoning-model chain of thought, 32k generated tokens. DeepSeek-R1-Distill-class dense GQ | untouchable 8.0% -> ceiling 12.5x | 10x cut of one term: decode kv reads 1.82x; decode weight reads 1.48x; kernel, launch and sampling overhead 1.05x; prefill 1.01x | 3x needs: decode kv reads, decode weight reads | ROOM
ARCHETYPE C: multi-turn agent or chat with prefix-cache reuse. 100k-token context, 90% hit, 10k new tok | untouchable 20.0% -> ceiling 5.0x | 10x cut of one term: new-input prefill plus cache write 1.52x; cache-read input 1.32x; output decode 1.16x; kv storage and transfer 1.00x | 3x needs: new-input prefill plus cache write, cache-read input, output decode | TIGHT
ARCHETYPE D: MLA model serving (DeepSeek-V3-class), 32k context, large expert-parallel decode.** | untouchable 15.0% -> ceiling 6.7x | 10x cut of one term: decode kv latent reads 1.37x; moe expert weight reads 1.29x; attention compute including latent up-projection 1.16x; all-to-all communication 1.16x | 3x needs: decode kv latent reads, moe expert weight reads, attention compute including latent up-projection, all-to-all communication | NO ROOM

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
NAME: Entropy-measured per-head bit allocation
MECHANISM: During prefill, compute each KV head's attention entropy over the prompt's own queries. Assign bit widths from that: broad heads get K2V1, middle heads K3V2, and sharp retrieval heads K4V4. Every token is kept, and the bits average about 2.1 including scales, or 7.5×. The closest earlier attempts are RazorAttention and DuoAttention. They evicted tokens in non-retrieval heads and saved only 1.67× on GQA. This design only lowers precision, which works on already-shared GQA heads and keeps multi-turn reuse safe. The deciding quantity is how stable head entropy rankings are across prompts and decode phases, measured by a Spearman rank correlation of at least 0.9.
VALUE: About 7.5× compression without calibration data, adapting per prompt to any GQA model.

IDEA 2
NAME: Progressive bit-plane attention
MECHANISM: K and V are stored after a Hadamard rotation as a 2-bit base plane plus a 2-bit refinement plane, with per-group FP8 scales, for about 4.3 bits per value in total. On each decode step the kernel first scores all tokens using the base plane. It then reads refinement planes only for the top 2% of pages by score plus the sink pages, and recomputes their logits and values at 4-bit precision. The closest earlier attempts are Quest and ShadowKV, which skip pages entirely and therefore act like eviction. Here every token is still attended, and only precision varies with the query, so multi-turn reuse and question changes are safe. The deciding quantity is the attention mass covered by the top 2%, which must be at least 99% on long CoT.
VALUE: HBM reads fall to about 2.2 bits per value (about 7× fewer than FP16) at roughly NVFP4 quality. Refinement planes can be offloaded to host memory to gain capacity. The added cost is an estimated 10–15% from the two-pass kernel. It is falsified if logit KL divergence versus FP16 exceeds NVFP4's on RULER-niah-multikey.

IDEA 3
NAME: Bit-plane on-demand attention precision
MECHANISM: Keys are stored pre-RoPE and rotated, then quantized to 4-bit codes laid out as bit-planes, at 4.5 bits per value in HBM. A FlashAttention tile reads only the top 2 planes plus scales (2.5 bits per value, 6.4× fewer bytes than FP16) to score every token. It then fetches the low planes only for the ≈2% of tokens whose coarse logit could land in the top softmax mass; the 4 sink tokens and a 64-token recent window always use full planes. The closest earlier attempts are Quest and ShadowKV, which drop the tokens they do not select and so lose them on reused or multi-turn queries; here no token is ever dropped, and the tail is still read at 2 bits. The deciding quantity is the softmax mass that falls on coarse-only tokens multiplied by their value error; it must stay ≤1e-3 per head.
VALUE: About 2.6 bits read per value during decode, against NVFP4's 4.5. This should give a 1.5–1.6× decode speedup in reasoning workloads, with quality bounded by NVFP4 (≤1% drop on AIME24 and RULER-64K for R1-Distill-8B). It is falsified if a one-day PyTorch prototype misses NVFP4 accuracy on AIME24.

IDEA 4
NAME: Rotated 3-bit fixed-codebook cache
MECHANISM: Keys and values are rotated with a fixed Hadamard matrix after RoPE. Each value is then coded with a fixed 3-bit Lloyd-Max Gaussian codebook, plus one FP8 scale per 64 values, for 3.125 bits per value or about 5.1× versus FP16. Sinks and the recent window stay in FP8, and a FlashAttention kernel dequantizes through an 8-entry lookup table in registers. The closest earlier attempt is TurboQuant, whose QJL residual added attention noise; this design drops QJL and spends that bit budget on the code itself. Anchors are KVQuant (<0.1 perplexity loss at 3 bits) and TurboQuant (neutral at 3.5 bits). The deciding quantity is the AIME accuracy gap at 32k tokens, which must be ≤1 point.
VALUE: A safe ~5× cache, against NVFP4's ~4×, with a predicted ≤1% drop on RULER and LongBench and no calibration.

