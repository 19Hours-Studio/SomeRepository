FIRST THOUGHTS:
- A persistent external memory the system writes to and reads from at inference, consolidated later
- A learned simulator of the environment used to imagine and search over futures before acting
- Specialist sub-networks competing for a shared bottleneck that decides what gets processed next
- A self-checking loop where outputs are verified by a separate checker and revised until they pass
- Small symbolic programs induced from examples and executed instead of pattern-matched

=== IDEAS ===
IDEA 1
NAME: Dimensional Exponent Tagging
MECHANISM: Every internal quantity carries, alongside its real-valued vector, a short integer vector of exponents over a learned set of base "kinds" (like length, time, count, agent). When two quantities are multiplied or divided, their exponent vectors add or subtract. When they are added or compared, the exponents must match, and any mismatch produces an imbalance residual. That residual is the learning signal. Persistent mismatches over many examples cause a new base kind or a conversion constant to be created, and kinds that never constrain anything are merged away.
VALUE: Reasoning steps that make no physical or logical sense get rejected because their kinds don't match, and the system can extrapolate to unseen magnitudes by scaling rules instead of memorized examples.

IDEA 2
NAME: Double-Entry Conservation Ledger
MECHANISM: Each state change described in the input or produced during reasoning is written as a transfer: one amount debited from one holder and credited to another, across a learned set of conserved quantities (objects, money, people, information). After every step, the totals for each quantity are summed, and they must balance. A nonzero imbalance is the training signal. If the imbalance persists, the system creates a new hidden holder to absorb it and keeps that holder only if it later balances other transfers. Quantities whose totals never actually stay constant get demoted from the conserved set.
VALUE: The system can track the state of the world exactly over very long sequences, and it can infer unmentioned participants or leaks from bookkeeping gaps.

IDEA 3
NAME: Self-Discovered Symmetry Harvesting
MECHANISM: The system keeps a growing pool of candidate input transformations, built by composing primitive edits: relabel, permute, reflect, rescale, swap roles. At inference it answers both the original input and several transformed copies, maps each answer back through the inverse transformation, and measures how much the answers disagree. A transformation's score rises when answers agree on cases that were verified correct, and it falls when they diverge. High-scoring transformations are kept and used both to vote at inference and to enlarge the training data. Low scorers are discarded, and recombinations of kept ones are proposed as new candidates.
VALUE: The system finds on its own which changes to an input must not change the answer, which gives it structured generalization far outside its training distribution.