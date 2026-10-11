FIRST THOUGHTS:
- A latent world model that plans over imagined rollouts (WMPLAN)
- A library of small programs as causal simulators, revised by synthesis (PROGSYN)
- An episodic memory consolidated offline through replay (CONSOL)
- An explicit causal graph revised from prediction error (CAUSGR)
- A competence map that routes between answering and abstaining (COMPMAP)

Diagnostics and how each one closes the loop:
1. Structural engineering: Maxwell–Calladine rigidity counting. It uses the null space of the rigidity matrix to find floppy mechanisms and states of self-stress. In the ported version, the floppy modes trigger new "bracing" variables, and self-stress triggers splits. Closest existing work is rigidity in sensor-network localization and regularizers for knowledge-graph embeddings. Neither of those adds structure, so this is not the same thing.
2. Population genetics: the Wahlund effect, a heterozygote deficit compared with Hardy–Weinberg expectations, which reveals hidden subpopulations. In the ported version, a unit that fails the test is split and given a new type. Closest existing work is detecting polysemantic features with sparse autoencoders (SAEs) and growing mixtures of experts. Those find split points after the fact or by load, not with an equilibrium test that triggers a split while the system runs.
3. Geodesy: traverse misclosure around closed survey loops, broken apart with a Hodge decomposition. In the ported version, each component of the decomposition triggers a different repair. Closest existing work is cycle-consistency losses, HodgeRank and sheaf neural networks. Those reduce inconsistency as a loss; none of them uses the harmonic part to create new context variables.

=== IDEAS ===
IDEA 1
NAME: Rigidity-Counted Concept Frameworks
MECHANISM: Concepts are stored as points in an embedding space, and each learned fact is a constraint between points (distance, angle or relation). The system keeps computing the rigidity matrix of this framework. Its null space gives "floppy modes", directions in which a concept can move without breaking any known fact, so the concept is underdetermined. Each floppy mode creates a bracing latent variable or a targeted query along that direction. Each state of self-stress (constraints that are redundant and in conflict) splits the stressed concept into two nodes, so that each one meets a consistent subset of the constraints.
VALUE: The system can tell, from the geometry alone, exactly which parts of its knowledge are underdetermined or overconstrained, and it repairs each part structurally.

IDEA 2
NAME: Wahlund Splitting of Representations
MECHANISM: Each internal unit's discretized activation states are treated as alleles, and pairs of co-occurring contexts are treated as diploid genotypes. A running Hardy–Weinberg test compares how often mixed ("heterozygous") pairs actually occur with how often they would occur in one homogeneous population. A significant heterozygote deficit is the Wahlund signature that the unit merges hidden subpopulations. In that case the unit is split into typed children, and the F-statistics between those children decide the routing. Children that later come back into equilibrium with each other are merged again.
VALUE: The model breaks apart conflated concepts while it runs, using an online statistical test instead of an analysis done after the fact.

IDEA 3
NAME: Misclosure-Driven Context Charts
MECHANISM: Learned transformations (analogies, translations, coordinate maps) are composed around closed cycles, and each cycle's misclosure is recorded the way a surveyor records a traverse error. A Hodge decomposition of these residuals over the cycle complex leads to three repairs. The gradient part goes back into local map corrections. The curl part localizes and deletes or rewires the specific inconsistent edges. The harmonic part shows a real topological hole, and it creates a new context variable that divides the domain into separate charts with explicit transition maps.
VALUE: The system can find out that its knowledge needs several context-dependent frames, and build them, instead of averaging contradictory regularities into one incoherent map.