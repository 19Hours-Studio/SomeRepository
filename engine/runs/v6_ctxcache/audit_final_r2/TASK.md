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
`/home/user/SomeRepository/engine/runs/v6_ctxcache/audit_final_r2/`: read no other files in the repository, do not modify other files, do not commit.

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
NAME: Canonical ordering plus position-independent chunks
MECHANISM: Runs on your own stack or provider-side and covers reordered documents and RAG sets. First, sort retrieved documents and tool schemas by stable ID and popularity, so most reorders become exact prefix hits. Berkeley's relational-query reordering already shows this works, with up to 3.4× faster jobs and 32% lower cost under OpenAI and Anthropic pricing. For the rest, use a store of KV per chunk, computed once with the shared system prompt in front of it. APE showed this shared prefix removes the per-chunk attention-sink error with no training, keeping 93–98% of sequential-encoding quality. At assembly time, re-rotate positions exactly, recompute the first few tokens of each chunk (EPIC: up to 8× TTFT and 7× throughput, with negligible accuracy loss) and selectively recompute 10–15% of tokens (CacheBlend: 1–3% quality loss, 2.2–3.3× TTFT). Token hit rate is then about 85–90% for permuted sets and 100% for the canonical ones. Storage is one KV copy per chunk instead of one per prefix: 30.5 GiB per 100k tokens in BF16, about 6× less with roughly 3-bit compression. To test, compare answers under canonical, random and adversarial document orders against full recompute, which measures both the order effect and the blending error. Chunks must be isolated per tenant: HijackKV shows shared position-independent KV can be poisoned across users.
VALUE: Adding canonical ordering in front of CacheBlend/EPIC turns most reorders into lossless exact hits, so blending's 1–3% loss applies only to the remainder. Expect about 5–10× less prefill than prefix caching on RAG traffic where the document set varies.

IDEA 2
NAME: Popularity-first exact-prefix document ordering
MECHANISM: Remove the blending stage, which is the part later papers dispute. Order retrieved documents by descending global retrieval frequency, using an online counter with ties broken by ID. Put the system prompt first and the question last. Every reuse is then an exact prefix hit, so the reused KV equals what full recomputation would give for that order. The only quality effect is the reorder itself. Stable-RAG reports that answers change with document order even under 1k tokens. To test it, run the same retrieved sets in relevance order and in popularity order and compare F1/EM and the spread across permutations (needs a real model). I replayed the same setup as FACT 5 (100k chunks, top-5, Zipf). Exact document-token reuse is 0.400, 0.546 and 0.768 at Zipf 1.05, 1.2 and 1.5. Hash order gives 0.152, 0.229 and 0.503; relevance (random) order gives 0.166, 0.249 and 0.425. A cache-aware trie-greedy order like CacheWeaver's gives 0.403, 0.548 and 0.769, the same as the counter. Because the counter needs no view of the cache, the method runs client-side through a third-party API. Under Anthropic's multipliers, the per-request bill is 1.17x, 1.35x and 1.78x cheaper than the usual practice of sending documents uncached. Caching documents only pays once reuse is above 0.217; hash order plus cache_control actually loses (0.95x). Self-hosted, the gain is 1.17x, 1.26x and 1.43x. Limits: per-document breakpoints (at most 4 per request), a 1,024-token minimum prefix, traffic arriving within the 5-minute TTL, and an LRU cap of 20k tree nodes that costs at most 1.4 points of reuse. Covers document reordering only.
VALUE: 1.2–1.8x per request against the best current API practice, without approximating any KV, and it works for API users. This is the smallest honest version; the old 5–10x needed blending. The advance over CacheWeaver is that a stateless counter matches its trie-greedy order, so no cache state is needed. Long-tail documents (23–60% of document tokens) still miss, so about 100% is not reachable.

