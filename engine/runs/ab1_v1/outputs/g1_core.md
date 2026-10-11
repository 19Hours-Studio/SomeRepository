**1. The three goals**
- G1: Learning continually from experience after deployment, with many copies learning in parallel, without the new learning interfering with the old.
- G2: Reasoning reliably over long horizons, which means finding and fixing the faulty step instead of letting errors compound.
- G3: Knowing what it has not yet considered, so it can estimate unseen possibilities and decide when to stop searching.

**2. The shared paradigm**
Mainstream approaches put knowledge, reasoning and confidence implicitly inside one gradient-trained network's shared weights and its forward passes. That is forbidden here as the mechanism.

**3. Mechanisms borrowed from distant fields**
- G1 from distributed databases: CRDTs (conflict-free replicated data types). Their state is a join-semilattice, and merging two copies is commutative, associative and idempotent.
- G2 from geodesy: least-squares network adjustment combined with Baarda's data snooping. This finds a blunder in a land survey from the misclosure of redundant loops.
- G3 from ecology and Bletchley codebreaking: species-richness estimators such as Good–Turing and Chao1. They estimate unseen mass from how often items were seen once (singletons) and twice (doubletons).

**4. Honesty check**
- G1: The closest work is model merging and federated averaging (TIES, FedAvg). Those methods average weights, so they are lossy and depend on order. Lattice joins are exact and independent of order, so this is kept.
- G2: The closest work is self-consistency voting and process reward models. Voting picks an answer but does not locate the faulty step, while network adjustment does. TMS retracts conclusions by logic, not by statistical residuals. Kept. An earlier candidate based on kinetic proofreading came out as essentially repeated verification, so it was discarded.
- G3: The closest work is semantic entropy (Farquhar 2024). Semantic entropy measures how spread out the sampled answers are, not how much remains unseen. Kept.

=== IDEAS ===
IDEA 1
NAME: Lattice-Merged Knowledge Replicas
MECHANISM: Knowledge is stored as many small content-addressed entries rather than shared weights. Each entry holds monotone state: grow-only evidence counters, last-writer-wins registers with vector clocks, and sets of exceptions that support adding and removing. Each deployed copy updates its own replica from its own experience, and replicas combine through the lattice join, so merges never conflict and never depend on order. Retractions are tombstones, and prediction reads the joined state.
VALUE: Millions of copies can learn from separate experiences and pool what they learned exactly, with no catastrophic interference.

IDEA 2
NAME: Survey-Adjusted Reasoning Networks
MECHANISM: Each reasoning step is treated as a survey observation with a variance. The planner deliberately builds redundancy by deriving key quantities along independent routes so the steps form closed loops. Least-squares adjustment spreads each loop's misclosure across the steps, and Baarda's w-test flags the step with the largest standardized residual. Only that step is re-derived, and the planner adds redundancy where the redundancy numbers show steps that cannot be checked.
VALUE: Long chains locate their own blunders and design themselves to be checkable, so errors do not silently compound.

IDEA 3
NAME: Unseen-Mass Coverage Estimator
MECHANISM: For each query, the system draws several decorrelated derivations, each with a different decomposition, persona, or retrieval seed. It clusters the considerations, candidate answers and counterexamples they produce, then computes Chao1 and Good–Turing estimates from the singleton and doubleton counts. The result is an estimate of the probability mass of relevant items it has not yet seen. Search continues until estimated coverage passes a target, and the output reports that remaining unseen mass.
VALUE: It gives the system a quantitative sense of how much it has not yet considered, which tells it when to stop searching and when to flag an answer as incomplete.