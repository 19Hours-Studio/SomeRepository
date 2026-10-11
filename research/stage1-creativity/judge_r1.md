SCORES
X01 | 4 | 5 | Hayek machine / classifier-system auctions
X02 | 3 | 8 | Hypernetwork-generated LoRA from context
X03 | 3 | 3 | Fast weights, differentiable plasticity, Titans
X04 | 2 | 7 | Complementary learning systems with replay
X05 | 6 | 5 | Merkle-chained memory plus repetition penalties
X06 | 3 | 7 | Voyager/DreamCoder skill library with tests
X07 | 4 | 5 | Bayesian experimental design, curiosity-driven learning
X08 | 5 | 5 | Capability-gated modular memory routing
X09 | 3 | 4 | Growing/pruning mixture-of-experts, Hayek-style
X10 | 3 | 5 | Neural causal models with active interventions
X11 | 4 | 6 | Per-user LoRA memory with decay
X12 | 2 | 6 | Memory networks with learned eviction, consolidation
X13 | 5 | 6 | E-processes / anytime-valid sequential testing
X14 | 3 | 4 | Graph neural cellular automata, graph rewriting
X15 | 3 | 6 | Embedding-routed program library (DreamCoder)
X16 | 4 | 7 | Replicator dynamics / particle filter / XCS
X17 | 4 | 5 | TextGrad/Reflexion natural-language credit assignment
X18 | 6 | 6 | Chemical reaction networks, conservation-constrained nets
X19 | 5 | 7 | Label propagation / truth maintenance belief revision
X20 | 3 | 7 | Structured perceptron over min-plus (Viterbi) graphs
X21 | 4 | 6 | Graph-of-thoughts with verifier, causal CoT faithfulness
X22 | 4 | 7 | Sequitur/Re-Pair grammar induction by compression
X23 | 4 | 4 | Concept-drift detection plus test-gated hypotheses
X24 | 4 | 4 | DreamCoder library learning with MDL, hypernetworks
X25 | 2 | 8 | DreamCoder/Voyager verified program library
X26 | 3 | 6 | Bayesian causal structure learning, experimental design
X27 | 5 | 6 | MDL program induction, grokking explanations

FAMILIES
Fast-weight parameter-level memory (adapter/plasticity): X02, X03, X11
Episodic store with offline consolidation into weights: X04, X12
Compress exact record into shortest program (MDL): X22, X24, X27
Verified executable knowledge library, edit/retire without weight edits: X06, X15, X23, X25
Self-reshaping specialist population (budget, split, prune): X01, X09, X16
Active-experiment causal/world-model inference: X07, X10, X26
Localized credit and repair of faulty step/module: X17, X21
Leased access-gated knowledge partitions: X08
Hash-chained causal memory with loop breaker: X05
Anytime-valid e-process answer commitment: X13
Differentiable typed-graph rewriting state: X14
Conservation-constrained reaction-network computation: X18
Table-row iterative belief revision: X19
Tropical min-plus derivation graph: X20

TOP3:
X18 - the most distinct mechanism here. Conservation by construction gives a real guarantee, and a prototype is easy to build and test on resource or probability-mass tasks.
X13 - it gives an actual statistical guarantee (anytime-valid error control) for committing to an answer. It is directly testable against self-consistency, but the validity of the learned likelihood ratios is the crux.
X27 - it makes the memorization-to-rule switch explicit through description length. It can be tested cheaply on grokking-style tasks, and it targets a clear open question.