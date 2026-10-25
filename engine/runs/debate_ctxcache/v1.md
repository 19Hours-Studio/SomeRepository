=== IDEAS ===

The fixed replay changes the framing. Once the prompt is append-only, the cache hit rate on re-sent tokens is already about 100% (99.5–100% in every replay below). What remains of the bill is (a) reading the live context on every turn at the cache-read price and (b) writing new content at the write price. Neither is a hit-rate problem. A large further gain therefore needs one of three things: a shorter live context at the same retained information (Idea 2), a cheaper real cost per hit (Idea 4), or reuse across requests and users (Idea 3).

Replay setup (`replay2.py`). The context starts with a 10k-token system prompt. Each turn appends 2,000 tokens of tool output and the previous 300-token assistant reply, and every 5 turns one earlier tool output changes. Tokens that were never sent before count as cache writes. An in-place edit breaks the prefix at a uniform point inside the changed segment, which is fairer to the baseline than breaking at the segment's start. Means are over 100 seeds. API prices are Anthropic 5-minute caching (write 1.25x, read 0.1x) and OpenAI (miss 1.0x, read 0.1x). Own-stack cost assumes a Llama-3-70B-class model with BF16 KV on an H100 at $2/h, 45% compute utilization (MFU) and 3.35 TB/s of HBM bandwidth.

There are two baselines:
- **in-place:** the edited state is rewritten where it sits. This is the case the question asks about.
- **append-full:** the new version is appended and the stale copy stays. This is what coding agents already do.

IDEA 1
NAME: Append-only client discipline (diff errata + first-seen document order)
WHERE: Client only, so it works on any API. Infrastructure cost is zero.
MECHANISM:
- Never mutate a token that has already been sent. A changed tool output or state block becomes a tagged diff at the tail, for example "[supersedes tool_result #17] line 42: x=3 → x=4".
- An insertion becomes an appended block that references its anchor.
- A document set is serialized in first-seen order, not hash order, and JSON is serialized with sorted keys. A reordered set then becomes an exact prefix match, and a new document is appended. The retrieval rank is restated as a one-line ID list at the tail, about 5 tokens per document.
- Compaction is triggered by the context window and by a quality cap (see below), not by a cost rule. The ski-rental rule is dropped: as the check showed, it never fired and contributed 0%.
COVERS: Middle edits and tool outputs exactly, insertions exactly, and reordering exactly within a session. Document sets that are new across users are not covered (see Idea 3). Deletions are not covered either: a client deletion breaks the cache.
NUMBERS (`replay2.out`, means over 100 seeds):
- **Against in-place, 50 turns:**
  - Billed input falls 35.8% at Anthropic prices (747k → 479k units) and 31.7% at OpenAI prices.
  - Hit rate on re-sent tokens is 100%. The total token hit rate is 96.3%, and the missing 3.7% is brand-new content that no cache can serve.
  - The saving scales with how often state changes: −6.2% / −20.3% / −35.8% / −59.9% for an edit every 25 / 10 / 5 / 2 turns.
  - Erratum size matters only a little: 50 / 200 / 1,000 / 2,000 tokens give 474k / 479k / 506k / 539k units.
- **Against append-full, 50 turns:** −11.0% (Anthropic) and −10.9% (OpenAI). The only lever is diff size.
- **Long sessions with a 200k window,** where each policy gets its own best compaction trigger and target: −39% to −40% against in-place, but only −3.0% to −7.3% against append-full.
- **Growing document set:** with 10 documents of 1k tokens each and one new document per request, hash order rewrites 6,003 tokens per request against 1,000 for first-seen order. With 50 documents of 500 tokens, it is 12,758 against 500 (`costs.out`). So the check's correction holds: first-seen order is strictly better.
- **Break-even, corrected** to a rewrite cost of (1.25 − 0.1)(N − p): 1,137 turns for an edit at 50k and 45 turns for an edit at 90k. Errata are almost always cheaper than a rewrite.
QUALITY:
- The KV is exact for the appended prompt, not for the edited one. The model sees stale text next to its correction.
- Published evidence says this hurts as updates pile up. In PI-LLM ("Unable to Forget"), retrieval of the latest value of a key falls log-linearly toward zero as overwritten updates accumulate, and prompting the model to ignore old values helps little.
- Rule: compact a segment once it has collected more than a small number m of errata. The value of m has to be measured.
- Test:
  - Run PI-LLM's public harness (GitHub) in three variants: in-place, errata, and errata with compaction at m.
  - Replay SWE-bench Verified agent runs in both forms: in-place, and errata.
  - SWE-bench Verified has 500 tasks, so the standard error of a pass rate is about 2.2 points. Detecting a 2-point gap needs paired, repeated runs.
