# Task: kill test - find the one number that decides whether each idea lives

QUESTION: Hosted LLM APIs (Anthropic, OpenAI and others) offer prompt caching. The provider stores the computed intermediate state (the attention key/value, or KV, cache) for a request's token prefix. A later request is served from that state only if its prefix is token-for-token identical, and the cached portion is billed at a discount. An edit in the middle of a prompt, an insertion, a changed tool output, or a different document order breaks the match from the first differing token onward. Everything after that point is recomputed and billed at full price. The asker wants a way to make cached context much cheaper and to reach a cache-hit rate close to 100%. This must include requests that differ from earlier ones in the middle, by insertions, tool outputs or reordered documents, and it must work without retraining or fine-tuning the model. The question does not say whether the asker runs their own serving stack or uses a third-party API, or whether the solution may sit on the client side, the server side, or both. What is the best way to do this?
A good answer: A good answer proposes one or more concrete, new or non-obvious approaches. Each must state three things:
- which request-change cases it covers: middle edit, insertion, tool output, document reordering;
- its expected hit rate and cost change, with the reasoning or a quantitative estimate;
- its effect on output quality compared with full recomputation, and how that effect could be tested.
Each approach must also say where it can run (client only, own serving stack, or provider-side) and what it costs in memory, storage and latency. It must be checked against existing prior art and say what it adds. It must state honestly which cases cannot reach about 100% under the stated constraints.
Constraints: 
- No retraining or fine-tuning of the model.
- Target hit rate close to 100% across non-identical prefixes.
- Much lower cost than current prefix caching.
- Nothing else was stated.

Below are 4 candidate ideas. You are a screening engineer with tools: WebSearch (WebFetch may not reach hosts; use
search excerpts) and Bash with python3 (pip install from PyPI works). Do not improve or redesign the ideas; judge them
as written. Work only in `/home/user/SomeRepository/engine/runs/v6_ctxcache/eval_g2/c1/`: write files only there, do not commit.

For EACH idea, spend about 3 minutes:
1. KILLER: the single quantity most likely to kill the idea at the scale it needs (a rate, a memory or bandwidth
   budget, an error or quality loss, a strength, a tolerance over the operating time, a condition that must hold).
   Compute what is REQUIRED and what is AVAILABLE from measured data or exact arithmetic, with a source for each
   decisive input. If the quantity can be measured by running code, measure it, after checking the measurement once
   on a case with a known answer. MARGIN = available / required (1 = just works, 0.1 = fails by 10x, 5 = five times
   headroom).
2. CHAIN: the gain the question asks for (cost, memory, speed, error per unit of the final product or service) with
   the idea, against the BEST current practice a competent practitioner would use, over the whole system rather than
   one part. Use the ledger below for the current structure. RATIO = current / with the idea (larger is better).
Ground every decisive input in a source or a measurement, not in the idea's own text.

