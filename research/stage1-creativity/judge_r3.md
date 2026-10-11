SCORES
Z01 | 3 | 6 | 6 | N | online genetic programming, Solomonoff-style mixtures
Z02 | 3 | 6 | 4 | Y | justification truth maintenance systems (Doyle/de Kleer)
Z03 | 5 | 4 | 3 | N | persistent homology, simplicial complexes (TDA)
Z04 | 5 | 6 | 4 | N | forward-mode sensitivities/RTRL, tracer hydrology
Z05 | 5 | 6 | 3 | N | ART / novelty-gated online clustering
Z06 | 3 | 8 | 4 | Y | coupled learning in physical flow networks
Z07 | 3 | 6 | 7 | N | DreamCoder + term/graph rewriting
Z08 | 3 | 4 | 6 | N | SILO LM, SISA unlearning, kNN-LM
Z09 | 3 | 8 | 3 | Y | rigidity-theory matrix completion (Singer-Cucuringu)
Z10 | 3 | 6 | 3 | Y | replicator dynamics / SMC resampling
Z11 | 2 | 7 | 4 | Y | Baum's Hayek machine, bucket brigade
Z12 | 4 | 7 | 5 | N | e-processes, testing by betting
Z13 | 6 | 3 | 4 | N | renormalization group, operator product expansion
Z14 | 3 | 4 | 5 | N | neural developmental programs, cellular encoding
Z15 | 3 | 7 | 4 | Y | case-based reasoning, case-difference adaptation
Z16 | 5 | 6 | 4 | N | Buckingham Pi learning, AI Feynman
Z17 | 3 | 6 | 3 | Y | EPAM discrimination nets, decision lists
Z18 | 6 | 6 | 3 | N | diffusion-limited aggregation, frontier exploration
Z19 | 3 | 7 | 4 | Y | iterated learning (Kirby; Ren et al.)
Z20 | 3 | 3 | 4 | N | reaction-diffusion computing, growing NCA
Z21 | 5 | 6 | 4 | N | max-flow/min-cut evidence, argumentation semantics
Z22 | 2 | 5 | 5 | Y | Voyager skill library, DreamCoder
Z23 | 1 | 7 | 6 | Y | complementary learning systems, episodic replay
Z24 | 5 | 4 | 5 | N | sheaf neural networks, local experts
Z25 | 2 | 5 | 3 | Y | conservative chemical reaction networks, Petri nets
Z26 | 1 | 7 | 6 | Y | active Bayesian causal discovery (Tong-Koller)
Z27 | 3 | 6 | 3 | Y | Physarum adaptive flow networks
FAMILIES
conserved-flow substrates (computation as conserved flow; provenance/no-creation guarantees): Z04, Z06, Z21, Z25, Z27
credit-economy populations (fixed/earned budget, split on success, delete on failure): Z01, Z10, Z11
program libraries / symbolic rewriting with MDL or verification: Z07, Z22
append-only provenance stores (knowledge as separable, traceable entries): Z02, Z08
morphogenetic growth substrates (local rules grow compute, self-repair): Z14, Z20
scaling-based variable discovery (invariance under rescaling creates variables): Z13, Z16
topological knowledge (homology): Z03
sheaf-glued local models: Z24
nucleation concept formation: Z05
rigidity-based abstention: Z09
anytime-valid answer commitment: Z12
case-difference edit chaining: Z15
confusion-driven probe lists: Z17
DLA exploration: Z18
iterated-learning bottleneck: Z19
fast/slow memory consolidation: Z23
active causal model search: Z26
TOP3:
Z07: the highest-value bet. Input-dependent depth and checkable intermediate steps target length generalization directly, and it can be tested on arithmetic and ARC right away.
Z12: cheap and concrete. It gives a real anytime error guarantee for when an LLM or agent commits to an answer, which current confidence and voting heuristics lack.
Z24: measured gluing obstructions give one mechanism for both locating self-contradiction and localizing continual-learning updates. Of all the ideas, it pairs moderate novelty and real value best.
NOTE: More than half the set takes a physics, chemistry or biology metaphor (fluid, reactions, nucleation, DLA, RG, morphogenesis) and pairs it with a "guaranteed by construction" claim (conservation, provenance, abstention). Five of the ideas are re-skins of the same conserved-flow idea. The most valuable ideas (Z07, Z23, Z26, Z08) are also the least original, mostly known methods under new descriptions.