- All of this needs a real model and was not run here.
PRIOR ART: Manus's "append-only context" guidance, and agents that append re-reads. Against those, the measured gain is 3–11%, from diff-sized errata and first-seen order. What this idea adds is the numbers and the interference cap. The large −36% applies only to state that really is edited in place, such as memory blocks or todo lists. In the one public SWE-agent demo trajectory I could fetch, 32% of the observation text re-displayed lines already in context (`trace_dup.py`, n=1, illustrative only).

IDEA 2
NAME: Span operations billed as hits: `delete_span` (hole-punch) and `replace_span` (patch)
WHERE: Own serving stack or provider-side, exposed as API operations. Memory: zero extra, because freed blocks go back to the pool. Recompute: k boundary tokens per hole. Position gaps are closed by a delta-RoPE rotation of K. For 150k tokens of 70B BF16 K (160 KB/token) that is a 48 GB read-plus-write, about 14 ms.
MECHANISM:
- `delete_span` removes the span's paged-KV blocks from the block table and keeps every later block.
- `replace_span` does the same and then computes only the new tokens and the first k tokens after each hole (EPIC-style). It can also follow CacheBlend's rule of recomputing the tokens that deviate most.
- With either operation, compaction (clearing old tool results) and errata no longer rewrite the suffix. They also remove the stale copy that causes Idea 1's interference.
- An exact mode, which recomputes the suffix, stays available per request.
COVERS: Middle edits, insertions, changed tool outputs, deletions and compaction.
NUMBERS:
- **50 turns, no window:**
  - `replace_span`: −36.4% against in-place and −11.8% against append-full. That is about the same as client errata, so there is no reason to use it in short sessions.
  - k matters little: k = 0 / 32 / 256 / 2,000 gives 475k / 475k / 478k / 496k units.
- **200 turns, 200k window, same retention for every policy** (compact at 195k down to 140k; quality-matched, because the same history is kept):
  - `delete_span` −24.5% and `replace_span` −25.8% against append-full.
  - −50.8% and −51.7% against in-place.
  - The hit rate on re-sent tokens is 99.99%, against 99.4% for append-full.
- **The same sessions when each policy picks its cheapest retention:** every policy picks a target of 40k, meaning it clears deep and rarely. The advantage then shrinks to −4.5% / −6.7% against append-full, because rewriting 40k tokens costs about as much as 5 turns of reads.
- So the gain is real only when the agent wants to keep a long history: a deep clear is cheap but throws information away.
- Anthropic's context-editing docs confirm the baseline behavior. Clearing invalidates the cached prefix, and `clear_at_least` exists so that each rewrite is worth its cost.
QUALITY:
- The result is not exact. Tokens after a hole keep what they absorbed from the deleted span.
- Test against full recompute of the edited prompt, and against Idea 1 errata, on the same three benchmarks as Idea 1: PI-LLM, SWE-bench replays, and teacher-forced next-token KL with top-1 agreement on agent traces. Test both the position-gap variant and the re-rotated variant.
- The hypothesis to test is that patch quality falls between errata and exact. If it falls below errata, use exact mode.
- This needs a real model and was not run here.
PRIOR ART:
- llama.cpp `--cache-reuse` already shifts cached KV chunks to reuse them after an earlier part of the prompt changes.
- StreamingLLM, H2O and SnapKV drop KV with the same mechanism, but choose tokens by heuristic.
- CacheBlend and EPIC use selective recompute for segments.
- What is new: an explicit, client-driven span API on a multi-tenant serving stack, billed as a hit, that replaces cache-invalidating context editing.

