**1. Mechanical confession (objects | flow | rule | signal)**
1. State vectors | predicted next state is compared with the actual one | gradient step on weights | prediction mismatch
2. Key-value records | a query retrieves the nearest record | append when the input is novel | mismatch size
3. Weight matrices | co-active units | outer-product increment | co-activity
4. Nodes and edges | values propagate along edges | add, cut or flip an edge | mismatch
5. Short code strings | run to produce outputs | edit-and-search | mismatch plus length
6. Modules | a gate routes inputs to them | adjust the gate weights | scalar reward
7. Agent and world | action produces sensation | update the policy | mismatch or reward
8. Self-made tasks | attempt them | keep tasks whose error is falling | rate of error drop
9. Candidate answer | a checker scores it | refine and repeat | pass or fail
10. Per-region counters | look them up | update the counts | verified error
11. Variable assignments | relax iteratively | descend a cost | scalar cost
12. Looping state | iterate until a learned halt | adjust the halt | confidence

**2. Mechanical paradigm**
Every row tracks one internal model of an outside target. Each changes it by small adjustments driven by error (gradient, search or counts). Each one answers to a single number: how far its output is from what happened, or reward. Forbidden: any change driven by mismatch, reward, score, or anything adjacent to them (surprise, novelty, uncertainty, confidence, compression, verifier pass).

**3. Built outside the table**
- A: objects are derivation paths. They flow as background random walks over stored facts. The rule compiles a conclusion into a primitive. The signal is a count of independent paths, not whether the conclusion is right.
- B: objects are concentrations of species. They flow as rewrite reactions. The rule is dilution. The signal is each species' own production minus consumption.
- C: objects are a log of operations. They flow as trial reorderings. The rule splits or fuses operations. The signal is whether two operations commute, an algebraic fact rather than an outcome.

Each differs from all 12 rows on at least 3 of the 4 parts, and no two share a signal.

=== IDEAS ===
IDEA 1
NAME: Path-Multiplicity Primitive Compilation
MECHANISM: Background random walks keep re-deriving conclusions from stored facts along many different routes. A tally records how many independent routes reach each conclusion (routes sharing no intermediate fact count separately). When the tally passes a threshold, the conclusion is frozen into a new atomic primitive that later walks can use as one step. Primitives that are no longer reachable by several routes are dissolved back into their parts.
VALUE: It builds new concepts from how well a conclusion is held together by the rest of what it knows, with no outside feedback, so abstraction can grow in domains where nothing ever says "correct."

IDEA 2
NAME: Autocatalytic Concept Chemistry
MECHANISM: Knowledge is a pool of symbolic "species" at varying concentrations, plus rewrite reactions that consume some species and produce others. Each cycle, every species is diluted at a fixed rate. It survives only if the reactions it takes part in regenerate it. New reactions come from random recombination, and the set that persists is whatever forms closed, self-maintaining loops.
VALUE: Concepts are defined by the network of processes that keep producing them, which gives self-sustaining, open-ended structure without any objective.

IDEA 3
NAME: Commutation-Carved Modularity
MECHANISM: Each experience is logged as an ordered sequence of operations. A background process swaps neighbouring pairs and tests whether the resulting record is identical. Operations that always commute are split into separate parallel threads with no shared state. Operations that never commute are fused into one indivisible unit, so the system's architecture becomes a map of the world's independence structure.
VALUE: The system can split the world into independent parts and recombine them freely, which gives built-in compositional generalization.