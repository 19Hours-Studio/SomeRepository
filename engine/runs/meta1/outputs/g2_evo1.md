Offspring 1 (Pair 1, Hint-Gap x Implementer Gaps). Gaps are found by rebuild disagreement, not by self-marking. Each step of a plain build plan is masked, and N fresh agents rebuild it from the surrounding plan. Steps where the rebuilds disagree are the real gaps. A fill passes only if two things hold. First, its 15-word hint makes the rebuilds of that step agree. Second, inserting it makes the independent rebuilds of the later steps agree too. Closest work: semantic-entropy uncertainty (Kuhn et al. 2023) and cloze infilling. Those measure uncertainty. They do not score a fill by how much it settles the later steps, so this is different.

Offspring 2 (Pair 2, Walker Stall x Slot Ablation). The walker's stall point replaces judge-scored value drop as the ablation signal. Each slot removed changes where the walk on a concrete instance stalls, and that gives a stall-shift map. Closest work: delta debugging (Zeller) and program slicing. Those localize failures that already exist. Here the map decides which slots may be rewritten off-attractor, and the rewrite has to move a stall later. That is a different purpose, so it is kept.

Offspring 3 (Pair 3, Success Record x Gap List). Records must hinge on a recurring gap, and the gap fill is accepted on numbers. Closest work: Amazon Working Backwards and test-driven development. Making the record a contrast pair (the vague default fill against a surprising fill) and deriving the mechanism from the difference between them was a second mutation. Closest to that is contrastive explanation (Miller 2019), which explains differences but does not generate fills.

=== IDEAS ===
IDEA 1
NAME: Downstream Convergence Gap Filling
MECHANISM: Each step of a plain build plan is masked in turn, and N fresh agents rebuild it from the rest of the plan. Steps where the rebuilds disagree most are treated as the true gaps. A generated fill plus its 15-word hint is kept only if two conditions hold. Hint-given rebuilds of the gap step must agree while hint-free rebuilds stay scattered. Inserting the fill must also cut the disagreement among independent rebuilds of all later steps. Disagreement profiles for each step and the hints that worked are stored, so a later "new" fill that an old hint reproduces is flagged as already known.
VALUE: An idea is rewarded for being unreachable from the question and also for making the rest of a valuable plan buildable. This is measured by sampling, not by what the judges know.

IDEA 2
NAME: Stall-Shift Slot Carving
MECHANISM: Each plain answer is split into slots. The walker replays it on a concrete instance with one slot removed at a time and records how far the stall point moves. Slots whose removal moves the stall earlier are frozen. Slots that do not move it are marked dead weight, and only those may be rewritten off-attractor. Each rewrite must push the stall later on an unpassed instance drawn from the cross-run stall table. That table is indexed by slot type, so carving targets carry over between runs.
VALUE: Originality is spent only on slots whose replacement measurably gets the answer past real failure points. Value is therefore checked by execution, not by a judge's guess.

IDEA 3
NAME: Contrast-Record Gap Derivation
MECHANISM: For each recurring gap, an agent writes two dated records. One is the measured outcome when the gap is filled the vague default way. The other is a surprising, better outcome. A blind agent derives the smallest mechanism that explains the numeric difference between the two records. It is accepted only if re-expanding the plan removes the gap and a forward walk reproduces both numbers. Unexplained contrast pairs are stored as open targets for the next run, and explained mechanisms are stored as forbidden templates.
VALUE: Each original idea arrives as a concrete fill for a step that obvious plans skip, with a specific, checkable improvement over the default.