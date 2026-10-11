**My 12 most obvious answers (now forbidden, along with anything close to them):**
1. State-space / linear-recurrent sequence models (Mamba-style)
2. Spiking / neuromorphic networks
3. Neuro-symbolic hybrids, differentiable logic
4. Continuous-time / liquid networks, neural ODEs
5. Predictive world models (JEPA-style)
6. Mixture-of-experts / modular routing
7. External differentiable memory / retrieval augmentation
8. Hyperdimensional / vector-symbolic computing
9. Energy-based models / modern Hopfield nets
10. Graph and capsule networks
11. Predictive coding, Hebbian/local learning, active inference
12. Evolved or self-modifying nets, neural cellular automata

Also forbidden as neighbors: diffusion-style reasoning, reservoir and oscillator networks, optical and quantum hardware, cortical-column models, program synthesis, and ensembles or debate.

=== IDEAS ===
IDEA 1
NAME: Interrogative Representation Engine
MECHANISM: The model stores no feature weights. It keeps only a growing list of yes/no questions, and each question is a small executable probe that compares the input with a stored example, the environment, or the model's own earlier answers. An input's representation is its string of answers. Learning starts from confusion: when two inputs with different outcomes produce the same answer string, a search over probe programs adds one question that separates them, and old questions are never revised.
DIFFERENCE: It can learn a concept from a single confusion without changing any earlier behavior, and every decision can be read as an explicit list of answered questions.

IDEA 2
NAME: Transmission-Bottleneck Learner Lineage
MECHANISM: The system is a chain of short-lived small learners instead of one long-lived network. Each learner is trained only on a tiny sample of its predecessor's input-output behavior, and then the predecessor is deleted. Only behavior that survives repeated handoffs through this bottleneck persists, which pushes knowledge toward compositional, compressible rules (as iterated-learning studies show). New world data is mixed into each handoff sample and competes with inherited behavior to be passed on, and there is no fitness selection.
DIFFERENCE: Generalization comes from having to survive relearning, not from regularizing a fixed set of parameters, so everything it knows can be learned from few examples and moved to any substrate.

IDEA 3
NAME: Homological Cycle Memory
MECHANISM: Knowledge is stored as the shape of a growing cell complex: experiences add vertices, co-occurrences add edges and higher cells, and concepts are holes (cycles) that persist across many fillings. Inference asks topological questions, such as whether a query path can be shrunk to a point and which cycles it winds around and how often, using sparse linear algebra on boundary matrices with no message passing. Learning adds cells that fill spurious holes, so only persistent homology classes remain as concepts.
DIFFERENCE: Its answers do not change under any continuous deformation of the data, so it directly counts loops, periodicity and winding, which architectures built on point embeddings can only approximate.