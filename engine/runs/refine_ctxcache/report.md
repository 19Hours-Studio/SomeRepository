# refine_ctxcache: stepwise improvement of a plain answer, judged afterwards

| version | words | cost |
|---|---|---|
| v0 | 1317 | plain answer |
| v1 | 2156 | $0.85 |
| v2 | 2539 | $1.16 |
| v3 | 3250 | $1.21 |
| v4 | 3754 | $0.84 |

| comparison | newer version won (both orders) | margins | score (+ newer, - older) |
|---|---|---|---|
| v1 vs v0 | 2 of 2 | clearly, clearly | +4 |
| v2 vs v0 | 2 of 2 | clearly, clearly | +4 |
| v3 vs v0 | 2 of 2 | clearly, clearly | +4 |
| v4 vs v0 | 2 of 2 | clearly, clearly | +4 |
| v2 vs v1 | 2 of 2 | clearly, clearly | +4 |
| v3 vs v2 | 2 of 2 | clearly, clearly | +4 |
| v4 vs v3 | 2 of 2 | clearly, clearly | +4 |

## Why (the judge, newer vs older)
- v1 vs v0: newer wins, clearly. B keeps all of A's mechanisms but corrects A's compaction break-even formula and overturns A's novelty claim for span deletion by citing Leyline. It adds actionable client-side levers (change-rate ordering, volatile tail, TTL choice, popularity-ordered RAG) with replay numbers. Its cost breakdown and bandwidth check show the asker that at ~100% hits the bill is dominated by reads and storage, whic
- v1 vs v0 (swapped): newer wins, clearly. A includes B's four ideas but corrects B's break-even formula, its overstated novelty claim (Leyline), and its NVMe recommendation (via a bandwidth check). It adds valuable client-side techniques: λ/s ordering, the volatile tail, TTL choice, and popularity ordering for RAG, each with quantified hit rates. Its cost breakdown, showing that cached reads dominate at 100% hits, and its more explicit li
- v2 vs v0: newer wins, clearly. B covers the same four ideas but adds more of what the person could act on: the cost breakdown at 100% hits, a verified ordering rule, a real-trace splice replay, and RAG with varying document sets. Its gate calibration is concrete and its limits argument is rigorous. A is sound but less quantified, misses several cost levers (TTL, routing, layout ordering), and says less about which cases cannot 
- v2 vs v0 (swapped): newer wins, clearly. A covers every requested dimension and adds high-value levers: the cost breakdown, TTL choice, routing sharding, a counterexample-checked ordering rule and a real-trace replay. Its ski-rental math is correct where B's overcounts the rewrite cost, and its limits section is more rigorous, including the layer-0 bound on exact reuse. B is a competent but thinner subset of the same ideas.
- v3 vs v0: newer wins, clearly. Both share the same core ideas. B adds concrete, quantified causes of cache misses that API users can fix themselves: the breakpoint lookback, reasoning-stripping templates, block ordering by odds of change, TTL choice and key sharding, plus a diagnostic tool. It also gives a stronger analysis of the limits, including the 1/L cap on exact reuse and the cost floor at 100% hits, which bears directly
- v3 vs v0 (swapped): newer wins, clearly. A covers the same four mechanisms as B but adds many concrete, quantified client-side levers that an API user can apply immediately, such as the lookback trap, reasoning stripping in templates, breakpoint placement, TTL and key sharding, and a diagnostic tool. It also shows the cost floor at 100% hits, which B misses. Its fallback-rate curve and its rigorous section on what cannot reach 100% make 
- v4 vs v0: newer wins, clearly. B covers everything A proposes and adds tested, actionable levers for each deployment setting. These include fan-out warm-up, batch break-even, the clearing schedule, the lookback and template traps, and a diagnostic tool. It is also more rigorous about the limits: the 1/L bound for exact reuse, the bill floor at 100% hits, and caps on new document combinations. A is correct but far less useful to
- v4 vs v0 (swapped): newer wins, clearly. Both share the same four core ideas and the same prior art. A adds many concrete, quantified levers that API users can apply (TTL, warm-up before fan-out, batch break-even, lookback and template traps, clearing schedule, diagnostic tool), and it covers every change case and deployment location explicitly. Its limits section is far more rigorous, while B's constraints and limits are thin by compari
- v2 vs v1: newer wins, clearly. B keeps A's structure but corrects the ordering rule with a brute-force check, and honestly concedes the popularity-ordering prior art that A overclaimed. It adds evidence from real SWE-agent traces, a concrete shadow-calibrated gate, cache-key sharding and a rigorous 1/L limit on exact reuse. Its scripts are present and runnable, while A's referenced scripts were reportedly missing.
- v2 vs v1 (swapped): newer wins, clearly. A replaces B's subtly wrong Smith's-rule ordering with the correct odds-per-token rule and backs it with a brute-force check. It adds a real-trace replay showing that client-side elision every step can raise cost while a server splice lowers it. A is more honest about prior art and keeps total and document-only hit rates apart. B points to scripts that apparently don't exist and claims popularity 
- v3 vs v2: newer wins, clearly. B contains everything useful in A and adds practical hit-rate levers that are quantified (breakpoint lookback, reasoning-stripping templates, tail placement relative to the last breakpoint) plus a diagnostic tool for finding cache breaks. It replaces Idea 3's single savings number with a fallback-rate curve, which makes the multi-hop limitation concrete. It is also more candid about the weak evide
- v3 vs v2 (swapped): newer wins, clearly. A keeps everything B offers and adds several high-value, actionable items: Anthropic's breakpoint-lookback trap, the cost of templates that strip reasoning and how to fix it, breakpoint placement before the volatile tail, and a tool that diagnoses where the cache breaks. Its cost-versus-fallback curve for the approximate segment cache is more honest than B's single best-case saving figure. Togethe
- v4 vs v3: newer wins, clearly. B contains everything in A and adds three concrete, quantified cost levers: warm-up before parallel fan-out, batch stacked with caching and its break-even, and a square-root rule for when to clear context. These directly address the read and write share of the bill that A says hit rate cannot reduce. B also lists more of the real limits on reaching 100% (minimum prompt length, 128-token granularit
- v4 vs v3 (swapped): newer wins, clearly. The two answers are nearly identical in structure and content, but A adds three quantified, directly usable cost levers: warm-up before parallel fan-out, batch stacked with caching with a break-even point, and a square-root clearing schedule for `clear_at_least`. The clearing schedule attacks the read-dominated bill that hit rate alone cannot fix. A also lists more cases that cannot reach about 10
