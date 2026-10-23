**Criteria for "best":** (1) GPU-seconds or $ per request; (2) accuracy change against an **FP8-KV baseline**, measured on RULER, SCBench multi-turn and long reasoning, because perplexity and LongBench hide failures; (3) calibration cost per model; (4) whether outputs stay bit-identical.

**Where room exists (from the ledger):**
- **D (shared-prefix RAG/chat):** prefill recompute is 66% of cost, so a 10× cut gives 2.46×. This is the only archetype with ROOM.
- **A (128K single request):** KV read is 25%. Even a 10× cut gives only 1.29×.
- **B (short-context serving):** KV is about 12% of cost.
- **C (hosted API):** the ceiling is 3.3×, mostly taken by provider margin. KV design cannot reach 3× there.

**"Any model, no training" is false as stated:**
- Only exact prefix reuse is bit-identical everywhere.
- FP8 KV is near-lossless on 8 dense GQA models, but degrades on DeepSeek-R1-Distill-Qwen-7B and Gemma-3-1B. It must be skipped on sliding-window layers ([vLLM](https://vllm.ai/blog/2026-04-22-fp8-kvcache)).
- No method I found was tested on hybrid or SSM models. MLA models already have a compressed latent cache, so KV-specific gains shrink there.
- The figures above are the authors' claims or my roofline estimates. I ran nothing.

**Falsification tests:**
- **Prefix reuse:** measure TTFT and $/request against hit rate. It is wrong if the break-even hit rate exceeds about 30% on NVMe.
- **Reversible eviction:** run SCBench multi-turn and RULER-128K at matched memory. It is wrong if it loses more than 1 point to FP8, or if throughput falls below FP8.
- **Per-model gate:** add a Gemma-3 or R1-Distill model. The gate must reject them, otherwise it is not catching known failures.

=== IDEAS ===
IDEA 1
NAME: Exact-prefix tiered KV reuse
MECHANISM: Hash each KV block by its exact token prefix, as in vLLM prefix caching, and spill cold blocks to CPU or NVMe through LMCache in the model's native KV dtype. On a hit, the server streams blocks back over PCIe instead of recomputing prefill, so the outputs stay bit-identical. The closest earlier attempts are CacheBlend, which is approximate and limited to 3 models, and CacheGen, which only helps when loading beats recompute. This design avoids CacheBlend's problem because it accepts only exact prefixes. It avoids CacheGen's problem because local PCIe loads 2.6 GB in about 0.1 s against about 0.76 s of prefill (my estimate). The deciding quantity is the hit rate times the prefill saved, compared with the load time from the slowest tier used.
VALUE: In shared-prefix workloads it can cut cost up to about 2.4× with no change to outputs, but it fails on low hit rates, reordered RAG chunks and SSD-only tiers.

IDEA 2
NAME: Reversible eviction with offload
MECHANISM: Score tokens query-agnostically, in the style of KVzip, and keep about 30% on the GPU in FP8. Move the evicted blocks to CPU memory instead of deleting them. Each decode step, retrieve them page by page, as Quest does, whenever their score against the current query passes a threshold. The closest earlier attempt is permanent eviction, which fails in multi-turn chat (SCBench, FlowKV), whereas this keeps O(n) total memory. The deciding quantity is the recall rate of offloaded pages per step multiplied by the PCIe cost.
VALUE: It gives roughly 3× more concurrent users or context per GPU in multi-turn chat while staying close to FP8 accuracy, but it stalls when recall exceeds the PCIe budget.

IDEA 3
NAME: Gated per-model FP8 KV
MECHANISM: Before deployment, run a 30-minute check per model that compares FP8 KV against BF16 on RULER-128K needles and a reasoning set. Enable FP8 for each layer only where accuracy holds, and keep BF16 on sliding-window layers or any layer that fails. The closest earlier attempt is blanket FP8, which silently degraded R1-Distill and Gemma-3. This design avoids that by measuring each model before enabling FP8. The deciding quantity is the per-model accuracy delta at 128K.
VALUE: It gives a safe 2× capacity default on any dense model, but it is worth only about 1.14× in cost on long single requests and cannot reach 3×.