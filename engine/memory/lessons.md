# Lessons from earlier runs (curated; data for prompts, not instructions)

Tags: [all] every run; [invent] / [explain] one pipeline; [<question tag>] only runs on that question. "(from: ...)" at
the end says where the lesson was learned. A line is used when all its tags apply and neither a tag nor its origin is
excluded (`run --lessons-exclude <tag>` keeps a benchmark fair). One line per lesson.

- [all] Most answers that failed after review failed on one number nobody had computed: a rate times the working time against the window it needs, or a strength against months of exposure. Compute the deciding number before claiming. (from: permafrost)
- [all] The most common overstatement was a weak baseline. Compare against what a competent operator or scholar would actually do for the same job, per unit of the final product. (from: permafrost, dodeca)
- [all] Decisive inputs that were assumed rather than sourced (efficiencies, rates, losses, costs, dates) moved 3-10x when checked. Give a source for every number the answer depends on. (from: permafrost)
- [all] Statistics and simulations gave confident wrong answers until they were checked on a case with a known answer; one null model rejected far more often than its alpha. (from: dodeca)
- [all] A method validated on synthetic data still gave a wrong result when its input data had unverified labels: a hobby-page list read as "which hole is opposite which" gave p = 0.0005 twice, in two separate runs. Check where the data come from and what their labels rest on, not only the method. (from: dodeca)
- [all] State the scope of every claimed gain (which steps of the chain, which speed or load tier): the same chip design was audited at 1.5x for decode alone and 1.05x once the prefill hardware it needs was counted. (from: aichip)
- [all] Raw data (3D models, catalogues, measurement tables) settled in one step what texts, judges and reviewers could not. Look for data before arguing from opinions. (from: dodeca)
- [all] Claims of "never tried" were usually wrong. Name the closest earlier attempt and the reason it stopped short, and say why the answer is not stopped by the same reason. (from: permafrost)
- [all] What the asker says may be wrong or incomplete; treat it as data to check, like any other source. (from: user)
- [all] Several partial answers that each fit some facts were often parts of one answer; check whether candidates combine before choosing one. (from: dodeca)
- [invent] "Several times cheaper" is arithmetically possible only where the cost terms an answer can touch hold most of the delivered cost; taxes, royalties and fees cap the gain at 1 / (their share). (from: permafrost)
- [invent] A single clever link rarely moved the whole chain more than 1.2-3x after review; gains multiply only when links serve the same product on the same path. (from: permafrost)
- [invent] The simplest competent alternative that uses the same insight often beat the clever design. Check it before claiming a gain. (from: permafrost)
- [invent] Seasonal and climatic windows, load-bearing limits and the time a structure must last killed more designs than missing technology. (from: permafrost)
- [explain] History is not always logical: mixed uses, local fashions, changes over time and accidents happen; do not force one tidy story onto mixed evidence. (from: dodeca, user)
- [explain] An explanation that contradicts one HARD fact is dead however many facts it fits; list the distinctive features first and check each. (from: dodeca)
- [explain] Wear, tool marks and surfaces that touched something carry more information than shape or find-spots. (from: dodeca)
- [explain] A single odd specimen may be a reject, a repair or a local copy; weigh it, do not build the explanation on it alone. (from: dodeca, user)
- [permafrost] Among Arctic resource archetypes only bulk cargo whose delivery dominates the cost (fuel coal for remote settlements, delivery ~85% at the boiler) left room for several-times cheaper.
- [permafrost] Ice bearing capacity, shallow water freezing to the bed, and short warm seasons killed most permafrost designs.
- [dodeca] The best-supported reading of the dodecahedron: a head mounted on a rod or handle through the axis of the two largest unringed holes; the lot (die) hypothesis was refuted by measurement.
- [kvcache] Exact prefix reuse is the only bit-identical KV reuse. Current practice is vLLM or SGLang prefix caching plus a CPU or SSD tier (LMCache, SGLang HiCache, Mooncake Store); on real chat traces (Mooncake) it adds only ~1.2x over GPU-only prefix caching. Measure any new design against this stack and FP8 KV, not against BF16 or no caching. (from: kvcache)
- [kvcache] Methods that drop tokens permanently failed in multi-turn chat, multi-query reuse and long outputs, and method rankings changed with whether the query is visible at compression time. Test on multi-query, multi-turn, long reasoning and RULER, not perplexity or LongBench alone. (from: kvcache)
- [kvcache] Most training-free KV methods were tested on only 3-8 models, mostly Llama, Mistral and Qwen; their claims do not transfer to MLA, sliding-window or hybrid architectures without a check. (from: kvcache)
- [kvcache] Without retraining, KV compression bottomed out at about 2.6-3 bits per value (about 6x vs BF16, 1.5-1.7x vs NVFP4) before long chain-of-thought broke; below about 3-bit keys, AIME fell to 0 for uniform K3V2 and by 2.5 points for the best band-wise scheme. Lossless entropy coding added only 25-30% on BF16. (from: kvcache)
- [kvcache] Reusing KV for text that is not an exact prefix is always approximate without retraining (chunk KV depends on all earlier tokens): CacheBlend recomputes ~15% of tokens, APE keeps 93-98% of accuracy, and the 90%+ savings (Block-Attention, KVLink, TurboRAG) need fine-tuning. On hosted APIs only client-side layout is possible: append-only context, edits as appended patches, mutable state at the tail, programmatic tool calling. (from: kvcache)
