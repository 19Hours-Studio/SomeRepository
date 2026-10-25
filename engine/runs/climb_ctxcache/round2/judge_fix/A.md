I replaced the synthetic-only evidence with a replay of 200 real SWE-agent trajectories, and I fixed or answered every point of the check. On real traces, almost all mid-prompt edits come from the harness clearing old tool outputs, not from tool outputs changing. A cache-aware clearing schedule cuts billed input by **45–47% against the common sliding-window clearing**, and the model never sees less context than under that window. It is also 24–26% cheaper than keeping everything. A near-100% token hit rate is impossible for any growing session: the measured ceiling is 97.1%, and the misses are new content.

=== IDEAS ===

**IDEA 1: Clear old tool outputs in price-timed batches, not one per turn (client only, any API)**

- **The real problem.** Agent harnesses keep prompts short by replacing old tool outputs with a placeholder. Examples: SWE-agent 0.x "last 5 observations", OpenHands condensers, Anthropic `clear_tool_uses`. A sliding window clears one output per turn. Each clear changes the middle of the prompt, so every turn rewrites the whole suffix at 1.25x.
- **The rule.** Clear all stale old outputs at once, and only when it pays:
  - Clear when R·S·H ≥ (W−R)·X.
  - S = stale tokens that would be removed; X = tokens that must be re-sent after the first cleared spot.
  - H = expected remaining requests. Online, guess H = requests so far.
  - W = 1.25 (write), R = 0.1 (read) on Anthropic; W = 1.0 on OpenAI.
- **Fair comparison.** Every scheduled prompt shows the model a superset of what the sliding window shows. `rule.py` checks this: 0 violations in 24,442 requests.
- **Measured on 200 real trajectories** (61 requests and ~29.9k-token prompts on average, Anthropic prices; OpenAI prices in brackets):

| Policy | Billed input vs sliding | Billed input vs append-only | Token hit rate |
|---|---|---|---|
| Sliding last-5 clearing | — | +39.7% | 72.5% |
| Horizon rule (online, no tuning) | −45.4% [−41.0%] | −23.7% | 89.9% |
| Fixed batch ≥5k tokens | −47.1% [−43.3%] | −26.0% | 91.8% |
| Offline optimum (DP, bound) | −50.9% | −31.3% | — |

  - With a 10-output window instead of 5, the horizon rule saves 60.4% against sliding.
- **Cases covered.** Deletions and compaction of tool outputs, which are the dominant mid-prompt edit in these traces.
- **Quality.** The KV state is exact, because every request is an ordinary prompt. The model sees at least as much as under sliding, so quality should be the same or better, but that is not guaranteed. Against append-only it sees less: about 14k vs 29.9k tokens. Test by running SWE-bench Verified resolution rates under both schedules. That needs a live model and was not run.
- **Costs.** Zero memory or storage. Latency is lower than sliding because there are fewer prefill rewrites.
- **Prior art.** Anthropic's `clear_at_least` and `trigger` parameters already exist so that clearing can be made "worth" the cache break. This idea adds:
  - a price-derived, parameter-free trigger;
  - the offline optimum as a bound (the online rule gets within about 5 points of it);
  - measurements on public traces.

**IDEA 2: Append-only errata with a per-edit choice between erratum and rewrite (client only)**

- **Mechanism.** For an edit, insertion or changed tool output, either append a tagged erratum (written as a diff) or rewrite in place, whichever is cheaper:
  - erratum: W·e + R·e·H;
  - in-place rewrite: (W−R)·suffix, with H guessed online as elapsed turns.
  - Documents go in first-appearance order, not hash order. Adding one document then invalidates 0% instead of 50% (check0).
- **Synthetic replay**, billing corrected, 200 seeds (`replay_v1.out`). The diff erratum size is measured, not assumed: real re-view diffs are 0.177x the full output (`diffstat.out`).

| Where edits land | Erratum size | Pure erratum saving | Hybrid saving |
|---|---|---|---|
| Spread across context | full (2,300 tokens) | 28.0% | 28.8% |
| Spread across context | diff (410 tokens) | 36.1% | 36.1% |
| Recent entries | full | −7.5% | −0.6% |
| Recent entries | diff | +4.7% | +4.7% |

  - The hybrid removes the check's +7.5% loss case.
  - Corrected break-even turns are 1,137 and 45, as the check said.
- **Real-trace reality check.** In SWE-agent traces, re-views of a file region already in context are only 5.1% of tool outputs. 71% of them are identical to what is already there, and they average 295 tokens. Sending them as diffs saved only 0.2% (`traces.out`, "delta"). Coding agents are already naturally append-only for changed outputs, so this idea matters mainly for harnesses that rewrite history.
- **Quality.** The KV state is exact, and 100% of previously sent tokens hit the cache. The risk is semantic: stale text sits next to its correction. Test with superseded-fact needle tests and an A/B on agent tasks, both of which need a live model.

**IDEA 3: Splice deletions on the server side (own stack or provider)**