Facts already collected for this question (data; check a decisive one before relying on it, and search only for
what is missing):
(a slice: all 0 HARD facts and the 12 of 25 other facts that bear most on these candidates, sources omitted; the full ledger with sources is /home/user/SomeRepository/engine/runs/v6_ctxcache/evidence.md - read it if you need a source or a fact that is not here)
FACT 1: Claude Code now has separate cache TTL settings for the main conversation and for subagents (`promptCacheTtl`, `subagentPromptCacheTtl`, v2.1.242 or later). It falls back to 5 minutes when usage credits are billed. A 1-hour write costs 2x base input. So per-gap TTL control is partly shipped already | NEW from eval_g0, check before relying on it
FACT 2: The usage API already splits writes into `ephemeral_5m_input_tokens` and `ephemeral_1h_input_tokens`, so f can be measured on the client | NEW from eval_g0, check before relying on it
FACT 4: Two 2026 preprints report that CacheBlend's quality degrades at longer contexts or multi-hop questions: FusionRAG says a "significant gap remains" against full attention; Decoupled Attention Fusion reports "severe accuracy degradation at longer contexts" | NEW from eval_g0, check before relying on it
FACT 5: Replay of hash-canonical top-5 RAG ordering (100k-chunk corpus, Zipf exponent 1.05–1.5): exact-prefix document-token reuse is only 15–50%. This is the ceiling the canonical-ordering stage gives before any blending | NEW from eval_g0, check before relying on it
FACT 6: In an exact recomputation (100k context, 1k new suffix, Anthropic multipliers), a uniform-position edit costs 6.11x a fully cached turn and a 200-token erratum costs 1.022x | NEW from eval_g0, check before relying on it
FACT 12: In my recomputation, the idea's own 50-turn model gives cached reads at 63.3% of the bill, writes 22.9% and output 13.8% (the idea says 60.5%, 26.3% and 13.2%); the conclusion is the same | NEW from eval_g0, check before relying on it
FACT 14: The automatic prefix check looks back only about 20 content blocks from each explicit breakpoint. A request may carry at most 4 breakpoints, and the docs suggest an extra breakpoint for content more than 20 blocks back. Anthropic now also offers a top-level automatic cache_control. | NEW from eval_g0, check before relying on it
FACT 15: Third-party guides say consecutive tool_result blocks may count as a single lookback position. If that holds, the "more than 20 parallel tool results" trigger becomes even rarer. This is not confirmed in the official docs. | NEW from eval_g0, check before relying on it
FACT 19: Close prior art not cited by the idea: PatchKV (an analytic RoPE fix for edited contexts) and HYPIC (fixed-width seam recompute for hybrid-attention models). The ChunkKV repo reports that selective recompute did not match full recompute on its test model. | NEW from eval_g0, check before relying on it
FACT 20: Replay of Mooncake's FAST25 traces with 512-token blocks: exact-prefix token hit rate with infinite TTL is 0.374 (conversation) and 0.571 (tool agent); with a 5-minute TTL it is 0.293 and 0.529. The input-cost ceiling of perfect TTL over 5 minutes is 1.112x and 1.081x. The traces cover only about 0.98 h, so gaps longer than that are cut off | NEW from eval_g1, check before relying on it
FACT 21: Breakpoint limit and TTL cost: limiting cache writes to 4 breakpoints costs 0.01–0.07 of reuse at 1k requests per 5 minutes. At 10 requests per 5 minutes, reuse falls to 0.05–0.42 and the method loses money at Zipf ≤ 1.2. The break-even reuse is 0.217 | NEW from eval_g1, check before relying on it
FACT 23: In Mooncake's traces, the only tokens expiry makes you rewrite are 8.0% (conversation) and 4.2% (tool agent) of input tokens; this is the most any TTL or keep-alive scheme can recover | NEW from eval_g1, check before relying on it

