=== REFRAMES ===

**ASSUMPTIONS:**
- One design can be best on memory, speed and quality together. (contradicted: rankings flip with query visibility, per the 2026 matched-budget audit; there is no single winner on reasoning workloads, per "Hold Onto That Thought")
- A smaller cache can give "the same outputs". (contradicted: only paging and exact prefix reuse are bit-identical; FP8 is only near-lossless, and CacheBlend approximates)
- It works on "any model" with no calibration. (contradicted: FP8 degrades on R1-Distill-Qwen-7B and Gemma-3-1B; hybrid sliding-window layers must skip FP8; DuoAttention drops from 2.55× to 1.67× on GQA; KVQuant and DuoAttention need calibration)
- The KV cache is the dominant cost term. (contradicted: it is 12% in short-context serving B; prefill attention, 28%, outweighs the KV read, 25%, in A; the Arc study found prefill compute was the bottleneck)
- A cheaper cache means a cheaper request on every deployment. (contradicted: the hosted-API ceiling is 3.3×, so there is no room)
- The right baseline is FP16. (contradicted: FP8 is the current default)
- Perplexity and LongBench are enough evidence. (contradicted: they hide multi-turn, long-output and reasoning failures)
- Eviction is safe for queries that arrive later. (contradicted: losses appear at 10% eviction under multi-query use; SnapKV scores 0 F1 on long-output tasks)
- The cache layout can be swapped independently of kernels and the serving stack. (contradicted: the FP8 128K needle regression depended on the kernel; TurboQuant was slower)
- Published evidence covers current architectures. (contradicted: mostly Llama, Mistral and Qwen; hybrid and SSM models were not tested)

**REFRAME 1:** Instead of asking for one best design, build a decision table. Rows are workload (A/B/D) × whether the query is visible at compression time × architecture class. For each cell, which training-free cache design gives the largest verified gain over FP8 at a fixed tolerance (for example ≤1 point on RULER, SCBench multi-turn and a long-reasoning set)? | CHANGES: target goes from one winner to a conditional map; baseline goes from FP16 to FP8; quality is defined by matched-budget failure-mode benchmarks | IMPORTANCE: high | POSSIBILITY: high | WHY: the material shows rankings do not transfer, and a map keeps the asker's "best" while making it checkable.

**REFRAME 2:** For self-hosted shared-prefix workloads (RAG and multi-turn, archetype D), which cache storage and reuse design cuts GPU-seconds per request the most against stock vLLM prefix caching? At what hit rate, prefix length and link bandwidth does loading stop beating recompute? | CHANGES: scope narrows to the workload with room (prefill recompute is 66% of cost, ceiling 10×); unit becomes GPU-seconds per request; the baseline is competent | IMPORTANCE: high | POSSIBILITY: high | WHY: it is the only archetype where 3× is reachable, and the crossover is a computable number that a benchmark can falsify.

**REFRAME 3:** Replace "works on any model" with a prediction problem. Which architecture or activation properties (GQA ratio, sliding-window or hybrid layers, outlier channels, reasoning distillation) predict whether a calibration-free KV quantizer below FP8 stays within tolerance? Can a cheap pre-deployment probe, run before rollout, predict the failure? | CHANGES: an impossible universal claim becomes a testable per-model gate | IMPORTANCE: high | POSSIBILITY: medium | WHY: the failures on R1-Distill and Gemma give known positive cases to validate a predictor against.

**REFRAME 4:** For long-context single requests (A, 128K), which training-free combination that keeps every token cuts both prefill attention and the decode KV read enough to reach ≥2× end-to-end, scored on RULER-128K against FP8? | CHANGES: target goes from cache size to end-to-end GPU-seconds, across two cost terms | IMPORTANCE: medium | POSSIBILITY: medium | WHY: the KV read is only 25%, and 3× needs three terms each cut 10× (TIGHT).

**REFRAME 5:** For multi-user serving (B), at what context length and SLA does KV capacity, rather than prefill compute or weight reads, become the binding limit on goodput? Above that point, how much does compression beyond FP8 add? | CHANGES: target goes from cache design to finding where cache design matters | IMPORTANCE: medium | POSSIBILITY: high | WHY: the KV share is 12% at 1K context and grows with length, so a threshold exists but is narrow.

**REFRAME 6:** On hosted APIs (C), reframe the problem as client-side context management (what to resend or summarize) rather than cache design. | CHANGES: the means move out of the cache | IMPORTANCE: low | POSSIBILITY: low | WHY: the provider margin (assumed 30%) caps the gain at 3.3×, and the provider controls the cache.

**KEEP:** 1, 2