**Offspring 1 (Pair 1).** In this design a lesson has to do two jobs. It teaches, and it also works as an answer-first generator: from the lesson the system builds twin tasks whose answers are fixed in advance. A fresh small student learns only from the lesson and is then scored on those twins. A discriminator matches real tasks to the lesson whose twins it cannot tell apart from them. That student's twin accuracy becomes the correctness estimate for the real task. So lessons decide what twins exist, and twin realism decides which lessons survive. A lesson whose twins are easy to tell from real tasks gets rewritten or pruned. Real tasks that no lesson's twins can imitate are flagged as untaught territory.
Closest work: Absolute Zero, iterated learning, and synthetic textbook data ("Textbooks Are All You Need"). This differs because the twin generator is the transmitted lesson itself, and pruning is driven by how indistinguishable its twins are.

**Offspring 2 (Pair 2).** Edits are applied at graded strengths, not just on or off. For each cluster, a kind-exponent vector is inferred from the log-log slope of the frozen predictor's response against edit magnitude. Clustering must respect the kinds: edits with incompatible slopes cannot share a cluster. In the other direction, each second-order interaction is tested against the kind algebra. If it composes multiplicatively and its exponents add up, it becomes a typed link. If it does not, the cluster splits into two kinds.
Closest work: data-driven discovery of dimensionless groups (Bakarji 2022, AI Feynman). Those work on labelled physical quantities. Here the kinds are found in raw perceptual input, through how a model responds to edits.

**Offspring 3 (Pair 3).** Each holding stage is a fresh student, and each stage's student is smaller than the one before. A candidate reasoning step, plus its one-line justification, is committed only after K students in a row each reproduce it from the current lessons alone. If any student fails, the step goes back to stage 0 and its justification is rewritten. The number of stages a step survives measures how far it can be compressed while still being taught. Steps that many others depend on get a larger K.
Closest work: prover-verifier legibility games (Kirchner 2024) and verifier cascades. Those use one verifier that is trained. Here the check is a sequence of shrinking students, with reset to the start on failure.

=== IDEAS ===
IDEA 1
NAME: Lessons That Forge Their Exams
MECHANISM: Every retained lesson must also run as an answer-first generator of twin tasks, and a fresh student taught only that lesson is scored on them. A discriminator assigns each real task to the lesson whose twins it cannot tell apart from it, and that student's twin accuracy is the correctness estimate for the real task. Lessons with twins that are easy to distinguish are rewritten or pruned. Real tasks that no lesson can imitate are marked as untaught territory for writing new lessons.
VALUE: It gives a calibrated correctness signal with no oracle, together with a map of what the system's explicit knowledge does not yet cover.

IDEA 2
NAME: Graded-Edit Scaling Kinds
MECHANISM: Input edits are applied at graded strengths, and each edit-effect cluster gets a kind-exponent vector inferred from the log-log slope of the frozen predictor's response. Clusters cannot mix incompatible exponents. Each second-order interaction is checked for multiplicative composition: a pass makes a typed link, and a failure splits the cluster into two new kinds. The stored kinds, exponents and edit library are refit as new inputs arrive.
VALUE: It finds dimension-like variables directly in raw text, pixels or sensor data, which supports extrapolation and sanity checks on answers in domains that have no unit system.

IDEA 3
NAME: Shrinking-Student Proofreading Ladder
MECHANISM: A candidate reasoning step with its one-line justification is committed only after K fresh students in a row, each smaller than the last, reproduce it from the current lessons alone. Any failure resets the step to stage 0 and forces its justification to be rewritten. The number of stages survived is stored as a graded legibility and confidence score, and K is raised for steps that many later steps depend on.
VALUE: Accuracy can be bought with compute while keeping every committed step explicit and teachable to a small mind.