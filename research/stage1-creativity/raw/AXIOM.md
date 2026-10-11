Each idea inverts the two assumptions named in its brief.

1. Inverting tokens and the weights/context split: raw continuous signals enter a plastic field where the same synapses compute and store, so no context buffer exists.
2. Inverting gradient loss and passive data: the learner chooses its own experiments and keeps hypotheses that compress its experience, with no global differentiable loss.
3. Inverting scale and the single model: capability comes from a coalition of small, redundancy-pruned specialists, with no single parameter set.

=== IDEAS ===

IDEA 1
NAME: Plastic Continuous Field Machine
MECHANISM: Raw continuous signals enter a recurrent field with no tokenization. Synapses are both the stored memory and the operator: each step produces output and applies local, decaying plasticity, while slow weights consolidate what fast weights retain. Experience is written into the parameters that do the computing, so no context is ever re-read.
DIFFERENCE: It learns from an unbounded stream at constant cost per step, with no context window or retraining.

IDEA 2
NAME: Self-Selecting Compression Learner
MECHANISM: The model keeps a population of candidate world-models and chooses the experiment that best splits them, maximizing expected information gain. Each observation reweights candidates by Bayesian evidence and proposes new ones by local mutation, keeping only those that shorten the description of its experience (minimum description length). No differentiable loss exists; its sole objective is measured learning progress.
DIFFERENCE: It can answer questions no fixed dataset contains by generating its own training data, which a loss-minimizer handed data cannot do.

IDEA 3
NAME: Composable Specialist Coalition Society
MECHANISM: The system is a population of small specialists with fixed parameter budgets. Each input recruits a task-specific coalition by bidding, and their outputs are merged by learned message passing. A specialist splits when it covers two skills and is pruned when it duplicates another, so capacity goes only to non-redundant knowledge. There is no single parameter set: identity lives in the coalition, and one skill can be revised without touching the rest.
DIFFERENCE: Capability can keep rising while total parameters and compute stay flat, and individual skills can be revised without catastrophic forgetting, which a monolithic model cannot do.