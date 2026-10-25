The answer's numbers reproduce exactly, and its main client-side result holds. Several headlines are inflated, though, because output tokens are never priced, and two cited sources don't support what they're used for. The provider-side figures of −35% and −55% compare against a compaction schedule no client would pick.

I copied the scripts into `critic2/` and re-ran them there. `sim3`, `ttl`, `tiers3` and `subagent` produce output byte-identical to round 2's. `costs` and `replay3` have no saved output, but my re-runs match every figure the answer quotes. My new checks are in `check2.py` / `check2.out`, and the full write-up is in `critique.md`.

## 1. Numbers that hold
- **Errata (Idea 1):** 747,086 → 479,425 units, −35.8% against in-place editing and −11.0% against append-full. The other figures also hold:
  - legacy OpenAI −31.7%; reads at 0.05x −47.0%;
  - edit-frequency sweep −6.2% to −59.9%; diff-size sweep 474k / 479k / 506k / 539k;
  - document rewrites 6,003 vs 1,000 and 12,758 vs 500 tokens.
- **Oracle claim:** errata cost 0.88% less than a perfect cache of the in-place prompt (483,697). This is true, partly because an erratum writes 200 tokens where the edited segment writes 2,000.
- **Batching, TTL and span-operation tables:** every cell reproduces. Patch plus batched pairs gives −66.2% against sequential append-full, about −63% against errata.
- **Own-stack figures:** 1.28x / 2.23x / 3.56x; $0.960 vs $0.984 (−2.4%); $0.0075/M vs $0.371/M; 320 KB and 69 KB per token; 14 ms; 6.6 s.
- **W&D paper:** $65.7 vs $102.5 per 100 tasks, 68% vs 66% accuracy and −40.6% wall-clock match the paper.

## 2. Unfair or unsupported points
1. **Output tokens are never priced.** Each call generates 300 tokens, which cost 5x input on Anthropic and 8x on OpenAI. Counting them at 5x:

   | Claim | As stated | Output priced (5x) | At 8x |
   |---|---|---|---|
   | Errata vs in-place | −35.8% | −32.6% | −30.9% |
   | Errata vs append-full | −11.0% | −9.6% | −9.0% |
   | Batched pairs | −36.2% | −31.3% | −29.0% |
   | Groups of 4 | −52.7% | −45.6% | −42.2% |
   | Pairs / quads vs a baseline that already pairs 30% | −31.7% / −49.4% | −27.2% / −42.3% | — |

   Thinking tokens could push batching the other way: −37% to −42%, but only if thinking cost scales with request count.
2. **The batching share is assumed, not measured.** The realistic rows, with output priced, are −14.3% (30% of calls paired) and −19.9% (50%). Nothing cited supports batching every coding call in groups of 4.
3. **SWE-grep can't count as evidence here.** Cognition's own post says it is RL-trained to make 8 parallel calls per turn, so it falls under the no-retraining exclusion. Bloop shows that an untrained model does not batch reliably. Only W&D survives, and it measures browsing, not coding.
4. **"New lever, unused before" is overclaimed.** Parallel tool calls are a provider feature, and the round-1 critic proposed this exact lever. What the answer adds is the accounting.
5. **Delegation's −36.3% is inflated.** Its baseline has no edits, and summaries and task prompts are billed as cache writes rather than generated output. With output priced it is about −26%, and the information is still not matched (the answer concedes this).
6. **Span ops' −35% / −55% compare against a schedule nobody would choose.** I plotted cost against the average live context per request. That confirms the percentages at matched context. But compacting 195k → 185k (every ~4–10 calls) buys only 154k average context, against 141k for errata compacting 195k → 140k (+9.5%). Against that sensible client setting, patch is −11.1% at 185k and about −17% at 140k. The robust provider-side gain is −9% to −18%.
7. **The ~100% hit rate holds by construction.** The simulation has no eviction apart from the modelled idle gaps. The answer's limits section does concede this.
8. **A quality risk in Idea 1 is not named.** First-seen ordering moves documents to arbitrary positions, and the known "lost in the middle" position sensitivity is never mentioned or tested.

## 3. Where the answer undersells itself
- **Span ops have a cleaner claim available.** Patch's cost per unit of average context stays flat at 23.6–24.3 once retention is 100k or more, while errata's rises from 26.6 to 52.7. In other words, span ops make cost independent of the compaction schedule.
- **The TTL policy could go further.** The answer already recommends a gap predictor. If it is used to write a 1-hour entry only on the request before a predicted idle gap, the idle penalty drops to +0.9% / +3.6%, against the best quoted +11.1% / +19.5%. This rests on one untested assumption: that a 1-hour write also extends the earlier, 5-minute-cached prefix. Two API calls 10 minutes apart, reading `cache_read_input_tokens`, would settle it.
- **The document-order baseline is too easy.** It compares first-seen order with canonical hash-sort, which is itself a known fix. Against the real default, relevance-ranked order, the saving would be larger; this isn't quantified.

## 4. Where a larger honest gain is most likely
- **Measure how many calls can actually be paired.** Replay real SWE-bench agent trajectories and mark the calls whose inputs don't depend on the previous result. Batching at that measured share is the largest client-only lever.
- **Selective 1-hour writes**, if the test above passes.
- **Own stack:** report span ops as a cost-versus-retained-context frontier rather than at matched compaction targets, combined with the ~2% real cost of a hit.

Sources:
- [W&D (arXiv 2602.07359)](https://arxiv.org/html/2602.07359v1)
- [Cognition SWE-grep](https://cognition.com/blog/swe-grep)
- [Portkey on mixing Anthropic cache TTLs](https://portkey.ai/docs/aigw/integrations/llms/anthropic/prompt-caching)
- [Spring AI issue on TTL ordering](https://github.com/spring-projects/spring-ai/issues/4325)

HONEST GAIN: Client-only errata −35.8% vs in-place (−32.6% with output priced) and −11% vs append-full (−9.6%); batching adds −14% to −31% on top, depending on the unmeasured pairable share; provider span ops −9% to −18% vs errata at sensible retention. All synthetic, quality untested.