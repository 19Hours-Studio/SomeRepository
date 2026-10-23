# Task: adversarial review - find what would make these ideas fail or overstate their value

QUESTION: Hosted LLM APIs (Anthropic, OpenAI and others) offer prompt caching. The provider stores the computed intermediate state (the attention key/value, or KV, cache) for a request's token prefix. A later request is served from that state only if its prefix is token-for-token identical, and the cached portion is billed at a discount. An edit in the middle of a prompt, an insertion, a changed tool output, or a different document order breaks the match from the first differing token onward. Everything after that point is recomputed and billed at full price. The asker wants a way to make cached context much cheaper and to reach a cache-hit rate close to 100%. This must include requests that differ from earlier ones in the middle, by insertions, tool outputs or reordered documents, and it must work without retraining or fine-tuning the model. The question does not say whether the asker runs their own serving stack or uses a third-party API, or whether the solution may sit on the client side, the server side, or both. What is the best way to do this?
A good answer: A good answer proposes one or more concrete, new or non-obvious approaches. Each must state three things:
- which request-change cases it covers: middle edit, insertion, tool output, document reordering;
- its expected hit rate and cost change, with the reasoning or a quantitative estimate;
- its effect on output quality compared with full recomputation, and how that effect could be tested.
Each approach must also say where it can run (client only, own serving stack, or provider-side) and what it costs in memory, storage and latency. It must be checked against existing prior art and say what it adds. It must state honestly which cases cannot reach about 100% under the stated constraints.
Constraints: 
- No retraining or fine-tuning of the model.
- Target hit rate close to 100% across non-identical prefixes.
- Much lower cost than current prefix caching.
- Nothing else was stated.

Below are 4 ideas, already repaired once against reality by a researcher. Your job is to be the toughest competent
outside reviewer: an engineer who will lose money if any of these claims is wrong. You do NOT fix or improve the
ideas; you find their defects, prove each one with a number, and rank them.

You have tools: WebSearch/WebFetch and Bash with python3 (check every claim in real code). Work only in
`/home/user/SomeRepository/engine/runs/ctxcache/audit_final/`: read no other files in the repository, do not modify other files, do not commit.

For each idea, attack in this order:
1. Recompute every number the text states (arithmetic, units, mass, energy or memory balances). Flag any that do not reproduce.
2. Consistency: list every tolerance, margin and window the design relies on, and check every rate in the design
   against it over the whole operating time (rate x duration vs window). Check that the conditions assumed really
   hold where the idea is used (site, route, season, workload, hardware) - find measured data.
3. Baseline: is the comparison against the best current practice a competent operator would use, per unit of
   recovered or delivered product or service? Name the real competing alternatives it ignores and recompute the ratio.
4. Assumptions: which decisive numbers (efficiencies, friction, rates, loss fractions, costs) are assumed rather
   than sourced? How far can they move, and does the claim survive the plausible range?
5. Evidence and statistics: are the proposed tests able to show what is claimed (sample sizes, confidence bounds)?
6. Hazards and showstoppers not mentioned (safety, environment, regulation, logistics, scale-up).
Facts marked NEW were found by earlier checks in this run and are not yet verified: do not count them toward FIT,
and do not base a FATAL or MAJOR defect on a NEW fact alone unless you have verified it yourself (its source and,
for measurements, which object and which hole, face or item each number belongs to).
Do not pad: a defect needs a mechanism and a number. If a claim survives your check, say so in one line.

Final answer (text only), exactly this format:
=== REVIEW ===
IDEA 1: <name>
DEFECT | <FATAL/MAJOR/MINOR> | <one sentence: what is wrong> | <the number or source that shows it>
(as many DEFECT lines as needed, most severe first)
SURVIVES | <claims that held up under your check, one line>
RATIO | <whole-chain cost ratio against the best current practice after your corrections: current cost / cost with the idea, one number> | <one line basis>
KNOWN | <yes / partly / no: is this already done or seriously proposed?> | <the closest existing system, project or proposal, with source>
NEW FACT | <any hard fact you found that the material did not contain> | <source> (optional, any number)
(same for the other ideas, in the same order as below)

