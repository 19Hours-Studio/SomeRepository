**Offspring 1 (Pair 1).** Each random walker is also a bet. It starts with capital 1, and at every node it visits its capital is multiplied by the predictor's likelihood ratio for that node. When it touches the aggregate, it sticks with probability min(1, capital). So the evidence decides where the fractal grows, and the shape of the growth decides which bets get made. Wealth lets the system commit to an answer; geometry moves walkers toward territory that hasn't been screened yet.
*Honesty:* The closest existing work is anytime-valid best-arm identification, which needs a fixed, listed set of arms. This offspring has no such list, so I kept it.

**Offspring 2 (Pair 2).** Messages passed during consistency propagation carry one tracer coordinate per patch, mixed by normalized restriction-map weights. This is linear mixing, not a conserved flow. Where an overlap still disagrees, a small unmixing solve gives each patch's exact share of the disagreement, and that blame pattern decides the repair.
*Honesty:* The closest existing work is sheaf diffusion plus forward-mode sensitivities, or truth-maintenance systems. Those retract beliefs. I changed this offspring so the blame is used to create new variables instead.

**Offspring 3 (Pair 3).** I moved it away from scaling and dimensions (an L3 family). The integer vectors are now over learned "kinds" rather than physical units. When a concept forms, it becomes a new kind, and the type vectors limit which items a cluster will accept.
*Honesty:* The closest existing work is SUSTAIN combined with type inference. Type inference does not create new base types when it is surprised, so I kept it.

=== IDEAS ===
IDEA 1
NAME: Betting Diffusion-Limited Search
MECHANISM: Random walkers start from unexplored regions of a graph of candidates with capital 1 and multiply that capital by a learned predictor's likelihood ratio at each node they visit. A walker that touches the discovered aggregate attaches with probability min(1, capital), so growth happens at tips that both screen the most unexplored territory and have the most evidence. Each attached candidate keeps a product of returned capital as an e-process, and an answer is committed once that exceeds 1/α. Launch rates move toward the regions whose capital grows fastest.
DIFFERENCE: It searches an unbounded answer space that is never listed out, while keeping an error bound on its committed answers that holds under any stopping rule.

IDEA 2
NAME: Obstruction-Traced Variable Invention
MECHANISM: Thousands of local patch models are reconciled by consistency propagation, and every message carries one tracer coordinate per patch, mixed by normalized restriction-map weights. Where an overlap still disagrees, a small linear solve splits the tracers into each patch's exact share of the obstruction. If the blame is concentrated in one patch, that patch is refitted or split. If the blame is spread around a cycle of patches that are each consistent on their own, it is treated as a missing variable, and a new context coordinate is added to separate them.
DIFFERENCE: It can tell "one of my models is wrong" apart from "my description of the world is missing a variable," and it creates that variable; gradient-trained networks cannot tell the two apart.

IDEA 3
NAME: Surprise-Nucleated Type Algebra
MECHANISM: Every item carries a small integer vector over k learned base kinds. Only items with identical vectors can be compared or clustered, and composing items adds their vectors. Each example joins its nearest compatible cluster, clusters shed members faster as they shrink, and the example's surprise sets a supersaturation S. A cluster that reaches the critical size n*(S) freezes into a new base kind (k grows to k+1), and a discrete search then changes as few vector entries as possible so that every frozen relation still type-checks.
DIFFERENCE: It builds its own type system from a few surprising examples and then refuses generalizations that mix incompatible types, a hard constraint that statistical networks cannot enforce.