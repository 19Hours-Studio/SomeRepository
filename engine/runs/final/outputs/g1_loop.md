Three diagnostic loops, each taken from a field far from AI:

1. Control engineering: controllability Gramian. Engineers check whether a plant's internal modes can be reached from its actuators. A mode with a near-zero Gramian eigenvalue is a hidden defect: the system has that state but the inputs can't drive it. Ported: treat the generator's latent dynamics as the plant and context/prompt embeddings as actuators. Directions the model represents (they show up in its activations) but can barely reach are concepts it "knows" and almost never says. Loop: create new permanent input channels aimed at those directions. Closest work: steering vectors and activation addition. Those steer toward concepts people already chose; here the reachability deficit picks the target, and the change adds architecture rather than nudging activations.

2. Crystallography: systematic absences. Reflections that are missing even though their intensity "should" be nonzero reveal hidden symmetry elements, the screw axes and glide planes. Ported: take a Fourier/co-activation transform over sparse-autoencoder features. Combinations whose parts are each frequent but which never co-occur expose selection rules the model absorbed from its corpus. Loop: find the circuit that enforces each rule, cut it and rewire it, then keep the cut only if outputs in the forbidden region pass verification. Closest work: concept erasure (LEACE) and SAE analysis. Those remove a known concept. This finds unknown prohibitions. It differs from CFWORLD because no world model is altered: the model's own learned bans are measured and deleted.

3. Structural mechanics: Maxwell counting and the rank of the rigidity matrix. These detect floppy mechanisms (under-constrained modes) and self-stress (redundant bars). Ported: build the Jacobian of the model's consistency constraints with respect to latent concept coordinates. Its null space holds the degrees of freedom the training data never pinned down, so outputs there are not recombinations of common patterns. Loop: explore along floppy modes, and when an output is verified, add a new constraint node (a "bar") that names the new concept. Delete constraints that carry self-stress. Closest work: underspecification and flat-minima research, which works in parameter space and only reports. This works in concept space and edits the graph.

=== IDEAS ===
IDEA 1
NAME: Gramian-Guided Actuator Growth
MECHANISM: Linearize the generator's latent dynamics around typical contexts and compute an empirical controllability Gramian with respect to the input embeddings. Eigendirections the model represents but can barely reach are flagged, and a new learned input channel (an adapter or token) is grown for each one. Channels whose outputs pass verification are kept, the Gramian is recomputed, and growth continues where reachability is still low.
VALUE: It surfaces concepts the model holds internally but structurally cannot express.

IDEA 2
NAME: Systematic-Absence Selection-Rule Breaking
MECHANISM: Measure co-activation statistics of sparse-autoencoder features and flag combinations whose marginals are frequent but whose joint occurrence is near zero, the way crystallographers flag systematic absences. Trace each one to the circuit that suppresses it, then cut or rewire that circuit. A rewiring is kept only if the newly reachable outputs pass external verification; failed cuts are restored and recorded as genuine laws.
VALUE: It turns hidden prohibitions absorbed from the corpus into removable structure, which opens regions the data never visited.

IDEA 3
NAME: Rigidity-Matrix Floppy-Mode Exploration
MECHANISM: Assemble the Jacobian of the model's consistency constraints over latent concept coordinates and compute its null space (floppy modes) and its left null space (self-stress). Generation moves along floppy modes. When an output is verified, a new constraint node pins that direction as a named concept; redundant self-stressed constraints are deleted.
VALUE: It generates in directions the training data never constrained, then turns the confirmed ones into permanent concepts the model can build on.