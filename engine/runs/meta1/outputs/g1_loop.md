**Answer 1: shared errors from manuscript studies (philology)**
- **Diagnostic:** Philologists who trace how copies of a text descend from one another rely on shared errors. If two copies share a rare, distinctive mistake, they come from the same lost ancestor, however different they look on the surface.
- **Port:** Pull out the rare, specific mechanism parts of each idea (for example "pre-registered threshold" or "persona swap"). Two ideas that share such parts likely come from the same hidden attractor, even if the judges put them in different families.
- **Loop:** Every group of ideas that shares two or more rare parts becomes a new family on the forbidden list straight away, at the layer where it shows up. Crossover may only pair parents with no shared rare parts.
- **Honesty:** The closest existing work is text phylogenetics and embedding clustering. Those group ideas by overall similarity; this groups them only by shared rare features, which is the defining move of shared-error analysis.

**Answer 2: mutation testing (software engineering)**
- **Diagnostic:** Mutation testing plants known defects in code and measures what share the test suite catches (the mutation score).
- **Port:** A mutator agent makes broken copies of the surviving ideas: a reversed causal claim, a cost that can't be met, a circular metric. These copies are mixed blind into the judges' batches.
- **Loop:** Each kind of planted defect that the judges miss gets a new scoring item and a dedicated checker role. Real ideas that look like a missed defect are marked "unverified" and lose their value score.
- **Honesty:** The closest existing work is perturbation tests of LLM judges (verbosity bias, for example). Those report bias; they don't build new parts of the pipeline from what got missed.

**Answer 3: estimating unseen species (ecology)**
- **Diagnostic:** The Chao1 estimate and Good-Turing coverage use how many species were seen exactly once or twice to estimate how many species have not been seen yet.
- **Port:** Count how often each family appears in the plain answers and in each technique's outputs. That gives an estimate of how many attractor families are still undiscovered at each layer.
- **Loop:** Generation can't start until coverage of the plain-answer families is at least 0.9; until then the mapping stage keeps sampling. A technique whose outputs keep adding families seen only once is split into versions with different seeds. A technique whose estimate is flat gets deleted.
- **Honesty:** The closest existing work is unseen-species estimation applied to LLM output diversity. That only measures diversity; here the estimate decides stage order and which techniques stay in the portfolio.

=== IDEAS ===
IDEA 1
NAME: Shared-Error Hidden Ancestry
MECHANISM: An extractor agent breaks each idea into its rare mechanism parts, and the pipeline computes which ideas share the same rare parts. Any group sharing two or more becomes a new forbidden family at once, at the current layer, and crossover may only pair parents with no shared rare parts. Part frequencies are stored across runs, so parts that become common stop counting as rare.
VALUE: Hidden attractors are caught at the layer where they appear instead of slipping through the judges' surface-level labels.

IDEA 2
NAME: Mutant Ideas Test Judges
MECHANISM: A mutator agent plants specific defects (reversed causal claims, costs that can't be met, circular metrics) in copies of the survivors and mixes them blind into the judges' batches. For each kind of defect, the share the judges catch is recorded. Kinds they miss create a new scoring item and a checker role, and real ideas that look like missed defects lose their value score.
VALUE: Judges' shared blind spots become checks the pipeline actually runs, which raises the real value of what survives.

IDEA 3
NAME: Unseen-Family Coverage Gate
MECHANISM: For each layer and each technique, the pipeline counts families seen once and twice and computes Chao1 and Good-Turing coverage. Generation can't start until plain-answer coverage is at least 0.9. Techniques that keep adding families seen only once are split into versions with different seeds, and techniques whose estimate is flat are deleted.
VALUE: The pipeline only starts generating once the plain-answer families are close to fully mapped, and it keeps only techniques that keep finding new families.