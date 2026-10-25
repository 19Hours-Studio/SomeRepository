The answer supports a modest gain: about **1.25–1.3× lower input cost** on agent traces, compared with batched tool-result clearing. That gain needs an approximate server-side splice that no API offers today. On a plain API, the only gain over current practice is a small layout refinement, and its quality effect is untested.

**Reproducibility.** `calc.py` and `traces/` are not in `/home/user/SomeRepository/engine`. The directory is empty, so none of the §C–§G numbers can be rerun. I rebuilt §0 independently:
- The bill split comes out as reads 59%, writes 27%, output 14%. The answer says 61/25/14, so this roughly matches.
- Keeping the last 10 turns gives an input ratio of about 0.53×. The answer says 0.62×. The direction is right.

**Baselines that need correcting**

1. **The 0.62× / 0.82× splice figures are compared with append-only or every-step elision.** The 1.79× every-step elision is a straw man. Batched clearing is already shipped practice: SWE-agent `polling`, and Anthropic context editing with `clear_at_least`. The answer cites both. The fair baseline is its own "polling = 15" row:
   - 30 steps: 1.05× → 0.82×, which is **1.28×**.
   - 80 steps: 0.77× → 0.62×, which is **1.24×**.

   This gain has several caveats:
   - It assumes splice tokens are billed as cached reads. That is a pricing assumption, not a property of the method.
   - It needs your own serving stack or a provider that offers splicing.
   - The splice is approximate, and its quality is unmeasured.
   - The polling value was not tuned. A better batching schedule, such as its own ski-rental rule, would shrink the gap.
   - The data is 3 small trajectories (median observation 65 tokens) resampled into synthetic sessions.

2. **The layout table (47% → 98%) starts from authoring order.** Current practice is stable content first, append-only, and a volatile tail (Manus, Anthropic docs). That practice already gives about 93.7–95.3% in the answer's own model.
   - The diff-only tail is the only incremental step, from 95.3% to 98.0%. In input-cost units (0.1·hit + 1.25·miss) that is 0.154 → 0.123, or about 1.25×.
   - The model is synthetic and the quality cost is untested. Not re-sending the tail gives up the deliberate end-of-context recitation that Manus uses.
   - The odds/size ordering rule improves on Smith's rule by a median of 1%, which is negligible.

3. **Idea 3's 1.7–2.5× is CacheBlend/EPIC-style segment reuse.** That is prior art, so it is not a gain over best current practice for a self-hoster. The shadow gate is new, but it adds about 1% compute and offers no measured benefit.

4. **Ideas 4, TTL choice and key sharding are documented provider features or existing tiered-cache work** (LMCache, Mooncake and similar). The 7.5× → 2.5× TTL figure is correct arithmetic on Anthropic's published prices, but it is not a new gain. The "GPT-5.6 write 1.25×" claim is unsourced.

**Parts the answer gets right**
- It states honestly that exact reuse after an in-place middle edit is impossible. Only layer-0 K/V can be reused, so at most about 1/L of the suffix work is saved.
- It is right that at about 100% hits, cost is dominated by reads and writes, not misses.
- It correctly says every approximate method leaves a multi-hop quality gap.

None of the approximate methods has a quality measurement. So the splice gain is a conditional cost estimate, not a demonstrated improvement.

HONEST GAIN: ~1.25x lower input cost vs batched tool-result clearing on small resampled SWE-agent traces, only with an unvalidated approximate server-side KV splice billed as cached reads; ~none for exact client-only methods beyond existing append-only/volatile-tail practice