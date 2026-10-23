=== REFRAMES ===

ASSUMPTIONS:
- A higher cache-hit rate is the lever that lowers cost (contradicted: in archetype A, hits are already near 100% and the remaining cost is reads at 54%, writes at 23% and decode at 23%).
- A hit rate near 100% across non-identical prefixes can be reached with outputs unchanged (contradicted: only exact prefix reuse is bit-identical, and the best training-free methods lose 2–7% (APE) or recompute about 15% of tokens (CacheBlend)).
- One mechanism can cover middle edits, insertions, tool outputs and reordering alike (contradicted: a new tool output is first-seen text that must be prefilled at least once, so it can never be a hit; independent documents and dependent history behave differently).
- The solution can sit anywhere, including client-only on a hosted API (contradicted: a client cannot get below the 0.1× read price, and providers expose no hook for approximate reuse).
- "Much cheaper" is reachable in every workload (contradicted: B's ceiling is 3.6×, and even cutting every touchable term 10× misses 3×).
- Cost means the provider's token price (contradicted for own stacks: in D the cost is GPU time, and 55% of it is prefill on missed tokens).
- The quoted prices and token mixes are reliable (partly unsupported: the prices come from third-party sites and the token mixes are modelling assumptions).
- The asker tolerates any change in output relative to full recomputation (unstated, and it decides whether approximate reuse is allowed at all).

REFRAME 1: On an own serving stack or provider-side, for prompts built from independently produced chunks (retrieved documents, inserted files) in varying order, how can a training-free method cut prefill cost on cache-missed tokens well below CacheBlend's ~15% recompute? Output divergence from full recomputation should stay within a stated bound on multi-hop, multi-turn and RULER tests, measured against vLLM/SGLang with LMCache and FP8 KV. | CHANGES: scope narrowed to the reorder and insertion cases on stacks that can reach the KV tensors; the target moves from hit rate to recomputed fraction plus a quality bound; the baseline becomes the strong one | IMPORTANCE: high | POSSIBILITY: medium-high | WHY: this is where the largest cost that nobody has cut sits (B 71%, D 55%), and the prior art leaves a measurable gap.

REFRAME 2: For each workload, what reduces total cost per completed task (prefill recompute, cache-read and cache-write volume, KV storage and transfer, decode), and how much does each term allow? A key case is the agent loop that re-reads its whole growing history every turn. | CHANGES: unit moves from hit rate to cost per task; the target moves to the dominant term for each archetype (A: reads, C: amortized writes) | IMPORTANCE: high | POSSIBILITY: medium | WHY: it fixes the metric error, since 100% hits still leaves A paying 54% for reads.

REFRAME 3: Split the problem into the four change cases and set an honest ceiling for each, both under exact reuse and under bounded-approximate reuse. Then attack first the case with the most cost and the most headroom. | CHANGES: one bundled question becomes sub-questions of very different difficulty, and "~100%" is replaced by a ceiling per case | IMPORTANCE: medium | POSSIBILITY: high | WHY: it keeps the answer from overclaiming on tool outputs and dependent edits, where ~100% cannot be reached.

REFRAME 4: On a third-party API with client-side control only, how much can the number of tokens after the first differing token be cut for edited-document sessions (C) and RAG (B), given 4 breakpoints, TTLs and the 0.1×/1.25× pricing? | CHANGES: scope limited to hosted APIs used client-side, with the price floor taken as fixed | IMPORTANCE: medium | POSSIBILITY: medium-low | WHY: most askers face this case, but the ceilings cap the gain at about 1.5–2×.

REFRAME 5: What API and billing contract would let a provider offer non-prefix KV reuse with a declared and verifiable quality bound, so that approximate semantics can be sold? | CHANGES: the target moves to the provider's interface and incentives | IMPORTANCE: medium | POSSIBILITY: low | WHY: this is the deployment blocker, but there is little material to build on.

REFRAME 6: What test protocol bounds output divergence between reused-KV and full recomputation across architectures (GQA, MLA, sliding-window) and task types, so that any reuse method can be judged? | CHANGES: the sub-question attacked first becomes the evaluation prerequisite | IMPORTANCE: medium | POSSIBILITY: high | WHY: every reported speedup is the authors' own and none has been replicated independently.

KEEP: 1, 2