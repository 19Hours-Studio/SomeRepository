**Loop 1: genetics, complementation test.** When two mutants share a phenotype, geneticists cross them. If the offspring is normal, the defects sit in different genes; if not, both hit the same unit.
- **Port:** Treat two observed failures as two "mutants." Patch the internal state of each failure into the other's run. If the combined run does not recover, the two failures share one functional unit.
- **Loop:** A unit that collects failures from unrelated task families gets split, and its downstream connections are re-assigned according to the complementation groups.
- **Honesty:** The closest work is activation patching and causal scrubbing, which only report. Mixture-of-experts routing is learned, not driven by a diagnostic.

**Loop 2: thermochemistry, cycle closure.** In free-energy perturbation networks, energy changes around any closed cycle must sum to zero. A nonzero sum points to the inconsistent edge.
- **Port:** The model learns transformation maps between concepts or contexts. It computes the cyclic (curl) part of these maps with a Hodge decomposition.
- **Loop:** Persistent curl on a cycle means some concept is being treated as one thing when it is two. The system adds a new context dimension and splits that concept along it, so each sub-cycle closes.
- **Honesty:** The closest work is HodgeRank and cycle-consistency losses. Both penalise curl; neither turns it into a change in what kind of thing a concept is. Prediction error does not trigger it, so it stays distinct from CAUSGR.

**Loop 3: metrology, Gauge R&R.** Gauge repeatability-and-reproducibility studies split the variance of a measurement into the instrument, the operator and the part being measured. A gauge with GRR above 30% is rejected.
- **Port:** Each internal feature is treated as a gauge. Its variance is split across stochastic re-runs (instrument), paraphrases or surface form (operator) and true content (part).
- **Loop:** A feature that fails GRR is re-typed as a nuisance channel. Downstream reads move to a rebuilt feature fitted only on the part-variance component.
- **Honesty:** The closest work is invariance learning, IRM and disentanglement. Those are training objectives; this is a per-feature audit that rewires the network's structure.

=== IDEAS ===
IDEA 1
NAME: Complementation-Driven Module Fission
MECHANISM: Failures are logged as "mutants," and pairs are crossed by swapping internal states between their runs. Pairs that fail to recover are grouped as sharing one unit. A unit that holds failures from unrelated groups is split and its connections are reassigned. The stored complementation table grows over time and guides later splits.
VALUE: The modular structure follows the real fault lines of what the model can and cannot do, so a fix in one place does not break something else.

IDEA 2
NAME: Curl-Triggered Concept Splitting
MECHANISM: The model learns transformation maps between concepts and contexts. It decomposes them by Hodge decomposition to find cycles whose sum is not zero. Where curl persists, it adds a new latent context dimension and splits the concept along it until the cycles close. The split concepts are stored with the cycle that triggered them.
VALUE: The model finds ambiguities it was not told about and gives each meaning its own concept, instead of averaging two incompatible ones.

IDEA 3
NAME: Gauge-R&R Feature Auditing
MECHANISM: Each feature's variance is split into run-to-run noise, surface-form variance and content variance. Features above a GRR threshold are re-typed as nuisance channels. Downstream reads move to rebuilt content-only features, and GRR scores are stored and checked again over time.
VALUE: Reasoning runs only on features shown to measure content, which removes failures caused by sensitivity to phrasing.