I've revised the answer against every point of the check. The headline baseline is now the append-only policy the agent actually ran, not sliding-window clearing. On the client side, most of the gain is prior art. The main new item is a quality measurement of the server-side splice against full recompute, on a real model running real traces. That model is small (135M parameters).

=== CHANGES IN RESPONSE TO THE CHECK ===

| Check point | Response |
|---|---|
| 1. SWE-agent `polling` already gets the result | **Conceded.** The horizon rule gets −23.7% against append-only, and SWE-agent's `polling=10` gets −23.2%. I swept every clearing family over every window size. The best existing-style setting I found is a fixed 5k batch at −26.0%, which is only 3.6% cheaper relative to `polling=10` (0.740 vs 0.768). On the client side, I add no new rule. |
| 2. The sliding baseline is a strawman | **Conceded.** All headline numbers below are against append-only, the policy the agent actually ran. Sliding clearing (+39.7%) appears only as a reference. |
| 3. Anthropic's 20-block lookback | **Confirmed, and worse than the check said.** In my stricter model, cache entries exist only at breakpoints written by earlier requests. With only an end-of-prompt breakpoint, the horizon rule costs +55.9% more than exact billing (the check found +31.6%) and becomes +19% against append-only. `polling=10` falls to −8.5% and the fixed 5k batch to −16.3%. The fix is cheap: one stable breakpoint after the last placeholder, plus one at the first edited position (4 in all, the API maximum). It brings every policy back to within 0.6–1.6% of exact billing: `polling=10` −22.7%, fixed 5k batch −25.6%, horizon −22.5%. Anthropic's docs already advise extra breakpoints when content sits more than 20 blocks back, so this is applied practice rather than a new idea. Still, without it every clearing policy loses most of its saving. |
| 4. The DP is called a "bound" | **Qualified.** It is the optimum among policies that clear all stale outputs at once: −31.3% against append-only for a 5-output window, −35.8% for a 3-output window. Clearing selectively by output size did not beat it in the check's tests. |
| 5. Splice priced at made-up API rates, rotation cost not counted, KV not exact | **Fixed.** The splice is now costed in own-stack GPU-hours, with the key re-rotation counted. Its quality was measured on a real model against full recompute (Idea 3). |
| 6. Output share; OpenAI price | **Accepted.** Output is 22% of the bill under append-only and about 27% under clearing. The OpenAI 0.1x cached-input price is still unverified, so the OpenAI figures are tentative. |

The undersold points still hold:
- Changing the chars-per-token estimate moves every ratio by 1 point or less.
- Bootstrap confidence intervals are about ±1 point.
- The online horizon guess is within 0.5 points of an oracle that knows the true number of remaining turns.

=== IDEAS ===

**IDEA 1: Clear old tool outputs in batches, with breakpoints placed for the lookback (client only, any API; mostly prior art)**
- **Cases covered.** Deletion and compaction of old tool outputs. These are the dominant mid-prompt edit in agent harnesses.
- **Measured on 200 real SWE-agent trajectories.** Anthropic prices, exact billing, which the 4-breakpoint placement achieves within 0.6–1.6% (`billing2.out` (a), (b)):

| Policy (keep last 5 outputs) | Billed input vs append-only | Mean prompt (tokens) | Token hit rate |
|---|---|---|---|
| Append-only (what the agent ran) | 0 | 29.9k | 97.1% |
| SWE-agent `polling=10` (prior art) | −23.2% | 15.7k | 91.8% |
| Horizon rule (round 1) | −23.7% | 14.0k | 89.9% |
| Fixed 5k batch | −26.0% | 15.2k | 91.8% |
| DP, clear-all-stale optimum | −31.3% | — | — |

  - A 3-output window gets −28% to −31% against append-only at about 13–14.8k tokens of mean prompt. The DP reaches −35.8% there.
- **Quality.** The KV is exact; only the prompt changes. With SmolLM2-135M on 18 traces cut to about 1.5k tokens (`clearq_sum.out`), clearing compared with the append-only prompt gives:
  - 5-output window: KL 0.0080 nats/token, top-1 agreement 98.6%;
  - 3-output window: KL 0.0231, top-1 97.2%.

  This is only a proxy. The deciding test is a SWE-bench Verified A/B of append-only against `polling=10`, which needs a live frontier model.
