A is the better answer, by a clear margin. It reproduces exactly and is backed by 200 real agent traces. B's one measured result comes from a replay with a billing bug.

**A**
- I re-ran `rule.py` and `traces.py` on A's 200 SWE-agent traces. The data checksum matches and both outputs are identical to the files A ships.
- Against sliding-window clearing of old tool outputs (keep the last 5), the price-timed batch-clearing rule cuts billed input by 45.4%, or 47.1% with a fixed 5k-token batch. Against keeping everything (append-only) it is 23.7–26% cheaper.
- The superset check holds: 0 violations in 24,442 requests, so the model never sees less than under sliding clearing.
- The server-side splice saves 58% against sliding. A labels it not exact, credits the prior art (Leyline, llama.cpp), and drops B's "12.5x" claim, which was only the price ratio 1.25/0.1.
- A is honest about limits. Hit rate tops out around 97% for any growing session, and diff-style corrections (errata) save only 0.2% on real traces.
- Small flaws:
  - The two scripts give slightly different hit rates (0.971 vs 0.966 append-only, 0.725 vs 0.707 sliding).
  - The baseline it beats by 45% is the weakest common practice. Anthropic's `clear_at_least` setting already covers part of the idea.
  - No quality test was run on a live model.

**B**
- The replay behind its headline (−40% cost, 99.75% hit rate) is in `calc.py`. It counts each new tool output as already cached on the next turn, so new content is never billed as a cache write.
- Its compaction rule never fires: the "erratum+ski" run gives exactly the same result as "erratum".
- I re-ran it with corrected billing (`bfix.py` in the scratchpad). The saving drops to about 30% and the hit rate to 96.3%, not 99.75%.
- The scenario is synthetic. A's real traces show that changed tool outputs rarely occur in place, so the idea is worth about 0.2% there.
- Sorting documents by content hash means adding one document invalidates about half the cache.
- The "12.5x cheaper suffix" is just the price ratio.
- Its server-side ideas (segment caching like CacheBlend/EPIC, storage tiers) are reasonable, but they are the same ideas A covers, with weaker numbers.

The corrected replay script is at `/tmp/claude-0/-home-user-SomeRepository-engine-runs-climb-ctxcache-round1-judge-fix-swap/86b61a25-826d-5e99-8ce4-43b0688ac74a/scratchpad/bfix.py`.

WINNER: A
MARGIN: clearly
WHY: I re-ran A's replay of 200 real SWE-agent traces and it reproduced exactly: 45–47% less billed input than sliding-window clearing, 24–26% less than append-only, and 0 cases where the model sees less context. B's only measurement is a synthetic replay that bills new content as cached and whose compaction rule never fires. Fixed, its 40% / 99.75% becomes about 30% / 96%, and A's real traces show the idea is worth about 0.2% in practice. B also inflates "12.5x" from the price ratio and proposes hash ordering, which invalidates about half the cache when one document is added.
REAL GAIN A: About 45% less billed input than sliding-window tool-output clearing (about 24% less than append-only, but with less context), measured on real traces. The hit rate rises from 72% to 90–92%. Output quality is untested.
REAL GAIN B: Only modest. Errata save about 30% on B's own synthetic workload once the billing is fixed, but almost nothing (0.2%) on A's real agent traces. The server-side ideas repeat prior art and come with no measurements.