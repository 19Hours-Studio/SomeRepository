# Task: kill test - find the one number that decides whether each idea lives

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

Below are 4 candidate ideas. You are a screening engineer with tools: WebSearch (WebFetch may not reach hosts; use
search excerpts) and Bash with python3 (pip install from PyPI works). Do not improve or redesign the ideas; judge them
as written. Work only in `/home/user/SomeRepository/engine/runs/kvcache/gate/c2/`: write files only there, do not commit.

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
Environment: huggingface.co and its CDN are blocked here, so model weights cannot be downloaded; measurements on a real model are impossible in this run. PyPI works. Use exact memory arithmetic (bytes per token from model configs) and published measurements, and say which numbers would need a run on a real model.
Assumptions in the question that may be wrong:

- One "best" architecture exists regardless of workload and model.
- Replacement is truly drop-in for any model. Method support differs by attention type (GQA, MLA, sliding-window, hybrid), by framework and by kernel.
- Training-free methods do not lose quality. Most lossy ones (eviction, 2-bit quantization) trade quality for savings, and the loss grows with compression.
- "Without retraining" means no calibration either. Some methods need a small calibration pass, which is not training but may not be "just swap".
- The "KV cache" is one thing. Storage layout (paging), compression and cross-request reuse are different layers that can be combined.
Where deciding data may exist:

- kvpress leaderboard and its benchmark code (RULER, LongBench, InfiniteBench).
- Public benchmarks: RULER, LongBench, Needle-in-a-Haystack, and the multi-turn OASST2-4k used in the KVP paper.
- Open implementations (kvpress, vLLM, LMCache, the KIVI repository) can be run on small open models to measure memory, latency and accuracy.
- The papers cited above, for ablations on models and bit-widths.

Value ledger (data):
Caveat: only the inputs are sourced (GPU price, KV sizes, API prices, the KIVI and Oracle numbers). The cost splits for A, B and D come from my own roofline-style model, not from a measured profile. I did not run any experiment. The model assumes H100 SXM at about 3.35 TB/s and about 500 TFLOPs effective, both my assumptions. The "other" shares for A, B and D are assumed. C's "other" is an assumed provider margin, not a measured one.

**ARCHETYPE A: Long-context single request.** Llama-3.1-8B, 128K context, BF16 weights, FP8 KV cache in vLLM, one H100 | cost ≈ $0.033 per request (128K tokens in, 1K out; about 28 GPU-seconds at $4.29/h) | target: cut GPU-seconds per request
- Sourced inputs: KV is about 128 KB per token, so about 17 GB per 128K sequence in BF16.
- Each decode step therefore reads about 16 GB of weights plus 17 GB of KV.
- Prefill attention is about 4.4 PFLOP against about 2 PFLOP for the linear layers.

SHARES: prefill attention compute 28% | prefill linear compute 13% | decode KV read 25% | decode weight read 23% | other 11%
LARGEST: prefill attention compute - a 10x cut of it removes 25% of the cost. KV-cache storage design (quantization or eviction) mainly acts on the decode KV read (25%), and a 10x cut there removes 22.5%.

**ARCHETYPE B: Multi-user serving, short to medium context.** Llama-3.1-70B FP8 in vLLM with PagedAttention and an FP8 KV cache, batch about 64, one H100 | cost ≈ $2.6 per 1M output tokens | target: higher tokens/s per GPU
- Throughput input: 460 tok/s at batch 64 (SGLang, one H100, FP8, 256 tokens in, 512 out).
- That works out to $4.29 / (460 × 3600) ≈ $2.6 per 1M output tokens.
- That benchmark is far from bandwidth-bound, so the split below is a rough guess.
- Hugging Face's Intel Arc Pro B70 RULER study found that extra cache capacity rarely raised SLA-qualified short-context concurrency, because prefill compute was the bottleneck.

SHARES: decode weight read 35% | decode KV read 12% | prefill compute 20% | scheduling, comms and sampling overhead 23% | other 10%
LARGEST: decode weight read - a 10x cut removes 31.5%. KV is only about 12% at about 1K context. It grows with context length, since 70B uses about 327 KB per token.

