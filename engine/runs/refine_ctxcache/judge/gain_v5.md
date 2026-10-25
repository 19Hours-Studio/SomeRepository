# Review: what gain the answer actually supports

## Verdict

The answer does not reach the asker's goal, and it says so. It finds that real agent traffic already has about 97% hits, and none of its methods raise that. Periodic clearing actually lowers the hit rate to 91.6%. What it really offers is a modest cut in the bill from **sending fewer tokens**. It does not make non-identical prefixes hit the cache.

I did not re-run `calc.py`, and I did not check that the S3 trace extraction is correct. The numbers below are the answer's own, adjusted only where its comparison is unfair.

## Where its own comparison is unfair or unsupported

1. **The 0.79× headline is not a like-for-like comparison.**
   - "Keep 3, every 9 steps" removes context that the baseline keeps. The answer itself says keep 3 is below any published window and its quality is untested.
   - A bill reduction that removes context and has no quality evidence is not a gain over best practice. It is a different product.
   - The only setting with even indirect quality support is **keep 10, every 18 steps, at 0.90×**. That support is an inference: it shows a superset of what the Complexity Trap's rolling window M=10 shows. Even M=10 is unconfirmed in the paper.

2. **"Rolling masking doubles the bill (2.01×)" is a comparison against a strawman.**
   - Nobody who runs under prompt caching and has read the docs re-clears every step.
   - Anthropic's context editing exposes `clear_at_least` precisely so that clearing is batched and cache invalidation is amortized.
   - Batched clearing is documented, intended practice, plus routine compaction in agent harnesses. It is not a new finding.
   - Two points are still useful and legitimately new: the EOQ choice of period, and the breakpoint placement for the client-side form.
   - The "30k trigger, 0.999×" row appears to leave out `clear_at_least`, so it undersells what the existing feature can do. The answer admits it did not verify the semantics.

3. **The replay is counterfactual.**
   - It reuses trajectories recorded with full context.
   - Under masking, the agent would take different, possibly longer, paths. That changes both cost and resolve rate.
   - So 0.90× is an offline estimate, not a measured bill.

4. **Measurement noise of a few percent.**
   - Token counts use chars/4. Code is closer to ~3.5 chars per token.
   - The tool schemas are assumed at 1,500 tokens.
   - The 0.90× and 0.79× figures each carry several percent of uncertainty.
   - The "EOQ predicts 9, replay finds 9" check is fitted on the same data, so it is a sanity check, not a validation.

5. **The self-hosting numbers are a roofline model with assumed hardware figures.**
   - The exact option, 0.84× GPU time, has no measurements behind it.
   - The splice, 4-bit KV and segment-cache figures (0.70×, 0.60×, ~96% coverage) depend on quality gates that were never run.
   - The segment-cache ideas themselves are prior art: CacheBlend, EPIC, APE and AgentKVShift.
   - The added gate and two-price scheme are reasonable engineering, but they are unvalidated.

6. **The API levers in §0 are documented practice, not gains.** These are the 1-hour TTL, warm-up before fan-out, stacking batch with caching, and routing.

## What survives

For agents shaped like SWE-agent on an Anthropic-style API, relative to append-only best practice at 97% hits, the answer supports one result with three qualifiers:

- **The result:** batched clearing tuned by the EOQ period, keeping about 10 recent observations, gives roughly **0.90× the total bill**. The KV is exact for the prompt actually sent.
- **The quality is plausible but untested.**
- **The figure comes from replay, not a live run.**
- **It mostly overlaps with `clear_at_least` and compaction.** If those are already configured well, the extra gain is near zero.

There is no gain in hit rate. Nothing in the answer brings middle edits, insertions or reordering to about 100% exactly.

HONEST GAIN: ~1.1x lower total API bill (0.90× vs append-only, exact KV, quality untested, offline replay on 42 SWE-agent traces); no hit-rate gain, and ≈none over well-configured batched context editing