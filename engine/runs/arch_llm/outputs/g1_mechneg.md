**1. Mechanical confession** (objects | flow | rule | signal)
1. Frozen large matrices plus small trainable matrices | the two outputs are added | gradient step on the small ones | next-symbol error at high-error positions
2. Large RAM table of weight blocks plus a small selector | selected blocks are copied to the GPU | gradient step on the selected blocks | next-symbol error
3. Fixed-size running state vector | each symbol is mixed in with a learned decay | gradient | next-symbol error
4. Weights limited to {-1, 0, 1}, with float shadow copies | integer multiply-add | gradient on the shadows, then rounding | next-symbol error
5. One block applied k times | its output is fed back in, and a score decides when to stop | gradient | next-symbol error plus a step penalty
6. Masked or noised symbol sequence | the whole sequence is cleaned up repeatedly | gradient | reconstruction error
7. Byte stream with variable boundaries | boundaries go where a small predictor is unsure, and a large network works on the chunks | gradient | next-byte error
8. Text plus an external executor | emitted code runs and its results are inserted | gradient | next-symbol error on the traces
9. Index of corpus substrings | exact-match counts become inputs | gradient on what the counts miss | next-symbol error
10. Hashed table of stored intermediate vectors | a hit skips layers and a miss writes a new entry | table write plus gradient | next-symbol error and confidence
11. Indexed rows of a teacher model's weights | top-k rows are fetched per symbol | gradient | mismatch with the teacher's outputs
12. Logged episodes plus spare slots | logs are replayed during idle time | gradient with replay | next-symbol error or mismatch with a teacher

**2. Mechanical paradigm**
- **Quantities tracked:** dense real-valued vectors for each symbol.
- **Rule:** gradient descent, or cached writes, on a loss that can be differentiated.
- **Signal:** error at each position in predicting, reconstructing or imitating a corpus or a teacher.
- **Forbidden:** every change rule driven by prediction, reconstruction or imitation error. That also rules out the adjacent signals: compression or description length, contrastive matching, distillation, and reward computed on predictions.

**3. Also excluded:** the 12 listed answers and any re-skin of them.

**4. Mechanics fixed first**
- **A.** Objects: integer proposition triples, each with a truth bit. Flow: parse, then constraint propagation. Rule: stochastic flips that become less random over time. Signal: the count of violated logical constraints.
- **B.** Objects: text-rewrite operators. Flow: operators are composed. Rule: equivalence classes are merged and split. Signal: the composition of two operators does not equal any known operator.
- **C.** Objects: phase oscillators. Flow: coupled phase dynamics. Rule: coupling strength is changed by coherence. Signal: how stably the phases stay locked.

Each of A, B and C differs from every row on all four parts, and no two share a signal.

=== IDEAS ===
IDEA 1
NAME: Contradiction-Annealed Belief Lattice
MECHANISM: A frozen small open-weight model parses text into hashed (subject, relation, object) triples. Up to about 500M of these sit in the 32 GB of RAM as integers, each with a truth bit and a pressure counter. Logical constraints are encoded as sparse incidence matrices: transitivity, one value per functional relation, mutual exclusion and type rules. The GPU counts the violated constraints in parallel. A Metropolis process flips truth bits, and its randomness is lowered over time until the total number of violations is at a minimum. To answer a query, the system reads the settled bits and the frozen model writes them out as text. Nothing is learned by gradients, and the GPU work is only sparse integer counting.
VALUE: It keeps a globally consistent belief store with hundreds of millions of facts that reconciles conflicting sources, which a 200M-parameter network can neither hold nor make consistent.

IDEA 2
NAME: Closure-Merged Rewrite Algebra
MECHANISM: The stored objects are edit operators: span-level rewrite transforms taken from aligned sentence pairs, such as a tense change, a negation or swapping roles. They live in RAM as typed diffs. The GPU composes operator pairs in bulk and checks whether each result matches an existing operator class. Classes are kept in a union-find structure that merges, and splits when a merge breaks closure. Generation applies chains of operators to retrieved exemplar sentences.
VALUE: It gives exact compositional and analogical generalization, applying any combination of known transformations to any sentence, instead of the approximate interpolation a same-budget network learns.

IDEA 3
NAME: Phase-Locked Entity Binding
MECHANISM: Each entity and attribute mentioned in a long document gets a complex-valued oscillator, with up to millions of them in VRAM. Links found by a frozen small parser couple them. The GPU integrates the coupled phase equations, which is cheap elementwise work, so linked items fall into phase-locked clusters. Coupling strengths are raised or lowered according to how stably each cluster stays locked over time. To answer a question, the system reads which oscillators share a phase, for example who holds what or where something is.
VALUE: It tracks state and variable bindings across an unbounded document at linear cost, which is where a small fixed-context transformer breaks down.