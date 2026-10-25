**Standard answers.** Most experts would propose these first, and they share one paradigm: *recompute a selected subset of tokens to restore cross-chunk attention*.
CacheBlend HKVD recompute, EPIC sink-token recompute, APE position/temperature scaling, Cache-Craft variant storage, layer-1 deviation token selection, prefix-aware reordering, a full recompute of the last chunk, and query-first recompute.

**Candidates**
1. Tune CacheBlend's recompute ratio per model | P 0.45
2. EPIC-style sink repair only | P 0.35
3. APE attention-temperature rescaling | P 0.25
4. Recompute the boundary tokens of each chunk | P 0.30
5. Store per-variant chunk KV (Cache-Craft-like) | P 0.20
6. Additive low-rank pairwise KV deltas from co-retrieval statistics | P 0.05
7. Select tokens to recompute by cross-chunk entity overlap, with no forward pass | P 0.07
8. Encode chunks under a corpus-centroid prefix instead of an empty one | P 0.06

I develop 6, 7 and 8.

**Shared scope**
- Runs on your own vLLM/SGLang stack with LMCache.
- Covers document reordering, insertion and middle edits for any chunk that is already cached. Tool outputs are covered only once cached; a new tool output is a cold write.
- Hit rate ≈ chunk-store coverage, so it can approach 100% for repeat corpora.
- Ceiling: prefill is 55% of the cost. Driving prefill to about 5% of its current cost gives 1/(0.45+0.03) ≈ 2.1x. This direction alone cannot reach 3x; that also needs decode savings.
- Quality test, required per model (Llama and Qwen3 diverge, per attempt 12):
  - Benchmarks: Musique, 2Wiki and RULER multi-hop.
  - Settings: multi-query and long chain-of-thought.
  - Baselines: full recompute and CacheBlend-15%, measuring F1 delta.
- Honest limits:
  - Unseen chunks are cold writes.
  - Gains are unverified on MLA, sliding-window and hybrid architectures.
  - Multi-hop bridges spanning three or more chunks may defeat a first-order correction.

**Per-idea cost**
- *Pairwise deltas.* Storage per pair ≈ r(T+d)/(T·d). With r=8, T=512 and d=1024, that is about 2.3% of the chunk KV per pair, or about 47% extra for 20 partners per chunk. Applying the deltas costs one GEMM per layer, under 1% of prefill.
- *Entity selection.* Recomputing 2–4% of tokens instead of 15% gives about 4x less recompute. Latency is under 1 ms on the CPU.
- *Centroid prefix.* The prefix adds about 128 tokens to each chunk's encode once, offline. Runtime cost is zero.

=== IDEAS ===
IDEA 1
NAME: Composable pairwise low-rank KV deltas
MECHANISM: Offline, for chunk pairs (A,B) that co-occur often in retrieval logs (the distribution is Zipf-skewed), run B after A once. SVD the difference between the contextual and isolated KV of B per layer, and store rank-8 factors. At splice time, add the summed pairwise deltas of all preceding chunks, as a first-order additive approximation. Fall back to sparse recompute for uncovered pairs. The closest prior art is Kamera's fitted rank-16 patch and Cache-Craft's per-context variants, which are respectively learned/global and non-composable. These deltas are forward-pass-derived, per pair, and compose across any order. The deciding quantity is the fraction of true KV deviation variance that the summed pairwise deltas capture on three or more chunks.
VALUE: It replaces CacheBlend's 15% recompute with a GEMM costing under 1%, for any order of covered chunks.

IDEA 2
NAME: Entity-overlap recompute selection
MECHANISM: Cross-chunk attention is lost mostly on tokens that refer to content elsewhere, such as shared entities, coreferents and numbers. Selection uses a cheap index of entity/n-gram overlap between spliced chunks, computed without any model pass, and recomputes only those tokens plus the chunk-start sink tokens, at 2–4%. CacheBlend's layer-1 deviation selection needs a partial forward pass and keeps about 15% because its proxy is noisy. Lexical bridges target multi-hop links directly. The deciding quantity is the recall of the top-deviation tokens at a 3% budget against a full-recompute oracle.
VALUE: It cuts recompute roughly 4x while aiming at the multi-hop failures that hurt training-free reuse most.

IDEA 3
NAME: Corpus-centroid conditioned chunk encoding
MECHANISM: Encode every chunk after a fixed, realistic prefix rather than an empty context. The prefix is the system prompt plus a short, medoid-selected corpus passage. Store the chunk's KV with that prefix trimmed and positions remapped by RoPE rotation. This removes the spurious attention-sink and out-of-distribution "document start" state that EPIC suppresses only by recompute. It also shrinks residual deviation, so any recompute budget goes further. The deciding quantity is the KV L2 deviation versus true context, relative to empty-prefix encoding, measured per layer.
VALUE: It gives a free, offline reduction of splice error that lowers the recompute share needed for parity across all chunk orders.