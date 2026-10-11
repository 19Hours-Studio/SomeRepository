The three proposals below each target one or more of the weaknesses you measured:

1. **Self-prediction originality.** Originality is scored as how far an answer lands from what the model itself would predict. The judges are not asked for an opinion on it.
2. **Kill-test pricing of value.** Value counts only after an idea survives an attempt to refute it, so it is no longer an unchecked claim or handed to an unnamed verifier.
3. **Stock-and-scion grafting.** This replaces free-form crossover so that offspring keep their concrete implementation.

Together they address these measured weaknesses: judges sharing the generators' knowledge gaps, run-to-run variance, attractor families reappearing at every layer, value being lower than plain answers, and crossover offspring losing concreteness.

=== IDEAS ===
IDEA 1
NAME: Self-Prediction Surprise Scoring
MECHANISM: Before generating, a "forecaster" agent is told the question and the technique, and writes 10 short predictions of what that technique will produce. Originality is then computed rather than judged: the score is the embedding distance from the answer to the nearest forecast and to all families in a cross-run attractor ledger. Each new family found at any layer is added to the ledger, which every later run loads as forbidden input from the start. Technique choice across runs uses Thompson sampling on the stored scores, and each run uses paired prompts so techniques are compared on the same inputs, which cancels out much of the run-to-run variance.
VALUE: Originality is measured against the model's own predicted outputs, so judges who share the generators' blind spots can no longer reward the obvious, and attractors are pre-empted instead of rediscovered every run.

IDEA 2
NAME: Kill-Test Bounty Value
MECHANISM: Each survivor must arrive with a pre-registered "kill test": the cheapest check whose failure would sink it, such as a back-of-envelope calculation, a search for a counterexample, or a conflict with a known constraint. A separate red-team agent role, rewarded in its prompt and scoring only for confirmed kills, runs that test and up to two of its own using web search and quantitative estimates. Value is then scored as surviving kill attempts multiplied by the size of the stated payoff, which replaces the judges' impression of usefulness. The test types that killed ideas are stored, and future generator prompts are seeded with that list so they avoid known failure patterns.
VALUE: Validity is checked inside the pipeline instead of handed to an external verifier, so original ideas that are actually wrong are filtered out and average value can rise above plain answers.

IDEA 3
NAME: Stock-and-Scion Grafting
MECHANISM: Crossover becomes asymmetric. The more concrete parent is the "stock" and is reduced to a fixed build sheet: its actors, inputs, steps, measurable output and first experiment. The other parent contributes exactly one "scion" mechanism, which must be grafted into a named step of that sheet. A checker agent rejects any offspring that removes or blurs a build-sheet field. The pipeline records which stock–scion pairings held up in final judging and uses that history to weight which families get paired in later runs.
VALUE: Offspring gain novelty from distant families while keeping a runnable implementation, which removes the measured loss of concreteness in crossover.