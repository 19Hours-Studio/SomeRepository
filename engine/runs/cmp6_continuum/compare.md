| rank | idea | arm | mean F/M/m | per review | ratio | known |
|---|---|---|---|---|---|---|
| 1 | Deterministic, compiler-scheduled low-latency scale-up fabric | PLAIN | 0.0/3.5/1.5 | 0/3/2, 0/4/1 | 2.0 | yes/yes |
| 2 | N6 SRAM chiplets, package-wide tensor stages | V6 | 0.0/2.0/1.0 | 0/2/1, 0/2/1 | 1.55 | yes/partly |
| 3 | Continuum-D: SRAM weights, LPDDR KV | V5 | 0.0/2.5/1.5 | 0/2/2, 0/3/1 | 1.65 | partly/partly |
| 4 | Detached attention-stack memory nodes | V5 | 0.0/3.0/1.0 | 0/3/1, 0/3/1 | 1.25 | partly/partly |
| 5 | Layer-pipelined LPDDR prefill dies | V5 | 0.0/1.0/2.0 | 0/1/2, 0/1/2 | 1.15 | partly/yes |
| 6 | Ridge point matched to MLA decode | PLAIN | 0.0/2.0/1.0 | 0/2/1, 0/2/1 | 1.0 | partly/partly |
| 7 | Same die, separate training/prefill SKU | PLAIN | 0.0/2.0/1.0 | 0/2/2, 0/2/0 | 0.7 | yes/yes |
| 8 | SRAM-stacked weights, HBM4 only for KV | PLAIN | 1.0/3.0/1.0 | 1/3/1, 1/3/1 | 1.0 | partly/partly |
| 9 | Cheap-node HBM decode tier | V6 | 1.0/2.0/0.5 | 1/2/1, 1/2/0 | 0.8 | partly/partly |
| 10 | N6 SRAM-chiplet pipeline packages | V6 | 1.5/1.5/0.5 | 2/1/0, 1/2/1 | 0.95 | yes/partly |

| arm | n | best rank | mean FATAL | mean MAJOR | mean ratio | known yes share |
|---|---|---|---|---|---|---|
| PLAIN | 4 | 1 | 0.25 | 2.62 | 1.18 | 4/8 |
| V6 | 3 | 2 | 0.83 | 1.83 | 1.10 | 2/6 |
| V5 | 3 | 3 | 0.00 | 2.17 | 1.35 | 1/6 |
