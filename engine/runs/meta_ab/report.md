# Отчёт прогона `meta_ab`

Вопрос: Propose a new architecture for an AI accelerator chip, named "Continuum", that could credibly be called the best in the world. The asker has not said which workloads count: training, inference, or both. They have not said what "best" is measured by, or which kind of target (data center, edge, or other) the chip is for. A good answer therefore has to state its own target workloads and metrics, then defend the architecture against the current leading designs. Those designs include GPUs such as the Nvidia Rubin class, Google TPUs such as Ironwood, and SRAM-centric dataflow chips such as Cerebras WSE-3 and Groq LPU. The architecture should cover compute, memory hierarchy, interconnect, numerics, programming model, packaging and power. It should cite known physical, economic and manufacturing limits, and say what would need to be true for it to work. Reported 2026 reference points are listed in CONTEXT. Many are vendor or blog figures, and the sources disagree on some numbers.

| arm | n | O | C | V | O×V | top3 O×V | NEW-доля | R=Y (все судьи) |
|---|---|---|---|---|---|---|---|---|
| C | 6 | 3.08 | 5.00 | 5.25 | 16.0 | 20.2 | 1.00 | 3/6 |
| COMP | 6 | 5.08 | 5.58 | 6.08 | 30.8 | 35.0 | 1.00 | 0/6 |
| INS | 6 | 3.58 | 4.92 | 5.67 | 20.2 | 25.7 | 1.00 | 2/6 |

## Лучшие идеи

| id | arm | O | V | O×V | бассейны | литература | name |
|---|---|---|---|---|---|---|---|
| comp1#2 | COMP | 6.0 | 6.0 | 36.0 | NEW/NEW | — | Checksum-governed adaptive precision |
| comp2#2 | COMP | 6.0 | 6.0 | 36.0 | NEW/NEW | — | Circulating optical weight broadcast |
| comp1#3 | COMP | 5.5 | 6.0 | 33.0 | NEW/NEW | — | Softmax-merging optical switches |
| comp2#3 | COMP | 5.0 | 5.5 | 27.5 | NEW/NEW | — | Error-budgeted escalating numerics |
| ins1#1 | INS | 4.0 | 6.5 | 26.0 | NEW/NEW | — | Near-Bank Associative Attention |
| ins2#2 | INS | 4.0 | 6.5 | 26.0 | NEW/NEW | — | Associative in-DRAM attention retrieval |
| comp1#1 | COMP | 4.0 | 6.5 | 26.0 | NEW/NEW | — | Retrieval-native HBM base die |
| comp2#1 | COMP | 4.0 | 6.5 | 26.0 | NEW/NEW | — | Compressed-domain attention in HBM |
| ins2#3 | INS | 5.0 | 5.0 | 25.0 | NEW/NEW | — | Wavelength-addressed expert routing fabric |
| c2#3 | C | 5.5 | 4.5 | 24.8 | NEW/NEW | — | Compiler-Scheduled Power Envelope |
