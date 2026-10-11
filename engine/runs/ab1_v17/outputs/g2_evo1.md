**Pair 1. Shared move:** a claim is judged by what it does to the fit of independent data, not by how plausible it looks. Offspring: make one two-sided edit and score it against raw data. Closest work: knowledge editing (ROME), influence functions and Toolformer's loss-reduction filter. None of these compares a claim with its negation on held-out raw data to decide whether the claim is true, so this is a different use.

**Pair 2. Shared move:** errors are estimated only from differences (innovations, spikes), never from absolute answers. Offspring: if a learner is updating optimally, its future surprise cannot be predicted from its past surprise. Closest work: Mehra's innovation-whiteness adaptive filtering and hypergradient learning rates. I mutated it to cross-lagged attribution, which pins the error on a specific source and region.

**Pair 3. Shared move:** a grade only counts if the graded component never saw the evidence (extrinsic messages, future data). Offspring: seal a prediction before every lookup. Closest work: Toolformer, outcome-based forecasting RL and next-token pretraining. The difference is grading at inference time, against tool results, within seconds, with no resolver design and no wait for future data.

=== IDEAS ===
IDEA 1
NAME: Claim-Versus-Negation Edit Contrast
MECHANISM: For each claim, the system makes two small weight edits: one that asserts the claim and one that asserts its negation. It then measures how well each edited model predicts a held-out stream of raw data (documents, logs, sensor records) that was not used for the edit. The difference in log-likelihood, compared against a null distribution from edits of random claims, is stored as the claim's support. Claims the world prefers are consolidated, and claims whose negation predicts better are retracted. Claims that sit inside the null band are labelled "uncontrolled by any data" rather than trusted.
VALUE: Unlabeled raw data, not the model's opinion, decides whether each belief is right, wrong or unverifiable.

IDEA 2
NAME: Predictable-Surprise Gain Correction
MECHANISM: The system logs its surprise (log-loss) on every incoming datum, tagged by source and knowledge region. It continuously regresses each region's later surprise on earlier surprises from each source. A positive lagged correlation means that source was under-weighted; a negative one, where the model was misled and corrected later, means it was over-weighted. These coefficients directly set the per-source trust weights and per-region learning rates, which are adjusted until the surprise sequences become unpredictable.
VALUE: The system learns continuously from untrusted streams and calibrates its own plasticity and each source's reliability from the stream alone, with no labels.

IDEA 3
NAME: Sealed Pre-Lookup Wagers
MECHANISM: Before every retrieval, calculator call, database query or sensor read made during ordinary work, the system hash-commits a probability distribution over the result. The returned value settles the wager immediately. Parametric weights are trained only on these settled log-scores, never on answers the system grades itself. Log-scores are also stored per topic and tool, giving a running, tamper-proof record of where its memory can be relied on.
VALUE: Every action the system takes in the world becomes a correctness signal it cannot fake, so it gets millions of uncontaminated grades a day instead of waiting months for the future to arrive.