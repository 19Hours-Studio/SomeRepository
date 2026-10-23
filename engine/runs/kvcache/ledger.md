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
