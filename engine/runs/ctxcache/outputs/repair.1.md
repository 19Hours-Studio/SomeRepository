I repaired both ideas and kept both anchors. Idea 1 is NICHE: its cost gain is real against exact-match caching, but it adds almost nothing over CacheBlend, and quality was not measured on a real model. Idea 2 WORKS only in long agent sessions (about 100 turns or more) and is NICHE for short ones. All quality numbers are published figures or assumptions, because model weights could not be downloaded here.

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