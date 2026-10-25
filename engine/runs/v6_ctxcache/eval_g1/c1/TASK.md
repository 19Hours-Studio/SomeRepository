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
as written. Work only in `/home/user/SomeRepository/engine/runs/v6_ctxcache/eval_g1/c1/`: write files only there, do not commit.

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
(a slice: all 0 HARD facts and the 12 of 19 other facts that bear most on these candidates, sources omitted; the full ledger with sources is /home/user/SomeRepository/engine/runs/v6_ctxcache/evidence.md - read it if you need a source or a fact that is not here)
FACT 1: Claude Code now has separate cache TTL settings for the main conversation and for subagents (`promptCacheTtl`, `subagentPromptCacheTtl`, v2.1.242 or later). It falls back to 5 minutes when usage credits are billed. A 1-hour write costs 2x base input. So per-gap TTL control is partly shipped already | NEW from eval_g0, check before relying on it
FACT 2: The usage API already splits writes into `ephemeral_5m_input_tokens` and `ephemeral_1h_input_tokens`, so f can be measured on the client | NEW from eval_g0, check before relying on it
FACT 3: Mooncake's layer-by-layer prefill streams each layer's KV while later layers are still computing, which hides the transfer. vLLM-Ascend sizes its prefetch window from the measured ratio of transfer time to compute time | NEW from eval_g0, check before relying on it
FACT 4: Two 2026 preprints report that CacheBlend's quality degrades at longer contexts or multi-hop questions: FusionRAG says a "significant gap remains" against full attention; Decoupled Attention Fusion reports "severe accuracy degradation at longer contexts" | NEW from eval_g0, check before relying on it
FACT 5: Replay of hash-canonical top-5 RAG ordering (100k-chunk corpus, Zipf exponent 1.05–1.5): exact-prefix document-token reuse is only 15–50%. This is the ceiling the canonical-ordering stage gives before any blending | NEW from eval_g0, check before relying on it
FACT 6: In an exact recomputation (100k context, 1k new suffix, Anthropic multipliers), a uniform-position edit costs 6.11x a fully cached turn and a 200-token erratum costs 1.022x | NEW from eval_g0, check before relying on it
FACT 10: CORVUS (synced file registry with only current contents injected) cut input tokens per task by 9–50% across four LLMs with comparable pass rates; 26% of file-read actions were repeats | NEW from eval_g0, check before relying on it
FACT 11: AgentDiet reports 21–36% total cost and 40–60% input-token reductions from trajectory pruning, in a different setup | NEW from eval_g0, check before relying on it
FACT 12: In my recomputation, the idea's own 50-turn model gives cached reads at 63.3% of the bill, writes 22.9% and output 13.8% (the idea says 60.5%, 26.3% and 13.2%); the conclusion is the same | NEW from eval_g0, check before relying on it
FACT 14: The automatic prefix check looks back only about 20 content blocks from each explicit breakpoint. A request may carry at most 4 breakpoints, and the docs suggest an extra breakpoint for content more than 20 blocks back. Anthropic now also offers a top-level automatic cache_control. | NEW from eval_g0, check before relying on it
FACT 15: Third-party guides say consecutive tool_result blocks may count as a single lookback position. If that holds, the "more than 20 parallel tool results" trigger becomes even rarer. This is not confirmed in the official docs. | NEW from eval_g0, check before relying on it
FACT 19: Close prior art not cited by the idea: PatchKV (an analytic RoPE fix for edited contexts) and HYPIC (fixed-width seam recompute for hybrid-attention models). The ChunkKV repo reports that selective recompute did not match full recompute on its test model. | NEW from eval_g0, check before relying on it

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
NAME: Priced prefix-preserving client
MECHANISM: Runs client-only, against any API. The client fits a survival curve over the idle gaps of each session. It sends a 1-token keep-alive read only when P(return) × 1.25 × prefix exceeds 0.1 × prefix. Instead of editing earlier content in place, it appends errata that reference the original span, so the cached prefix never changes. It compacts and rewrites the prompt only when the accumulated errata cost more than one rewrite.
VALUE: Edited turns cost about 1.02× instead of 6.11× a cached turn, which together with keep-alive gives about a 2.4× lower bill with no server changes.

