=== IDEAS ===

**What changed this round.** Earlier rounds used only synthetic sessions. This round replays **441 real agent trajectories**: mini-SWE-agent v2.4.2 with gemini-3-5-flash on SWE-bench Verified, 19,514 requests in total. They come from the submitter's public repo `john-b-yang/20260901_mini-v2.4.2_gemini-3-5-flash`, which records real `prompt_tokens`, `completion_tokens` and `reasoning_tokens` plus timestamps for every request. The round also uses **one real Claude Opus 4.6 trajectory** with provider cache fields (`SWE-bench/experiments`, `analysis/test_data/claude-4-6-opus.json`). Output tokens are now priced in every number (5x input on Anthropic, 8x on OpenAI). Scripts: `round3/trace4.py`, `own4.py` and `sim4.py`, with matching `.out` files.

**Framing, measured on real traces** (`trace4.out`, Anthropic prices: read 0.1x, 5-minute write 1.25x, output 5x):
- The traces are append-only already. Exact prefix caching already saves **78.9%** against no caching (95.2M vs 450.4M units).
- On the real Claude trajectory the hit rate on re-sent tokens is **99.38%**, and the token hit rate is 94.8%. My pricing reproduces its logged bill exactly ($0.4036 = 80,728 units × $5/M).
- What remains of the bill: **reads 41.9%, writes 19.9%, output 38.2%.** The real Claude run splits 41.7% / 25.6% / 30.1%.
- Per request: mean context 21.2k tokens, 759 new input tokens, 373 output tokens. Sessions peak at a median of 29.7k tokens and a maximum of 125k. Only 0.20% of requests exceed 100k.
- Gaps between requests: median 2.2 s, p99 40 s, maximum 112 s. **None of the 19,073 gaps exceeds 5 minutes.**

So on a well-built autonomous agent, "close to 100% hits" is already true, and output cannot be cached. The levers left are fewer requests (reads), less duplicated content (writes and reads), and fixing harnesses that *mutate* their context. The last is where the large gains are. Each idea below states which regime it applies to.

---

**IDEA 1 — Append-only client discipline: errata, back-references, first-seen document order**

WHERE: Client only, so it works on any API. Infrastructure cost is zero; latency is unchanged.

MECHANISM:
- Never mutate a token that has already been sent.
- A changed tool output or state block becomes a tagged diff at the tail, e.g. `[supersedes tool_result #17] line 42: x=3 → x=4`.
- An insertion becomes an appended block that names its anchor.
- **New this round: back-references.** The tool wrapper replaces runs of lines that were already shown verbatim with `[lines 120-180 unchanged, see obs #7]`.
- Document sets are serialized in first-seen order (JSON with sorted keys). The current relevance rank is restated at the tail, about 5 tokens per document.
- An interference cap compacts a segment after m errata; m has to be measured.

COVERS: Middle edits, changed tool outputs, insertions and reordering within a session. Not covered: deletions (Idea 4) and cross-user combinations (Idea 5).

NUMBERS (output priced at 5x; the second figure is at 8x):

| Regime | Change | Source |
|---|---|---|
| Real append-only agent: back-references only | 26.9% of observation tokens are verbatim re-shows; **−3.7%** | measured, `trace4.out` §B |
| Mutating harness (in-place edit every 5th call) | **−32.6%** (−30.9%) vs in-place | synthetic, `sim4.out` §1 |
| Agents that re-display the full file (append-full) | −9.6% (−9.0%) | synthetic |
| Multi-turn RAG, 10 of 60 docs, relevance drift 0.1 / 0.3 | **−43.6% / −36.3%** vs relevance-ranked order (the real default) | synthetic, `sim4.out` §4 |

- On the RAG row, canonical hash-sorting saves nothing in this model, because the retrieved *set* changes every turn. First-seen order wins only because it keeps the union of documents seen so far: the final context is 44.7k / 62.4k tokens against 24.7k. This is **not information-matched**: the model sees more documents, including stale ones. Cap the union with periodic compaction.
- Oracle result (round 2, still valid): errata cost 0.9% *less* than a perfect cache of the in-place prompt.

QUALITY:
- The KV is exact for the appended prompt, but the prompt itself differs from the edited one. Two risks:
  1. **Interference** from stale text sitting next to its correction. PI-LLM shows that retrieving the latest value degrades log-linearly as overwritten updates accumulate.
  2. **Position.** First-seen order can put the currently most relevant document in the middle, where accuracy dips ("Lost in the Middle", Liu et al., TACL 2023: a U-shaped curve over position).
  - Back-references make the model look up earlier content instead of re-reading it.
