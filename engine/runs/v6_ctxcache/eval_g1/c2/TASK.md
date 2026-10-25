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

Below are 2 candidate ideas. You are a screening engineer with tools: WebSearch (WebFetch may not reach hosts; use
search excerpts) and Bash with python3 (pip install from PyPI works). Do not improve or redesign the ideas; judge them
as written. Work only in `/home/user/SomeRepository/engine/runs/v6_ctxcache/eval_g1/c2/`: write files only there, do not commit.

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
FACT 3: Mooncake's layer-by-layer prefill streams each layer's KV while later layers are still computing, which hides the transfer. vLLM-Ascend sizes its prefetch window from the measured ratio of transfer time to compute time | NEW from eval_g0, check before relying on it
FACT 4: Two 2026 preprints report that CacheBlend's quality degrades at longer contexts or multi-hop questions: FusionRAG says a "significant gap remains" against full attention; Decoupled Attention Fusion reports "severe accuracy degradation at longer contexts" | NEW from eval_g0, check before relying on it
FACT 5: Replay of hash-canonical top-5 RAG ordering (100k-chunk corpus, Zipf exponent 1.05–1.5): exact-prefix document-token reuse is only 15–50%. This is the ceiling the canonical-ordering stage gives before any blending | NEW from eval_g0, check before relying on it
FACT 6: In an exact recomputation (100k context, 1k new suffix, Anthropic multipliers), a uniform-position edit costs 6.11x a fully cached turn and a 200-token erratum costs 1.022x | NEW from eval_g0, check before relying on it
FACT 8: KV-Repurpose, a vLLM testbed: naive segment reuse holds up on single-document tasks but fails on cross-document reasoning | NEW from eval_g0, check before relying on it
FACT 12: In my recomputation, the idea's own 50-turn model gives cached reads at 63.3% of the bill, writes 22.9% and output 13.8% (the idea says 60.5%, 26.3% and 13.2%); the conclusion is the same | NEW from eval_g0, check before relying on it
FACT 14: The automatic prefix check looks back only about 20 content blocks from each explicit breakpoint. A request may carry at most 4 breakpoints, and the docs suggest an extra breakpoint for content more than 20 blocks back. Anthropic now also offers a top-level automatic cache_control. | NEW from eval_g0, check before relying on it
FACT 15: Third-party guides say consecutive tool_result blocks may count as a single lookback position. If that holds, the "more than 20 parallel tool results" trigger becomes even rarer. This is not confirmed in the official docs. | NEW from eval_g0, check before relying on it
FACT 16: 2609.17983 (Mao, Mackey, Lin, Sep 2026) uses a main budget of K=32 tokens. A contiguous window recovers ≥0.94 of the answer margin only when the dependent text is adjacent to the edit. | NEW from eval_g0, check before relying on it
FACT 18: 2606.17107: a field's own KV drives under 1% of the decision, because conclusions are written into downstream tokens during prefill. The paper finds a one-line appended correction cheap and robust, while top-K recompute is unreliable. | NEW from eval_g0, check before relying on it
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

THE 2 IDEAS:
IDEA 1
NAME: Probe-routed position-independent KV reuse
MECHANISM: Runs on your own serving stack or provider-side only; the claim to help third-party API users is dropped. Chunks are still found by content hash at any offset, keys are stored before the position rotation is applied, and the EPIC fix (recompute each chunk's first tokens), CacheBlend's top-r recompute and the seam-window recompute are kept. The change is in the gate. The old design ran a full shadow recompute on 1% of traffic. Instead, every request uses the layer-1 full recompute that CacheBlend already does to pick tokens to fix. If the share of tokens whose keys changed a lot across chunk boundaries passes a threshold (a sign that the question needs several sources), the blended result is thrown away. The request then takes the exact prefix-cache path, which costs a wasted 1/32 ≈ 3.1% of a full prefill on an 8B model. So multi-source requests get exact quality instead of the 0.53–0.6 repair that KVShareArena measured. Blending stays only on single-source requests, where KV-Repurpose finds plain segment reuse holds and CacheBlend reports 1–3% loss. Whole-bill ratio against prefix caching (self-hosted cost model from the earlier checks: 45% fixed + 55% prefill, blended path 24.2% of full compute, exact path 83% + 3.1%, plus the 1% shadow check): **1.52x** if 10% of requests are routed to exact recompute (m = 0.1), 1.43x at m = 0.2, 1.35x at m = 0.3 and 1.22x at m = 0.5. It stays at 1.5x or better only while m ≤ 0.12. Memory and transfer are unchanged: 128 KiB per token at 8B, and 4,096 tokens load in 10.7 ms over PCIe5. Covers reordering, moved or re-read tool outputs, and text after an insertion. A changed middle span is always recomputed.
VALUE: 1.2–1.5x lower whole bill than prefix caching, with exact quality on the requests the probe routes away. That is less than the old 1.64x, but the hardest multi-hop cases no longer carry the 0.53 repair risk. Two things are untested and need a real model: whether the probe catches the multi-source requests (2WikiMQA, MuSiQue, agent replays, compared with full recompute), and the real value of m. 2606.17107 warns that deviation-style signals can be unreliable. So "≈100% hit at full quality" is still out of reach for multi-hop work. Those requests become exact misses.

IDEA 2
NAME: SLO-gated canonical chunk blending
MECHANISM: Retrieved documents are sorted by stable ID so most reorders hit exactly. The remainder is assembled from per-chunk KV with a shared-system-prompt prefix (APE), plus EPIC and selective recompute. On 1% of traffic, a full recompute runs in shadow and the KL of the first 32 output tokens is compared. This learns the recompute ratio r per query type and document type, and routes the classes that fail, such as multi-hop, to exact recompute.
VALUE: The disputed multi-hop quality loss becomes a measured, bounded SLO, at about 0.42 of full compute even if 30% of traffic falls back, against 0.83 for prefix caching.

