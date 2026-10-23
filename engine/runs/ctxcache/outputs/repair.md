I repaired both ideas and kept both anchors. Idea 1 is NICHE: its cost gain is real against exact-match caching, but it adds almost nothing over CacheBlend, and quality was not measured on a real model. Idea 2 WORKS only in long agent sessions (about 100 turns or more) and is NICHE for short ones. All quality numbers are published figures or assumptions, because model weights could not be downloaded here.

I repaired both ideas and kept both anchors. Each now fixes a different failure. One caveat covers everything: these are cost and hit-rate results only. Quality has not been measured on any model, because model weights are blocked here and arXiv full text was also blocked. The work files are `LOG.md`, `model.py`, `model2.py` and `model3.py` in the c2 folder.
=== IDEAS ===
IDEA 1
NAME: Audit-calibrated chunk KV fusion
MECHANISM: The anchor is a closed loop: 1–2% of requests are served by full recompute and also run in shadow through the reused-KV path. The results set the recompute threshold per workload against a measured answer-flip budget (the share of answers that differ from full recompute), instead of a fixed 15% recompute. The repairs are these. (1) The audit compares the whole answer by scoring it token by token under the reused KV, which catches multi-hop failures that first-token KL misses. (2) The token-selection method is pluggable, and a correcting one such as AgentKVShift is needed to get recompute down to about 10%; CacheBlend-style selection loses 47.5% F1 at 10%. (3) It stacks on top of exact-match document reordering (ContextPilot-style), and if the audit says more than 30% recompute is needed it falls back to exact matching. (4) Stored KV sits in a DRAM hot set plus a 4×NVMe array, because the node needs 24–39 GB/s of KV loads at 160 KiB/token (FP8, 70B). At 10% recompute a request costs 271 GPU-ms, against 720 for ContextPilot reordering and 1,003 for plain prefix caching. Certifying a flip rate of 2% or less at 95% confidence takes 148 clean audits, which is about 7.4k requests per calibration window.
VALUE: About 2.6× cheaper per request than the best exact-match practice (ContextPilot reordering) and about 3.7× cheaper than plain prefix caching, with a measured quality bound. It is only about 1.09× cheaper than CacheBlend at 15%, so its value is the guarantee, not the price.

IDEA 2
NAME: Context-length-gated turn collapsing
MECHANISM: The anchor is that the agent stops to observe only when the expected value of seeing the result is worth one more full-context read, priced at C×0.1×p (C is the current context length, p the base input price). The threshold therefore tightens as C grows: early turns observe freely, and turns after about 20–40k tokens are folded into multi-step scripts (k=3 steps per turn). Each script filters its tool outputs down to the lines needed for the next decision, so less text enters the context and every later read shrinks. The design changes are these. Only read-only or idempotent tools are folded. A script stops early as soon as an expectation check fails. Folded batches longer than 5 minutes use the 1-hour cache TTL. On a 40-turn session the gate gives 1.48× and the gate plus 50% filtering gives 1.81×. On a 150-turn session, where reads are 75% of cost, the gate gives 2.02× and gate plus filtering gives 2.42×.
VALUE: About 2.0–2.4× cheaper per long agent task than the plain cached agent loop. That compares with 1.20× for CodeAct's measured 30% turn cut and 0.83× for observation masking once cache rewrites are paid.

=== NOTES ===
**Idea 1**
- **Anchor kept?** Yes, but moved. Prior-art checks show the "deviation gate" itself is already known (CacheBlend, KVBoost, Cache-Craft), so the anchor is now the closed-loop audit, which none of them have.
- **Decisive numbers:**
  - KV size: 160 KiB/token at FP8 (FACT 6, halved from FP16).
  - Hardware: H100 at 1,979 TFLOPS FP8 and 50% MFU (my assumption).
  - Reuse without any recompute: Musique F1 falls from 0.35 to 0.15 (CacheBlend, arXiv 2405.16444).
  - At 10% recompute: AgentKVShift loses 5.9%, CacheBlend loses 47.5% (arXiv 2607.21604).
  - Reordering alone: ContextPilot reaches 34–60% hits with F1 64.15→64.68 (arXiv 2511.03475).
- **Baseline per request served** (from `idea1_calc.py`):

  | scheme | GPU-ms/request | idea at r*=0.10 is |
  |---|---|---|
  | full recompute | 1,141 | – |
  | plain prefix caching | 1,003 | 3.7× cheaper |
  | ContextPilot reordering | 720 | 2.65× cheaper |
  | CacheBlend at 15% | 295 | 1.09× cheaper |
  | AgentKVShift at 10% | 254 | 0.94× (slightly dearer, the 2% audit) |
  | idea at r*=0.10 | 271 | – |
  | idea + ContextPilot | 237 | – |

  At $2.5 per GPU-hour that is about $0.19 per 1k requests against $0.50.