THE 4 IDEAS:
IDEA 1
NAME: Audit-calibrated chunk KV fusion
MECHANISM: The anchor is a closed loop: 1–2% of requests are served by full recompute and also run in shadow through the reused-KV path. The results set the recompute threshold per workload against a measured answer-flip budget (the share of answers that differ from full recompute), instead of a fixed 15% recompute. The repairs are these. (1) The audit compares the whole answer by scoring it token by token under the reused KV, which catches multi-hop failures that first-token KL misses. (2) The token-selection method is pluggable, and a correcting one such as AgentKVShift is needed to get recompute down to about 10%; CacheBlend-style selection loses 47.5% F1 at 10%. (3) It stacks on top of exact-match document reordering (ContextPilot-style), and if the audit says more than 30% recompute is needed it falls back to exact matching. (4) Stored KV sits in a DRAM hot set plus a 4×NVMe array, because the node needs 24–39 GB/s of KV loads at 160 KiB/token (FP8, 70B). At 10% recompute a request costs 271 GPU-ms, against 720 for ContextPilot reordering and 1,003 for plain prefix caching. Certifying a flip rate of 2% or less at 95% confidence takes 148 clean audits, which is about 7.4k requests per calibration window.
VALUE: About 2.6× cheaper per request than the best exact-match practice (ContextPilot reordering) and about 3.7× cheaper than plain prefix caching, with a measured quality bound. It is only about 1.09× cheaper than CacheBlend at 15%, so its value is the guarantee, not the price.

IDEA 2
NAME: Floating depth-1 override ledger
MECHANISM: Anchor: an edit never rewrites earlier context; it is sent as an appended patch, so the cached prefix stays byte-identical. Repair: patches no longer pile up in history. The client keeps one deduplicated ledger with a single entry per stable section or state key ("§4 now reads…", "plan.status = …"). It places the ledger after the last cache breakpoint, right after the current question, and drops it from the history it sends next turn. Each turn therefore re-pays only the ledger at 1.0× plus the reply tokens. Each key only ever has the original plus one override, so the depth-driven interference measured by PI-LLM and DKI stays at depth 1. The ledger is folded into the document when its spend exceeds one rewrite from the earliest edited position, when it passes 10% of the context, or for free on any turn where the cache has already expired. In the model, a 150k-token agent context with 8k of mutable state at the front (40 calls, 20 state edits) costs $0.0735 per request against $0.336 for inline rewriting. That is 4.6× cheaper and within 6% of the no-edit floor. A 25k-token document with 10 questions and 3 edits comes out 1.46× cheaper with the 10% cap.
VALUE: When the same state or section is edited repeatedly on a hosted API, cost per request falls 2.6–4.6× against inline rewriting, at the same cost as the patch chain coding agents already use (within 4–8%) but with override depth held at 1 instead of the chain's 3–7.

IDEA 3
NAME: Context-length-gated turn collapsing
MECHANISM: The anchor is that the agent stops to observe only when the expected value of seeing the result is worth one more full-context read, priced at C×0.1×p (C is the current context length, p the base input price). The threshold therefore tightens as C grows: early turns observe freely, and turns after about 20–40k tokens are folded into multi-step scripts (k=3 steps per turn). Each script filters its tool outputs down to the lines needed for the next decision, so less text enters the context and every later read shrinks. The design changes are these. Only read-only or idempotent tools are folded. A script stops early as soon as an expectation check fails. Folded batches longer than 5 minutes use the 1-hour cache TTL. On a 40-turn session the gate gives 1.48× and the gate plus 50% filtering gives 1.81×. On a 150-turn session, where reads are 75% of cost, the gate gives 2.02× and gate plus filtering gives 2.42×.
VALUE: About 2.0–2.4× cheaper per long agent task than the plain cached agent loop. That compares with 1.20× for CodeAct's measured 30% turn cut and 0.83× for observation masking once cache rewrites are paid.

IDEA 4
NAME: Cost-optimal patch folding
MECHANISM: Anchor: edits become structured appended patches, and a full rewrite runs only when the patches cost more than one fresh write. Repair: the fold rule is now ski-rental, which is guaranteed to cost at most 2× what the best possible fold timing would have cost. The client folds once the patches' cumulative extra reads reach the cost of rewriting from the earliest patched position, not from the start of the document. Two triggers are new: a second edit to the same key forces a fold (depth cap 1, because the PI-LLM/DKI evidence shows accuracy on the latest value falls as updates accumulate), and folding is free on any request that would miss the cache anyway (gap longer than the TTL), since that request rewrites everything regardless. Documents are given stable section IDs when they are loaded so patches can address sections. In the model this gives 1.52× (25k document, 10 questions, 3 edits) and 2.66× (120k copilot document, 30 questions, 15 edits) against inline rewriting. The token-weighted hit rate is 96.4%, which is every reusable token; inline gets about 71%.
VALUE: Document sessions with scattered edits on hosted APIs get 1.5–2.7× lower cost per question than inline rewriting, with no more than one override per section. The gain shrinks to about 1.2–1.4× when 30% of gaps between turns exceed the cache TTL.

