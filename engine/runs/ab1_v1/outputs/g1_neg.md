**The 12 answers most people would give first:**
1. A latent world model used for planning
2. A neurosymbolic hybrid reasoner
3. Persistent memory with continual learning
4. A causal-graph reasoning module
5. Program synthesis as a way of thinking
6. Energy-based iterative inference
7. Embodied active inference
8. A metacognitive uncertainty monitor
9. Modular experts with learned routing
10. A global-workspace bottleneck
11. Fast Hebbian or plastic weights
12. Self-play driven by intrinsic curiosity

**The paradigm they share:** they all give a single agent the inner parts that cognitive science says a mind has (a model, memory, a reasoner, a controller) and hope new abilities come from that inner structure.

All of that is forbidden, along with anything close to it and the families PROGSYN, CAUSGR, COMPMAP, MODMKT, TMS, CONSOL, ENERGY, WMPLAN, ACTINF, VSA, CURIO, GWS and PLAST. The ideas below instead target abilities that LLMs lack at the substrate level: knowing where a belief came from, conserving information, and producing abstractions that can be passed on to another learner.

=== IDEAS ===
IDEA 1
NAME: Source-Sharded Additive Weights
MECHANISM: Training data is split into hashed provenance shards (one per source or document cluster). Each shard trains its own low-rank weight delta on a frozen base. At inference the deltas are combined additively, with input-dependent coefficients produced by a small probe. That probe is trained on held-out data to predict which shard's evidence an answer actually needs, so each output carries a list of the shards that contributed. A source is removed by deleting its delta, and a disputed fact can be re-checked by switching shards off and seeing whether the answer survives.
VALUE: Knowledge becomes traceable to its sources and exactly removable, so the system can say where a belief came from and forget it on demand without retraining.

IDEA 2
NAME: Reversible Inference with Uncompute
MECHANISM: Reasoning runs on a bijective (invertible-layer) network that keeps the full input-plus-scratch state rather than throwing information away. After producing an answer, the system runs the computation backward from the answer and its stated premises only, then measures how much of the original input it can reconstruct. Low reconstruction means the answer depended on something the premises do not contain, so the gap is surfaced as an unstated assumption. Training penalises those gaps, which pushes the model to make every load-bearing assumption explicit.
VALUE: Hidden assumptions become detectable as missing information rather than through confidence scores, so it becomes visible when a conclusion really depends on something unsaid.

IDEA 3
NAME: Teachability Bottleneck
MECHANISM: An internal concept is kept only if it passes a transmission test. The system compresses the concept into a short message, and a freshly initialised learner with a different architecture, given only that message plus a few examples, must succeed on held-out tasks. Concepts that fail are rewritten or dropped. The surviving messages are stored as the system's vocabulary of abstractions and get re-tested whenever the pool of naive learners is refreshed.
VALUE: The system ends up holding abstractions that are explainable and transferable by construction, rather than private features entangled with one particular network.