- Tests on a real model (not run here, since weights cannot be downloaded):
  - A PI-LLM harness in three variants: in-place, errata, and errata with compaction at m.
  - A position-controlled multi-document QA: relevance-ordered vs first-seen with the tail rank list, on the same retrieved set.
  - Paired SWE-bench Verified runs with back-references off vs on. With 500 tasks the standard error is about 2.2 points, so repeated paired runs are needed.

PRIOR ART: Manus append-only guidance; agents that re-read files by appending. What this idea adds: the oracle-cost result, measured duplication on real traces, quantified first-seen ordering against the relevance-ranked default, and the interference cap.

---

**IDEA 2 — Fewer requests: batch the calls that are measurably independent** *(accounting is mine; the lever is a provider feature and was raised by the round-1 critic)*

WHERE: Client only, on any API with parallel tool calls. Latency falls.

MECHANISM: Once hits are about 100%, each request re-reads the whole live context at r, so merging k requests into one turn removes (k−1) reads of L. Batching is prompted or enforced; Bloop shows Claude does not batch reliably without a reminder.

**Measured pairable share (new).** All 19,514 real requests issued one call per turn. A call j was counted as mergeable into the previous turn only if all of the following hold:
- every earlier call in that turn is read-only;
- call j writes nothing;
- call j uses no identifier component or number that first appeared in that turn's observations.

The **strict** variant also excludes:
- calls that follow an empty or failed result, or a traceback;
- line numbers within ±60 of a number shown in the observation;
- one experiment run following another;
- continued reads of the same file.

I hand-checked 30 sampled merges for each variant. The lexical test alone is too generous: about 10 of 30 merges were dependent. The strict test reaches **77–90% precision** (3 of 30 clearly dependent, 4 ambiguous).

| Rule (all output tokens kept) | Requests merged away | Cost |
|---|---|---|
| strict, pairs, read-only follow-ups | 15.4% | −5.7% |
| strict, up to 4 per turn, any non-write | 22.7% | **−8.7%** |
| strict, up to 8 | 23.0% | −8.8% |
| lexical upper bound, up to 8 | 50.7% | −19.0% |

- Adjusted for precision, the expected saving is **about −5% to −8%** on this workload.
- The round-2 headline of −36% to −53% assumed that every call could be paired or grouped. It is withdrawn: on real coding traces the share is about 15–23%.
- On the synthetic session with output priced, a 23% share gives −11.8% (`sim4.out` §1). Real sessions gain less because their reads are a smaller share of the bill.

COVERS: All four change cases indirectly, because it composes with Idea 1.

QUALITY:
- Batching removes the reasoning step between calls. The strict filter targets calls whose next step did not use the previous result, but semantic dependence remains a possibility (the 10–23% imprecision above).
- Evidence on a real model: W&D (BrowseComp, arXiv 2602.07359) measured 3 parallel calls per turn at $65.7 vs $102.5 per 100 tasks, with 68% vs 66% accuracy. That is browsing, not coding.
- SWE-grep is **dropped as evidence**: it is RL-trained to issue parallel calls, which breaks the no-retraining constraint.
- Test: paired SWE-bench Verified with a batching nudge off vs on, comparing pass rate, step count and the `cache_read_input_tokens` totals.

**Combined with back-references (real traces, strict, up to 4 per turn): −12.0%** (`trace4.out`).

Delegation to sub-agents, re-priced with output at 5x and edits in both arms (`sim4.out` §3): −23.9% with 500-token summaries, but only −3.9% with 2,000-token summaries. The parent sees only summaries, so this is not information-matched; it is kept only as an option.

---

**IDEA 3 — TTL policy: only for human-in-the-loop sessions**

The real autonomous traces have **no gap longer than 112 s**, so a 5-minute TTL never expires in them. This idea matters only when a human pauses the session.

| Policy | Idle penalty (5% / 20% of requests after a 15–45 min gap) | Status |
|---|---|---|
| Let it expire | +42.7% / +158.5% | round-2 `ttl.out` |
| Best of keep-alive pings or all-1h writes | +11.1% / +19.5% | round-2 `ttl.out` |
| **Selective 1h:** a 1h breakpoint only on the request before a predicted gap | **+0.9% / +3.6%** | conditional |

How the selective-1h figure is computed: 0.75 × 2,340 × 0.05 × 49 / 479,425 = 0.9%. It holds **only if** a 1h breakpoint placed after a 5-minute-cached prefix extends the TTL of that earlier prefix. Anthropic documents that 1h entries must precede 5-minute ones in a request. It does not say whether the earlier prefix is re-tagged. If it is not, the full prefix has to be rewritten at 2x, which is worse than letting it expire (2.1L vs 1.25L).

