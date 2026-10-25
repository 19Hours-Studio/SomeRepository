# How to make cached context much cheaper, with hits near 100%

The data is 42 real SWE-agent sessions: Claude Sonnet 4 on SWE-bench Verified, full text, re-tokenized with the legacy Claude tokenizer. On this traffic, plain prefix caching already hits **97.0%**. So the hit rate is not the lever. The cost sits in re-reading context the provider already holds:
- **API bill:** cache reads are 56%, writes 22%, output 22%.
- **Runner GPU time:** about 55% is attention over cached keys plus KV reads during decode.

## Short answer, by who you are

**1. API user running an agent (client only).**
- **References (exact, no information dropped): 0.881× of the bill.** Before sending each tool result or tool input, replace every run of 4 or more lines that already appears verbatim earlier in the request with a pointer such as `[n lines identical to lines a–b of message #j]`. The best prior-art equivalent is Claude Code's whole-file re-read stub. Emulated on the same traces it gives 0.993×.
- **References + batching of read-only calls: 0.816×.** This is an upper bound and changes how the agent behaves; see Idea V.
- **References + batched clearing:** 0.720× at keep 10, against 1.006× for the provider's context editing at its best swept setting. At keep 3: 0.625× against 0.868×. This drops content on purpose.

**2. Self-hosted runner or provider.** Measured against **prefix caching + FP8 KV + vLLM's own suffix decoding at its best swept setting**, with cascade attention where sessions share a prefix:

| Regime | Exact (references) | Approximate (+ sparse attention over cached KV) |
|---|---|---|
| These traces (mean decode context 30k), 32 concurrent sequences | **0.884×** | 0.815× (decode only), **0.730×** (decode + prefill over cache) |
| HBM-bound concurrency | 0.873× | 0.776× (decode only) |
| +100k of fixed context unique to each session | 0.958× | **0.591×** |
| +100k of fixed context shared by all sessions (cascade in baseline) | 0.936× | **0.578×** |
| +170k shared | 0.945× | **0.532×** |

**3. RAG that builds a new document combination for each query.** Reuse beyond what exact prefix caching gives (34–60% of document tokens) is only possible approximately; see Idea 3.

## Corrections to the previous version

