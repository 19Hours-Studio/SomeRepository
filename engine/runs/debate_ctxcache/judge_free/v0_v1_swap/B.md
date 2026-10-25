=== IDEAS ===
IDEA 1
NAME: Append-only errata with ski-rental compaction
MECHANISM: This runs on the client only and works with any API. Never change content that has already been sent. Express a middle edit, a changed tool output or an insertion as a short tagged erratum at the end of the prompt, for example "[supersedes tool_result #17]: …". Sort documents into a fixed order, such as by content hash, and serialize JSON with sorted keys, so that reordering becomes an exact prefix match. Do a real in-place rewrite (compaction) only when the running cost of the errata reaches the one-time cost of rewriting the suffix. That is the ski-rental rule, and it costs at most 2x the best possible schedule. With Anthropic's prices (cache write 1.25x the base input price, cache read 0.1x), an erratum of e tokens placed after an edit at position p in an N-token context breaks even with a rewrite only after T* = (1.25(N−p) − 1.25e)/(0.1e) turns. For N=100k, p=50k and e=500 that is 1,238 turns; for an edit near the end (p=90k, e=2k) it is 50 turns. So the erratum is almost always cheaper, and compaction is driven by the context-window limit, not by cost. In a 50-turn synthetic agent replay with 2k-token tool outputs and an earlier tool output changing every 5 turns, the token hit rate rose from 92.9% to 99.75% and billed input fell from 604k to 365k units (−40%). Tokens are exactly what the model would compute, so the KV state matches full recomputation exactly. The only quality risk is semantic: stale text stays in the prompt next to its correction.
VALUE: This gives a hit rate near 100% for edits, tool outputs and insertions, and for reordering of document sets that repeat, at no infrastructure cost. In the replay it cut input cost by about 40% against append-and-edit prefix caching. It extends Manus's "append-only context" guidance with a cost-optimal rule for when to compact. Quality has to be tested as an A/B on agent traces, for example SWE-bench success rate and needle-in-a-haystack tests with superseded facts. That test needs a real model and was not run here.

IDEA 2
NAME: Hole-punch deletes via block-table edits
MECHANISM: This needs your own serving stack or provider-side changes, and would be exposed as a new API operation such as `delete_span(id)`. The most common mid-prompt change in agents is deletion: clearing old tool results or compaction. Provider "context editing" features currently throw away the cached prefix at that point. Instead, drop the deleted span's paged-KV blocks from the request's block table and keep every later block as it is. New tokens either continue after a gap in position IDs (PyramidKV-style) or have their keys rotated back into a dense range with a delta RoPE rotation (HERMES and KV Packet rotation). The cost is zero recompute and zero extra memory, and the freed blocks are returned to the pool. The hit rate on the remaining tokens is 100%, but the result is not exactly what full recomputation gives. Tokens after the hole still carry information they absorbed from the deleted span. That is often harmless or even useful for compaction, but harmful when the deleted text was wrong, so pair it with an erratum from Idea 1. Prior art: llama.cpp context shift, and KV-eviction methods (StreamingLLM, H2O, SnapKV), which use the same mechanism to choose tokens heuristically. What is new is driving it from an explicit edit request and billing it as a cache hit.
VALUE: Deletions and compaction become cache hits at 0.1x instead of a rewrite of the whole suffix at 1.25x, a 12.5x cheaper suffix. Quality test: KL divergence and top-1 agreement of next-token distributions against full recomputation on real agent traces, measured with the gap and the rotation variants. This needs a real model.

IDEA 3
NAME: Segment cache with boundary recompute
MECHANISM: This runs on your own stack, for example LMCache's CacheBlend in vLLM, or provider-side. Cache the KV of each document or tool output on its own, keyed by content hash. Compute it after the real shared system prompt (APE's "shared prefix") so it differs less from in-context KV. When reusing a segment at a new position, rotate its RoPE positions and recompute only the tokens whose KV deviates most. CacheBlend recomputes about 15% of tokens and reports a 2.2–3.3x faster time-to-first-token with same-quality answers on RAG question answering. EPIC recomputes only the first few tokens of each chunk (about 32 of 512 tokens, roughly 6%, so about 94% effective hit) and reports up to 8x faster time-to-first-token with "negligible" loss. Add a deviation gate: if the layer-1 deviation (the CacheBlend signal) is above a threshold, fall back to exact recompute. Covered cases: reordering, insertions and changed segments. Only the changed segment and its boundary tokens are recomputed. Storage grows with one KV copy per unique segment: 320 KB per token for Llama-3-70B in BF16, 69 KB per token for DeepSeek-V3's MLA. Latency adds a PCIe load of about 6.6 s per 1M tokens of 70B BF16 KV.
VALUE: About 85–94% of non-prefix tokens are served from cache, and prefill compute falls about 3–7x against exact prefix caching on RAG and reordered workloads. Quality is not exact. The SIGMOD'26 Fusion-RAG paper and AgentKVShift report a remaining gap on multi-hop and agent-memory tasks. Quality test: run it against full recomputation on 2WikiMQA and MuSiQue (multi-hop QA), on LongBench, and on real agent traces.

