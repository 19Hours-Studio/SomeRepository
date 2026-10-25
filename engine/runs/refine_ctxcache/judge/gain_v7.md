# Review: what the answer actually supports

## Bottom line

After the corrections below, the only gain over best current practice that is **measured** (not modelled) and **does not drop content** is Idea A. "Reference, don't repeat" brings the API bill to **0.881×**, against **0.993×** for the strongest information-exact prior art (Claude Code-style whole-file re-read dedup). That is **0.887×, about 11% lower**. It comes from cost replays of 42 traces. Output quality was not tested. Every larger number either compares against a weak baseline, depends on an inferred provider behaviour, rests on a roofline model, or drops content with untested quality.

## Corrections to the answer's own comparisons

**1. Batched clearing vs. provider context editing (0.745 and 0.796 ratios): not supported as stated.**
- **The provider's semantics are inferred, not measured.** The keep-3 and keep-10 advantages depend on `clear_tool_uses` being stateless, so the cleared boundary moves every turn even with `clear_at_least`. The answer says it inferred this from the docs. `clear_at_least` exists to amortize cache rewrites, which is what batching does. If the inference is wrong, much of the gap may close.
- **At keep 10 the baseline is not current practice.** The provider tool scores 1.006×, which is worse than not clearing. No sensible practitioner would run it. The fair baseline is no clearing (1.0×), so the measured gain is 0.801×, not 0.796.
- **Quality is only plausibly covered in one setting.** Clearing tool *inputs*, and keep 3, are untested. The only setting with any outside quality support is results-only, keep 10, via *The Complexity Trap*'s observation masking. That setting gives **0.880× against no clearing**. Clearing old observations is itself prior art (Complexity Trap, Manus, the provider tool). What is new is the batching schedule and the EOQ rule for T, which is a modest addition.
- **The combined keep-10 figure (0.720×) also relies on untested input clearing.**

**2. Runner: 0.556× GPU time against a no-speculation stack is the wrong baseline.**
- Best current practice for agent and code traffic already includes model-free speculation. SuffixDecoding ships in vLLM via Arctic Inference. Against suffix decoding with a cross-session corpus (0.708×), the claim becomes 0.556/0.708 ≈ **0.785×**.
- **The draft-length cap is ordinary tuning.** Capping drafts at ⌊t_mem/t_token⌋−1 is roofline tuning of `num_speculative_tokens`. SuffixDecoding already adapts speculation length. Treating "default settings" as the baseline overstates novelty. Against a tuned drafter (0.626×), the remaining gain is just references: 0.556/0.626 ≈ **0.89×**.
- **None of it is measured.** These are roofline numbers for a 70B dense model on 8×H100, driven by Claude outputs and a legacy tokenizer.
- **The 0.80× figure against MTP is also modelled**, with acceptance assumed from DeepSeek-V3.

**3. The 4-bit KV, splicing (0.406×) and segment-cache (Idea 3) results are prior-art techniques with approximate quality.**
- 4-bit KV and splicing correspond to KV quantization, Leyline/KV-Editable/PatchKV, and CacheBlend/EPIC/APE.
- The Idea 3 savings come from a synthetic Zipf replay.
- None of these count as supported gains.

**4. Smaller internal inconsistencies.**
- **"12× more than whole-result stubs" does not match the table.** The savings are 0.119 vs 0.007, which is about **17×** at MINRUN=4 and about 15× at MINRUN=8.
- **The warm-up figures don't follow from the stated prices.** With writes at 1.25× and reads at 0.1×, warm-up before fan-out saves 2.5/1.45 ≈ **1.72×** at N=2 (claimed 1.9×) and 62.5/6.25 = **10.0×** at N=50 (claimed 10.2×).
- **The bill model misses logged cost by 25%** ($38.01 modelled vs $50.63 logged). The answer argues ratios still hold because the ratio is stable at 0.70–0.77 across sessions. That is reasonable, but it is calibration, not validation.
- **The `round7/` artifacts are not in this workspace**, so I could not reproduce any number.

**5. Idea A's own caveats.**
- **The hit rate is unchanged** (97.0% → 97.1%). The gain is fewer tokens, not more hits.
- **"Information-exact" is not the same as "quality-neutral".** The model must resolve pointers, and must reproduce `old_str` for `str_replace` from a distant copy. The answer correctly proposes an A/B test on resolve rate and `No replacement was performed` errors, but did not run it.

## Does it meet the question's targets?

- **Near-100% hits after middle edits: no.** The answer says so honestly. Exact reuse past an in-place change is impossible, so it falls back to append-only errata, which is established practice (Manus, Anthropic docs).
- **Insertions and reordering:** handled only by canonical layout (prior art), or approximately (Idea 3).
- **"Much lower cost":** reached only by dropping content (clearing) or by approximate KV, whose quality is unverified.
- **Its honest-limits section is largely accurate.** That is the answer's strongest part.

## Supported gain, by audience

| Claim | As stated | Fair baseline | Supported gain | Status |
|---|---|---|---|---|
| A: references (API) | 0.881× vs as-sent | Claude Code dedup, 0.993× | **0.887×** | Measured cost, quality untested |
| B: batched clearing, results only, keep 10 | 0.874× vs provider | No clearing, 1.0× | 0.880× | Measured cost; mostly prior art |
| B: keep 3 / inputs cleared | 0.745× vs provider | Depends on unverified semantics | Not supported | Quality untested |
| C: runner | 0.556× vs no speculation | Tuned suffix decoding, ~0.626× | ~0.89× (0.785× if the cap counts) | Modelled only |

HONEST GAIN: ~0.89× of the API bill (≈11% lower) vs Claude Code-style re-read dedup, information-exact, measured on 42 replayed SWE-agent traces; output quality untested