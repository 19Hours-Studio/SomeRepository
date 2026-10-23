**Bottom line:** under the stated constraints, a hit rate near 100% with outputs identical to full recomputation is impossible after a middle edit. A token's KV depends on every token before it, so only exact prefixes reuse losslessly. Each approach below either turns edits into appends, accepts measured approximation, or makes the stable prefix larger.

**Ceilings that bound the claims:**
- **B (RAG):** capped at 3.6×, so no answer reaches 3× on B.
- **A (coding agent):** client-side work cannot go below the 0.1× read price. A only gains where edits currently force rewrites.
- **D (own stack):** the main target is prefill on cache-missed tokens, 55% of cost.

**Quality test for all three:** compare against full recomputation on the same prompts.
- Exact-match or LLM-judge agreement.
- RULER and multi-hop QA (HotpotQA, MuSiQue).
- Multi-turn agent task success (SWE-bench-lite).
- Long reasoning.
- At least three model families, including one MLA or sliding-window model.

All numbers are estimates from the ledger and have not been measured.

=== IDEAS ===
IDEA 1
NAME: Edits become appended patches
MECHANISM: A client wrapper never rewrites earlier context. It appends a short, structured patch such as "§3 of doc X now reads…" or "tool call 7 output superseded by…", so the cached prefix stays byte-identical. It covers middle edits, insertions and replaced tool outputs, with ~100% prefix hits. A full rewrite (compaction) runs only when the accumulated patch tokens make up more of the cost than one fresh write would. This differs from Manus append-only discipline, which forbids edits; here edits are allowed and converted into appends. The deciding quantity is how much answer accuracy the model loses when it reads patched text instead of clean text. Runs client-only, with no extra storage. In C, a mid-document edit drops from a ~25k-token 1.25× rewrite (~$0.09) to ~1k new tokens (~$0.004).
VALUE: Edit-heavy document and agent sessions on hosted APIs keep near-100% hits, saving 1.3–1.7× in those sessions, not across all traffic.

IDEA 2
NAME: Cluster-pinned RAG context
MECHANISM: The corpus is clustered offline, and each cluster gets a fixed, ordered "hot set" of about 30k tokens that is cached once on the provider. Each query is routed to a cluster and its question appended after that cached prefix, so varying retrieval order no longer breaks the cache. Chunks outside the hot set are appended uncached. This extends cache-augmented generation (CAG), which preloads a whole small corpus, by routing per cluster so the method scales to large corpora. The deciding quantity is in-cluster recall: the fraction of needed chunks already inside the pinned set. Runs client-only. Estimated cost: 30k×$0.25/M + output ≈ $0.014 vs $0.022, about 1.6×. Quality risk is distraction from the longer context, tested with a RAG eval at matched recall.
VALUE: Hosted-API RAG gets near-100% hits despite reordering, but stays well under the 3.6× ceiling.

IDEA 3
NAME: Head-sparse blended recompute
MECHANISM: Chunk KV is cached by content hash and re-rotated to each new position, as in CacheBlend. An offline per-model profile finds which layers and heads actually attend across chunk boundaries. Selective token recompute (~15%) then runs only in those layers, not in all of them. EPIC and CacheBlend choose tokens; this also chooses layers, so the recompute fraction can multiply down (for example 15% × 30% ≈ 5%). If the measured KV deviation exceeds a set threshold, the request falls back to exact recompute. The deciding quantity is the fraction of layers that can be skipped at <1% loss against full recompute; residual-stream coupling between layers may make it small. Runs on an own stack or provider-side, with roughly prefix-cache-scale storage for chunk KV (FP8). The method is lossy and must be offered opt-in. In D, prefill on missed tokens falls by up to ~10×, giving ~1.9× overall.
VALUE: Reordered and inserted documents become cheap to reuse with a quality bound that is measured and can be enforced, and they bill near cache-read prices.