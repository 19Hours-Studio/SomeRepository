=== IDEAS ===
IDEA 1
NAME: Slot-written continual memory adapters
MECHANISM: Writes go to a slot store, where a write head decides whether to touch an existing slot with a small additive update or to overwrite it, based on the distinction between the new key and the stored keys. Each slot keeps its content in formats that are dense vectors or sparse codes, while the base encoder stays frozen and never changes. When surprise crosses a breakpoint and recent slots are distilled into low-rank adapters by a laforge pass, the freed slots are reused.
DIFFERENCE: It keeps absorbing new facts after deployment and consolidates them into adapters while the core stays fixed, which fixed-weight transformers cannot do without catastrophic forgetting.

IDEA 2
NAME: Self-routing executable program memory
MECHANISM: Each input is scored by how it differs from each stored program's prediction, and every program carries its own ltconfig of weights and step limits. Text is split at whitespaces and the router assigns each segment to the program whose progname matches its learned signature. The state is read through viewkeys and each running program executes as a jupyter cell whose output seeds the next cell, with a timely halting check that stops a cell once its step budget is spent.
DIFFERENCE: It adds or revises behaviors as separate stored programs without retraining shared weights, which current architectures cannot do while keeping prior behaviors intact.

IDEA 3
NAME: Order-free set contraction reasoner
MECHANISM: A khaled encoder maps each stored fact to a vector, and a washington reader contracts the unordered set of facts by repeatedly merging pairs with a symmetric function. The reader's documented permutation guarantee holds by construction, since each lippitsch layer applies a reduce operation over the merged pairs. Training learns only the symmetric merge function, the stored set is never rewritten, and a query is answered once the set contracts to a single vector.
DIFFERENCE: It answers queries over unordered fact sets with order-independence guaranteed by construction, a property that sequence models with positional encodings do not provide.