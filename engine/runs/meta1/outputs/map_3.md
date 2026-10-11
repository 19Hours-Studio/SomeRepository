The pipeline's main gaps are that its validity checks are outsourced, its judges share the generators' blind spots, and it forgets what it learned between runs. The three changes below target those structural causes; they are not tweaks to the prompt techniques.

=== IDEAS ===
IDEA 1
NAME: Executable Kill-Test Gate
MECHANISM: Add a "kill-test engineer" agent after blind judging. For each survivor it writes the cheapest decisive test the pipeline can run itself: a short code simulation, an order-of-magnitude calculation, or a targeted search with a pre-registered expected result. The pipeline runs the test, and the judges' value score is multiplied by the outcome (pass, partial or fail). Failed tests and their reasons go into a persistent library. In later runs that library acts as a repulsion constraint for generation and crossover, and serves as reusable test templates. Crossover offspring must inherit at least one parent's passing test unchanged. This stops them from blending away concrete detail.
VALUE: Validity moves inside the pipeline instead of going to an unnamed external verifier, so the ideas that rank highest have survived a real check and are not just plausible to the same model that wrote them.

IDEA 2
NAME: Grounded Constraint Dossier
MECHANISM: Before attractor mapping, a retrieval agent builds a dossier of real-world constraints for each question. It covers documented failed attempts, cost and scale limits, practitioner complaints, and open-problem statements, each with a source. Every generated idea must name the dossier constraint it removes and say how. Judges score value only against the cited constraint and its evidence, not their own intuition. The dossier persists across runs. Constraints that no idea has resolved gain weight and are handed to the generators as explicit targets.
VALUE: Value is anchored in external evidence rather than the judges' shared knowledge gaps, which should close the value gap with plain answers while still pushing originality toward constraints that remain unsolved.

IDEA 3
NAME: Cross-Run Attractor Ledger
MECHANISM: Keep a persistent ledger of every idea family detected at any layer, in any run, with descriptions and the layer where each family first appeared. Each new run starts with the whole ledger forbidden. Families that first appeared late in a run are fed back as seeds for the next run's attractor mapping. Final selection uses replicated scoring: three judge resamples with shuffled order and swapped judge roles. Ideas are ranked by the lower confidence bound of their score, not the mean, so only results that stay stable across judges are kept.
VALUE: Each run starts beyond everything earlier runs found, and the ranking filters out wins that are just run-to-run noise. Improvements then add up across runs instead of being lost to variance.