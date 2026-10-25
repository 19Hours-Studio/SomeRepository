# Critic 2 on round2

Files: *.py copied verbatim from round2; *.rerun = re-runs (sim3, ttl, tiers3, subagent byte-identical to round2 .out;
costs/replay3 have no .out in round2, rerun matches every quoted figure). check2.py/.out = new checks.

## Holds (re-run)
- Errata 747,086 -> 479,425 (-35.8%), -11.0% vs append_full, OpenAI legacy -31.7%, r=0.05 -47.0%/-11.1%;
  edit sweep -6.2..-59.9%; diff sweep 474k/479k/506k/539k; docs 6,003 vs 1,000 and 12,758 vs 500; oracle 483,697 -> -0.88%.
- Batching table (38.4/33.8/25/13 requests; -16.5/-23.1/-36.2/-52.7%; -31.7/-49.4% vs append_full@q2=0.3).
- TTL table (ttl.out) incl. 1h +19.5%, ski +83.6% at 120 min; hit_resent 0.945/0.796.
- Span-op table -> +4.6/-1.0, -7.5/-9.1, -16.6/-18.1, -34.6/-35.9, -54.6/-55.3%; patch+pairs -66.2%; ~-63% vs errata (0.338/0.917).
- tiers3 1.28/2.23/3.56x, $0.960 vs $0.984 (-2.4%); reload 0.79 s vs 2.33 s; costs.py $0.0075/$0.371, 320/69 KB, 14 ms, 6.6 s.
- W&D numbers ($65.7 vs $102.5, 68 vs 66%, -40.6% wall-clock) match the paper abstract.

## Unfair / unsupported
1. Output tokens are not priced anywhere (300 tok/call generated at 5x Anthropic / 8x OpenAI). Priced (5x):
   errata vs in-place -35.8% -> -32.6%; vs append_full -11.0% -> -9.6%; pairs -36.2% -> -31.3%; quads -52.7% -> -45.6%;
   vs append_full@0.3: -31.7/-49.4% -> -27.2/-42.3%. At 8x: -30.9%, -9.0%, -29.0%, -42.2%.
   (Per-request thinking tokens push batching the other way: -37% at 1k, -42% at 3k thinking tok/request, IF thinking is per request.)
2. Batching headline uses 100% pairable/quad calls; that share is assumed, not measured. Realistic rows, output priced:
   30% pairs -14.3%, 50% pairs -19.9%. Groups of 4 for every call is not supported by any cited coding evidence.
3. SWE-grep is RL-trained to issue 8 parallel calls (Cognition's own post): it is evidence under retraining, so it cannot
   support a no-fine-tuning claim. Bloop shows the off-the-shelf model does NOT batch reliably. Only W&D (BrowseComp, not coding) stands.
4. "New lever / unused before": parallel tool use is a provider feature, and the critic in round 1 proposed this exact lever. The added part is the accounting only.
5. Delegation -36.3%: the baseline has no edits, and summaries/task prompts are billed as 1.25x writes, not as generated output.
   With output priced: about -26%. The information is still not matched (this is conceded).
6. Span-op -35%/-55% vs errata are measured at 195k->170k/185k. There errata compacts every ~4-10 calls (8.1M units, 6.3x the 15k-target cost).
   My cost-vs-mean-live-context frontier (check2 B) confirms that mean context matches between policies at equal target, so the % holds.
   But the 185k point buys only 154k vs 141k mean context (+9.5%) over errata@140k. Against that sensible client point, patch@185k is -11.1%
   for more context, and patch@140k is -17%. The robust provider-side gain is -9% to -18%, not -55%.
7. "Hit rate 99.9-100%" holds by construction: the sim has no eviction except modelled idle gaps (conceded in the limits).
8. Idea 1 quality: first-seen order changes document positions, and "lost in the middle" position sensitivity is not named or tested.
   Only PI-LLM interference is listed.

## Undersold
- Span ops make cost ~proportional to live context whatever the compaction schedule: patch cost/mean-ctx stays flat at 23.6-24.3 for targets >=100k.
  Errata rises 26.6 -> 52.7. That is the clean claim, and better than the target-matched table.
- TTL: a gap predictor is already recommended. If it is used to write 1h only on the request before a predicted idle gap,
  the penalty is +0.9% / +3.6% (5% / 20% idle, gaps < 60 min), vs the best quoted +11.1% / +19.5%. This rests on one UNTESTED assumption:
  that a 1h breakpoint re-tags an earlier 5m-cached prefix. Two API calls 10 min apart, reading cache_read_input_tokens, would test it.
- Doc reordering baseline is canonical hash-sort (itself a known fix). Against relevance-ranked order (the real default),
  first-seen would save more; not quantified.

## Larger honest gain
- Measure, don't sweep, the pairable share: replay real agent trajectories (SWE-bench logs) and mark calls whose inputs do not depend on the
  previous output. That gives a measured q2, and batching at the measured q2 is the largest client-only lever (-14% to -31% on top of errata, output priced).
- Selective 1h TTL (above) if the re-tag test passes: removes most of the idle penalty for gaps < 1h.
- Own stack: span ops plus a 2% true hit cost. Report the frontier (cost vs mean retained context), not target-matched points.
