**Absurd ideas (unfiltered), each with its hidden kernel**

1. Forget every input the instant you read it, so the model stays humble. Kernel: learned forgetting under a memory budget.
2. Store no weights; brute-force a seed per prompt that happens to answer correctly. Kernel: weights should be the shortest program that generates them.
3. Pick each token's expert by the alphabetical order of the previous word. Kernel: content-keyed sparse routing.
4. Train by asking the network to write a haiku about its loss, then fine-tune on it. Kernel: a natural-language diagnosis can say which part failed.
5. Make neurons gossip in a town hall and vote on the output. Kernel: many weak units settling to a fixed point.

Picked 1, 2, and 4: they target continual learning, compressed and inspectable structure, and localized credit assignment, which current architectures handle poorly.

=== IDEAS ===

IDEA 1
NAME: Budgeted Forgetting Memory Machine
MECHANISM: The model streams inputs into a fixed-size slot memory with no context window. When full, a learned scorer predicts each slot's future utility and evicts the lowest, while unretrieved slots decay. Frequently retrieved slots are periodically distilled into slow weights during an offline consolidation pass.
DIFFERENCE: It learns continuously from an unbounded stream under an explicit memory budget, moving knowledge into parameters without catastrophic interference, which fixed-context models cannot do.

IDEA 2
NAME: Description-Length Generator Weights
MECHANISM: Instead of dense matrices, the model stores a library of reusable motifs plus a typed program that composes and parameterizes them into layers on demand. Training minimizes task loss plus the bit cost of the program, rewarding reusable structure. New skills are added by editing a few program fragments and fitting their few parameters rather than retraining everything.
DIFFERENCE: Capability scales with program size rather than parameter count, and the structure stays discrete and inspectable, so it can extend itself through targeted edits that dense networks cannot make.

IDEA 3
NAME: Language-Directed Credit Routing
MECHANISM: The network is a set of separately addressable modules. After a failure, a critic writes a natural-language diagnosis naming the responsible module and step; that diagnosis selects which parameters receive gradient and becomes a corrected trace in a replay buffer. Learning thus uses rich textual error signals to localize updates instead of one scalar backpropagated through everything.
DIFFERENCE: It can repair a specific faulty capability from a handful of failures at deployment, with credit localized by explanation rather than by global gradient.