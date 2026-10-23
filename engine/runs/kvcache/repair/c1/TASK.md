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
python3 (do every estimate in real code). Work only in `/home/user/SomeRepository/engine/runs/kvcache/repair/c1/`: read no other files in the repository, do not
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
FACT 4: In the Mooncake trace, prefix-cache hit ratio rises from 34% to 55% as capacity grows from 1K to 50K blocks, with minimal gains beyond that | NEW from gate, check before relying on it
FACT 5: LMCache + vLLM reports up to 15× throughput on multi-round QA and document analysis | NEW from gate, check before relying on it
FACT 6: vLLM found that FP8 NIAH accuracy at 128K on Hopper fell from 91% to 13%. The cause was FP32 accumulation in the kernel, not the FP8 format, and a fix restores it to near BF16. vLLM also ships `--kv-cache-dtype-skip-layers` and recommends skipping sliding-window layers | NEW from gate, check before relying on it
FACT 7: The FP8 RULER study on 10 models found near-lossless results on 8 dense GQA models. Degradation was major on DeepSeek-R1-Distill-Qwen-7B and meaningful on Gemma-3-1B-IT. No per-layer data was published | NEW from gate, check before relying on it
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
NAME: Exact-prefix tiered KV reuse
MECHANISM: Hash each KV block by its exact token prefix, as in vLLM prefix caching, and spill cold blocks to CPU or NVMe through LMCache in the model's native KV dtype. On a hit, the server streams blocks back over PCIe instead of recomputing prefill, so the outputs stay bit-identical. The closest earlier attempts are CacheBlend, which is approximate and limited to 3 models, and CacheGen, which only helps when loading beats recompute. This design avoids CacheBlend's problem because it accepts only exact prefixes. It avoids CacheGen's problem because local PCIe loads 2.6 GB in about 0.1 s against about 0.76 s of prefill (my estimate). The deciding quantity is the hit rate times the prefill saved, compared with the load time from the slowest tier used.
VALUE: In shared-prefix workloads it can cut cost up to about 2.4× with no change to outputs, but it fails on low hit rates, reordered RAG chunks and SSD-only tiers.
KILL TEST: killer Load time from the slowest tier compared with recomputing prefill, for 20K tokens on Llama-3.1-8B (2.62 GB KV in BF16, 425 TFLOP prefill) | margin 16.0 | whole-chain ratio 1.2 | WOUNDED: The physics has 2–16× headroom and outputs are exact, but this is already current practice (vLLM + LMCache). On real traces, the gain over GPU-only prefix caching is about 1.2×, not 2.4×.

IDEA 2
NAME: Probe-gated per-layer precision
MECHANISM: Run about 100 long prompts once with BF16 KV and once with FP8 KV, and measure per-layer attention-output error and final-logit KL divergence. Layers above a threshold stay in BF16; all others use stock FP8 kernels, so no custom datatypes are needed, unlike KVQuant. The deciding quantity is whether probe KL predicts the RULER loss.
VALUE: Turns "FP8 everywhere" into a model-checked default, with no weight changes. The hypothesis is falsified if the gated layers fail to restore RULER accuracy on Gemma-3-1B or R1-Distill.
KILL TEST: killer Whether the FP8 failure is confined to a few layers. Per-layer gating only pays off if the share f of layers kept in BF16 is small (f ≤ 0.5 for RATIO ≥ 1.1) and probe KL predicts the RULER loss | margin ? | whole-chain ratio 1.18 | WOUNDED: It is cheap and can be falsified with stock vLLM flags, but it only helps on the few models where FP8 fails, and then by at most about 1.2×. If the failures come from the kernel rather than from particular layers, gating reverts to all-BF16.

