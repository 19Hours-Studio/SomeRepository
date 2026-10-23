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

Below are 8 candidate ideas. You are a screening engineer with tools: WebSearch (WebFetch may not reach hosts; use
search excerpts) and Bash with python3 (pip install from PyPI works). Do not improve or redesign the ideas; judge them
as written. Work only in `/home/user/SomeRepository/engine/runs/ctxcache/gate/`: write files only there, do not commit.

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

Value ledger (data):
Token mixes are my own modelling assumptions, not measured data. The prices come from third-party sites (Anthropic's and OpenAI's own pages were not reachable), so check them against the providers' pricing pages. No source gave a cost split directly.

**ARCHETYPE A (coding agent, long tool-using session on Anthropic Sonnet):** a stable system prompt and tool block, a growing append-only history, and explicit cache breakpoints with the 5-minute or 1-hour TTL | cost ≈ $1.3 per 40-turn task (context 20k→100k, 2k new tokens and 0.5k output per turn). Anthropic's published average is about $13 per developer per active day | Sonnet $3 in / $15 out per million tokens; cache write 1.25×, cache read 0.1×.
SHARES: cache reads 54% | cache writes of new tool output 23% | uncached input ~0% | output decode 23% | other (output decode counted above, nothing else unaffected) 0%
Revised to sum to 100: cache reads 54% | cache writes 23% | uncached input 0% | other (output decode) 23%
LARGEST: cache reads - a 10x cut of it removes about 49% of the cost.

**ARCHETYPE B (RAG question answering, retrieved chunks vary in order and content per query):** short fixed system prompt cached by prefix, with documents placed after it and retrieved by similarity | cost ≈ $0.022 per answer (GPT-5.4-class pricing: $2.50 in / $0.25 cached / $15 out per million tokens; 1.2k cached prefix, 6.1k uncached docs and question, 0.4k output) | a 90% discount on cached input.
SHARES: cached prefix 1% | uncached document and query input 71% | other (output decode) 28%
LARGEST: uncached document input - a 10x cut of it removes about 64% of the cost.
Why it is large: exact-prefix caching only covers the shared prefix, because retrieved chunks arrive in varying order. CacheBlend-style reuse of non-prefix KV reports 2.2–3.3× lower TTFT, with about 15% of tokens recomputed. One paper argues approximate matching can hurt accuracy. CacheWeaver-style reordering reports 20–33% lower median TTFT.

**ARCHETYPE C (chat or Q&A over a 50k-token document, 10 questions per session, document sometimes edited or swapped):** the document goes first with a cache breakpoint, and questions are asked inside the TTL | cost ≈ $0.042 per question (Sonnet). The write is $0.1875 per session, amortized over 10 questions. Cache read is $0.015 per question, new input $0.0009, output $0.0075.
SHARES: cache write, amortized 44% | cache reads 36% | new uncached input 2% | other (output decode) 18%
LARGEST: cache write, amortized - a 10x cut of it removes about 40% of the cost.
If the session is shorter or the TTL lapses, writes dominate even more. A mid-document edit forces a fresh 1.25× write of everything after the edit.

**ARCHETYPE D (own serving stack: vLLM or SGLang with automatic prefix caching, 70B-class model on H100s, 8k-token prompts, 300 output tokens, LMCache-style CPU/disk offload as the best current practice):** the cost is GPU time, not tokens | cost ≈ $0.002–0.003 per request. This is my estimate: 2 H100s at about $2.5/GPU-hour, about 1 s of prefill and about 0.4 s of batched decode. It is unsourced, so measure your own.
SHARES: prefill compute on cache-missed tokens 55% | decode compute 25% | KV memory, offload and transfer 8% | other (idle capacity, margin, power overhead) 12%
LARGEST: prefill compute on missed tokens - a 10x cut of it removes about 50% of the cost.
Non-prefix reuse (CacheBlend) reports 2.8–5× higher throughput against full recompute. This archetype is where a new method could actually run.

**Reading across the archetypes:**
- For a competent practitioner on a hosted API, the cache hit rate is already high in append-only agent loops (A). Their remaining cost is cache reads and writes, which a better hit rate does not change.
- The unreduced cost is in B and D, where documents are reordered or inserted and the prefix cache misses.
- On a hosted API, a client-only trick cannot beat the 0.1× read price. Only a provider-side or own-stack change can.

