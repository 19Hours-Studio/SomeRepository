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
