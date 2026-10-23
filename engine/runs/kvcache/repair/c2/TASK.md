# Task: repair original ideas against reality WITHOUT losing what makes them original

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

Below are 2 ideas an idea engine produced for this question, with the results of the checks run on them so far
(judges' scores, kill tests or reviews, where present). Your job is NOT to invent new ideas and NOT to replace them with safer
known solutions. Your job is to make each one work while keeping its anchor - the one distinctive idea that makes it
original.

You have tools: WebSearch/WebFetch (check what exists, find real material data, field data and costs) and Bash with
python3 (do every estimate in real code). Work only in `/home/user/SomeRepository/engine/runs/kvcache/repair/c2/`: read no other files in the repository, do not
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
(a slice: all 0 HARD facts and the 12 of 14 other facts that bear most on these candidates, sources omitted; the full ledger with sources is /home/user/SomeRepository/engine/runs/kvcache/evidence.md - read it if you need a source or a fact that is not here)
FACT 1: Modern offloading methods become lossy, or need much higher PCIe budgets, on context-intensive tasks (Text2JSON). The authors blame landmark-based token selection, which is the same kind of scoring Quest uses | NEW from gate, check before relying on it
FACT 2: KVzip stays near-lossless at a 30% cache ratio on Qwen2.5-7B/14B, Llama-3.1-8B and Gemma3-12B (global layers only). It fails on one retrieval variant | NEW from gate, check before relying on it
FACT 3: ShadowKV achieves 6× larger batches and 3.04× throughput on A100, tested on 6 models. It keeps low-rank pre-RoPE K on the GPU and fetches only V | NEW from gate, check before relying on it
FACT 4: In the Mooncake trace, prefix-cache hit ratio rises from 34% to 55% as capacity grows from 1K to 50K blocks, with minimal gains beyond that | NEW from gate, check before relying on it
FACT 5: LMCache + vLLM reports up to 15× throughput on multi-round QA and document analysis | NEW from gate, check before relying on it
FACT 6: vLLM found that FP8 NIAH accuracy at 128K on Hopper fell from 91% to 13%. The cause was FP32 accumulation in the kernel, not the FP8 format, and a fix restores it to near BF16. vLLM also ships `--kv-cache-dtype-skip-layers` and recommends skipping sliding-window layers | NEW from gate, check before relying on it
FACT 8: Bandwidth is not the problem. Hiding the load needs 3.08 GB/s for BF16 and 1.54 GB/s for FP8 (128 or 64 KiB/token ÷ 42.6 µs/token computed for 20K prefill at 500 TFLOPs). PCIe4 x16 at about 25 GB/s gives a margin of about 8× | NEW from gate, check before relying on it
FACT 9: LMCache already does per-layer CUDA-stream pipelining, CPU, local-disk, remote and Redis tiers, and chunks larger than vLLM's 16-token pages, and reports up to 15× throughput on multi-round QA | NEW from gate, check before relying on it
FACT 11: Real hit rates depend heavily on the workload: 3.3% at a 16K-token cache, 18.5% at 4M, 34.2% at 16M, with a 37.4% ceiling on the Mooncake conversation trace. There is also an unverified blog claim of >90% for Kimi coding workloads | NEW from gate, check before relying on it
FACT 12: "Bit-identical" is not given for free. Cached and recomputed prefixes go through different batch shapes and kernels, so exact equality needs a batch-invariant kernel mode and would have to be checked on a real model. That check is not possible here because Hugging Face is blocked | NEW from gate, check before relying on it
FACT 13: Production traces show that reuse is skewed, that single-turn reuse matters as much as multi-turn, and that the cache size needed for an ideal hit ratio is moderate | NEW from gate, check before relying on it
FACT 14: Marconi's FLOP-aware eviction gives up to 34.4× hit rate, but only on hybrid SSM models and against modified vLLM+/SGLang+ baselines. On LMSys and ShareGPT the P95 win is 45.6% and 19.0% | NEW from gate, check before relying on it
Notes from the user (data; the user may be wrong):
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
NAME: Reversible eviction with offload
MECHANISM: Score tokens query-agnostically, in the style of KVzip, and keep about 30% on the GPU in FP8. Move the evicted blocks to CPU memory instead of deleting them. Each decode step, retrieve them page by page, as Quest does, whenever their score against the current query passes a threshold. The closest earlier attempt is permanent eviction, which fails in multi-turn chat (SCBench, FlowKV), whereas this keeps O(n) total memory. The deciding quantity is the recall rate of offloaded pages per step multiplied by the PCIe cost.
VALUE: It gives roughly 3× more concurrent users or context per GPU in multi-turn chat while staying close to FP8 accuracy, but it stalls when recall exceeds the PCIe budget.
KILL TEST: killer Share of the offloaded KV that can be fetched over PCIe each decode step without stalling. This applies when many users run long contexts at once, which is the "3× users" regime the idea claims. I took 30% resident and FP8 KV on Llama-3.1-8B (64 KB/token) | margin 0.29 | whole-chain ratio 1.21 | DEAD: In the multi-user regime it is pitched for, the step stalls on PCIe by about 3.5×, and in the single-request regime where the bandwidth fits, it saves only about 1.2×.

IDEA 2
NAME: Recompute-cost-per-byte store eviction
MECHANISM: Score each stored prefix by (expected reuses × FLOPs saved) ÷ bytes held. Long prefixes score higher because attention cost is superlinear, and expected reuses decay with time since last hit. Evict the lowest scores first, instead of LRU. The closest earlier attempt is CacheBlend, which raised effective hits through approximate non-prefix reuse; this design stays exact by raising the exact hit rate. The deciding quantity is the working set against tier capacity. It is falsified if, on a replayed RAG or chat trace, the hit-weighted FLOPs saved are not at least 15% above LRU at equal capacity.
VALUE: Raises the exact-reuse hit rate h, which sets the 1/(1−0.66h) gain, without changing any model output.
KILL TEST: killer hit-weighted FLOPs gained over LRU when the working set is compared with tier capacity (its own kill line is <15%) | margin 0.6 | whole-chain ratio 1.02 | DEAD: A better eviction policy only helps when capacity is short, and SSD tiers make capacity cheap, so the system-level gain is about 2–5% even if the 15% target is met.

