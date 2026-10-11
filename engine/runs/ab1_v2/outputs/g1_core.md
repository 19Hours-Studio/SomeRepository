**1. Goals (the three that matter most):** (a) learning continually from a handful of experiences without retraining and without forgetting; (b) reliable multi-step inference whose error rate the system can drive down by spending more compute; (c) systematic generalization to new scales and combinations far outside the training distribution.

**2. Paradigm negated:** Mainstream approaches share one fixed-weight differentiable function. It is fit by gradient descent to a static corpus and answers in one learned forward pass per token. This is forbidden as the mechanism.

**3. Forbidden families:** I avoided all 13 listed families, including recombinations of them.

**4. Ported mechanisms:**
- **For (a), from tracing JIT compilers (PyPy, LuaJIT).** These solved the problem of being fast on hot paths while staying correct everywhere. They record a hot execution trace and compile it with explicit guards. When a guard fails, they fall back to the interpreter, and an exit that keeps failing gets its own compiled trace.
- **For (b), from molecular biology: kinetic proofreading (Hopfield, 1974).** Spending energy on irreversible, delayed checking stages multiplies the discrimination accuracy, so errors fall as f^K.
- **For (c), from engineering similarity theory (the Buckingham Pi theorem).** Wind-tunnel results transfer to full-size aircraft because laws are written over dimensionless groups.

**5. Honesty check:**
- Idea 1: the closest work is SOAR chunking and Voyager-style skill libraries. What is new here is the guard and deoptimization semantics and the counting of failing side exits. Kept.
- Idea 2: the closest work is verifier cascades and self-consistency voting. What is new is that a failure resets the candidate to the start, and that error falls geometrically as stages are added. Kept, but this is the weakest of the three on novelty.
- Idea 3: the closest work is AI Feynman and units-aware neural networks, which take units as given for physics. Here the "dimensions" are latent type exponents learned in any domain. Kept.

=== IDEAS ===
IDEA 1
NAME: Guarded Trace Compilation of Skills
MECHANISM: A slow, general deliberative solver handles new problems and records the step trace it executes. When a trace becomes hot, it is compiled into a fast specialized routine with explicit guard predicates, which are the input conditions the trace assumed. At runtime, a failed guard falls back to the solver and increments a counter on that exit. An exit that keeps failing is compiled into its own child trace, so the trace tree grows and existing traces are never overwritten.
VALUE: The system gains new skills from a few experiences, with no gradient retraining and no forgetting, because old traces stay intact behind their guards.

IDEA 2
NAME: Kinetic Proofreading Inference
MECHANISM: A candidate inference step must survive K sequential, irreversible holding stages before it is committed. At each stage it is re-tested for match against an independently perturbed context, and if it detaches it resets to the beginning rather than to the previous stage. Errors therefore decay roughly as f^K. The number of stages a candidate survives gives a confidence score, and the system can raise K wherever stakes are high.
VALUE: Reasoning accuracy can be bought with compute in a predictable, near-exponential way, instead of being capped by a single forward pass.

IDEA 3
NAME: Learned Dimensional Similarity Algebra
MECHANISM: Every latent quantity carries a learned vector of integer "dimension" exponents. These are inferred so that every observed relation is dimensionally homogeneous, by keeping the dimension matrix's integer nullspace consistent across relations. Learned laws are stored only as functions of the dimensionless groups the Pi theorem derives from that matrix. When no consistent assignment exists, the system takes it as a sign of a missing hidden quantity and introduces one.
VALUE: A relation learned in one regime transfers exactly to unseen scales and configurations that share the same dimensionless groups.