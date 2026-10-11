=== VALUED C01 ===
ANCHOR: Schild/pA2 invariants split features
NAME: Receptor-Site Network
MECHANISM: The network's units are binding sites rather than neurons. Each input cue has a learned affinity and efficacy at each site, and a site's output is its occupancy computed from a fixed competitive-binding law, so the response to any mixture of cues has a closed form. While learning, the system titrates cues against each other on its own sites. If the Schild slope is not 1, or the pA2 changes depending on which agonist cue is used, the site is split into gated sub-sites. The split is kept only if each child passes both tests and predicts observed outcomes for cue mixtures it was not fitted on, so the repair is graded by a mathematical invariant plus held-out world data, not by a judge.
VALUE: The system can predict how evidence, interventions or factors combine in mixtures it has never seen, such as drug combinations, multi-symptom diagnosis or multi-factor risk, because combination follows a validated law and is not memorized. Clinicians, pharmacologists and analysts who must weigh many interacting signals at once would use it.

=== VALUED C02 ===
ANCHOR: Hodge-decomposed cycle misclosures
NAME: Self-Surveying Knowledge Atlas
MECHANISM: All knowledge is stored as an atlas: local representation charts joined by learned transition maps (analogies, translations, unit and coordinate changes). Every inference is a transport along a path in this atlas. After each batch, the misclosures around all independent cycles are Hodge-decomposed. The gradient part is spread back over the edges by least-squares network adjustment. The curl part is pinned to a blundered edge by comparing cycles that pass through it with cycles that avoid it. The harmonic part becomes a new context variable with separate charts. Each edge's trust is the number of independent cycles that close through it, so redundancy stands in for a benchmark.
VALUE: The system keeps several frames that are each consistent but disagree with each other, such as jurisdictions, scientific paradigms or conventions. For any claim it can say whether a conflict is an error or a frame boundary, and which frame the claim belongs to. Researchers, translators and analysts who reconcile inconsistent sources would use it.

=== VALUED C03 ===
ANCHOR: Adaptive phase-oscillator bank
NAME: Oscillator-Clocked Agent Memory
MECHANISM: A bank of coupled oscillators that adapt their frequencies is the agent's clock and its memory index. Every event and memory is stored under the phase vector that was current when it happened, retrieval works by phase similarity, and actions are scheduled as target phases. Oscillators adapt to reduce the phase error at the moment each event arrives. A phase-locking pattern is consolidated into a routine or concept only if its predicted arrival times beat the same bank driven by jittered surrogate streams. The correctness signal is the actual arrival time of the next event.
VALUE: Long-running agents get a real sense of duration, rhythm and lateness. They can notice that something is overdue, find hidden periodicities and anticipate what comes next. Operations teams, care monitoring and logistics would use it to watch event streams that never stop.

=== VALUED C04 ===
ANCHOR: Treatment/control subsets grade each fact
NAME: Randomized-Trial Knowledge Admission
MECHANISM: The model is a population of sub-models, and each new fact is held by a random half of them. Every ordinary prediction is therefore also a controlled trial for every fact that is still in admission. A fact's binding margin is how much better its holders predict incoming observations than its non-holders, scored before those observations are absorbed and accumulated over all routine predictions. The trial grows with how much of the model the fact would change. A fact is dropped as soon as its margin is reliably negative, and it is fully admitted once its accumulated margin crosses a sequential-test bound.
VALUE: A deployed system can keep learning from untrusted streams (web text, user corrections, reports) and admit only claims that make it better at predicting what actually happens next, with a causal credit attached to each fact. Assistants and monitoring systems that must update continuously without being poisoned would gain from it.

=== VALUED C05 ===
ANCHOR: Pseudo-random code lock-in demodulation
NAME: Lock-In Concept Learner
MECHANISM: Every internal channel, and every sensor channel the agent reads from the world, carries a demodulating integrator. When the agent learns, it varies examples, non-examples or its own interventions according to a pseudo-random code that it controls. Orthogonal decoy codes that drove nothing are demodulated at the same time, giving a measured noise floor and false-lock rate. Channels locked above the floor are stored as a new concept unit together with its signal-to-noise ratio. The unit is re-tested with a fresh code and fading channels are dropped. Correctness rests on what the agent itself varied, so no judge is needed.
VALUE: An agent can learn a new concept or causal effect from a handful of noisy trials and report a calibrated false-detection rate for it. Lab automation, robotics and product experimentation would use it where trials are costly and confidence must be known.

=== VALUED C06 ===
ANCHOR: Capture-recapture over failure-diverse passes
NAME: Capture-History Belief Store
MECHANISM: The system is built from several generators that are decorrelated on purpose: different data shards, sources, tools and decompositions. Every belief it stores carries a capture history, meaning the set of generators that produced it. A latent-class log-linear model over these histories gives each belief a probability of being real rather than a phantom, and gives each query an estimate of how many relevant items remain unseen. Interaction terms that reveal a shared bias are used to train or recruit a new generator that is penalized for that dependence, and search stops when the estimated unseen and phantom shares both fall below a threshold.
VALUE: Without any oracle, the system can say both "I have found about 90% of what exists" and "about 5% of this list is probably spurious", and it knows when to stop. Systematic reviewers, auditors, due-diligence analysts and security teams would gain from this because completeness matters to them as much as accuracy.

=== VALUED C07 ===
ANCHOR: Learned invariance group with closure
NAME: Self-Discovered Symmetry Representation
MECHANISM: The system grows explicit transformation operators by composing primitive edits (relabel, permute, reflect, rescale, swap roles). An operator earns credit only if answers mapped back through it agree more than they do under random control edits of matched size. The kept set must stay closed under composition, and when closure fails the weakest member is removed. The learned group is not a test-time wrapper: inputs are encoded as an orbit-invariant core plus group coordinates. New problems are solved by mapping them into a canonical form, and answers that break the group are flagged and used as training signal.
VALUE: The system finds out for itself which changes to an input must not change the answer, and builds on that structure to generalize far outside its training data. It can also catch its own inconsistent answers. Scientists, engineers and people working on code or puzzles with hidden structure would gain from this.