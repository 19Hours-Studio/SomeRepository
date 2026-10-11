**Diagnostic loops**

1. Pharmacology, the Schild plot. You plot log(dose-ratio − 1) against log(antagonist concentration). A slope of 1 means one competitive binding site. Any other slope means a hidden second site or mechanism.
   - Port: treat two cues as agonist and antagonist acting on one internal unit or feature. Measure how much of cue A is needed to restore the output as cue B increases.
   - Loop: when the slope is not 1, split the unit into two "receptor sites", each with its own gate.
   - Honesty: sparse autoencoders and polysemanticity work find mixed features from activation statistics. None use a dose-response invariant to trigger splits at runtime.

2. Genetics, the complementation test. Two recessive mutants are crossed. If the offspring look normal, the defects are in different genes. If not, they are in the same gene.
   - Port: two parameter lesions that each cause the same failure are "crossed" by splicing activations from both lesioned copies.
   - Loop: the complementation groups found this way become the module boundaries, and parameters are re-assigned to modules.
   - Honesty: ablation studies and circuit discovery do lesioning, but they don't use pairwise complementation to define and rebuild module partitions.

3. Phylogenetics, the four-point condition. A distance matrix is tree-like only if, for every set of four taxa, the two largest of the three pairwise sums are equal. Violations reveal hybridization or horizontal transfer.
   - Port: run the test over concept embeddings that the system's taxonomy treats as a tree.
   - Loop: quartets that violate it turn a node into a reticulation node with two parents. Inheritance and inference then flow along both lineages.
   - Honesty: Gromov δ-hyperbolicity (Khrulkov 2020) only measures tree-likeness, and hyperbolic embeddings assume a tree. Neither rewires a live concept hierarchy.

FIRST THOUGHTS:
- Fast generator plus slow verifier loop
- Latent world model with planning
- Neurosymbolic program-synthesis library
- Episodic memory with sleep consolidation
- Explicit causal graph revised by surprise

=== IDEAS ===
IDEA 1
NAME: Schild-Slope Feature Splitting
MECHANISM: For pairs of cues that compete over an internal feature, the system measures dose-response shifts, meaning how much more of cue A is needed as cue B increases, and fits a Schild slope. A slope of 1 confirms that one mechanism mediates both cues. If the slope differs from 1, the feature is split into two sites, each with its own learned gate. The slopes are stored per feature, and they are re-tested whenever new competing cues show up.
VALUE: Features that are secretly several mechanisms get found and separated by a quantitative invariant, so the model's internals become more faithful and reasoning that combines cues becomes more reliable.

IDEA 2
NAME: Complementation-Group Remodularization
MECHANISM: When a behavior fails, the system creates small parameter lesions that reproduce the failure. Pairs of lesions are "crossed" by mixing activations from the two lesioned copies. If the mix restores the behavior, the lesions sit in different functional units. If it doesn't, they sit in the same one. The groups found this way define module boundaries, and parameters are re-partitioned and re-routed to match. A map of the groups is stored and updated as new failures appear.
VALUE: The module structure comes from functional evidence, not from a design chosen in advance, so fixes, transfer and growth stay local to the unit that is actually responsible.

IDEA 3
NAME: Four-Point Reticulate Concept Hierarchy
MECHANISM: The system continuously runs the four-point condition on embedding distances among concepts in its taxonomy. Quartets that violate it point to hybrid concepts, and those concepts are re-typed as reticulation nodes with two weighted parent lineages. Properties are then inherited from both parents. The violation magnitudes are stored, and edges are reweighted as evidence accumulates.
VALUE: The system can represent and reason about concepts that blend lineages, such as loanwords, hybrid organisms or mixed genres, which strictly tree-shaped hierarchies get wrong.