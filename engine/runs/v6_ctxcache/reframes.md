ASSUMPTIONS:
- Hit rate is the metric that drives cost. (contradicted: in A the hit rate is already 92%, yet cache write is 47% and cache read 42% of the bill; the write premium on new tokens barely moves as the hit rate rises.)
- A cache hit is nearly free. (contradicted: reads cost 0.1×, a $0.30/MTok floor, and they make up 42% of A's bill.)
- One method can serve hosted-API and self-hosted users alike. (contradicted: hosted APIs expose only exact-prefix matching and no KV handles, so attempts 6–11 cannot run client-side.)
- Close to 100% hits on non-identical prefixes is reachable without training at full quality. (contradicted: training-free reuse either recomputes 15–30% of tokens or loses accuracy, and the loss depends on the model. Methods that skip recompute entirely need fine-tuning.)
- "Much cheaper" has room in every setting. (contradicted for B: output is 26%, so the ceiling is 3.8×, and the table finds 3× unreachable even with every term cut 10×.)
- Authors' quality claims for position-independent reuse carry across models. (contradicted: multi-hop scores 0.41 on Llama vs 0.03 on Qwen3, and there is no independent replication of CacheBlend.)
- The right baseline is no caching or naive prefix caching. (contradicted: a competent operator already uses an append-only layout, or prefix caching plus LMCache/HiCache offload and FP8 KV.)
- Mid-prompt changes are the main loss in every archetype. (partly contradicted: in A the remaining cost is new-suffix writes, re-reads and expiry.)

REFRAME 1: For a long-running tool-using agent on a hosted API, how can the cost per completed task be minimised across cache writes, re-read volume and expiry rewrites, measured against a disciplined append-only baseline? | CHANGES: unit (from hit rate to $/task) and target terms (write and read, not misses) | IMPORTANCE: high | POSSIBILITY: medium-high | WHY: write and read together are 89% of A's measured bill; the ceiling is 10× and needs exactly these two terms.

REFRAME 2: On your own serving stack, for reordered or varying chunk sets and mid-prompt insertions, what fraction of prefill GPU-seconds can be avoided while staying within a stated accuracy margin of full recompute, per model and on multi-hop, multi-turn and RULER tests? The baseline is prefix caching plus a CPU/SSD tier with FP8 KV. | CHANGES: scope (self-hosted only), target (prefill GPU-seconds at bounded quality, not "100% hits") and baseline | IMPORTANCE: high | POSSIBILITY: medium | WHY: prefill is 55% of C (ceiling 10×), and position-independent reuse is the only route to a high hit rate there, but its quality is unverified.

REFRAME 3: Which of the four change cases (middle edit, insertion, tool output, reordering) can be turned into prefix-stable form by request layout alone, and which are inherently non-prefix and need KV access? | CHANGES: splits a bundled question into sub-questions of very different difficulty, to attack first | IMPORTANCE: medium-high | POSSIBILITY: high | WHY: it sets honest per-case limits before any design is chosen, as the answer must do anyway.

REFRAME 4: For RAG through a hosted API, how far can the per-request bill fall toward $0.007 by reducing the full-price retrieved-document tokens, given that the ceiling is about 3.8×? | CHANGES: target (cost per request within the ceiling, not ~100% hits) and the term attacked (documents at 69%) | IMPORTANCE: medium | POSSIBILITY: medium | WHY: exact-prefix caching cannot reach this term when chunk sets vary, and the output share caps the gain.

REFRAME 5: What chunk-level, approximate-reuse cache interface and price would a provider have to offer to make reordered contexts cheap, and how would its quality be audited? | CHANGES: where it runs (provider-side) | IMPORTANCE: medium | POSSIBILITY: low | WHY: it is the only path for hosted users with reordering, but it is outside the asker's control and the quality risk is unresolved.

REFRAME 6: When is it cheaper to keep a cache warm or route requests to the same replica than to pay for a rewrite after expiry or a spread-out miss? | CHANGES: narrows scope to the expiry and replica states | IMPORTANCE: low-medium | POSSIBILITY: high | WHY: it is a computable break-even, but it moves only part of the write term.

KEEP: 1, 2
