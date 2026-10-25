**Candidates (P = chance a typical strong answerer gives it)**

1. Prompt-lookup or n-gram drafting from the prompt (Prompt Lookup Decoding, LLMA) | P 0.35
2. EAGLE or Medusa draft heads | P 0.40, excluded because the heads need training
3. Instruct the model to answer briefly, with max_tokens caps | P 0.45
4. Diff or str_replace edit formats instead of full rewrites (Aider, Claude Code) | P 0.30
5. SuffixDecoding or REST with a global store of past outputs | P 0.15
6. Quote-anchor output: the model cites spans and the client expands them | P 0.06
7. Draft trees keyed by retrieved-chunk IDs | P 0.05
8. Replay the previous generation as the draft after a mid-context change, with draft length set by batch size | P 0.07

**Arithmetic.** For B, a 10x input cut alone gives 2.64x. Reaching 3x also needs output cost to fall from $0.0045 to about $0.0037 per request, a cut of about 17%. For C, a 10x prefill cut needs decode cut about 3x to reach 3.0x. A 2x decode cut gives only 2.6x.

**Shared caveat.** Exact verification leaves quality unchanged. Greedy decoding is token-identical, and rejection sampling keeps the same output distribution. The savings, though, shrink as batch size grows, because verification stops being nearly free once decode becomes compute-bound.

=== IDEAS ===
IDEA 1
NAME: Quote-anchor output expansion
MECHANISM: The model writes `⟦c3: "first six words … last six words"⟧` instead of re-typing text it is quoting from a retrieved chunk. The client fuzzy-matches the anchors against the chunk and splices in the exact text, re-asking on a miss. This runs client-side on any hosted API with no stored state. It differs from OpenAI Predicted Outputs, the closest prior art, which bills rejected tokens and so cuts latency, not cost; quote anchors instead remove output tokens before they are generated. The deciding quantity is the quoted share of answer tokens multiplied by the anchor-resolution accuracy, which should be tested against full answers on multi-hop QA with an LLM judge plus exact-match on the quoted spans.
VALUE: If at least 35% of answer tokens are quotes, B's output cost falls at least 17%, which is the output share needed, alongside a 10x input cut, to bring RAG Q&A to the 3x target.

IDEA 2
NAME: Chunk-keyed speculative draft trees
MECHANISM: On your own vLLM or SGLang stack, store past generations in suffix trees indexed by the hashes of the retrieved chunks they were conditioned on. Draft from the trees whose chunk sets overlap the current request, and let the target model verify the drafts exactly. SuffixDecoding and REST, the closest prior art, use global or per-request stores, so their acceptance falls when unrelated traffic dilutes the store. Keying by document narrows the candidates to text actually written about these sources, and storage is only text, a few KB per answer. The deciding quantity is mean accepted tokens per verification step at production batch size.
VALUE: Repeat-document RAG could get roughly 2–3x fewer decode GPU-seconds at moderate batch with output unchanged, which is the decode cut that has to accompany a 10x prefill cut to reach 3x.

IDEA 3
NAME: Previous-answer replay drafting
MECHANISM: When an agent turn is regenerated because a tool output, document or instruction in the middle of the context changed, use the previous answer to that turn as the draft. Exact verification keeps the unchanged runs, and when a token is rejected, drafting re-aligns by searching the old answer for the newly generated suffix. Draft length k is chosen per step from the current batch size and the recent acceptance rate, and drafting turns off when decode is compute-bound. Closest prior art is Predicted Outputs, which is billed per token on hosted APIs; on your own stack only the verification pass costs anything. The deciding quantity is the fraction of tokens kept between the old and new answers.
VALUE: Re-answers after a mid-context edit, the case prefix caching serves worst, would cost decode time roughly in proportion to how much the answer actually changed, with token-identical output.