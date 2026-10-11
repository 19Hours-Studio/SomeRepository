Today's generative models sample from their learned distribution, so their output stays near high-density regions of the training data. To get ideas that are actually new, a system needs a mechanism that pushes it away from that density and then checks that what it finds holds together. Here are three proposals.

1. **Tension-driven world-model repair.** The system keeps an explicit, executable model of a domain. It continuously searches for contradictions between that model's predictions and real observations or simulations. Each contradiction becomes a training target, and the system must invent new latent variables or rules to resolve it. The new ideas come from the structure of the problem, not from the corpus.

2. **Anti-density latent exploration.** A second network learns the density of the training data in the model's latent space. The generator is rewarded for finding points that this density model scores as very unlikely, but only if the points still decode into coherent, internally consistent artifacts. A verifier and a self-consistency check enforce that. This makes the search for "low prior, high validity" a direct optimization goal.

3. **Evolving private formal languages.** Separate agent populations solve tasks in an environment while developing their own symbolic notations under pressure to compress what they discover. The notations are never trained against human text. A translator maps only the most useful constructs back into human concepts afterwards. Ideas form in a representation that is not shaped by how humans usually frame things.

=== IDEAS ===
IDEA 1
NAME: Tension-Driven World-Model Repair
MECHANISM: The system maintains an executable world model (programs and causal graphs) and actively looks for inputs where its predictions conflict with observations or with each other. It stores these conflicts in a "tension buffer" ranked by severity. It then searches over structural edits (new latent variables, new operators, broken assumptions) that resolve the most conflicts with the least added complexity. Accepted edits are kept permanently, and the search moves on to the next conflicts these edits create.
VALUE: It generates concepts because reality demands them, not because they appeared in the training text, much like how scientific revolutions resolve anomalies.

IDEA 2
NAME: Anti-Density Latent Exploration
MECHANISM: A separate density estimator learns how probable each region of the generator's latent space is under the training data. The generator is optimized for the product of low density and high validity, with validity scored by verifiers, simulators and checks for internal consistency. Valid low-density discoveries are stored in an archive. The density model is updated to include them, so the same regions stop counting as novel and exploration keeps moving outward.
VALUE: It systematically finds ideas that are coherent but statistically unlikely, which plain sampling almost never reaches.

IDEA 3
NAME: Evolving Private Formal Languages
MECHANISM: Agent populations solve open-ended tasks while co-evolving their own symbolic languages, rewarded for compressing solutions and for reusing abstractions across tasks. The languages never receive human linguistic priors. Abstractions that greatly shorten solutions are kept as library primitives. A late-stage translator explains only the highest-value primitives in human terms.
VALUE: It produces conceptual building blocks without human framing biases, which can show us ways of breaking down problems that we have not thought of.