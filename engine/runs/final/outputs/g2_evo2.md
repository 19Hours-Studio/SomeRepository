**Pair 1.** In the offspring, the circuit-cutting parent supplies the steps of the step-by-step construction. Each step forces one frequent-but-never-joint SAE feature pair to fire together, which removes the circuit that normally blocks it. The construction parent's consistency prover then decides what happens to that circuit. If the prover refutes the step, the blocking circuit counts as carrying a real law and the pair is retired. If the step is accepted, the circuit counts as a corpus habit and is weakened permanently, which changes the concept clusters the construction escapes from next.
Closest work: Denial Prompting, and SAE steering for creativity. The difference is that the conditions are internal absences checked by a prover, and the prover's verdicts edit the model.

**Pair 2.** The offspring merges the two parents into one generalized eigenproblem. The search looks for latent directions v that keep the model's consistency rules satisfied (J_k v = 0) while maximizing the downstream payoff that known ideas cannot reproduce (‖P⊥ J_c v‖²). Each accepted idea adds a constraint row and a hedging vector at the same time. Constraints that are mutually redundant (self-stress) mark known ideas whose payoffs overlap, and those ideas are merged.
Closest work: novelty search over behaviour descriptors, DreamCoder, and Latent Constraints. None of them solves for directions that are both unconstrained and impossible to reproduce from known ideas.

**Pair 3.** In the offspring, the difference between how the ablated model and the intact model rank artifacts becomes a candidate evaluation axis. That axis then serves as the goal the ablated model rebuilds the domain toward.
Closest work: Unlearning-as-Ablation, model diffing with crosscoders, and From Weights to Words. None of them turns an ablation-induced preference into the objective for building a new foundation.

=== IDEAS ===
IDEA 1
NAME: Absence-Driven Generic Forcing
MECHANISM: The system builds a candidate one condition at a time. Each condition forces a systematically absent SAE feature pair to co-activate, gated for that candidate only, and must break the defining feature of a concept cluster the candidate has not yet escaped. A prover checks each condition against the earlier ones. A refutation records the suppressing circuit as a law and retires the pair; an accepted, verified candidate permanently weakens every suppressor it needed, after which concept clusters are recomputed and the order of the next forcing steps changes.
VALUE: It separates the corpus's real laws from its habits by trying to build consistent objects, and removes only the habits.

IDEA 2
NAME: Unhedgeable Floppy-Mode Eigensearch
MECHANISM: The system solves a generalized eigenproblem: maximize ‖P⊥ J_c v‖² subject to J_k v = 0. Here J_k is the Jacobian of the consistency constraints, J_c is the Jacobian from latent coordinates to downstream-task payoffs, and P⊥ projects out the span of known ideas' consequence vectors. Generation follows the top eigendirections. A verified idea adds a constraint row to J_k and a vector to the hedge span. Redundant constraints (left null space) identify known ideas with collinear payoffs, which are merged.
VALUE: It points generation straight at directions that are both left free by the data and impossible to reproduce from known ideas.

IDEA 3
NAME: Ablation-Born Values, Rebuilt Foundations
MECHANISM: The system unlearns concept C from a copy of the model. Both copies rank the same artifact corpus, and the difference between their rankings is distilled into a small learned axis. The axis is kept only if it is stable, learnable from a few examples, independent of a bank of human criteria, and not just a detector for mentions of C. The ablated copy then rebuilds the domain using that axis as its objective. The concepts it builds are kept as alternative foundations if, once put back into the intact model, they raise the axis scores of new artifacts. The next concept to ablate is the one whose predicted axis is most independent of the stored axes.
VALUE: It finds new kinds of "good" together with the alternative concepts that make them possible to pursue.