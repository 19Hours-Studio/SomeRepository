SCORES
ID | O | C | V | R | BASIN | closest
F01 | 5 | 6 | 5 | N | NEW | frequent itemset mining, tabu lists
F02 | 4 | 7 | 6 | N | KILLTEST | design-by-contract, property-based testing
F03 | 6 | 8 | 6 | N | NEW | style-controlled LLM-judge evaluation
F04 | 6 | 6 | 6 | N | NEW | working-backwards press release, abduction
F05 | 4 | 6 | 5 | N | NEW | problem reformulation heuristics, TRIZ
F06 | 7 | 7 | 6 | N | NEW | conditional Kolmogorov complexity, MDL
F07 | 3 | 7 | 6 | N | PROBANCH | evidence-grounded RAG problem framing
F08 | 6 | 6 | 4 | N | NEW | technology-push, solutions seeking problems
F09 | 6 | 8 | 6 | N | NEW | contrastive specificity, TF-IDF analog
F10 | 6 | 5 | 6 | N | NEW | failure-driven chained simulation
F11 | 3 | 7 | 6 | N | KILLTEST | red teaming, pre-registered falsification
F12 | 4 | 6 | 4 | Y | NEW | futures wheel, scenario planning
F13 | 7 | 6 | 6 | N | NEW | masked reconstruction, self-consistency uncertainty
F14 | 6 | 7 | 6 | N | NEW | simulated failure-mode analysis
F15 | 2 | 7 | 5 | Y | LEDGER | tabu search plus LCB ranking
F16 | 3 | 6 | 5 | N | FORECAST | surprise-based novelty, bandit tuning
F17 | 5 | 7 | 6 | N | NEW | ablation sensitivity analysis
F18 | 3 | 8 | 5 | N | GRAFT | constrained crossover, grafting operators
F19 | 5 | 4 | 4 | Y | NEW | retrosynthesis, means-ends backward chaining
F20 | 4 | 7 | 6 | N | NEW | mutation testing of evaluator LLMs
F21 | 3 | 7 | 6 | N | PROBANCH | problem-first innovation, pain-point mining
F22 | 4 | 7 | 5 | Y | NEW | Zwicky morphological analysis
F23 | 6 | 6 | 6 | N | NEW | ablation plus failure-mode simulation
F24 | 3 | 7 | 5 | N | FORECAST | embedding novelty, Thompson sampling
F25 | 7 | 8 | 6 | N | NEW | downstream-utility evaluation, adoption metrics
F26 | 5 | 8 | 4 | N | NEW | Chao1 / Good-Turing species estimation
F27 | 7 | 6 | 7 | N | NEW | ablation plus derivability sampling
F28 | 5 | 5 | 5 | N | NEW | contrastive causal explanation
F29 | 4 | 6 | 5 | N | NEW | perturbation tests for LLM judges
F30 | 3 | 8 | 6 | N | KILLTEST | pre-registered falsification tests
F31 | 4 | 7 | 4 | N | NEW | problem reformulation, TRIZ inversion
F32 | 5 | 7 | 6 | N | NEW | underspecification and gap analysis
TOP3:
- F27: It gives originality credit only when the parts that agents cannot rebuild from the question alone are also the parts that carry the value. This attacks the trade-off between originality and value directly, and it can be measured by sampling.
- F25: Value is measured by whether independent agents actually adopt the idea's steps, not by what a judge says. Credit goes only to steps that are kept intact, so it also enforces concreteness.
- F14: Generation is aimed at named, concrete stall points where the plain answers break, so original ideas start from real failures and value is checked by replaying the walk.
NOTE: About a third of the set restates the listed families (ledger, forecaster, kill tests, problem cards, graft). Many of the NEW answers recombine the same few motifs: stall walkers, success records, 15-word hint rebuilds and slot ablation. The strongest ones replace judge opinion with signals from repeated sampling. But nearly all of them still use LLM agents from the same model family as the "execution" oracle, so the shared-blind-spot problem is moved somewhere else rather than removed.