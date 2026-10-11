Brief offspring notes:

Pair 1: The residual register (B) sets each step's variance in the adjustment (A). In the other direction, the loop structure (A) decides which residual bits count as "explained": a residual from one route that a parallel route can rebuild backward counts as derived, not invented. Misclosure is measured in bits, not numbers.
Honesty: The closest existing work is self-consistency voting, cycle-consistency losses and Baarda reliability. None of these measures loop closure as information that two routes fail to reconstruct for each other, and none uses that measure to decide where to add redundancy.

Pair 2: Reconstruction gaps from the invertible net (B) are computed between pairs of premise contexts and treated as edge flows. A Hodge decomposition of those flows (A) separates two kinds of gap. A gradient part is a consistent missing premise. A curl part is an equivocation, where one term changes meaning around a cycle of contexts. Each split adds a context coordinate as a premise slot for the backward pass.
Honesty: The closest existing work is HodgeRank and reverse-thinking verification. HodgeRank ranks preferences and does not diagnose reasoning. Reverse verification cannot tell a hidden assumption from an equivocation. This offspring is distinct from both.

Pair 3: Teachability (A) defines the order of the merge lattice (B) instead of a fixed CRDT order. Merges that fail the test (B) produce candidate abstractions for teaching (A).
Honesty: The closest existing work is MELD/CRDT merging, DreamCoder library learning and federated distillation. All of these use a fixed merge order or a fixed similarity measure. None derives the order from a cross-architecture transmission test.

=== IDEAS ===
IDEA 1
NAME: Cross-Route Residual Closure
MECHANISM: Each key quantity is derived by two or more reversible routes, and each route writes the bits it cannot reverse into a residual register. Each route's residual is fed into the backward pass of the other routes. Bits that no route can rebuild form the loop's misclosure, and that misclosure is measured in bits. A Baarda-style test, weighted by each step's residual size, flags the single step that is invented rather than derived. The planner then adds new independent routes where residual bits cannot be cross-checked by any other route.
VALUE: A long chain can find exactly which step introduced unsupported content and can build itself to be checkable.

IDEA 2
NAME: Equivocation Curl Detector
MECHANISM: An invertible reasoner reconstructs its inputs from the answer under many premise subsets, and the reconstruction gap between each pair of subsets is stored as a flow on a graph. A Hodge decomposition splits these flows. The gradient part is surfaced as one explicit missing assumption. The curl part marks a term whose meaning shifts around the cycle, so that concept is split along a new latent context axis. The new axis becomes a premise slot that the next backward pass must fill.
VALUE: The system can tell an argument that rests on an unstated assumption from one that quietly changes what a word means.

IDEA 3
NAME: Teachability-Ordered Knowledge Lattice
MECHANISM: Each deployed copy stores concepts as short messages. One message ranks above another if a fresh learner with a different architecture, taught only that message, passes all of the other message's held-out tasks. A join is the shortest message that teaches both, found by compressing them together. When no such message is found, the two are kept as tombstone-safe sibling branches with grow-only evidence counters. Counter growth triggers retesting against a refreshed pool of naive learners, and a branch that no longer teaches is retracted by a tombstone.
VALUE: Millions of copies can pool what they learned into shared abstractions that stay explainable, and they never blend incompatible ones.