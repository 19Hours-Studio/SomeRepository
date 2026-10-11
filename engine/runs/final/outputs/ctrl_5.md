Recombination happens because generation is anchored to the training distribution: the model samples where the density is high. To get original ideas, the system needs a source of structure that isn't the corpus, plus a test against reality that rewards distance from consensus rather than closeness to it. Each mechanism below provides both.

**1. Ontology mutation.** Don't perturb outputs. Perturb the model's concepts. Take the learned feature directions (from sparse dictionaries or circuits) and ablate, merge, split or re-wire them, so you get "mutant" worldviews that carve reality in ways no human text does. Each mutant is checked against held-out observations. A mutant survives only if it predicts something the original concepts miss.

**2. Synthetic-universe transfer.** The system invents formal micro-worlds: rule systems, algebras and physics it generates itself and that appear in no data. It explores them by simulation and proof search, and stores the deep structures it finds there. When it faces a real problem, it searches for a structural match with these alien results. That brings in ideas whose origin is outside human culture entirely.

**3. Contrarian prediction market.** Many internal sub-models hold different hypotheses and bet on future observations or experiment outcomes. Payouts scale with how far a winning bet was from the consensus prior. Capital, meaning compute and influence on output, flows to minority views that turn out right. This selects for ideas that are both new and true.

=== IDEAS ===
IDEA 1
NAME: Ontology Mutation with Reality Selection
MECHANISM: Interpretability tools pull out the model's internal concept dictionary (feature directions or circuits). An evolutionary loop then mutates it by ablating, splitting, merging and re-binding features, which produces alternative ontologies. Small probe heads trained on each mutant ontology are scored on how well they predict held-out real-world data that the base model predicts poorly. Mutants that win are kept in an archive and folded back into the base through distillation, and the mutation rates adapt toward the operator types that succeed.
VALUE: The system can find new ways of carving up reality, not just new combinations of the concepts it already has.

IDEA 2
NAME: Synthetic Universe Transfer
MECHANISM: A generator invents formal micro-worlds such as rule sets, algebras and toy physics. A solver explores each one by simulation and proof search, and stores the invariants, theorems and dynamics it finds as graph-structured motifs. For a real problem, a structure-matching module searches this motif library for homomorphisms to the problem's formalization and turns any match into a candidate method. Universes whose motifs transfer often get more generation budget.
VALUE: Ideas can come from structures that were never in human data, while staying grounded through tested transfer to real problems.

IDEA 3
NAME: Contrarian Internal Prediction Market
MECHANISM: A population of sub-models, each holding an explicit hypothesis, places stakes on predictions that can be checked against experiments, simulations or future data. When an outcome resolves, payout is weighted by how far the winning bet sat from the population's consensus distribution. Accumulated capital decides each sub-model's share of compute and its weight in final answers. Bankrupt hypotheses are replaced by mutated copies of rich contrarians.
VALUE: Persistent, rewarded dissent replaces averaging toward the consensus, so the system selects for ideas that are both non-obvious and correct.