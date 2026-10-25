=== IDEAS ===

**What changed this round**
- **New real-trace regime.** I replayed the same 441 real trajectories (19,514 requests, real token counts and timestamps) under a harness policy that really does change earlier context: SWE-agent's `LastNObservations`. Its docs give n=5 as the classic setting and say it "breaks prompt caching". This moves the "edit in the middle" case from synthetic sessions onto real token streams.
- **New provider lever.** I priced `replace_span`/`delete_span` on those streams and on the RAG model.
- **Corrections.** I adopted the check's corrections to the headline, the back-reference rule, the RAG baseline and the operator model.
- **Files.** Scripts are `round4/trace5.py`, `rag5.py` and `hitrate5.py`, each with a `.out` file. Prices are in units of base input: read 0.1, 5-minute write 1.25, output 5.

**Framing (real traces, unchanged and confirmed by the check)**
- Exact prefix caching already saves 78.9% against no caching.
- The real Claude run hits 99.38% of re-sent tokens and 94.8% of all input tokens (n=1, 36 requests).
- What remains of the bill: reads 41.9%, writes 19.9%, output 38.2%. Reasoning tokens alone are about 29% of the bill.
- No gap between requests exceeds 112 s.

So "close to 100%" is already true for append-only agents. The large losses come from harnesses and RAG layouts that change earlier context. That is where the big honest gains below come from.

---

**IDEA 1 — Cache-aware elision for harnesses that mask or trim observations** (client only, any API; new real-trace numbers)

MECHANISM:
- Harnesses that elide old tool outputs, such as SWE-agent `LastNObservations` or the JetBrains "observation masking" recommendation, change a middle block on every step. Everything after it is then rewritten at 1.25x.
- Fix: elide in batches. Every p steps, mask everything older than the last n observations. SWE-agent's `polling` parameter is exactly this; it is prior art and is credited.
- My contribution is pricing it on real streams.

COVERS: Middle edits and changed or elided tool outputs.

