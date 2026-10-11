# Отчёт прогона `meta1`

Вопрос: You are improving an automated pipeline that generates highly original ideas for hard open questions. The pipeline orchestrates LLM subagents (no access to model weights or training) in these stages: (1) attractor mapping: a few plain answers are clustered by a judge into idea families; (2) a portfolio of five prompt techniques generates answers while those families are forbidden; (3) two blind LLM judges score originality, concreteness and value and classify each answer into a family or NEW; (4) survivors get a web literature check; (5) survivors from different families are crossed over, with repulsion from known families and from the nearest literature; (6) final blind judging. Measured weaknesses: average value is lower than plain answers; crossover offspring lose concreteness; validity is usually delegated to an unspecified external verifier; the judges are the same model family as the generators and share its knowledge gaps; run-to-run variance is larger than most differences between techniques; new attractor families appear at every layer. How could this pipeline be changed so it produces ideas that are both more original and more valuable? Every mechanism must be implementable as a change to this pipeline: prompts, agent roles, stage order, selection or scoring rules, or data kept between runs.

| arm | n | O | C | V | O×V | top3 O×V | NEW-доля | R=Y (все судьи) |
|---|---|---|---|---|---|---|---|---|
| control | 9 | 3.00 | 7.00 | 5.83 | 17.7 | 21.7 | 0.00 | 1/9 |
| engine | 23 | 5.37 | 6.24 | 5.43 | 29.7 | 44.3 | 1.00 | 1/23 |

## Лучшие идеи

| id | arm | O | V | O×V | бассейны | литература | name |
|---|---|---|---|---|---|---|---|
| g2_evo2#1 | engine | 7.0 | 7.0 | 49.0 | NEW/NEW | — | Surprise-Must-Carry-Value Map |
| g1_mech#2 | engine | 7.0 | 6.0 | 42.0 | NEW/NEW | PARTIAL | Hint-Gap Selection |
| g2_evo1#1 | engine | 7.0 | 6.0 | 42.0 | NEW/NEW | — | Downstream Convergence Gap Filling |
| g2_imm#3 | engine | 6.5 | 6.0 | 39.0 | NEW/NEW | — | Peer Uptake Count |
| g1_mech#3 | engine | 6.0 | 6.0 | 36.0 | NEW/NEW | PARTIAL | Outcome-First Reverse Build |
| g2_imm#2 | engine | 6.0 | 6.0 | 36.0 | NEW/NEW | — | Decoy-Question Specificity Margin |
| g2_evo1#2 | engine | 6.0 | 6.0 | 36.0 | NEW/NEW | — | Stall-Shift Slot Carving |
| g2_evo2#2 | engine | 6.0 | 6.0 | 36.0 | NEW/NEW | — | Stall-Pinned Record Chains |
| g1_neg#2 | engine | 5.5 | 6.5 | 35.8 | NEW/NEW | PARTIAL | Hand-Wave Mining |
| g1_mech#1 | engine | 5.5 | 6.5 | 35.8 | NEW/NEW | PARTIAL | Stall-Point Seeding |
