**The 12 I would propose first (and most researchers would too):**
1. State-space and linear recurrent models (Mamba, RWKV)
2. Sparse mixture-of-experts
3. Retrieval-augmented external memory
4. Differentiable neural memory (NTM-style)
5. Discrete diffusion language models
6. Joint-embedding predictive world models
7. Neurosymbolic program synthesis and tool use
8. Test-time search and extended reasoning
9. Fast weights and test-time training
10. Energy-based models
11. Spiking and neuromorphic networks
12. Byte-level hierarchical models

**Forbidden region:** neural function approximators over real vectors or tensors, trained by gradients or local rules, plus any of the 12 and their recombinations.

**Outside it:** a statistical controller, a non-real algebra, and a conservation-constrained dynamical system. All three are untested sketches.

=== IDEAS ===

IDEA 1
NAME: Anytime-valid betting reasoner
MECHANISM: The state is a wealth vector of e-processes, one per candidate answer. Each new observation multiplies each candidate's wealth by a likelihood ratio from a learned predictor, and compute is spent on the fastest-growing bets. An answer is committed when its wealth exceeds 1/α, and that error bound holds under any stopping rule.
DIFFERENCE: It bounds the error of committed answers at any stopping time, which confidence scores and self-consistency voting cannot guarantee.

IDEA 2
NAME: Min-plus derivation lattice
MECHANISM: Knowledge is a weighted directed graph with learned edge costs, and inference is tropical (min-plus) relaxation: each conclusion's cost is the minimum over derivations of summed edge costs, with no softmax or matrix multiply. Learning is perceptron-style and updates only the edges on the argmin derivation, so credit is exact rather than gradient-approximated. Missing derivations trigger new edges.
DIFFERENCE: Every output carries an exact, globally optimal derivation and exact sensitivity to each premise, which approximate networks can only explain post hoc.

IDEA 3
NAME: Conserved-budget stoichiometric machine
MECHANISM: The state is a nonnegative vector of species counts, and computation is a set of learned reactions with mass-action rates. Each reaction's stoichiometry must satisfy a fixed conservation law, so designated totals (resources, evidence, probability mass) move between species but are never created or destroyed. Learning tunes rates and reaction sets within those constraints.
DIFFERENCE: It guarantees by construction that multi-step computation cannot invent budget, evidence, or probability mass, which approximators can only approximate.