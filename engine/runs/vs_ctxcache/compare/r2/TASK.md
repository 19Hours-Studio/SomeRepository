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

Below are 7 ideas, already repaired once against reality by a researcher. Your job is to be the toughest competent
outside reviewer: an engineer who will lose money if any of these claims is wrong. You do NOT fix or improve the
ideas; you find their defects, prove each one with a number, and rank them.

You have tools: WebSearch/WebFetch and Bash with python3 (check every claim in real code). Work only in
`/home/user/SomeRepository/engine/runs/vs_ctxcache/compare/r2/`: read no other files in the repository, do not modify other files, do not commit.

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

THE 7 IDEAS:
IDEA 1
NAME: Hole-punch deletes via block-table edits
MECHANISM: This needs your own serving stack or provider-side changes, and would be exposed as a new API operation such as `delete_span(id)`. The most common mid-prompt change in agents is deletion: clearing old tool results or compaction. Provider "context editing" features currently throw away the cached prefix at that point. Instead, drop the deleted span's paged-KV blocks from the request's block table and keep every later block as it is. New tokens either continue after a gap in position IDs (PyramidKV-style) or have their keys rotated back into a dense range with a delta RoPE rotation (HERMES and KV Packet rotation). The cost is zero recompute and zero extra memory, and the freed blocks are returned to the pool. The hit rate on the remaining tokens is 100%, but the result is not exactly what full recomputation gives. Tokens after the hole still carry information they absorbed from the deleted span. That is often harmless or even useful for compaction, but harmful when the deleted text was wrong, so pair it with an erratum from Idea 1. Prior art: llama.cpp context shift, and KV-eviction methods (StreamingLLM, H2O, SnapKV), which use the same mechanism to choose tokens heuristically. What is new is driving it from an explicit edit request and billing it as a cache hit.
VALUE: Deletions and compaction become cache hits at 0.1x instead of a rewrite of the whole suffix at 1.25x, a 12.5x cheaper suffix. Quality test: KL divergence and top-1 agreement of next-token distributions against full recomputation on real agent traces, measured with the gap and the rotation variants. This needs a real model.

IDEA 2
NAME: Cost-optimal patch folding
MECHANISM: Anchor: edits become structured appended patches, and a full rewrite runs only when the patches cost more than one fresh write. Repair: the fold rule is now ski-rental, which is guaranteed to cost at most 2× what the best possible fold timing would have cost. The client folds once the patches' cumulative extra reads reach the cost of rewriting from the earliest patched position, not from the start of the document. Two triggers are new: a second edit to the same key forces a fold (depth cap 1, because the PI-LLM/DKI evidence shows accuracy on the latest value falls as updates accumulate), and folding is free on any request that would miss the cache anyway (gap longer than the TTL), since that request rewrites everything regardless. Documents are given stable section IDs when they are loaded so patches can address sections. In the model this gives 1.52× (25k document, 10 questions, 3 edits) and 2.66× (120k copilot document, 30 questions, 15 edits) against inline rewriting. The token-weighted hit rate is 96.4%, which is every reusable token; inline gets about 71%.
VALUE: Document sessions with scattered edits on hosted APIs get 1.5–2.7× lower cost per question than inline rewriting, with no more than one override per section. The gain shrinks to about 1.2–1.4× when 30% of gaps between turns exceed the cache TTL.

IDEA 3
NAME: Append-only errata with ski-rental compaction
MECHANISM: This runs on the client only and works with any API. Never change content that has already been sent. Express a middle edit, a changed tool output or an insertion as a short tagged erratum at the end of the prompt, for example "[supersedes tool_result #17]: …". Sort documents into a fixed order, such as by content hash, and serialize JSON with sorted keys, so that reordering becomes an exact prefix match. Do a real in-place rewrite (compaction) only when the running cost of the errata reaches the one-time cost of rewriting the suffix. That is the ski-rental rule, and it costs at most 2x the best possible schedule. With Anthropic's prices (cache write 1.25x the base input price, cache read 0.1x), an erratum of e tokens placed after an edit at position p in an N-token context breaks even with a rewrite only after T* = (1.25(N−p) − 1.25e)/(0.1e) turns. For N=100k, p=50k and e=500 that is 1,238 turns; for an edit near the end (p=90k, e=2k) it is 50 turns. So the erratum is almost always cheaper, and compaction is driven by the context-window limit, not by cost. In a 50-turn synthetic agent replay with 2k-token tool outputs and an earlier tool output changing every 5 turns, the token hit rate rose from 92.9% to 99.75% and billed input fell from 604k to 365k units (−40%). Tokens are exactly what the model would compute, so the KV state matches full recomputation exactly. The only quality risk is semantic: stale text stays in the prompt next to its correction.
VALUE: This gives a hit rate near 100% for edits, tool outputs and insertions, and for reordering of document sets that repeat, at no infrastructure cost. In the replay it cut input cost by about 40% against append-and-edit prefix caching. It extends Manus's "append-only context" guidance with a cost-optimal rule for when to compact. Quality has to be tested as an A/B on agent traces, for example SWE-bench success rate and needle-in-a-haystack tests with superseded facts. That test needs a real model and was not run here.

