**Offspring 1 (Pair 1).** For each systematic absence (feature pair i,j whose marginals are frequent but whose joint is near zero), the absence itself defines the task battery: the battery contains only tasks where i and j are each useful on their own. The suppressor circuit is released at graded strengths, which gives a dose-response matrix of consequences. A minimum-cost regression hedges this matrix against the consequence vectors of earlier cuts and known ideas. Only cuts with an unhedgeable residual are applied, at the dose where the residual peaks. A failed cut becomes a law, which is added as a short position (a negative basis vector) that hedges later candidates. So each parent steers the other: absences choose what gets valued, and residuals decide what gets cut and how deeply.

**Offspring 2 (Pair 2).** Concepts are not picked by hand for unlearning. The model ablates whichever concept node most raises the count of floppy modes (the rank drop of the constraint Jacobian) per unit of lost verified competence. Ablating a self-stressed, redundant node frees nothing, so the measure picks out keystone concepts. The naive copy then has to rebuild using only the freed modes. A rebuilt concept counts as an alternative foundation if it re-pins the same subspace with different constraint normals. Any mode it leaves floppy is explored and verified, and then pinned as a new concept.

**Offspring 3 (Pair 3).** An artifact and its quality axis are forced together. Each step adds two things: a condition that breaks the defining feature of a listed concept, and a pairwise preference ranking the partial artifact above that concept's exemplars. A step is admitted only if the solver finds it compatible, and the axis so far stays stable, few-shot learnable and independent of the human-criteria bank. The listing order goes first to concepts whose exemplars make the axis correlate with known criteria.

**Honesty check.**
- Offspring 1: the closest work is creativity steering (2412.06060) together with DreamCoder-style usefulness scoring. Neither uses co-occurrence absences to define the evaluation battery, prices cuts at graded doses, or treats failed cuts as hedging assets. It is also not ANTIPRED, because it rewards residual consequences, not improbability.
- Offspring 2: the closest work is Unlearning-as-Ablation (2508.17681). That work picks targets by hand and only tests re-derivation. Here rigidity picks the target and limits the rebuild, and leftover freedom is explored. It is not CFWORLD, because the model's concepts change, not the world's laws.
- Offspring 3: the closest works are Denial Prompting and Weights-to-Words. Both handle the artifact and the criterion separately. Here each step must certify both at once.

=== IDEAS ===
IDEA 1
NAME: Suppression Arbitrage Dosing
MECHANISM: Each systematic absence among SAE features defines its own task battery, and the circuit suppressing it is released at graded doses to build a dose-consequence matrix. A minimum-cost regression hedges that matrix against stored consequence vectors from known ideas and earlier cuts. A cut is applied only at the dose where the unhedgeable residual peaks. Failed cuts are stored as laws and act as negative hedging assets for future candidates.
VALUE: Only those hidden corpus prohibitions are removed whose removal unlocks capabilities that nothing already known can reproduce.

IDEA 2
NAME: Keystone Concept Rigidity Excavation
MECHANISM: The model ablates the concept node whose removal frees the most floppy modes (Jacobian rank drop) per unit of lost verified competence; this skips redundant, self-stressed concepts. An ablated copy rebuilds the domain from raw phenomena using only the freed modes. Rebuilt concepts that re-pin the same subspace with different constraint normals are stored as alternative foundations. Modes left unpinned are explored, verified and named as new concepts.
VALUE: It finds the concepts that history made load-bearing and recovers the conceptual routes they closed off.

IDEA 3
NAME: Co-Forced Artifact and Criterion
MECHANISM: An artifact and a new quality axis are built step by step together. Each step adds a condition that breaks one listed concept's defining feature and a preference ranking the partial artifact above that concept's exemplars. A step is admitted only if a solver confirms consistency and the axis stays stable, few-shot learnable and independent of the bank of human criteria. The listing order goes first to concepts that keep the axis correlated with known criteria.
VALUE: Each output is an idea outside everything the model can name, delivered together with a new, teachable reason why it is good.