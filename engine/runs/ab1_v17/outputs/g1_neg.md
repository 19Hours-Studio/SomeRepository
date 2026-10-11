**The 12 answers I would propose first:**
1. A neurosymbolic reasoner with a theorem-prover checker.
2. A latent world model used for planning.
3. A continual learner with episodic memory.
4. A causal-graph learner.
5. A library of synthesized programs.
6. An embodied active-inference agent.
7. A routed mixture of experts with a compute market.
8. A metacognitive uncertainty calibrator.
9. Fast-weight plasticity.
10. A global workspace.
11. Hyperdimensional binding.
12. Curiosity-driven self-play.

**The paradigm they share:** a single agent improves itself by comparing its own internal model against error signals that it generates or checks itself.

I forbid that paradigm, all 12 answers, anything adjacent to them, and the listed families. What remains has to get correctness from structure the model cannot write: time, independence between sources of evidence, and planted ground truth.

=== IDEAS ===
IDEA 1
NAME: Time-Sealed Commitment Escrow
MECHANISM: The system turns each belief into a falsifiable prediction about future raw data streams, such as sensor feeds, registries, prices or archives. It hash-commits the prediction together with a resolver: a small, deterministic parsing predicate frozen at commit time. Weights may learn only from predictions that have matured, and each one is scored by its frozen resolver against data that did not exist when the model made the claim. The escrow ledger stores calibration per domain and per horizon, and resolvers that drift or turn out ambiguous are retired.
VALUE: The current model cannot shape its own grade, because the world settles the score later through a judge fixed before the outcome existed.

IDEA 2
NAME: Triangulated Independent-View Accuracy
MECHANISM: Three or more predictor lineages are trained on disjoint evidence channels about the same events, such as text reports, numeric logs and imagery. The channels are chosen so that their errors are conditionally independent. From the pairwise and three-way rates at which the lineages agree, a latent-class (Dawid-Skene-style) estimator recovers each lineage's accuracy per region without any labels. The system trains only on events where the triangulated posterior is confident. It runs higher-order agreement tests to detect when independence has broken down and then splits or reroutes channels.
VALUE: It gives label-free, mathematically identifiable accuracy estimates in open domains, derived from how independent views agree rather than from any one model judging itself.

IDEA 3
NAME: Planted-Canary Capture-Recapture
MECHANISM: The system corrupts known-true items to create canary errors whose falsehood it knows by construction, and mixes them into its normal stream of claims. Two error-detection procedures with different mechanisms flag suspect claims. Their catch rates on canaries measure each procedure's recall. The overlap of their real-error catches, combined with that recall, gives a Lincoln-Petersen estimate of how many errors went undetected in each domain. The canary generator adapts its corruptions so that, statistically, canaries cannot be told apart from the real errors detected so far. Learning budget goes to domains whose estimated hidden-error mass is largest.
VALUE: The system can measure the errors it has not caught, using ground truth it planted itself, instead of trusting its own sense of being right.