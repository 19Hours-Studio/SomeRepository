GOALS (chosen for importance, not originality):
1. Learning continually after deployment without damaging what the model already knows.
2. Long chains of reasoning that find and pin down their own errors.
3. Knowing how much it does not know, meaning when a search for facts, cases or solutions is actually complete.

PARADIGM NEGATED: Mainstream systems get every ability from one fixed-weight network, trained by gradient descent and run as a forward pass over a context window. That is forbidden as the mechanism.

PERIPHERY PORTS:
- Goal 1 comes from weather data assimilation. Forecasting centers feed millions of observations into a huge model state every few hours without restarting it.
- Goal 2 comes from geodetic surveying. Least-squares network adjustment, together with Baarda's data snooping, finds blunders in measurements that should agree.
- Goal 3 comes from wildlife ecology. Capture-recapture and Chao estimators work out the size of a population that has not been seen yet.

HONESTY CHECK:
- Idea 1: the closest work is Ensemble Kalman Inversion for neural-network training (Kovachki and Stuart, 2019) and low-rank Kalman filters for online learning (Chang et al., 2022). The new parts are learned covariance localization as the explicit guard against interference, plus inflation as plasticity control for editing knowledge.
- Idea 2: the closest work is self-consistency voting and loop closure in pose-graph SLAM. Neither computes redundancy numbers or runs blunder tests on chains of reasoning claims, so this is kept.
- Idea 3: the closest work is semantic entropy (Farquhar et al., 2024) and Good-Turing arguments about hallucination (Kalai and Vempala, 2024). Those measure uncertainty or prove bounds. Neither estimates the unseen remainder while the system is running, so this is kept.

FIRST THOUGHTS:
- Neuro-symbolic program synthesis over a library of skills
- Latent world model plus tree-search planning
- Episodic memory plus sleep-like consolidation
- Energy-based iterative reasoning with a verifier
- Mixture of experts routed by uncertainty

=== IDEAS ===
IDEA 1
NAME: Assimilated Knowledge Ensemble
MECHANISM: The system keeps about 64 copies of a "knowledge state", which is a subset of its parameters. Each new fact or correction is handled as a weather-style observation. The update gain comes from the copies' cross-covariance between parameters and their predictions of that fact. A learned taper limits the update to parameters close to the fact in concept space, which stops a new fact from overwriting distant ones. When the copies agree too much, they are spread apart again so the system can keep learning.
VALUE: The system can absorb a stream of new facts and corrections, each with a real confidence level, without retraining, and without the long-range damage that causes forgetting.

IDEA 2
NAME: Survey-Adjusted Reasoning Networks
MECHANISM: Each intermediate claim is a "station" that is derived along at least two independent routes, so the routes form closed loops. Each loop has a computed mismatch (misclosure). A least-squares adjustment spreads small mismatches across the loop, and Baarda's w-test singles out the one derivation step that is a blunder. Each claim gets a redundancy number. Any claim with a value near zero is unchecked, so the planner deliberately adds a new route to it before answering.
VALUE: Long chains of reasoning check themselves. The system can say which step is wrong and which conclusions nothing has verified yet.

IDEA 3
NAME: Capture-Recapture Ignorance Estimator
MECHANISM: For a given query, the system runs several retrieval or generation passes that are deliberately independent, each using different cues, sources or decompositions. It records which candidate facts or solutions each pass "captures". From the overlaps it computes Chao or Lincoln-Petersen estimates of how many relevant items are still missing, adjusting for the fact that some items are easier to capture than others. It keeps sampling until the estimated unseen share falls below a set threshold, and its answer states how complete it is.
VALUE: The system can say "I have probably found 90% of the relevant cases" and know when to stop searching.