**ARCHETYPE C: Multi-turn agent or chat through a hosted API with prompt caching.** 50K-token context, 1K new tokens and 500 output tokens per turn, Sonnet-class prices | cost ≈ $0.026 per turn with caching, against $0.158 without | price: $3/M input, $0.30/M cache read, $3.75/M cache write, $15/M output
- Cache reads are priced at 0.1× the base input price.
- OpenAI's discount is reported as only about 50%, but only third-party sources say so.

SHARES: cache read 40% | output tokens 20% | cache write for the new turn 10% | other (provider margin, assumed) 30%
LARGEST: cache read - a 10x cut removes 36%. The provider has already moved most of the saving into the price.

**ARCHETYPE D: Self-hosted RAG or multi-turn chat with shared prefixes.** Llama-3.1-8B, 20K-token context, 200 output tokens, batch 16, vLLM prefix caching plus LMCache offload to CPU or SSD | cost ≈ $0.0014 per request without reuse (about 1.15 GPU-seconds) | target: skip prefill on cache hits
- Without reuse, prefill dominates the split below.
- With a hit, loading about 2.6 GB of KV over PCIe takes roughly 0.1 s and can overlap with compute. That is my estimate, not a benchmark.
- Oracle's LMCache run on OCI (Granite 3.3 8B) reported about 2× throughput and a TTFT cut of 50% or more. That is a vendor figure for one setup.

SHARES: prefill recompute 66% | decode KV read 18% | decode weight read 6% | other 10%
LARGEST: prefill recompute - a 10x cut removes 59%. This is the largest and most reachable term anywhere in the ledger.

**What this says for the question**
- **Where KV design bites:** it matters most in D and A, through reuse and the decode KV read.
- **Where it matters less:** in B at short context it is a small term, and in C the provider has already captured the saving.
- **FP8 KV status:** it is the current practical default. Near-lossless RULER results were reported on 8 models, mainly dense GQA models such as Llama, Qwen and Mistral. Degradation was major on DeepSeek-R1-Distill-Qwen-7B and meaningful on Gemma-3-1B.
- **KIVI 2-bit:** it reports 2.6× less peak memory including weights, and 2.35–3.47× throughput from up to 4× larger batches. It was tested on Llama-2, Falcon and Mistral. I found no evidence on newer architectures.
- **Not found:** no measured decode-profile share at 128K, and no RULER-scored throughput study on Llama 3.1. Those would settle the A and B splits.

SOURCES:
- https://vllm.ai/blog/2026-04-22-fp8-kvcache
- https://www.plushcap.com/content/huggingface/blog/huggingface-fp8-kv-cache-on-intel-arctm-pro-b70-2-capacity-with-strong-long-context-throughput-gains
- https://arxiv.org/abs/2402.02750v2
- https://blogs.oracle.com/ai-and-datascience/accelerate-llm-inference-lmcache-on-oci-data-science
- https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching
- https://www.hivenet.com/post/nvidia-h100-pricing
- https://intuitionlabs.ai/articles/h100-rental-prices-cloud-comparison
- https://cerebrium.ai/blog/benchmarking-vllm-sglang-tensorrt-for-llama-3-1-api
- https://mlsysbook.ai/mlsysim/tutorials/03_kv_cache.html

