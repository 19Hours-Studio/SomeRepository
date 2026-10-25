I rebuilt the numbers from scratch, because the earlier answer's `calc2.py` and `calc3.py` were not in this directory. A replay of real SWE-agent trajectories is now included. The scripts are `calc.py` (stdlib only, runs in about 2 minutes) and the trajectories in `traces/`. Nothing was committed.

---

**Short answer:** you can only get a near-100% hit rate that is also exact on the client side. You do it by never editing what was already sent and by putting the parts that change most often last. That works with any API.

Every method that reuses KV after a change in the middle is approximate. It needs your own serving stack or the provider's. It has to be checked against full recomputation, and it should be priced as a separate, cheaper "approximate hit".

At ~100% hits, most of the input bill is cached reads plus cache writes. So "much cheaper" also means reading fewer tokens: deleting KV in place cuts the input bill to 0.62×. A higher hit rate cannot do that.

## 0. What the bill is made of at a 100% hit rate
`calc.py` §A models a 50-turn agent:
- 10k-token system prompt, plus 2k tokens of tool output and 300 output tokens per turn.
- Anthropic multipliers: write 1.25×, read 0.1×, output 5× the base input price.

The bill splits into **reads 61%, writes 25%, output 14%**. A higher hit rate cannot reduce any of these. Keeping only the last 10 turns' tool results and outputs, deleted in place (Idea 2), brings the input bill to **0.62×** (total bill 0.67×) at the same hit rate.

Two more things affect hits on top of prompt layout:
- **Time-to-live (TTL) choice (§G).** Take a context reused N times at 6–60-minute gaps. With the 5-minute TTL it costs 1.25·(N+1) per token: 7.5× at N=5. With the 1-hour TTL it costs 2 + 0.1·N: 2.5× at N=5.
- **Routing.** OpenAI says that above roughly 15 requests per minute per prefix and `prompt_cache_key`, requests overflow to other machines and miss even with an identical prefix. From GPT-5.6 on, writes also cost 1.25×. The fix is to split traffic across ⌈rate/15⌉ cache keys. Then each key still gets about 15 requests per minute and its cache stays warm.

Measure the real hit rate as `cache_read_input_tokens / (cache_read + cache_creation + input_tokens)` on Anthropic, or as `cached_tokens / prompt_tokens` on OpenAI.

---

## Idea 1: Cache-stable prompt layout (client only, exact)
**Where it runs and what it costs:** client side, with any API. No extra memory or storage. Latency is the same or lower.

