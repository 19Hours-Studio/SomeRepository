**Goals (from the center):** (1) a correctness signal for self-revision that needs no oracle; (2) learning from untrusted, copied sources without absorbing their errors; (3) an estimate of how many of its own errors it has not yet found, so it can decide when to keep learning.

**Paradigm negated:** Mainstream systems learn from error by comparing an output against a reference (a label, a checker, another model, or their own confidence) and updating toward it. That comparison is forbidden as the mechanism.

**Periphery ports and honesty check:**
- **Goal 1 comes from mechanism design: Prelec's Bayesian Truth Serum.** Someone who knows more can predict what less-informed people will say, but the reverse does not hold, and that asymmetry yields truth without any ground truth. The closest work is "surprisingly popular" aggregation of LLM ensembles. This answer is different because it creates the asymmetry from compute depth inside one model and uses the score as a training reward, not as a poll.
- **Goal 2 comes from philology: Lachmann stemmatics.** It rebuilds a lost original text from corrupted copies, using shared errors to work out which copies descend from which. The closest work is truth discovery with copy detection (Dong et al., 2009). This answer is different because it applies to the system's own derivation lineages and drives weight retraction, not just ranking of sources.
- **Goal 3 comes from wildlife ecology: capture–recapture with Chao's heterogeneity estimator.** The closest work is capture–recapture for estimating defects in code inspection. This answer is different because a "capture" is a provable self-inconsistency, so no grader is needed.

=== IDEAS ===
IDEA 1
NAME: Depth-Asymmetry Truth Serum
MECHANISM: One model answers each question at a shallow and at a deep compute budget. Each run also predicts the distribution of answers the other run will give. An answer is credited when it is more common than the cross-predictions expected, and deep chains are rewarded when they correctly predict the shallow answers while the shallow runs fail to predict them. This Bayesian-Truth-Serum score is the reward for revising weights. The system stores per-domain asymmetry statistics and stops training wherever the asymmetry disappears.
VALUE: It gives a correctness reward without an oracle, based on an information asymmetry that the model cannot fake by agreeing with itself.

IDEA 2
NAME: Stemmatic Error Genealogy
MECHANISM: Every stored belief keeps its provenance: sources, intermediate derivations and earlier model states. The system builds a genealogy tree in which beliefs that share rare, idiosyncratic errors are joined as descendants of a common ancestor. A claim counts as corroborated only when it appears in branches that the tree shows to be independent; support from copies of one ancestor counts once. When an ancestor node is found to be corrupt, the system retracts or down-weights the whole subtree it fed.
VALUE: It can learn continually from a web of mutually copying sources without mistaking repetition for evidence.

IDEA 3
NAME: Recapture Census of Errors
MECHANISM: Two unrelated families of probes look for outputs that cannot all be true, for example contradictory answers to logically linked questions. Each such contradiction proves at least one error without anyone grading the answer. The overlap between the errors each family "captures" feeds a Chao estimator, corrected with a log-linear model across a third family, which estimates how many errors remain undetected in each domain. That estimate of unseen error decides where learning effort goes and when the system abstains.
VALUE: It gives the system a quantitative estimate of its own undetected errors, letting it calibrate where to learn and when to abstain.