I rebuilt the answer around one finding: the bill is driven by re-reading the cached context on every request, not by cache misses. Raising the hit rate can save at most 37.9% in the agent replay. Cutting the number of reads and their price takes the saving to about −63%, against the current answer's honest −28%. Everything below comes from arithmetic and replays. Nothing was run on a real model, because huggingface.co is blocked here.

=== IDEAS ===

IDEA 0 (the reframe, measured)
NAME: The hit-rate ceiling
MECHANISM: The input bill has two parts. New tokens are billed at 1.25x. Every request also pays 0.1x for its whole cached prefix again, so read cost grows with the square of the number of turns. I used check0's corrected agent replay: 10k-token system prompt, 50 tool calls of 2,000 + 300 tokens each, and an earlier entry changing every 5th call.
- Current practice (in-place edits) bills 761,649 input units.
- Removing every edit's cache break, which is what a perfect 100%-hit scheme with no quality loss would do, gives 472,855. That is −37.9%, and it is the most that any hit-rate method (errata, splicing, CacheBlend or EPIC) can save on this workload.
- At that floor, about two thirds of the bill (316k of 473k) is 0.1x re-reads of tokens that already hit.
- On the real Mooncake public traces with an infinite exact prefix cache, the token hit rate is 57% (toolagent), 37% (conversation) and 65% (synthetic). Misses are 87–95% of the input bill there. The traces' block hashes are chained, so they cannot show whether those misses are reusable content in a new position or simply new text. The −80% to −88% "100%-hit" bound for those traces is therefore not achievable as shown.
VALUE: Hit rate is the wrong target once append-only gets you to about 96%. The larger gains come from fewer reads per cached token (Idea 2) and a cheaper read (Idea 3). Files: `levers.py`, `trace_bound.py`.

IDEA 1
NAME: Diff errata plus first-appearance order (exact, client only, any API)
MECHANISM: Never change text you have already sent. Express a change as a short diff erratum at the end of the prompt, such as "[supersedes tool_result #17]: diff…". Order documents by when they first appeared, not by hash, so that adding a document invalidates nothing. Compact (rewrite in place) only when the context window forces it.
- **Cases covered:** middle edits, changed tool outputs and insertions. Reordering of documents is covered only if you keep the first-appearance order instead of sending the new order.
- **Hit rate and cost:** −33.6% input with 1,000-token diff errata, −28.0% with full-size errata. Token hit rate rises from 88.7% to 96.3%. Every token sent before is reused at 100% with exact KV.
- **Limit:** about 0% saving, and −7.5% with full-size errata, when edits are to recent entries (check0).
- **Quality:** the model computes exactly what it would from the full prompt. The risk is semantic, because stale text stays next to its correction. Test with an A/B on SWE-bench and with needle tests that use superseded facts.
- **Where it runs, and what it costs:** client only, no memory or latency cost. The context grows by about 1,000 tokens per edit.
- **Prior art:** Manus's append-only guidance. What this adds is the corrected cost and its ceiling.

IDEA 2
NAME: Cache-aware turn batching (exact KV, client only)
MECHANISM: Issue independent actions together in one request, as parallel tool calls or ordered batches such as "edit, then run the test". Each batch then pays one prefix read instead of k.
- **Effect on reads:** with k calls per request, re-read cost falls by about k times, whatever the edit pattern.
- **Edit-free session:** k=1.5 saves −22.5%, k=2 saves −36.2%. The gain grows with session length: −15% at 20 calls, −22.5% at 50, −27% at 100.
- **With diff errata:** −48.4% input at k=1.5, −57.6% at k=2.
- **How large k really is:** the one public SWE-agent demo trajectory I could fetch has 11 actions. They group into about 6 requests (create+insert+run, ls+find, open, edit+run, rm+submit), so k≈1.8. That is a single example, not a measurement.
- **Quality:** each request's KV is exact, but the agent's behaviour changes. A dependent action issued too early wastes a call, and the agent decides with less feedback between steps. LLMCompiler reports up to 6.7x lower cost and up to ~9% higher accuracy against ReAct on its own benchmarks; those are best cases. Test: SWE-bench resolve rate, requests per task and tokens per task, with and without a prompt asking for batched independent actions. That needs a real model.
- **Where it runs, and what it costs:** client only, on any API with parallel tool use. No memory cost, and fewer round trips lower latency.
- **Prior art:** parallel function calling and LLMCompiler. What this adds is that, under cached billing, batching cuts the dominant re-read term about k times, and that this is worth more than any hit-rate method on long sessions.

