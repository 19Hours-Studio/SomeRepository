**Bottom line:** under the "same outputs" reading, exact reuse stops at the first differing token. Middle edits, changed tool outputs and reordering can only be served by approximate reuse with a quality audit. Prefix-exact methods get there by changing the prompt layout, so the prompt itself differs. Nothing reaches ~100% hits at bit-identical output.

Deciding arithmetic, computed from your ledgers:

- **A:** reads cost 40 turns × 60k average context × $0.30/M ≈ $0.72, which is 54% of the cost. The only client-side lever is to read fewer tokens.
- **B:** the 28% decode share caps the gain at 3.6×.
- **D:** 8.3× is available. Prefill on missed tokens is the term to cut.

=== IDEAS ===
IDEA 1
NAME: Deviation-gated chunk KV reuse
MECHANISM: This runs on your own serving stack or provider-side. Store each chunk's KV computed once after the fixed system prompt, with positions shifted exactly by re-rotating RoPE at use. On each request, recompute only the tokens whose layer-1–3 key deviation exceeds a threshold, and send a 1–2% sample of requests to full recompute so the threshold adapts to keep first-token KL under budget. The closest prior art is CacheBlend, with a fixed ~15% recompute, and EPIC, which recomputes the first k tokens. Both are open-loop. This adds a measured, per-workload guarantee, and it can recompute less than 15% where chunks are independent. The deciding quantity is the recompute fraction needed to hold KL under budget. If it is ≤10%, uncached input falls to about 0.2× and B gets about 2.3× cheaper. The cost is FP8 KV at about 160 KiB/token for a 70B model, so about 1 GB per 6k tokens of documents on SSD. At about 10 GB/s that is about 0.1 s to load. Test this on multi-hop QA and RULER against full recompute.
VALUE: It covers reordering, insertion and changed tool outputs at a measured quality cost, cutting RAG and own-stack prefill cost about 2–3×. It cannot reach ~100% hits at exact outputs.

IDEA 2
NAME: Canonical-order exact prefix trees
MECHANISM: This is client-only. Emit retrieved chunks sorted by a stable corpus ID instead of by relevance, and put tool outputs into fixed slots. Any two queries that share their lowest-ID chunks then share an exact prefix in an SGLang radix tree or a provider prefix cache. The closest prior art is RAGCache and CacheWeaver, which reorder to fit the cache. This instead makes order a deterministic function of the chunk set, so all reuse is bit-exact. The deciding quantity is the chunk-set overlap between queries. The hit rate equals the shared-prefix fraction, so expect perhaps 30–60%, nowhere near 100%. Quality risk comes from losing relevance order ("lost in the middle"). A/B test sorted against relevance order on your own evaluation set.
VALUE: It gives exact, zero-approximation savings on reordering, with no storage or latency added.

IDEA 3
NAME: Append-patch history with stubbing
MECHANISM: This is client-only, for agent loops. Never edit the history in place. A middle change is appended as a patch, which keeps the cached prefix exact. Every 10 turns, take one deliberate cache-rewrite and replace tool outputs older than 5 turns with a short stub, keeping the full text retrievable by a tool call. The closest prior art is Manus's append-only discipline, which still re-reads the whole history every turn. This changes the read volume instead. The deciding quantity is the share of tool output in the history. At about 70%, average context falls from about 60k to about 25k, so reads drop about 2.4×. Net of 4 rewrite writes, that is about 1.5× cheaper per task. Quality is lossy. Test pass rate and re-fetch rate on SWE-bench against the unstubbed baseline.
VALUE: It covers middle edits and tool outputs on any hosted API, with about 1.5× lower cost for each long coding task.