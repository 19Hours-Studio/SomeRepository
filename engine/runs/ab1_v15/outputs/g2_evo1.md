CROSSOVER NOTES
- Pair 1: In Parent A, each claim is checked along more than one route, and the w-test points to the step that broke. Parent B's Hodge split decides whether that broken step is a real mistake or a sign that two frames are needed. In return, A's redundancy numbers and minimal detectable bias decide where B should test whether a gap in its map is real.
- Pair 2: A balanced ledger has the same form as a self-stress in a rigid framework: the transfers into each holder sum to zero. So the bookkeeping and the rigidity analysis can share one matrix.
- Pair 3: Members of the ensemble act as the separate re-encodings used at each proofreading stage. The proofreading result then sets how much weight the Kalman update gives the fact.

HONESTY CHECK
- Offspring 1: The closest existing work is sheaf cohomology and Hodge-based ranking, combined with Baarda reliability theory. What it adds is a test the system runs itself: it builds new derivations that close a suspected gap, and that tells a real gap apart from a mistake.
- Offspring 2: The closest existing work is Petri-net place invariants, which find conserved quantities from the null space of an incidence matrix. What it adds is that the holders are learned points in an embedding. Conserved quantities are found online as stresses, and imbalances that won't go away are used to place hidden holders.
- Offspring 3: The closest existing work is quality control in operational data assimilation, such as gross-error and buddy checks. What it adds is several rejection stages that cannot be undone, spaced out in time while other facts are absorbed. The number of stages grows with how much of the model the fact's update would reach.

FIRST THOUGHTS:
- Hodge-weighted least-squares adjustment of reasoning loops
- Conservation laws added as constraints in a rigidity matrix
- Majority voting over the ensemble before each Kalman update
- A graph neural network that predicts misclosures
- An ensemble Kalman filter whose observations are reasoning steps

=== IDEAS ===
IDEA 1
NAME: Hole-Filling Derivation Probes
MECHANISM: Claims are nodes, and derivations are edges that carry transformations; whatever error is left after going round a loop is that loop's misclosure. When the Hodge split finds a harmonic residual, the system doesn't accept it as a real gap straight away. First it builds bridging derivations across the gap, choosing them with Baarda's minimal-detectable-bias so that each new derivation best tells the possible explanations apart. If the new pieces bring the error back to zero, it was a mistake, and the w-test finds the bad step. If the error survives every bridge, the system creates a new context variable that splits the claims into separate frames.
VALUE: The system can tell a mistake in its own reasoning apart from a real need for separate frames, and it finds out by running its own test.

IDEA 2
NAME: Stress-Space Bookkeeping
MECHANISM: Holders are learned points, and each transfer is a bar between two of them. A balanced set of transfers is an equilibrium stress, so a quantity counts as conserved only while its transfers stay in that stress space. An imbalance that won't go away is treated as a load on the framework. The system adds a hidden holder at the position where the loose directions (floppy modes) can absorb that load. Where stresses conflict, the holder splits in two.
VALUE: The system can keep exact track of world state, and the geometry shows where unknown participants must be and which quantities are not really conserved.

IDEA 3
NAME: Delayed Proofreading Assimilation
MECHANISM: A new fact first goes into a queue. At each stage it is checked against a different, separate subset of the roughly 64 ensemble members, and only after other facts have been absorbed in between. Agreement between those members gives the fact's binding margin, and a fact rejected at any stage is gone for good. The number of stages grows with how much of the model the update would change. Facts that pass more stages get smaller observation noise, so the update counts them more.
VALUE: The system can keep learning from a stream of new facts, and wrong facts that would cause broad damage are stopped before they get in.