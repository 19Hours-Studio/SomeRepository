1. GOALS
(a) Behave correctly on combinations of familiar parts it has never seen. (b) Keep learning for a lifetime by reusing old skills instead of overwriting them. (c) Give the same answers when input sources drift or are recalibrated.

2. PARADIGM NEGATION
All mainstream AI tunes one large block of numbers by following the gradient of a single global error. That is forbidden here as a mechanism.

3. KNOWN ESCAPES
Families A–H are excluded.

4. MECHANISM FROM THE PERIPHERY
(a) Electrical network theory: any subcircuit reduces to its terminal equivalent (Thévenin), and any assembly of subcircuits is solved with Kirchhoff conservation.
(b) Fluvial geomorphology: stream-power erosion carves drainage trees that are hierarchical and last a long time.
(c) Radio interferometry: closure quantities cancel each antenna's unknown gain, and self-calibration then recovers those gains.

5. HONESTY CHECK
(a) Closest work is port-Hamiltonian networks and graph-based simulators. Those train jointly on whole assemblies. Here each part is fitted alone and parts are combined with no training. Kept.
(b) Closest work is Physarum and ant-colony path reinforcement, which strengthen single edges. Here each node holds a potential, accumulated flux is conserved, and the result is merge trees taught by base-level drops. Kept.
(c) Closest work is bispectral and gauge-equivariant networks, which cancel one global symmetry. Here every source has its own unknown gain, estimated again for each input. Kept.

=== IDEAS ===
IDEA 1
NAME: Terminal-Equivalent Kirchhoff Composer
MECHANISM: Each part stores only an interface law for each port: effort = Z·flow + source. Z and source are fitted by local least squares from probing that part's terminals. A situation is a wiring diagram of parts, and prediction solves for efforts and flows so that flows sum to zero at every junction and efforts agree across joined ports, re-linearizing any nonlinear parts. Adding a new part never changes the others.
DIFFERENCE: It predicts the behavior of new assemblies of known parts without retraining, because conservation laws fix how parts combine instead of examples teaching it.

IDEA 2
NAME: Erosional Drainage-Tree Learner
MECHANISM: Units on a lattice each hold an elevation. Input falls as "rain", and each unit passes its accumulated load to its steepest downhill neighbor, merging tributaries, until the load reaches an outlet (an output). Elevation changes as dz/dt = U − K·A^m·S^n, where A is accumulated flux, S is slope and U is slow uplift: paths many inputs share deepen into durable trunks, while unused terrain rises back as free capacity. Teaching lowers the base level at the correct outlet, and that drop travels upstream as a knickpoint and captures headwaters.
DIFFERENCE: It grows its own hierarchy of shared subcomputations, and new tasks join and deepen old channels instead of overwriting shared parameters.

IDEA 3
NAME: Closure-Phase Self-Calibrating Recognizer
MECHANISM: Input is split into sources (sensors, regions or speakers), and each pair gives a complex correlation V_ij, corrupted by unknown factors g_i·conj(g_j). Only loop quantities pass onward: closure phases arg(V_ij·V_jk·V_ki) and closure amplitudes |V_ij·V_kl|/|V_ik·V_jl|, in which every g cancels. Stored category templates are running averages of these. For each input, self-calibration alternates template matching with closed-form solves for each g_i, and returns both the content and the corruptions.
DIFFERENCE: Its answers are guaranteed not to change under any independent recalibration of any subset of sources; current models only approximate this by training on augmented data.