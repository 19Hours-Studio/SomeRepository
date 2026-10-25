# Review of the answer's claims

I checked the answer's reasoning and its comparisons. I did not run `calc.py` or rebuild the traces, because `round6/` is not in this workspace. The trace numbers below are therefore taken as reported. The question is whether they show a gain over **best current practice**, not over a weakened baseline.

## 1. Runner side: 0.66× GPU time from "lossless speculation"

**The baseline is not best practice.** The 0.663× is measured against "prefix caching with FP8 KV and **no speculation**." Model-free speculation is already a shipped config option in vLLM. Prompt-lookup decoding (`ngram`) and SuffixDecoding (`suffix`, Arctic Inference) both exist, and SuffixDecoding was evaluated on the same kind of workload (OpenHands on SWE-bench). The answer lists all of these as prior art. Turning on an existing feature is the best-practice baseline, not a gain over it.

**The draft-length cap is also prior art.** The cap accounts for 0.737× → 0.663×. Adaptive draft lengths are standard, and SuffixDecoding already adapts speculation length per request. The answer admits the effect with EAGLE or MTP is unmeasured. Its figure is also a roofline model, not measured GPU-seconds.

**The replay transfers less than it claims.** The replay is exact only for greedy Claude outputs with a legacy tokenizer. A self-hosted 70B model's copying rate is unmeasured, and the answer says so.

**It is off target.** Speculation speeds up decode. It does not make reused context cheaper after middle edits, insertions or reordering, and it gives API users nothing.

**Corrected gain over best practice: none demonstrated.** What remains is a useful measurement: acceptance rates on public agent traces, and the finding that clearing old tool inputs lowers acceptance from 2.46 to 1.96 tokens per pass. Those are observations, not a cost improvement over current practice.

## 2. API side: 0.647× bill, or 0.74× of Anthropic context editing

**The competitor is set up wrongly.** The answer models Anthropic context editing as rolling and stateless, clearing one more turn every step. It concludes that client-side *batched* clearing beats it (0.647 against 0.874). But Anthropic's `clear_tool_uses` strategy has a `clear_at_least` parameter. It exists to force each clear to remove a minimum number of tokens, so the cache-invalidating rewrite happens rarely. That is batched clearing. The strategy also has `clear_tool_inputs`, which clears tool inputs. The answer's grid sweeps only `trigger` and never tunes `clear_at_least`. The answer also concedes that the "exact stateless semantics of context editing" were not verified. With `clear_at_least` tuned, the provider's feature performs the same batching, so most of the 0.874 → 0.647 gap is an artifact of the comparison.

**The content kept is not the same on both sides.** Keep 3 against a 20k trigger is "close but not identical in content" by the answer's own admission.

**Quality is not established for the headline setting.** The 0.647× setting keeps 3 results and also clears inputs. The answer says this is "below or outside any published setting," and no resolve rate was measured. The setting that published results plausibly support is batched keep-10 on results only, at 0.880×. That is no better than the provider's 0.874×. A cost gain bought by dropping content cannot be credited without a quality-matched comparison.

**The bill model has a small bias.** It undercounts by about 25%, partly from missing tool schemas. Schemas are a fixed per-request cost that clearing cannot remove. Including them moves every ratio toward 1, so the "ratios hold" claim slightly overstates the savings.

**Corrected gain over best practice: none demonstrated.** Batching and input clearing both already exist in the provider's tool. The EOQ rule for choosing the period is a convenient tuning heuristic for `clear_at_least`, not a new cost level.

## 3. Everything else

- **Splicing (0.561×, 0.436×) and the segment cache (Idea 3):** approximate. Quality is untested, and the Idea 3 coverage comes from a synthetic Zipf replay. The answer itself assigns these to prior work (CacheBlend, EPIC, APE, Leyline and others).
- **4-bit KV:** approximate and prior art.
- **Idea 1** (layout, errata, ordering) and **Idea 4** (pricing retention per memory tier): prior art (Manus, *Don't Break the Cache*, tiering). Idea 4 is about 1.2× by the answer's own figure, and on these traces it "mainly avoids breaks."
- **The honest-limits section is the answer's strongest part.** It correctly states that exact reuse after an in-place change is capped at about 1/L of the suffix work, and that hit rate (already 97%) is not the lever on agent traffic. These points are correct, but they are limits, not gains.

## Verdict

After correcting the baselines, the answer supports no measured gain over best current practice:
- The runner baseline should include existing ngram or suffix speculation.
- The API competitor should include `clear_at_least` and `clear_tool_inputs`.
- Lossy settings should be compared at matched quality.

What it does contribute is a reproducible way to measure cost on public traces, and a few hypotheses that are worth testing.

HONEST GAIN: none