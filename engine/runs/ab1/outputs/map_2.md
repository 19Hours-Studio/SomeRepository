Today's LLMs have three structural gaps: their weights are frozen after training, they only predict correlations without running causal models, and they have no stored record of where their own outputs fail. Each proposal below targets one of these gaps by adding a different computational substrate, not a bigger transformer.

**1. Learning during life without forgetting.** A fast episodic store records surprising experiences verbatim. Offline "sleep" cycles replay them and try out candidate weight updates in a sandboxed copy of the model. An update is committed only if it passes an automatically maintained regression suite of the system's past competencies. The result is a model that keeps learning after deployment, with forgetting caught by an explicit check rather than hoped away.

**2. Reasoning by simulation, not by text continuation.** The system keeps a competing population of small executable programs, each a candidate simulator of some part of the world. It answers questions by running these simulators forward or intervening on them. Mismatches between predicted and observed outcomes drive program-synthesis edits, and simulators that keep failing to predict are culled. This gives genuine counterfactual and causal reasoning, and the discovered models can be inspected.

**3. Knowing where it is competent.** A learned map records the system's verified error rate for each region of problem space. The map is updated whenever an outcome is checked against ground truth. It is consulted before every answer to decide whether to answer, abstain, gather more information or trigger learning. This grounds calibration in the system's own track record instead of in fluent-sounding confidence.

=== IDEAS ===
IDEA 1
NAME: Audited Sleep Consolidation
MECHANISM: Surprising experiences go verbatim into a fast episodic buffer. During offline phases the system replays them to propose weight deltas inside a sandboxed copy of its slow network. Each delta is accepted only if a self-maintained regression suite of past skills shows no loss, and rejected deltas are stored as interference records that shape later proposals.
VALUE: It enables continual lifelong learning after deployment without catastrophic forgetting.

IDEA 2
NAME: Evolving Executable World Simulators
MECHANISM: The system maintains a population of small probabilistic programs, each a candidate simulator of some part of the environment. Queries are answered by running or intervening on the best-scoring simulators. Prediction errors drive program-synthesis mutations, and simulators are selected by how well they compress observations and predict accurately.
VALUE: It gives explicit causal and counterfactual reasoning and lets the system discover new models that can be inspected.

IDEA 3
NAME: Verified Competence Cartography
MECHANISM: An embedding-indexed map stores the system's ground-truth-verified error statistics for each region of problem space, updated whenever an outcome is checked. Before answering, the system looks up the query's region. It then answers, abstains, asks for information, or routes the region to the learning loop, depending on the measured reliability and the cost of being wrong.
VALUE: It gives reliable self-knowledge of where the system is competent, so it can abstain and direct its own learning based on its actual track record.