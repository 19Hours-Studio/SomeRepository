Most generative models score their outputs by how likely those outputs are under the training data. That pulls them toward the middle of what they have already seen, so they recombine common ideas. Originality needs a different target: build structure that the data does not already contain, then check it against something other than whether it looks familiar. All three proposals below swap "be probable" for a different internal pressure.

1. Contradiction-driven concept invention. The system keeps a model of its own beliefs and actively looks for spots where it can't explain its own predictions (two confident subsystems disagree, or no compressed explanation fits). It then grows new latent variables whose only job is to resolve those contradictions. A new concept counts as an invention, not a recombination, when it explains the conflict better than any concept it already has.

2. Self-modifying representational substrate. The system doesn't search inside one fixed embedding space. It runs a meta-process that changes the space itself: it adds dimensions, changes what counts as near, or redefines the basic building blocks. Ideas that were far away or impossible to express in the old space become simple in the new one. That matches how paradigm shifts actually happen.

3. Grounded counterfactual world-forking. The system branches internal simulations of worlds whose basic rules differ slightly from the training distribution. It develops ideas inside those worlds and brings back only what still holds when tested in reality. Because the idea came from somewhere the data never covered, it can't be a remix of common patterns. Reality acts as a filter, so it isn't just made up either.

=== IDEAS ===
IDEA 1
NAME: Contradiction-Driven Concept Invention
MECHANISM: Two or more independently trained predictive modules watch each other, and the system records places where they disagree or where its own predictions are internally inconsistent. Each recorded spot opens a "concept slot": a new latent variable is trained only to resolve that conflict, under a strong pressure to describe it compactly (minimum description length). A slot is kept only if it lowers inconsistency across many other conflicts, and kept slots become reusable building blocks for later reasoning.
VALUE: It creates new abstractions out of the system's own explanatory gaps rather than out of patterns that are common in the data.

IDEA 2
NAME: Self-Rewriting Representation Space
MECHANISM: A meta-learner proposes changes to the base representation: new primitives, a new distance measure, or new ways to combine elements. It scores each change by how much it shortens descriptions of hard, previously unexplained phenomena. Accepted changes are stored as versioned "lenses," and generation runs inside the newest lens, so ideas that were very improbable before become short and easy to produce.
VALUE: It allows paradigm shifts, meaning new ways of framing a problem, instead of new points inside an old frame.

IDEA 3
NAME: Counterfactual World-Fork Distillation
MECHANISM: A learned world model is copied into many variants, each with a basic rule changed or removed (for example, a different conservation law, causal ordering or incentive structure). Agents optimize inside each variant and find strategies or structures that are native to it. A transfer test then keeps only the artifacts that still work when moved back into the real-world model and checked against real data, and those are added to a growing library.
VALUE: It produces solutions that come from regions the training data never covered, while reality testing keeps them valid.