IDEA 4
NAME: Storage-priced retention, not token-priced hits
MECHANISM: This runs on your own stack or provider-side. At high hit rates, the real cost of a hit is storing the KV, not computing it. Recomputing a token of a 70B model costs about $0.175 per 1M tokens (H100 at $2/h, 45% compute utilization). Holding the same KV for one hour costs about $8.2 per 1M tokens in GPU memory (HBM), $1.6 in CPU RAM (DRAM) and $0.07 on NVMe SSD. So a 1h DRAM-resident cache only pays off if the context is reused about every 6 minutes. NVMe pays off down to about one reuse per 2.5 h. FP8 halves these costs, and MLA models cut them about 4.6x. Retention per prefix should therefore use a ski-rental rule too: keep the KV in a tier while (expected reuses) × (recompute cost) is greater than storage cost × time. The default for long-tail sessions should be NVMe with a long TTL plus MLA or FP8 KV, not GPU memory.
VALUE: This is what makes a hit rate near 100% affordable, at a storage cost about 20x lower than DRAM. It also shows that pushing hit rate and price down together is limited by storage. Prior art is tiered caching (Mooncake, LMCache, HiCache), which per earlier runs gains only about 1.2x over GPU-only prefix caching. The addition is cost-based eviction per prefix.

What cannot reach about 100% without quality loss: any middle insertion or substitution under Ideas 2 and 3. Tokens after the edit really do change, so exact output needs recompute, and only Idea 1's rewrite-free route stays exact. Plain API users can use only Idea 1.

=== NOTES ===
- The arithmetic and the replay are in `/home/user/SomeRepository/engine/runs/vs_ctxcache/baseline/calc.py`. The replay is synthetic; I did not replay the Mooncake trace. It cannot test non-prefix reuse anyway, because its block hashes are chained to the prefix.
- GPU price, utilization and DRAM/NVMe $/GB-h are my assumptions.
- I could not confirm OpenAI's 0.1x cached-input price on an official page.
- All quality claims are the papers' own. They need a run on a real model, which was not possible here because huggingface.co is blocked.

Sources:
- [CacheBlend](https://arxiv.org/html/2405.16444v3)
- [LMCache CacheBlend blog](https://blog.lmcache.ai/2024-10-09-cacheblend/)
- [EPIC](https://arxiv.org/abs/2410.15332v3)
- [APE](https://arxiv.org/pdf/2502.05431)
- [Cache-Craft](https://arxiv.org/abs/2502.15734)
- [Fusion RAG Cache, SIGMOD'26](https://madsys.cs.tsinghua.edu.cn/publication/from-prefix-cache-to-fusion-rag-cache-accelerating-llm-inference-in-retrieval-augmented/SIGMOD26-wang.pdf)
- [AgentKVShift](https://www.alphaxiv.org/abs/2607.21604.md)
- [RelayCaching](https://arxiv.org/html/2603.13289)
- [KVCOMM](https://arxiv.org/pdf/2510.12872)
- [KV Packet](https://arxiv.org/pdf/2604.13226)
- [HERMES](https://arxiv.org/pdf/2601.14724)
- [PyramidKV](https://arxiv.org/pdf/2406.02069)
- [Manus context engineering](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)
- [Anthropic prompt caching docs](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)
- [NVIDIA KV compression blog](https://research.nvidia.com/labs/eai/blogs/kv-cache-compression-and-its-infra-problems/)
- [devtk GPT-5 pricing (unverified)](https://devtk.ai/en/models/gpt-5/)