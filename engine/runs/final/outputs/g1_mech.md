All three ideas avoid the eleven forbidden families. Each is described only by the objects it stores, how they flow, the rule that changes them and the signal behind the change. The name comes last.

1. **Unmet requirements build up pressure.** The system keeps a graph of what each stored object needs and what it provides. When many requirements have no provider, the system creates a placeholder object. The placeholder is defined only by the shape of those requirements, never by any known object. The novelty comes from what the system's knowledge is missing, not from what is common in it.

2. **Failed attempts are kept and reused.** Normal problem solving builds and throws away many partial structures. Training data mostly contains finished results, so these dead ends are material it has never seen. The system stores them with labels for what they did and why they failed, and checks later problems against them.

3. **Concepts that bundle two things are split.** Some stored concepts glue together properties that only appear together by historical accident. The system measures how differently a concept is used across contexts and splits it when the usage forms separate clusters. The pieces can then combine in ways the original bundled concept never could.

=== IDEAS ===
IDEA 1
NAME: Requirement-Pressure Placeholder Synthesis
MECHANISM: The system keeps a graph of stored objects, each with a list of what it needs and what it provides. A pressure counter is kept for each unmet requirement and goes up every time a task needs it and no stored object provides it. When a group of related unmet requirements passes a threshold, the system creates a placeholder object defined only by the requirements it must meet, then looks for or builds something that fits. The placeholder is kept if filling it lets many waiting requirements be met, and its weight grows with how many it unblocks.
VALUE: New objects come from the shape of what is missing, not from reshuffling what is common.

IDEA 2
NAME: Discarded-Intermediate Reuse Heap
MECHANISM: Every partial structure built during problem solving and then thrown away goes into a heap. Each entry is labelled with what the structure did and why it failed for its original goal. When a new goal arrives, the system matches it against those labels, ignoring the original goal, before it looks at solutions that worked. Labels on entries that turn out useful later get a higher retrieval priority, so the heap learns which kinds of failure are worth keeping.
VALUE: It works from dead ends that finished-outcome data never contains.

IDEA 3
NAME: Usage-Divergence Concept Fission
MECHANISM: For each stored concept, the system records the contexts it is used in and measures how spread out and clustered that usage is. When usage splits into two or more separate clusters, the concept is split into child concepts, each keeping only the properties used in its cluster. The children are then allowed to combine freely with other objects, including combinations the bundled parent blocked. A split is kept when the new combinations it allows pass outside checks; otherwise the children are merged back.
VALUE: It frees properties that were glued together by accident, so the system can build ideas no single existing concept could express.