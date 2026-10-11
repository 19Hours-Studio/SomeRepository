Today's LLMs share three structural limits. Their weights freeze after training. They can't test hypotheses by intervening on the world. And they can't revise a belief and pass the change through everything that depends on it. Each proposal below replaces one of those limits with a new mechanism instead of patching a transformer.

**1. Causal programs refined by experiment.** Knowledge is stored as a library of small causal programs that can be run, not as statistical correlations in weights. The system picks interventions to separate competing programs, so it learns by asking "what if I do X" rather than by predicting the next token.

**2. A belief ledger that maintains itself.** Every claim the system holds is an explicit node that records where it came from and what it depends on. A contradiction triggers dependency-directed retraction, which gives memory that can be updated, audited and never silently overwritten.

**3. Thinking as a compute market.** Specialist modules bid for a shared, limited compute budget, priced by how much uncertainty their output is expected to remove. Deliberation therefore grows and shrinks with how hard a problem actually is, and the modules can be learned and swapped while the system is running.

=== IDEAS ===
IDEA 1
NAME: Experimenting Causal Program Library
MECHANISM: The system keeps a growing library of small probabilistic programs, each encoding a candidate causal mechanism (e.g., "pressure causes leak if seal is worn"). When several programs explain the observations equally well, it computes which intervention (real action, simulator query or tool call) would best tell them apart, runs it, and reweights or deletes programs based on the result. New programs are synthesized by recombining fragments of programs that survived, so the library compresses over time.
VALUE: It can discover and reliably use real cause-and-effect structure, including in situations that never appeared in its data.

IDEA 2
NAME: Self-Revising Provenance Belief Ledger
MECHANISM: Every assertion the system adopts becomes a node in a persistent graph that stores its source, confidence and the nodes it was derived from. On each inference step a constraint checker scans for contradictions. Conflicts are resolved by retracting the least-supported justification, and the retraction automatically propagates to all dependent conclusions (truth maintenance). Generation is restricted to drawing on the active ledger and has to cite node IDs.
VALUE: It enables lifelong learning without catastrophic forgetting, with traceable reasoning and instant correction of any fact and everything derived from it.

IDEA 3
NAME: Information-Priced Compute Market
MECHANISM: Many heterogeneous modules (search, simulation, symbolic solvers, small neural nets) bid for slices of a shared compute budget. A bid is priced by the expected reduction in task uncertainty, and the payout is the realized reduction. Modules that bid well gain budget and get copied with mutations, while chronically bad bidders are retired. The architecture is therefore an evolving economy rather than a fixed graph.
VALUE: It makes possible adaptive, open-ended allocation of reasoning effort and self-directed architectural growth after deployment.