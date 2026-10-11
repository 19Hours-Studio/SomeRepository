**1. Mass-balance closure (analytical chemistry)**
Diagnostic: when the quantified components of a sample add up to less than 100%, the missing mass means a compound nobody has identified yet.
Port: break each activation down into a sparse dictionary of named concepts (SAE features) and measure the residual mass that the dictionary does not explain.
Loop: when that residual is large, low-entropy and recurs across many contexts, the system creates a new atom and a new token type for it. It then trains the generator to emit and compose with that token. The model gets a primitive that has no name anywhere in its corpus.
Honesty check: the closest work is SAE "dark matter" analysis (Engels et al. 2024). That work only reports the residual. Here the residual becomes a token the model can generate with, which is the new part.

**2. Linkage disequilibrium (population genetics)**
Diagnostic: Hardy-Weinberg and LD tests compare how often alleles actually occur together against the product of their marginal frequencies. A deviation shows hidden population structure.
Port: compute D = P(a,b) − P(a)P(b) for pairs of concept features in the model's internal representations.
Loop: some pairs have high |D|, yet a verifier accepts outputs where one feature is present without the other. These are bundles inherited from the corpus, not logical necessities. The system splits the shared units into two independently addressable units and retypes each one. Originality comes from separating concepts that human data always fused, as happened historically when mass was separated from weight.
Honesty check: the closest work is β-VAE disentanglement and SAE feature splitting. Those apply a global pressure or happen as a side effect of scale. This version is targeted, uses a statistical test and needs verifier confirmation.

**3. Species-coverage estimation (ecology)**
Diagnostic: Chao1 and Good-Turing sample coverage, C = 1 − f₁/n, estimate how many species remain unseen from the counts of singletons and doubletons.
Port: cluster the generator's outputs inside each concept region and estimate coverage for that region.
Loop: once C ≈ 1, the region's support is closed and more sampling only repeats it. The system then inserts a permanent projection gate that removes that region's principal output directions for that context. It also grows a fresh low-rank adapter, initialised orthogonally, and trains it only on verified outputs outside the old support.
Honesty check: the closest work is novelty search and coverage-based diversity metrics. Those reward or score outputs, which is close to ANTIPRED. Here the estimator changes the architecture instead of the reward.

=== IDEAS ===
IDEA 1
NAME: Mass-Balance Concept Minting
MECHANISM: Activations are decomposed into a dictionary of sparse concept features, and the unexplained residual "mass" is tracked per context class. When the residual is large, structured (low-entropy) and recurrent, it becomes a new dictionary atom and a new vocabulary token. The generator is then fine-tuned to produce and compose with that token. The ledger of residual mass is recomputed after every mint.
VALUE: It turns representational content that has no human name into usable building blocks for generation.

IDEA 2
NAME: Linkage-Disequilibrium Concept Unbundling
MECHANISM: The system computes D = P(a,b) − P(a)P(b) over pairs of internal features. For strongly linked pairs it asks a verifier whether outputs with one feature but not the other are valid. If they are, the shared units are split into two independently addressable units and each is retyped. The resulting set of primitives is recorded, and LD is re-estimated over time.
VALUE: The model can think with distinctions that its training data always merged.

IDEA 3
NAME: Coverage-Saturation Support Closure
MECHANISM: Outputs are clustered per concept region, and Good-Turing/Chao1 coverage is estimated from singleton and doubleton counts. When coverage saturates, the system inserts a permanent projection gate that removes that region's dominant output directions. It then grows an orthogonally initialised adapter that is trained only on verified outputs beyond the closed support. The gates and adapters build up as a map of regions that have been exhausted.
VALUE: The model stops resampling familiar ground and gains new capacity exactly where its corpus-derived repertoire has run out.