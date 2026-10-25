# Gain check of answer.md

Reproduced: every number in baseline/calc.py reruns exactly (92.9% -> 99.75% hit; 604k -> 365k units; KV sizes; $/M-token figures).

## Idea 1 (append-only errata + ski-rental compaction)
- The -40% compares append-only against *in-place editing*. In-place editing is the known anti-pattern, not best practice. Manus's guidance
  ("make context append-only", stable prefix, deterministic serialization) and normal agent loops (a re-read file is a new tool result
  at the end) already do this. Against that baseline the only new part is the ski-rental compaction rule.
- replay_check.py: the ski-rental rule fires 0 times in every realistic setting (50 or 200 turns, edits every 2 or 5 turns, errata of 1k or 2.3k tokens),
  so "erratum+ski" == "erratum". It fires only with an edit every turn for 200 turns, and then cost goes *up* (9,885,645 vs 9,880,355).
- Over 200 seeds the headline saving ranges from 24% to 56% (mean 43%), but all of it comes from the strawman baseline.
- Sorting by content hash makes only a *pure* reorder of an identical set exact. An inserted document lands at a random position
  (on average about half the document block is recomputed), and dropping relevance order is an untested quality risk.
- Quality (stale text next to its correction): not tested.

## Idea 2 (hole-punch deletes)
- The mechanism is llama.cpp's KV seq_rm/seq_add context shift plus StreamingLLM-style position handling. The answer itself cites these as prior art.
- "12.5x cheaper" is just Anthropic's price ratio 1.25/0.10, not a measured compute or quality result. Output is not equal to full recompute, and its quality is unmeasured.

## Idea 3 (segment cache + boundary recompute)
- This is CacheBlend / EPIC / LMCache, with the papers' own numbers. AgentKVShift (NeurIPS'26: 10-30% refresh, near full-recompute quality)
  is newer, comparable or better prior art. The "deviation gate" is CacheBlend's own signal and is untested.
- "3-7x prefill compute" is 1/recompute-fraction. The measured TTFT gain is 2.2-3.3x (CacheBlend), and that belongs to prior art.

## Idea 4 (storage-priced retention)
- The arithmetic checks out ($0.175/M recompute; $8.19 / $1.64 / $0.07 per M tok-h). But it ignores attention FLOPs at long context
  (about 2x more recompute at 100k), and NVMe bandwidth (about 7 GB/s, not PCIe 50 GB/s) means about 4.7 s to load a 100k-token 70B context.
- Prior art: Gemini explicit caching already prices storage per token-hour (~$4.50/M/h for Pro), and AttentionStore, Mooncake and LMCache already do tiered,
  cost-aware retention. Nothing is measured.

## Bottom line
Nothing beyond current best practice is demonstrated. The one measured number (-40%) is a gain over a baseline that best practice already avoids.
The novel part (the ski-rental rule) shows 0% gain in the answer's own replay.
