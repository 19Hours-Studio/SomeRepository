Recombination happens because a model can only produce what lies in the span of its learned representations, and it is rewarded for staying close to its training distribution. Getting original ideas therefore needs mechanisms that do three things: create representations outside that span, get experience no human has recorded, and break the priors the model inherited from its training data.

**1. Orthogonal concept synthesis.** Use a sparse dictionary (for example a sparse autoencoder) to break the model's internal activations into concept atoms. Then deliberately build new atoms that are orthogonal to every atom learned from training data. Inject each new direction into the model's hidden states while it predicts outcomes in simulators, code execution or physical data. Keep an atom only if it measurably improves prediction somewhere. The result is a concept that is useful but has no human-language precedent.

**2. Alien micro-world exploration.** Have the system invent formal toy universes with novel rule systems, run them, and mine stable regularities from them: invariants, conservation laws and emergent structures. Then use structure-mapping to test whether any of those regularities match real-world data. Ideas come from experience gathered in worlds that are not in the training data, instead of from text about our world.

**3. Prior-free anomaly learners.** Track clusters of persistent prediction failures that small fine-tuning updates cannot fix. When such a cluster appears, train a small learner from scratch, with no pretrained weights, only on the anomaly data plus raw observations. Then let it compete with the main model. The new framework is not shaped by consensus priors, much like an outsider who solves a field's open problem.

=== IDEAS ===
IDEA 1
NAME: Orthogonal Concept Synthesis
MECHANISM: A sparse autoencoder breaks the model's activations into a dictionary of concept atoms. The system generates candidate directions orthogonal to all of these atoms, injects them into hidden states, and tests whether they improve prediction in simulators, code execution or real data. Atoms that survive are stored as new dictionary entries and gain names and uses through further training. The dictionary keeps growing, and novelty is always measured against the current span.
VALUE: It lets the AI form concepts that have no counterpart in any human-written text.

IDEA 2
NAME: Alien Micro-World Exploration
MECHANISM: A generator writes novel rule-based universes, such as cellular automata, invented physics or algebraic games, and runs them at scale. It mines invariants and emergent structures from these runs and stores them with the rules that produced them. A structure-mapping module tests whether each invariant matches patterns in real-domain data. Worlds whose invariants transfer get rewarded, so the generator learns to invent more fertile worlds.
VALUE: It is a source of ideas grounded in experience that nobody has recorded.

IDEA 3
NAME: Prior-Free Anomaly Learners
MECHANISM: The system clusters persistent prediction failures that resist gradient updates to the main model. For each cluster it initializes a fresh learner with no pretrained weights and trains it only on that anomaly plus raw observations. The learner then competes with the main model on held-out predictions, and a learner that wins is distilled back in as a new module. Recurring anomaly types tune when these learners are spawned.
VALUE: It lets the AI build explanatory frameworks that its inherited consensus priors would have ruled out.