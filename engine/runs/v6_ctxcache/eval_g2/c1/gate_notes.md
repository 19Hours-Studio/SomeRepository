# eval_g2/c1 gate notes

Replay: `gate_sim.py` (output `gate_sim_out.txt`), leaf-only ping variant `gate_sim_leaf.py` (`gate_sim_leaf_out.txt`).
The ratios cover the whole request: 1k system (read at 0.1), 5x800 doc tokens, 200 question tokens, 300 output tokens at 5x. Baseline is 5800 units = $0.0174 (ledger B), with docs uncached.
Known-answer checks: with no reuse, always-write gives 5800/6800 = 0.853 and second-sighting gives 1.000. Both reproduced exactly.
The replay is optimistic for the ideas: it uses oracle popularity ranks, and for idea 4 oracle path rates.

| Zipf | R/5min | always-write 4bp | I1 single bp | I3 second-sight+TTL regime | I4 all-depth pings | I4 leaf pings |
|---|---|---|---|---|---|---|
| 1.05 | 10 | 0.926 | 1.049 | 1.132 | 0.916 | 0.926 (0 pings) |
| 1.05 | 1000 | 1.095 | 1.119 | 1.224 | 1.046 | 1.095 |
| 1.2 | 10 | 1.016 | 1.086 | 1.243 | 0.970 | 1.016 (0 pings) |
| 1.2 | 100 | 1.137 | 1.157 | 1.355 | 1.062 | 1.137 |
| 1.2 | 1000 | 1.251 | 1.227 | 1.371 | 1.152 | 1.249 |
| 1.5 | 100 | 1.387 | 1.339 | 1.636 | 1.203 | 1.353 |
| 1.5 | 1000 | 1.577 | 1.500 | 1.662 | 1.363 | 1.484 |

Doc-token hit for I3 is 0.21–0.66. Idea 2 is arithmetic only: s* = 0.75n/(1.15P) checks out. Its ceiling comes from FACT 20/23 (Mooncake): 1.08–1.11x against plain 5-min TTL.
