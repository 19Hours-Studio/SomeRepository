GOALS (from the center)
1. Reliable multi-step reasoning: keep errors from compounding over long chains.
2. Continual learning: learn new skills after deployment without losing old ones.
3. Few-shot concept acquisition: pull a new concept out of a handful of noisy examples.

PARADIGM NEGATED
Mainstream approaches share one paradigm: a single fixed function, fit by gradient descent on static data, then run feedforward at inference. That is forbidden as a mechanism.

MECHANISMS FROM THE PERIPHERY
- Goal 1 comes from molecular biology. Kinetic proofreading (Hopfield/Ninio) lets ribosomes and polymerases reach an error rate of about ε^n, far below what a single binding step could give, by spending energy on irreversible delay stages.
- Goal 2 comes from evolutionary genetics. Gene duplication with degeneration-complementation (DDC) is how genomes gain new functions without losing old ones.
- Goal 3 comes from experimental physics. The lock-in amplifier recovers signals buried far below the noise by modulating the stimulus with a known reference and integrating the correlation.

HONESTY CHECK
- Idea 1: the closest work is self-consistency voting and verifier reranking. This idea differs because each step passes through a sequential, irreversible cascade of discards with a set energy budget, so error falls geometrically. It is not a parallel vote.
- Idea 2: the closest work is splitting steepest descent (Liu 2019), Progressive Nets, and MoE growth. This idea differs in two ways. A split is triggered by a conflict with a stored functional signature of old behavior. Both copies are then forced to degenerate in complementary ways, so the old behavior is kept jointly rather than by freezing.
- Idea 3: the closest work is activation patching and steering vectors. This idea differs because a pseudo-random code modulates the inputs continuously during operation, and per-channel integrators detect the concept at very low SNR. It is not a one-shot contrast.

FIRST THOUGHTS:
- Latent world model with planning over imagined rollouts
- Neurosymbolic program synthesis over a library of programs
- Episodic memory with sleep-like consolidation
- Energy-based iterative reasoning until a verifier passes
- Curiosity-driven self-play curriculum

=== IDEAS ===
IDEA 1
NAME: Kinetic Proofreading Reasoning Cascade
MECHANISM: Each candidate reasoning step gets a "binding margin": how strongly it is re-derived when the context is re-encoded in a different way. The step then passes n sequential stages, and at each stage the context decorrelates further (paraphrase, dropout, abstraction). The chance of being discarded rises as the margin falls, and a discarded step cannot be restored. Only steps that survive all n stages are committed, so the error rate falls roughly as ε^n. The system adapts n, the compute it spends, to how much downstream work depends on the step.
VALUE: Long chains can be made as reliable as needed, with an explicit dial between speed and accuracy, instead of errors compounding.

IDEA 2
NAME: Duplication-Degeneration Skill Growth
MECHANISM: Each module stores a compact functional signature: its input-output behavior on a probe set. When the gradient from new data conflicts with that signature beyond a threshold, the module is duplicated rather than overwritten. Both copies then receive complementary sparse degeneration masks, so each loses a different subset of sub-functions while the pair together still reproduces the old signature. The new copy specializes on the new data. Copies that end up redundant are pruned.
VALUE: New capabilities can grow after deployment, with old ones preserved in the network's structure rather than by penalties or replay.

IDEA 3
NAME: Lock-In Concept Extraction
MECHANISM: To learn a new concept from a few examples, the system modulates the hypothesized feature (present or absent, at varying strength) across its inputs following a pseudo-random reference code. Per-channel integrators multiply each internal activation by the reference and low-pass the product, which pulls out the channels coherently locked to the concept even far below the noise. The locked channel set becomes a durable address for the concept. A new code then re-tests the address, and channels whose lock fades are dropped.
VALUE: Concepts can be isolated precisely from very few, noisy examples, with a signal-to-noise level that can be measured.