- **Costs.** No memory or storage. Latency drops because prompts are shorter.
- **What it adds.** The breakpoint requirement, quantified (it is what makes the saving real on Anthropic), and a fair frontier measured on public traces.

**IDEA 2: Splice deletions on the server side, with a measured quality check (own stack or provider)**
- **Mechanism.** Cut the cleared output's KV, compute KV for the short placeholder on the unchanged prefix, and RoPE-shift the later keys. Prior art: Leyline (arXiv 2606.01065, MLA only) and llama.cpp `seq_rm`/`seq_add`.
- **Hit rate.** Only new tokens and 12-token placeholders are computed, so reuse stays near the 97.1% append-only ceiling while the context shrinks. That follows from the design; it was not measured separately.
- **Cost.** Own-stack model: Llama-3-70B shape, BF16 KV, H100, all 200 traces. It counts prefill FLOPs including the re-rotation, decode KV reads, and the decode weight compute that is the same for every policy (`billing2.out` (c), `decode_dilute.out`). GPU-hours against append-only:

| Policy | 45% decode MFU | 15% decode MFU |
|---|---|---|
| `polling=10`, exact | −24.7% | −22.6% |
| Fixed 5k batch, exact | −27.7% | −25.3% |
| `polling=10` + splice | −36.0% | −32.9% |
| Sliding + splice | −41.9% | −38.3% |
| Sliding + splice, full refresh every 8 splices | −14.8% | −13.5% |
| Sliding + splice, full refresh every 4 splices | +13.4% | +12.3% |

  - So the splice adds about 11–14 points beyond the best exact client policy, at the same context.
  - A fixed refresh schedule throws away most of that gain, so any fallback should be triggered per request by measured drift, not by a timer.
  - In round 1's API-price terms, sliding + splice is −41% against append-only. That is hypothetical, because no API sells splicing.
- **Quality, measured.** SmolLM2-135M, dequantized to fp32 with an exact forward pass (`smol.py`), on real traces. Each spliced cache is compared with full recompute of the same cleared prompt (`spliceq_sum.out`, `poll4_sum.out`).
  - Checks passed:
    - splicing out tokens and re-inserting the same tokens reproduces the original cache to 1e-5;
    - the correct RoPE convention scores NLL 3.24, against 4.74 for the wrong one;
    - the numerical noise floor is KL 2.5e-8.

| Mode | KL (nats/token) [95% CI] | Top-1 agreement | ΔNLL on the real next message |
|---|---|---|---|
| Splice, one output per turn (44 points) | 0.0128 [0.0103–0.0155] | 97.9% | −0.013 [−0.026, −0.000] |
| Splice without key shift | 0.0171 | 97.2% | −0.005 |
| Reference: exact prompt showing one more output | 0.0111 | 98.2% | — |
| Splice, batched 4 at a time (18 points) | 0.0057 [0.0039–0.0073] | 98.3% | −0.008 |

  - The splice's error is about the size of moving the window by one output, a change harnesses already accept when they choose a window length.
  - It is also smaller than the effect of choosing to clear at all (0.008–0.023).
  - The key shift matters: without it the error is 33% larger.
  - I measured no harm on the real next message.
- **Limits of this evidence.** The model has 135M parameters, contexts are about 1.5k tokens, messages are capped at 192 tokens, a 3-output window was used, and there are 18 traces. KL is not task success. The deciding run is a 70B-class model replaying these traces at their full ~30k-token length, measuring KL, top-1 agreement and SWE-bench resolution, with the drift-gated fallback.
- **Costs.** No extra memory; the context KV kept is 0.45–0.53x that of append-only. The extra compute is only the re-rotation, which is already counted above.

**IDEA 3: Append-only errata, choosing per edit between an erratum and a rewrite (client only)**
- **Cases covered.** Middle edits, insertions and changed tool outputs.
- **Rule.** Append a diff erratum when W·e + R·e·H is smaller than the rewrite cost (W−R)·suffix. Documents go in first-appearance order, so adding one invalidates 0% instead of 50%.
- **Synthetic replay.**
  - Edits spread across the context: 28.8% saving with full-size errata, 36.1% with diffs.
  - Edits in recent entries: −0.6% and +4.7%. The hybrid removes the round-1 −7.5% loss.
