The answer's main measured claim, a 40% input-cost cut with a 99.75% hit rate from append-only errata, is inflated by a billing bug in its replay. After the fix the honest number is about 28%, and only when edits land deep in the context. All the other arithmetic reproduces. Idea 2 is not new: there is direct prior art the answer missed.

## 1. Re-derived numbers

| Claim | Status |
|---|---|
| Break-even after 1,238 turns (edit at 50k) and 50 turns (edit at 90k) | **Holds, slightly high.** A rewrite replaces a 0.1x read of the suffix, so its extra cost is 1.15×(N−p), not 1.25×(N−p). That gives 1,137 and 45 turns. The conclusion that errata almost always win on cost still stands. |
| Replay: hit rate 92.9% → 99.75%, billed input 604k → 365k (−40%) | **Does not hold.** The script reproduces it for seed 0, but `calc.py` counts each turn's new tool result and assistant output (2,300 tokens) as cache reads. They are new input and are billed as 1.25x writes. Corrected, averaged over 200 seeds: in-place edits 88.7% hit and 762k units; errata 96.3% and 506k (−33.6%). |
| "Erratum + ski-rental" result | **Not tested.** Compaction never triggers in 50 turns: the two policies give identical output. So the "at most 2x the best schedule" claim is never exercised. |
| KV size per token: 320 / 160 / 69 KB | Holds. |
| Recompute $0.175 per 1M tokens; holding 1M tokens for 1h costs $8.19 in GPU memory, $1.64 in CPU RAM, $0.07 on NVMe | Arithmetic holds. The price inputs are the author's own assumptions. |
| PCIe load 6.6 s per 1M tokens | Holds. |
| Effective hit 85% (CacheBlend) and ~94% (EPIC) | The arithmetic holds. CacheBlend's 15% recompute and 2.2–3.3x faster time-to-first-token, and EPIC's "up to 8x", match the papers. |
| OpenAI cached input at 0.1x | Third-party aggregators list GPT-5 at $0.125 cached vs $1.25 base. That fits, but it is still not confirmed on an official OpenAI page. |
| Anthropic context editing invalidates the cache | Confirmed by Anthropic's docs. |

## 2. Unfair or unsupported points

**Where the answer overstates:**
- **The billing bug.** Fixing it lowers both hit rates (99.75% → 96.3%) and cuts the saving from about 43% (200-seed mean with the bug) to 33.6%.
- **Erratum size.** The replay uses a 1,000-token erratum to replace a 2,300-token entry. A full-size erratum lowers the saving from 33.6% to **28.0%**. The 1,000-token figure is only fair if errata are diffs, and the answer never says so.
- **Where edits land.** The replay picks the edited entry uniformly across the whole context. Agents mostly re-read recent files. With edits a mean of 2 entries back, the saving is −0.9% (1,000-token erratum) and **+7.5% more expensive** (full-size erratum). So the 40% only holds for edits deep in the context.
- **The ~100% hit-rate claim.** Even with no edits at all, the corrected floor is 96.3%. New content per turn is always a miss, so no session whose context keeps growing reaches about 100% token hit rate. The "cannot reach 100%" section should say this.
- **Hash-sorting documents.** This handles a pure reordering of the same document set. But adding one new document invalidates **50%** of the document tokens on average (simulated for 5 to 50 documents). Ordering by first appearance invalidates 0%. It can also hurt quality wherever relevance order matters.
- **Idea 2's novelty.** Leyline (arXiv 2606.01065, June 2026) already proposes explicit replace/remove-span directives with a RoPE rotation fix in SGLang, and reports +11.2 percentage points of hit rate. llama.cpp's `seq_rm` and `seq_add` already delete spans on an explicit request. What remains is only the billing proposal, and the "12.5x cheaper" figure is just the price ratio 1.25/0.1, not a measurement.
- **Idea 3's compute saving.** The "3–7x" figure mixes compute fractions with time-to-first-token numbers. EPIC reports that CacheBlend's own overhead is 16–63% of time-to-first-token. FusionRAG reports that at 15% recompute, Qwen2.5-7B only recovers to Qwen2.5-3B quality. The answer cites FusionRAG, but still calls the result "same-quality".
- **Idea 4 comparison.** "MLA cuts storage 4.6x" compares two different models, and their recompute costs differ too.

**Where the answer undersells itself:**
- **Recompute cost.** The $0.175 figure ignores attention compute. Including it gives $0.227 per 1M tokens at 32k context and $0.338 at 100k. The break-even reuse interval then grows from 6 minutes to 8–12 minutes for CPU RAM, and from 2.5 h to 3.5–5.2 h for NVMe. That strengthens Idea 4.
- **Hit rate on reused tokens.** Measured only on tokens that were sent before, Idea 1 reaches exactly 100% and the KV is exact. The answer could claim that cleanly instead of the inflated 99.75%.
- **Frequent deep edits.** With full-size errata and edits deep in the context, the saving reaches 45% when edits come every 2 turns and 57% at every turn. The tradeoff is extra context of 57k–115k tokens.

## 3. Where a larger honest gain is most likely
- **Diff errata plus first-appearance ordering (client only).** Errata written as diffs make the small-erratum assumption honest, which is worth about 6 points (28% → 34%). Ordering documents by first appearance removes the 50% invalidation when a document is added.
- **Reads are the cost, not writes.** In the corrected no-edit floor, 0.1x reads are about two-thirds of billed input. So the biggest lever is Idea 4's storage-priced read on the provider side, and the case gets stronger at long context once attention is counted.
- **Own serving stack.** Combine a Leyline-style splice for deletes and replacements with CacheBlend or EPIC for reordered documents. Gate it on measured KL divergence against full recomputation. That needs a real-model run, which this environment cannot do.

Everything is in `/home/user/SomeRepository/engine/runs/climb_ctxcache/check0/`: `REPORT.md`, plus `replay_fixed.py` and `checks.py` with their `.out` files, and `calc_orig.py` (a copy of the author's script).

Sources:
- [CacheBlend](https://arxiv.org/html/2405.16444v3)
- [FusionRAG](https://arxiv.org/pdf/2601.12904)
- [LMCache CacheBlend blog](https://blog.lmcache.ai/2024-10-09-cacheblend/)
- [EPIC](https://www.alphaxiv.org/abs/2410.15332.md)
- [AgentKVShift](https://www.alphaxiv.org/abs/2607.21604.md)
- [Leyline](https://arxiv.org/pdf/2606.01065)
- [Anthropic context editing](https://docs.claude.com/en/docs/build-with-claude/context-editing)
- [devtk GPT-5 pricing](https://devtk.ai/en/models/gpt-5/)
- [pricepertoken GPT-5](https://pricepertoken.com/pricing-page/model/openai-gpt-5)

HONEST GAIN: Idea 1 cuts billed input by about 28% against in-place edits (token hit rate 88.7% → 96.3%, not 92.9% → 99.75%), for full-size errata with edits spread across the context every 5 turns. The gain is about 0% or negative when edits are to recent context.