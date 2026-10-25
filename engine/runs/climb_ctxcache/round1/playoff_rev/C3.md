=== IDEAS ===

**What still limits the gain (measured).** I replayed 63 real SWE-agent trajectories (Claude 3.5 Sonnet on SWE-bench Verified, 2,068 API calls) with exact prefix-cache billing. Each trace's token count is calibrated so that SWE-agent's own policy matches the `tokens_sent` it recorded. Under Anthropic 5-minute prices (write 1.25x, read 0.1x), the bill for plain append-only context splits like this:

- reads of the per-task fixed prefix: 18%
- reads of the growing history: 46%
- first writes of new content: 36%
- output tokens: another 17% on top of input

So once you append only, cache reads are the largest term (64%). They grow with (context kept) × (number of calls), and no hit-rate gain can reduce them. After the best client-side policy below, the bill is:

- first writes of new content: 41%. No caching scheme can remove these; only sending fewer new tokens does.
- history reads: 28%
- fixed-prefix reads: 26%
- rewrites after cache breaks: 5%

That is what the ideas below target.

**IDEA 0 (new, headline): cost-priced batch masking plus content-addressed delta views**
- **Where it runs:** client only, with any API.
- **Mechanism:**
  - **(a) Delta views.** When the agent views a file again, any run of 3 or more lines it has already seen unchanged (same path, same line offset) is replaced by a 12-token back-reference, for example "(lines 40–139 unchanged, see view #7)". A view that something later still points to is never masked. This is the current answer's "erratum as a diff", applied in the place where edits really happen.
  - **(b) Batch masking with a price-based trigger.** Old observations become eligible for masking only when SWE-agent's own last-5 rule would hide them. They are actually masked in one batch, when the running read cost of keeping them (0.1 × tokens) reaches the one-time cost of rewriting the suffix (1.15 × suffix). This is a ski-rental rule.
- **Cases covered:** changed tool outputs and re-views (exact, using delta views), and tool-result clearing and compaction (which are really deletions). It does not help with document reordering or middle insertions.
- **Result on real traces** (fixed agent actions; `replay.out`, `robust.out`, `thresh.out`):

| Policy | Billed input | vs append-only | Token hit rate |
|---|---|---|---|
| Append-only | 9.54M | — | 95.7% |
| SWE-agent's shipped last-5 masking (breaks the cache) | 15.06M | +58% | 69.7% |
| Delta views only (no information removed) | 7.68M | −19.4% | 95.8% |
| Delta views + batch masking | 6.64M | −30.4% | 93.6% |

- **Robustness of the −30.4%:**
  - The 95% bootstrap confidence interval is −26.3% to −33.8%. It is better than append-only on all 63 traces (median −20.6%).
  - OpenAI prices give −32.2%; Anthropic's 1-hour cache gives −26.4%.
  - The ski-rental trigger costs 1.025x the exact offline optimum (computed with dynamic programming).
  - It beats the best fixed `clear_at_least`-style threshold (that is, Anthropic context editing tuned in hindsight) only by 1–4% (0.964x without delta views, 0.988x with them). Most of the gain comes from the delta views and from batching, not from the price rule itself. Its edge is that it needs no tuning.
