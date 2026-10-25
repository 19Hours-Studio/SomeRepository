# Making cached context much cheaper, with hits near 100%

Numbers come from `calc.py` (`python3 -I calc.py`, about 2 minutes, standard library only; output in `calc_out.txt`). SWE-agent trajectories are in `traces/`. `cachediff.py` finds where a request breaks the cache, with test pairs in `examples/`. Nothing was committed. Model weights couldn't be downloaded, so **every quality claim is either published or untested.**

**New in this version:**
- **§K:** a warm-up request before parallel fan-out makes the prefix 5.8× cheaper at 10 requests.
- **§L:** batch stacks with caching and halves the bill. It beats interactive use only above about 81% in-batch hits.
- **§M:** clearing old tool results every ~8 turns cuts a 200-turn agent's bill to 0.43×. A square-root rule predicts the best period and sets Anthropic's `clear_at_least`.

## Short answer

| You are | Do | Exact? |
|---|---|---|
| API user | Idea 1: append-only layout, volatile blocks last, errata not edits, breakpoints/TTL, warm-up, square-root clearing, batch, `cachediff.py` | Yes, except clearing |
| Self-hosting | Idea 1, a template that doesn't rewrite history (or token IDs), Idea 2, Idea 4 | Ideas 1 and 4 exact; Idea 2 approximate |
| Provider | All of the above, plus Idea 3 sold as a cheaper "approximate hit" | Idea 3 approximate, gated |

**Key fact 1.** No exact method reuses KV after an in-place change. Server-side fixes are approximate and must be checked against full recompute, so near-100% exact hits require the client to stop editing in place.

**Key fact 2.** At 100% hits the bill is mostly reads and writes. "Much cheaper" means reading fewer tokens (§M, Idea 2) or paying less per token (TTL, batch).

## 0. The bill at 100% hits

The model is a 50-turn agent: 10k system prompt, 2k tool output and 300 output tokens per turn, priced at write 1.25×, read 0.1×, output 5×. **Reads are 59% of the bill, writes 28%, output 13%.**

Measure the hit rate from usage fields:
- Anthropic: `cache_read_input_tokens / (cache_read + cache_creation + input_tokens)`
- OpenAI: `cached_tokens / prompt_tokens`. From GPT-5.6 on, OpenAI also reports `cache_write_tokens`, billed at 1.25×.

| Lever | Effect |
|---|---|
| TTL (§G) | N reuses at 6–60-minute gaps cost 1.25·(N+1) with a 5-minute TTL (7.5× at N=5), but 2+0.1·N with a 1-hour TTL (2.5×) |
| Warm-up (§K) | Entries exist only after the first response begins, so concurrent requests all miss. Send one request first (`max_tokens=1`): the prefix gets 1.9× cheaper at N=2, 5.8× at 10, 10.2× at 50, for one extra TTFT |
| Batch (§L) | The 50% discount stacks, so a read costs 0.05×. In-batch hits are best-effort, so warm up synchronously with a 1-hour TTL. With a 20k prefix and 1,000 requests, batch costs 0.56× interactive at 98% hits, 1.28× at 70%, 2.30× at 30% |
| Routing | OpenAI: keep each `prompt_cache_key` to about 15 requests/min. Split traffic over ⌈rate/15⌉ stable keys |
| Minimum length | 1,024 tokens (4,096 for Opus 4.5/4.6 and Haiku 4.5). OpenAI matches in 128-token steps |

## Idea 1: Cache-stable layout (client only, exact)

- **1a. Ordering.** Sort blocks by **pᵢ/((1−pᵢ)·sᵢ), ascending**, where pᵢ is the chance a block changes and sᵢ its size. This was optimal in all 3,000 brute-forced layouts. Plain p/s was suboptimal in 59% (median 1% worse, at most 17%).
- **1b. Volatile tail.** Put the to-do list, memory and current state after the conversation, and re-send them only as diffs when they change. Place the last breakpoint before the tail, so it bills at 1.0× instead of 1.25× (§J).
- **1c. Errata and normalization.** Turn middle edits into end notes, such as `[supersedes tool_result #17]: …`. Normalize timestamps, UUIDs and key order, and put documents in canonical order.
- **1d. Folding errata back in.** Rewrite in place after T* = (1.15·S − 1.25·e)/(0.1·e) turns, where S is the number of tokens after the edit and e the erratum size. S=50k, e=500 gives 1,138 turns; S=10k, e=2k gives 45. This is within 2× of the best schedule in hindsight.
- **1e. Square-root clearing (§M).** In a 200-turn run, tool results older than 3 turns become 20-token placeholders:

| Clear every | 1 | 5 | **8** | 10 | 40 | 100 | never |
|---|---|---|---|---|---|---|---|
| Bill | 0.56× | 0.43× | **0.43×** | 0.43× | 0.51× | 0.69× | 1.00× |

  - This assumes the prefix up to the clear point stays cached. If only the system prompt survives (Anthropic without a breakpoint there), the best period is 20 turns at 0.49×.
  - **Rule:** T* ≈ √(2·1.25·K/(0.1·g)), where K is the tokens re-written per clear and g the clearable tokens added per turn. It predicts 9 and 15 turns against the simulated 8 and 20.
  - On Anthropic, set `clear_at_least` ≈ T*·g.
  - **Caveat:** in §D's short real sessions (median observation 65 tokens), clearing every step cost 1.79×.
  - **Quality:** clearing drops information on purpose. Test task success across T.