IDEA 2
NAME: Popularity-first exact-prefix document ordering
MECHANISM: Remove the blending stage, which is the part later papers dispute. Order retrieved documents by descending global retrieval frequency, using an online counter with ties broken by ID. Put the system prompt first and the question last. Every reuse is then an exact prefix hit, so the reused KV equals what full recomputation would give for that order. The only quality effect is the reorder itself. Stable-RAG reports that answers change with document order even under 1k tokens. To test it, run the same retrieved sets in relevance order and in popularity order and compare F1/EM and the spread across permutations (needs a real model). I replayed the same setup as FACT 5 (100k chunks, top-5, Zipf). Exact document-token reuse is 0.400, 0.546 and 0.768 at Zipf 1.05, 1.2 and 1.5. Hash order gives 0.152, 0.229 and 0.503; relevance (random) order gives 0.166, 0.249 and 0.425. A cache-aware trie-greedy order like CacheWeaver's gives 0.403, 0.548 and 0.769, the same as the counter. Because the counter needs no view of the cache, the method runs client-side through a third-party API. Under Anthropic's multipliers, the per-request bill is 1.17x, 1.35x and 1.78x cheaper than the usual practice of sending documents uncached. Caching documents only pays once reuse is above 0.217; hash order plus cache_control actually loses (0.95x). Self-hosted, the gain is 1.17x, 1.26x and 1.43x. Limits: per-document breakpoints (at most 4 per request), a 1,024-token minimum prefix, traffic arriving within the 5-minute TTL, and an LRU cap of 20k tree nodes that costs at most 1.4 points of reuse. Covers document reordering only.
VALUE: 1.2–1.8x per request against the best current API practice, without approximating any KV, and it works for API users. This is the smallest honest version; the old 5–10x needed blending. The advance over CacheWeaver is that a stateless counter matches its trie-greedy order, so no cache state is needed. Long-tail documents (23–60% of document tokens) still miss, so about 100% is not reachable.

IDEA 3
NAME: Canonical-prefix fallback for blended KV
MECHANISM: Runs on your own stack or provider-side. Spans are stored by content hash in a rolling-hash, position-independent KV store and repaired with EPIC/CacheBlend. Retrieved documents are sorted canonically first, so 15–50% of tokens become lossless exact-prefix hits. When the shadow-KL gate rejects a blended request, it is recomputed only after the last canonically matched document, not from the start.
VALUE: The quality loss from blending is confined to the non-canonical remainder, raising the recovered multi-source gap to about 0.6–0.77, and exact fallback costs 50–85% of full prefill instead of 100%.

IDEA 4
NAME: Hazard-gated keep-alive as TTL guard
MECHANISM: Client-only and the same rule as before: send a 1-output-token read of the prefix just before the 5-minute expiry only if P(return in the next window) × 1.25 > 0.1, which is a break-even hazard of 0.08. It is fitted per account from the `ephemeral_5m_input_tokens` and `ephemeral_1h_input_tokens` usage fields. What changed is the deciding number: it is now measured rather than assumed. I replayed Mooncake's public 1-hour conversation and tool-agent traces at the request level; one ping refreshes the whole prefix. f is **0.114 and 0.089**, not 0.4. Even if every rewrite became a free read, the ceiling is 1.096x and 1.069x. The chance that a session comes back after 5 minutes of idling is about 0.002 per window, far below 0.08. So the rule correctly sends no pings and lands at 1.00x. The alternatives lose money: one fixed keep-alive ping gives 0.97x and 0.93x, three pings give 0.83x and 0.75x, and a blanket 1-hour TTL gives 0.736x and 0.732x. Against the blanket 1-hour TTL, the rule is 1.36–1.37x cheaper. It has no effect on output.
VALUE: The weak link cannot be fixed: f is 0.09–0.11, nowhere near the 0.8 needed. Against plain 5-minute caching the rule gains 1.07–1.10x at most. Its honest value is as a guard: it avoids the 1.36x overpay of a blanket 1-hour TTL and the 1.03–1.34x overpay of fixed keep-alive scripts, at zero quality cost. Claude Code already ships manual TTL settings, which reduces what is new. Human-in-the-loop coding sessions may return more often than these traces show; per-account usage logs would show that.

