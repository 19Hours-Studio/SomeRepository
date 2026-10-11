=== IDEAS ===
IDEA 1
NAME: Phase-synchrony binding oscillator network
MECHANISM: Each concept is a group of coupled oscillators whose state is a phase and frequency vector. A binding between a role and a filler is a locked phase offset between their groups, and inference is the network relaxing into a synchronized attractor under learned coupling. Learning adjusts coupling strengths with a phase-Hebbian rule (in-phase pairs strengthen, anti-phase pairs weaken), with no backpropagated gradients.
DIFFERENCE: It keeps arbitrarily many simultaneous instances of the same concept distinct within a fixed-size state, identified by phase rather than by index or position slot, so binding does not require a per-instance parameter budget.

IDEA 2
NAME: Exactly invertible bidirectional reasoner
MECHANISM: The model is a stack of coupling layers that forms a bijection between observation and latent state, with weights shared in both directions. Forward passes predict, and backward passes compute exactly, without search, the latent states consistent with a given outcome, so abduction is a native operation. Activations are not stored for training because each layer is recomputed by inversion, which keeps training memory constant in depth.
DIFFERENCE: It answers "what latent states would yield this outcome" by exact inversion of its own computation, which a non-invertible model can only approximate through sampling or search.

IDEA 3
NAME: Cellular medium working memory
MECHANISM: The input is written as a seed into a spatial lattice of cells, each holding a learned vector. One shared local update rule, applied in parallel to each cell and its neighbors, runs for a number of steps set by the problem's geometry, and the lattice's spatial extent serves as working memory. Learning trains only the shared rule, by backpropagating through the unrolled steps on problems of varied size.
DIFFERENCE: The same fixed parameters can run on problems larger than any seen in training, with each cell's update cost fixed regardless of how large the medium grows, because computation scales with the medium rather than with a context window or fixed depth.