The answer's numbers are reproducible, but several headline claims are larger than its own model supports. All of its scripts re-run byte-identical. The cost and size arithmetic (per-token costs, break-even intervals, KV sizes, 14 ms, 6.6 s) checks out by hand. My files, including the summary `critique.md`, are in `engine/runs/debate_ctxcache/critic1/`.

## 1. Decisive numbers that hold
- **Idea 1 (errata) against in-place editing:** 747,086 → 479,425 units, which is −35.8% at Anthropic prices and −31.7% at OpenAI prices. Against append-full it is −11.0%.
  - The edit-frequency sweep (−6% / −20% / −36% / −60%) and the diff-size sweep (474k / 479k / 506k / 539k) both reproduce.
- **Document order:** 6,003 vs 1,000 tokens rewritten per request, and 12,758 vs 500.
- **Idea 2, matched retention (195k → 140k):** −24.5% (`delete_span`) and −25.8% (`replace_span`) against append-full.
- **Idea 4:** the break-even intervals and the 1.37x / 3.21x / 9.49x ratios are what `tiers.py` actually outputs.

## 2. Unfair or unsupported points
1. **Idea 2 uses the wrong baseline.** Its headline is measured against append-full, but the answer's own client recommendation is errata. Against errata, the gain is −16.6% (`delete_span`) and −18.1% (`replace_span`), not −24.5% / −25.8%. It also depends heavily on how much history is kept: −7.5% at a 100k target and −34.6% at 170k.
2. **"Cheapest retention = 40k" is just the bottom of the grid it tried.** With a deeper grid, every policy moves to 60k/15k, which is again the grid edge. There, `delete_span` is +4.6% against errata and `replace_span` is −1.0%. Cost keeps falling as less history is kept, so there is no real optimum, and the "−4.5% to −7%" figure is an artifact.
3. **Idea 4 mixes pricing bases.** HBM is priced at rental cost and DRAM at hardware cost. Pricing both at rental gives 1.28x / 2.24x / 3.57x for 5 / 30 / 120 s gaps, not 1.37x / 3.21x / 9.49x. Reload time and the HBM it occupies are not charged.
   - At 120 s, discarding and recomputing costs $1.11 per session, about the same as pinning in HBM ($1.02). The fair baseline is the cheapest of pin, discard and swap.
4. **Idea 4's novelty claim fails.** [InferCept](https://arxiv.org/pdf/2402.01869) already chooses preserve, discard or swap per tool call. [Continuum](https://arxiv.org/html/2511.02230v2) sets the HBM pinning time from the reload cost when CPU offload is on. "Choosing the tier per session from the predicted gap" is prior art.
5. **Bookkeeping bug in the in-place baseline.** The edited segment's tokens are counted as new twice.
   - The billed amount is unaffected.
   - The in-place hit rate on re-sent tokens drops from 0.9342 to 0.9281.
   - The Anthropic best-case cost for the in-place prompt drops from 507,502 to 483,697. The 469,295 printed by the script is the OpenAI figure.
6. **A case that cannot reach ~100% is missing: cache expiry.** Anthropic's cache lasts 5 minutes. If 5% of turns sit idle longer than that, the errata bill rises 39% (479k → 666k); at 20% it rises 155%. OpenAI's in-memory cache lasts 5–10 minutes, or up to 24 h with [extended retention](https://developers.openai.com/api/docs/guides/prompt-caching). There are [forum reports](https://community.openai.com/t/prompt-caching-returns-cached-tokens-0-intermittently-same-static-prefix-same-prompt-cache-key/1386029/2) of hits failing intermittently on identical prefixes. The "100% hit on re-sent tokens" is an assumption of the model, not something the API guarantees.
7. **The OpenAI write price may be out of date.** Secondary sources ([Azure docs](https://learn.microsoft.com/en-my/Azure/foundry/openai/how-to/prompt-caching)) say cache writes on gpt-5.6 cost 1.25x, the same as Anthropic. I could not confirm this from OpenAI directly.
8. **The 32% duplicate-observation figure (n=1) is not robust.** On the three trajectories available locally (5–11 steps each) it is 18.7%, 38.1% and 64.4%.
9. **Minor strawman:** the question never says the asker assumes input dominates cost.

## Where the answer undersells itself
- **Errata reach the ideal in-place cost.** At 479k, errata are within 1% of the cost of the in-place prompt with a perfect cache (484k after the bug fix). That is a stronger and cleaner claim than "−35.8%".
- **Mutable state near the top of the prompt** (memory or todo blocks right after the system prompt) gives −53.6% against in-place, not −35.8%.

## 3. Where a larger honest gain is most likely
- **Fewer requests per unit of work.** Once nearly every re-sent token is a hit, the bill is mostly (number of requests) × (live context) × read price. Batching 2 or 4 independent tool calls per request, with the same tokens, cuts the errata bill by a further −34.8% / −54.9%. It works client-only on any API. The quality and latency effects are untested.
- **Span operations in long-history sessions.** They pay off only when a lot of history is kept (−35% against errata at 170k retention), which is exactly the long-context agent case.
- **Own serving stack.** There a hit really costs about 2% of a recompute, not the 10% read price the APIs charge.

All of this is still synthetic replays, and output quality is untested on any real model.

HONEST GAIN: −35.8% billed input vs in-place editing (Anthropic, synthetic replay, edit every 5 turns; only −11% vs append-full; provider span ops add −16.6% over errata at 140k retention), ~100% hit on re-sent tokens assuming no cache expiry; quality untested