Test: write at t=0, send the 1h-breakpoint request at t=4 min, then a request at t=15 min, and read `cache_read_input_tokens`.

Gaps beyond the longest TTL (1 hour on Anthropic, 12 hours on OpenAI at 2.5x writes) cannot be fixed client-side.

QUALITY: None; the prompt is identical.

---

**IDEA 4 — Span operations billed as hits: `delete_span` / `replace_span`** (provider or own stack)

WHERE / MECHANISM / COSTS: unchanged from round 2.
- Freed paged-KV blocks return to the pool.
- k = 32 boundary tokens are recomputed per hole.
- Optional delta-RoPE re-rotation: about 14 ms for 150k tokens of 70B K.
- An exact mode (suffix recompute) stays available.

COVERS: Deletions and compaction, which no client trick can cover, plus edits and insertions.

NUMBERS (now as a cost vs **mean live context** frontier, output priced; `sim4.out` §2, 200 calls, 200k window):
- **Patch** cost per unit of mean context stays flat at 25.5–26.7 for any retention of 100k or more. **Errata** rises from 28.9 to 54.7 as compaction gets shallower. Span ops make cost roughly independent of the compaction schedule.
- **Fair comparison**, against errata's most cost-efficient setting (195k → 100k):

  | Patch retention | Cost vs errata@100k | Context vs errata@100k |
  |---|---|---|
  | 100k | **−8.4%** | same |
  | 140k | −1.7% | **+9.1%** |
  | 185k | +6.1% | +20.3% |

- Against a client that insists on the same deep retention:

  | Retention | Patch vs errata |
  |---|---|
  | 140k | −16.9% |
  | 170k | −34.0% |
  | 185k | −53.4% |

  These large numbers apply only to that choice.
- The robust gain is **−8% to −17%**, or about +9–20% more retained context at roughly equal cost.
- **Real-trace relevance:** these SWE-bench sessions peak at 125k tokens and never trigger compaction, so the gain is 0 on them. It applies only to long sessions.

QUALITY: Not exact: tokens after a hole keep what they absorbed from the deleted span. Test against exact recompute and against errata with PI-LLM, paired SWE-bench replays, and teacher-forced next-token KL plus top-1 agreement on agent traces. Run both the position-gap and re-rotated variants. If quality falls below errata, use exact mode. This needs a real model.

PRIOR ART: llama.cpp `--cache-reuse`, StreamingLLM / H2O / SnapKV, CacheBlend / EPIC. What this idea adds: a client-driven span API billed as a hit, and its frontier against errata.

---

**IDEA 5 — Segment cache with gated selective recompute** (cross-user reordering; own stack or provider)

Unchanged and mostly prior art:
- CacheBlend: 85–94% of segment tokens reused, time-to-first-token 2.2–3.3x faster.
- EPIC: up to 8x faster.
- LoCoMo at a 10% recompute budget: CacheBlend loses 47.5% of relative F1, AgentKVShift 5.9%.
- Storage: 320 KB/token for 70B BF16, 69 KB/token for MLA.

Approximate. Test on 2WikiMQA, MuSiQue, LongBench and LoCoMo against full recompute. Only the deviation gate and the per-workload engine choice are mine.

---

**Operator view: what cached context really costs on the real workload** (`own4.out`; 70B GQA, BF16 KV, H100 at $2/h, real per-request tokens and gaps)
- Cost split with all hits served and KV pinned in HBM across gaps ($17.37 for 441 tasks):
  - decode KV reads 53.1%;
  - HBM holding 25.5%;
  - new-token prefill 15.5%;
  - attention over the cached prefix 5.9%.
- Recomputing those prefixes instead would add $91.86.
- **True marginal cost of a hit** = attention over the cached prefix + holding. With DRAM swap over the real gaps it is **2.1% of recompute**; pinned in HBM it is 5.9%. API read prices are 10%, so an operator has room to cut the read price roughly 2–5x at cost parity on hits.
- **Swap over gaps instead of pinning:** holding falls from $4.42 to $0.88, about −20% of operator cost. The reload of about 7 GB at 21k tokens takes 0.14 s and is assumed hidden behind prefill. This is InferCept / LMCache prior art.
- **FP8 KV** halves the decode reads (−26.5%), also prior art.
- The largest operator cost of reused context is re-reading it during decode, not storing it.

---

