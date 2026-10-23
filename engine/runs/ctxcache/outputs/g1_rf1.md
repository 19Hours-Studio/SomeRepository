**Where the gain is possible.** Own-stack prefill (D) and edit-heavy document sessions (C) have room for a 3× gain. RAG on a hosted API (B) tops out at about 2.8× because output decode is 28% of its cost.

**What cannot reach about 100%:**
- **Exact reuse after a middle change.** No training-free method keeps outputs bit-identical once content before a token changes.
- **Long-tail RAG queries on a closed API.** The only client-side lever there is the order of the prompt.

**Coverage, quality and placement:**

| Idea | Cases covered | Quality vs full recompute | Where it runs |
|---|---|---|---|
| Query-gated recompute | Insertions, reordering, tool outputs, middle edits | Bounded divergence, not exact | Own stack or provider |
| Popularity-ordered chunks | Reordering only | Exact KV; only document order changes | Client only |
| Append-only patches | Middle edits, tool-output replacement | Exact cache; the model must apply patches | Client only |

**How to test quality.** Compare each idea with full recompute on the same stack:
- token-level KL divergence and exact-match on HotpotQA and MuSiQue (multi-hop);
- multi-turn reuse of the same corrected cache;
- RULER at 32k–128k tokens;
- long reasoning outputs;
- models: Llama, Qwen, and one MLA or sliding-window model.

**Baseline.** vLLM or SGLang with LMCache and FP8 KV. KV storage is about 160 KiB per token for a 70B model at FP8, held in the same CPU or disk tiers that baseline already uses.

=== IDEAS ===
IDEA 1
NAME: Query-gated selective KV recompute
MECHANISM: Chunk KV is precomputed and stored in LMCache, then joined in any order. Layer by layer, the attention of the short query over the reused KV is computed, and only the tokens that carry the top attention mass are recomputed, stopping once the bound "attention mass on unrecomputed tokens × measured KV deviation" falls below ε. The closest prior art is CacheBlend, which picks about 15% of tokens by KV deviation without looking at the query, and Cache-Craft and EPIC, which use static or per-chunk rules. Gating on what the query actually reads aims at about 3% recompute, re-gating cheaply for each new query or turn and every N decode steps. The deciding quantity is the fraction of tokens needed to capture, say, 95% of the query's attention mass on multi-hop tasks.

VALUE: It makes about 97% of document tokens reusable at a stated divergence bound, cutting own-stack prefill on missed tokens about 5× more than CacheBlend, which takes 0.85 + 0.15 recomputed to about 0.03 + probe overhead (estimated 1.6–1.8× total cost in archetype D).

IDEA 2
NAME: Popularity-ordered chunk prefixes
MECHANISM: The client or router places retrieved chunks in a global order by corpus popularity rather than by relevance score. Overlapping chunk sets then share long exact prefixes, and the question goes last. This works on any hosted prefix cache, with zero extra memory or latency. The closest prior art is RAGCache and CacheWeaver, which are server-side and keep order sensitivity. This idea works client-only and keeps exact KV, so only the effect of document order needs testing, through an order-ablation test on lost-in-the-middle benchmarks. The deciding quantity is the Zipf skew of retrieval, which sets the probability that the first k chunks repeat across queries.

VALUE: In RAG on a closed API, it turns part of the 71% uncached document spend into 0.1× reads with no approximation. The hit rate is bounded by how much queries overlap, and the long tail stays uncovered.

IDEA 3
NAME: Append-only patch log
MECHANISM: Instead of editing a document or tool output in place, the client appends a compact diff, written as "replace lines X–Y with …", after the cached content. It compacts the prompt into a fresh write only when the patch tokens exceed a threshold such as 5% of the context. The closest prior art is Manus append-only discipline, which forbids edits rather than encoding them. The deciding quantity is how accurately the model applies the patches, tested as answer agreement against a rewritten document on edit-heavy QA.

VALUE: In archetype C, a 200-token mid-document edit costs 200 new tokens instead of a 1.25× rewrite of about 25k tokens, keeping cache hits near 100% between compactions on any hosted API.