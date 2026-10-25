The answer's numbers are correct, but its large gains are measured against poor baselines. The only gain over best current practice that holds up is about 11–14% lower cost from server-side span deletion in agents that mask old tool outputs. That figure is modelled, not measured: it needs a provider or your own serving stack, and its effect on output quality was never tested. For someone using a plain API, I find no real gain.

**Reproduction.** I re-ran `trace5.py`, `rag5.py` and `hitrate5.py` on the 441 real trajectories. All three outputs match the shipped `.out` files byte for byte. My own sensitivity checks are in `sensitivity_check.py` and the claim-by-claim table is in `verdict.md`, both in this folder.

**Claim by claim, against the right baseline:**
- **Idea 1, batched masking ("polling"), −29% to −52%.** This is measured against SWE-agent's per-step masking, which is known to break caching. Against plain append-only it saves 0.4%. Batching the clearing is already standard practice: SWE-agent has `polling`, and Anthropic's context editing has `clear_at_least` so that each cache rewrite is worth it. The answer credits SWE-agent but not Anthropic. **No gain.**
- **Idea 2, provider-side span deletion, −42.5%.** That figure is also against per-step masking. Against the best client-side batching it is **−11% to −14%**, and against append-only −14.1%. Token hit rate is 94.2%, against 92.7% for batching, so it barely improves hit rate.
  - It depends on how many tokens after each deleted span are recomputed (32 in the answer). My sweep: −13.7% at 32, −11.8% at 128, −3.9% at 512, +26.5% at 2,000.
  - The mechanism is prior art the answer does not cite: KVEraser, and Budgeted KV-Cache Repair (delete the entries, fix the positions, recompute a small budget). The new parts are only the idea of billing it as a cache hit and the pricing on these traces.
  - Its effect on output quality has not been measured.
- **Idea 3, retrieved documents at the end of the prompt (RAG), −35%.** This is measured against LangChain's layout, which puts documents before the chat history. Provider caching guides already say to put changing content last, so this is best practice already. Two variants claim more:
  - Keeping documents and capping the set at 12 gains −0.7% to −20.5% over end placement. It is not robust: with 200 or 1,000 candidate documents, or faster relevance drift (how quickly the top documents change between turns), it costs 3–5% more.
  - Adding provider span deletion gains −16% to −50% depending on the parameters, and −2% to −46% with 256 recomputed tokens. This model is entirely synthetic, and quality is untested.
- **Idea 4, batching, −9.7% to −10.8%.** This is against mini-SWE-agent, which runs one command per request. Parallel tool calls are already standard in modern harnesses, and the figure comes from replaying traces with the agent's actions assumed unchanged. The "errata" figure (−32.6%) is synthetic only.
- **Ideas 5 and 6.** Idea 5 (longer cache lifetime for sessions paused by a human) is conditional on an API test the answer has not run. Idea 6 (segment caching) is prior art (CacheBlend, EPIC), as the answer admits.

**Where the answer is honest:**
- It admits that new tokens are always full-price writes.
- It admits that output, about 38% of the bill, is outside caching.
- It admits that exact quality after an edit needs recomputation.
- It concedes that client-side masking never beats append-only.
- Its claim that append-only agents already hit about 95–99% is supported by its own real traces. So "close to 100%" was already true there, and the gain is in cost, not hit rate.

Sources:
- [Anthropic context editing (clear_tool_uses, clear_at_least)](https://docs.claude.com/en/docs/build-with-claude/context-editing)
- [Budgeted KV-Cache Repair for Evolving Contexts](https://arxiv.org/html/2610.17338)
- [KVEraser](https://arxiv.org/html/2606.17034)
- [Contiguity, Not Importance: Budgeted Repair of Stale KV Caches](https://arxiv.org/html/2609.17983)

HONEST GAIN: about −11% to −14% total cost against batched tool-output clearing, modelled only, needing server-side span deletion billed as a cache hit, with quality untested; none for client-only API users