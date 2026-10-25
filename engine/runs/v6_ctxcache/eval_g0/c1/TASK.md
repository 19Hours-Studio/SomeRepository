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
as written. Work only in `/home/user/SomeRepository/engine/runs/v6_ctxcache/eval_g0/c1/`: write files only there, do not commit.

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
NAME: Return-hazard priced keep-alive
MECHANISM: The client logs the gaps between turns per user and per tool, including long test runs. From this it fits a survival curve, S(t) = the probability the user has not yet returned after t minutes. Just before a 5-minute expiry, it sends a 1-output-token read of the whole prefix only if the expected cost of rewriting (P(return soon) × 1.25 × prefix) exceeds 0.1 × prefix. It uses the 1-hour TTL only on the stable header when parallel sub-agents will read it. The closest prior art is fixed keep-alive scripts and the blanket 1-hour TTL. Those either ping dead sessions forever or pay +0.75× on every write, whereas this rule prices each gap. Deciding quantity: the share f of write tokens that are rewrites after expiry. If f = 0.4, the saving is about 15% of the bill (about 1.18×). It runs client-only and adds roughly zero latency; time-to-first-token after an idle gap also improves.
VALUE: It removes rewrites after expiry and during tool waits for about 0.1× per window, without changing output.

IDEA 2
NAME: Append-only journal with cost-optimal compaction
MECHANISM: This runs on the client only, works with any plain API, and is the only approach here that is exact. Never change earlier tokens. A middle edit or insertion becomes a short correction appended at the end ("§3.2 now reads …"). Tool outputs are never cut back in place. Documents go in a fixed order, sorted by content hash, and the relevance ranking is given in a short note at the end. Rewriting from the earliest edit point (compaction) happens only when a ski-rental rule says so: compact once the 0.1x re-read spend on accumulated corrections reaches (1.25−0.1)·(N−p_min). This rule is guaranteed to cost at most 2x the best possible schedule. My exact arithmetic for a 100k context with a 400-token edit at 30k: rewriting in place costs 90,500 base-token units, appending costs 10,500, so appending is 8.6x cheaper this turn and stays cheaper for 2,000 later turns. For idle gaps longer than the 5-minute TTL, a 1-token "keep-alive" request costs 0.1N against 1.25N for rewriting after a miss. That pays for up to 12.5 pings (about 62 minutes) if the user is sure to return, or 5.8 pings if the chance is 50%. A 1-hour write costs the same as 7.5 pings. On the cost side, there is no extra memory and no extra latency. The appended text adds a few hundred tokens per edit, re-read at 0.1x.
VALUE: Every request type becomes a pure prefix extension, so the hit rate equals 1 − (new tokens / total). That is typically 94–98% per agent turn. Against a client that edits in place, a single missed 10% of old context per turn adds 69% to the bill (35% at 5%). Quality risk: the model now sees the stale text plus a correction rather than a clean edit. Test it on your own evals (SWE-bench-style pass rate) and measure how often stale facts leak into answers, comparing journal against rewrite. This needs a real-model run.

IDEA 3
NAME: Attention at the KV store
MECHANISM: On each agent turn, only the new suffix is prefilled. The suffix's queries go to the node that already holds the session's prefix KV, and that node returns partial attention outputs with log-sum-exp values. These merge exactly with local attention over the suffix, so the KV never moves and the output matches full recomputation bit-for-bit up to floating-point order. Closest earlier work: Lamina (2024) offloads decode attention only; this applies the same split to suffix prefill. The deciding quantity is traffic, n·Hq/(L·Hkv) = 8n/L. It wins whenever the n new tokens are fewer than L/8, for example 2k new tokens over a 100k context gives about 6× less traffic than a BF16 fetch. Costs: 80 per-layer round trips per turn, and compute on the store node. It runs on your own stack or provider-side.
VALUE: Hits on 100k+ contexts become cheap from any replica without moving the KV. This lowers the provider's cost of cache reads (42% of the bill), but it does nothing for middle edits.

IDEA 4
NAME: Canonical ordering plus position-independent chunks
MECHANISM: Runs on your own stack or provider-side and covers reordered documents and RAG sets. First, sort retrieved documents and tool schemas by stable ID and popularity, so most reorders become exact prefix hits. Berkeley's relational-query reordering already shows this works, with up to 3.4× faster jobs and 32% lower cost under OpenAI and Anthropic pricing. For the rest, use a store of KV per chunk, computed once with the shared system prompt in front of it. APE showed this shared prefix removes the per-chunk attention-sink error with no training, keeping 93–98% of sequential-encoding quality. At assembly time, re-rotate positions exactly, recompute the first few tokens of each chunk (EPIC: up to 8× TTFT and 7× throughput, with negligible accuracy loss) and selectively recompute 10–15% of tokens (CacheBlend: 1–3% quality loss, 2.2–3.3× TTFT). Token hit rate is then about 85–90% for permuted sets and 100% for the canonical ones. Storage is one KV copy per chunk instead of one per prefix: 30.5 GiB per 100k tokens in BF16, about 6× less with roughly 3-bit compression. To test, compare answers under canonical, random and adversarial document orders against full recompute, which measures both the order effect and the blending error. Chunks must be isolated per tenant: HijackKV shows shared position-independent KV can be poisoned across users.
VALUE: Adding canonical ordering in front of CacheBlend/EPIC turns most reorders into lossless exact hits, so blending's 1–3% loss applies only to the remainder. Expect about 5–10× less prefill than prefix caching on RAG traffic where the document set varies.

