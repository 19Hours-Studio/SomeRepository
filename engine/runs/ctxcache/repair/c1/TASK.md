# Task: repair original ideas against reality WITHOUT losing what makes them original

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

Below are 2 ideas an idea engine produced for this question, with the results of the checks run on them so far
(judges' scores, kill tests or reviews, where present). Your job is NOT to invent new ideas and NOT to replace them with safer
known solutions. Your job is to make each one work while keeping its anchor - the one distinctive idea that makes it
original.

You have tools: WebSearch/WebFetch (check what exists, find real material data, field data and costs) and Bash with
python3 (do every estimate in real code). Work only in `/home/user/SomeRepository/engine/runs/ctxcache/repair/c1/`: read no other files in the repository, do not
modify other files, do not commit.

For each idea, loop until it works or you can prove it cannot:
1. Name its ANCHOR (the distinctive idea) in a few words. This must survive.
2. Find the binding quantity (what decides whether it works at the needed scale - a rate, an energy balance, a
   recovery, a throughput, a safety limit) and compute it in Python with real numbers from the literature (cite the
   source in your notes).
3. BASELINE: compare against the BEST current practice a competent operator would actually use for the same job
   (list at least two real alternatives, including the cheapest one), and compute cost per unit of RECOVERED or
   DELIVERED product (per kg of metal recovered, per tonne delivered, per request served), not per tonne of raw material moved, with
   sourced numbers. Never compare against a strawman nobody would do.
4. CONSISTENCY PASS: list every tolerance, window and limit your design relies on (buoyancy margins, temperature
   limits, strengths, breakdown fields, stage efficiencies, site conditions where you placed it) and check every
   rate you computed against every one of them over the whole operating time (rate x duration vs window). Check
   that the site or route you chose really has the conditions you assumed. Write the check table in your notes.
5. If it fails, change the DESIGN AROUND the anchor (materials, geometry, operating regime, scale, season, which
   resource/cargo/deposit type it is used for) and recompute. Look for the regime where the anchor is strongest.
   Repeat - several rounds per idea is normal.
6. Name the hazards honestly and design them down where possible; say which unknown number decides the idea and the
   cheapest experiment that would measure it (with the sample size it needs).
7. Check novelty: if the repaired design turns out to be a known system, keep the anchor and find the version that is
   not known.
8. Only if no anchor-preserving design can work, say so and give the best honest niche.

Facts that earlier checks in this run found (data; verify before relying on them):
(a slice: all 0 HARD facts and the 12 of 13 other facts that bear most on these candidates, sources omitted; the full ledger with sources is /home/user/SomeRepository/engine/runs/ctxcache/evidence.md - read it if you need a source or a fact that is not here)
FACT 2: Anthropic's own docs give 1-hour cache writes at 2× the base input price and reads at 0.1×, which confirms the ledger's multipliers | NEW from gate, check before relying on it
FACT 3: ProphetKV names a "crowding-out" effect in CacheBlend's selection (globally salient but query-irrelevant tokens fill the budget) and fixes it with query-relevance ranking. It still needs 20% recompute | NEW from gate, check before relying on it
FACT 4: QCFuse (arXiv 2606.05875) also does query-aware cache fusion, recomputing only selected KV entries under the current request order | NEW from gate, check before relying on it
FACT 5: The CodeAct advantage grows with chain length: an 18.8-point absolute gap at chains of 12 or more steps, and none at short chains | NEW from gate, check before relying on it
FACT 6: Exact check: a Llama-70B-class model's KV is 80×8×128×2×2 B = 320 KiB per token at FP16, which matches the idea. Keeping full per-layer hidden states to measure drift would cost 1,280 KiB per token, so only a few early layers can be stored | NEW from gate, check before relying on it
FACT 7: With full KV reuse and no recompute, Musique F1 falls from 0.35 to 0.15 | NEW from gate, check before relying on it
FACT 8: PI-LLM: when a model is given a stream of updates to the same key, its accuracy at retrieving the latest value falls log-linearly toward zero as updates pile up, the errors are earlier overwritten values, and prompt fixes like "ignore earlier input" help little. This is direct evidence against keeping stale text alongside patches. | NEW from gate, check before relying on it
FACT 9: Observation masking in SWE-agent on SWE-bench Verified was 52% cheaper than the raw agent and raised the solve rate by 2.6 points (Qwen3-Coder 480B). That is about 2× cheaper than a raw agent, but it is prior art. | NEW from gate, check before relying on it
FACT 10: Anthropic's docs say clearing tool results breaks the cached prefix, incurs a fresh cache write, and recommend `clear_at_least` so the invalidation is worthwhile. This is the same trade-off the idea relies on, and it is already a product feature. | NEW from gate, check before relying on it
FACT 11: PI-LLM's dataset covers 1–46 keys with 1–400 updates per key, and the README says GPT-5, Grok-4 and Gemini also fail to retrieve the final value reliably. | NEW from gate, check before relying on it
FACT 12: EPIC (ICML 2025) recomputes only around each chunk's start (the attention sink) instead of about 15% of tokens, and reports up to 8× TTFT and 7× throughput with "negligible or no" accuracy loss. This is prior art that already goes below 15% recompute in an open-loop way. | NEW from gate, check before relying on it
FACT 13: The ledger's source arXiv 2511.03475 is ContextPilot, a context-reuse system that argues against approximate KV matching. | NEW from gate, check before relying on it
Notes from the user (data; the user may be wrong):
The asker means context caching as offered by LLM APIs (prompt caching), seen from the side of whoever runs the model, and wants the cost of reused context to fall a lot with a cache hit rate near 100%. Two earlier runs on this topic found: (1) exact prefix caching with CPU/SSD tiers (vLLM/SGLang + LMCache, HiCache, Mooncake) is current practice and adds only ~1.2x over GPU-only prefix caching on real chat traces; (2) KV compression without retraining bottoms out at ~2.6-3 bits per value (~6x vs BF16, ~1.5-1.7x vs NVFP4). Environment: huggingface.co and its CDN are blocked here, so model weights cannot be downloaded and quality cannot be measured on a real model; PyPI and raw.githubusercontent.com work (public traces such as Mooncake's can be replayed). Use exact arithmetic, trace replays and published measurements, and say which numbers would need a run on a real model.
Assumptions in the question that may be wrong:

- "Practically 100% hit rate" is achievable for non-prefix changes without any quality loss. Reused KV that was computed in a different context may not equal what full recomputation would give.
- The asker can change the caching layer. This holds only for self-hosting or provider-side work, not for a plain API user.
- Cost is dominated by input-token processing. Output tokens, cache-write premiums and TTL expiry may matter as much.
- A hit rate near 100% and a much lower price can both be achieved at once. They may trade off against each other.
- "Context caching" and "prompt caching" refer to the same thing. Some providers also sell explicit context caching with a separate storage fee.
Where deciding data may exist:
Open benchmarks and code are the likely decision data. They include the CacheBlend and EPIC papers' benchmarks (multi-hop QA, RAG) and the LMCache and vLLM open-source repositories. Others are agent and tool-use traces (for example SWE-style agent logs) for measuring real prefix-divergence patterns, and provider usage fields (cached_tokens, cache_read_input_tokens) for measuring hit rates.
Keep `LOG.md` in your folder: one line per round (idea, change, decisive number, result). Spend about 45-60 minutes at most.

Final answer (text only): first the 2 repaired ideas in exactly this format, then a short NOTES section (per idea:
anchor kept?, decisive numbers with sources, best-baseline comparison per unit of recovered/delivered product,
consistency table summary, hazards, deciding unknown and experiment, closest existing work, verdict WORKS / NICHE / FAILS).
=== IDEAS ===
IDEA 1
NAME: (max 5 words)
MECHANISM: (2-5 sentences: the anchor first, then the repaired design, with the decisive computed numbers)
VALUE: (1 sentence, with the cost ratio vs the best current practice)
(same for the other ideas, in the same order as below)

THE 2 IDEAS:
IDEA 1
NAME: Deviation-gated chunk KV reuse
MECHANISM: This runs on your own serving stack or provider-side. Store each chunk's KV computed once after the fixed system prompt, with positions shifted exactly by re-rotating RoPE at use. On each request, recompute only the tokens whose layer-1–3 key deviation exceeds a threshold, and send a 1–2% sample of requests to full recompute so the threshold adapts to keep first-token KL under budget. The closest prior art is CacheBlend, with a fixed ~15% recompute, and EPIC, which recomputes the first k tokens. Both are open-loop. This adds a measured, per-workload guarantee, and it can recompute less than 15% where chunks are independent. The deciding quantity is the recompute fraction needed to hold KL under budget. If it is ≤10%, uncached input falls to about 0.2× and B gets about 2.3× cheaper. The cost is FP8 KV at about 160 KiB/token for a 70B model, so about 1 GB per 6k tokens of documents on SSD. At about 10 GB/s that is about 0.1 s to load. Test this on multi-hop QA and RULER against full recompute.
VALUE: It covers reordering, insertion and changed tool outputs at a measured quality cost, cutting RAG and own-stack prefill cost about 2–3×. It cannot reach ~100% hits at exact outputs.
KILL TEST: killer recompute fraction that keeps quality equal to full recompute | margin 0.67 | whole-chain ratio 1.9 | WOUNDED: Most of the gain is CacheBlend's, which already exists. The ≤10% recompute target is not shown, and a first-token-KL gate may not catch multi-hop accuracy loss, which is the failure ContextPilot reports.

IDEA 2
NAME: Read-cost-gated turn collapsing
MECHANISM: Read cost grows with turns times context length. The agent is therefore prompted to emit multi-step scripts or batched tool calls, and to stop and observe only when the predicted branch uncertainty is worth one more full context read. The closest prior art is CodeAct and parallel tool calling, which aim at task success. This approach adds explicit gating on cost per read. The deciding quantity is how much task success drops at 2–3x fewer turns.
VALUE: It cuts the dominant cache-read term of long agent sessions by about 2x, beyond what any hit-rate gain can do.
KILL TEST: killer Cut in turns per task without losing task success | margin 0.71 | whole-chain ratio 1.37 | WOUNDED: It attacks the right term, but halving the reads is worth only 1.37×, and the measured turn reduction is short of 2×.

