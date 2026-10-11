PAIR 1 notes: In Parent A, the loops come from rerunning derivations. Parent B adds conservation identities, and each balance identity is a closed condition equation that costs nothing to check. Going the other way, A's statistics replace B's fixed rules for when to invent a holder and when to demote a quantity. The mutation step borrows self-calibration from photogrammetry. When residuals show one pattern across many loops, that suggests a missing parameter, not a single blunder.

PAIR 2 notes: In Parent B, each re-encoding stage is a learned map between context encodings. So the step's re-derivations close cycles, and Parent A's Hodge decomposition can classify why the step fails. Going the other way, A's harmonic charts decide which re-encodings B's proofreading has to cross.

HONESTY CHECK:
- Offspring 1: The closest work is self-calibrating bundle adjustment with variance-component estimation (Brown 1971; Helmert/MINQUE), combined with Schulte's hidden particles. Neither applies to symbolic state tracking during reasoning. Neither decides between "blunder step" and "unseen holder" with competing w-test hypotheses. Offspring 1 does both, so it is distinct.
- Offspring 2: The closest work is self-consistency/MAKER voting and HodgeRank. Neither turns discard patterns into edge flows over a complex of re-encodings. Neither commits steps only within one chart, or charges extra proofreading for crossing a chart boundary. Offspring 2 does both, so it is distinct.

FIRST THOUGHTS:
- Chain-of-thought verifier that checks conservation constraints
- Majority vote over paraphrased reasoning paths
- Sheaf neural network that enforces consistency of local reasoning
- Graph of reasoning paths with consistency voting
- Autoencoder that infers hidden variables from residuals

=== IDEAS ===
IDEA 1
NAME: Self-Calibrating Ledger Adjustment
MECHANISM: Every double-entry balance identity is treated as a surveying condition equation. A least-squares adjustment runs over all transfers, and Baarda w-tests compare two kinds of explanation: "a blunder in step k" (a residual pattern local to one step) and "an unseen holder h" (one systematic pattern shared across many balance loops). Hidden holders are added the way self-calibration adds parameters: only when they pass a significance test and lower the minimal detectable bias of other claims. Variance-component estimation learns a reliability weight for each quantity, which continuously demotes a quantity toward "approximately conserved". Redundancy numbers point the planner to the claims nothing checks yet, and it then asks for or derives the one extra count that would close a loop around them.
VALUE: The system can track world state over very long texts and say which step is wrong or which unmentioned participant must exist, with a stated confidence in each verdict.

IDEA 2
NAME: Hodge-Sorted Chart Proofreading
MECHANISM: Each proofreading stage re-encodes the context with a learned map (paraphrase, abstraction, dropout). A step's binding margins across these encodings therefore form edge flows on a cycle complex, and a Hodge decomposition splits them into three parts. The gradient part is encoder bias: correct the map and keep the step. The curl part is real fragility: discard the step irreversibly. The harmonic part means the step holds only in some contexts: commit it locally to a new chart, with an explicit context variable and a transition map. Later steps that cross chart boundaries face extra proofreading stages, scaled to the misclosure of the transition map they cross. A new chart is kept only if steps committed in it survive this proofreading.
VALUE: Error rates in long reasoning drop exponentially without discarding conclusions that are true only in some contexts, and the system learns where its knowledge splits into separate frames.