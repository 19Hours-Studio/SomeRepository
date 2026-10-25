**Candidates** (P = chance a typical strong answerer gives it)

1. Append-only context with errata instead of in-place edits | P 0.35
2. Sort retrieved chunks into canonical order | P 0.40
3. Preload the whole corpus as one cached prefix (CAG-style) | P 0.15
4. Route to cost-sized corpus shards, with chunk-ID pointers at the tail | P 0.07
5. Compact accumulated errata at natural cache-expiry gaps | P 0.06
6. Send tool outputs as diffs against the copy already in context | P 0.09
7. Semantic response cache in front of the API | P 0.25
8. LLMLingua-style compression with stable output | P 0.12

I develop 4, 5 and 6, which all fall below the 0.10 cutoff.

**What cannot reach ~100%:**
- **Archetype B (RAG):** output is 26% of cost and cannot be touched, so the ceiling is 3.8x. A 10x cut of retrieved-document input gives at most 2.64x. The $0.007 per-request target is unreachable.
- **Genuinely new tokens:** these always pay a write or an uncached charge.
- **Output:** no client-side layout changes output cost.

=== IDEAS ===
IDEA 1
NAME: Cost-sized corpus shard prefixes
MECHANISM: Cluster the corpus offline into shards of S tokens, each in a fixed, canonical order. Each shard is a cached prefix on the hosted API. Each request is routed to one shard and appends only "relevant: §17, §203" plus the question, so varying or reordered chunk sets never change the prefix. The closest prior art is cache-augmented generation (CAG) and CacheWeaver. CAG preloads the whole corpus and pays 0.1x on every corpus token each request. CacheWeaver only shares partial prefixes. Choosing S explicitly against the 0.1x read price avoids both limits. The deciding quantity is S relative to the retrieved size R (4k): reading the shard costs 0.3·S against 3·R, so S = 16k gives $0.0048 against $0.012 for the document term. That is $0.0102 per request, or 1.7x, plus a shard write of $0.06 per cache lifetime, amortized over requests. Quality, the share of answers recovered when a needed chunk falls outside the shard, and pointer-versus-inline reading should be tested on MuSiQue and HotpotQA against inline RAG.
VALUE: Order-independent, near-100% hits on the document part of RAG through any exact-prefix API, giving about 1.5–2x per request within the 3.8x ceiling.

IDEA 2
NAME: Errata ledger, expiry-aligned rebase
MECHANISM: Middle edits, insertions and changed tool outputs are never applied in place. They are appended as compact errata ("tool result #12 superseded: …"), so the cached prefix survives. The closest prior art is Manus append-only discipline and Anthropic context editing; each edit or clear there forces a rewrite of everything after the change. Here the client instead tracks dead tokens D and rebases (compacts) the context only when D·T > 12.5·C, where T is the number of remaining turns and C the context length. It also rebases during idle gaps longer than the cache lifetime, when a rewrite is due anyway, so compaction costs nothing extra. Example: an edit at the midpoint of a 100k context costs about $0.19 in place, against about $0.002 as a 500-token erratum. The deciding quantity is the share of current cache writes that are re-writes of invalidated suffixes rather than first-time tokens. It can be measured from logs as cache_creation_input_tokens minus the new tokens in each turn. Quality should be tested as SWE-bench pass rate and stale-fact override accuracy with errata versus in-place edits.
VALUE: Cuts the agent cache-write term in proportion to how much of it is invalidation-driven, and covers edits, insertions and tool-output changes.

IDEA 3
NAME: Diff-encoded repeated tool outputs
MECHANISM: The client hashes every tool output it has already placed in context. When a file or command result is requested again, it appends only "unchanged since turn 12" or a unified diff, never a second full copy. This shrinks the genuinely new tokens that pay the 1.25x write charge. The closest prior art is the file-unchanged notices in some agents. Those cover only identical re-reads; this also handles changed outputs as deltas, so a changed tool output costs the size of its diff, not its full size. The deciding quantity is the share of written tokens that duplicate content already in context, measurable from agent traces. Quality should be tested by SWE-bench and Terminal-Bench pass rate and by error rates when applying diffs.
VALUE: Directly shrinks Archetype A's largest term, cache write at 47% of the agent bill, when re-reads dominate the written tokens.