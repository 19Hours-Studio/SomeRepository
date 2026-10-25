| rank | idea | arm | mean F/M/m | per review | ratio | known |
|---|---|---|---|---|---|---|
| 1 | Same die, separate training/prefill SKU | BASE | 0.0/1.0/1.5 | 0/1/2, 0/1/1 | 0.7 | yes/yes |
| 2 | Layer-pipelined LPDDR prefill dies | ENGINE | 0.0/1.5/2.0 | 0/2/2, 0/1/2 | 1.1 | yes/yes |
| 3 | Ridge point matched to MLA decode | BASE | 0.0/1.5/1.0 | 0/2/1, 0/1/1 | 1.0 | partly/partly |
| 4 | SRAM-stacked weights, HBM4 only for KV | BASE | 0.0/2.0/2.5 | 0/2/2, 0/2/3 | 1.1 | partly/partly |
| 5 | Continuum-D: SRAM weights, LPDDR KV | ENGINE | 0.0/2.5/2.0 | 0/3/2, 0/2/2 | 2.3 | partly/partly |
| 6 | Deterministic, compiler-scheduled low-latency scale-up fabric | BASE | 0.0/2.5/1.5 | 0/3/1, 0/2/2 | 1.75 | yes/yes |
| 7 | Detached attention-stack memory nodes | ENGINE | 0.0/2.5/1.5 | 0/3/1, 0/2/2 | 1.27 | yes/yes |

| arm | n | best rank | mean FATAL | mean MAJOR | mean ratio | known yes share |
|---|---|---|---|---|---|---|
| BASE | 4 | 1 | 0.00 | 1.75 | 1.14 | 4/8 |
| ENGINE | 3 | 2 | 0.00 | 2.17 | 1.56 | 4/6 |