- **Real traces.** Re-views of a region already in context are only 5.1% of tool outputs, and sending them as diffs saves 0.2%. Coding agents are already append-only for changed outputs, so this idea matters only for harnesses that rewrite history.
- **Quality.** The KV is exact. The risk is stale text sitting next to its correction; test it with superseded-fact needle tests.

**IDEA 4: Segment cache with boundary recompute, for reordering and insertion (own stack)**
- **Mechanism.** CacheBlend or EPIC with a deviation gate.
- **Reuse and speed.** About 85% (CacheBlend) or 94% (EPIC) of non-prefix tokens are reused. Reported time-to-first-token gains are 2.2–3.3x and up to 8x.
- **Quality is not equal.** FusionRAG reports that Qwen2.5-7B with 15% recompute only reaches Qwen2.5-3B quality. Test on 2WikiMQA, MuSiQue and LongBench.
- **Costs.** One KV copy per segment: 320 KB per token for Llama-3-70B in BF16, 69 KB per token for DeepSeek-V3's MLA.

**IDEA 5: Choose the storage tier by each model's break-even reuse interval (own stack or provider)**
- **Break-even intervals.** Each model's recompute cost is set against its own storage cost (`idea4.out`). For Llama-3-70B with BF16 KV at 8k tokens: 1.4 min in GPU memory, 6.9 min in CPU RAM, 2.9 h on NVMe. For DeepSeek-V3's MLA at 100k tokens: 13.8 min, 69 min, 28.8 h.
- **Why it matters.** Cache reads are 73% of billed input under append-only, so cheaper reads are the biggest provider-side lever.
- **Quality.** Exact, because only the storage location changes.

**What cannot reach about 100%:**
- **Any growing session.** New content is always a miss; the measured ceiling is 97.1%.
- **Exact KV after a deletion.** It costs a hit-rate drop to 90–92% (Idea 1). Keeping about 97% reuse after a deletion requires inexact KV (Ideas 2 and 4), whose quality has been measured only on a 135M model.
- **Plain API users.** They get only Ideas 1 and 3, and Idea 1 is essentially SWE-agent `polling` or Anthropic's `clear_at_least` plus correct breakpoint placement.
- **Output.** Output tokens (22–27% of the bill) are untouched.
- **Agent behaviour.** The replays hold the agent's actions fixed, so behaviour changes under a different context are not measured.

=== NOTES ===
- **Assumptions.** Tokens estimated as chars/3.5; a 2,500-token tool prefix; the TTL never expires inside a trace; own-stack runs at 45% MFU for prefill and 70% of HBM bandwidth.
- **Reproduction.** All work is in `/home/user/SomeRepository/engine/runs/climb_ctxcache/round2/fix/`, and `README.md` lists the commands.
  - I re-ran `billing2.py` and got byte-identical output. The splice and clearing summaries also re-ran identically from their stored outputs.
  - The `traces.jsonl` sha256 matches round 1.
  - The model weights come from a PyPI wheel, checked by sha256 (`get_model.sh`).

Sources:
- [Leyline](https://arxiv.org/pdf/2606.01065)
- [SWE-agent history processors (polling)](https://swe-agent.com/latest/reference/history_processor_config/)
- [SWE-agent PR #1580](https://github.com/SWE-agent/SWE-agent/pull/1580)
- [Anthropic context editing](https://docs.claude.com/en/docs/build-with-claude/context-editing)
- [Anthropic prompt caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)
- [CacheBlend](https://arxiv.org/html/2405.16444v3)
- [EPIC](https://arxiv.org/abs/2410.15332v3)
- [FusionRAG](https://arxiv.org/pdf/2601.12904)
- [SWE-bench experiments](https://github.com/SWE-bench/experiments)

HONEST GAIN:
- **Plain API, against the append-only policy the agent ran.** Batch clearing saves 23–26% of billed input, which existing SWE-agent `polling` already achieves (the gain over it is about 3.6% relative). It only holds on Anthropic with the 4-breakpoint placement; with a single end breakpoint the horizon rule costs more than append-only (+19%).
- **Own stack.** Splicing adds 11–14 points: −33% to −42% GPU-hours against append-only, compared with −23% to −28% for exact clearing.
- **Splice quality.** Its measured error (KL 0.006–0.013, top-1 98%, no NLL harm) is about the size of a one-output window change, on a 135M model. A 70B-class run is still needed.