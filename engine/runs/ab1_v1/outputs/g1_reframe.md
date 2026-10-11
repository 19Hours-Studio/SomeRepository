None of these three ideas fix a known weakness of current models. Each one adds a kind of behaviour that today's systems have no form for, and none of them falls in the forbidden families.

=== IDEAS ===
IDEA 1
NAME: Subtractable Upbringing Ledger
MECHANISM: During training, each distinct data stream (a corpus, a school of thought, a language community) writes into its own separate low-rank weight delta, so the model is stored as a base plus a ledger of experience deltas. At inference the system can add, remove or reweight deltas to bring up "counterfactual selves" that would have existed under a different upbringing. It runs these selves side by side and computes a structured diff of their beliefs. The ledger keeps growing as new streams arrive, and each stream stays a separable entry.
VALUE: It can answer "what would I believe if I had never read X, or had grown up on Y instead?", tracing a conclusion back to the experiences that formed it.

IDEA 2
NAME: Oscillator-Entrained Timing Core
MECHANISM: Representations are held as the phases and amplitudes of a large bank of coupled oscillators, not as static vectors. Inputs drive phase-locking, and the outputs are emitted at moments set by phase alignment rather than by a request-response cycle. Coupling strengths adapt from phase error against external rhythms such as speech cadence, music or other agents' actions. Learned coupling patterns are stored as reusable "groove" templates.
VALUE: It can act as a real-time timing partner that shares tempo with humans or other agents in improvisation, joint movement and overlapping conversation, not just answer prompts.

IDEA 3
NAME: Sealed Commitment Register
MECHANISM: Inference runs deterministically on quantized arithmetic, so any internal state can be replayed exactly. A commitment register stores cryptographic hashes of chosen latent plans, predictions or intentions at the moment they are formed. A policy layer is trained to be penalized for actions that conflict with open commitments. Later the system can reveal a commitment and prove by replay, or with a zero-knowledge proof, what it believed or intended at that earlier time.
VALUE: It lets an AI make credible precommitments, sealed bets and verifiable promises to people or other AIs, opening up negotiation, contracts and game-theoretic coordination it cannot take part in today.