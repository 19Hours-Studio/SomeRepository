Goals: reliable reasoning, learning from little data, open-ended discovery.

Shared paradigm, banned as mechanism: a fixed differentiable function tuned by gradient descent on one global loss over static data.

No idea uses A through H as its mechanism. Closest existing work: Idea 1 is provenance-tracked generation and stratified logic programs; Idea 2 is surprise-gated memory writes and nonparametric clustering; Idea 3 is frontier and count-based exploration. Each differs in its core update rule.

=== IDEAS ===
IDEA 1
NAME: Stratigraphic belief column
MECHANISM: Each belief is a layer deposited into one append-only column, placed above the layers it rests on, so its depth is one more than its deepest support. Support chains therefore end at observations, and self-support cannot be written. A contradiction is logged as a dated intrusion that cuts an older layer without erasing it, and a conclusion is emitted only if no unresolved intrusion lies on its support chain; resolving one means depositing a new layer that rests on both sides.
DIFFERENCE: Circular justification is impossible by construction, and every conclusion carries full provenance to observations, which a single forward pass re-deriving its own support cannot guarantee.

IDEA 2
NAME: Surprise-triggered concept nucleation
MECHANISM: The state is a set of proto-concepts, clusters of past examples each with a member count n. Each example joins its nearest cluster or seeds a new one, and every cluster loses members at a rate that rises as it shrinks. The example's surprise, meaning how badly existing clusters predicted it, sets a supersaturation S; a cluster reaching a critical size n*, which falls steeply as S rises, freezes into a stable concept, while smaller clusters dissolve.
DIFFERENCE: A single highly surprising example can fix a concept, while unsurprising noise fades rather than accumulating, so the data needed is set by surprise rather than by a fixed learning rate.

IDEA 3
NAME: Harmonic-measure frontier growth
MECHANISM: The state is an aggregate of discovered items on a graph of candidate items. Random walkers launched from unexplored territory step between neighbors until they touch the aggregate and attach, adding one item and exposing new frontier. Growth concentrates at tips that screen the most unexplored territory, since walkers reach them first, so the aggregate branches fractally over the reachable space. Launch and attachment rules adapt to the yield of new items per walker.
DIFFERENCE: It covers an unbounded space in proportion to the unexplored territory each frontier point screens, with no value function or novelty score, which current exploration bonuses must learn.