NUMBERS (`trace5.out` §B; 441 real token streams; output priced; the agent's actions are assumed unchanged under masking):

| Policy | Cost vs append-only | Token hit rate | Mean context |
|---|---|---|---|
| append-only | 0 | 96.3% | 21.2k |
| LastN n=5, polling=1 (classic) | **+49.3%** | 74.9% | 13.9k |
| n=5, polling=5 | +5.5% | — | 14.5k |
| n=5, polling=20 | −0.4% | 92.7% | 16.3k |
| n=10, polling=1 | +115.5% | — | 15.3k |
| n=10, polling=20 | +3.9% | — | 17.2k |

- Against the classic per-step setting, polling gives **−29% to −33%** (n=5) and **−52%** (n=10).
- Against append-only it saves nothing: a client can trim context at no extra cost, but cannot make trimming pay.
- So the JetBrains finding that masking "roughly halves cost" does not carry over to these traces once cache reads are priced. That agrees with the check's mask_check result (+1.5% to +19%).

QUALITY:
- Published: on SWE-bench Verified, masking matched LLM summarization, and with Qwen3-Coder 480B it went from 53.8% to 54.8% against the raw agent (Lindenbauer et al. 2025).
- Polling shows the model between n and n+p−1 observations, which is a superset of LastN(n). So quality should be no worse than the classic setting.
- Test: paired SWE-bench Verified runs (500 tasks, standard error about 2.2 points, so repeat them) comparing p=1 vs p=20. Track pass rate, *step count* (masking may cause re-reads, which this replay cannot see) and the `cache_read_input_tokens` totals.

---

**IDEA 2 — Provider `replace_span` / `delete_span`, billed as a hit** (own stack or provider; extends round-3 Idea 4, now priced on real streams)

MECHANISM:
- The client marks a span for replacement, for example an observation turned into a 10-token placeholder.
- The server edits the paged-KV block table and recomputes k=32 boundary tokens after each hole.
- Positions are handled either with RoPE gaps or with delta-RoPE re-rotation (about 14 ms for 150k tokens on 70B).
- Everything else is billed as a read, and freed blocks return to the pool.
- An exact mode (recompute the suffix) stays available.

COVERS: Deletions, compaction and masking, which no client trick can make cheap, plus replacements.

NUMBERS on real streams (`trace5.out`):

| Comparison | Cost | Token hit rate | Context |
|---|---|---|---|
| LastN n=5 via span ops vs classic LastN(5), identical visible prompt | **−42.5%** | 94.2% vs 74.9% | same |
| Same, vs append-only | −14.1% | — | −34% |
| vs the client's cheapest polling setting with at least the same mean context (fair frontier, n=5/10/15) | **−11.0% to −13.7%** | — | — |
| span n=5 + strict batching, precision-scaled, vs append-only | **−18.5% to −19.2%** | — | — |

- Sensitivity: with k=128 boundary tokens instead of 32, cost rises by about 2.3% (110 extra units per hole against 4,879 per request).
- Operator side: mean live context falls from 21.2k to 13.9k. That cuts decode-time KV reads by about 14% of operator cost, or about 21% if KV is pinned in HBM. These are first-order scalings of the check's batch-32 model.
- Long synthetic sessions (round 3, `sim4.out` §2) give −8.4% at equal context. I drop the −17% end, as the check asked.

QUALITY:
- Not exact: tokens after a hole keep what they absorbed from the elided text, so this sits between "masked" and "raw". Both of those score about the same on SWE-bench in the published masking results, but that has not been shown for the hybrid.
- Tests on a real model (not runnable here):
  - teacher-forced next-token KL and top-1 agreement against exact recompute of the masked prompt, on these trace prompts;
  - paired SWE-bench Verified runs;
  - both position variants (gaps and re-rotation).
- Fall back to exact mode if span ops score below polling.

PRIOR ART: llama.cpp `--cache-reuse`; StreamingLLM, H2O and SnapKV (server-chosen eviction); CacheBlend and EPIC.

ADDS: a client-chosen span API billed as a hit, and its price on real masking streams.

---

**IDEA 3 — RAG: never put retrieved documents ahead of the history; append only new documents** (client) **+ `delete_span` for documents that drop out** (provider)

**Baseline (partly refuting the check).** Calling this layout "the real default" is supported. LangChain's chat-history RAG how-to puts `{context}` in the system message, *before* `MessagesPlaceholder("chat_history")`. Every change to the retrieved documents therefore rebills the whole history.

**Conceded.** The round-3 gain came from document *position*, not from first-seen order. First-seen order is withdrawn.

NUMBERS (`rag5.out`; the check's model: 30 turns, top-10 of 60 documents of 800 tokens each; synthetic):

| Layout (drift 0.1 / 0.3) | vs LangChain layout | vs tail | Mean context | Information |
|---|---|---|---|---|
| tail: this turn's documents after the history | **−34.9% / −36.2%** | 0 | 17.45k | same as baseline |
| tail, only new documents, union capped at 12 | −48.3% / −36.6% | −20.5% / −0.7% | 18.1k / 17.6k | ≈ same |
| tail, only new documents, uncapped union | −69.1% / −59.9% | −52.5% / −37.2% | 28.3k / 41.9k | more, including stale documents |
| **tail_new + `delete_span` of departed documents** | **−67.7% / −55.4%** | **−50.3% / −30.2%** | 17.5k | same document set; order differs |

- Token hit rates at drift 0.3: 12.3% (LangChain layout), 49.9% (tail), 70.0% (span).
- The ceiling is set by genuinely new documents, which are always writes.

QUALITY:
- Tail placement keeps exactly the baseline's information but moves the documents next to the question. "Lost in the Middle" suggests that position near the end is, if anything, favourable.
- The span variant is approximate in the same way as Idea 2, and documents sit in first-seen order.
- Test: position-controlled multi-document QA (NaturalQuestions-Open in the Liu et al. setup) and a multi-turn RAG benchmark, comparing the LangChain layout, tail, and tail_new+span on the same retrieved sets.

---

**IDEA 4 — Append-only discipline for in-place editors: errata, back-references, batching** (client)

- **Errata** (a superseding diff at the tail instead of an in-place edit): **−32.6%** (−30.9% at 8x output) against in-place edits. This is synthetic only; how common in-place editing is was not measured. Interference risk: PI-LLM. Test with a PI-LLM harness comparing in-place, errata, and errata with compaction.
- **Back-references, corrected rule** (runs of at least 3 re-shown lines): −3.2%; at least 5 lines: −2.5%.
- **Strict batching** (cap 4, precision 77–90%, all output kept): −8.7% raw.

**Combined, precision-scaled, real traces: −9.7% to −10.8%** (runs ≥3). The check's −10.4% to −11.5% used the looser back-reference rule; with runs ≥5 I get −9.0% to −10.1%.

- If merged requests drop a quarter of their output (one reasoning pass fewer, unverified): −11.7% to −13.1%.
- Batching evidence on a real model: W&D (browsing, not coding) measured $65.7 vs $102.5 per 100 tasks at 68% vs 66% accuracy.
- Test: paired SWE-bench runs with a batching nudge off vs on.

---

**IDEA 5 — TTL for human-paused sessions** (client)

The idea is unchanged:
- Expiry penalty: +42.7% / +158.5%.
- Best verified policy (keep-alive pings or all-1h writes): +11% / +20%.
- Selective 1h breakpoint on the turn that waits for a human: **+0.9% / +3.6%**.

Plausibility, upgraded per the check:
- Cache entries are keyed by prefix.
- The gap is predictable: it starts at the end of the assistant turn, when it waits for the human.
- From memory (search excerpts did not show it), Anthropic bills mixed TTLs as: read up to the last hit, 1h write up to the 1h breakpoint, 5-minute write after that.

It is still conditional on the re-tag test: write at t=0, send the 1h-breakpoint request at t=4 min, then a request at t=15 min, and read `cache_read_input_tokens`. Autonomous traces gain nothing, since their longest gap is 112 s.

**IDEA 6 — Segment cache with selective recompute** (cross-user reordering)

This is prior art, unchanged:
- CacheBlend reuses 85–94% of segment tokens.
- EPIC is up to 8x faster.
- On LoCoMo at a 10% recompute budget, CacheBlend loses 47.5% of relative F1 and AgentKVShift 5.9%.

Only the gating is mine. Test against full recompute on 2WikiMQA, MuSiQue and LoCoMo.

**Operator view** (corrected per the check: decode weight reads included, batch 32, $22.64 for 441 tasks):
- Decode KV reads are 40.7% of operator cost.
- FP8 KV saves −20.4% and swapping KV to DRAM over gaps saves −15.6%. Both are prior art.
- The true marginal cost of a hit is 2.1% of recompute if the reload is hidden, 3.7% if not, against a 10% API price.
- Span-op masking (Idea 2) adds roughly −14% (decode KV) by shrinking the live context.

---

**WHAT CANNOT REACH ~100%, OR NOT WITHOUT QUALITY LOSS**
- **New tokens are always writes.** That means 94.8% token hits on the real Claude run, and 70% at best in drifting RAG.
- **Output (30–38% of the bill, about 29% of it reasoning)** is outside caching. Reasoning budgets are an untested lever.
- **Gaps longer than the longest TTL** (1h on Anthropic, 12h on OpenAI) rebill the whole context.
- **Exact output after an edit or deletion** needs a suffix recompute:
  - errata and polling are exact for a *different* prompt;
  - span ops and segment reuse are approximate.
- **Plain API users** get Ideas 1, 3 (tail placement), 4 and 5. Span ops need a provider or their own stack.
- **Cross-user reordering at exact quality** is impossible.

=== NOTES (response to the check) ===

| # | Check point | Resolution |
|---|---|---|
| 1 | −12% uses batching before the precision discount | Accepted: precision-scaled −9.7% to −10.8% |
| 2 | Back-reference rule too loose | Accepted: runs ≥3 give −3.2%, runs ≥5 give −2.5% |
| 3 | RAG first-seen gain is a baseline artefact | First-seen order is withdrawn. "Real default" is supported by the LangChain how-to layout. New best: tail −35% (information-matched, client); tail_new+span −68% / −55% at the same document set |
| 4 | Operator model leaves out weight reads and sets reload to zero | Accepted: 40.7% / −20.4% / −15.6%; 3.7% if the reload is not hidden |
| 5 | Span ops −17% | Dropped. New real-stream frontier: −11% to −14% |
| 6 | Mutating regime unmeasured | Addressed with a documented real policy (LastN) replayed on real streams: +49% penalty; polling and span ops fix it |
| U1 | Batching that removes reasoning passes | Given as a range (−11.7% to −13.1%), not counted in the headline |
| U2 | Selective 1h more plausible | Upgraded; test still required |
| U3 | Compaction on short sessions | Agreed, and quantified: client masking never beats append-only (best −0.4%) |

**HONEST GAIN** (no quality number measured on a real model; replays assume unchanged agent actions):
- **Append-only agent, real traces, client only: −9.7% to −10.8%.**
- **Real streams with a masking harness:**
  - client polling: −29% to −52% against the classic per-step setting;
  - **provider span ops: −42.5% at an identical prompt, −11% to −14% against the client's best at equal or greater context, −18.5% to −19.2% against append-only together with batching.**
- **Multi-turn RAG** (synthetic, LangChain-layout baseline):
  - tail placement **−35%** (client, information-matched);
  - **tail_new + delete_span −55% to −68%** (provider, same document set);
  - a capped client union adds −1% to −21% over tail.
- **In-place editors:** errata −32.6% (synthetic).
- **Idle humans:** penalty from +158% down to +20% (verified) or +3.6% (conditional).

Sources:
- [mini-SWE-agent + gemini-3-5-flash trajectories](https://github.com/john-b-yang/20260901_mini-v2.4.2_gemini-3-5-flash)
- [SWE-bench experiments](https://github.com/SWE-bench/experiments)
- [SWE-agent history processors (LastNObservations, polling, "breaks prompt caching")](https://swe-agent.com/latest/reference/history_processor_config/)
- [SWE-agent PR #1580 (polling)](https://github.com/SWE-agent/SWE-agent/pull/1580)
- [The Complexity Trap (arXiv 2508.21433)](https://arxiv.org/abs/2508.21433)
- [LangChain: add chat history to RAG](https://python.langchain.com/docs/how_to/qa_chat_history_how_to)
- [Anthropic prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
- [Portkey: Anthropic TTL mixing](https://portkey.ai/docs/aigw/integrations/llms/anthropic/prompt-caching)
- [Koog cache-control docs](https://docs.koog.ai/prompts/prompt-creation/cache-control/index.md)
- [Anthropic Ruby SDK CacheCreation](https://www.rubydoc.info/github/anthropics/anthropic-sdk-ruby/main/Anthropic/Models/CacheCreation)
- [Vertex AI Claude prompt caching](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/claude/prompt-caching)
- [Lost in the Middle](https://arxiv.org/abs/2307.03172v3)
- [W&D parallel tool calling](https://arxiv.org/pdf/2602.07359)
- [OpenAI prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching)
- [InferCept](https://arxiv.org/pdf/2402.01869)
