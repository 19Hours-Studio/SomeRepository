Three directions that drop attention over tokens entirely: knowledge as glued local theories, computation as physical pattern formation, and reasoning as self-modifying symbolic rewriting.

=== IDEAS ===
IDEA 1
NAME: Sheaf-Glued Local Theories
MECHANISM: Knowledge is stored as thousands of small, separately trained local models. Each one is valid only on an overlapping region of context space (a "patch"), and learned restriction maps say how neighbouring patches must agree where they overlap. Inference searches for a global section: an assignment that satisfies all active patches at once, found by iterative consistency propagation instead of a single forward pass. Learning adds, splits or refits patches only where the measured disagreement (the obstruction to gluing them together) is high, and leaves every other patch untouched.
DIFFERENCE: It can pinpoint and report exactly where its own knowledge contradicts itself, and it can learn new facts without overwriting old ones because no globally shared weights exist to interfere.

IDEA 2
NAME: Morphogenetic Compute Substrate
MECHANISM: Computation runs as reaction-diffusion dynamics on a continuous 2D or 3D field of chemical-like state variables. Inputs are injected as boundary conditions, and outputs are read from the stable patterns the field settles into. Memories are attractor patterns encoded in local reaction rules that every cell shares, like a genome. Learning adjusts those rules through local error signals that diffuse through the field, and the substrate grows new cells where unresolved error is steepest.
DIFFERENCE: It repairs itself after arbitrary damage and gives more physical compute to hard sub-problems at runtime, with no fixed graph or parameter count.

IDEA 3
NAME: Self-Rewriting Program Graph
MECHANISM: The model's state is a typed graph of small symbolic programs and data nodes. Computation applies learned graph-rewrite rules over and over until the graph reaches a normal form, and that normal form is the answer. Rules live in a library and are scored by how much they compress observed experience (minimum description length). Gradient-free search proposes new rules by abstracting recurring rewrite sequences into single rules, while a small neural prior only ranks which rule to apply next.
DIFFERENCE: Its computation depth is unbounded and depends on the input, every intermediate step can be checked exactly, and it can generalize to inputs of any size (for example, longer arithmetic) instead of only interpolating within its training distribution.