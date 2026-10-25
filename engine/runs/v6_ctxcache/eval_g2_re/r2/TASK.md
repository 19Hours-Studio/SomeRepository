# Task: check the deciding numbers independently

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

For each idea below, an earlier check named the one quantity most likely to decide whether it works. Estimate that
quantity yourself, independently: what the idea REQUIRES at the scale it claims, and what is AVAILABLE, from measured
data or exact arithmetic, each with a source. You are not shown the earlier numbers on purpose. Tools: WebSearch
(WebFetch does not reach hosts here; use excerpts) and Bash with python3. About 3 searches per idea. Do not judge the
ideas otherwise and do not improve them. Work only in `/home/user/SomeRepository/engine/runs/v6_ctxcache/eval_g2_re/r2/`: write files only there, do not commit.

Facts collected for this question (data; check a decisive one before relying on it):
(a slice: all 0 HARD facts and the 12 of 31 other facts that bear most on these candidates, sources omitted; the full ledger with sources is /home/user/SomeRepository/engine/runs/v6_ctxcache/evidence.md - read it if you need a source or a fact that is not here)
FACT 1: Claude Code now has separate cache TTL settings for the main conversation and for subagents (`promptCacheTtl`, `subagentPromptCacheTtl`, v2.1.242 or later). It falls back to 5 minutes when usage credits are billed. A 1-hour write costs 2x base input. So per-gap TTL control is partly shipped already | NEW from eval_g0, check before relying on it
FACT 6: In an exact recomputation (100k context, 1k new suffix, Anthropic multipliers), a uniform-position edit costs 6.11x a fully cached turn and a 200-token erratum costs 1.022x | NEW from eval_g0, check before relying on it
FACT 19: Close prior art not cited by the idea: PatchKV (an analytic RoPE fix for edited contexts) and HYPIC (fixed-width seam recompute for hybrid-attention models). The ChunkKV repo reports that selective recompute did not match full recompute on its test model. | NEW from eval_g0, check before relying on it
FACT 20: Replay of Mooncake's FAST25 traces with 512-token blocks: exact-prefix token hit rate with infinite TTL is 0.374 (conversation) and 0.571 (tool agent); with a 5-minute TTL it is 0.293 and 0.529. The input-cost ceiling of perfect TTL over 5 minutes is 1.112x and 1.081x. The traces cover only about 0.98 h, so gaps longer than that are cut off | NEW from eval_g1, check before relying on it
FACT 21: Breakpoint limit and TTL cost: limiting cache writes to 4 breakpoints costs 0.01–0.07 of reuse at 1k requests per 5 minutes. At 10 requests per 5 minutes, reuse falls to 0.05–0.42 and the method loses money at Zipf ≤ 1.2. The break-even reuse is 0.217 | NEW from eval_g1, check before relying on it
FACT 23: In Mooncake's traces, the only tokens expiry makes you rewrite are 8.0% (conversation) and 4.2% (tool agent) of input tokens; this is the most any TTL or keep-alive scheme can recover | NEW from eval_g1, check before relying on it
FACT 26: Several third-party guides say Anthropic's cache has been isolated per workspace rather than per organization since 5 Feb 2026, so a cached prefix is shared only within one workspace (not confirmed in official docs) | NEW from eval_g2, check before relying on it
FACT 27: Replay with whole-request costs: always writing at 4 breakpoints gives 0.93–1.58x, so it loses money at 10 requests per 5 min with Zipf 1.05; second-sighting with the 5-minute TTL only gives 1.05–1.66x | NEW from eval_g2, check before relying on it
FACT 28: In a low-traffic organisation, a 5-document leaf path essentially never reaches 0.08 hit probability per 5-minute window (at 10–100 requests per 5 min, Zipf ≤ 1.2, 100k chunks), so leaf keep-alive does nothing | NEW from eval_g2, check before relying on it
FACT 29: Replay with 100k chunks, top-5 Zipf, 100k requests (checked first: identical requests give reuse 0.999). Doc-token exact reuse for hash order vs popularity order: s = 1.05 gives 0.201 vs 0.448 with infinite TTL and 0.100 vs 0.337 with a 1k-request window; s = 1.2 gives 0.295 vs 0.598 and 0.153 vs 0.477; s = 1.5 gives 0.607 vs 0.818 and 0.354 vs 0.696. Chunk-level KV hit, the condition the blended path needs: 0.65–0.98 | NEW from eval_g2, check before relying on it
FACT 30: Popularity ordering alone, with every request on the exact path (m = 1), gives 1.14–1.33x on the whole bill over hash-canonical prefix caching. If a competent baseline already sorts chunks by popularity, the probe and blending stages add only about 1.1–1.2x on top | NEW from eval_g2, check before relying on it
FACT 31: These numbers still need a run on a real model, which is blocked here because huggingface.co is unreachable: probe recall, and blended-path F1 against full recompute on 2WikiMQA/MuSiQue and on contexts of 32k tokens or more | NEW from eval_g2, check before relying on it

Final answer (text only), one line per idea in the order given:
=== RECHECK ===
IDEA 1: <quantity> | required <number unit> (<source>) | available <number unit> (<source>) | MARGIN <available / required, a number>
(same for the other ideas)

