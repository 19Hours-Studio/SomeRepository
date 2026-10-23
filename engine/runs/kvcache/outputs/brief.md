=== BRIEF ===
TYPE: invent

QUESTION: Which KV-cache design (storage layout, compression, eviction, quantization, offloading or reuse) can be swapped into an existing pretrained transformer LLM with no retraining and no fine-tuning, so that the same model gives the same outputs with a smaller, faster or cheaper cache? The asker wants to take any model and replace one component with another. This design should be the best across memory, speed and quality. "Best" is not defined. The answer should say which metric or workload it is best for, and where it stops working. Plausible workloads are long-context single requests, multi-user serving, multi-turn chat and prefix reuse. The asker did not give a model family, hardware, context length or serving stack. The answer may be a ranking of existing approaches, a new combination of them, or a new idea. Each claim must be checkable against published benchmarks or an experiment that can be run.

SUCCESS:
- It names the criteria that define "best" (memory saved, throughput or latency, accuracy loss, calibration cost) and the workload each applies to.
- It checks "no training, any model" against published evidence: which models and architectures it was tested on, and what happens on an architecture it was not tested on.
- It gives numbers (compression ratio, accuracy change on benchmarks such as RULER, LongBench or multi-turn tasks, throughput) with sources.
- It states the conditions under which it fails, including a compression level, a task type and a model type.
- If it proposes something new, it gives a test that could show the idea is wrong.

CONSTRAINTS:
- No retraining and no fine-tuning of the model weights.
- It should be near plug-and-play and work on "any" model. See ASSUMPTIONS on whether that is possible.

CONTEXT:
- NVIDIA's kvpress library implements many KV-compression methods ("presses") on Hugging Face transformers. Its leaderboard scores them on RULER at 4k context with Llama-3.1-8B. Source: github.com/NVIDIA/kvpress; nvidia-kvpress-leaderboard.hf.space
- KIVI is a tuning-free, asymmetric 2-bit KV quantization (keys per channel, values per token). The authors report about 2.6x less peak memory and 2.35–3.47x throughput on Llama-2, Falcon and Mistral. Source: arxiv.org/abs/2402.02750 (the throughput figures are from secondary summaries).
- Paged blocks, automatic prefix caching and offloading (vLLM, LMCache) change how the cache is stored or reused without altering the model's computation. Reuse is exact only when prefixes match. The reported gains (for example TTFT of about 11 s down to about 1.5 s) come from blogs and are unverified. Source: the premai.io and introl.com blogs.
- Eviction methods (H2O, SnapKV, StreamingLLM) are training-free but lossy. A 2026 audit found policies with similar accuracy fail differently, for example on absent-needle trials. Source: neurips.cc/virtual/2026/173796
- A secondary report says that seven eviction strategies fail at prompt boundaries unless part of the cache is protected. The original paper was not checked. Source: themodelwire.com
- NaCl argues that earlier eviction results are over-optimistic because the benchmarks are too weak. Source: arxiv.org/html/2408.03675v2
- A vendor benchmark found that a training-free norm-based press failed at 80% compression, while a retrofitted model (DMS) did not. This is one model, from a vendor with an interest. Source: Hyperstack kvpress tutorial.
- KVzap, KVzip and Expected Attention are recent training-free scorers, but the claims come from NVIDIA-affiliated or the authors' own papers. Source: arxiv.org/pdf/2510.00636
- The "KV cache" differs by architecture. GQA/MQA, MLA, sliding-window, state-space and hybrid models all have different caches, so methods do not transfer automatically. This is background knowledge and was not searched.

DATA:
- kvpress leaderboard and its benchmark code (RULER, LongBench, InfiniteBench).
- Public benchmarks: RULER, LongBench, Needle-in-a-Haystack, and the multi-turn OASST2-4k used in the KVP paper.
- Open implementations (kvpress, vLLM, LMCache, the KIVI repository) can be run on small open models to measure memory, latency and accuracy.
- The papers cited above, for ablations on models and bit-widths.

ASSUMPTIONS:
- One "best" architecture exists regardless of workload and model.
- Replacement is truly drop-in for any model. Method support differs by attention type (GQA, MLA, sliding-window, hybrid), by framework and by kernel.
- Training-free methods do not lose quality. Most lossy ones (eviction, 2-bit quantization) trade quality for savings, and the loss grows with compression.
- "Without retraining" means no calibration either. Some methods need a small calibration pass, which is not training but may not be "just swap".
- The "KV cache" is one thing. Storage layout (paging), compression and cross-request reuse are different layers that can be combined.

CORRECTED: Wording is clarified, not changed. "Best" is split into criteria and workloads. "Any model" is treated as a claim to test. Exact reuse (prefix caching, paging) is separated from lossy compression, because the question mixes them.

UNCLEAR:
1. What matters most: memory, speed, long context, many users, or output quality? Is a small quality loss acceptable?
2. Which models and serving stack (for example Llama or Qwen on vLLM or Hugging Face) and which GPU?
3. Does "without calibration" also rule out a short data-driven calibration step?

MODE: standard

Sources:
- [NVIDIA kvpress](https://github.com/NVIDIA/kvpress)
- [KVPress leaderboard](https://nvidia-kvpress-leaderboard.hf.space)
- [KIVI](https://arxiv.org/pdf/2402.02750)
- [Expected Attention](https://arxiv.org/pdf/2510.00636)
- [NaCl](https://arxiv.org/html/2408.03675v2)
- [Multilingual audit of numeric retrieval under KV-cache eviction](https://neurips.cc/virtual/2026/173796)
- [Learning to Evict from Key-Value Cache](https://arxiv.org/html/2602.10238)
- [Protection Is (Nearly) All You Need](https://themodelwire.com/article/protection-is-nearly-all-you-need-structural-protection-dominates-scoring-in-glo-01KRZ1B88RPX4TF2V03S4Z2FYN)
- [Hyperstack kvpress tutorial](https://www.hyperstack.cloud/technical-resources/tutorials/optimizing-long-context-llms-with-kvpress-compression-on-hyperstack)
- [premai.io KV cache blog](https://blog.premai.io/kv-cache-optimization-pagedattention-prefix-caching-memory-management)
- [introl.com KV cache guide](https://introl.com/blog/kv-cache-optimization-memory-efficiency-production-llms-guide)