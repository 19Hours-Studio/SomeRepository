All three ideas tackle the core problem the same way: the correctness signal comes from structure the system builds itself, so the same model never grades its own answers.

**1. Gross-error test from chemical-plant data reconciliation.** Plants estimate each flow from redundant sensors. A chi-square test on how far the mass balances fail to close, plus a per-sensor test, shows which sensor is faulty. Here, every quantity is derived along at least two paths that share no sources. The test picks out which path (a module or source) is to blame, and that path is retired, split by context or retyped. Closest existing work is self-consistency voting and truth maintenance. This differs because the residual is quantitative, the faulty path is pinpointed statistically, and the result is rewiring rather than retracting a belief.

**2. Capture-recapture from ecology.** Ecologists estimate how many animals were never caught from how much independent samples overlap. Here, the samples are critics trained on separate views of the data. The estimated number of errors nobody caught in each region drives creating new critics and deleting redundant ones. Closest existing work is capture-recapture defect estimation in software inspection (Eick et al., 1992). That only reports a number; here the number changes the architecture.

**3. Standard addition from analytical chemistry.** Chemists add known amounts of a substance to a real sample, and recovery below 100% reveals interference from the sample itself. Here, perturbations whose correct effect is known by construction are injected into live inputs. Closest existing work is metamorphic testing and needle-in-a-haystack probes. Those are offline pass/fail tests. This one runs on real inputs, corrects estimates by extrapolation and grows adapters.

=== IDEAS ===
IDEA 1
NAME: Reconciliation-Driven Derivation Pruning
MECHANISM: Every quantity or claim the system asserts is computed along several derivation paths that share no sources, linked by arithmetic, unit and accounting identities. Weighted least squares adjusts the estimates so the identities hold, a chi-square test checks how far they fail to close, and a per-path test isolates the path most likely to carry a gross error. That path is retired, given a learned bias term, or split by context where its errors cluster. Agreement between independent paths under fixed identities is the correctness signal, so no oracle or self-judgment is needed.
VALUE: Faulty knowledge sources can be found and repaired in open domains without ground truth.

IDEA 2
NAME: Capture-Recapture Blind-Spot Growth
MECHANISM: Several critics trained on disjoint views of the data flag suspected errors in the system's outputs. A latent-class capture-recapture model fits the overlaps between their flags and estimates each critic's false-flag rate, how strongly the critics depend on each other, and how many errors went uncaught in each input region. Where the estimated uncaught errors are high, the system trains a new critic on a fresh disjoint view. Where critics have become too similar, it retrains one of them to make them independent again, and it deletes critics whose catches the others already cover.
VALUE: The system can measure what it fails to notice and grow detectors exactly there, without an oracle.

IDEA 3
NAME: Standard-Addition Matrix Calibration
MECHANISM: The system injects graded perturbations into live tasks, and the correct effect of each one is known by construction: inserted facts with fixed consequences, unit rescalings, swapped entities, planted sub-results. It fits a line of output shift against spike size. The slope gives recovery for that input type, and extrapolating the line to zero spike gives a bias-corrected answer. Input types with low or uneven recovery get their own adapter modules, and an adapter is deleted if recovery does not improve. The system only grades known differences, never its own absolute answers.
VALUE: Context-specific distortions are measured and corrected on real inputs where no answer key exists.