- **Shared prefix:** the 7.1k-token system prompt plus demo is identical in every task. If it is cached once for a whole fleet, both policies save 0.50M. Delta views + batch masking + shared prefix then comes to 6.14M against 9.04M for append-only + shared prefix, which is −32.1%.
- **Hit rate trade-off:** the cost goes down while the token hit rate goes down too (95.7% → 93.6%). Hit rate is the wrong target. On tokens that were already sent, append-only already hits 100%, and what remains is reading them again.
- **Quality:** KV is exact; no token is ever reused out of its context.
  - At all 4,136 (call, variant) checks, batch masking hid only observations that SWE-agent's shipped last-5 policy also hid (`superset.out`). So the model always sees at least what the shipped agent saw.
  - Lindenbauer et al. (The Complexity Trap, NeurIPS'25) found that last-N masking matches or beats the raw agent's solve rate on SWE-bench Verified.
  - Delta views need their own test, because the model has to follow back-references. The test is an A/B on SWE-bench Verified: solve rate, plus how often the model asks to view the same file again, comparing append-only, last-5 masking, and Idea 0. That needs a real model and was not run here.
- **Costs:** none in storage or latency. The client keeps a per-line hash index (kilobytes).
- **Prior art:** Anthropic context editing (`trigger` / `clear_at_least`), SWE-agent's last-N observation masking, and Manus's "restorable compression". What this adds: a real-trace measurement showing that the shipped masking costs +58% under caching, a trigger set by prices instead of tuning, and lossless diff re-views.

**IDEA 1 (kept, corrected): append-only errata with ski-rental compaction**
- **Where it runs:** client only. Same mechanism as before.
- **Corrected numbers:**
  - Break-even is T* = (1.15(N−p) − 1.25e)/(0.1e) turns. That gives 1,137 turns for the edit at 50k and 45 turns for the edit at 90k (previously 1,238 and 50).
  - In the synthetic replay with billing fixed (200 seeds), errata cut cost by 28.0% with full-size errata and 33.6% with diff errata (hit rate 88.7% → 96.3%). The gain is only for edits deep in the context. For edits to recent entries it is +0.9% (diff errata) and −7.5% (full-size errata, more expensive).
- **Document order:** order documents by first appearance, not by content hash. With hash order, adding one document invalidates 50% of document tokens on average; with first-appearance order, none.
- **Quality:** KV is exact. The risk is that stale text stays next to its correction, so it needs an A/B test with superseded-fact needle tests.

**IDEA 2 (kept, re-scoped): span deletes via block-table edits**
- **Where it runs:** your own serving stack, or provider-side.
- **Mechanism:** drop the KV blocks of a deleted span; keep the later blocks as they are, with a position gap or a RoPE re-rotation.
- **Prior art:** Leyline (arXiv 2606.01065, which reports +11.2 percentage points of hit rate) and llama.cpp's `seq_rm` / `seq_add` already do this. All that is new is billing a deletion as a hit.
- **On real traces:** last-5 masking plus this splice comes to 6.56M (−31.3% vs append-only); with delta views it is −35.0%. That is only about 5 points better than client-only Idea 0, and the KV is no longer exact, because tokens after the hole still carry what they absorbed from the deleted span.
- **Quality test:** KL divergence and top-1 agreement against full recompute on these traces, then the solve rate on SWE-bench. Needs a real model.

**IDEA 3 (kept): segment cache with boundary recompute** (CacheBlend / EPIC with a deviation gate)
- **Where it runs:** your own stack, or provider-side.
- **Cases covered:** the only idea here that handles reordering and middle insertion for documents that do not repeat.
- **Hit rate:** about 85–94% of reused tokens. Time-to-first-token improves 2.2–3.3x (CacheBlend) and up to 8x (EPIC).
- **Quality is not the same as full recompute.** FusionRAG reports that at 15% recompute, Qwen2.5-7B only recovers to Qwen2.5-3B quality. Test against full recompute on 2WikiMQA, MuSiQue and LongBench.
- **Storage:** one KV copy per unique segment (320 KB per token for 70B BF16).

**IDEA 4 (kept, strengthened): cost-based pricing of retention and reads**
- **Where it runs:** your own stack, or provider-side.
- **Physical cost of a read** for a 70B model on an H100, using the real traces' mean of 1,076 new and 156 output tokens per call (`phys.out`):
  - prefill attention against a cached token: 0.020x the cost of recomputing it
  - streaming its KV during decode: 0.048x, which cascade or shared-prefix attention can divide across concurrent sessions
- **Implication:** on your own stack, fixed-prefix reads (26% of the bill) could be priced near 0.02–0.03x instead of 0.1x. Re-billing earlier assistant output as a read instead of a 1.25x write saves another 0.37M (about 6%); vLLM already keeps that KV.
- **Retention:** keep each prefix in a storage tier only while expected reuses × recompute cost exceed storage cost × time. Counting attention, the break-even reuse interval is 8–12 minutes for CPU RAM and 3.5–5.2 hours for NVMe.

**What cannot reach about 100%:**
- Any session that keeps growing: each call's new content is a miss. That is 41% of the best bill, and caching cannot remove it.
- Exact middle insertion or substitution in reused KV (Ideas 2 and 3): only appending stays exact.
- Reordering of documents that do not repeat, on a plain API.
- Plain API users get Ideas 0 and 1 only. Those deliver about −30% on real agent traces, not 10x. Beyond that, the only levers are less context kept (Idea 0's quality trade-off) or provider-side pricing (Idea 4).

=== NOTES ===
- **Files** are in `/home/user/SomeRepository/engine/runs/climb_ctxcache/round1/lever/`, with commands in `README.md`. `extract.py` builds `traces.json`, a 1-in-8 sample of the public `swe-bench-submissions` S3 bucket, holding message sizes and per-line hashes. The scripts are `replay.py`, `robust.py`, `terms.py`, `thresh.py`, `superset.py` and `phys.py`, each with a matching `.out` file. `replay.py` was re-run after adding the `thresh` policy, and its output is unchanged.
- **Assumptions:**
  - Tokens are chars/3.45 (median per-trace calibration); no tokenizer was available.
  - Back-references are 12 tokens. Sensitivity runs at 30 tokens and longer minimum runs move the result by at most about 2 points.
  - The 5-minute TTL never expires inside a trace.
  - Agent actions are held fixed, so these are prompt costs, not changes in behaviour.
- **Needs a real-model run:** the quality of every idea. huggingface.co is blocked here, so no quality claim was measured.

Sources:
- [The Complexity Trap (arXiv 2508.21433)](https://arxiv.org/abs/2508.21433)
- [Anthropic context editing](https://docs.claude.com/en/docs/build-with-claude/context-editing)
- [Anthropic context management announcement](https://www.anthropic.com/news/context-management)
- [Helicone context editing reference](https://docs.helicone.ai/gateway/concepts/context-editing)
- [Agno Anthropic context management](https://docs.agno.com/models/providers/native/anthropic/usage/context-management.md)
- [Anthropic prompt caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)
- [Leyline](https://arxiv.org/pdf/2606.01065)
- [CacheBlend](https://arxiv.org/html/2405.16444v3)
- [EPIC](https://arxiv.org/abs/2410.15332v3)
- [FusionRAG](https://arxiv.org/pdf/2601.12904)
- [Manus context engineering](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)
- [devtk GPT-5 pricing (unverified)](https://devtk.ai/en/models/gpt-5/)