IDEA 3
NAME: Read priced at real cost, with KV parked in DRAM or NVMe during tool gaps (exact; own stack or provider)
MECHANISM: When the model stops on a tool call, the next request's prefix is known: it is the previous prompt plus the model's output. Move that KV out of GPU memory (HBM) into DRAM or NVMe while the tool runs. Reload it layer by layer when the tool result arrives, overlapped with prefill of the new tokens. Then price cache reads from the resulting real cost instead of a flat 0.1x.
- **Where the real cost of a hit comes from** (70B BF16, H100 at $2/h, `op_cost.py`): most of it is holding KV in GPU memory across the gap, not compute. Over a 10–60 s gap, an HBM-resident read costs 7–70% of a full recompute. Parked in DRAM it costs 1.8–17%, on NVMe 0.5–4.4%, and on NVMe even across a 600 s gap 3.9–9.5%. The exact attention of new tokens over the cache is only 0.5–3.8%.
- **Price this supports:** reads at 0.03–0.05x at the same margin as base input, instead of 0.1x. KV kept on NVMe for hours stays cheaper than recompute, so returning sessions get close to 100% hit.
- **Gains, as billed input:** 0.05x reads alone save −19% (in-place edits). Errata plus k=1.5 plus 0.05x saves −63.4%. k=2 with 0.03x saves −72.4%. Including output, the savings are −57.7% and −65.9% (`combo.py`).
- **Quality:** bit-exact KV. Test by comparing logits against a GPU-resident cache; no model risk.
- **Latency:** reloading 100k tokens (32 GB) takes about 0.8 s over PCIe. That hides behind a 2.3k-token prefill (about 2.1 s) but adds about 0.4 s to time-to-first-token for 0.5k-token turns. A single NVMe drive at about 7 GB/s needs about 4.7 s, so stripe 4–8 drives or stage through DRAM.
- **Storage:** about 0.33 MB per token.
- **Prior art:** InferCept (keep, swap or discard KV during tool calls), Continuum (time-to-live pinning in GPU memory for tool calls), AttentionStore, and Gemini's explicit cache, which charges a storage fee of $4.50 per 1M tokens per hour. By my estimate NVMe holds 70B KV for about $0.07 per 1M tokens per hour, roughly 64x less. What this adds is the cost comparison showing that GPU-memory residency, not compute, is most of a hit's cost, and the read price that follows from it.

IDEA 4 (weaker, lossy)
NAME: Digest side-calls
MECHANISM: Read each bulky tool output once, in a short side request off a small shared prefix, and keep only a 300-token digest in the main thread.
- **Cost:** −53.8% input, but output tokens cost 5x and the digests double output spend, so the total saving is only −40%.
- **Context size:** final context shrinks from 134k to 49k tokens.
- **Quality:** lossy. Test with an A/B on task success.
- **Use:** only when the context window is the binding limit.

Own-stack approximate reuse (Leyline-style span splicing, CacheBlend, EPIC) can only turn misses into hits, so Idea 0's ceiling bounds it: at most −37.9% on the agent replay. Its quality is not exact; FusionRAG reports that at 15% recompute a 7B model only recovers to 3B-level quality. Use it only for retrieval workloads that reorder shared documents across users, and gate it on measured KL divergence against full recomputation.

**What cannot reach about 100% hit:**
- New tokens in every turn always miss, which caps this session at about 96% token hit.
- Exact reuse after a middle edit is possible only through errata.
- Reordered prompts can be served exactly only if you keep the first-appearance order instead of sending the new order.
- Plain API users cannot change the read price (Idea 3).
- Batching is limited by real dependencies between actions.

=== NOTES ===
- **Files** (in `/home/user/SomeRepository/engine/runs/climb_ctxcache/round1/reframe/`): `README.md`, `levers.py`, `combo.py`, `noedit.py`, `op_cost.py`, `trace_bound.py`, each with a `.out`. Running `levers.py` reproduces check0's corrected numbers.
- **Assumptions:** GPU, DRAM and NVMe prices; the 5x output ratio (Sonnet, $15 vs $3); k≈1.5–2 from one demo trajectory; layer-wise reload overlap.
- **Needs a real model:** the quality effect of batching on agents, errata quality, and the KL gate for approximate reuse. I also have no measured distribution of agent tool-gap lengths.

Sources:
- [Anthropic prompt caching docs](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)
- [Mooncake traces](https://github.com/kvcache-ai/Mooncake)
- [SWE-agent demo trajectories](https://github.com/SWE-agent/SWE-agent)
- [LLMCompiler](https://arxiv.org/abs/2312.04511)
- [ICML LLMCompiler](https://proceedings.mlr.press/v235/kim24y.html)
- [InferCept](https://arxiv.org/pdf/2402.01869)
- [Continuum](https://arxiv.org/html/2511.02230v2)
- [LMCache](https://arxiv.org/html/2510.09665v2)
- [Gemini caching pricing (fast.io)](https://fast.io/resources/gemini-context-caching/)
- [Gemini caching forum](https://discuss.ai.google.dev/t/gemini-2-5-pro-context-cache-pricing-per-request-vs-cumulative-token-counting/92919)
- [Doubleword SWE-bench agents](https://blog.doubleword.ai/swe-bench-pro-64-deepseek-agents)
- [TRAJECT-Bench](https://arxiv.org/pdf/2510.04550)
- [CacheBlend](https://arxiv.org/html/2405.16444v3)
- [FusionRAG](https://arxiv.org/pdf/2601.12904)
- [Leyline](https://arxiv.org/pdf/2606.01065)
- [Manus](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)