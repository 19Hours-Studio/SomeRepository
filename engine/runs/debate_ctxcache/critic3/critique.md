# Critic 3: check of round-3 answer

All round-3 scripts were re-run on the same data (441 mini-SWE-agent trajectories + 1 Claude Opus 4.6 trajectory).
trace4.out, sim4.out, own4.out and ttl.out reproduce byte-for-byte. Our own checks: usage_check.py, check3.py,
rag_check.py, own_check.py and mask_check.py (each has a matching .out file).

## Numbers that hold
- 441 traj / 19,514 req; mean prompt 21.2k, new 759, output 373. Reasoning tokens are NOT double-counted:
  total_tokens = prompt + completion + reasoning (e.g. 1439+57+65=1561), so adding them is correct.
  Reasoning = 76% of output tokens, i.e. ~29% of the whole bill.
- Append-only base 95.2M units; caching saves 78.9%; split 41.9 / 19.9 / 38.2. Gaps max 112 s, none > 300 s.
- Claude trace: 99.38% hit on re-sent tokens, 94.77% token hit, $0.4036 = 80,728 x $5/M (n=1, 36 requests).
- Batching strict -5.7..-8.8%; lexical -19.0%; back-references -3.7%; combined -12.0%.
- Hand check of 20 random strict merges (check3.out §3): ~17/20 independent -> consistent with 77-90%.
- sim4 synthetic: errata -32.6% / -30.9%; span-op frontier; delegation; RAG figures; TTL 0.9% arithmetic.

## Unfair / unsupported (number, change)
1. Headline -12% uses unscaled batching (-8.7%). Precision-scaled (0.77-0.90): -10.4% .. -11.5%.
2. Back-references count any >=20-char line seen before (generic code lines, repeated tags). Runs >=3 lines: -3.2%;
   runs >=5 lines: -2.5% (vs -3.7%). Combined then about -9.5% .. -11%.
3. RAG "first-seen -36..-44% vs relevance": the gain comes from the baseline putting retrieved docs BEFORE the
   history (every doc change rebills the history), not from first-seen order. An information-matched baseline
   (this turn's docs at the tail, same 24.7k context) already gets -34.9% / -36.2%. First-seen adds only
   -13.3% (drift 0.1) / -0.3% (drift 0.3) over that, with 1.8-2.5x the context. With the recommended union cap
   (20 docs) it is 0.0% / +37% vs tail. The answer's own design is dominated: appending only *new* docs at the
   tail gives -69.8% / -60.6% vs relevance (-46% / -38% vs first-seen) at the same union context.
   The claim that relevance-ranked docs-before-history is "the real default" is unsupported.
4. Operator view omits decode weight reads. At batch 32 (+$5.28): total $22.64, not $17.37. Decode-KV share
   40.7% (not 53.1%), FP8 KV -20.4% (not -26.5%), swap -15.6% (not -20%). Swap reload is set to zero in the code; if it
   is not hidden, hit marginal cost is 3.7% (not 2.1%) of recompute. The direction holds.
5. "Robust span-op gain -8% to -17%": the -16.9% end is the deep-retention comparison the answer itself set aside.
   At errata's efficient point it is -8.4%, or -1.7% with +9% context. Synthetic, and 0 on the real traces.
6. Errata -32.6% and span ops are still synthetic. The real traces show this harness never mutates its context,
   so how common the "mutating regime" is remains unmeasured.

## Undersold
- Batching keeps 100% of the output of merged requests. One fewer reasoning pass per merged call is plausible
  (reasoning is 76% of output). Keeping 75% / 50% of it gives -11.3% / -13.9% (vs -8.7%).
- Selective 1h: Anthropic bills by prefix position (read up to the hit, 1h write for the rest). Entries are
  prefix-keyed, so the full prefix at the 1h breakpoint should survive. The predictor is trivial (end of the
  assistant turn = waiting for the human). Still needs the stated test.
- The answer is right not to recommend compaction on short sessions: cache-aware observation masking on the real
  traces costs +1.5% .. +19.1% (mask_check.out). Masking prior art (JetBrains 2025) does not transfer once cache reads
  are priced at 0.1x.

## Larger honest gain
- RAG / document workloads: append newly retrieved docs at the tail and never place docs ahead of the history
  (-35% information-matched, -60..-70% with a union). This beats Idea 1's first-seen design.
- Output/reasoning (38% of the bill, 29% of it reasoning): batching that removes reasoning passes, plus reasoning
  budgets, are the largest client levers left on append-only agents. Quality must be measured on a real model.
