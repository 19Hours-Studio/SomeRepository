Today's LLMs have three structural gaps. Their weights are fixed when they run, so they cannot learn anything lasting from a single experience. They have no internal state that runs alongside the world and can be checked against it, so they cannot notice when their beliefs are wrong. And every query gets roughly the same compute in one forward pass, so they cannot hold a goal open and work at it until it is actually reached. Each proposal below targets one of these gaps with a different computational structure, not a larger or tweaked transformer.

1. **Learning stored as sparse, gated memory patches.** Instead of a context window, the system grows small permanent memory units during operation. Each one is created only when a surprise signal crosses a threshold. A consolidation process that runs offline later merges or removes them.

2. **A world model that predicts, gets checked, and is repaired.** The system keeps a structured world state made of objects, relations and causal links. It predicts what it should observe next and compares that against what it actually observes. When they disagree, it does not just ignore the mismatch. It finds the causal links responsible, repairs them, and records how reliable each link is.

3. **Reasoning by settling until constraints are met.** Thought is a process that runs until it settles, rather than a fixed number of layers. Candidate answers, sub-goals and constraints are linked units that keep adjusting each other until a checker accepts the result. Compute therefore grows with how hard the problem is, and the system knows when it has failed.

=== IDEAS ===
IDEA 1
NAME: Surprise-Gated Synaptic Patch Memory
MECHANISM: When prediction error on an input crosses a learned threshold, the system writes a small key-value module next to the frozen core. The key is the context embedding and the value is a low-rank change to the core's weights. Those changes take effect only when a later context is similar to that key. During an offline phase, the system replays old episodes against the patches. It merges patches that do the same thing and deletes ones that conflict, using how often they agree as the score. Each patch keeps a count of how often it was used and how often it was confirmed, and patches that stop earning their place are removed.
VALUE: The system could learn permanently from a single experience without forgetting what it already knows or needing retraining.

IDEA 2
NAME: Falsifiable Causal World-Graph
MECHANISM: Perception updates a running graph of objects, their attributes and typed causal links. Each link carries a probability and a count of how many times its predictions came true. Before each step the system simulates what it expects to observe, then compares that with what it actually observes. When they differ, it traces the error back through the graph to the links most to blame and revises them: it adds hidden variables, splits links or reverses their direction. It can also run interventions inside the graph to test competing explanations before acting.
VALUE: The system could know when its beliefs are wrong, reason about counterfactuals, and keep a consistent, inspectable model of the world over long periods.

IDEA 3
NAME: Verifier-Halted Constraint Relaxation
MECHANISM: A query is turned into a set of variables, which are partial answers and sub-goals, plus constraints between them that are learned or extracted from the query. Local update rules pass messages between these units, and the system keeps iterating until either a symbolic checker or a learned checker confirms that every constraint is met, or the energy of the system stops falling. When progress stalls, the system adds intermediate variables, for example lemmas or sub-plans, and stores successful arrangements as reusable templates.
VALUE: The system could spend compute in proportion to how hard a problem is and solve multi-step problems it cannot solve in one pass, with a clear signal for when it has succeeded and when it has failed.