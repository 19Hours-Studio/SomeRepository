**1. Action first.** I listed the structural changes a system could undergo and struck the forbidden ones (split, merge, partition, brace, add capacity or timescales). What remained: delete, revert, quarantine, change coordinate chart, invert, go dormant, graft, recalibrate, break symmetry. I chose three that mainstream AI work almost never triggers automatically:
- (a) change of coordinate chart
- (b) reverting one specific learned update
- (c) quarantining a knowledge region

**2–3. Trigger search, port and close.**

**(a) Celestial mechanics.** N-body integrators measure how close two bodies are, or how badly the equations are conditioned. Below a threshold they switch to Kustaanheimo–Stiefel regularized coordinates and rescale time (Sundman transform, dt = r·ds).
- **Port:** during multi-step latent reasoning, compute κ, the condition number of the step map's Jacobian.
- **Threshold:** if κ > κ*, jump to whichever stored invertible chart gives the lowest κ, and set step size proportional to 1/κ.
- **After many firings:** an atlas of charts with learned transition maps, concentrated where reasoning is singular.
- **Closest existing work:** chart-autoencoders and adaptive-step neural ODEs. Neither switches charts on conditioning at inference time.

**(b) Pharmacovigilance.** Regulators compute a proportional reporting ratio (PRR). Under the Evans criteria a signal fires when PRR ≥ 2, χ² ≥ 4 and n ≥ 3, which can lead to a label change or withdrawal.
- **Port (outward):** every learned weight update has a provenance ID. "Adverse events" are user corrections, re-asks and abandoned sessions in interactions that the update influenced.
- **Measure:** PRR of adverse events for each update against all other updates.
- **Action:** when the signal fires, subtract that update's weight change. The PRR sets how much is subtracted (partial to full).
- **After many firings:** a lineage of surviving updates that users have validated over time.
- **Closest existing work:** MLOps rollback and machine unlearning. Neither uses per-update disproportionality from field reports.

**(c) Epidemiology.** Agencies estimate the effective reproduction number R_t from case series and generation intervals, then impose quarantine.
- **Port (outward):** track claims the system emitted that come back to it later (pasted into new prompts, cited in documents). When a claim is shown wrong, compute R_t for its embedding region from those re-entries.
- **Threshold:** if R_t > 1, seal the region so it cannot generate without a fresh external source. Quarantine length = generation interval × log(R_t).
- **After many firings:** a map of sealed and unsealed regions that follows how the system's errors spread among its users.
- **Closest existing work:** misinformation-spread models on social networks. None feeds back into the AI system's own architecture.

**4. Outward readings.** Ideas 2 and 3 measure interaction with users over time, which meets the "at least half" rule.

**5. Honesty check.** The closest work for each idea is named above. None of the three is essentially that work, so I kept all three fields.

=== IDEAS ===
IDEA 1
NAME: Conditioning-Triggered Chart Switching
MECHANISM: During latent multi-step reasoning, the system computes the condition number of its step map's Jacobian. When it crosses a threshold, the system switches to a stored invertible reparameterization (a chart) and rescales its step size as celestial mechanics does with KS regularization. New charts and transition maps are learned where singularities keep recurring, building an atlas.
VALUE: Reasoning stays stable through near-singular regions, where today's models silently degrade.

IDEA 2
NAME: Pharmacovigilance Rollback of Updates
MECHANISM: Each weight update carries a provenance ID and is linked to the interactions it influenced. User corrections, re-asks and abandonments count as adverse events. A proportional reporting ratio with the Evans thresholds flags harmful updates, which are subtracted partially or fully in proportion to the signal.
VALUE: A continually learning system can withdraw its own bad lessons, judged by evidence from real use.

IDEA 3
NAME: Error Reproduction-Number Quarantine
MECHANISM: The system tracks how its emitted claims come back to it through user prompts and documents. For refuted claims it estimates R_t in each embedding region. If R_t > 1, the region is sealed for generation-interval × log(R_t), and it may answer only from fresh external sources.
VALUE: The system can contain errors that spread through its users before they turn into consensus it has fed back to itself.