- **Consistency checks:**
  - One NVMe drive fails the load bandwidth; a 4×NVMe array or DRAM passes.
  - Storing a chunk pays off at 0.25 reuses/hour on NVMe and 7.6/hour in DRAM, so this is the admission rule.
  - Output decoding is about half the remaining cost, so the whole-request gain is capped near 2× more even with zero recompute.
  - Tenants with fewer than about 7k requests per window cannot be certified and get the exact-match fallback.
- **Hazards:** Shared chunk KV can be poisoned (HijackKV), so only share it within a tenant, keyed by content hash. Audits must be stratified so rare, heavily interacting chunk sets get sampled. Offline evaluations overstate quality (arXiv 2609.31415), which supports auditing online.
- **Which cases cannot reach ~100%:** ~100% reuse with exact outputs is impossible. Middle edits inside a chunk, and instructions whose meaning depends on order, always need recompute.
- **Deciding unknown:** the answer-flip rate as a function of recompute fraction on real multi-hop traffic.
- **Experiment:** Llama-3.1-70B on Musique, 2Wiki and the operator's own traces, sweeping recompute over {5, 10, 15, 30}% with about 300 queries per point (enough to bound a 1% flip rate at 95%).
- **Closest work:** CacheBlend, EPIC, Cache-Craft, KVBoost, AgentKVShift, ProphetKV and QCFuse. All of them are open-loop.
- **Verdict:** NICHE. It suits own-stack or provider RAG with high traffic.

**Idea 2**
- **Anchor kept?** Yes.
- **Decisive numbers:**
  - Prices: write 1.25×, read 0.1×, output 5× (Anthropic docs, FACT 2).
  - Turn cuts measured so far: CodeAct reaches up to 30% fewer actions (arXiv 2402.01030), and its advantage grows with chain length (FACT 5).
  - In real Claude Code usage, cache traffic is about 89% of the bill, and the long sessions run a median of 237 turns. Both come from secondary sources.
- **Baseline per task completed:**

  | approach | × cheaper than the plain cached loop |
  |---|---|
  | uniform 2× turn cut | 1.41× |
  | CodeAct (30% fewer turns) | 1.20× |
  | observation masking with clears batched, rewrite paid each time (my model) | 0.83× |
  | ReWOO-style plan-everything-upfront | not computed; its 5× token figure is for uncached use |
  | idea, 40 turns (gate only / with filtering) | 1.48× / 1.81× |
  | idea, 150 turns (gate only / with filtering) | 2.02× / 2.42× |

- **Consistency checks:**
  - Batches longer than 5 minutes need the 1-hour TTL.
  - Scripts can raise output tokens by about 120% (AIMultiple); the model does not include this, so it is a hazard.
  - The saving is about $0.41 per task, so the success drop must be close to zero for valuable tasks.
- **Hazards:** acting blind on a wrong branch, and irreversible actions. Both are designed down by folding only read-only tools and stopping early on a failed check.
- **Deciding unknown:** the success drop at k=3 folding beyond the context threshold.
- **Experiment:** paired runs on SWE-style tasks. 1,307 tasks detect a 3-point drop; SWE-bench Verified's 500 only detect about 5 points.
- **Closest work:** CodeAct, ReWOO, LLMCompiler, BATS (it tracks a tool-call budget, not context-dependent read cost) and Anthropic's programmatic tool calling (which already does the in-script filtering). What the idea adds is the gate that tightens with context length.
- **Verdict:** WORKS for long sessions (about 100 turns or more); NICHE for short ones (under 1.5× at 40 turns without filtering). It does not raise the hit rate; it cuts the number of cached reads.

Everything is in `/home/user/SomeRepository/engine/runs/ctxcache/repair/c1/`: the per-round log in `LOG.md`, the full tables in `NOTES.md`, and the cost models in `idea1_calc.py` and `idea2_calc.py`. Nothing was committed.

