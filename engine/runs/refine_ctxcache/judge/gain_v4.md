# Review of the answer: what it gains over current best practice

I checked the answer's arithmetic by hand. I did not run `calc.py` or `cachediff.py`, so the simulated numbers (0.43×, 98.0%, the §D replay) are taken as reported. All of them come from synthetic layouts or a 3-trajectory replay. No quality claim was tested on a model, as the answer itself says.

## Arithmetic that checks out

- **Bill split (§A):** reads 59%, writes 28%, output 13%. Recomputed as about 332k + 156k + 75k token-units.
- **TTL (§G):** 1.25·(N+1) versus 2 + 0.1N, giving 7.5 versus 2.5 at N=5.
- **Warm-up (§K):** 12.5 / (1.25 + 9·0.1) = 5.8×, and 10.2× at N=50.
- **Batch break-even (§L):** about 81%, and 0.55–0.56× at 98% in-batch hits.
- **Ski-rental thresholds:** 1,138 and 45 turns.
- **Idea 3 savings:** 2.40× and 1.60×. These follow from 34% and 60% exact document hits versus a covered cost of about 0.25 at 96% coverage, plus 1% shadow traffic.
- **"Only layer-0 K/V is exactly reusable":** correct.

## Corrections to the answer's own comparisons

1. **The headline baselines are naive setups, not best practice.**
   - 47.1% → 98.0% starts from "authoring order". Stable-first, append-only layout with volatile content last is already standard advice (Manus, Anthropic, *Don't Break the Cache*). That layout already gives 93.7–95.3%.
   - 5.8× (warm-up), 2–3× (TTL) and about 0.56× (batch plus caching) compare against users who ignore Anthropic's own documentation. These are prior art, so they add no gain over best practice.

2. **0.43× is measured against "never clear".** Context editing with `clear_at_least` already exists.
   - In the answer's own table the optimum is flat: periods of 5, 8 and 10 turns all give 0.43×. The square-root rule therefore matters only against a poorly chosen period.
   - The realistic baseline is Anthropic's default trigger at 100k input tokens. In this simulation that clears roughly every 30–40 turns, which the table puts at about 0.51×.
   - The 0.43× also assumes the cache survives up to the clear point. The answer's own Anthropic-realistic figure is 0.49×. Against a default of about 0.5×, that is close to no gain.
   - Most of the saving comes from deleting content, and the effect on task success is untested.

3. **The odds/size ordering rule improves on p/s by a median of 1% (at most 17%).** Practitioners don't use p/s anyway, so the real gain is about 1×.

4. **The diff-only tail (95.3% → 98.0%) is the one layout increment that is not prior art.**
   - Unchanged tail tokens are re-sent for about 450 tokens per turn instead of about 2.5k. That cuts input cost per turn by roughly 1.2× in the synthetic layout.
   - The cost is that the model has to rebuild its state from accumulated diffs, and the effect on quality is untested.

5. **The splice (Idea 2) is about 1.2–1.3× cheaper on input than the best client-side policy** (1.00 → 0.82 at 30 steps, 0.77 → 0.62 at 80 steps).
   - This comes from 3 trajectories with chars/4 token counts.
   - It needs your own serving stack and is approximate, with no deviation measured.
   - The mechanism is prior art (llama.cpp context shift, Leyline, PatchKV).

6. **Idea 3 is not ahead of CacheBlend, EPIC or AgentKVShift on cost.**
   - Its 1.6–2.4× is measured against exact prefix reuse, at a 0% fallback rate.
   - Measured against those methods, the gate *adds* cost (shadow runs plus fallback) in exchange for a quality guarantee that has not been measured.
   - Storage and retention for about 1M segment tokens are left out of the saving, which is exactly the cost Idea 4 says should be counted.

7. **Unsupported sentence:** "the ~1.2× gain from tiered caching that your earlier run measured" cites a run that appears nowhere in the answer.

8. **What the hit rate means:** the near-100% figure for middle edits, insertions and changed tool outputs comes from turning them into appended errata. It removes those cases rather than serving them. The answer does admit that exact reuse after an in-place change is impossible.

## Net assessment

**What is real:**
- Small client-side gains on top of best practice: the diff-only tail, and a clearing period tuned against the default trigger. Each is about 1.15–1.2× in simulation.
- For self-hosters, about 1.2× on input cost from splicing.

All of these come with untested quality costs. The rest of the answer is prior art presented clearly, with useful break-even numbers (81% batch break-even, T*, the 20-block lookback trap) and a diagnostic tool. None of it is a large gain over current practice. Under the answer's own analysis, the "much cheaper at near-100% hits" goal is capped by the read-dominated floor.

HONEST GAIN: ~1.15–1.2x lower total/input bill in simulation (tuned clearing vs. default trigger; diff-only tail; server splice), quality untested — none vs. prior art for the headline 0.43×, 5.8× and 98% figures