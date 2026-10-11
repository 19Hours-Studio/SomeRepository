**Offspring 1 (Pair 1: easy-direction twins × kind exponents)**
This is a crossover where each parent changes the other. The system makes forward twins: it fixes the answer first, then builds the problem. The exponent algebra then rescales or swaps kinds in each twin. That turns one known-answer twin into a whole orbit of known-answer twins, including ones at magnitudes the system has never seen. So the algebra multiplies the twin generator, and accuracy gets measured as a function of how far along the orbit a twin sits from experience.

The twins also referee the algebra. Suppose a real task's output doesn't change the way its exponents predict. If the matched twin at that orbit position is solved correctly but still breaks the predicted change, the algebra is at fault, so a kind is split or an exponent revised. If the twin itself is solved wrongly, the solver is at fault, and that cell's accuracy is lowered.

Closest existing work: metamorphic testing, and calibration by consistency under transformations. The difference here is that the relations are learned and revised, and that known-answer twins decide who is to blame for each violation. So this is not just a re-skin.

**Offspring 2 (Pair 2: edit-effect variables × kinetic proofreading)**
In this crossover, the "independently perturbed context" at each proofreading stage is an edit taken from a different effect cluster. The clusters are ordered from far to near in the link graph. A step that detaches from any stage resets to the start. Each committed step keeps its survival profile as its "scope", which is the set of variables it has been shown not to depend on. Later steps can combine only with committed steps whose scopes are compatible.

Proofreading also rewrites the clustering. Suppose an edit keeps detaching steps even though the clustering marked its cluster as unlinked. Then that cluster is split, or a typed link is added. This finds second-order structure that the passive frozen-predictor probing missed.

Closest existing work: CheckList-style invariance testing, IRM, and verifier cascades. The differences are that the perturbation set comes from discovered variables, that survival gives a reusable scope rather than a pass/fail, and that the failures rebuild the parse.

=== IDEAS ===
IDEA 1
NAME: Covariant Orbit Twin Calibration
MECHANISM: Known-answer twins are generated from fixed answers. Each twin is then pushed through the learned kind-exponent algebra (rescalings and kind swaps) to make an orbit of further known-answer twins at magnitudes the system has not seen. Accuracy is stored per twin cluster and per orbit distance. When a real task's output breaks the change its exponents predict, the matched twin decides the cause: a correct twin that still breaks it means the algebra is wrong (split a kind or revise an exponent), and a wrongly solved twin means the solver is wrong (lower that cell's accuracy).
VALUE: Calibrated correctness estimates that reach into extrapolation regimes, plus a units algebra that can tell its own errors apart from solver errors.

IDEA 2
NAME: Scope-Earning Perturbation Ratchet
MECHANISM: Before an inference step is committed, it must survive K irreversible stages. Each stage applies an edit from a different discovered effect cluster, going from far to near in the link graph, and any detachment resets the step to stage one. Each committed step stores its survival profile as a scope, meaning the variables it has been shown not to depend on, and steps can combine only when their scopes are compatible. When an edit keeps detaching steps even though the clustering marked its cluster as unlinked, the clustering is refit: that cluster is split or a typed link is added.
VALUE: Reasoning steps that come with an explicit, tested record of what they do not depend on, while the input's variable structure keeps getting corrected by the reasoning's own failures.