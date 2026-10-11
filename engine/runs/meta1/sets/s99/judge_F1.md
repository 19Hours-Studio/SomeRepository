SCORES
ID | O | C | V | R | BASIN | closest
F01 | 5 | 6 | 5 | N | NEW | atypical-combination novelty metrics (Uzzi)
F02 | 4 | 7 | 7 | N | KILLTEST | executable verification, AI-Scientist-style checks
F03 | 5 | 8 | 6 | N | NEW | LLM-judge style bias, paraphrase robustness
F04 | 6 | 6 | 6 | N | NEW | Amazon PR-FAQ, backcasting
F05 | 4 | 6 | 5 | N | NEW | problem reformulation, step-back prompting
F06 | 7 | 6 | 6 | N | NEW | conditional compressibility, MDL novelty
F07 | 3 | 6 | 6 | N | PROBANCH | evidence-grounded problem framing, RAG ideation
F08 | 5 | 5 | 4 | N | NEW | solutions-seeking-problems, garbage-can model
F09 | 6 | 7 | 6 | N | NEW | negative controls, contrastive specificity
F10 | 6 | 5 | 6 | N | NEW | backcasting plus plan simulation
F11 | 3 | 7 | 7 | N | KILLTEST | pre-registration, red-team falsification
F12 | 4 | 6 | 4 | N | NEW | futures wheel, scenario planning
F13 | 7 | 5 | 6 | N | NEW | masked reconstruction, ensemble disagreement
F14 | 5 | 7 | 7 | N | NEW | plan simulation, failure-driven ideation
F15 | 2 | 7 | 5 | Y | LEDGER | novelty-search archive, LCB ranking
F16 | 3 | 6 | 5 | N | FORECAST | novelty search, bandit selection
F17 | 5 | 6 | 6 | N | NEW | ablation, sensitivity analysis
F18 | 3 | 8 | 6 | N | GRAFT | template-constrained recombination
F19 | 4 | 4 | 4 | N | NEW | retrosynthesis, HTN backward chaining
F20 | 5 | 7 | 6 | N | NEW | mutation testing, judge perturbation audits
F21 | 3 | 6 | 7 | N | PROBANCH | needs-finding, problem-first ideation
F22 | 4 | 7 | 5 | Y | NEW | Zwicky morphological analysis
F23 | 6 | 5 | 6 | N | NEW | ablation plus plan simulation
F24 | 3 | 7 | 5 | N | FORECAST | novelty search, Thompson sampling
F25 | 6 | 7 | 6 | N | NEW | adoption/uptake metrics, peer influence
F26 | 6 | 7 | 4 | N | NEW | Chao1 / Good-Turing richness estimation
F27 | 7 | 6 | 7 | N | NEW | ablation plus derivability sampling
F28 | 5 | 5 | 5 | N | NEW | contrastive explanation, backcasting
F29 | 5 | 5 | 5 | N | NEW | mutation testing for judges
F30 | 3 | 8 | 7 | N | KILLTEST | pre-registered tests, AI Scientist
F31 | 4 | 6 | 4 | N | NEW | problem reformulation, TRIZ/SCAMPER
F32 | 6 | 6 | 7 | N | NEW | plan elaboration, gap analysis
TOP3:
F27 - credits originality only where the non-derivable parts carry the value, which goes straight at the originality-vs-value tradeoff, and it can be measured by sampling.
F14 - gives generators real failure points to aim at and checks the result by replay, so value is grounded without an external verifier.
F02 - puts falsifiable checks inside the pipeline and uses slot-preserving crossover, which fixes both the validity-delegation weakness and the concreteness-loss weakness.
NOTE: The listed families (KILLTEST, PROBANCH, FORECAST, LEDGER, GRAFT) each show up as several near-duplicates. The NEW answers also collapse into a few unlisted families that repeat across IDs: walker/stall replay (F10, F14, F23), slot ablation and derivability (F17, F23, F27), backward success records (F04, F10, F28), question mutation (F05, F31) and planted-defect judge audits (F20, F29). The new-attractor problem shows up in this answer set too.