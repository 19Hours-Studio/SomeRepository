HONESTY CHECK
1. Closest work: neural sheaf diffusion (Bodnar 2022) and ART vigilance. Those train restriction maps by gradient or cluster data points. Here the glue between patches is what nucleates, and it forms from contradiction loops.
2. Closest work: HodgeRank (Jiang 2011) and potential-based shaping (Ng 1999). HodgeRank decomposes a fixed set of comparisons. Here credit decides which holes survive. I dropped tracer flow because it falls in L3.
3. Closest work: Petri-net P-invariants and AI Poincaré. Those analyse given nets or continuous trajectories. Here integer invariants are learned online and prune the rewrite search. I dropped the MDL library (L1) and scale collapse (L3).

=== IDEAS ===
IDEA 1
NAME: Contradiction-Nucleated Gluing Maps
MECHANISM: Knowledge sits in local patches. Examples that land where overlapping patches disagree are grouped by the loop of overlaps around which agreement fails, and each group grows a candidate restriction map (a "twist") with member count n that decays faster as it shrinks. The loop's gluing obstruction acts as supersaturation S: a twist freezes into a permanent gluing rule once n exceeds n*(S), which falls steeply with S, and weak candidates dissolve. Frozen twists change which global sections exist, which lowers obstruction on neighbouring loops and suppresses redundant nucleation there.
DIFFERENCE: It learns a new relation between two already-stable bodies of knowledge from one sharp contradiction, without refitting either of them.

IDEA 2
NAME: Circulation-Credited Cell Complex
MECHANISM: Experienced transitions build a cell complex. Each edge holds a credit value, and every delayed outcome adds one linear constraint: the summed credit along that trajectory chain equals the outcome. Solving these sparse boundary-matrix systems splits credit into a gradient part (ordinary state value), a curl part (local noise) and a harmonic part (the net gain per winding around each hole). Holes with near-zero harmonic credit are filled with 2-cells, and holes with persistent non-zero circulation are kept as concepts, which are repeatable strategies.
DIFFERENCE: It represents and exploits cyclic, non-transitive gains (loops that pay off on every pass), which a scalar value function cannot express because it is a pure gradient with zero circulation.

IDEA 3
NAME: Learned Conservation-Law Type System
MECHANISM: Computation rewrites a typed graph of symbols with learned rules. Each symbol carries a small integer grade vector over k hidden bases, chosen with the smallest k first so that every observed rewrite conserves total grade. Grades act as types: any proposed rewrite or plan that changes total grade is rejected without being run, and a sparse table indexed by grade records which normal forms have been reached. When an observed rewrite breaks conservation, the system splits a grade or raises k, so the invariants are revised.
DIFFERENCE: It can certify that a goal is unreachable at any search depth, which gives provable negative knowledge that sampling-based models cannot produce.