**The 12 answers I would propose first:**
1. A learned world model used for planning
2. Neuro-symbolic reasoning modules
3. Persistent episodic memory with consolidation
4. Explicit causal graphs
5. Program synthesis over libraries of simulators
6. Embodied active inference
7. A global-workspace bottleneck
8. Metacognitive uncertainty and calibration maps
9. Vector-symbolic binding
10. Energy-based iterative constraint solving
11. Curiosity-driven open-ended self-play
12. Meta-learned Hebbian or fast-weight plasticity

**The paradigm they share:** all of them add cognitive-science-inspired modules to a single learner, so it builds, stores and revises better internal models in its own head.

I set aside that whole paradigm, those 12 answers, anything close to them, and the 13 listed families. The 3 answers below change other things instead: how the system relates to outside parties, which direction its computation can run, and which inputs it has.

=== IDEAS ===
IDEA 1
NAME: Invertible Abductive Core
MECHANISM: Every layer is an exact bijection, built from coupling flows that carry an explicit "residual" latent that keeps all discarded information, so any computation can be run backward without loss. To answer "what must have been true for X to happen?", the system fixes the output and samples the residual latent while running backward. This gives the full set of inputs that are exactly consistent with X. Because the mapping can be reversed, the system can also take one training example's contribution back out of the weights by applying its inverse update exactly. Approximate fine-tuning is not needed for this.
VALUE: Exact abduction and exact, provable unlearning and provenance, which a forward-only network that discards information cannot provide.

IDEA 2
NAME: Pre-committed Belief Hashing
MECHANISM: Before the system sees evidence or produces a reasoning trace, it must publish a cryptographic hash of its quantized answer distribution, plus a salt, to an external log it cannot change. After the evidence arrives, it reveals the commitment. An independent verifier then checks whether the final answer departs from the committed one more than the evidence statistically justifies. Training penalizes departures without justification and rewards accurate commitments, so the architecture learns to keep "what I believed beforehand" separate from "what I can rationalize afterward".
VALUE: Third parties can check that the system is not rewriting its beliefs after the fact, which is a property no current LLM can prove about itself.

IDEA 3
NAME: Self-Built Instrument Channels
MECHANISM: The input layer has a variable width. When the system cannot reduce its loss on some quantity from its existing inputs, it writes and deploys an external probe: a code instrumentation hook, a sensor configuration, a lab-assay protocol or a database query. Whatever stream the probe produces is attached as a new typed input channel with its own learned encoder. Channels whose removal does not hurt downstream performance are pruned, so over time the system's perceptual alphabet becomes a set of instruments it designed itself.
VALUE: It can perceive and reason about quantities that no human ever chose to give it, instead of being limited to the fixed modalities it was trained on.