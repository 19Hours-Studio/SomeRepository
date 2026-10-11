Most generative AI samples from where its training data is densest, so its outputs are recombinations of what is common. A really new idea comes from somewhere the data never went. All three mechanisms below change what generation optimizes or where it gets its material. None depend on how the model is prompted.

**1. Foreign-axiom worlds.** The system builds many internal world models. In each one, a few causal links or invariants from its main world model are deliberately inverted or deleted, for example "information is conserved" or "the cost grows with size." It reasons inside these worlds until it finds structures that are internally consistent there, such as strategies, designs or theorems. It then brings them back and checks them against the real verifier, meaning a simulator, a proof checker or an experiment. Whatever survives started from premises nobody in the corpus held, so it cannot be an interpolation of the corpus.

**2. Compression-driven discovery.** The system stores its knowledge as a library of executable abstractions rather than as weights alone. An "idea" is a new primitive that shortens the total description length of many unrelated parts of that library at once. A search runs continuously, proposing primitives and refactoring the library around them. A primitive is kept only if the compression gain carries over to new observations. Because the primitive is chosen for how much it shortens the library, and not for how familiar it looks, the system lands on concepts that unify things no training example linked together.

**3. Self-anticipation adversary.** A second network is trained online to predict the generator's next idea, given the corpus and the generator's own history. The generator is rewarded only for outputs that both surprise this predictor and pass validity checks. The predictor keeps learning, so any pattern the generator falls into soon becomes predictable and stops earning reward. That pressure keeps pushing the generator out of its own habits and the corpus's habits, while the verifier stops it from drifting into nonsense.

=== IDEAS ===
IDEA 1
NAME: Foreign-Axiom World Forking
MECHANISM: The system clones its learned world model and, in each clone, inverts or deletes selected causal edges or invariants. Inside each altered world it searches for structures that are internally consistent there. Candidates are mapped back and checked against real verifiers. A bandit learns which kinds of axiom change produce ideas that survive, and those changes are stored and reused.
VALUE: It produces ideas that start from premises absent from the training data, not from blends of common patterns.

IDEA 2
NAME: Compression-Driven Concept Invention
MECHANISM: Knowledge is kept as a library of executable abstractions. A search proposes new primitives and keeps only those that cut the total description length across many unrelated parts of the library, and the gain must hold on new observations. Each accepted primitive triggers a refactor of the library, which changes where the next search for gains happens.
VALUE: It finds unifying concepts that link domains no training example ever connected.

IDEA 3
NAME: Self-Anticipation Adversarial Generation
MECHANISM: A predictor network is trained continuously to forecast the generator's outputs from the corpus and the generator's own history. The generator is rewarded for outputs that are both unpredictable to this predictor and accepted by a validity verifier. The predictor's updates are stored and accumulate, so patterns the generator falls into quickly stop earning reward.
VALUE: It builds steady, self-renewing pressure away from both corpus clichés and the system's own habits, without giving up correctness.