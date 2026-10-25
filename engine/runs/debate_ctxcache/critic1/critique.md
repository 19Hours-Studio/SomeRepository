# Critic 1 on round1 answer

Files here: replay2/costs/tiers reruns (*.rerun, byte-identical to round1), check.py/check.out,
replay2_fix.py (inplace new-token double count fixed), tiers_check.py/.out, trace_dup.rerun.

## Holds (re-run, identical)
- Idea 1 errata: 747,086 -> 479,425 units = -35.8% vs in-place (Anthropic), -31.7% OpenAI; -11.0% vs append_full;
  edit-frequency sweep -6/-20/-36/-60%; diff sweep 474k/479k/506k/539k. Doc order 6,003 vs 1,000 and 12,758 vs 500.
- Idea 2 section C: -24.5% / -25.8% vs append_full; k sweep. Idea 4 per-token costs ($0.0075, $0.371, $0.0163, $0.068),
  break-evens (2.5 min, 13 min, 6.8 h, 5.2 h, 339 h), tiers.out ratios 1.37/3.21/9.49x. KV sizes 320 KB/69 KB, 14 ms, 6.6 s.

## Unfair / unsupported (number changed)
1. Idea 2's headline compares against append_full, but the answer's own client recommendation is errata.
   Increment over errata at 195k->140k: punch -16.6%, patch -18.1% (not -24.5/-25.8%). Strongly retention-dependent:
   -7.5% at 100k target, -34.6% at 170k.
2. Sec B "cheapest retention = 40k" is a grid edge. Extending the grid, every policy moves to 60k/15k (still the edge),
   and there punch is +4.6% vs errata, patch -1.0%. "Cheapest" has no interior optimum here; cost just falls with retention.
3. Idea 4 ratios mix bases: HBM at rental, DRAM at hardware capex. Rental-vs-rental: 1.28x/2.24x/3.57x (5/30/120 s),
   not 1.37x/3.21x/9.49x. Reload time/HBM occupancy not charged. At 120 s the real alternative is discard+recompute
   ($1.11/session ~ HBM pin $1.02), so the baseline should be min(pin, discard, swap).
4. Idea 4 novelty: InferCept already picks preserve/discard/swap per interception from estimated duration;
   Continuum sets TTL from reload cost with CPU offload. "Choosing the tier per session from predicted gap" is prior art.
5. inplace bookkeeping bug: the edited segment's tokens are counted "new" twice. API bill unaffected; inplace hit_resent
   0.9342 -> 0.9281, its no-miss floor 507,502 -> 483,697. (Answer's printed floor 469,295 is the OpenAI one.)
6. Omitted case that cannot reach ~100%: cache TTL/eviction. Anthropic 5-min TTL: if 5% of turns idle >5 min,
   errata bill +39% (479k -> 666k); 20% -> +155%. OpenAI in-memory 5-10 min (24 h extended), forum reports of
   intermittent cached_tokens=0. The 100%-on-re-sent figure is a model assumption, not an API guarantee.
7. OpenAI w=1.0 may be stale: secondary sources say gpt-5.6 bills cache writes at 1.25x (unverified), making the
   OpenAI column equal to Anthropic's.
8. trace_dup 32%, n=1: on the three local trajectories it's 18.7% / 38.1% / 64.4% (toy demos, 5-11 steps). Still illustrative only.
9. "Asker assumed input dominates" - the question doesn't say so; minor strawman.

## Undersold
- Errata (479k) is within 1% of a perfect in-place cache's own floor (484k after fix): the client trick achieves the
  oracle cost of the edited prompt. That's a stronger, cleaner claim than "-35.8%".
- Mutable state near the top (memory/todo blocks): edits at segment 1 give -53.6% vs in-place (vs -35.8% uniform).

## Larger honest gain
- Bill after ~100% hits is reads ~ requests x live context. Fewer requests per unit of work (batching 2/4 independent
  tool calls per request, same tokens): -34.8% / -54.9% on top of errata. Quality/latency need testing; no provider change.
- Provider span ops pay off only at high retention (-35% vs errata at 170k), which is exactly the long-context regime.
- Hit-price on own stack is ~2% of recompute, not 10%: own-stack users already get much more than API pricing shows.
