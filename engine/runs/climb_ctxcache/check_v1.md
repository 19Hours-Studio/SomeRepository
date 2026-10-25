The answer's numbers all reproduce: every script re-runs and gives byte-identical output, and the data hash matches. But the headline −45% is measured against per-turn sliding clearing. The traced agent never ran that policy, and it costs 39.7% more than append-only. A clearing option SWE-agent already ships gets the same result.

## 1. Re-derived numbers

I copied all scripts into `check1/rerun/` and re-ran them. The sha256 of `traces.jsonl` matches, and all six `.out` files are identical to the answer's. My own probes are in `check1/exp/`, and the summary is in `check1/REPORT.md`.

**Numbers that hold:**
- **Averages:** 61.1 requests per trace and a 29.9k-token mean prompt.
- **Idea 1 table:**
  - sliding is +39.7% vs append-only;
  - horizon rule: −45.4% vs sliding (−41.0% at OpenAI prices) and −23.7% vs append-only;
  - fixed 5k batch: −47.1% and −26.0%;
  - DP: −50.9% and −31.3%;
  - token hit rates 72.5%, 89.9% and 91.8%, against a 97.1% ceiling;
  - 60.4% with a 10-output window.
- **Bootstrap 95% CIs over the 200 traces:** horizon vs sliding −46.4% to −44.3%; vs append-only −25.1% to −22.2%. These are tight.
- **Token estimate:** at 2.8 or 4.2 chars per token instead of 3.5, every ratio moves by 1 point or less (`chsens.out`).
- **Superset check:** 0 violations is correct. It holds by construction, though, since the rule only ever clears from sliding's set, so it is not an empirical finding.
- **Other ideas:**
  - Idea 3's splice: −58.0%.
  - Idea 2: delta re-views save 0.2%; the 5.1%, 71% and 0.177 figures hold; the synthetic table (28.0%, 36.1%, −7.5%, hybrid −0.6%) and the break-even values of 1,137 and 45 reproduce.
  - Idea 5 tier table: holds; 320 KB per token and 69 KB per token check out, and 6.6 s per 1M tokens is consistent with about 50 GB/s over PCIe.

## 2. Unfair or unsupported points

1. **Missed prior art that matches the result (the main problem).** SWE-agent's `LastNObservations` processor has a `polling` parameter. Its docs say the processor breaks prompt caching and offer polling as the workaround. I emulated it:

   | Policy | vs sliding | vs append-only | Mean prompt (tokens) |
   |---|---|---|---|
   | Answer's horizon rule | −45.4% | −23.7% | 14.0k |
   | SWE-agent `polling=10` | −45.0% | −23.2% | 15.7k |

   `polling=10` costs the same within 0.4 points and shows the model more context. Anthropic's `clear_at_least` is the same idea, and the answer's own fixed 5k batch beats the "parameter-free" rule.
   - The horizon rule's gain over existing practice is therefore about 0 to 2 points, not 45.
   - What is new is the DP bound (−50.9%) and the measurement on real traces.
   - The answer gives the sliding baseline as "SWE-agent 0.x" and does not mention the 1.x `polling` option.

2. **The baseline is a policy nobody runs with caching on.** The traced agent ran append-only: I found no elision placeholders in any of the 200 traces. Sliding clearing with a cache is a dominated policy, at +39.7% vs append-only.
   - The quality-equivalent headline (−45%) is against that strawman.
   - Against what the agent actually ran, the saving is −23.7%, with less than half the context (14.0k vs 29.9k tokens) and quality not measured.
   - The "60.4% with a 10-output window" figure is inflated the same way: vs append-only it is only −12.6%.

3. **Unstated requirement: Anthropic's ~20-block cache lookback.** The replay assumes a hit at any longest common prefix. With only an end-of-prompt breakpoint, the batch clears land more than 20 blocks back:

   | Policy | Change in cost | Effect on headline |
   |---|---|---|
   | horizon | +31.6% | −45.4% shrinks to −28.1% vs sliding, about append-only's cost |
   | fixed 5k batch | +12.1% | |
   | `polling=10` | +19.2% | |

   Sliding and append-only are unaffected. The fix is free: at each clear, write a second breakpoint at the start of the kept window and keep it there. The answer has to state this for the −45% to hold on Anthropic. OpenAI's automatic caching has no lookback limit.

4. **The DP is called a "bound".** It is only optimal within the policy family that clears all stale outputs at once. I tested size-selective clearing and it did not beat it (−38% to −42% vs sliding), so the label is close to right but should be qualified.

5. **Idea 3's −58% is in hypothetical provider prices.** No API sells splicing, and on your own stack the 1.25 and 0.1 multipliers are not compute costs. The RoPE re-rotation cost is not counted, and the KV is not exact.

6. **Minor:**
   - Output's share of the bill is 22% under append-only. It rises to about 27% under clearing, because input shrinks.
   - The OpenAI 0.1x cached-input price is flagged as unverified; treat the OpenAI column as tentative.

**Where the answer undersells itself:**
- Its results do not depend on the tokenizer estimate (±1 point).
- The CIs are about ±1 point.
- The online rule is within 0.5 points of an oracle that knows the true remaining turns, so the "H = requests so far" guess is not a weakness.

## 3. Where a larger honest gain is likely

- **Fair client-side comparison.** Compare a tuned `polling` or `clear_at_least` against the DP. The remaining client-side headroom is about 4 to 6 points (−45% to −51% vs sliding), so this lever is nearly used up.
- **Own stack: splice plus a quality gate.** This is the only regime that clearly beats client-side clearing: 28.5M vs 33.3M units, about 15% below the DP and −41% vs append-only. It is worth it only if a KL or top-1 agreement test against full recompute shows the inexact KV is harmless. Run that test on an open model replaying these exact traces.
- **Cost against quality.** Append-only shows 2.1x the context for +31% cost. A SWE-bench Verified A/B of append-only vs `polling=10` would decide whether the 24% saving is real or paid for in resolved issues. Without that, the 24% figure has no quality backing.

Sources:
- [SWE-agent history processors docs](https://swe-agent.com/latest/reference/history_processor_config/)
- [SWE-agent PR #1580 (polling)](https://github.com/SWE-agent/SWE-agent/pull/1580)
- [Helicone context-editing docs](https://docs.helicone.ai/gateway/concepts/context-editing)
- [Agno Anthropic context management](https://docs.agno.com/models/providers/native/anthropic/usage/context-management)
- [Claude context editing](https://platform.claude.com/docs/zh-TW/build-with-claude/context-editing)
- [Context engineering blog](https://www.developersdigest.tech/blog/context-engineering-for-agents-explained)

HONEST GAIN: −45.4% billed input vs per-turn sliding clearing reproduces (CI −46.4% to −44.3%), but existing SWE-agent `polling=10` gets −45.0%, so the gain beyond prior art is about 0–2 points. Against the append-only policy the agent actually ran it is −23.7%, at less than half the context and with untested quality. On Anthropic it needs a second cache breakpoint, or it falls to −28%.