Sources: [CacheBlend](https://arxiv.org/pdf/2405.16444), [Cache-Craft](https://arxiv.org/abs/2502.15734), [KVBoost](https://arxiv.org/pdf/2608.21362), [AgentKVShift](https://arxiv.org/pdf/2607.21604), [ContextPilot](https://arxiv.org/pdf/2511.03475), [KV-reuse accuracy evaluation](https://arxiv.org/pdf/2609.31415), [HijackKV](https://arxiv.org/pdf/2607.19957), [EPIC](https://proceedings.mlr.press/v267/hu25j.html), [CodeAct](https://arxiv.org/pdf/2402.01030), [ReWOO](https://arxiv.org/pdf/2305.18323), [BATS](https://arxiv.org/abs/2511.17006), [Anthropic prompt caching](https://docs.claude.com/en/docs/build-with-claude/prompt-caching), [89% cache traffic writeup](https://levelup.gitconnected.com/89-of-my-coding-agent-bill-was-cache-traffic-and-most-token-saving-tools-cannot-reach-it-a5c6eb314c9e), [Coralogix session analysis](https://coralogix.com/?p=79565), [AIMultiple code-execution benchmark](https://research.aimultiple.com/code-execution-with-mcp), [KVBoost docs](https://kvboost.readthedocs.io/en/latest/guide/recompute.html).

IDEA 3
NAME: Floating depth-1 override ledger
MECHANISM: Anchor: an edit never rewrites earlier context; it is sent as an appended patch, so the cached prefix stays byte-identical. Repair: patches no longer pile up in history. The client keeps one deduplicated ledger with a single entry per stable section or state key ("§4 now reads…", "plan.status = …"). It places the ledger after the last cache breakpoint, right after the current question, and drops it from the history it sends next turn. Each turn therefore re-pays only the ledger at 1.0× plus the reply tokens. Each key only ever has the original plus one override, so the depth-driven interference measured by PI-LLM and DKI stays at depth 1. The ledger is folded into the document when its spend exceeds one rewrite from the earliest edited position, when it passes 10% of the context, or for free on any turn where the cache has already expired. In the model, a 150k-token agent context with 8k of mutable state at the front (40 calls, 20 state edits) costs $0.0735 per request against $0.336 for inline rewriting. That is 4.6× cheaper and within 6% of the no-edit floor. A 25k-token document with 10 questions and 3 edits comes out 1.46× cheaper with the 10% cap.
VALUE: When the same state or section is edited repeatedly on a hosted API, cost per request falls 2.6–4.6× against inline rewriting, at the same cost as the patch chain coding agents already use (within 4–8%) but with override depth held at 1 instead of the chain's 3–7.

IDEA 4
NAME: Cost-optimal patch folding
MECHANISM: Anchor: edits become structured appended patches, and a full rewrite runs only when the patches cost more than one fresh write. Repair: the fold rule is now ski-rental, which is guaranteed to cost at most 2× what the best possible fold timing would have cost. The client folds once the patches' cumulative extra reads reach the cost of rewriting from the earliest patched position, not from the start of the document. Two triggers are new: a second edit to the same key forces a fold (depth cap 1, because the PI-LLM/DKI evidence shows accuracy on the latest value falls as updates accumulate), and folding is free on any request that would miss the cache anyway (gap longer than the TTL), since that request rewrites everything regardless. Documents are given stable section IDs when they are loaded so patches can address sections. In the model this gives 1.52× (25k document, 10 questions, 3 edits) and 2.66× (120k copilot document, 30 questions, 15 edits) against inline rewriting. The token-weighted hit rate is 96.4%, which is every reusable token; inline gets about 71%.
VALUE: Document sessions with scattered edits on hosted APIs get 1.5–2.7× lower cost per question than inline rewriting, with no more than one override per section. The gain shrinks to about 1.2–1.4× when 30% of gaps between turns exceed the cache TTL.

=== NOTES ===

**Shared basis.**
- **Prices:** Sonnet-class models at $3/M input and $15/M output. Cache writes cost 1.25× (5-minute TTL) or 2× (1-hour), reads 0.1× (FACT 2 / Anthropic docs; Manus quotes $0.30 vs $3).
- **Unit:** cost per request served, averaged over 300 random sessions. Each turn has a 60-token question and a 400-token answer on top of a 3k system prompt.
- **Baselines (client-only):**
  - Inline rewrite with prefix caching: the cheapest and the default for document copilots.
  - Document placed after the history: 2.5–2.7× worse than inline, so dropped.
  - The plain patch chain: shipped practice. Claude Code already injects file-change diffs as appended reminders, and users report the resulting context bloat ([#21650](https://claudeissues.com/issue/21650-bug-system-reminders-for-modified-files-repeat-excessively-consuming-context), [#20850](https://claudeissues.com/issue/20850-bug-title-file-modification-system-reminders-consume-excessive-context)). Manus's [append-only rule](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus) is related.
- **Server side:** CacheBlend, EPIC, ProphetKV and QCFuse (FACTS 3, 4, 12) need your own serving stack and are approximate.
- **What neither idea can do:** document reordering is not covered. The only client-side fix is keeping a fixed canonical order, which is prior art. With reordering in the mix, neither idea reaches about 100%.

**Idea 1: Floating depth-1 override ledger**
- **Anchor kept?** Yes.
- **Decisive numbers:**
  - Scenario E (150k agent context, 8k mutable state at the front, 40 calls, 20 edits): $0.0735 per request. Inline is $0.336, the plain chain $0.0703, the no-edit floor $0.0694.
  - Scenario D (120k document, 30 questions, 15 edits): 2.63× vs inline.
  - Scenario C (25k document, 10 questions, 3 edits): 1.46× vs inline with a 10% cap, but only 1.16× with a 5% cap.
- **Against the best baseline:** about 4–8% more expensive than the plain chain, and its value is quality (depth 1 instead of up to 7).
- **Consistency checks:**

| Limit | Value used | Result |
|---|---|---|
| Context window | E ends at about 171k tokens | Under 200k, passes |
| Cache breakpoints | One per turn | Under the 4-breakpoint limit; 20-block lookback is fine |
| Ledger size | About 3.2k tokens (under 2% of E) | Passes |
| Tokens after the last breakpoint | Billed at 1.0× | Included in the model |
| 5-minute TTL | 30% of gaps expired | Gain falls to 1.43× (D); a 1-hour TTL costs 2× per write |

- **Hazards:**
  - Stale text is still visible. DKI (arXiv 2603.12271) finds the earliest state is recalled well even when the latest is not, so multi-hop questions over superseded text can bring back the old value.
  - Earlier assistant answers in the history may quote stale text, though inline rewriting has the same problem.
  - A bug that leaves the ledger inside the history recreates the depth chain.
- **Deciding unknown:** the accuracy drop on edited-text questions with a depth-1 ledger at the tail, compared with inline editing.
- **Experiment:** run it on a hosted API, which needs no weights. Use a paired McNemar test with 696–1306 questions (to detect a 3-point drop at 8–15% disagreement between arms), for example 100 documents × 10 questions × 2 arms. Estimated cost is about $45 including output.
- **Closest work:** Claude Code's appended diffs, Manus's append-only rule, and Anthropic's context editing. What this adds: the ledger is re-sent each turn rather than accumulated, so override depth stays at 1, and it folds for free when the cache has expired anyway.
- **Verdict:** WORKS for repeated edits to the same keys (agent state, plans, forms, memory). NICHE for one-off document edits.

**Idea 2: Cost-optimal patch folding**
- **Anchor kept?** Yes.
- **Decisive numbers:**
  - C: $0.0272 vs inline $0.0414 (1.52×).
  - D: $0.0664 vs $0.1767 (2.66×).
  - E: only 2.95×, against 4.6× for Idea 1.
  - Depth-cap sweep in E: $0.114, $0.087, $0.077 and $0.070 for caps 1, 2, 3 and unlimited. This is the direct price of quality.
- **Against the best baseline:** at a cap of 1 it costs about 1–7% more than the plain chain in C and D (60% more in E), and its value is depth ≤ 1.
- **Edge case:** edits in the last 10% of the document gain only 1.07×, because inline rewriting is already cheap there.
- **Consistency checks:** same limits as Idea 1. D ends at about 141k tokens, under 200k. With 30% of gaps past the TTL, the gain is 1.19× (C) and 1.43× (D).
- **Hazards:** the same stale-text risk as Idea 1, plus fold storms when the same key is edited again and again. That case should go to the Idea 1 ledger.
- **Deciding unknown and experiment:** the same paired evaluation as Idea 1, plus measuring real gaps between turns against the TTL in production logs (`cache_read_input_tokens`).
- **Closest work:** Anthropic's `clear_at_least` (FACT 10) uses the same "only invalidate when it's worth it" logic, but for clearing content. What this adds: fold cost measured from the earliest edited position, folding forced by repeated edits, and free folding when the cache has expired.
- **Verdict:** WORKS for document sessions with scattered edits and turn gaps under the TTL. NICHE elsewhere.

**Which numbers still need a real model run:** every quality claim. Neither idea has measured answer agreement yet; for both it is the deciding unknown. The PI-LLM per-depth accuracy tables could not be fetched (arXiv blocked), so "depth 1 is safe enough" is a hypothesis, not a measurement.

Sources:
- [PI-LLM, arXiv 2506.08184](https://arxiv.org/abs/2506.08184)
- [DKI retrieval bias, arXiv 2603.12271](https://arxiv.org/abs/2603.12271)
- [Manus context engineering](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)
- [Claude Code issue #21650](https://claudeissues.com/issue/21650-bug-system-reminders-for-modified-files-repeat-excessively-consuming-context)
- [Claude Code issue #20850](https://claudeissues.com/issue/20850-bug-title-file-modification-system-reminders-consume-excessive-context)
- [IKE / DeCK, arXiv 2405.11613](https://arxiv.org/pdf/2405.11613)
- [Context-memory conflicts with real documents, arXiv 2404.16032](https://arxiv.org/pdf/2404.16032)
