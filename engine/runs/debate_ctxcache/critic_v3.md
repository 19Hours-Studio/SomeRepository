The answer's measured numbers all reproduce. But its real-trace headline is a bit too high: about **−11%**, not −12%. Its biggest synthetic claim, first-seen document order cutting RAG cost by 36–44%, mostly comes from a weak baseline and not from first-seen order itself.

I re-ran `trace4.py`, `sim4.py`, `own4.py` and `ttl.py` on the author's downloaded data: 441 mini-SWE-agent trajectories and the one Claude trajectory. All four outputs match their `.out` files byte for byte. My own checks and the full write-up are in `critic3/`, mainly `critique.md`.

## 1. Numbers that hold
- **Real-trace base:** 19,514 requests; mean context 21.2k tokens, 759 new input and 373 output tokens per request. The base bill is 95.2M units, exact caching saves 78.9%, and the split is reads 41.9 / writes 19.9 / output 38.2%. No gap between requests exceeds 112 s.
- **Reasoning tokens are not double-counted.** The logged `total_tokens` equals prompt + completion + reasoning (for example 1439 + 57 + 65 = 1561), so adding them is correct. Reasoning is 76% of output tokens, about 29% of the whole bill.
- **Claude trajectory:** 99.38% hit on re-sent tokens, 94.77% token hit rate, and $0.4036 = 80,728 units × $5/M. This is one run of 36 requests.
- **Batching:** −5.7% to −8.8% under the strict rule, −19.0% for the lexical upper bound. I hand-checked 20 random strict merges and about 17 of 20 look independent, which fits the claimed 77–90% precision.
- **Back-references** −3.7%, combined −12.0%. The synthetic results (errata −32.6% / −30.9%, the span-op frontier, delegation) and the selective-1h arithmetic (0.9%) also reproduce.

## 2. Unfair or unsupported points

| Claim | Problem | Corrected |
|---|---|---|
| −12% combined | Uses batching before the precision discount the answer itself applies | **−10.4% to −11.5%** |
| Back-references −3.7% | Counts any repeated line of 20+ characters, including generic code lines and tags | −3.2% (runs of 3+ lines), −2.5% (5+); combined about −9.5% to −11% |
| RAG first-seen −36% to −44% vs relevance order | The baseline puts documents *before* the history, so every change in retrieved documents rebills the whole history. Putting this turn's documents at the tail, with the same documents and the same 24.7k context, already gives −34.9% / −36.2%. | First-seen adds only **−13.3% / −0.3%**, at 1.8–2.5× the context. With the answer's own union cap of 20 documents it is 0% / **+37%** worse than tail placement. Calling relevance-ranked order "the real default" is unsupported. |
| Operator view: decode KV reads are 53.1%, FP8 saves −26.5%, swap saves −20% | Leaves out decode weight reads, and sets the swap reload cost to zero in the code | At batch 32: 40.7%, −20.4%, −15.6%. If the reload is not hidden, a hit costs 3.7% of recompute instead of 2.1%. The direction holds. |
| Span ops "−8% to −17%" | The −17% end is the deep-retention comparison the answer itself set aside | −8.4%, or −1.7% with 9% more context. Synthetic only, and 0 on the real traces. |
| "Mutating harnesses are where the big gains are" | The real harness never mutates its context, so how common this case is was not measured | −32.6% stays synthetic |

## Where the answer undersells itself
- **Batching keeps all output of merged requests.** Merging calls plausibly removes one reasoning pass each. Keeping 75% or 50% of that output gives −11.3% / −13.9% instead of −8.7%.
- **Selective 1h TTL** is more plausible than the answer admits. Cache entries are keyed by prefix, and the gap is easy to predict: it starts at the end of the assistant's turn, when it waits for the human. The proposed re-tag test is still needed; my search found no official Anthropic text on how mixed TTLs are billed.
- **Not compacting short sessions is the right call.** Cache-aware observation masking on the real traces costs +1.5% to +19.1%, because rewrites at 1.25× outweigh reads at 0.1×. Masking savings reported in earlier work don't carry over once cached reads are priced.

## 3. Where a larger honest gain is likely
- **RAG and document workloads:** never put retrieved documents ahead of the history.
  - Tail placement gives −35% with the same information as the baseline.
  - Appending only *new* documents at the tail gives **−60% to −70%** against the baseline. That is −38% to −46% against the answer's first-seen design, at the same accumulated context.
  - Quality still needs a position-controlled test.
- **Append-only agents:** what's left is mostly output, and especially reasoning (29% of the bill). The levers are batching that removes reasoning passes and reasoning budgets. Their quality cost has to be measured on paired SWE-bench Verified runs.

Sources:
- [Spring AI issue on TTL ordering](https://github.com/spring-projects/spring-ai/issues/4325)
- [Portkey: Anthropic prompt caching](https://portkey.ai/docs/aigw/integrations/llms/anthropic/prompt-caching)
- [Helicone prompt caching](https://docs.helicone.ai/gateway/concepts/prompt-caching)
- [Vertex AI Claude prompt caching](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/claude/prompt-caching)

HONEST GAIN: about −11% of the total API bill (−10% to −12%) on real append-only agent traces, client-only, quality untested; −32.6% vs in-place-editing harnesses holds only in synthetic replay; the RAG first-seen claim falls to 0–13% over tail placement of the documents.