**Mechanism.**
1. **Ordering rule, corrected.** Assume each block i (size sᵢ) changes independently with probability pᵢ per request. Then the expected recompute is Σ P(block i is the first to change)·(tokens from i onward).
   - Swapping two neighbouring blocks shows the optimum sorts blocks by **pᵢ / ((1−pᵢ)·sᵢ)** ascending: the odds of a change per token, not the probability.
   - Brute force over 3,000 random 6-block layouts (§C): the odds rule was optimal in all of them.
   - The plain p/s rule (Smith's rule) was suboptimal in 59% of cases, by a median of 1% and up to 17%.
2. **Volatile tail.** Blocks that change often (to-do list, memory file, current state) go after the conversation, re-sent each turn. The previous turn's tail sat right after the cached conversation, so dropping it costs nothing. Better still, re-send a block only when it changed, as a diff.
3. **Append-only errata.**
   - A middle edit, an insertion or a changed tool output becomes a short note at the end, such as `[supersedes tool_result #17]: …`.
   - Normalize the noise: timestamps, unordered listings, JSON key order.
   - Serialize document sets in a canonical order.
4. **Compaction by ski rental.** An erratum of e tokens, with S tokens after the edited point, becomes cheaper to rewrite in place after T* = (1.15·S − 1.25·e)/(0.1·e) turns.
   - S = 50k, e = 500: 1,138 turns. S = 10k, e = 2k: 45 turns. If S ≤ e, rewrite now.
   - Rewriting at T* costs at most 2× the best schedule in hindsight.
   - SWE-agent's `polling` parameter and Anthropic's `clear_at_least` are batched versions of the same idea.

**Cases and hit rate (§C).** Agent layout: 3k system prompt, 8k tool schemas, 2k memory changing 10% of turns, 500-token to-do list changing 50%, 20k documents changing 2%, 40k conversation, 1k new tokens per turn.

| Layout | Token hit rate |
|---|---|
| Authoring order | 47.1% |
| Optimal order, conversation last | 67.4% |
| Volatile tail after the conversation | 93.7% |
| + document changes as errata | 95.3% |
| + tail re-sent only when changed | **98.0%** |

- A middle edit, insertion or changed tool output costs only the erratum as a miss: e/prompt size, e.g. 500 tokens of 74k gives 99.3% that turn.
- Reordering the same document set gives 100%.
- **RAG with a different document set per query (§E):** 2,000 documents of 500 tokens, 5 per query, Zipf popularity with exponent 0.8–1.2.
  - Total hit rate, counting the 2k shared system prompt: relevance order 55–63%, hash order 57–68%, **popularity order 63–77%**.
  - Counting document tokens only: 20–33% for relevance order versus 34–60% for popularity order.
  - An online walk of the radix tree, greedy in the style of CacheWeaver and RAGBoost, added only 0–0.4 points over a static popularity order under i.i.d. Zipf. It should matter more when popularity drifts or topics correlate, which I did not model.

**Quality.** The KV is exactly what the model computes for the prompt it gets. The risks are in the meaning:
- stale text stays next to its correction;
- position effects ("lost in the middle") when popularity order differs from relevance order.

Tests (A/B against in-place editing, real model needed):
- a needle test where a superseded fact sits next to its erratum;
- SWE-bench or debug-gym resolve rate;
- RAG question answering under relevance versus popularity order, with and without an order hint (RAGBoost adds one).

**Prior art and what this adds.**
- Already known:
  - Manus and Anthropic advise append-only context and stable content first.
  - *Don't Break the Cache* (2601.06007) measures 41–80% cost cuts from excluding dynamic tool results.
  - RAGCache, RAGBoost/ContextPilot and CacheWeaver already reorder documents for cache reuse, so popularity ordering is not new.
- New here:
  - the odds/size rule, with a counterexample to the naive rule;
  - the diff-only volatile tail;
  - the ski-rental compaction threshold;
  - TTL choice by reuse interval and cache-key sharding, as cost levers;
  - the finding that a static popularity order already captures nearly all of the greedy walk's gain under i.i.d. Zipf.

---

## Idea 2: Delete and splice KV in place (own stack or provider, approximate)
**Mechanism.** An operation `edit_span(range, replacement)`:
- drop the span's paged KV blocks;
- re-rotate the RoPE keys after the span to their new positions, or leave a gap in position IDs;
- prefill only the replacement tokens;
- on a sampled request, compare against exact recomputation of the suffix, with fallback (see the gate in Idea 3).

**Cost.** No extra memory: the freed blocks go back to the pool. The rotation is O(suffix) element-wise work.

**Cases and hit rate.** Deletion and clearing of tool results, and replacing a tool output. The hit rate for a replacement is remaining/(remaining + replacement).

**Real-trace replay (§D).** 3 SWE-agent trajectories (sizes at chars/4, 41 steps), resampled into 30- and 80-step sessions, keeping the last 5 observations:

| Policy | Hit, 30 steps | Input cost, 30 steps | Hit, 80 steps | Input cost, 80 steps |
|---|---|---|---|---|
| Append-only | 94.4% | 1.00× | 97.8% | 1.00× |
| Client elision every step (SWE-agent classic) | 69.8% | **1.79×** | 80.1% | 1.30× |
| Client elision, polling = 15 | 90.5% | 1.05× | 94.4% | 0.77× |
| **Server splice** | 91.8% | **0.82×** | 95.5% | **0.62×** |

Eliding old observations on the client every step costs more than not eliding at all, as SWE-agent's own code comments warn. The splice keeps the benefit of the deletion without paying the suffix rewrite. The hit rate falls slightly only because the denominator shrinks.

These demo traces are small (median observation 65 tokens). Long real sessions would show larger effects.

**Quality.** Not exact. Tokens after the deleted span keep what they absorbed from it, and only keys, not values, have a position correction (PatchKV). Leyline reports splices that track the full-context baseline on MLA models, with +11.2 points of replay hits in SGLang. Its gains depend on the workload.

Tests on agent traces against full recomputation:
- KL divergence and top-1 agreement of next-token distributions;
- task success, gap variant versus rotation variant;
- a "deleted wrong fact" probe, where leftover influence is most harmful. In that case, also append an erratum (Idea 1).

**Prior art.** llama.cpp context shift, StreamingLLM, Leyline (splice directives, with a re-prefill mode for semantic forgetting), *KV Cache Can Be Editable and Composable* (2606.17107), and KVEraser (needs a learned editor, so it fails the no-training rule).
- What this adds: billing a splice as a hit, a gate triggered by measured deviation (Leyline's choice of mode is driven by semantics), and the cost comparison on a real trace.

---

## Idea 3: Content-addressed segment cache with a shadow-calibrated gate (own stack or provider, approximate)
**Mechanism.**
1. Cache each document, tool output or memory unit by content hash, prefilled after the shared system prompt (APE style).
2. When a segment appears at a new position, re-rotate its keys.
3. Recompute the most-deviating ~15% of tokens (CacheBlend), or the first tokens of each chunk (EPIC), or apply an offset correction (AgentKVShift, 10–30% refreshed).
4. **Gate, new:** on 1% of traffic, run exact prefill in parallel ("shadow mode"). Fit the threshold of a cheap deviation signal, such as the KV deviation on recomputed tokens, so that top-1 agreement over the first 64 generated tokens is ≥99%. Requests above the threshold fall back to exact recompute.
5. Charge two prices: an exact hit and a cheaper approximate hit.

**Cases.** Reordering, insertions, changed segments, and RAG with a different document set per query.

**Hit rate and cost.** In the Zipf replay, 98% of document occurrences had been seen before, so segment coverage reaches 96% of document tokens, versus 34–60% for prefix reuse with popularity order.

Compute per document token (load ≈ 0.1, recomputed fraction 0.15, miss = 1.0):

| | s = 0.8 | s = 1.2 |
|---|---|---|
| Prefix cache, popularity order | 0.70 | 0.46 |
| Segment cache | 0.28 | 0.28 |
| **Saving** | **2.5×** | **1.7×** |

Shadowing adds 1% extra compute. Published prefill speedups:
- CacheBlend: 2.2–3.3× time to first token;
- EPIC: up to 8×;
- CacheSlide: 3.1–4.3×;
- AgentKVShift: 2–3.5×.

**Storage:** one KV copy per unique segment. That is 320 KiB/token for Llama-3-70B in BF16, 160 KiB in FP8, and about 69 KB for DeepSeek-V3's MLA (as reported earlier).

**Quality.** The papers report results close to full recompute on single-hop RAG. All methods leave a gap on multi-hop and cross-chunk reasoning (Fusion-RAG; AgentKVShift says so itself).

Tests:
- 2WikiMQA, MuSiQue and LongBench against exact prefill;
- KVShareArena;
- the gate's fallback rate, which counts as a cost.

**What this adds.** A gate calibrated in production by shadow sampling, with a stated agreement target, plus an explicit approximate-hit price. Running Idea 1's ordering first sends only the truly non-prefix tokens down this approximate path.

---

## Idea 4: Price retention against recompute cost and bandwidth (own stack or provider, exact)
Keep KV in a tier only while expected reuses × recompute cost exceed storage cost × time. Load from a tier only if that is faster than recomputing.

§F uses Llama-3-70B on 8×H100 at $2 per GPU-hour and 45% utilization; these are assumptions.

**Recompute cost:**

| Context length | Recompute speed | Cost per 1M tokens |
|---|---|---|
| 8k | 23.7k tokens/s | $0.19 |
| 32k | 19.6k tokens/s | $0.23 |
| 128k | 11.6k tokens/s | $0.38 |

**Retention break-even (BF16):**

| Tier | Keep only if reused within |
|---|---|
| GPU memory (HBM) | 1.4 min |
| CPU memory (DRAM) | 6.9 min |
| NVMe SSD | 2.6 h |

FP8 doubles these windows.

**Bandwidth check.** One NVMe drive loads 21k tokens/s in BF16, no faster than recomputing. Four drives (85k tokens/s) or 400 Gb/s RDMA (153k tokens/s) do help. This fits the ~1.2× gain from tiered caching measured on real traces (your earlier run).

**Cost versus price.** A provider's recompute cost for a 70B-class token (~$0.19/M) is below a $3/M model's cached-read price ($0.30/M). The size of the hit discount is a pricing choice, not a cost fact. Self-hosters should optimize their own compute cost, not mimic API prices.

**Quality:** no effect, since the KV is exact. This makes a near-100% hit rate affordable for long-tail sessions, but it creates no hits after middle changes.

---

## What cannot reach about 100% under these constraints
- **Exact hits after an in-place change in the middle.** In a causal transformer, K/V at layer ≥1 for every token after the change depend on the changed token. Only layer-0 K/V depend on just token and position, and exact RoPE re-rotation can reuse them. So an exact method can skip at most about 1/L of the suffix work (1/80 ≈ 1.25% for a 70B model). Exact near-100% hits therefore require not editing in place (Idea 1), with the risks to meaning that brings.
- **New document combinations per query.** Exact prefix reuse is capped at 34–60% of document tokens in the replay. Segment reuse reaches ~96%, but only approximately.
- **Multi-hop and cross-chunk reasoning on reused segments.** Every published approximate method leaves a gap. Expect the gate to fall back often on these requests.
- **Cost.** At 100% hits the floor is reads + writes + output (61/25/14%). Going further needs fewer tokens read (Ideas 1 and 2), not more hits. Retention (Idea 4) can make 100% uneconomic for sparse reuse.

## What needs a real model
All quality claims fall into this group: errata semantics, document-order effects, splice deviation, the reuse gap and the gate threshold. They are either the papers' own results or untested here, because huggingface.co is blocked.

What I did here:
- exact arithmetic;
- brute-force checks of the ordering rule;
- a Zipf RAG replay;
- a bootstrap over real SWE-agent trajectory sizes (token counts estimated at chars/4).

I did not replay the Mooncake trace. Its hashes are chained to the prefix, so it cannot test non-prefix reuse. GPU, storage and DRAM prices are my assumptions. Gemini's discounts (75% on implicit hits, $4.50/MTok/h explicit storage on 2.5 Pro) come only from secondary sources.

Sources:
- [Anthropic prompt caching](https://docs.claude.com/en/docs/build-with-claude/prompt-caching)
- [Anthropic context editing](https://docs.claude.com/en/docs/build-with-claude/context-editing)
- [OpenAI prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching)
- [OpenAI community: prompt_cache_key](https://community.openai.com/t/how-is-prompt-cache-key-actually-used-in-api-calls/1357766)
- [Gemini caching (secondary)](https://docs.helicone.ai/gateway/concepts/prompt-caching) and [Gemini implicit caching](https://simonwillison.net/2025/May/9/gemini-implicit-caching)
- [Don't Break the Cache](https://arxiv.org/pdf/2601.06007)
- [Manus context engineering](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)
- [SWE-agent history processors](https://github.com/SWE-agent/SWE-agent/blob/main/sweagent/agent/history_processors.py)
- [RAGCache](https://arxiv.org/pdf/2404.12457)
- [RAGBoost/ContextPilot](https://arxiv.org/pdf/2511.03475)
- [CacheWeaver](https://papers.cool/arxiv/2606.19667)
- [CacheBlend](https://arxiv.org/html/2405.16444v3)
- [EPIC](https://arxiv.org/abs/2410.15332v3)
- [APE](https://arxiv.org/pdf/2502.05431)
- [CacheSlide](https://www.usenix.org/conference/fast26/presentation/liu-yang)
- [Leyline](https://arxiv.org/pdf/2606.01065)
- [KV Cache Editable and Composable](https://arxiv.org/pdf/2606.17107)
- [PatchKV](https://arxiv.org/pdf/2609.26219)
- [KVEraser](https://arxiv.org/pdf/2606.17034)
- [KVShareArena](https://arxiv.org/pdf/2609.10266)
- [AgentKVShift](https://arxiv.org/pdf/2607.21604)
- [Fusion RAG Cache](https://madsys.cs.tsinghua.edu.cn/publication/from-prefix-cache-to-fusion-rag-cache-accelerating-llm-inference-in-retrieval-augmented/SIGMOD26-wang.pdf)