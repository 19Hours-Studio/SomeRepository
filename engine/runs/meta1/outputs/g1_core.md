**1. Goals from the center**
- G1: Make answers more original without losing the value of the plain answers.
- G2: Keep same-family judges from rewarding defects they cannot see. Today validity is left to an unnamed verifier.
- G3: Keep ideas concrete and implementable, especially after recombination.

**2. Paradigm negation**
Mainstream fixes all generate candidates, then score and select them, so better ideas come from better filters, judges or forbidden zones. I forbid generate-then-score-select as the mechanism. It is still allowed as a goal.

**3–4. Mechanisms from the periphery**
- G1 comes from structural topology optimization (SIMP). The state is a material density per element. The update removes material where the compliance sensitivity is low. Ported here: a plain answer is split into component slots. An ablation agent deletes each slot, and judges measure how much value drops. Slots with high sensitivity are frozen. Slots with low sensitivity are carved out and refilled off-attractor. Novelty only goes where it costs no value.
- G2 comes from mutation testing in software. Faults are planted to measure whether a test suite catches them, and the kill rate drives trust. Ported here: a mutator agent plants known defects in copies of real answers. Examples are a broken causal step, an inflated value claim, a disguised known family, and a step that cannot be implemented. These go into the judging stream. Each judge criterion is weighted by its measured kill rate per defect type.
- G3 comes from retrosynthesis in chemistry. Work backward from the target molecule through known reactions until every leaf is a purchasable reagent. Ported here: start from a target effect and chain backward until every leaf is an available primitive (prompt, role, stage, scoring rule, stored data). Unresolved leaves are the driving signal.

**5. Honesty check**
- Idea 1: the closest work is self-refine-style editing and ablation attribution. It differs because the edit is placed by a value-sensitivity map. It is not REFINE, which restores concreteness instead.
- Idea 2: the closest work is gold questions in crowdsourcing and benchmarks of LLM-judge bias. It differs because it runs inside the pipeline every run, the mutants are typed, and they reweight criteria. That is neither DIVJUDGE nor KILLTEST.
- Idea 3: the closest work is Corey retrosynthesis and backward-chaining planning (STRIPS). No ideation pipeline builds ideas backward from primitives. It is not GRAFT, because it does no crossover.

=== IDEAS ===
IDEA 1
NAME: Sensitivity-Guided Answer Carving
MECHANISM: Each plain answer is split into 4–8 component slots. An ablation agent removes one slot at a time, and judges score how much value drops, which gives a value-sensitivity map. Slots with high sensitivity are frozen. Generators may rewrite only slots with low sensitivity, and only off-attractor. The cycle repeats with the map recomputed after each carve. Sensitivity maps are stored per question type across runs.
VALUE: Originality goes only where it costs no value, so value stops falling below plain answers.

IDEA 2
NAME: Mutation-Tested Judges
MECHANISM: A mutator agent plants typed defects in copies of real answers: a broken causal step, an inflated value claim, a disguised known family, or a step that cannot be implemented. These go into each judging batch. The pipeline computes each judge's kill rate per defect type and weights each scoring criterion by that rate. Defect types with low kill rates are flagged so that idea must state its own evidence. The mutant library and kill rates persist across runs, and mutants judges keep missing are planted more often.
VALUE: The judges' shared blind spots are measured and discounted instead of silently rewarded.

IDEA 3
NAME: Retrosynthetic Idea Assembly
MECHANISM: Ideas are built backward from a stated target effect, such as "value at least the baseline" or "concreteness survives recombination." An agent proposes "reactions": each is a step that produces the effect from precursors. It recurses until every leaf is an available pipeline primitive. Trees with leaves that cannot be resolved are rejected. Validated reactions are stored as a library across runs, and novel reactions get a bonus.
VALUE: Every idea comes out concrete and implementable by construction, not restored after the fact.