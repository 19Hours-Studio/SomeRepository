=== VALORIZED V01 ===
ANCHOR: Hodge split of derivation-loop misclosure
NAME: Hodge-Audited Claim Graph
MECHANISM: Claims are nodes and derivations are transformation edges. A Hodge decomposition splits the misclosure of every loop into three parts: a curl part (local, so the faulty step can be found with a w-test), a harmonic part (global, so it is either a mistake or a real frame split), and a gradient part (systematic offsets that no loop can see). The harmonic part gets bridging derivations, each chosen by minimal-detectable-bias and taken from a different source than the loop it crosses (tool, retrieval, model). If the misclosure collapses, it was a mistake. If it survives every bridge, a context variable splits the frames. The crux is handled by the decomposition itself: the gradient subspace is exactly what the system cannot grade by itself, so the system never trusts it and spends external observations ("control points") only on the nodes that span it.
VALUE: The system can find and classify its own reasoning errors with no oracle, and it can say exactly which beliefs only outside evidence can check.

=== VALORIZED V02 ===
ANCHOR: Ensemble Kalman assimilation of facts
NAME: Self-Calibrating Knowledge Assimilation
MECHANISM: About 64 ensemble copies of a parameter subset take each new fact as an observation, with a gain built from parameter-prediction cross-covariance and a learned locality taper so that distant knowledge is untouched. Before a fact is assimilated, it is used as an honest forecast test: its innovation (observed minus ensemble-predicted) is compared against the ensemble spread plus that source's error variance. Desroziers-style innovation statistics, gathered over many facts, estimate each source's error variance online, so unreliable sources are down-weighted automatically, and a fact that fails the chi-square gate is quarantined instead of written in. The correctness signal therefore comes from prequential consistency between independent future observations and prior forecasts, not from the model judging itself.
VALUE: The system can keep absorbing streams of facts and corrections from sources of unknown reliability, learning how far to trust each one, without retraining and without forgetting.

=== VALORIZED V03 ===
ANCHOR: Learned kind-exponent vectors, imbalance residual
NAME: Falsifiable Learned Kind Algebra
MECHANISM: Every internal quantity carries an integer exponent vector over learned base kinds. Multiplication adds the vectors, and addition or comparison requires them to match, so an imbalance is computed by exact integer arithmetic, not by a learned judge. The model only proposes kind assignments. These are scored against expressions people actually write in corpora, tables and spreadsheets (external data the model did not produce), and the score maximizes the number of syntactically possible combinations the kind system forbids while keeping zero imbalance on observed expressions. This stops the trivial "everything is one kind" solution. A persistent imbalance creates a new kind or a conversion constant, and a kind that forbids nothing is merged away.
VALUE: Nonsensical reasoning steps are rejected by an exact check that the fallible model cannot argue its way around, and magnitudes extrapolate through scaling rules.

=== VALORIZED V04 ===
ANCHOR: Prediction only through Buckingham-pi groups
NAME: Cross-Scale Dimensionless Predictor
MECHANISM: Quantities carry integer dimension exponents, and Smith normal form over them yields the dimensionless groups. Every prediction is a learned function of those groups only. The correctness signal is cross-scale transfer on real data: a pi-law fitted on one magnitude band must predict observations in another band unchanged, because the world, not the model, supplies the variation in scale. If transfer fails while the in-band fit holds, the dimension assignment is wrong. SNF then adds a base dimension that separates the offending groups, and the scale test is re-run.
VALUE: The system can extrapolate far outside its training range, with a built-in falsification test whenever its notion of "same kind of quantity" is wrong.

=== VALORIZED V05 ===
ANCHOR: Ledger balances as surveying condition equations
NAME: Geodetic Adjustment of World-State
MECHANISM: Every conservation identity in a narrative ledger becomes a condition equation in a least-squares adjustment. Baarda w-tests then decide between "blunder at step k" (a local residual) and "hidden holder h" (a shared pattern across loops), and a holder is admitted only if it passes significance and lowers other claims' minimal detectable bias. The conservation identities act as the oracle because they are structural, not judged by the model. Variance-component estimation learns per quantity how strictly conservation actually holds. Redundancy numbers mark the claims that no identity checks, and only for those does the planner request or derive one extra external count.
VALUE: The system can track world state over very long texts, saying which step is wrong or which unmentioned participant must exist, with a confidence for each verdict and an explicit list of what it cannot check.

=== VALORIZED V06 ===
ANCHOR: Sequential decorrelating stages, binding margin
NAME: Exclusive-Pair Calibrated Commit Cascade
MECHANISM: Each candidate step passes n stages of increasingly decorrelated re-encoding, and it is discarded irreversibly with a probability that rises as its binding margin falls. The true per-stage false-pass rate is measured without an oracle by also pushing mutually exclusive step pairs through the cascade (the step and a sampled contradicting alternative). At most one of each pair can be true, so the fraction where both survive gives a lower bound on false-pass. Comparing that fraction stage by stage exposes correlated stages, which are replaced with more distant re-encodings. n is then set from the measured rate, not the assumed ε^n, and scaled by how much downstream work depends on the step.
VALUE: Long reasoning chains get a calibrated, self-measured reliability dial instead of compounding errors or overconfident self-verification.

=== VALORIZED V07 ===
ANCHOR: Rigidity matrix over concept constraints
NAME: Rigidity-Braced Concept Framework
MECHANISM: Concepts are points and facts are geometric constraints, and the system continuously computes the framework's rigidity matrix. Its null space (floppy modes) marks underdetermined concepts, which trigger a query along exactly that direction, and an answer is accepted only if it removes the mode without creating stress. A state of self-stress is the oracle-free error signal. If the stress concentrates on one constraint, that fact is retracted. If it splits the constraints into two groups that are each rigid and stress-free, the concept is split in two. Facts in redundant, stress-free regions are trusted because they are cross-checked; facts in floppy regions are explicitly unverified.
VALUE: From geometry alone, the system can tell where its knowledge is wrong, ambiguous or unverified, and repair each case structurally.

=== VALORIZED V08 ===
ANCHOR: Lesion complementation crosses
NAME: Complementation-Mapped Modular Network
MECHANISM: Small parameter lesions that change a behavior are paired and "crossed" by mixing activations between the two lesioned copies. Restoration means separate functional units and no restoration means the same unit, and the resulting groups re-partition and re-route the parameters. The reference phenotype is the intact model's own output, not a correct answer, so module discovery needs no oracle. A proposed fix for an externally flagged failure is accepted only if it complements the lesions of exactly one group and leaves behavior on the other groups' probes unchanged. The anchor cannot say what counts as a failure (that one flag stays external), but it makes localization and side-effect checking oracle-free.
VALUE: The system's module structure comes from functional evidence, so fixes, transfer and growth stay local and their side effects can be verified.