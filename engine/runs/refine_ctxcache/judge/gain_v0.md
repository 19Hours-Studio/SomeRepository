The answer supports **no measurable gain over best current practice**. Its one measured number, −40%, compares against a baseline that best practice already avoids, and the replay favours its own method. The arithmetic itself checks out. I reran `runs/vs_ctxcache/baseline/calc.py` and got the same T* values (1,238 and 50 turns), the same replay totals (604,200 vs 364,632 units, 92.86% vs 99.75% hit rate), and the same storage and recompute figures ($0.175, $8.19, $1.64 and $0.066 per 1M tokens per hour, and 6.6 s PCIe per 1M tokens).

**Idea 1: the replay is unfair, and the baseline is not best practice**
- The "edit" arm rewrites a full 2k-token tool output in place. The "errata" arm appends only `ERR=60` tokens, described as a "pointer + short summary". So the erratum never carries the new tool output. This contradicts the text, which uses e = 500 to 2k. With a fair erratum of 2,000 tokens, billed input is 384,032 vs 604,200, so the saving is −36%, not −40%. The hit rate stays at 99.73%.
- More importantly, rewriting the middle in place is not the best current practice. The answer cites Manus's append-only context, which is that practice, and the errata arm is exactly that practice. The only addition is the ski-rental compaction rule. By the answer's own T* numbers, that rule almost never fires on cost; the context-window limit triggers compaction first. So it changes nothing in the replay. Gain over best practice: about 0.
- Sorting documents by content hash and using sorted JSON keys is also standard practice.

**Idea 2: the 12.5x figure is a billing ratio, not a measured gain**
- The 12.5x comes from 1.25 / 0.1. That is a price the provider would choose to charge, not a saving shown on any workload.
- The output is not exact: tokens after the hole still carry what they absorbed from the deleted span. Quality, measured as KL divergence or top-1 agreement against full recomputation, was not tested.
- The mechanism is prior art: llama.cpp context shift and KV-eviction methods.

**Idea 3: the method is CacheBlend and EPIC themselves**
- The 3–7x figure and the 85–94% reuse are those papers' own results, which makes them the best current practice for this case.
- The proposed deviation gate is close to CacheBlend's existing selection signal. No result is given for it.
- The quality gaps the answer cites (Fusion-RAG, AgentKVShift) remain.

**Idea 4: correct break-evens, but nothing measured**
- The break-even arithmetic is correct. DRAM pays off at about one reuse every 6.4 minutes, NVMe at about one reuse every 2.7 hours. The recompute cost counts only linear FLOPs and leaves out attention, so it understates recompute at long contexts.
- Cost-based eviction across tiers already exists in tiered KV caches (Mooncake, LMCache, AttentionStore and others).
- The answer itself puts tiering at about 1.2x over GPU-only caching and measures no added gain from per-prefix ski-rental eviction.

**What holds up**
- The answer correctly says that exact reuse after a mid-prompt change is possible only by appending, and that every non-prefix reuse method is approximate and untested here.
- None of the quality claims were run on a real model.

HONEST GAIN: none