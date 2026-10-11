Today's models mostly interpolate. They sample from dense regions of a learned distribution, so their outputs drift toward what is common in the training data. Real originality needs ways to leave that distribution while staying coherent. Each of the three proposals below gives the system a source of novelty that does not come from how often something appears in the data. The sources are altered premises, unexplained residue and rewarded dissent.

**1. Premise mutation over an explicit world model.** Instead of one entangled network, the system learns a world model built from separable constraint modules, such as "objects persist" or "cost scales with size." To create ideas, it deletes, inverts or swaps one module and simulates forward to work out what follows. It keeps a mutated world only if that world stays consistent and explains some anomaly better than the original. The new idea comes from reasoning out the consequences of a changed rule, not from blending examples, much as non-Euclidean geometry came from dropping one axiom.

**2. Concept birth from residuals.** The system logs where its predictions keep failing. When a group of such errors cannot be compressed by any existing concept, it creates a new latent primitive. That primitive is trained only on the errors, with the rest of the model frozen. The new concept survives only if it then compresses data in other, unrelated domains. The model's vocabulary therefore grows from what the data fails to explain, the reverse of frequency-driven learning.

**3. A market of dissenting submodels.** Many small learners share one base model. Each is penalised for agreeing with the base model and with the other learners. A learner earns compute credit only when its prediction is correct and the others' are wrong. Learners that run out of credit die, and successful ones fork. Over time this produces a population of rare but valid viewpoints. It rewards being right where the consensus is wrong, not simply being different.

=== IDEAS ===
IDEA 1
NAME: Premise Mutation World Models
MECHANISM: The world model is learned as a set of separable constraint modules, such as conservation laws or causal regularities. The system deletes, inverts or swaps a module and simulates what follows. It stores the mutated worlds that stay consistent and explain anomalies better, and uses which mutations succeed to decide what to mutate next.
VALUE: It produces ideas worked out from changed premises rather than interpolated from common examples.

IDEA 2
NAME: Residual-Driven Concept Birth
MECHANISM: The system clusters prediction errors that keep recurring and that no existing concept can compress. For each cluster it creates a new latent primitive, trained only on that error while the rest of the model is frozen. It keeps the primitive only if it also compresses data in unrelated domains, so the concept vocabulary grows from what the data fails to explain.
VALUE: It creates concepts the training data never named, grounded in real anomalies rather than in frequency.

IDEA 3
NAME: Market of Dissenting Submodels
MECHANISM: A population of submodels shares a base model. Each submodel is penalised for agreeing with the base model and with its peers. A submodel earns compute credit only for predictions that are correct where the others are wrong. Submodels without credit die and successful ones fork, so a minority view survives only by being right.
VALUE: It reliably finds valid ideas that the majority view, and therefore the training distribution, would suppress.