SOURCES:
- https://www.morphllm.com/openai-api-pricing
- https://www.morphllm.com/claude-code-api-cost
- https://tkmxai.it.com/claude-api-cost-pricing-26 (listed as https://tkmxai.it.com/claude-api-cache-pricing-26)
- https://arxiv.org/abs/2405.16444v2 (CacheBlend)
- https://blog.lmcache.ai/2024-10-09-cacheblend/
- https://www.emergentmind.com/papers/2606.19667 (CacheWeaver)
- https://arxiv.org/html/2511.03475v1

Archetype A's SHARES line has two versions: the revised line is the one that sums to 100.

Ceilings computed from the ledger (data):
Target: 3x cheaper. Ceiling = 1 / (share no engineering can touch: taxes, royalties, fees, margins). 'needs' = the fewest cost terms that must each fall 10x to reach the target.
ARCHETYPE ? | untouchable 0.0% -> ceiling infx | 10x cut of one term: cache reads 1.95x; cache writes of new tool output 1.26x; output decode 1.26x; uncached input ~ 1.00x | 3x needs: cache reads, cache writes of new tool output | ROOM
ARCHETYPE ? | untouchable 28.0% -> ceiling 3.6x | 10x cut of one term: uncached document and query input 2.77x; cached prefix 1.01x | 3x needs: impossible even with every physical term cut 10x | NO ROOM
ARCHETYPE ? | untouchable 18.0% -> ceiling 5.6x | 10x cut of one term: cache write, amortized 1.66x; cache reads 1.48x; new uncached input 1.02x | 3x needs: cache write, amortized, cache reads | ROOM
ARCHETYPE ? | untouchable 12.0% -> ceiling 8.3x | 10x cut of one term: prefill compute on cache-missed tokens 1.98x; decode compute 1.29x; kv memory, offload and transfer 1.08x | 3x needs: prefill compute on cache-missed tokens, decode compute | ROOM

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

THE 8 IDEAS:
IDEA 1
NAME: Edits shipped as appended patches
MECHANISM: The client never rewrites earlier context. A changed document section or replaced tool output becomes a short appended note ("section 4 now reads: …; ignore the earlier version"), so the stored prefix stays identical and every earlier token is a cache read. The client rebuilds the prompt once patches exceed a set share of the context (for example 5%). The closest earlier attempt is append-only discipline (Manus), which stopped short because it forbids edits; this design keeps edits and changes only where they are written. Covers middle edits, insertions and tool-output replacement (not reordering), runs client-only on hosted APIs, and costs only the patch tokens. In C, rewriting after a mid-document edit drops from about $0.094 (25k tokens × 1.25 × $3/M) to about $0.002 for a 500-token patch. The deciding quantity is answer agreement between patched and inline prompts, which you can test with paired evaluations, including multi-hop questions that touch the edited text.
VALUE: Hosted-API document edits stay at nearly 100% cache hits without access to the server.

IDEA 2
NAME: Query-gated selective KV recompute
MECHANISM: Chunk KV is precomputed and stored in LMCache, then joined in any order. Layer by layer, the attention of the short query over the reused KV is computed, and only the tokens that carry the top attention mass are recomputed, stopping once the bound "attention mass on unrecomputed tokens × measured KV deviation" falls below ε. The closest prior art is CacheBlend, which picks about 15% of tokens by KV deviation without looking at the query, and Cache-Craft and EPIC, which use static or per-chunk rules. Gating on what the query actually reads aims at about 3% recompute, re-gating cheaply for each new query or turn and every N decode steps. The deciding quantity is the fraction of tokens needed to capture, say, 95% of the query's attention mass on multi-hop tasks.
VALUE: It makes about 97% of document tokens reusable at a stated divergence bound, cutting own-stack prefill on missed tokens about 5× more than CacheBlend, which takes 0.85 + 0.15 recomputed to about 0.03 + probe overhead (estimated 1.6–1.8× total cost in archetype D).

IDEA 3
NAME: Read-cost-gated turn collapsing
MECHANISM: Read cost grows with turns times context length. The agent is therefore prompted to emit multi-step scripts or batched tool calls, and to stop and observe only when the predicted branch uncertainty is worth one more full context read. The closest prior art is CodeAct and parallel tool calling, which aim at task success. This approach adds explicit gating on cost per read. The deciding quantity is how much task success drops at 2–3x fewer turns.
VALUE: It cuts the dominant cache-read term of long agent sessions by about 2x, beyond what any hit-rate gain can do.

