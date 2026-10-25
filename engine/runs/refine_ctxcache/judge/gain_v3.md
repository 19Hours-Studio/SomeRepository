# Check of the answer

**What I could verify.** I tried to inspect the directory and run checks, but none of the tool calls returned any output to me. So I could not confirm that `calc.py`, `calc_out.txt`, `cachediff.py`, `traces/` or `examples/` exist, or what they print. Everything below comes from re-deriving the answer's numbers by hand from its stated assumptions.

## Arithmetic that holds up

- **§A bill split.** With 12k tokens written on the first turn, then 2.3k per turn, reads at 0.1, writes at 1.25 and output at 5 over 50 turns, I get reads 58.8%, writes 27.8%, output 13.4%. That matches the stated 59/28/13.
- **TTL.** The 7.5× and 2.5× figures (1.25·6 and 2 + 0.5) are correct.
- **Ski-rental threshold.** (57,500 − 625)/50 ≈ 1,138 and (11,500 − 2,500)/200 = 45 are correct. The 2-competitive bound is the standard result.
- **Ordering rule.** The adjacent-swap exchange gives cost(ij) − cost(ji) ∝ pᵢsⱼ(1−pⱼ) − pⱼsᵢ(1−pᵢ). So sorting by p/((1−p)s) ascending is correct. It is a Smith's-rule-style result, and the measured gain over p/s is a median of 1%.
- **`cachediff` multipliers.** An 11% hit gives 0.011 + 1.25·0.89 = 1.12, which is 11.2× a full hit. A 0% hit gives 12.5×. Both are correct.
- **§H reasoning stripping.** 0.126 → 0.161 per token is about 1.27×. Correct.
- **Idea 3 table.** It reproduces exactly if the baseline is popularity-ordered prefix reuse (34% or 60% hits), approximate tokens cost 0.25, and the shadow adds 0.01. For example, s = 0.8, f = 0 gives 0.694/0.29 = 2.40×. The baseline is therefore fair.

## Unfair or unsupported comparisons

1. **The headline §C baseline is a strawman.** "Authoring order 47.1%" is not current practice. Manus and Anthropic already recommend a stable prefix, append-only history, deterministic serialization and the to-do list recited at the end. Those correspond to the 93.7–95.3% rows. The only increments that are new are the diff-only tail re-send and the breakpoint placement, which take 95.3% to 98.0%.
   - Input cost per token is about 0.0953 + 1.25·0.047 ≈ 0.154 before and 0.098 + 1.25·0.02 ≈ 0.123 after. That is about 1.25× on input.
   - Input is about 87% of the bill, so the total gain is about 1.2×.
   - This comes from a synthetic model. The quality of a model reading accumulated tail diffs is untested.
2. **Idea 2 (splice) is compared against weak baselines.** The best current exact practice is batched clearing, as in Anthropic context editing with `clear_at_least`, which is the answer's "every 15 steps" row.
   - Against that row the splice gains 1.05/0.82 ≈ 1.28× at 30 steps and 0.77/0.62 ≈ 1.24× at 80 steps.
   - These numbers come from 3 tiny trajectories with a 65-token median observation.
   - The splice is billed as an exact-priced hit even though its output is approximate.
   - Its quality was not measured, and the method is prior art (llama.cpp context shift, StreamingLLM, Leyline).
   - So no supported gain.
3. **Idea 3's 1.4–2.4× belongs to CacheBlend, EPIC and APE, not to this answer.** The answer's addition, the shadow gate, can only *reduce* cost savings relative to ungated CacheBlend, through fallbacks plus the 1% shadow. Its quality benefit is unmeasured. There is no supported cost gain.
4. **Idea 4 is exact but creates no new hits.** Tiered retention is prior art (LMCache, Mooncake, CachedAttention). The "~1.2× your earlier run measured" refers to data that isn't shown.
5. **§0's "0.63× input bill" depends on Idea 2.** It is approximate and should not be read as an exact saving.
6. **Unverifiable claims.** I could not check "GPT-5.6 `cache_write_tokens` at 1.25×, confirmed" or the 1.7% → 92.2% blog figure.

## What the answer gets right

- It states clearly that exact reuse after an in-place change is capped at roughly 1/L of the suffix work.
- It acknowledges that near-100% hits on real middle edits are possible only approximately.
- It notes that at 100% hits the bill floor is reads + writes + output.

These limits are correct, and they mean the question's target is not met for real middle edits under the no-retraining constraint.

## Net assessment

The only gain over best current practice that is both exact and supported comes from the client-side layout refinements: diff-only tail and breakpoint placement. In the answer's own synthetic agent model, they raise the hit rate from about 95.3% to 98.0%. That is about 1.25× lower input cost per token, or about 1.2× on the total bill. The result is modelled, not measured on real traffic, and the effect of tail diffs on quality is untested. Splice and segment-cache gains are either prior art or unvalidated approximations.

HONEST GAIN: ~1.2x lower input cost per token (95.3%→98.0% token hit rate, exact, client-side, synthetic agent model only); no supported gain for real middle edits