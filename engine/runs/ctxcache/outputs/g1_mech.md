Under these constraints, roughly 100% hits with output identical to full recomputation is impossible for middle edits and insertions. Every token after an edit attends to the edit, so its stored state really changes. Only appended text and identical prefixes can be reused exactly. The three answers below either turn changes into appends, which is exact reuse with a small quality risk, or recompute only the states that actually moved.

Feasibility from the ceilings table:
- **A (coding agent):** room for 3x.
- **B (RAG):** capped at 3.6x by output decode, so 2.8x is the real limit.
- **C (document chat):** room for 3x.
- **D (own serving stack):** room for 3x, but 3x also needs a cut in decode compute.

Cases nothing here brings near 100%:
- A wholesale document swap in C.
- Any change in B's retrieved document set that adds new content.
- A's cache-read share (54%). A better hit rate does not reduce it, and no client-side change beats the 0.1× read price.

All dollar figures below are my own arithmetic from the prices in your ledger.

=== IDEAS ===
IDEA 1
NAME: Edits shipped as appended patches
MECHANISM: The client never rewrites earlier context. A changed document section or replaced tool output becomes a short appended note ("section 4 now reads: …; ignore the earlier version"), so the stored prefix stays identical and every earlier token is a cache read. The client rebuilds the prompt once patches exceed a set share of the context (for example 5%). The closest earlier attempt is append-only discipline (Manus), which stopped short because it forbids edits; this design keeps edits and changes only where they are written. Covers middle edits, insertions and tool-output replacement (not reordering), runs client-only on hosted APIs, and costs only the patch tokens. In C, rewriting after a mid-document edit drops from about $0.094 (25k tokens × 1.25 × $3/M) to about $0.002 for a 500-token patch. The deciding quantity is answer agreement between patched and inline prompts, which you can test with paired evaluations, including multi-hop questions that touch the edited text.
VALUE: Hosted-API document edits stay at nearly 100% cache hits without access to the server.

IDEA 2
NAME: Drift-gated partial recompute
MECHANISM: On your own serving stack, after an edit, first recompute only the edited span plus a few early layers for the tokens after it. Measure how far each later token's hidden state moved compared with the cached version. Fully recompute only tokens above a threshold, and stop at layers where drift has died out. Full recomputation of 1% of requests checks the threshold against output agreement. The closest earlier attempt is CacheBlend, which stopped short at a fixed ~15% recompute with no quality bound; this design sets the recompute share per edit from measured drift and audits it. Costs: one extra early-layer pass, and stored states (~320 KiB per token at FP16 for a 70B model, half that at FP8). The deciding quantity is the share of post-edit tokens above threshold. At ≤5% it cuts prefill on edited requests about 10x, worth about 1.8x on D overall. Test it with greedy-output agreement, RULER and multi-turn tasks.
VALUE: Middle edits and tool-output swaps on your own stack cost close to the edited span, with a measured quality bound.

IDEA 3
NAME: Popularity-ranked document order
MECHANISM: Before building the prompt, sort retrieved chunks by a global retrieval-frequency rank instead of by similarity. Common chunks then always sit first and in the same order, so the server's prefix tree reuses them exactly, bit-identically. The rank is refreshed daily, with hysteresis so the order rarely changes. The closest earlier attempts are RAGCache (order-sensitive, so it misses) and CacheWeaver (20–33% lower time to first token); this design makes the order identical across users rather than tuned per request. Covers reordering only, runs client-only or on your own stack, and costs nothing extra to store. The deciding quantity is how skewed retrieval frequencies are: strong skew might give 60–80% hits, a guess to be measured from your logs. Test the quality cost with permutation-sensitivity evaluations.
VALUE: Reordered RAG context becomes exact cache hits, within B's 2.8x limit.