THE 5 IDEAS:
IDEA 1
NAME: Reuse-gated single-breakpoint document ordering
MECHANISM: The client orders retrieved documents by an online retrieval-frequency counter, with ties broken by ID. From each document's counter rate λ, it estimates P(reuse within TTL) = 1−e^(−5λ). It places one cache breakpoint after the last document with P > 0.217 (the break-even), and sends the rest after the breakpoint uncached at 1.0x instead of a 1.25x write. Exact prefix KV means output equals full recompute for that order; the reorder effect is tested by F1/EM across order permutations on a real model.
VALUE: Estimated 1.33x, 1.50x and about 1.9x per request at Zipf 1.05, 1.2 and 1.5, client-only through third-party APIs, with one breakpoint and no money-losing writes at low traffic; tail documents still miss, so about 100% hit is out of reach.
DECIDING QUANTITY: gate uses each document's own reuse probability, but a hit needs the whole prefix path (all earlier documents) to repeat

IDEA 2
NAME: Per-session TTL switch from return hazard
MECHANISM: The client measures, per session, s (the share of turns that come back after a 5–60 minute gap) and n/P (tokens written per turn divided by the cached prefix). It uses the 1-hour TTL when s > s* = 0.75n/(1.15P). Otherwise it uses the 5-minute TTL with a 1-token keep-alive read sent only while the return probability exceeds 0.08 per window. Prior art is Claude Code's static `promptCacheTtl`/`subagentPromptCacheTtl` (5m or 1h per request type, about v2.1.243). What this adds is choosing the TTL per session from measured s and n/P. Input-bill ratios: - Long agent session (100k prefix, 2k tokens per turn, s* = 0.013): 1.15x at s = 0.02 and 1.71x at s = 0.10 against plain 5-minute TTL. It matches a blanket 1-hour TTL there. - Short-prefix sessions with large writes (s* = 0.33): 1.40–1.52x cheaper than a blanket 1-hour TTL. On the Mooncake traces the measured rewrite share is f = 0.09–0.11, so the ceiling there is only 1.07–1.10x. It covers no edit cases, only expiry. Output is byte-identical, so there is no quality risk. It runs client-only with zero added latency.
VALUE: 1.0–1.5x on input against the best static TTL choice. The gain is large only for sessions with real 5–60 minute pauses, and nothing on short-gap traffic. This is the smallest honest version: it cannot make edited or reordered context cheaper.
DECIDING QUANTITY: share of input tokens that cache expiry forces you to rewrite (the most any TTL choice can recover)

IDEA 3
NAME: Popularity order with second-sighting cache writes
MECHANISM: Documents are still sent in order of descending global retrieval count from an online counter (ties broken by ID), with the system prompt first and the question last. Every hit is therefore an exact prefix match and the cached state is exact. Two changes fix the weak link. (1) Second-sighting admission. The client keeps a list of document-prefix hashes it has seen recently, with no cached state behind them. A cache breakpoint is placed only at prefix depths already seen within the TTL window. Documents past that depth go after the last breakpoint and are billed at 1.0x instead of a 1.25x write. This is the CDN "cache on second hit" / TinyLFU admission idea applied to breakpoint placement. (2) TTL by traffic regime. The 1-hour TTL (2x write cost) is used when the organisation sends fewer than about 1k requests per 5 minutes, and the 5-minute TTL otherwise. Replay setup: 100k chunks, top-5, Zipf, 4 breakpoints at document depths 2–5, Anthropic multipliers, compared with sending documents uncached. Bill ratios across 10 to 1,000 requests per 5 minutes: - Zipf 1.05: 1.06–1.24x - Zipf 1.2: 1.19–1.44x - Zipf 1.5: 1.46–1.83x The old always-write rule gave 0.88–1.61x and lost money at low traffic. The method now never loses in any tested regime, and 1.5x holds at Zipf 1.5 from about 100 requests per 5 minutes (1.66x), where the old rule needed about 1k. It covers document reordering only. Quality effect: only the reordering itself. Test it by comparing F1/EM and the spread across permutations against relevance order on a real model.
VALUE: 1.06–1.83x cheaper per request than the best current API practice (documents uncached), with no approximated KV, and it runs client-side only. It no longer loses money at low traffic or flat popularity. Rarely retrieved documents still miss (23–60% of document tokens), so a hit rate near 100% is not reachable.
DECIDING QUANTITY: document-token hit rate against the near-100% target

IDEA 4
NAME: Shared-prefix hazard keep-alive
MECHANISM: An org-wide counter gives each popularity-ordered document-prefix path an arrival rate, which serves as the hazard. Before each 5-minute expiry, the client sends a 1-token read of every leaf path whose P(hit before next expiry) × 1.25 > 0.1; one ping serves every user sharing that path. Output is unchanged because only exact prefixes are kept warm.
VALUE: Low-traffic organisations could approach the reuse that only ≥1k requests per window give today (from 0.05–0.42 toward 0.40–0.77), with each ping positive in expected value; the net gain needs a trace replay, and per-session gaps remain capped at about 1.1x.
DECIDING QUANTITY: cost of pings compared with the extra hits they buy

IDEA 5
NAME: Popularity-ordered probe-routed KV reuse
MECHANISM: On a self-hosted or provider stack, documents are ordered by global retrieval frequency before lookup. CacheBlend's layer-1 recompute measures cross-chunk key deviation; single-source requests are blended from position-independent chunk KV, and requests above the threshold take the exact prefix path. That exact path now hits the popularity-ordered prefix, cutting its cost from about 84.7 to 62–74 units against an 83-unit prefix-caching baseline.
VALUE: At m = 0.25 routed away, the whole bill falls 1.46–1.55x, and 1.5x holds up to m = 0.18–0.38 instead of 0.12; probe recall still needs testing on 2WikiMQA and MuSiQue against full recompute.
DECIDING QUANTITY: largest share m of requests the probe can send to the exact-prefix path while the whole bill still falls 1.5x

