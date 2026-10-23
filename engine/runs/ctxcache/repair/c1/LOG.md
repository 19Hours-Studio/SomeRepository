# LOG — repair c1 (one line per round)

| # | idea | change | decisive number | result |
|---|------|--------|-----------------|--------|
| 1 | I1 | prior-art check of "deviation gate" | CacheBlend, KVBoost (2608.21362) and Cache-Craft (SIGMOD'25) already select tokens by KV deviation or context impact | gate is known, so the anchor is moved to the closed-loop audit |
| 2 | I1 | cost per request served (70B FP8, 8×H100, 6k doc tokens, 200 out) | r*=0.10 with a 2% audit: 271 GPU-ms vs 720 for ContextPilot reorder (h=0.34), 1003 for exact prefix, and 295 for CacheBlend 15% | 2.65× vs the best exact-match practice, only 1.09× vs CacheBlend 15% |
| 3 | I1 | audit metric changed from first-token KL to answer flip under teacher forcing on the served full-recompute answer, plus a per-class answer-match check | zero-failure certification at ε=2%/95% needs 148 audits, i.e. 7.4k requests per window at a=2% | catches multi-hop answer flips, which first-token KL misses |
| 4 | I1 | selector made pluggable and an AgentKVShift-style residual correction used | CacheBlend selection at 10% loses 47.5% F1 on AMem while AgentKVShift loses 5.9% (2607.21604) | r*≤0.10 only plausible with a correcting selector |
| 5 | I1 | bandwidth and storage consistency | the node needs 24–39 GB/s of KV loads, so one NVMe (7–14 GB/s) fails and 4×NVMe or a DRAM tier is needed; NVMe break-even is 0.25 reuses/h per chunk, DRAM 7.6/h | admission rule needed; design changed to DRAM hot set + NVMe RAID |
| 6 | I1 | fallback: if the audit says r*>0.3, revert to exact-prefix/ContextPilot | worst-case overhead is about a×(shadow fused pass), roughly 0.5% | never meaningfully worse than the exact baseline |
| 7 | I2 | session cost model (Anthropic 1.25/0.1/5×, 40 turns, 8k system, 1.2k obs) | reads are 47% of cost; uniform 2× turn cut gives 1.41×; CodeAct's 30% gives 1.20× | confirms the kill test (~1.37×) |
| 8 | I2 | gate threshold tied to the current context length (fold steps only when C>C*) | k=3 folding above 20k: 1.48× with 21 turns | better per lost observation than uniform folding |
| 9 | I2 | added in-script observation filtering (cuts Δ, so every later read shrinks) | gate + 50% filter: 1.81×; + 30% filter: 1.92× | close to 2× on a 40-turn session |
| 10 | I2 | moved to the regime where the anchor is strongest: long sessions (150 turns, 20k system, read share 75%) | gate alone 2.02×; with 50% filter 2.42× | WORKS in long sessions; NICHE for short ones |
| 11 | I2 | baseline: observation masking under caching (rewrite after each clear) | 0.83× in my model (rewrites at 1.25×), vs 52% cheaper reported uncached (FACT9) | masking does not transfer to cached pricing unless clears are rare |
| 12 | I2 | test power | 1,307 paired tasks to detect a 3-point drop; SWE-bench Verified's 500 tasks only detect about 5 points | the deciding experiment is sized |