**WHAT CANNOT REACH ~100%, OR NOT WITHOUT QUALITY LOSS**
- **Brand-new tokens are always writes.** The measured token hit rate is 94.8% on the real Claude run. Only the hit rate on re-sent tokens reaches ~99.4%.
- **Output (30–38% of the real bill)** is outside caching altogether.
- **Gaps longer than the longest TTL** rebill the whole context. Selective 1h writes are unverified. Intermittent `cached_tokens=0` on identical prefixes has been reported, so measure the real rate from usage fields.
- **Exact output after an edit, insertion or deletion** needs a suffix recompute:
  - errata and back-references are exact for a *different* prompt;
  - span ops and segment reuse are approximate;
  - delegation and first-seen unions change what the model sees.
- **Plain API users** get Ideas 1–3 only.
- **Cross-user reordering at exact quality** is impossible.
- **Already append-only harnesses** have little left to gain: about −12% measured.

=== NOTES (response to the check) ===

| # | Check point | Resolution |
|---|---|---|
| 1 | Output tokens not priced | Accepted. Output is priced everywhere: −32.6% / −9.6% for errata. On real traces output is 38.2% of the bill. |
| 2 | Batching share assumed | Accepted and **measured**: 15.4–23.0% of real requests (strict, precision 77–90%) give −5.7% to −8.8%. The 100%-paired and groups-of-4 headlines are withdrawn. |
| 3 | SWE-grep is RL-trained | Accepted. Dropped as evidence; W&D is the only evidence left. |
| 4 | "New lever" overclaim | Accepted. Credited as a provider feature raised by the round-1 critic; only the accounting and the measurement are mine. |
| 5 | Delegation inflated | Accepted. Re-priced with output and edits: −23.9% (500-token summaries) to −3.9% (2,000). Not information-matched. |
| 6 | Span ops against an unrealistic schedule | Accepted. The frontier now gives −8.4% at equal context, or +9% context at −1.7%. The −34% / −55% figures apply only to deep retention. |
| 7 | 100% hits by construction | Refuted with data: a real Claude trace measures 99.38% on re-sent tokens (n=1, 36 requests). Real gaps are 112 s or less. |
| 8 | Lost in the middle not named | Accepted. Named, with a position-controlled test. |

On the critic's undersold points, the flat-cost frontier and selective 1h are adopted, and the relevance-ranked document baseline is quantified (−36% to −44%, not information-matched).

**HONEST GAIN** (no quality number was measured on a real model):
- **Already append-only agent, real traces, client only:** about **−12%** (batching −5% to −9% after precision, plus back-references −3.7%). Hit rate on re-sent tokens is already about 99.4%.
- **Harnesses that mutate or reorder context (synthetic):**
  - errata: **−32.6%** vs in-place (−30.9% at 8x output);
  - RAG first-seen order: **−36% to −44%** vs relevance order, with a larger context.
  - This is the regime with the large gains.
- **Human-in-the-loop idle gaps:** expiry penalty of +42.7% / +158.5%. The best verified policy brings it to +11% / +20%; selective 1h would bring it to +0.9% / +3.6% if the re-tag test passes.
- **Provider span ops on long sessions:** −8% to −17%, or +9–20% retained context at equal cost.
- **Operator:** true hit cost is 2.1–5.9% of recompute against a 10% price. Swap-over-gaps (−20%) and FP8 KV (−26.5%) are prior art.

Sources:
- [mini-SWE-agent + gemini-3-5-flash trajectories](https://github.com/john-b-yang/20260901_mini-v2.4.2_gemini-3-5-flash)
- [SWE-bench experiments (claude-4-6-opus test trajectory)](https://github.com/SWE-bench/experiments)
- [Anthropic prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
- [Portkey on mixing Anthropic TTLs](https://portkey.ai/docs/aigw/integrations/llms/anthropic/prompt-caching)
- [Spring AI issue on TTL ordering](https://github.com/spring-projects/spring-ai/issues/4325)
- [Lost in the Middle (arXiv 2307.03172)](https://arxiv.org/abs/2307.03172v3)
- [W&D parallel tool calling](https://arxiv.org/pdf/2602.07359)
- [Bloop SWE-bench](https://bloop.ai/blog/swe-bench)
- [Cognition SWE-grep (RL-trained)](https://cognition.com/blog/swe-grep)
- [OpenAI prompt caching guide](https://developers.openai.com/api/docs/guides/prompt-caching)
- [OpenAI 12-hour TTL at 2.5x](https://aiweekly.co/alerts/openai-adds-12-hour-prompt-cache-ttl-to-api-25x-write-cost)
- [OpenAI forum: intermittent cached_tokens=0](https://community.openai.com/t/prompt-caching-returns-cached-tokens-0-intermittently-same-static-prefix-same-prompt-cache-key/1386029/2)
- [InferCept](https://arxiv.org/pdf/2402.01869)
- [Continuum](https://arxiv.org/html/2511.02230v2)