Notes from the user and about the environment (data; the user may be wrong):
The asker means context caching as offered by LLM APIs (prompt caching), seen from the side of whoever runs the model, and wants the cost of reused context to fall a lot with a cache hit rate near 100%. Two earlier runs on this topic found: (1) exact prefix caching with CPU/SSD tiers (vLLM/SGLang + LMCache, HiCache, Mooncake) is current practice and adds only ~1.2x over GPU-only prefix caching on real chat traces; (2) KV compression without retraining bottoms out at ~2.6-3 bits per value (~6x vs BF16, ~1.5-1.7x vs NVFP4). Environment: huggingface.co and its CDN are blocked here, so model weights cannot be downloaded and quality cannot be measured on a real model; PyPI and raw.githubusercontent.com work (public traces such as Mooncake's can be replayed). Use exact arithmetic, trace replays and published measurements, and say which numbers would need a run on a real model.
Assumptions in the question that may be wrong:

- "Practically 100% hit rate" is achievable for non-prefix changes without any quality loss. Reused KV that was computed in a different context may not equal what full recomputation would give.
- The asker can change the caching layer. This holds only for self-hosting or provider-side work, not for a plain API user.
- Cost is dominated by input-token processing. Output tokens, cache-write premiums and TTL expiry may matter as much.
- A hit rate near 100% and a much lower price can both be achieved at once. They may trade off against each other.
- "Context caching" and "prompt caching" refer to the same thing. Some providers also sell explicit context caching with a separate storage fee.
Where deciding data may exist:
Open benchmarks and code are the likely decision data. They include the CacheBlend and EPIC papers' benchmarks (multi-hop QA, RAG) and the LMCache and vLLM open-source repositories. Others are agent and tool-use traces (for example SWE-style agent logs) for measuring real prefix-divergence patterns, and provider usage fields (cached_tokens, cache_read_input_tokens) for measuring hit rates.

Ledger: where the cost or the defect comes from (data):
KIND: cost

Method: the shares for A come from one developer's measured bill. The shares for B and C are my own calculations from list prices and stated assumptions, not measurements. Prices are Claude Sonnet list prices: $3.00/MTok input, $3.75 cache write (1.25x), $0.30 cache read (0.1x), $15 output.

ARCHETYPE A: Long-running tool-using agent (Manus or Claude Code style). Best practice is an append-only context, a stable system prompt with no timestamps, deterministic tool serialization, and explicit cache breakpoints. | cost about $0.58 per MTok of input at a 92% hit rate, against $3.00 uncached (about 5x cheaper, from my arithmetic) | the target is a hit rate close to 100%, and the floor is $0.30 per MTok
SHARES: cache write 47% | cache read 42% | fresh uncached input 1% | other (output tokens) 10%
LARGEST: cache write - a 10x cut of it removes 42% of the cost
- These shares are the bill of one heavy Claude Code user over 3.44B tokens. Cache traffic was 89% of the bill.
- The hit rate is already high. Requesty gateway data for April 2026 shows Claude Code at 92%, OpenCode at 89% and Kilo Code at 46%.
- Manus reports an input-to-output ratio of about 100:1. It calls hit rate the most important production metric.
- The remaining cost is the write premium on every new suffix, plus cache expiry (5 minutes by default).
- The "write" term is the 1.25x charge on tokens that are new on each turn. Higher hit rates barely change it.

ARCHETYPE B: RAG or document Q&A through a third-party API. Best practice is system prompt and instructions first, retrieved chunks sorted into a canonical order, and the question last. | cost about $0.0174 per request (my calculation) | the target is below $0.007 per request
Assumptions: 1k system tokens cached, 4k retrieved-document tokens uncached, 0.2k question tokens, 0.3k output tokens.
SHARES: retrieved-document input 69% | question input 3% | system prompt (cache read) 2% | other (output) 26%
LARGEST: retrieved-document input - a 10x cut of it removes 62% of the cost
- Exact-prefix caching cannot serve this term when chunk sets or orders vary.
- With n chunks there are n! possible orders.
- One paper projects the hit rate "asymptotes to 0%" as fragment length grows.
- Reordering chunks to share prefixes (CacheWeaver) cuts TTFT by only 20–33%.
- The documented API discounts are OpenAI at 50% (up to 90% in its cookbook) and Anthropic at 90%. All of them need an identical prefix of at least 1,024 tokens.

ARCHETYPE C: Self-hosted RAG or multi-turn serving on vLLM or SGLang. Best practice is automatic prefix caching plus prefix-aware routing, with LMCache offload for the KV cache. | cost is GPU-seconds per request. I have no sourced dollar figure. | the target is a 2–3x cut in prefill GPU time
SHARES (assumed, not sourced): prefill compute 55% | decode compute 25% | KV storage and transfer 5% | scheduling and idle 5% | other 10%
LARGEST: prefill compute - a 10x cut of it removes 50% of the cost
- Routing alone raised the KV hit rate from about 25% to 82% in one SageMaker test. That test used a long shared prefix, not production RAG.
- Position-independent reuse is the only route to a high hit rate when the middle of the prompt changes.
  - CacheBlend cuts TTFT 2.2–3.3x and raises throughput 2.8–5x by recomputing about 15% of tokens. Its authors report no quality loss.
  - Naive full reuse of independently cached chunks drops F1 by up to 55% on Musique, because cross-chunk attention is missing.
  - I found no independent replication of CacheBlend's quality claim.

STATES (the cases where the saving must hold, worst first):
- Reordered or varying document sets.
- Middle insertion or edit.
- A changed tool output early in the context.
- Cache expiry between calls (5 minutes by default).
- Traffic spread over many replicas.
- Contexts of 100k+ tokens, where KV storage costs the most.

SOURCES:
- https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching
- https://openai.com/index/api-prompt-caching
- https://developers.openai.com/cookbook/examples/prompt_caching_201
- https://manus.im/en/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus
- https://levelup.gitconnected.com/89-of-my-coding-agent-bill-was-cache-traffic-and-most-token-saving-tools-cannot-reach-it-a5c6eb314c9e
- https://www.requesty.ai/data/coding-agent-cache-hit-rate-apr-2026
- https://arxiv.org/pdf/2511.02749
- https://arxiv.org/pdf/2601.12904
- https://blog.lmcache.ai/2025-03-31-eurosys
- https://arxiv.org/html/2404.12457v1

Ceilings computed from the ledger (data):
Target: 3x cheaper. Ceiling = 1 / (share no engineering can touch: taxes, royalties, fees, margins). 'needs' = the fewest cost terms that must each fall 10x to reach the target.
ARCHETYPE A: Long-running tool-using agent (Manus or Claude Code style). Best practice is an append-onl | untouchable 10.0% -> ceiling 10.0x | 10x cut of one term: cache write 1.73x; cache read 1.61x; fresh uncached input 1.01x | 3x needs: cache write, cache read | ROOM
ARCHETYPE B: RAG or document Q&A through a third-party API. Best practice is system prompt and instruct | untouchable 26.0% -> ceiling 3.8x | 10x cut of one term: retrieved-document input 2.64x; question input 1.03x; system prompt 1.02x | 3x needs: impossible even with every term cut 10x | NO ROOM
ARCHETYPE C: Self-hosted RAG or multi-turn serving on vLLM or SGLang. Best practice is automatic prefix | untouchable 10.0% -> ceiling 10.0x | 10x cut of one term: prefill compute 1.98x; decode compute 1.29x; kv storage and transfer 1.05x; scheduling and idle 1.05x | 3x needs: prefill compute, decode compute | ROOM

VERDICT: ALIVE if MARGIN >= 1 and RATIO >= 1.5; DEAD if MARGIN < 0.3 or RATIO < 1.1; otherwise WOUNDED.
Be strict and fair: a beautiful idea that fails by 10x is DEAD; a dull idea with headroom is ALIVE.

Final answer (text only), exactly this format, one block per idea in the order given:
=== GATE ===
IDEA 1: <name>
KILLER | <quantity> | required <value unit> | available <value unit> (<source>) | MARGIN <number>
CHAIN | <best current practice> | now <value unit> | with idea <value unit> | RATIO <number>
VERDICT | <ALIVE/WOUNDED/DEAD> | <one sentence>
NEW FACT | <any hard, sourced fact you found that the ledger did not contain> | <source> (optional, any number)
(same for the other ideas)

THE 4 IDEAS:
IDEA 1
NAME: Reuse-gated single-breakpoint document ordering
MECHANISM: The client orders retrieved documents by an online retrieval-frequency counter, with ties broken by ID. From each document's counter rate λ, it estimates P(reuse within TTL) = 1−e^(−5λ). It places one cache breakpoint after the last document with P > 0.217 (the break-even), and sends the rest after the breakpoint uncached at 1.0x instead of a 1.25x write. Exact prefix KV means output equals full recompute for that order; the reorder effect is tested by F1/EM across order permutations on a real model.
VALUE: Estimated 1.33x, 1.50x and about 1.9x per request at Zipf 1.05, 1.2 and 1.5, client-only through third-party APIs, with one breakpoint and no money-losing writes at low traffic; tail documents still miss, so about 100% hit is out of reach.

IDEA 2
NAME: Per-session TTL switch from return hazard
MECHANISM: The client measures, per session, s (the share of turns that come back after a 5–60 minute gap) and n/P (tokens written per turn divided by the cached prefix). It uses the 1-hour TTL when s > s* = 0.75n/(1.15P). Otherwise it uses the 5-minute TTL with a 1-token keep-alive read sent only while the return probability exceeds 0.08 per window. Prior art is Claude Code's static `promptCacheTtl`/`subagentPromptCacheTtl` (5m or 1h per request type, about v2.1.243). What this adds is choosing the TTL per session from measured s and n/P. Input-bill ratios: - Long agent session (100k prefix, 2k tokens per turn, s* = 0.013): 1.15x at s = 0.02 and 1.71x at s = 0.10 against plain 5-minute TTL. It matches a blanket 1-hour TTL there. - Short-prefix sessions with large writes (s* = 0.33): 1.40–1.52x cheaper than a blanket 1-hour TTL. On the Mooncake traces the measured rewrite share is f = 0.09–0.11, so the ceiling there is only 1.07–1.10x. It covers no edit cases, only expiry. Output is byte-identical, so there is no quality risk. It runs client-only with zero added latency.
VALUE: 1.0–1.5x on input against the best static TTL choice. The gain is large only for sessions with real 5–60 minute pauses, and nothing on short-gap traffic. This is the smallest honest version: it cannot make edited or reordered context cheaper.

IDEA 3
NAME: Popularity order with second-sighting cache writes
MECHANISM: Documents are still sent in order of descending global retrieval count from an online counter (ties broken by ID), with the system prompt first and the question last. Every hit is therefore an exact prefix match and the cached state is exact. Two changes fix the weak link. (1) Second-sighting admission. The client keeps a list of document-prefix hashes it has seen recently, with no cached state behind them. A cache breakpoint is placed only at prefix depths already seen within the TTL window. Documents past that depth go after the last breakpoint and are billed at 1.0x instead of a 1.25x write. This is the CDN "cache on second hit" / TinyLFU admission idea applied to breakpoint placement. (2) TTL by traffic regime. The 1-hour TTL (2x write cost) is used when the organisation sends fewer than about 1k requests per 5 minutes, and the 5-minute TTL otherwise. Replay setup: 100k chunks, top-5, Zipf, 4 breakpoints at document depths 2–5, Anthropic multipliers, compared with sending documents uncached. Bill ratios across 10 to 1,000 requests per 5 minutes: - Zipf 1.05: 1.06–1.24x - Zipf 1.2: 1.19–1.44x - Zipf 1.5: 1.46–1.83x The old always-write rule gave 0.88–1.61x and lost money at low traffic. The method now never loses in any tested regime, and 1.5x holds at Zipf 1.5 from about 100 requests per 5 minutes (1.66x), where the old rule needed about 1k. It covers document reordering only. Quality effect: only the reordering itself. Test it by comparing F1/EM and the spread across permutations against relevance order on a real model.
VALUE: 1.06–1.83x cheaper per request than the best current API practice (documents uncached), with no approximated KV, and it runs client-side only. It no longer loses money at low traffic or flat popularity. Rarely retrieved documents still miss (23–60% of document tokens), so a hit rate near 100% is not reachable.

IDEA 4
NAME: Shared-prefix hazard keep-alive
MECHANISM: An org-wide counter gives each popularity-ordered document-prefix path an arrival rate, which serves as the hazard. Before each 5-minute expiry, the client sends a 1-token read of every leaf path whose P(hit before next expiry) × 1.25 > 0.1; one ping serves every user sharing that path. Output is unchanged because only exact prefixes are kept warm.
VALUE: Low-traffic organisations could approach the reuse that only ≥1k requests per window give today (from 0.05–0.42 toward 0.40–0.77), with each ping positive in expected value; the net gain needs a trace replay, and per-session gaps remain capped at about 1.1x.