| Previous claim | Now |
|---|---|
| Runner: 0.556× from my capped drafter + references, vs no speculation; 0.77× vs vLLM `ngram` at default settings | **Unfair baseline.** I built the official Arctic Inference `SuffixDecodingCache` (the code vLLM's `method: suffix` imports) and replayed it at 11 settings. At its best it reaches 3.22 tokens per pass, against 2.46 for my drafter. Its best setting is **x0.585** of no speculation at 32 sequences. My drafter, auto-capped, gives 0.626×, which is **1.07× worse** (1.05–1.11× across concurrency). Tuned `ngram` (num_spec = 4) gives 0.646×. My draft cap applied to the official drafter adds only 0.983–0.986×. I withdraw the drafter as a contribution. The measured runner gain from round 7 is references alone: 0.884× |
| "vLLM ngram default 0.720×" used as the speculative baseline | Tuned `ngram` is 0.646×; best suffix is 0.585× (§T) |
| MTP comparison (0.80× of MTP alone) | It rested on the withdrawn drafter. Removed. References and sparse attention act on prefill and KV reads, so they apply on top of any drafter. Their multipliers here were measured on the suffix baseline only |
| My own re-implementation of suffix decoding (`spec8.py`) | Under-performs the official code (2.01–2.23 tokens per pass vs 2.45–3.22). It is kept only to document that home-made baselines can be unfair |

## Files

All files are in `round8/`.
- **`calc8.py`** (new): §T official-drafter baseline, §U sparse decode, §V batching read-only calls, §W long context. It runs in about 3 minutes with `python3 -I calc8.py` and writes `calc8_out.txt`.
- **`traces/c4/spec8b.py` + `merge8b.py`**: replay the official drafter, producing `spec8b.json`. Setup: the `arctic_inference-0.3.0` sdist from PyPI, with `csrc/suffix_decoding` built through cmake and nanobind. It takes 8 minutes on 4 shards.
- **`calc.py`**: the round-7 sections A–S, unchanged.
- **`traces/c4/dedup.py`**: rebuilds the references data from the 42 public `.traj` files, `https://swe-bench-submissions.s3.amazonaws.com/<key>`, with keys in `pick.txt`.

---

## Idea A: "Reference, don't repeat" (client only; exact information; KV exact)

**Mechanism.**
- When a tool result or tool input arrives, find each maximal run of 4 or more lines that occurs verbatim and contiguously earlier in the request.
- `cat -n` line numbers are part of the match, so a shifted line never matches.
- Replace the run with a pointer, once, on arrival. Keep the rewritten text, so history stays append-only and the prefix cache never breaks.

**Where the repeats come from.**
- Re-viewed files.
- The editor echoing back the edited snippet.
- Overlapping view ranges.
- Re-run test output.
- `old_str` and `file_text` payloads that copy earlier content.

They make up 17.5% of tool-result tokens, 25% of tool-input tokens and **18.1% of the final context**.

**Measured** (`calc.py` §R; runner numbers from `calc8.py` §U/§W):

| Variant | API bill | Runner GPU time vs best practice |
|---|---|---|
| Whole-result stub (Claude Code Read dedup, emulated) | 0.993× | — |
| References, MINRUN = 8 / 4 / 2 | 0.897× / **0.881×** / 0.873× (hit 97.1%) | 0.884× at 32 sequences (0.915× at 8, 0.878× at 128) |
| + batched clearing, keep 10 / keep 3 | 0.720× / 0.625× | — |

**Details.**
- **Coverage:** tool outputs that repeat earlier content. It does not cover middle edits or reordering; see Idea 1.
- **Hit rate:** it does not raise the hit rate. It shrinks what is written once and then re-read on every later step.
- **Where and cost:** in the agent harness, on any API. A line index takes a few MB of CPU memory. The 42 sessions take 16 s in pure Python. No GPU or storage cost, and time to first token goes down.
- **Quality:** no information leaves the context, but the model must follow a pointer. The main risk is exact copying for `str_replace`, since `old_str` must be reproduced from an earlier copy.
- **Test:** A/B on SWE-bench Verified. Measure resolve rate, the rate of `No replacement was performed` errors, steps per task, and a pointer probe (ask for a line that exists only behind a pointer).
- **Prior art:** Claude Code's whole-file, mtime-keyed dedup (reported stale after external edits), diff-style edit formats (Aider) and LZ77. What this adds:
  - line-run granularity, worth 12× the saving of whole-result stubs here;
  - content keys, so it cannot go stale;
  - persistence that is safe for the cache;
  - a measured replay.

## Idea U: Sparse attention over the cached KV (runner; approximate; training-free) — new in this version

**Why this is the unused lever.**
- Once speculation is at its best, the rest of the cost of cached context is reading it.
  - **Decode:** every verify pass reads the whole KV of the sequence. At 30k tokens that is 5 GB of FP8 per sequence, against 2.2 GB per sequence for its share of the weights at 32 concurrent sequences.
  - **Prefill:** each step's 1–2k new tokens attend over all cached keys.
- Speculation amortizes the reads; it does not shrink them. Quantization shrinks them about 2× at most (prior run: ~2.6–3 bits per value is the floor).
- Top-k page selection shrinks them to a fixed budget, whatever the context length.

**Mechanism.**
- **Decode (Quest-style):** keep per-page min/max keys (pages of 16 tokens; metadata is 1/16 of the KV). Each query scores pages and attends to the top pages, up to 4,096 tokens. The first 2 layers stay dense. The full KV stays resident, so nothing is lost permanently and a dense fallback is always possible.
- **Prefill over cache:** each block of 64 new queries attends to the union of its top pages, up to 8,192 cached tokens. New tokens attend to each other densely.
- **With speculation:** the k+1 verify queries may pick different pages. I bracket this as "shared" (same pages) or "indep" (k+1 times the budget).

**Measured on the 42 sessions** (`calc8.py` §U; roofline: 70B dense, 8×H100, FP8 weights and KV; baseline is the best official suffix setting for each concurrency):

| Concurrency | top-2048 shared | top-4096 indep | references + top-4096 indep | + 4-bit KV |
|---|---|---|---|---|
| 8 | 0.824× | 0.963× | 0.898× | 0.818× |
| 32 | 0.793× | 0.891× | **0.815×** | 0.784× |
| 128 | 0.800× | 0.858× | 0.780× | 0.771× |

**The gain depends on context length.** Decode time at 32 sequences, top-4096 indep vs dense:

| Context | Decode time |
|---|---|
| < 16k | 0.996× |
| 16–32k | 0.916× |
| 32–64k | 0.634× |
| > 64k | **0.423×** |

Per verify pass it is 0.314× at 128k and 0.237× at 200k. SWE-bench sessions are short (decode-weighted mean context 30k), so their gain is modest.

**Agents with large fixed context** (§W: the same sessions with X extra tokens in front, such as a repo map, docs or memory):
- Concurrency is capped by resident KV: 106 sessions at X = 0, 24 at X = 100k unique.
- When X is shared, the baseline gets cascade attention: the shared KV is read once per batch and stored once.

| X | Baseline prefill share | Sparse decode | + sparse prefill over cache | + references | + 4-bit |
|---|---|---|---|---|---|
| 0 | 55% | 0.891× | 0.764× | 0.730× | 0.699× |
| 100k, unique | 66% | 0.768× | 0.606× | 0.591× | 0.569× |
| 100k, shared (cascade) | 61% | 0.977× | 0.594× | **0.578×** | 0.577× |
| 170k, shared (cascade) | 61% | 0.986× | 0.544× | **0.532×** | 0.532× |

- **Lesson:** at long context, prefill of each step's new tokens over the cached keys dominates. Sparse decode alone stalls at about 0.77×, and with a shared prefix cascade attention already removes most of the decode reads. The large gain needs sparse prefill over the cache as well.
- **Where it runs and what it costs:** own stack or provider.
  - TensorRT-LLM ships training-free RocketKV in its sparse-attention framework.
  - SGLang's HiSparse supports Quest; it keeps KV in host memory with a small GPU cache, which also lifts the HBM cap on concurrency.
  - Memory: metadata is +6% of KV. Latency per token goes down. The 8k sparse prefill path for short chunks over long caches is less mature than decode sparsity.
- **Coverage:** all cases, including middle edits, because it makes every cached read cheaper rather than creating hits.
- **Quality:** approximate. Training-free top-k methods report near-dense results on RULER-32K and LongBench (UNIQUE; Quest). I found **no published, training-free result on multi-turn agent tasks**; HySparse2's agent gains need post-training. Error can compound over 50+ turns.
- **Test, which needs the model:**
  1. **Teacher-forced replay of these 42 sessions:** score the realized outputs under dense and sparse attention. Report top-1 agreement and KL per step, binned by context length. This is cheap, with no rollouts.
  2. **SWE-bench resolve-rate A/B** at budgets 2k/4k/8k.
  3. **Production gate:** recompute 1% of requests dense in shadow, and ship a budget only where top-1 agreement is ≥ 99%. Otherwise raise the budget or fall back to dense.
- **What this adds over prior art:** the methods exist. What is new here:
  - the accounting on real agent traces, against a tuned suffix baseline and with cascade in the baseline;
  - the finding that the gain lives at long context and needs prefill over the cache, not just decode;
  - the union bracket under speculative verify;
  - the capacity effect.

## Idea V: Fewer requests, not fewer tokens (client; changes agent behaviour)

**Mechanism.** Each request re-reads the whole prefix. 31.6% of the actions are read-only: view, grep, find, ls, cat. When consecutive actions are both read-only, the model could have issued them as parallel tool calls in one turn. Prompt for this and allow parallel tool use.

| Batching (§V, upper bound: assumes all such pairs are independent) | Requests removed | Bill |
|---|---|---|
| Up to 2 calls per turn | 12.8% | 0.946× |
| Up to 3 calls per turn | 17.2% | 0.928× |
| No limit | 23.1% | 0.903× |
| With references, up to 3 | — | **0.816×** |

- **Quality risk:** a later read may depend on an earlier result, and the model then reads the wrong thing. Test: resolve rate and steps per task, with and without a "batch independent reads" instruction.
- **Prior art:** parallel tool use is a standard API feature (Claude, OpenAI). What this adds is a measured bound on cached-read cost from batching.

## Idea B: Batched clearing of old tool results and inputs (client only; KV exact; content dropped on purpose)

**Mechanism.**
- Every T steps, replace all tool results and inputs older than the last K with placeholders of about 20 tokens, and keep the placeholders.
- Put an explicit breakpoint at the first block that has not been cleared. This avoids Anthropic's 20-block lookback.
- Choose T by the economic-order-quantity rule T* ≈ √(2·1.25·K/(0.1·g)), where K is the kept window rewritten at each clear and g the clearable tokens added per step. It predicts 9, and the replay finds 9.

**Against the provider's `clear_tool_uses`, at its best of a full sweep** (trigger 5k–100k, keep 1/3/10, inputs on or off, `clear_at_least` 0–40k; `calc.py` §S):

| Keep | Content | Provider best | Client batched | Ratio |
|---|---|---|---|---|
| 1 | results + inputs | 0.533× | 0.533× | 1.00 |
| 3 | results + inputs | 0.868× | 0.647× (T = 9) | **0.745** |
| 10 | results + inputs | 1.006× | 0.801× (T = 17) | **0.796** |
| 10 | results | 1.007× | 0.880× (T = 18) | 0.874 |

**Details.**
- **Why the provider tool loses at keep ≥ 3:** under stateless semantics the cleared boundary moves one turn per step, so every step rewrites about K results. I inferred these semantics from the docs; check them with `cache_read_input_tokens`.
- **Floor for any policy that reduces context:** 0.466×. Output alone is 0.220×.
- **Quality evidence:** *The Complexity Trap* masks results with a window of 10 and matches the raw agent (Qwen3-Coder 480B: 53.8% → 54.8%). Batched keep 10 always shows a superset of that, so 0.880× is plausibly covered by its evidence. Keep 3, and clearing inputs at all, are untested.
- **Test:** resolve rate over {results, + inputs, inputs over 200 tokens} × keep {3, 10}, with cost taken from the usage fields.

## §0. Levers that don't depend on layout (API; `calc.py` §G–L)

- **Measure hits:**
  - Anthropic: `cache_read_input_tokens / (cache_read + cache_creation + input_tokens)`.
  - OpenAI: `cached_tokens / prompt_tokens`. From GPT-5.6 on, OpenAI also reports `cache_write_tokens`, billed at 1.25×.
- **1-hour TTL** when gaps between reuses exceed 5 minutes. At 5 reuses: 7.5× for the 5-minute TTL against 2.5× for the 1-hour TTL.
- **Warm up before fan-out:** send one `max_tokens=1` request first. This makes the shared prefix 1.9× cheaper at N = 2 and 10.2× at N = 50.
- **Batch API plus caching** breaks even at about 81% in-batch hits.
- **OpenAI routing:** about 15 requests per minute or fewer per `prompt_cache_key`.
- **Minimum length:** prompts below 1,024 tokens (4,096 on some Anthropic models) are never cached.

## Idea 1: Cache-stable layout (client only, exact) — the only exact route for middle edits

- **Errata instead of in-place edits** for middle edits, insertions and changed tool output. A 500-token erratum in a 74k prompt keeps about 99.3% hits.
- **Fold errata back in** after T* = (1.15·S − 1.25·e)/(0.1·e) turns, where e is the erratum size and S the tokens after the edit. This is a ski-rental rule, at most 2× the hindsight optimum.
- **Canonical order** for documents already seen, so reordering costs nothing.
- **Normalize** timestamps, IDs and JSON key order.
- **Order blocks** by p/((1−p)·s), ascending, where p is the chance a block changes and s its size. This was optimal in 3,000 of 3,000 brute-force layouts.
- **Volatile tail** below the last breakpoint. Use up to 4 breakpoints. Keep reasoning in the template; stripping it costs 1.27× per input token at 5 tool steps per query.
- **`cachediff.py`** finds the first breaking block.

**Quality risk:** a stale fact next to its correction. Test with a needle test that places a superseded fact next to its erratum.

**Prior art:** Manus, Anthropic docs, *Don't Break the Cache*, RAGCache, RAGBoost, CacheWeaver.

## Idea 2: Delete and splice KV in place (runner, approximate)

- **Mechanism:** drop the span's KV pages, re-rotate the RoPE keys that follow, and prefill only the replacement.
- **Bill-equivalent:** 0.561× against 0.647× for batched clearing.
- **Quality:** not exact, because later tokens keep what they absorbed from the deleted span. Leyline, KV-Editable and PatchKV report results close to full recomputation; I read their abstracts only.
- **Gate:** the same 1% shadow recompute as in Idea U.

## Idea 3: Content-addressed segment cache with a shadow-calibrated gate (runner, approximate; RAG)

- **Mechanism:** cache each document by content hash, prefilled after the shared system prompt (APE-style). Re-rotate its keys at a new position. Repair cross-segment attention with CacheBlend (about 15% of tokens recomputed), EPIC or AgentKVShift.
- **Gate:** exact shadow prefill on 1% of traffic, fitted to top-1 agreement ≥ 99%. Requests above the threshold fall back to exact prefill.
- **Coverage (synthetic Zipf replay):** about 96% of document tokens, against 34–60% for exact prefix reuse.
- **Saving:** 2.40× at popularity skew s = 0.8 with no fallback, 1.40× at 50% fallback.
- **Quality:** weakest on multi-hop reasoning. Test on 2WikiMQA, MuSiQue, LongBench and KVShareArena. For agents, Idea A gets most of the repeated-content saving exactly.

## Idea 4: Price retention against recompute cost (runner, exact)

Keep KV in a tier only while expected reuses × recompute cost exceed storage cost × time. With assumed prices, BF16 KV pays for itself if it is reused within:

| Tier | Reused within |
|---|---|
| GPU memory (HBM) | 1.4 min |
| CPU memory (DRAM) | 6.9 min |
| NVMe SSD | 2.6 h |

One NVMe drive loads about 21k tokens/s, which is no faster than recomputing. This agrees with your earlier ~1.2× from tiering.

---

## What cannot reach ~100%, or a large gain, under these constraints

- **Exact hits after an in-place change:** impossible beyond the first differing token. Use errata (Idea 1) or accept approximation (Ideas 2 and 3).
- **Hit rate as the lever on agent traffic:** it is already 97%.
- **Exact information-preserving gains** are modest:
  - API: 0.881× (references); 0.816× if batched reads prove safe.
  - Runner, vs a tuned suffix-decoding baseline: 0.873–0.915×.
  - Everything larger is approximate (Ideas U, 2, 3, 4-bit) or drops content (Idea B).
- **Large runner gains (0.53–0.60×) only at long context (≥ 80k)**, and only with sparse prefill over the cache, whose agent-task quality is unpublished. On these short SWE-bench sessions the honest approximate figure is 0.73–0.82×.
- **API bills below 0.466×** are impossible without dropping the current turn or cutting output.
- **Keep 1:** the provider's tool already reaches 0.533×.
- **API users cannot use runner levers.** They gain only if the provider passes savings into prices.

## What needs a real model

- Resolve rate with references and with batched read-only calls.
- Clearing at keep 3 vs keep 10.
- Teacher-forced top-1 agreement and KL for sparse decode and prefill (budgets 2k/4k/8k), binned by context.
- Real GPU-seconds in vLLM, SGLang or TensorRT-LLM with suffix decoding plus sparse attention, including the page-union effect under verify.
- Splice deviation; 4-bit KV quality; errata and order effects; the gate threshold for segment reuse.

**What was done here:**
- Real-trace replays.
- The **official** suffix-decoding code, replayed exactly. The replay is exact because a deterministic draft is accepted with probability p(d), which equals sampling and matching.
- Sweeps of both vLLM drafters, so the baseline is at its best.
- Cascade attention and the HBM cap in the baseline.
- A bill-model check: modelled $38.01 against logged $50.63. The ratio is 0.75 and varies only 0.70–0.77 across sessions, so ratios hold while absolute token counts run about 25% low.

**Not verified:**
- Claude's current tokenizer (I used the legacy one).
- The size of the tool schema.
- The semantics of context editing.
- The roofline itself; it is a model, not a measurement.
- The outputs are Claude's, so your model's copying rate, and therefore suffix acceptance, will differ.

Sources:
- [Anthropic prompt caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)
- [Anthropic context editing](https://platform.claude.com/docs/en/build-with-claude/context-editing)
- [OpenAI prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching)
- [OpenRouter GPT-5.6 notes](https://openrouter.ai/docs/cookbook/evaluate-and-optimize/model-migrations/gpt-5-6)
- [Nadir: Pay to Forget](https://getnadir.com/blog/context-editing-clear-tool-uses-cache-write-cost/)
- [Claude Code Read dedup issue 88118](https://claudeissues.com/issue/88118-read-dedup-does-not-account-for-posttooluse-updatedtooloutput-repeated-reads-byp)
- [Claude Code stale-read issue 60684](https://claudeissues.com/issue/60684-bug-read-tool-returns-file-unchanged-after-external-on-disk-edits-serving-a-stal)
- [SWE-bench experiments](https://github.com/SWE-bench/experiments)
- [The Complexity Trap](https://arxiv.org/pdf/2508.21433)
- [SuffixDecoding](https://arxiv.org/html/2411.04975v2)
- [vLLM suffix decoding API](https://docs.vllm.ai/en/stable/api/vllm/v1/spec_decode/suffix_decoding/)
- [vLLM speculative decoding (suffix defaults)](https://docs.vllm.ai/en/v0.20.2/features/speculative_decoding/)
- [Arctic Inference suffix decoding](https://arcticinference.readthedocs.io/en/stable/suffix-decoding.html)
- [Empirical Study of Speculative Decoding on SE Tasks](https://arxiv.org/pdf/2604.26469)
- [Quest](https://arxiv.org/pdf/2406.10774)
- [UNIQUE top-k sparse attention](https://arxiv.org/pdf/2605.27740)
- [TensorRT-LLM sparse attention](https://nvidia.github.io/TensorRT-LLM/1.3.0rc22/blogs/tech_blog/blog17_Sparse_Attention_in_TensorRT-LLM.html)
- [HiSparse (SGLang)](https://mast.stanford.edu/pubs/hisparse_scaling_sparse_attention_decoding_with_hierarchical_kv_cache_management/)
- [HySparse2](https://arxiv.org/pdf/2609.26368)
- [STS: speculative token sparsity](https://arxiv.org/html/2605.15508)
- [FlashInfer cascade](https://docs.flashinfer.ai/api/python/cascade.html)
- [Don't Break the Cache](https://arxiv.org/pdf/2601.06007)
- [Manus context engineering](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)
- [RAGCache](https://arxiv.org/pdf/2404.12457)
- [RAGBoost](https://arxiv.org/pdf/2511.03475)
- [CacheWeaver](https://papers.cool/arxiv/2606.19667)
- [CacheBlend](https://arxiv.org/html/2405.16444v3)
- [EPIC](https://arxiv.org/abs/2410.15332v3)
- [APE](https://arxiv.org/pdf/2502.05431)
- [Leyline](https://arxiv.org/pdf/2606.01065)
- [KV Cache Editable](https://arxiv.org/pdf/2606.17107)
- [PatchKV](https://arxiv.org/pdf/2609.26219)
- [KVShareArena](https://arxiv.org/pdf/2609.10266)
- [AgentKVShift](https://arxiv.org/pdf/2607.21604)
