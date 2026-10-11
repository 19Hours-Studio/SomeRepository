**1. Goals**
- G1: Make candidates that fall outside the span of the model's learned concepts, not just in their low-probability tails.
- G2: Judge the value of an idea that has no precedent to compare it against.
- G3: Keep a new concept alive. Further training pulls rare concepts back toward the majority patterns in the data.

**2. Paradigm negated**
Mainstream approaches sample from a distribution fitted to past data and then filter or select what comes out. That is forbidden here as a mechanism.

**3. Periphery ports**
- G1, from set theory (Cohen forcing and diagonalization). A generic object is built from finite, compatible conditions. Each step must meet one dense set listed from the ground model, so the result provably differs from every object the ground model can define.
- G2, from finance (no-arbitrage replication). A derivative that has never traded is priced by building a portfolio of traded assets that replicates its payoffs. What cannot be replicated is the part that is genuinely new.
- G3, from epigenetics (read-write chromatin marks). Histone marks recruit enzymes that write the same mark on neighbouring sites. This bistable positive feedback, bounded by insulator elements, keeps a cell state alive through divisions without changing the DNA.

**4. Honesty check**
- G1: The closest work is novelty search and ANTIPRED. Both reward improbability. Forcing instead constructs the candidate step by step and guarantees it leaves the span, with no reward signal involved.
- G2: The closest work is Data Shapley and marginal-contribution valuation. Those split credit among existing items. This port measures the residual a candidate's consequences have outside the span of known ideas.
- G3: The closest work is EWC and context-dependent gating. Those apply fixed importance penalties. This port uses a self-spreading bistable mark with boundaries, which is a different mechanism.

=== IDEAS ===
IDEA 1
NAME: Forcing-Style Diagonal Construction
MECHANISM: The system lists its existing concepts as dense sets, i.e. clusters in representation space, each with a defining feature. It builds a candidate by adding finite conditions one at a time. Each condition has to break at least one listed concept's defining feature while staying logically compatible with every condition added so far, which a solver or prover checks. The conditions are stored as a growing partial object, and the listing order adapts to which concepts the candidate has not yet escaped.
VALUE: It produces consistent ideas that are guaranteed to lie outside the span of everything the model can name.

IDEA 2
NAME: Replication-Residual Idea Pricing
MECHANISM: Each candidate is put to use, as a lemma, tool or design rule, across a battery of downstream tasks, which gives a consequence vector. A minimum-cost regression projects that vector onto the stored consequence vectors of known ideas, playing the role of the replicating portfolio. The idea's value is the payoff in the residual that known ideas cannot hedge, and the library of consequence vectors grows as candidates are accepted.
VALUE: It can value ideas that have no precedent by what they make possible that nothing known can reproduce, rather than by how plausible they look.

IDEA 3
NAME: Self-Propagating Concept Marks
MECHANISM: An accepted concept gets a learned gating mark on the weights or latent region that carries it. Whenever that region is active, a read-write rule copies the mark onto co-active neighbours, and boundary units stop the spread. Marked parameters resist gradient pull toward the majority distribution, and because the dynamics are bistable a mark either takes hold or disappears.
VALUE: Rare new concepts survive further training and can be built on, instead of being averaged back into the common patterns.