IDEA 3
NAME: Segment cache with gated selective recompute, for reuse across requests and users
WHERE: Own stack (LMCache CacheBlend in vLLM) or provider-side. Storage holds one KV copy per unique segment: 320 KB/token for 70B BF16, 69 KB/token for DeepSeek-V3 MLA. Loading costs 6.6 s per 1M tokens over PCIe at 50 GB/s.
MECHANISM:
- Cache each document or memory unit on its own, keyed by content hash and computed after the real shared system prompt (APE).
- On reuse, rotate its positions and recompute a fraction of tokens. Engine choice:
  - RAG passages: CacheBlend (about 15% recompute) or EPIC (32 tokens per chunk, 6.25%).
  - Structured agent memory: AgentKVShift. It applies one probe-estimated per-memory offset correction to every reused token, with 10–30% refreshed.
- A deviation gate falls back to exact recompute.
COVERS: Reordering and new combinations of documents across requests. Within one session, Idea 1's first-seen order does this exactly.
NUMBERS (papers' own):
- **RAG:** 85–94% of segment tokens are reused. CacheBlend reports a 2.2–3.3x faster time-to-first-token. EPIC reports up to 8x with "negligible" loss.
- **Agent memory:** this is where the check's correction applies.
  - On LoCoMo with a 10% budget, CacheBlend loses 47.5% of relative F1. AgentKVShift loses 5.9% (0.319 against 0.339 for full recompute).
  - So agent-memory reuse is about 70–90% with AgentKVShift. With CacheBlend, the check reports that 45–55% recompute is needed to recover quality. I could not verify that figure from the excerpts I could read.
QUALITY: Not exact. Test against full recompute on 2WikiMQA, MuSiQue, LongBench and LoCoMo, plus the PI-LLM and SWE-bench replays above. This needs a real model.
PRIOR ART: CacheBlend, EPIC, APE, Cache-Craft, Fusion-RAG (SIGMOD'26), AgentKVShift, KVCOMM, RelayCaching. What this idea adds is only the gating and the engine choice per workload. It is listed because it is the only route to cross-user reordering, not as a new idea.

IDEA 4
NAME: Price and tier a hit at its real cost (gap-aware parking)
WHERE: Own stack or provider-side.
MECHANISM:
- The real marginal cost of keeping one cached token through one agent turn is:
  - prefill attention from the turn's new tokens: $0.0075/M, which is 2.0% of a recompute at position 60k ($0.371/M);
  - decode KV reads: $0.016/M for 300 output tokens in BF16, $0.008/M in FP8 and $0.0035/M with MLA;
  - holding the KV during the tool gap. For a 30 s gap that is $0.068/M in HBM, $0.014/M in DRAM at cloud-rental prices, and $0.0004/M in DRAM at hardware cost over three years.
- Holding in HBM is therefore the largest part of a hit's input-side cost. Park the KV in DRAM whenever the predicted tool gap is longer than a few seconds, and prefetch it layer by layer when the tool result arrives. Reloading 100k tokens takes 0.66 s in BF16, 0.33 s in FP8 and 0.14 s with MLA, and it overlaps with the prefill of the new tokens.
- A provider could then charge for reads at roughly 2–5% of the base input price instead of 10%. That is a pricing choice, not something measured here.
NUMBERS (`tiers.out`, errata policy, 50 turns, own-stack $ per session):
- Against HBM pinning in the style of Continuum, DRAM parking costs 1.37x less for a 5 s gap, 3.2x less for 30 s, and 9.5x less for 120 s. On the input side alone (prefill plus holding) the factors are 1.8x / 5.7x / 18x.
- Honest caveat: HBM holding is a real cost only when the batch is limited by memory. A GPU with spare HBM pays nothing for pinning.
- Corrected break-even intervals between holding and recomputing (recompute averaged over a 100k prefill, $0.338/M):

  | Tier | Break-even interval |
  |---|---|
  | HBM | 2.5 min |
  | DRAM, cloud-rental price | 13 min |
  | DRAM, hardware cost over 3 years | 6.8 h |
  | NVMe, cloud block-storage price | 5.2 h |
  | NVMe, hardware cost over 3 years | 339 h |

  The ordering NVMe < DRAM < HBM holds. The size of the gaps depends on the pricing basis.
- In the own-stack session cost, decode KV reads are about half ($0.055 of $0.103). So the asker's assumption that input dominates cost is wrong for long agent contexts. FP8 or MLA KV halves, or cuts about 4.7x, that half regardless of hit rate.
PRIOR ART:
- InferCept (preserve, discard or swap during tool calls) and Continuum (TTL pinning in HBM by predicted tool time).
- LMCache, Mooncake and HiCache tiering. The earlier runs' 1.2x is a hit-rate gain on chat traces. The gain here is HBM opportunity cost on agent loops, so the two numbers do not conflict.
- Gemini explicit caching, which already bills storage at $4.50 per M token-hours (2.5 Pro) and $1 (Flash).
- What this idea adds: choosing the tier per session by cost, from the predicted gap, and the cost breakdown above.

WHAT CANNOT REACH ~100%, OR NOT WITHOUT QUALITY LOSS
- **Brand-new content** is about 3.7% of tokens here and is always billed as a write. The total token hit rate tops out around 96%. Only the hit rate on re-sent tokens can reach about 100%.
- **Exact output after an in-place edit, insertion or deletion** needs a suffix recompute. Idea 1 stays exact only for a different prompt (stale text plus correction), and that has a measured interference cost. Ideas 2 and 3 are approximate.
- **Plain API users** have only Idea 1: −32% to −36% against in-place, but only −3% to −11% against agents that already append. Deletions on the client side still break the cache.
- **Cross-user reordering at exact quality** is not possible: that needs recompute.

=== NOTES ===
How each point of the check was handled:
- **Billing bug:** accepted and fixed. The 92.9% / 99.75% / −40% figures are replaced by 89.1% / 96.3% / −35.8% (100-seed means with a 200-token diff; seed 0 gives −34.8%). This differs from the check's −30% because the check used 1k errata and a break at the segment's start. With 2k errata the result here is −27.9%, which matches its −25% to −29%.
- **Ski-rental:** dropped.
- **Strawman baseline:** accepted. Both baselines are now reported.
- **"Exact KV":** rephrased, with PI-LLM evidence added.
- **Hash sort:** replaced by first-seen order, with numbers.
- **Idea 3 agent number:** corrected.
- **Idea 4 recompute price and pricing bases:** corrected ($0.338/M; break-even intervals recomputed on both bases).
- **Prior art:** llama.cpp `--cache-reuse` and Gemini storage pricing added.
- **OpenAI 0.1x:** accepted as confirmed.

Scripts and outputs in `engine/runs/debate_ctxcache/round1/`: `replay2.py` and `replay2.out`, `costs.py` and `costs.out`, `tiers.py` and `tiers.out`, `trace_dup.py` and `trace_dup.out`. The replays are synthetic, and the edit frequency is an assumption, so it is swept. The Mooncake trace was not used, because its chained block hashes cannot show reuse that does not start at the prefix. GPU price, utilization and $/GB-h figures are my assumptions. Every quality claim comes from the cited papers or is untested.

HONEST GAIN (synthetic replays):
- **Client only:** −35.8% billed input against in-place editing (Anthropic; −31.7% OpenAI; range −6% to −60% over edit frequency), at 100% hit on re-sent tokens. Only −3% to −11% against agents that already append.
- **Provider-side span operations:** −25% against append-full and −52% against in-place for long sessions at matched retention. Only −4.5% to −7% if the client accepts clearing deep.
- **Own stack:** parking KV in DRAM during tool gaps cuts per-session cost 1.4x to 9.5x against HBM pinning, for 5–120 s gaps.
- Quality is untested on a real model throughout.
