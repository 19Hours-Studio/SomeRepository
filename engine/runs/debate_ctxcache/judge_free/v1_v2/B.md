=== IDEAS ===

**Framing.** If the prompt is kept append-only, almost every re-sent token is already a cache hit (99.9–100% in the replays below). The bill is then about **reads + writes** ≈ r · Σ(live context per request) + w · (new tokens). In the 50-call errata session below, reads are 324k of 479k units and writes are 156k. So "close to 100% hits" is the easy part. A much lower bill needs one of four things:
1. **Never break the prefix:** Idea 1.
2. **Fewer requests per unit of work:** Idea 2. This lever was unused before and is the largest one available client-only.
3. **No silent expiry:** Idea 3.
4. **No suffix rewrite when old context is cleared:** Idea 4, provider or own stack.

Cross-user reuse (Idea 5) and the own-stack cost floor are listed for completeness. They are mostly prior art.

**Replay setup** (`round2/sim3.py`; it reproduces round 1 exactly and includes the check's bookkeeping fix):
- A 10k-token system prompt. Each tool call adds 2,000 tokens of output plus a 300-token assistant turn.
- Every 5th call changes an earlier tool output.
- Work is fixed at 50 tool calls; the long-session runs use 200.
- Means over 100 seeds unless stated.
- **Prices:**
  - Anthropic: 5-minute TTL with writes at 1.25x and reads at 0.1x; 1-hour TTL with writes at 2x.
  - OpenAI GPT-5.6: 30-minute minimum TTL, reads at 0.1x, writes at 1.25x. The 1.25x is confirmed by secondary pricing pages and an excerpt attributed to OpenAI's guide, but not by OpenAI's pricing table.
  - Legacy OpenAI: writes at 1.0x.

**Baselines:**
- **in-place:** edited text is rewritten where it sits.
- **append-full:** the new full version is appended and the stale copy stays. This is what coding agents do today.

---

**IDEA 1 — Append-only client discipline (diff errata + first-seen document order)**

WHERE: Client only, so it works on any API. Infrastructure cost is zero. Latency is unchanged.

MECHANISM:
- Never mutate a token that has already been sent.
- A changed tool output or state block becomes a tagged diff at the tail, e.g. `[supersedes tool_result #17] line 42: x=3 → x=4`.
- An insertion becomes an appended block that names its anchor.
- Document sets are serialized in first-seen order, and JSON with sorted keys. The current retrieval rank is restated as a short ID list at the tail, about 5 tokens per document.
- Compaction is triggered by the context window and by an interference cap: compact a segment after m errata. m has to be measured.

COVERS: Exactly: middle edits, changed tool outputs, insertions, and reordering within a session. Not covered: deletions (a client-side delete breaks the prefix; see Idea 4) and new document combinations across users (Idea 5).

NUMBERS (`sim3.out`):
- **Against in-place:** 747,086 → 479,425 units, −35.8%.
  - Same −35.8% at GPT-5.6 prices, −31.7% at legacy OpenAI, −47.0% if reads cost 0.05x. The 0.05x read price for newer Anthropic models appears in one secondary source and is unverified.
  - Range over edit frequency: −6% to −60% (one edit every 25 to every 2 calls).
  - If the mutable state sits near the top of the prompt (a memory or todo block), the saving is −53.6%.
- **The stronger form of the claim:** errata cost 479k, which is 0.9% *below* the cost of the edited prompt even with a perfect cache (483,697, after the bookkeeping fix). So client-only errata reach the oracle cost of in-place editing.
- **Against append-full:** −11.0% (−11.1% if reads cost 0.05x). The only lever is diff size: diffs of 50 / 200 / 1,000 / 2,000 tokens give 474k / 479k / 506k / 539k units.
- **Hit rate on re-sent tokens:** 100% for errata, about 0.93 for in-place.
- **Growing document set:** 1,000 vs 6,003 tokens rewritten per request (10 docs × 1k), and 500 vs 12,758 (50 docs × 500) (`costs.py`).

QUALITY:
- The KV is exact for the *appended* prompt. The model sees stale text next to its correction.
- PI-LLM ("Unable to Forget") shows that retrieving the latest value of a key degrades log-linearly as overwritten updates accumulate.
- Test with a real model:
  - PI-LLM harness in three variants: in-place, errata, and errata with compaction at m.
  - Paired SWE-bench Verified replays, in-place vs errata. With 500 tasks the standard error is about 2.2 points, so repeated paired runs are needed to resolve a 2-point gap.
- Not run here: model weights cannot be downloaded in this environment.

PRIOR ART:
- Manus "append-only context" guidance, and agents that re-read files by appending.
- Duplicate re-display in SWE-agent demo trajectories is 18.7% / 38.1% / 64.4% (n=3 toy trajectories of 5–11 steps; illustrative only).

What this idea adds: the oracle-cost result, diff-sized errata, first-seen ordering, and the interference cap.

---

**IDEA 2 — Fewer requests per unit of work: batch independent tool calls, optionally delegate exploration** *(new lever)*

WHERE: Client only, on any API that supports parallel tool calls (Anthropic and OpenAI both do). Memory and storage are unchanged. Latency falls: fewer round-trips, and tools run concurrently.

MECHANISM:
- Once hits are about 100%, each request re-reads the whole live context at r. Halving the number of requests for the same tool calls removes about half of the reads Σ L.
- **(a) Batching.** Prompt or enforce that independent reads, greps and tests go out in one turn. Bloop's SWE-bench agent injects a reminder whenever the model makes only one call, because Claude did not batch reliably without it.
- **(b) Delegation.** A sub-agent runs a burst of exploration calls in a fresh context (sharing the cached system prompt) and returns a summary of S tokens. This shortens the parent's live context.

COVERS: All four change cases indirectly, because it composes with Idea 1. It does not by itself make a broken prefix hit.

NUMBERS (`sim3.out`, 50 calls; assistant output is scaled to 300 tokens per call issued, which is conservative):

| Calls batched | Requests | Errata cost | vs errata, sequential | vs append-full, sequential |
|---|---|---|---|---|
| 30% in pairs | 38.4 | 400k | −16.5% | — |
| 50% in pairs | 33.8 | 369k | −23.1% | — |
| 100% in pairs | 25 | 306k | −36.2% | −43.2% |
| 100% in groups of 4 | 13 | 227k | −52.7% | −57.9% |

- **Fair baseline:** current agents already batch some calls. Against append-full with 30% of calls already paired, errata with all calls paired gives −31.7%, and with groups of 4 gives −49.4%.
- **Published measurement on a real model** (W&D, BrowseComp, arXiv 2602.07359): 3 parallel calls per turn cost $65.7 per 100 tasks against $102.5 for one call per turn (−35.9%), with accuracy 68% against 66% and wall-clock −40.6%. The same paper finds a moderate width beats the maximum. Cognition's SWE-grep went from 4 to 8 parallel searches and cut turns from 6 to 4 at the same performance.
- **Delegation** (`subagent.out`, append-only, Anthropic prices): delegating 4 of every 5 calls with a 500-token summary gives −36.3% at 50 calls (−25.8% with 2,000-token summaries) and shrinks the final parent context from 125k to 41k tokens. This is **not** an information-matched comparison: the parent sees only summaries.

QUALITY:
- **Batching** removes the reasoning step between independent calls. Batching dependent calls would hurt.
  - Test: paired SWE-bench Verified with batching nudges off vs on, comparing pass rate, steps and cost. This needs a real model.
  - The BrowseComp result above is the only measured evidence, and it is not from coding.
- **Delegation** risks losing details the parent later needs.
  - Test: the same paired SWE-bench design, plus a probe of whether the parent can recall facts that only appeared inside the sub-agent.

PRIOR ART:
- Parallel tool use (provider feature), W&D, Bloop, SWE-grep.
- Sub-agents: Claude Code and Anthropic's multi-agent research system. Note that the latter *raised* total tokens because it ran wider, not because it delegated.

What this idea adds: the accounting showing that, once hits are near 100%, **request count × live context** is the cost driver, with the cost curve as a function of batching share.

---

**IDEA 3 — TTL-aware client: keep-alive pings vs 1-hour writes vs letting it expire**

WHERE: Client only. A ping is a request with the same prefix and `max_tokens=1`. It is billed at r × L and refreshes the cache entry.

COVERS: Answers the check's point 6. "100% hit on re-sent tokens" holds only while every gap stays inside the TTL.

NUMBERS (`ttl.out`, errata session; reference cost 479k with no idle gaps). "Idle share" is the fraction of requests that come after an idle gap of the given length.

| Idle gap | Idle share | Let expire | Keep-alive (ping every 4.5 min) | 1-hour TTL writes | Best option |
|---|---|---|---|---|---|
| 15 min | 5% | +42.7% | **+11.1%** | +19.5% | keep-alive, −22% vs expire |
| 15 min | 20% | +158.5% | +41.3% | **+19.5%** | 1h, −54% |
| 45 min | 5% | +42.7% | +33.4% | **+19.5%** | 1h, −16% |
| 45 min | 20% | +158.5% | +124% | **+19.5%** | 1h, −54% |
| 120 min | any | **+42.7% / +158.5%** | worse | worse | expire |

- With expiry, the hit rate on re-sent tokens falls to 0.945 at a 5% idle share and 0.796 at 20%.
- A blind online ski-rental rule (ping up to 11 times, then stop) matches keep-alive for gaps under 50 minutes. At 120-minute gaps it is up to about 2x worse than letting the cache expire (+83.6% vs +42.7% at a 5% idle share). So the policy should use a gap predictor ("handed back to the human" vs "tool running").
- GPT-5.6's 30-minute minimum TTL removes the 15-minute case entirely (+0.0%). At 45 minutes, keep-alive gives +3.7% / +13.8% against +42.7% / +158.5% for expiry. OpenAI also offers a 12-hour TTL at 2.5x writes.

QUALITY: None; the prompt is identical.

PRIOR ART: The TTL options are provider features. Keep-alive pinging is a known community practice, not something I could find in official guidance. What this idea adds is the policy table. Whether a 1-hour-TTL request can upgrade an existing 5-minute entry without a rewrite is untested.

---

**IDEA 4 — Span operations billed as hits: `delete_span` (punch) and `replace_span` (patch)**

WHERE: Own serving stack, or provider-side as an API operation.
- Freed paged-KV blocks return to the pool, so memory cost is zero.
- Recompute is k = 32 boundary tokens per hole.
- Optional delta-RoPE re-rotation of K: for 150k tokens of 70B BF16 K, about 48 GB of reads and writes, roughly 14 ms.
- An exact mode (suffix recompute) stays available per request.

MECHANISM: Clearing old tool results, or applying a patch, drops or replaces blocks in the block table. Everything after the change is reused, and only the new tokens plus k boundary tokens are computed (EPIC-style). This also removes the stale copies that cause Idea 1's interference.

COVERS: Middle edits, insertions, tool outputs, **deletions and compaction**, which no client trick can cover.

NUMBERS (`sim3.out` §3; 200 calls, 200k window). Against **errata**, the best client policy, as the check required:

| Retention: compact down to | punch vs errata | patch vs errata |
|---|---|---|
| 60k → 15k (deep) | +4.6% | −1.0% |
| 195k → 100k | −7.5% | −9.1% |
| 195k → 140k | −16.6% | −18.1% |
| 195k → 170k | −34.6% | −35.9% |
| 195k → 185k | −54.6% | −55.3% |

- The gain is set by how shallow and frequent compaction is (target/trigger ratio), not by an optimum. Cost falls monotonically as less history is kept, so retention is a quality choice, not a cost choice.
- The round-1 "cheapest retention = 40k, so −4.5% to −7%" was a grid-edge artifact and is withdrawn.
- Combined with batched pairs (Idea 2) at 170k retention: −66.2% against sequential append-full, about −63% against sequential errata.

Why this matters: current practice clears deep partly *because* each clear rewrites the suffix. Anthropic's context editing invalidates the cached prefix and offers `clear_at_least` so that each rewrite is worth its cost. Span ops make keeping more history affordable.

QUALITY:
- Not exact: tokens after a hole keep what they absorbed from the deleted span.
- Test against exact recompute of the edited prompt and against errata: PI-LLM, paired SWE-bench replays, and teacher-forced next-token KL with top-1 agreement on agent traces. Run both the position-gap and re-rotated variants.
- If quality falls below errata, use exact mode.
- This needs a real model.

PRIOR ART: llama.cpp `--cache-reuse` (chunk shifting); StreamingLLM, H2O and SnapKV (heuristic dropping); CacheBlend and EPIC (selective recompute). What this idea adds: a client-driven span API billed as a hit, and its cost curve against errata by retention.

---

**IDEA 5 — Segment cache with gated selective recompute (cross-request and cross-user reuse)**

WHERE: Own stack (LMCache CacheBlend in vLLM) or provider-side.
- Storage: one KV copy per unique segment; 320 KB/token for 70B BF16, 69 KB/token for DeepSeek-V3 MLA.
- Load: 6.6 s per 1M tokens over PCIe at 50 GB/s.

MECHANISM:
- Cache each document or memory unit on its own, keyed by content hash and computed after the shared system prompt (APE).
- On reuse, re-rotate positions and recompute a fraction of tokens:
  - RAG passages: CacheBlend (about 15%) or EPIC (32 tokens per chunk).
  - Agent memory: AgentKVShift (10–30% refreshed).
- A deviation gate falls back to exact recompute.

COVERS: Reordering and new document combinations across requests and users.

NUMBERS (from the papers):
- **RAG:** 85–94% of segment tokens reused; time-to-first-token 2.2–3.3x faster (CacheBlend), up to 8x (EPIC).
- **LoCoMo at a 10% recompute budget:** CacheBlend loses 47.5% of relative F1; AgentKVShift loses 5.9% (0.319 vs 0.339).

QUALITY: Approximate. Test against full recompute on 2WikiMQA, MuSiQue, LongBench and LoCoMo.

PRIOR ART: CacheBlend, EPIC, APE, Cache-Craft, Fusion-RAG, AgentKVShift, KVCOMM, RelayCaching. It is listed only because it is the sole route to cross-user reordering. Only the gating and per-workload engine choice are mine.

---

**Own-stack cost floor** (round-1 Idea 4, demoted: per the check it is prior art)

- On an own stack a hit really costs about 2% of a recompute ($0.0075/M of prefill attention vs $0.371/M recompute at position 60k), not the 10% that APIs charge.
- Decode KV reads are about half of session cost ($0.055 of $0.103). FP8 KV halves that part and MLA cuts it about 4.7x. (The round-1 claim that the asker had assumed input dominates is withdrawn; the question never says so.)
- **Tool-gap holding, rental basis on both tiers** (`tiers3.out`): HBM at $2/h per 80 GB, DRAM at $0.005/GB-h, reload stall charged.

  | Tool gap | Pin in HBM | Swap to DRAM | Discard + recompute |
  |---|---|---|---|
  | 5 s | 1.28x | 1x | — |
  | 30 s | 2.23x | 1x | — |
  | 120 s | 3.56x | 1x | — |
  | 600 s | — | $0.984 | $1.104 |

  At 600 s, the per-turn minimum of the three options ($0.960) beats swap-only by just 2.5%.
- Reload is hidden: 0.79 s to reload 120k tokens, against 2.33 s to prefill the 2.3k new tokens.
- This per-turn choice **is** InferCept's preserve / discard / swap, and Continuum sets HBM pinning time from reload cost. The gain over that prior art is about 0. It is kept only as the cost floor an own-stack operator should assume.

---

**WHAT CANNOT REACH ~100%, OR NOT WITHOUT QUALITY LOSS**
- **Brand-new content** (about 3.7% of tokens here) is always a write. The total token hit rate tops out around 96%; only the hit rate on re-sent tokens can reach about 100%.
- **Gaps longer than the longest affordable TTL:** more than about 1 hour on Anthropic, more than about 12 hours on OpenAI. These rebill the whole context (+43% at a 5% idle share, +159% at 20%). Even inside the TTL, hits are not guaranteed: there are forum reports of intermittent `cached_tokens=0` on identical prefixes. Measure the real rate from `cache_read_input_tokens` / `cached_tokens`.
- **Exact output after an edit, insertion or deletion** requires a suffix recompute:
  - Idea 1 is exact only for a different prompt (stale text plus correction), which has a measured interference cost.
  - Ideas 4 and 5 are approximate.
  - Ideas 2b and 4 at low retention change what the model sees.
- **Plain API users** get Ideas 1–3 only. Client-side deletions and compaction still break the prefix.
- **Cross-user reordering at exact quality** is not possible: it needs recompute.

=== NOTES (response to the check) ===

| # | Check point | Resolution |
|---|---|---|
| 1 | Idea 2 baseline | Accepted. Now reported against errata: −7.5% to −55% by retention, +4.6% when clearing deep. |
| 2 | 40k "optimum" | Accepted as an artifact. Withdrawn; there is no interior optimum. |
| 3 | Mixed pricing bases | Accepted. Now 1.28x / 2.23x / 3.56x on rental vs rental, with reload stall charged and min(pin, discard, swap) as the baseline. |
| 4 | Novelty of Idea 4 | Accepted. Demoted to a cost floor. |
| 5 | Bookkeeping bug | Fixed (`replay3.py`). The in-place oracle cost is 483,697, which errata undercut by 0.9%. |
| 6 | TTL | Accepted. It is now Idea 3, with policies that recover 16–54% of the expiry penalty for gaps under 1 hour. |
| 7 | OpenAI write price | Accepted. Secondary pricing pages and a quoted excerpt of OpenAI's guide give 1.25x writes and a 30-minute minimum TTL; the 12-hour TTL is at 2.5x. OpenAI's own pricing table did not appear in search results, so the 1.25x is not first-hand confirmed. With 1.25x writes, the GPT-5.6 column matches Anthropic's. |
| 8 | 32% duplicate figure | Replaced by 18.7–64.4%, n=3, illustrative only. |
| 9 | "Asker assumed input dominates" | Withdrawn. |

Undersold points (oracle cost, early mutable state at −53.6%, batching) are now included.

All replays are synthetic, and edit frequency, batching share and idle gaps are swept assumptions. No quality number was measured on a real model, because model weights cannot be downloaded in this environment. The only quality evidence comes from cited papers (W&D, PI-LLM, AgentKVShift, CacheBlend, EPIC).

The scripts and outputs are in `engine/runs/debate_ctxcache/round2/`: `sim3.py`, `ttl.py`, `tiers3.py` and `subagent.py` with matching `.out` files, plus `replay3.py`, `costs.py` and `trace_dup.py`.

**HONEST GAIN (synthetic replays, quality untested on a real model):**
- **Client only, any API, no idle gaps:**
  - Errata reach the oracle cost of in-place editing: −35.8% against in-place, −11% against append-full.
  - Adding batched pairs gives −43.2% against sequential append-full, or −31.7% if the baseline already pairs 30% of calls. Groups of 4 give −57.9% / −49.4%.
  - Published real-model evidence: −35.9% cost at +2 points of accuracy (W&D, BrowseComp).
- **With idle gaps:** a TTL policy cuts the expiry penalty by 16–54% for gaps under 1 hour. Gaps over 1 hour on Anthropic cannot be fixed.
- **Provider or own stack:** span operations give −17% / −35% / −55% against errata at 140k / 170k / 185k retention, about −1% when clearing deep, and −66% against sequential append-full when combined with batching at 170k.
- **Hit rate on re-sent tokens:** 99.9–100% while gaps stay inside the TTL.

Sources:
- [OpenAI prompt caching guide](https://developers.openai.com/api/docs/guides/prompt-caching)
- [GPT-5.6 caching billing (aihubmix)](https://aihubmix.com/blog/gpt-5-6-is-live-prompt-caching-billing-changes-explained)
- [GPT-5.6 pricing (techjacksolutions)](https://techjacksolutions.com/ai-tools/chatgpt/gpt-5-6-pricing/)
- [OpenAI 12-hour TTL at 2.5x (aiweekly)](https://aiweekly.co/alerts/openai-adds-12-hour-prompt-cache-ttl-to-api-25x-write-cost)
- [Azure prompt caching](https://learn.microsoft.com/en-my/Azure/foundry/openai/how-to/prompt-caching)
- [Anthropic prompt caching docs](https://docs.claude.com/en/docs/build-with-claude/prompt-caching)
- [Firecrawl on cache read prices](https://www.firecrawl.dev/blog/prompt-caching)
- [OpenAI forum: intermittent cached_tokens=0](https://community.openai.com/t/prompt-caching-returns-cached-tokens-0-intermittently-same-static-prefix-same-prompt-cache-key/1386029/2)
- [W&D parallel tool calling](https://arxiv.org/pdf/2602.07359)
- [Bloop: SWE-bench in half the steps](https://bloop.ai/blog/swe-bench)
- [Cognition SWE-grep](https://cognition.com/blog/swe-grep)
- [InferCept](https://arxiv.org/pdf/2402.01869)
- [Continuum](https://arxiv.org/html/2511.02230v2)