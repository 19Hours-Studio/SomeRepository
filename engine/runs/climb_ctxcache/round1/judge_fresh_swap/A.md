I built a different approach and ran it. The current answer tries to push the cache-hit rate toward 100%. Mine drops old tool outputs from the context in batches, on a schedule set by cost, which deliberately accepts a slightly lower hit rate.

On the current answer's own workload this cuts billed input by **47.9%** versus in-place edits. The current answer's honest figure is about 28%. My method saves another 28.6% on top of its errata. On sessions resampled from real SWE-agent steps it saves 19–43%. On the short recorded traces it saves 0%. The billing results are replays I ran myself. The quality results are published measurements and were not re-run here.

=== IDEAS ===

**IDEA 1: Cost-scheduled observation masking (shrink the context instead of appending to it)**

**Why it works.** With prefix caching in place, most of the bill is cache reads, not misses. The cached context is re-read at 0.1x on every turn, so read cost grows with the square of session length. Errata (the current answer's Idea 1) only add tokens that are then re-read forever. The lever is to remove stale tool outputs, and to do it rarely and in batches, because each removal forces one rewrite of everything after it.

**Mechanism.**
- Keep the last `n` tool outputs in full, and leave the assistant's own turns untouched.
- When it pays, replace every older tool output in one go with a roughly 15-token stub ("Old output omitted (N lines)").
- This is a batch-ordering problem, so the standard economic-order-quantity formula gives the best batch size: K\* = √(2(W−R)·n·(a+o) / (R·(o−s))).
  - W and R are the full and cached prices; a is assistant tokens per turn, o is tool-output tokens per turn, s is the stub size.
  - For Anthropic (W=1.25, R=0.1) with n=5, K\* ≈ √(23n) ≈ 11.
- A version with no settings to tune uses the same break-even logic as ski rental:
  - each turn, add R × (stale tokens still in full) to a running total;
  - mask as soon as that total reaches (W−R) × (the tokens that masking would rewrite);
  - then reset the total.
- The KV state is exact: the model computes exactly the tokens that are sent.

**Cases covered.**
- **Changed tool outputs and middle edits:** the new value is appended, and the stale copy is masked in the next batch.
- **Insertions:** appended at the end.
- **Deletions:** handled by masking itself.
- **Reordering:** not covered here; see Idea 2.

**Measured results** (`experiments.out`, Anthropic prices, n=5):

| Workload | Policy | Hit rate | Cost vs reference |
|---|---|---|---|
| Current answer's workload: 50 turns, 2,300-token entries, edit every 5 turns, full-size errata, 200 seeds | In-place edits | 0.890 | 751k (reference) |
| | Errata (current answer) | 0.963 | −27.0% |
| | Mask every turn (old SWE-agent 0.7 behaviour) | 0.606 | +0.9% (costs more) |
| | Ski-rental rule = closed-form K\*=12 = best fixed K | 0.899 | **−47.9%** (−28.6% vs errata) |
| | Anthropic-style `clear_tool_uses` (trigger 100k, keep 3, at least 20k) | 0.940 | −40.9% |
| Same, 100 turns | Ski-rental rule | 0.918 | −68.1% (−50.8% vs errata) |
| Real SWE-agent steps resampled into 50-step sessions (19 public trajectories; mean tool output 288 tokens) | Ski-rental, n=5 / n=10 | 0.93 / 0.94 | −19.5% / −8.7% vs append-only |
| Same, 100 steps | Ski-rental, n=5 / n=10 | 0.95 / 0.95 | −39.3% / −29.7% (OpenAI prices: −42.8% at n=5) |
| Real trajectories as recorded (4–21 steps) | Ski-rental | — | 0% (never triggers); masking every turn costs +80% |

In the resampled sessions the context never reaches 100k, so a `clear_tool_uses` setup triggered at 100k never fires and saves 0%.

**Cost, memory and latency.**
- The ski-rental rule matched or beat the best fixed batch size found by search, so no tuning is needed.
- Peak context fell from 143k to 54k tokens on the current answer's workload. That means about 2.6x less KV held per session and faster prefill on normal turns.
- About once every K turns there is one extra prefill of roughly n·(a+o) tokens (about 12k here).

**Where it runs.**
- On the client, with any API.
- As a provider-side context-management strategy, for example a "cost-optimal" mode replacing fixed trigger and `clear_at_least` thresholds.
- On your own stack: the same formula applies with W/R set to the real ratio of recompute cost to cache-hit cost.

**Quality.**
- At every turn, this policy shows a superset of what a plain last-n masker shows: between n and n+K−1 full outputs. It always shows a subset of the full history.
- The Complexity Trap paper (NeurIPS'25) found that last-n masking on SWE-bench Verified roughly halves cost relative to the raw agent while matching or exceeding LLM summarization's solve rate. For Qwen3-Coder 480B it was 52% cheaper than the raw agent and 2.6% better on solve rate.
- So quality is expected to fall between masking and full history, but this is not proven.
- **Test:** a paired A/B on SWE-bench Verified with four arms: raw, mask(n, K=1), mask(n, K\*) and ski-rental. Use McNemar's test on solve rate, and measure cost from `cache_read_input_tokens` and `cache_creation_input_tokens`, because masking can also change trajectory length. This needs a real model and was not run here.

**Prior art and what is new.**
- Already exists: SWE-agent's `polling` option (a fixed K with no rule for choosing it); Anthropic's `clear_tool_uses` with `trigger` and `clear_at_least` (fixed, size-driven thresholds); Complexity Trap (masking quality); "Don't Break the Cache" (caching for agents).
- New here:
  - the closed-form K\* and the tuning-free trigger, which matched or beat the best fixed K;
  - evidence that masking every turn or triggering on context size leaves 7–40 points of saving unused;
  - a correction to the current answer: compaction is driven by cost, not just by the context limit.

**IDEA 2: For reordered documents, choose by cost, not by hit rate**

**Mechanism.** There are three ways to handle a document set that changes and reorders every turn:
- **Rebuild:** keep the system prompt and history cached, and send this turn's documents in relevance order after them. This is the usual practice.
- **Pin:** append each document once, at its first appearance, and later refer to it by id. Reordering then costs nothing.
- **Pin + evict:** pin, and mask documents unused for m turns, using Idea 1's trigger.

**Measured results** (`rag.out`, 50 turns, k=5 documents of 600 tokens, 200 seeds; p_reuse is the chance a retrieved document was used recently):

| p_reuse | Rebuild | Pin | Pin + evict |
|---|---|---|---|
| 0.6 | hit 0.748 (reference) | hit 0.962, +22% cost | +13% cost |
| 0.8 | reference | −17.8% | −15.3% |

The policy with the highest hit rate is the most expensive unless reuse is above about 0.7. So pin only when the expected future retrievals × (W−R) exceed R × the turns the document stays in context.

- **Cases covered:** reordering and insertion of documents.
- **Where it runs:** client only. Memory scales with how many documents are pinned.
- **Quality:** pinned documents sit far from the question, so the "lost in the middle" effect applies. Test on multi-turn RAG QA and LongBench against rebuild. Not run here.

**What cannot reach about 100%, honestly:**
- **Exact middle edits.** With causal attention, every token after an edit really changes. An exact result needs recompute, and approximate reuse (CacheBlend, EPIC, Leyline) loses quality.
- **New content.** It is always a miss, so a session whose context keeps growing has a floor of about 96% hit rate even with no edits.
- **My own methods.** They deliberately lower the hit rate to 0.90–0.95 because that is cheaper. Hit rate near 100% and lowest cost conflict, as the RAG results show. Only the reused prefix is 100% hit and exact.
- **Short sessions** (under about 15 steps) gain nothing.

=== NOTES ===
- To reproduce, run `python3 experiments.py` (about 3.5 min) and `python3 rag.py` in `/home/user/SomeRepository/engine/runs/climb_ctxcache/round1/fresh/`. The code is in `sim.py`, the data in `data/swea_steps.json`, and `README.md` explains the setup.
- My simulator gives −27.0% for errata on the current answer's workload, against −28.0% in the check's corrected replay. The small gap comes from splitting each entry into two segments.
- **Limits of the data:** tokens are estimated as characters/4. The real trajectories are short demos, so the 50- and 100-step sessions are resampled from their steps, which breaks the correlation between steps.
- **Not modelled:** output tokens, cache TTL expiry, and any change in agent behaviour caused by masking.
- The quality evidence is published (Complexity Trap), not re-run: model weights are blocked here.

Sources:
- [The Complexity Trap (arXiv 2508.21433)](https://arxiv.org/abs/2508.21433)
- [NeurIPS 2025 listing](https://neurips.cc/virtual/2025/131688)
- [Anthropic context editing](https://platform.claude.com/docs/en/build-with-claude/context-editing)
- [Don't Break the Cache (arXiv 2601.06007)](https://arxiv.org/pdf/2601.06007)
- [Observation masking guide](https://agentpatterns.ai/context-engineering/observation-masking/)
- [SWE-agent repo (trajectories, `polling` docstring)](https://github.com/SWE-agent/SWE-agent)
- [CacheBlend](https://arxiv.org/html/2405.16444v3)
- [EPIC](https://arxiv.org/abs/2410.15332v3)
- [Leyline](https://arxiv.org/pdf/2606.01065)
- [Anthropic prompt caching docs](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)