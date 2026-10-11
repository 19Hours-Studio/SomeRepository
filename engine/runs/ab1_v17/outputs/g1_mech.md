All three mechanisms below take their correctness signal from somewhere other than the system's own judgement. The sources are events the system cannot influence, agreement between sub-systems that cannot share mistakes, and transformations whose effect on the answer is known by construction. None of them uses a grader that is the same fallible model.

=== IDEAS ===
IDEA 1
NAME: Sealed Forecasts Against Time
MECHANISM: Whenever the system makes a claim, it also writes down concrete, checkable predictions about data that has not arrived yet: future entries in incoming streams, logs, measurements or published records that the system cannot write to. Each prediction is stored with a fingerprint and a deadline so it cannot be changed afterwards. When the data arrives, a fixed string or number comparison settles the prediction mechanically. Only settled predictions change the parameters, and each update is weighted by how surprising the outcome was. The claims that produced wrong forecasts lose influence on future answers.
VALUE: The system can correct itself in open-ended domains with no oracle, because the world's future acts as the grader and that grader cannot be flattered or influenced.

IDEA 2
NAME: Disjoint-Evidence Agreement Ledger
MECHANISM: The raw evidence is split into partitions that do not overlap, and a separate copy of the system is trained on each one. The copies answer the same question independently. Agreement counts as a label only when the copies' evidence is disjoint. Its weight shrinks by how correlated their errors are, which is measured by quietly corrupting one partition and seeing whether the other copies follow the corruption. A ledger stores, for each pair of copies, how often they agree by chance and how often their errors move together. Copies whose dissent later turns out justified get more weight.
VALUE: Copies that saw different evidence can label each other's work, and the ledger keeps them from passing shared bias off as truth.

IDEA 3
NAME: Known-Effect Transformation Audits
MECHANISM: A small rule set, checked once by hand, holds transformations whose effect on the correct answer is fixed by construction. Examples: swapping units should rescale a number, reordering items should leave a count unchanged, duplicating a list should double a sum, and negating a premise should flip a conclusion. The system answers both the original question and its transformed version. Any answer pair that breaks the known relationship is certainly wrong, whatever the true answer is. The violation rate is stored for each pair of topic and transformation, and the parameters are pushed toward restoring the relationship. Topics with high violation rates get the most new transformations.
VALUE: The system finds certain errors on questions nobody knows the answer to, because the error signal comes from fixed algebra rather than from the model's opinion.