=== VALUED C01 ===
ANCHOR: lesion-crossing complementation defines modules
NAME: Complementation-Routed Modular Network
MECHANISM: The network learns its own module boundaries during training. Pairs of small lesions that change a behavior are "crossed" by mixing activations between the two lesioned copies. If the behavior comes back, the lesions hit separate units; if it does not, they hit the same unit. The resulting complementation groups become the network's routing partition, and it is re-partitioned periodically. Every later update, such as a gradient from a user correction or a task outcome, is confined to the parameters of exactly one group and is committed only if it fixes the flagged behavior while every other group's probe phenotype stays unchanged. That phenotype is measured against the intact model's own outputs, so no oracle is needed. The failure flag itself stays external and can be sparse. Localization, containment and side-effect verification are things the architecture computes for itself.
VALUE: Teams that run continually updated models can apply each correction from sparse real-world feedback as a local edit whose lack of side effects is verified, so the model can keep learning for years without regressions or retraining.

=== VALUED C02 ===
ANCHOR: learned integer kind-exponent vectors
NAME: Kind-Typed Neural Algebra
MECHANISM: Every activation that stands for a quantity or entity carries an integer exponent vector over learned base kinds, and the network's composition operations are typed. Multiplication adds the vectors. Addition, comparison and attention between values are masked unless the vectors match, so an ill-kinded combination is impossible inside the computation rather than caught afterwards. The kind lexicon is fitted to expressions people actually write in corpora, tables and spreadsheets, which are external data the model did not produce. Its objective is to forbid as many syntactically possible combinations as it can while keeping zero imbalance on observed expressions. A persistent imbalance adds a new kind or a conversion constant, and a kind that forbids nothing is merged away. Kinds are not limited to physics: currencies, per-capita versus totals, people versus households, and dates versus durations all become learned base kinds.
VALUE: Analysts in finance, policy, science and engineering get quantitative reasoning in which whole classes of category errors are impossible by construction rather than something the model has to notice, and magnitudes extrapolate through exact scaling rules.

=== VALUED C03 ===
ANCHOR: Hodge decomposition of derivation misclosures
NAME: Cochain Belief Store
MECHANISM: The system's memory stores beliefs as edge quantities, meaning derivations that relate claims. Node beliefs are read out as the least-squares potentials of that graph, and a Hodge decomposition runs on it continuously as part of inference. The curl part of each loop's misclosure points to the faulty derivation (found with a w-test). The harmonic part triggers a bridging derivation chosen by minimal detectable bias and taken from a source different from the loop it crosses: if the misclosure collapses it was a mistake, and if it survives it marks a real frame split, which adds a context variable. The gradient subspace is exactly what the system cannot grade itself, so it is never trusted internally, and external observations ("control points") are spent only on the nodes that span it.
VALUE: Researchers, auditors and intelligence analysts get an AI whose belief state separates internally verified conclusions from genuine frame disagreements, and gives the smallest set of outside observations needed to anchor the rest.

=== VALUED C04 ===
ANCHOR: SNF pi-groups validated by cross-scale transfer
NAME: Scale-Falsified Dimension Learner
MECHANISM: For any numeric inputs, including tabular or sensor data with no units, the model learns integer dimension assignments. Smith normal form turns them into dimensionless groups, and the predictor can see only those groups. The training signal is cross-scale transfer on real data: a law fitted on one magnitude band must predict another band unchanged, because the world, not the model, supplies the variation in scale. If transfer fails while the in-band fit holds, SNF adds a base dimension that separates the offending groups, and the test is run again. The dimensional structure is therefore discovered from the data and keeps getting falsified by it, rather than being given by hand.
VALUE: Engineers and scientists scaling from lab to plant, or from simulation to field, get models that extrapolate far outside the training range and report when their notion of "same kind of quantity" has broken.

=== VALUED C05 ===
ANCHOR: least-squares adjustment of conservation ledgers
NAME: Adjusted-Ledger Working Memory
MECHANISM: The model's working memory is a ledger of quantities: objects, money, people, stock and allocated resources. Every conservation identity it implies is a condition equation, and the model reads state only from the least-squares-adjusted ledger, never from raw recall. Baarda w-tests separate "blunder at step k" (a local residual) from "hidden holder h" (a pattern shared across loops). A holder is admitted only if it is significant and lowers other claims' minimal detectable bias. Variance-component estimation learns how strictly each identity holds. The identities are structural rather than judged by the model, and redundancy numbers mark every unchecked claim, for which the agent requests one external count.
VALUE: Agents doing long-horizon bookkeeping, logistics, case files or multi-day tasks keep a state that stays consistent and can name the wrong step or the missing participant, with a confidence for each verdict and a list of what it cannot check.

=== VALUED C06 ===
ANCHOR: decorrelated cascade calibrated by contradiction pairs
NAME: Contradiction-Calibrated Reasoning Cascade
MECHANISM: Each reasoning step is generated by passing through stages that are the model's own re-encoding blocks. A step is discarded irreversibly with a probability that rises as its binding margin falls. The training signal is oracle-free: each step is paired with a sampled alternative that contradicts it, and the stages are trained to minimize how often both survive. That rate is a lower bound on the false-pass rate, so stages that fail together are pushed apart in training, not just swapped out. At inference the measured per-stage rate sets each step's cascade depth from a user-specified target error and from how much downstream work depends on that step.
VALUE: People running long proofs, plans or agent workflows get a reliability dial: they set a target error rate, and the system measures its own pass rates and spends compute only where the measurements say it is needed.

=== VALUED C07 ===
ANCHOR: ensemble Kalman assimilation with innovation statistics
NAME: Ensemble-Weight Assimilating Memory
MECHANISM: Knowledge-bearing weights are stored as a mean plus about 64 low-rank anomaly directions, so the ensemble is cheap. Assimilation replaces fine-tuning as the way new facts get in: the gain comes from parameter-prediction cross-covariance with a learned locality taper. Before a fact is written in, its innovation is gated against ensemble spread plus the source's error variance. Desroziers statistics over many facts estimate each source's error variance and the cross-source error covariance, so correlated sources are not double-counted. Facts that fail the chi-square gate are quarantined. The ensemble spread at inference gives calibrated uncertainty on every answer.
VALUE: Newsrooms, clinical-guideline systems and intelligence desks get a model that absorbs live feeds and corrections every day without retraining or forgetting, learns how far to trust each source, and says how sure it is.

=== VALUED C08 ===
ANCHOR: rigidity matrix: floppy modes and self-stress
NAME: Rigidity-Governed Knowledge Framework
MECHANISM: Concepts are embedding points. Each fact is a learned constraint function on them, not only a distance, and the generalized rigidity matrix (the Jacobian of all constraints) is maintained incrementally by sparse factorization as the model's knowledge store. Floppy modes trigger a query along exactly that direction, and an answer is accepted only if it removes the mode without adding stress. Self-stress is counted as evidence only among constraints from independent sources, so constraints the model generated itself can never cross-check each other. Concentrated stress retracts a fact, and stress that splits into two rigid, stress-free blocks splits the concept in two.
VALUE: Knowledge-base builders, tutors and research agents get a model that asks the one question that pins down an ambiguous concept, and can show which facts are cross-checked and which are not.