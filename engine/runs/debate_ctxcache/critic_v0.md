Most of the answer's arithmetic reproduces. Its main measured result does not: the replay has a billing bug, so the gain is about −30%, not −40%, and the hit rate is 96.3%, not 99.75%. Both numbers come from a synthetic replay, and no quality claim has been tested on a real model.

## 1. Re-derived numbers

**These hold:**
- **Break-even turns (Idea 1):** 1,238 / 50 / 1,550 at Anthropic prices and 990 / 40 / 1,240 at OpenAI prices reproduce. Strictly, a rewrite costs (1.25 − 0.1)(N−p), not 1.25(N−p), because those suffix tokens would have been read at 0.1x anyway. That gives 1,137 and 45 turns. The conclusion is unchanged.
- **KV sizes:** 320 KB per token for Llama-3-70B in BF16, 69 KB per token for DeepSeek-V3's MLA (4.66x smaller), and 6.6 s per 1M tokens over PCIe at 50 GB/s all reproduce.
- **Storage cost per 1M tokens per hour:** $8.19 (GPU memory), $1.64 (CPU RAM) and $0.066 (NVMe) reproduce, given the answer's $/GB-h assumptions.
- **CacheBlend / EPIC:** 15% recompute, EPIC's 32/512 = 6.25%, and EPIC's "up to 8x time-to-first-token with negligible loss" match the papers.
- **OpenAI price:** cached input at 0.1x is confirmed for GPT-5 ($0.125 vs $1.25), so the answer's note that it couldn't confirm this can be dropped.

**These do not hold:**
- **Replay bug:** each turn's new 2,300 tokens (tool output plus the previous assistant reply) and the turn-0 system prompt are billed as cache reads. The script takes the cached length after appending them, but they were never sent before, so they are cache writes.

| | Answer's claim | Fixed |
|---|---|---|
| Hit rate, in-place edits | 92.9% | 89.8% |
| Hit rate, errata | 99.75% | 96.3% |
| Billed input, in-place | 604k | 721k |
| Billed input, errata | 365k | 506k |
| Saving (seed 0) | −40% | **−30%** |
| Saving if the erratum restates the whole 2k tool output | — | −25% |
| Saving over 200 seeds (1k erratum / 2k erratum) | — | mean −33% / −29%, range −10% to −46% |
| Saving at OpenAI prices (no write premium) | — | −26% |

## 2. Unfair or unsupported points

1. **Ski-rental does nothing in the replay.** The "erratum" and "erratum+ski" runs give identical results because compaction never fires. The code adds the erratum's cost once per edit instead of every turn it is re-read. With that fixed, compaction fires once in 200 turns and costs slightly more (6.34M vs 6.18M). The "at most 2x the best schedule" claim adds 0% to the measured gain. The real limit is the context window: the errata context reaches 141k tokens by turn 50.
2. **The baseline is partly a strawman.** Agents such as Claude Code already append a re-read file as a new tool result instead of editing the old one. Against that practice Idea 1 gains about 0%. The −30% applies only to state that really is edited in place, such as memory blocks or a todo list inside the system prompt.
3. **"KV matches full recomputation exactly" is misleading.** The KV is exact for a different prompt (stale text plus its correction), not for the edited prompt. That is a quality risk with no measurement behind it.
4. **Sorting documents by hash backfires when the set changes.** A new document lands at a random position, so on average about half the document block is rewritten. It also throws away retrieval rank order. Keeping documents in first-seen order is append-only and strictly better for sets that grow.
5. **Idea 3's 85–94% hit rate is a RAG number.** On agent memory, AgentKVShift (NeurIPS 2026) reports that CacheBlend-style methods need 45–55% recompute. So the hit rate for agent workloads is about 45–55%, not 85%.
6. **Idea 4's recompute cost is too low.** At 100k context, attention adds 94% to the FLOPs, so recompute costs $0.338 per 1M tokens, not $0.175. The two storage tiers are also priced on different bases: CPU RAM at a cloud-rental rate, NVMe at a block-storage rate. If CPU RAM is priced at hardware cost spread over three years, it costs $0.05 per 1M tokens per hour. Its break-even reuse interval is then 3.5–6.8 hours, not 6 minutes. The ordering (NVMe cheapest, then CPU RAM, then GPU memory) still stands, but the "20x" depends on the pricing basis.
7. **Prior art is missing:**
   - llama.cpp's `--cache-reuse` already shifts cached KV chunks to reuse them after mid-prompt changes. That is close to Idea 2, so what Idea 2 really adds is billing such reuse as a cache hit.
   - Gemini's explicit context caching already charges for storage by the token-hour ($4.50 per 1M tokens per hour for 2.5 Pro, $1 for Flash). That is close to Idea 4, so what Idea 4 adds is cost-based eviction per prefix.

**Where the answer undersells itself:**
- On tokens that were sent before, Idea 1's hit rate really is about 100%. The remaining 3.7% miss is new content that no cache can serve, and the answer could say so.
- The saving grows with session length: −37% at 200 turns and −43% at 500, if the context window allowed it.
- AgentKVShift is not only a quality caveat. It recomputes 10–30% of tokens and nearly matches full recompute (F1 0.284 vs 0.296), so it is a better engine for Idea 3 on agent workloads than CacheBlend.

## 3. Where a larger honest gain is likely

- **Combine Ideas 1 and 2.** Append errata, then use the hole-punch delete to compact. That removes the context-window limit, which is the real ceiling on Idea 1. Server-side "context editing" (clearing old tool results), which currently throws away the cache from the cleared point onward, is the largest unused lever on the provider side.
- **Don't expect much from shorter errata.** Diff-sized errata of 200 tokens only move the saving from −30% to −34%. The remaining cost is reading the ever-growing prefix plus writing the new tokens at the 1.25x premium. For Anthropic users, that write premium is the remaining lever.
- **Regime:** long agent sessions with in-place state edits, and growing document sets kept in first-seen order.

The critique, the fixed replay and the storage re-check are in `/home/user/SomeRepository/engine/runs/debate_ctxcache/critic0/`: `CRITIQUE.md`, `recheck.py` and `recheck_storage.py`.

Sources:
- [llama.cpp KV cache reuse discussion #13606](https://github.com/ggml-org/llama.cpp/discussions/13606)
- [Liquid AI llama.cpp docs](https://docs.liquid.ai/deployment/on-device/llama-cpp/chat)
- [Gemini caching pricing (forum)](https://discuss.ai.google.dev/t/question-about-gemini-api-caching-pricing/107349)
- [fast.io Gemini context caching](https://fast.io/resources/gemini-context-caching/)
- [OpenAI GPT-5 Chat model page](https://developers.openai.com/docs/models/gpt-5-chat-latest)
- [pricepertoken GPT-5](https://pricepertoken.com/pricing-page/model/openai-gpt-5)
- [AgentKVShift](https://arxiv.org/pdf/2607.21604)
- [EPIC](https://www.alphaxiv.org/abs/2410.15332.md)

HONEST GAIN: about −30% billed input tokens (range −10% to −46% across seeds; −25% if the erratum restates the whole tool output) for Idea 1 against in-place-edit prefix caching, at a 96.3% (not 99.75%) token hit rate, in a synthetic replay only, with quality untested; about 0% against agents that already append re-reads