Recombination is the default because generation samples from a density fitted to the training data. To get past it, the system needs a source of signal the corpus does not contain, and it must be allowed to build new representational primitives from that signal. All three proposals below rest on that idea.

**1. Anomaly-driven concept invention.** In science, new concepts usually appear to explain persistent failures, not to blend old ideas. The system keeps several separate world models and an anomaly ledger. The ledger records cases where those models disagree with each other, or where predictions fail inside executable environments such as formal math, code or simulators. A search process proposes new latent variables, meaning candidate concepts. A concept is kept only if it shortens the description of the anomaly ledger without making the existing knowledge more expensive to encode. Concepts are judged by what they explain, not by how likely they look under the training data.

**2. Orthogonal latent growth.** The system records the subspace that its activations on training data occupy. It then adds new dimensions that are forced to stay orthogonal to that subspace. Those dimensions are trained only on outcomes the system checks for itself in grounded environments. Content stored there cannot be a mixture of training representations, so the system ends up with a separate vocabulary built from its own experience.

**3. Divergent taste ecology.** A population of generators each has its own learned measure of what counts as "interesting." Each measure is rewarded for differing from the others and from human-corpus preferences, while staying predictive of verified downstream usefulness. An idea scores highly when one agent values it, peers cannot predict it, and it later proves useful. Over time this produces new standards of value, not just new outputs.

=== IDEAS ===
IDEA 1
NAME: Anomaly-Compressing Concept Invention
MECHANISM: Several independent world models make predictions inside executable environments. Every disagreement or failed prediction goes into a persistent anomaly ledger. A search process proposes new latent variables and adopts one only if it reduces the description length of the ledger without increasing the cost of encoding prior knowledge. Adopted concepts become reusable primitives, and the ledger is then re-scored against them.
VALUE: Lets the system invent explanatory concepts that are justified by unexplained evidence, not by how often things co-occur in the corpus.

IDEA 2
NAME: Orthogonal Latent Growth
MECHANISM: The system estimates and stores the basis of the subspace its activations on training data occupy. It adds new latent dimensions with a penalty on any projection onto that basis, and trains them only on self-generated outcomes verified in grounded environments. When an expansion region saturates, it is frozen and a new orthogonal region is grown.
VALUE: Gives the system a growing set of representations that cannot be built from training-data patterns.

IDEA 3
NAME: Divergent Taste Ecology
MECHANISM: Each generator in a population learns its own interestingness function. Each function is rewarded for differing from its peers and from human-corpus preferences, but only while it still predicts verified downstream usefulness. Ideas are scored by how much one agent values them, how poorly peers predict them, and how useful they later prove. Agents whose tastes fail to predict usefulness are culled and replaced by mutated variants.
VALUE: Lets the system discover new criteria for what is worth pursuing, opening directions that a model rewarded for human-like preferences would never pick.