- **1f. Silent breakers.**
  - **20-block lookback.** With one breakpoint at the end of 200 blocks, an edit at block 150 loses everything, including the 13k system prompt (§J). Use up to 4 breakpoints: after tools and system prompt, after documents, and before the clear point.
  - **Parallel fan-out**, including parallel subagents.
  - **History-rewriting templates.** Qwen3 drops earlier reasoning and gpt-oss drops analysis. In §H the hit rate falls from 97.7% to 94.7% and cost rises to 1.27× at 5 steps per query (1.10× at 20). xAI names dropped `reasoning_content` as the top cause of misses. Fixes: keep reasoning, send token IDs, or splice (Idea 2).
  - **Re-serialization:** key order, schema order, timestamps.
- **1g. `cachediff.py prev.json next.json`.** It reports the first differing block, the likely cause, the tokens recomputed with the resulting cost multiplier, and lookback warnings. A one-character change to a tool output at message 4 of 61 costs 11.2×; reordered schema keys cost 12.5×.

**Hit rates (§C).** The agent has a 3k system prompt, 8k tools, 2k memory changing on 10% of turns, a 500-token to-do list changing on 50%, 20k documents changing on 2%, and a 40k conversation.

| Layout | Hits |
|---|---|
| Authoring order | 47.1% |
| Best order | 67.4% |
| Volatile tail last | 93.7% |
| + document errata | 95.3% |
| + diff-only tail | **98.0%** |

**RAG (§E).** With 2,000 documents, 5 per query and Zipf popularity (s=0.8–1.2):
- Total hits: relevance order 55–63%, hash order 57–68%, **popularity order 63–77%**.
- A greedy radix-tree walk adds only 0–0.4 points.

**Quality risks:** stale text sits next to its correction, popularity order differs from relevance order, and kept reasoning is out of distribution. A/B test with needle probes, SWE-bench and RAG QA.

## Idea 2: Splice KV in place (approximate)

`edit_span(range, replacement)` works in four steps:
1. Drop the span's blocks.
2. Re-rotate the later RoPE keys, or leave a position gap.
3. Prefill only the replacement.
4. Gate the result on sampled exact recompute.

It needs no extra memory and removes 1e's rewrite cost.

**Trace replay (§D).** Illustrative only; the last 5 observations are kept.

| Policy | 30 steps (hits, cost) | 80 steps (hits, cost) |
|---|---|---|
| Append-only | 94.4%, 1.00× | 97.8%, 1.00× |
| Elide every step | 69.8%, 1.79× | 80.1%, 1.30× |
| Elide every 15 | 90.5%, 1.05× | 94.4%, 0.77× |
| **Splice** | 91.8%, **0.82×** | 95.5%, **0.62×** |

**Quality:** later tokens keep what they absorbed from the deleted span. Test KL divergence and top-1 agreement against full recompute, plus a deleted-wrong-fact probe.

## Idea 3: Segment cache with a shadow-calibrated gate (approximate)

**Mechanism:**
- Cache each document or tool output by content hash (APE-style) and re-rotate it at new positions.
- Fix cross-segment attention with CacheBlend (~15% of tokens recomputed), EPIC or AgentKVShift.
- **Gate:** run exact prefill in shadow on 1% of traffic. Fit a threshold that gives ≥99% top-1 agreement over 64 tokens, and fall back to exact prefill above it.
- Charge separate prices for exact and approximate hits.

Coverage reaches 96% of document tokens, against 34–60% for prefix reuse. Compute saving by fallback rate f:

| f | 0% | 10% | 30% | 50% |
|---|---|---|---|---|
| s=0.8 | 2.40× | 2.10× | 1.68× | 1.40× |
| s=1.2 | 1.60× | 1.51× | 1.35× | 1.22× |

- **Published speedups:** TTFT 2–8×.
- **Storage:** 320 KiB per token for Llama-3-70B in BF16.
- **Quality:** near-exact on single-hop RAG, but every method has a multi-hop gap. Test on 2WikiMQA, MuSiQue and LongBench.

## Idea 4: Retention priced against recompute (exact)

Keep KV only while expected reuses × recompute cost exceed storage cost. The cost model is Llama-3-70B on 8×H100 at $2/GPU-hour.

- **Recompute:** $0.19 per 1M tokens at 8k context, $0.38 at 128k.
- **Break-even reuse window (BF16; FP8 doubles it):** HBM 1.4 minutes, DRAM 6.9 minutes, NVMe 2.6 hours.
- **Bandwidth:** one NVMe drive is no faster than recompute. Four drives or 400 Gb/s RDMA help.
- **Price:** recompute cost sits below a $0.30/M cached-read price, so the size of the discount is a pricing choice.

## Limits

- After an in-place change, only layer-0 KV is reusable exactly: about 1/80 of the suffix work for a 70B model.
- New document combinations cap exact reuse at 34–60%.
- Other limits:
  - multi-hop gaps on reused segments;
  - templates you don't control;
  - simultaneous first requests;
  - prompts below the minimum length.
- At 100% hits the cost floor is reads + writes + output.

**Needs a real model:** errata semantics, document order, kept reasoning, the task-success curve for clearing, splice deviation, and the gate threshold.

**Unverified:**
- The Mooncake trace was not replayed.
- Hardware prices are assumptions.
- In-batch hit rates (30–98%) are third-party figures; measure your own.
- Gemini figures come from secondary sources.

**Key sources:** Anthropic prompt-caching and context-editing docs, OpenAI and xAI caching docs, *Don't Break the Cache*, CacheBlend, EPIC, Leyline, AgentKVShift, Fusion RAG Cache.