IDEA 4
NAME: Context-length-gated turn collapsing
MECHANISM: The anchor is that the agent stops to observe only when the expected value of seeing the result is worth one more full-context read, priced at C×0.1×p (C is the current context length, p the base input price). The threshold therefore tightens as C grows: early turns observe freely, and turns after about 20–40k tokens are folded into multi-step scripts (k=3 steps per turn). Each script filters its tool outputs down to the lines needed for the next decision, so less text enters the context and every later read shrinks. The design changes are these. Only read-only or idempotent tools are folded. A script stops early as soon as an expectation check fails. Folded batches longer than 5 minutes use the 1-hour cache TTL. On a 40-turn session the gate gives 1.48× and the gate plus 50% filtering gives 1.81×. On a 150-turn session, where reads are 75% of cost, the gate gives 2.02× and gate plus filtering gives 2.42×.
VALUE: About 2.0–2.4× cheaper per long agent task than the plain cached agent loop. That compares with 1.20× for CodeAct's measured 30% turn cut and 0.83× for observation masking once cache rewrites are paid.

IDEA 5
NAME: Storage-priced retention, not token-priced hits
MECHANISM: This runs on your own stack or provider-side. At high hit rates, the real cost of a hit is storing the KV, not computing it. Recomputing a token of a 70B model costs about $0.175 per 1M tokens (H100 at $2/h, 45% compute utilization). Holding the same KV for one hour costs about $8.2 per 1M tokens in GPU memory (HBM), $1.6 in CPU RAM (DRAM) and $0.07 on NVMe SSD. So a 1h DRAM-resident cache only pays off if the context is reused about every 6 minutes. NVMe pays off down to about one reuse per 2.5 h. FP8 halves these costs, and MLA models cut them about 4.6x. Retention per prefix should therefore use a ski-rental rule too: keep the KV in a tier while (expected reuses) × (recompute cost) is greater than storage cost × time. The default for long-tail sessions should be NVMe with a long TTL plus MLA or FP8 KV, not GPU memory.
VALUE: This is what makes a hit rate near 100% affordable, at a storage cost about 20x lower than DRAM. It also shows that pushing hit rate and price down together is limited by storage. Prior art is tiered caching (Mooncake, LMCache, HiCache), which per earlier runs gains only about 1.2x over GPU-only prefix caching. The addition is cost-based eviction per prefix.

IDEA 6
NAME: Segment cache with boundary recompute
MECHANISM: This runs on your own stack, for example LMCache's CacheBlend in vLLM, or provider-side. Cache the KV of each document or tool output on its own, keyed by content hash. Compute it after the real shared system prompt (APE's "shared prefix") so it differs less from in-context KV. When reusing a segment at a new position, rotate its RoPE positions and recompute only the tokens whose KV deviates most. CacheBlend recomputes about 15% of tokens and reports a 2.2–3.3x faster time-to-first-token with same-quality answers on RAG question answering. EPIC recomputes only the first few tokens of each chunk (about 32 of 512 tokens, roughly 6%, so about 94% effective hit) and reports up to 8x faster time-to-first-token with "negligible" loss. Add a deviation gate: if the layer-1 deviation (the CacheBlend signal) is above a threshold, fall back to exact recompute. Covered cases: reordering, insertions and changed segments. Only the changed segment and its boundary tokens are recomputed. Storage grows with one KV copy per unique segment: 320 KB per token for Llama-3-70B in BF16, 69 KB per token for DeepSeek-V3's MLA. Latency adds a PCIe load of about 6.6 s per 1M tokens of 70B BF16 KV.
VALUE: About 85–94% of non-prefix tokens are served from cache, and prefill compute falls about 3–7x against exact prefix caching on RAG and reordered workloads. Quality is not exact. The SIGMOD'26 Fusion-RAG paper and AgentKVShift report a remaining gap on multi-hop and agent-memory tasks. Quality test: run it against full recomputation on 2WikiMQA and MuSiQue (multi-hop QA), on LongBench, and on real agent traces.

IDEA 7
NAME: Floating depth-1 override ledger
MECHANISM: Anchor: an edit never rewrites earlier context; it is sent as an appended patch, so the cached prefix stays byte-identical. Repair: patches no longer pile up in history. The client keeps one deduplicated ledger with a single entry per stable section or state key ("§4 now reads…", "plan.status = …"). It places the ledger after the last cache breakpoint, right after the current question, and drops it from the history it sends next turn. Each turn therefore re-pays only the ledger at 1.0× plus the reply tokens. Each key only ever has the original plus one override, so the depth-driven interference measured by PI-LLM and DKI stays at depth 1. The ledger is folded into the document when its spend exceeds one rewrite from the earliest edited position, when it passes 10% of the context, or for free on any turn where the cache has already expired. In the model, a 150k-token agent context with 8k of mutable state at the front (40 calls, 20 state edits) costs $0.0735 per request against $0.336 for inline rewriting. That is 4.6× cheaper and within 6% of the no-edit floor. A 25k-token document with 10 questions and 3 edits comes out 1.46× cheaper with the 10% cap.
VALUE: When the same state or section is edited repeatedly on a hosted API, cost per request falls 2.6–4.6× against inline rewriting, at the same cost as the patch chain coding agents already use (within 4–8%) but with override depth held at 1 instead of the chain's 3–7.