IDEA 4
NAME: Drift-gated partial recompute
MECHANISM: On your own serving stack, after an edit, first recompute only the edited span plus a few early layers for the tokens after it. Measure how far each later token's hidden state moved compared with the cached version. Fully recompute only tokens above a threshold, and stop at layers where drift has died out. Full recomputation of 1% of requests checks the threshold against output agreement. The closest earlier attempt is CacheBlend, which stopped short at a fixed ~15% recompute with no quality bound; this design sets the recompute share per edit from measured drift and audits it. Costs: one extra early-layer pass, and stored states (~320 KiB per token at FP16 for a 70B model, half that at FP8). The deciding quantity is the share of post-edit tokens above threshold. At ≤5% it cuts prefill on edited requests about 10x, worth about 1.8x on D overall. Test it with greedy-output agreement, RULER and multi-turn tasks.
VALUE: Middle edits and tool-output swaps on your own stack cost close to the edited span, with a measured quality bound.

IDEA 5
NAME: Edits become appended patches
MECHANISM: A client wrapper never rewrites earlier context. It appends a short, structured patch such as "§3 of doc X now reads…" or "tool call 7 output superseded by…", so the cached prefix stays byte-identical. It covers middle edits, insertions and replaced tool outputs, with ~100% prefix hits. A full rewrite (compaction) runs only when the accumulated patch tokens make up more of the cost than one fresh write would. This differs from Manus append-only discipline, which forbids edits; here edits are allowed and converted into appends. The deciding quantity is how much answer accuracy the model loses when it reads patched text instead of clean text. Runs client-only, with no extra storage. In C, a mid-document edit drops from a ~25k-token 1.25× rewrite (~$0.09) to ~1k new tokens (~$0.004).
VALUE: Edit-heavy document and agent sessions on hosted APIs keep near-100% hits, saving 1.3–1.7× in those sessions, not across all traffic.

IDEA 6
NAME: Append-patch history with stubbing
MECHANISM: This is client-only, for agent loops. Never edit the history in place. A middle change is appended as a patch, which keeps the cached prefix exact. Every 10 turns, take one deliberate cache-rewrite and replace tool outputs older than 5 turns with a short stub, keeping the full text retrievable by a tool call. The closest prior art is Manus's append-only discipline, which still re-reads the whole history every turn. This changes the read volume instead. The deciding quantity is the share of tool output in the history. At about 70%, average context falls from about 60k to about 25k, so reads drop about 2.4×. Net of 4 rewrite writes, that is about 1.5× cheaper per task. Quality is lossy. Test pass rate and re-fetch rate on SWE-bench against the unstubbed baseline.
VALUE: It covers middle edits and tool outputs on any hosted API, with about 1.5× lower cost for each long coding task.

IDEA 7
NAME: Append-only patch log
MECHANISM: The client never edits earlier prompt text. It appends a compact patch instead, such as "doc X, §4 now reads …" or "tool output #12 is superseded by …", so the cached prefix stays byte-identical. Once the patches exceed a set fraction ε of the document, the client compacts them into one fresh cached copy. The closest prior art is Manus's append-only discipline, which forbids mid-prompt edits; this approach turns those edits into appends instead of forbidding them. The deciding quantity is how accurately the model applies patches as their number grows.
VALUE: Mid-document edits and replaced tool outputs no longer trigger 1.25× rewrites, so near-100% prefix hits are possible on hosted APIs with no model access.

IDEA 8
NAME: Deviation-gated chunk KV reuse
MECHANISM: This runs on your own serving stack or provider-side. Store each chunk's KV computed once after the fixed system prompt, with positions shifted exactly by re-rotating RoPE at use. On each request, recompute only the tokens whose layer-1–3 key deviation exceeds a threshold, and send a 1–2% sample of requests to full recompute so the threshold adapts to keep first-token KL under budget. The closest prior art is CacheBlend, with a fixed ~15% recompute, and EPIC, which recomputes the first k tokens. Both are open-loop. This adds a measured, per-workload guarantee, and it can recompute less than 15% where chunks are independent. The deciding quantity is the recompute fraction needed to hold KL under budget. If it is ≤10%, uncached input falls to about 0.2× and B gets about 2.3× cheaper. The cost is FP8 KV at about 160 KiB/token for a 70B model, so about 1 GB per 6k tokens of documents on SSD. At about 10 GB/s that is about 0.1 s to load. Test this on multi-hop QA and RULER against full recompute.
VALUE: It covers reordering, insertion and changed tool outputs at a measured quality cost, cutting RAG and own-stack prefill cost about 2–3×. It cannot reach ~100% hits at exact outputs.