- **Mechanism.** Drop the cleared span's KV blocks, write only the placeholder, and RoPE-shift the downstream keys.
- **Prior art, credited.** Leyline (arXiv 2606.01065) already does this with replace and remove directives. It reports +11.2 percentage points of hit rate, and its rotation kernel covers MLA only. llama.cpp `seq_rm`/`seq_add` already does it for GQA.
- **What this adds: the dollar value on real traces.** Sliding clearing with a splice costs 28.5M units against 67.9M for sliding (−58%). It is also 23% below Idea 1's horizon rule, at the same context the model sees. The earlier "12.5x" was only the price ratio 1.25/0.1, and I withdraw it.
- **Quality.** Not exact: downstream KV still carries information from the deleted text. The deciding test is next-token KL divergence and top-1 agreement against full recompute, plus SWE-bench resolution. Use a fallback gate: if the divergence exceeds a threshold, use Idea 1's rewrite instead. This needs a real model.
- **Costs.** No extra memory; freed blocks go back to the pool.

**IDEA 4: Segment cache with boundary recompute, for reordering and insertion (own stack)**

- **Mechanism.** CacheBlend or EPIC with a deviation gate, as in the previous answer.
- **Corrected numbers.** About 85% (CacheBlend) or 94% (EPIC) of non-prefix tokens are reused. The reported time-to-first-token gains are 2.2–3.3x for CacheBlend and up to 8x for EPIC. I withdraw the "3–7x compute" figure, which mixed compute fractions with latency numbers. EPIC also reports that CacheBlend's own overhead is 16–63% of its time-to-first-token.
- **Quality is not equal.** FusionRAG reports that Qwen2.5-7B with 15% recompute only reaches Qwen2.5-3B quality. Test on 2WikiMQA, MuSiQue and LongBench against full recompute.
- **Costs.** One KV copy per unique segment: 320 KB per token for Llama-3-70B in BF16, 69 KB per token for DeepSeek-V3's MLA. Loading over PCIe takes about 6.6 s per 1M tokens.

**IDEA 5: Choose the storage tier by each model's own break-even interval (own stack or provider)**

- **Mechanism.** Keep a prefix in a tier while the expected reuse rate is above that tier's break-even rate.
- **Fair per-model comparison.** Each model's recompute cost (including attention, H100 at $2/h, 45% utilization) is set against its own KV storage cost (`idea4.out`). Break-even reuse intervals:

| Model and KV format | Context | GPU memory | CPU RAM | NVMe |
|---|---|---|---|---|
| Llama-3-70B, BF16 KV | 8k | 1.4 min | 6.9 min | 2.9 h |
| Llama-3-70B, BF16 KV | 100k | 2.5 min | 12.4 min | 5.2 h |
| Llama-3-70B, FP8 KV | 8k | 2.8 min | 13.8 min | 5.7 h |
| Llama-3-70B, FP8 KV | 100k | 5.0 min | 24.8 min | 10.3 h |
| DeepSeek-V3, MLA | 8k | 4.0 min | 20 min | 8.3 h |
| DeepSeek-V3, MLA | 100k | 13.8 min | 69 min | 28.8 h |

- **Why reads matter.** In real append-only traces, 0.1x reads are 73% of billed input (`traces.out`). Lowering the cost of a read is the biggest provider-side lever.
- **Prior art and what it adds.** Mooncake, LMCache and HiCache provide the tiers; the addition is cost-based tier choice per prefix. Quality is exact, because this only changes where the KV is stored.

**What cannot reach about 100%:**
- **Any growing session.** New content is always a miss. The real append-only ceiling is 97.1% of tokens.
- **Exact KV after a mid-prompt change.** Ideas 1 and 2 keep the KV exact, but at a hit rate below 100% (Idea 1 at 89.9–91.8%). Ideas 3 and 4 reach high reuse but are not exact.
- **Plain API users** get only Ideas 1 and 2.
- **Input is not everything.** Output is 22% of the bill in these traces, and the cache does not touch it.

=== NOTES ===
- **Assumptions:** tokens estimated as chars/3.5 (no tokenizer could be downloaded here); a 2,500-token tool-schema prefix; the 5-minute TTL never expires inside a trace.
- **Untested here:** the replays hold the agent's actions fixed, so behavioural changes under a different context are not measured. Every quality claim needs a live-model run, which was not possible here.
- **Unverified:** OpenAI's 0.1x cached-input price is from aggregator sites only.

Sources:
- [Leyline](https://arxiv.org/pdf/2606.01065)
- [Anthropic context editing](https://docs.claude.com/en/docs/build-with-claude/context-editing)
- [CacheBlend](https://arxiv.org/html/2405.16444v3)
- [EPIC](https://arxiv.org/abs/2410.15332v3)
- [FusionRAG](https://arxiv.org/pdf/2601.12904)
- [Manus context engineering](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)
- [Anthropic prompt caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)
- [SWE-bench experiments](https://github.com/SWE-bench/experiments)

Everything is in `/home/user/SomeRepository/engine/runs/climb_ctxcache/round1/fix/`; `README.md` has the commands to re-run each result:
- `fetch_traces.py`
- `traces.py`, `traces.out`
- `rule.py`, `rule.out`, `rule_keep10.out`
- `diffstat.py`, `diffstat.out`
- `replay_v1.py`, `replay_v1.out`
- `idea4.py`, `idea4.out`
- `data/traces.jsonl` and its sha256

HONEST GAIN: On 200 real SWE-agent trajectories, price-timed batch clearing cuts billed input by 45.4% against sliding-window clearing (47.1% with a fixed 5k batch), and the model never sees less context. It is 24–26% cheaper than append-only, but shows less context than append-only. The token hit rate rises from 72.5% to 89.9–91.8%, against a 97.1% ceiling. The server-side splice saves 58% against sliding, but its KV is not exact.