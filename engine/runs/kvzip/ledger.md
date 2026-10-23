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
