# Отчёт прогона `meta_ab`

Вопрос: Propose a new architecture for an AI accelerator chip, named "Continuum", that could credibly be called the best in the world. The asker has not said which workloads count: training, inference, or both. They have not said what "best" is measured by, or which kind of target (data center, edge, or other) the chip is for. A good answer therefore has to state its own target workloads and metrics, then defend the architecture against the current leading designs. Those designs include GPUs such as the Nvidia Rubin class, Google TPUs such as Ironwood, and SRAM-centric dataflow chips such as Cerebras WSE-3 and Groq LPU. The architecture should cover compute, memory hierarchy, interconnect, numerics, programming model, packaging and power. It should cite known physical, economic and manufacturing limits, and say what would need to be true for it to work. Reported 2026 reference points are listed in CONTEXT. Many are vendor or blog figures, and the sources disagree on some numbers.

| arm | n | O | C | V | O×V | top3 O×V | NEW-доля | R=Y (все судьи) |
|---|---|---|---|---|---|---|---|---|
| AUDIT | 6 | 2.25 | 4.50 | 5.50 | 12.2 | 13.8 | 1.00 | 5/6 |
| C | 6 | 3.33 | 4.75 | 5.25 | 17.4 | 22.2 | 1.00 | 2/6 |
| CLEAR | 6 | 3.83 | 5.08 | 5.75 | 22.0 | 28.2 | 1.00 | 2/6 |
| COMP | 6 | 4.67 | 5.17 | 5.83 | 27.2 | 31.2 | 1.00 | 0/6 |
| INS | 6 | 3.42 | 4.50 | 5.50 | 18.8 | 22.7 | 1.00 | 1/6 |
| PRESS | 6 | 4.25 | 3.92 | 5.92 | 24.9 | 31.8 | 1.00 | 2/6 |
| RIVAL | 6 | 4.25 | 5.08 | 5.92 | 25.5 | 33.7 | 1.00 | 1/6 |
| ZERO | 6 | 2.67 | 4.83 | 5.17 | 13.8 | 17.2 | 1.00 | 3/6 |

## Лучшие идеи

| id | arm | O | V | O×V | бассейны | литература | name |
|---|---|---|---|---|---|---|---|
| rival2#3 | RIVAL | 6.0 | 6.5 | 39.0 | NEW/NEW | — | Optical Weight-Broadcast Fabric |
| comp1#3 | COMP | 6.0 | 6.0 | 36.0 | NEW/NEW | — | Softmax-merging optical switches |
| rival1#2 | RIVAL | 6.0 | 6.0 | 36.0 | NEW/NEW | — | Photonic Multicast Weight Streaming |
| press1#3 | PRESS | 6.0 | 6.0 | 36.0 | NEW/NEW | — | Physical Optical Gradient Summation |
| comp2#2 | COMP | 5.0 | 6.0 | 30.0 | NEW/NEW | — | Circulating optical weight broadcast |
| clear2#3 | CLEAR | 5.0 | 6.0 | 30.0 | NEW/NEW | — | Optical weight broadcast fabric |
| press1#2 | PRESS | 6.0 | 5.0 | 30.0 | NEW/NEW | — | Retrieval-Replaced Feed-Forward Layers |
| press2#2 | PRESS | 4.5 | 6.5 | 29.2 | NEW/NEW | — | Charge-Recycling Resonant Tensor Arrays |
| comp1#2 | COMP | 5.0 | 5.5 | 27.5 | NEW/NEW | — | Checksum-governed adaptive precision |
| clear1#3 | CLEAR | 5.5 | 5.0 | 27.5 | NEW/NEW | — | Early-Terminating MSB-First Arithmetic |