IDEA 3
NAME: Popularity order with second-sighting cache writes
MECHANISM: Documents are still sent in order of descending global retrieval count from an online counter (ties broken by ID), with the system prompt first and the question last. Every hit is therefore an exact prefix match and the cached state is exact. Two changes fix the weak link. (1) Second-sighting admission. The client keeps a list of document-prefix hashes it has seen recently, with no cached state behind them. A cache breakpoint is placed only at prefix depths already seen within the TTL window. Documents past that depth go after the last breakpoint and are billed at 1.0x instead of a 1.25x write. This is the CDN "cache on second hit" / TinyLFU admission idea applied to breakpoint placement. (2) TTL by traffic regime. The 1-hour TTL (2x write cost) is used when the organisation sends fewer than about 1k requests per 5 minutes, and the 5-minute TTL otherwise. Replay setup: 100k chunks, top-5, Zipf, 4 breakpoints at document depths 2–5, Anthropic multipliers, compared with sending documents uncached. Bill ratios across 10 to 1,000 requests per 5 minutes: - Zipf 1.05: 1.06–1.24x - Zipf 1.2: 1.19–1.44x - Zipf 1.5: 1.46–1.83x The old always-write rule gave 0.88–1.61x and lost money at low traffic. The method now never loses in any tested regime, and 1.5x holds at Zipf 1.5 from about 100 requests per 5 minutes (1.66x), where the old rule needed about 1k. It covers document reordering only. Quality effect: only the reordering itself. Test it by comparing F1/EM and the spread across permutations against relevance order on a real model.
VALUE: 1.06–1.83x cheaper per request than the best current API practice (documents uncached), with no approximated KV, and it runs client-side only. It no longer loses money at low traffic or flat popularity. Rarely retrieved documents still miss (23–60% of document tokens), so a hit rate near 100% is not reachable.

IDEA 4
NAME: Content-addressed position-independent KV with gated repair
MECHANISM: This runs on your own serving stack or on the provider side. Split token streams at content-defined boundaries: a rolling hash over token IDs plus message and tool delimiters. A re-sent span (a reordered document, a re-read file, a moved tool output, the text after an insertion) is then found at any offset with an O(1) hash lookup. Store keys before the positional rotation is applied, so reusing them at a new position is free inside the attention kernel. Repair in layers: recompute the first ~32 tokens of each chunk to remove the false attention-sink effect (EPIC), the top-r tokens by key deviation (CacheBlend), and a 16-token window after each splice point. Add a quality gate: on ε≈1% of traffic, run a full recompute in shadow, compare the next-token distributions (KL) on the first 32 output tokens, and adjust r per chunk type. Fall back to exact recompute when the gate fails. My model for 8×512-token chunks with a 1k system prompt in a new order on an 8B model, against full recompute: EPIC-only repair needs 8.4% of full compute, r=15% needs 15.6%, the full stack needs 23.2%, and r=30% for multi-hop needs 27.9%. Prefix caching here needs ~83% of full compute, because only the system prompt hits. Memory: 128 KiB of KV per token at 8B (320 KiB at 70B, so 328 GB per 1M tokens). Loading 4,096 reused tokens takes 10.7 ms over PCIe5 or 77 ms from NVMe, against ~152 ms for full prefill. The shadow check adds ε of full prefill.
VALUE: On reordered or re-positioned content, compute drops 3–10x against prefix caching, and token reuse rises from 19% to 74–92%. Prior art covers most of the parts: CacheBlend, EPIC, Cache-Craft, KVShare, SemShareKV, and LMCache's CacheBlend for agents. What this adds is offset-independent lookup plus a quality SLO with exact fallback. Quality is model-dependent. KVShareArena finds that repairs recover only half to two-thirds of the gap on multi-source questions, and that unrepaired caches can be worse than no cache. So "≈100% hit at full quality" is not reachable for multi-hop work. The deciding test is KL/F1 against full recompute on 2WikiMQA, MuSiQue and agent replays (needs a real model).

