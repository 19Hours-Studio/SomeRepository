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
as written. Work only in `/home/user/SomeRepository/engine/runs/v6_ctxcache/eval_g0/c2/`: write files only there, do not commit.

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
(none recorded)

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
NAME: Erratum-append discipline with rebase-on-cold
MECHANISM: Client-only, so it works on any API (Anthropic: reads 0.1×, 5-minute writes 1.25×; OpenAI GPT-5: $0.125 cached vs $1.25 input). The context is append-only and serialized deterministically (sorted JSON keys, no timestamps up front, as in the Manus write-up). A middle edit or changed tool output becomes an appended erratum ("field X is now Y"), never an in-place change. Exact arithmetic for a 100k-token context: an in-place edit at a uniform position costs 6.78× a fully cached turn; an erratum costs 1.03×, a 6.6× saving per edit. Over 200 simulated turns with edits on 20% of them, total cost was 1.85× lower than in-place edits and within 4% of a context that never changes. The rule I add is to fold errata back into the context only when the cache is being rewritten anyway (TTL expiry, compaction), which costs nothing extra. A ski-rental rule never triggered in the simulation for 200-token errata. Quality caveat: the model uses the erratum reliably mainly with chain-of-thought (2606.17107). Without it, test erratum vs in-place on your own tasks and compare to a fresh prompt. That paper reports a 98.5% hit rate in an online vLLM benchmark.
VALUE: Hit rate near 100% and about 1.85× lower input cost for edit-heavy agents on any API. The floor is the provider's read price (0.1×); nothing client-side can go below it.

IDEA 2
NAME: Content-addressed position-independent KV with gated repair
MECHANISM: This runs on your own serving stack or on the provider side. Split token streams at content-defined boundaries: a rolling hash over token IDs plus message and tool delimiters. A re-sent span (a reordered document, a re-read file, a moved tool output, the text after an insertion) is then found at any offset with an O(1) hash lookup. Store keys before the positional rotation is applied, so reusing them at a new position is free inside the attention kernel. Repair in layers: recompute the first ~32 tokens of each chunk to remove the false attention-sink effect (EPIC), the top-r tokens by key deviation (CacheBlend), and a 16-token window after each splice point. Add a quality gate: on ε≈1% of traffic, run a full recompute in shadow, compare the next-token distributions (KL) on the first 32 output tokens, and adjust r per chunk type. Fall back to exact recompute when the gate fails. My model for 8×512-token chunks with a 1k system prompt in a new order on an 8B model, against full recompute: EPIC-only repair needs 8.4% of full compute, r=15% needs 15.6%, the full stack needs 23.2%, and r=30% for multi-hop needs 27.9%. Prefix caching here needs ~83% of full compute, because only the system prompt hits. Memory: 128 KiB of KV per token at 8B (320 KiB at 70B, so 328 GB per 1M tokens). Loading 4,096 reused tokens takes 10.7 ms over PCIe5 or 77 ms from NVMe, against ~152 ms for full prefill. The shadow check adds ε of full prefill.
VALUE: On reordered or re-positioned content, compute drops 3–10x against prefix caching, and token reuse rises from 19% to 74–92%. Prior art covers most of the parts: CacheBlend, EPIC, Cache-Craft, KVShare, SemShareKV, and LMCache's CacheBlend for agents. What this adds is offset-independent lookup plus a quality SLO with exact fallback. Quality is model-dependent. KVShareArena finds that repairs recover only half to two-thirds of the gap on multi-source questions, and that unrepaired caches can be worse than no cache. So "≈100% hit at full quality" is not reachable for multi-hop work. The deciding test is KL/F1 against full recompute on 2WikiMQA, MuSiQue and agent replays (needs a real model).

IDEA 3
NAME: Diff-encoded repeated tool outputs
MECHANISM: The client hashes every tool output it has already placed in context. When a file or command result is requested again, it appends only "unchanged since turn 12" or a unified diff, never a second full copy. This shrinks the genuinely new tokens that pay the 1.25x write charge. The closest prior art is the file-unchanged notices in some agents. Those cover only identical re-reads; this also handles changed outputs as deltas, so a changed tool output costs the size of its diff, not its full size. The deciding quantity is the share of written tokens that duplicate content already in context, measurable from agent traces. Quality should be tested by SWE-bench and Terminal-Bench pass rate and by error rates when applying diffs.
VALUE: Directly shrinks Archetype A's largest term, cache write at 47% of the agent bill, when re-reads dominate the written tokens.

IDEA 4
NAME: Cut the re-read bill, not misses
MECHANISM: This runs on your own stack or provider-side. Once hits are near 100%, re-reading cached context dominates. In my model of a 50-turn agent (20k base context, +2k tokens per turn, 300 output tokens per turn), cached reads at 0.1x are 60.5% of the bill, writes 26.3% and output 13.2%. Re-read cost grows with the square of the number of turns. So hold cached KV pages in CPU/SSD and fetch only the top-K pages per query (Quest-style min/max key bounds per page, no training) for decode and for attention from new tokens. With a 2–4k token budget, that reads 6.4–12.8% of the dense KV at 32k context and 1.6–3.2% at 128k. Page metadata adds about 6% of the KV size. Quest reports up to 7.03x faster self-attention and 2.23x lower latency, with negligible accuracy loss.
VALUE: This targets the largest remaining cost line at a near-100% hit rate. It could plausibly lower the per-token cost of cached reads by about 2–5x end to end. Providers could then price cached reads by pages actually touched. Quality risk is on retrieval-heavy long-range tasks. Test it with RULER/LongBench and agent replays against dense attention (needs a real model).

