**My 12 most probable first answers:**
1. Latent world model plus planning
2. Neurosymbolic reasoning with program synthesis
3. Explicit causal graphs
4. Episodic memory with consolidation
5. Continual learning without forgetting
6. Energy-based or constraint-satisfaction inference
7. Active inference with embodiment
8. Vector-symbolic binding
9. Curiosity-driven self-play
10. Global workspace
11. Meta-learned plasticity / fast weights
12. Calibrated self-knowledge with abstention and routing

**The paradigm they share:** each one gives a single learner an explicit internal model, memory or controller that it uses to represent, predict and revise its beliefs about the world.

I forbid that whole paradigm, these 12 answers, anything next to them, and the listed families (PROGSYN, CAUSGR, COMPMAP, MODMKT, TMS, CONSOL, ENERGY, WMPLAN, ACTINF, VSA, CURIO, GWS, PLAST).

The three answers below do not change what the system believes. They change other things:
- **Physics of the computation:** it runs reversibly.
- **Who must be able to receive the knowledge:** a learner with no shared state.
- **How evidence is combined:** by signed interference instead of averaging.

=== IDEAS ===
IDEA 1
NAME: Fully reversible uncomputable inference
MECHANISM: Every layer and every reasoning step is a bijection, built from invertible couplings with explicit "garbage" registers, so each output can be run backward exactly to the inputs and training examples that produced it. Learning is done as reversible updates that are logged as compact inverse operations. To forget a datum, or to undo a conclusion, the system uncomputes the matching update chain instead of retraining. Nothing is erased irreversibly, so in principle the system also runs near the thermodynamic limit.
VALUE: Exact, verifiable unlearning and bit-level provenance for any output, which approximate gradient-based models cannot give.

IDEA 2
NAME: Teach-to-retain transmission bottleneck
MECHANISM: A capability counts as kept only if the system can write a short, human-readable lesson that lets a fresh, small, randomly initialized student reach the same behavior within a fixed budget of examples. Anything that cannot be transmitted this way is pruned on each generation cycle, and the surviving lessons become the next generation's training core (iterated cultural learning). The system adapts by changing what it teaches, not by refining a model of the world.
VALUE: Knowledge becomes explicit, portable and auditable by design, and opaque shortcuts that cannot be taught are removed systematically.

IDEA 3
NAME: Phase-interference evidence aggregation
MECHANISM: Every derivation path to a candidate answer contributes a complex amplitude, and the path's phase is set by the assumptions it relies on. Paths that support an answer through incompatible assumptions cancel each other out, while paths that agree reinforce each other. The final confidence is the squared magnitude after summing. The phase assignments are learned, so that recurring conflicting assumption pairs become orthogonal or opposed.
VALUE: The system can represent "many reasons that cancel out" as real uncertainty, which averaging probabilities cannot express, so it stops being overconfident when it has many weak, conflicting justifications.