Ceilings computed from the ledger (data):
Target: 3x cheaper. Ceiling = 1 / (share no engineering can touch: taxes, royalties, fees, margins). 'needs' = the fewest cost terms that must each fall 10x to reach the target.
ARCHETYPE A: Long-context single request.** Llama-3.1-8B, 128K context, BF16 weights, FP8 KV cache in v | untouchable 11.0% -> ceiling 9.1x | 10x cut of one term: prefill attention compute 1.34x; decode kv read 1.29x; decode weight read 1.26x; prefill linear compute 1.13x | 3x needs: prefill attention compute, decode kv read, decode weight read | TIGHT
ARCHETYPE B: Multi-user serving, short to medium context.** Llama-3.1-70B FP8 in vLLM with PagedAttenti | untouchable 10.0% -> ceiling 10.0x | 10x cut of one term: decode weight read 1.46x; scheduling, comms and sampling overhead 1.26x; prefill compute 1.22x; decode kv read 1.12x | 3x needs: decode weight read, scheduling, comms and sampling overhead, prefill compute | TIGHT
ARCHETYPE C: Multi-turn agent or chat through a hosted API with prompt caching.** 50K-token context, 1K | untouchable 30.0% -> ceiling 3.3x | 10x cut of one term: cache read 1.56x; output tokens 1.22x; cache write for the new turn 1.10x | 3x needs: impossible even with every physical term cut 10x | NO ROOM
ARCHETYPE D: Self-hosted RAG or multi-turn chat with shared prefixes.** Llama-3.1-8B, 20K-token context | untouchable 10.0% -> ceiling 10.0x | 10x cut of one term: prefill recompute 2.46x; decode kv read 1.19x; decode weight read 1.06x | 3x needs: prefill recompute, decode kv read | ROOM

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
NAME: Tiered exact-prefix KV reuse
MECHANISM: Hash each prefix block, keep hot blocks on GPU and spill cold blocks to CPU/SSD in BF16 (lossless) or FP8, and load them on a hit instead of running prefill again. The closest earlier attempt is CacheBlend/CacheGen. Both are approximate, need extra kernels, and are measured only against full recompute. Exact-prefix hits avoid that limit because outputs are unchanged. The deciding quantity is hit rate h. The gain is 1/(1−0.66·h) minus load overhead, where loading about 2.6 GB over PCIe takes about 0.1 s against about 0.76 s of prefill. The idea is wrong if, on a replayed RAG or chat trace, h is below 0.4 or loads do not overlap with compute, giving a gain under 1.3×.
VALUE: It is the only verified several-fold saving (up to 2.46× ceiling) on self-hosted RAG and multi-turn chat, with identical outputs.

IDEA 2
NAME: Exact tiered prefix store
MECHANISM: Hash fixed-size token blocks of each prompt and keep their FP8 key/value tensors in GPU, CPU and SSD tiers. On a later request with a matching block chain, stream those blocks back instead of recomputing them, overlapping the transfer with prefill of the unmatched suffix. Unlike CacheGen or CacheBlend, nothing is lossily encoded or approximately stitched, so outputs match the uncached run. The deciding quantity is hit rate × prefix length × (recompute time − load time), roughly 32 µs versus 2.6 µs per token for an 8B model.
VALUE: Up to about 2.5× fewer GPU-seconds on shared-prefix RAG and chat, with outputs identical to the uncached run. The hypothesis is falsified if, measured against the same stack with prefix caching off, end-to-end throughput gains less than 1.5× at a 50% hit rate.

IDEA 3
NAME: FP8 tiered exact-prefix store
MECHANISM: Store the FP8 KV blocks the model already produces, hash-keyed by prefix, in GPU, then DRAM, then NVMe, and load them layer by layer, overlapped with compute. The closest earlier attempt is CacheGen; it needed a codec and won only at low bandwidth, whereas this keeps the native FP8 bytes, so a hit gives exactly what recompute would give with no decoder kernel. The deciding quantity is link bandwidth against about 1.5 GB/s for 8B (64 KB/token ÷ about 42 µs/token). It is falsified if TTFT on hits over NVMe is not at least 3× lower than vLLM's GPU-only prefix cache at a matched hit rate.
VALUE: Gives a bit-identical, any-dense-model cut of up to about 2.5× in GPU-seconds for RAG and multi-turn at hit rates near 0.9.

IDEA 4
NAME: Recompute-cost-per-byte store eviction
MECHANISM: Score each stored prefix by (expected reuses × FLOPs saved) ÷ bytes held. Long prefixes score higher because attention cost is superlinear, and expected reuses decay with time since last hit. Evict the lowest scores first, instead of LRU. The closest earlier attempt is CacheBlend, which raised effective hits through approximate non-prefix reuse; this design stays exact by raising the exact hit rate. The deciding quantity is the working set against tier capacity. It is falsified if, on a replayed RAG or chat trace, the hit-weighted FLOPs saved are not at least 15% above LRU at equal capacity.
VALUE: Raises the exact-reuse hit rate h, which sets the 1/(1−0.66h) gain, without changing any model output.

