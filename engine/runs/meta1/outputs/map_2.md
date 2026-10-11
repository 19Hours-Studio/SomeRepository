The three changes target the pipeline's measured weaknesses directly: low value, crossover losing concreteness, validity handed to an outside verifier, judges sharing the generators' blind spots, high run-to-run variance and new families appearing at every layer.

The first change puts value before generation. Right now ideas are generated first and their value is judged afterwards, which is why value ends up below plain answers. Grounding every idea in a documented, costed problem pins value down before any originality pressure is applied.

The second change stops trusting judge opinion on validity. Each idea has to carry checks the pipeline can run on itself, so the score comes from evidence. This also gets around the problem of judges sharing the generators' knowledge gaps, and it gives crossover typed parts to recombine.

The third change makes originality measurable across runs. A persistent archive and a forecaster turn "new" into "not predictable from everything seen before". Using replicate runs for selection stops the pipeline from chasing noise.

=== IDEAS ===
IDEA 1
NAME: Problem-Card First Inversion
MECHANISM: Move the literature stage to the front. A scout agent searches the web for documented, specific unsolved failures ("problem cards"), each with evidence of who it hurts and the cost. Attractor mapping and all five techniques then run per card, and every answer must name the card and the cost it reduces. Value is scored against that stated cost rather than in the abstract. Cards are kept between runs as solved, partial or open, and the scout gives priority to open cards that keep coming back.
VALUE: Originality pressure works inside a value frame that is already anchored, so unusual ideas stop trading away usefulness.

IDEA 2
NAME: Executable Claim Contracts
MECHANISM: Each idea must come with a contract: typed slots (input, operation, stored state, feedback loop) plus 2-3 falsifiable checks the pipeline can run itself. Examples of checks: a search query with a predicted hit or no-hit, a Fermi estimate, or a small code simulation. A verifier agent with web and code tools runs the checks, and the score uses pass rates and evidence instead of judge opinion. Crossover swaps slots between parents. A child survives only if a compatibility checker accepts the combined slots and the child keeps at least one passed check from each parent.
VALUE: Validity gets tested inside the pipeline rather than handed to an unspecified verifier, and crossover offspring stay concrete because they are built from verified parts.

IDEA 3
NAME: Forecast-Surprise Archive with Replicates
MECHANISM: Keep a persistent cross-run archive of every family and every idea, recording the layer where each family first appeared. Before a run, a forecaster agent reads the archive and the question and predicts the likely families. Originality is then scored as forecast failure plus distance from the nearest archive entry, not as a judge's raw impression. Families that first appeared in late layers are added to the next run's forbidden list from layer 1. Each configuration runs as paired replicates, and a bandit updates the technique weights only when an effect is larger than the measured replicate variance.
VALUE: The pipeline gets a cumulative, measurable novelty baseline, so it stops rediscovering attractors and stops tuning itself on noise.