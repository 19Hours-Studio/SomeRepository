# LOG — repair c2 (one line per round: idea | change | decisive number | result)

- I1 R0 | as given: KVzip 30% resident + per-STEP Quest recall of 10% from CPU | PCIe/HBM time ratio 25.8 at B=64, 32K (idea1_budget.py) | DEAD (matches kill test)
- I1 R1 | recall per TURN (once per user message, amortized over mean 343 output tok, Mooncake conv trace) | PCIe/HBM 0.08; 64 vs 26 users at 32K; 2.49x decode tok/s vs FP8-full | decode OK
- I1 R2 | add per-step Quest "valve" | valve must be <=0.36% of context/step or it stalls; stalls if output <26 tok/turn | bounded valve kept
- I1 R3 | include prefill + KVzip scoring in GPU-s/request | break-even scoring overhead 0.29x prefill at trace-average 7.6K new tok/turn; at 500 new tok/turn ratio 0.49-0.61 | KVzip full scoring kills it on doc-heavy turns; WORKS in shared-context follow-up chat or with cheap (window/head-level) score
- I1 R4 | novelty | ArkVale (NeurIPS'24) = recallable page eviction per step; RocketKV-MT keeps all tokens, per-step select | turn-granular recall + query-agnostic residency not found | anchor kept, version distinct
- I2 R0 | as given: value-density eviction vs LRU | system gain 2-5% (kill test) | DEAD at large tiers (confirmed: 0% gain >=25M tok in replay)
- I2 R1 | replay Mooncake FAST25 traces, leaf-only eviction, FLOP-density half-life 180 s | +43..+75% FLOPs saved (8B) and +156..+207% (DSv3 MLA) at 0.5-1M tok; never worse than -5% | WORKS only in capacity-short last tier
- I2 R2 | GDSF aging / 600 s half-life | up to -25% vs LRU at 5-10M tok | rejected; half-life is a tuning hazard
- I2 R3 | move anchor to SSD ADMISSION under endurance budget, per-block | deep blocks useless without ancestors -> ~0 value | bug in design, fixed next
- I2 R4 | chain-level admission, score = P(reuse|bucket) x chain FLOPs / new bytes | DSv3: +37%..+95% SSD value per byte written vs random at 10-35% writes; 8B dense: +11% conv, -18% toolagent | NICHE: MLA-class models
- I2 R5 | economics | wear $0.088/TB written; write-all = $17/day vs $576/day node (DSv3), $80/day + 119 drives' endurance for 70B-BF16 | $ value small except write-capped tiers
