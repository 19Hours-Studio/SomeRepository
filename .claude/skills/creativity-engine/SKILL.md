---
name: creativity-engine
description: Run the evidence-based creativity engine (protocol v1.9: layers A-B-C, plus D for physical questions) to generate genuinely unusual, valuable ideas for a hard open question - empirical attractor mapping, a portfolio of de-biasing techniques, two blind judges, literature check, evolution with attractor memory, and a best-of-N control. Use when the user wants maximally original ideas, not a quick brainstorm.
---

# Creativity engine

Deterministic core: `engine/ce.py` (state in `engine/runs/<RUN>/`). You orchestrate the subagents.
Why each step exists: `engine/README.md` and `research/stage1-creativity/03-deep-analysis.md`.

## Rules (each one is backed by an experiment)
- Generators get NO examples in prompts (examples get copied verbatim).
- Never trust a single judge or model-judged novelty: always 2 judges + a literature check.
- Do not add "text diffusion", random-word or lexical constraints: tested, they do not help.
- Process constraints must be enforced by `ce.py`, not requested in a prompt.
- Keep every generator on the same model and effort level within a run.
- Set names must sort chronologically (`s00`, `s01`, ..., `s99`): scores come from the latest set.
- Never relax the known-basin filter when choosing parents: the v2 A/B showed known-basin parents weaken generation 2.
- v2 options (`gapwalk`/`gap`, `strip`, `audit`, `select --v2`) exist but did NOT beat v1 in A/B; do not use them by default.
- For A/B tests of engine changes use `fork` (shared attractor map, isolated memory) and `import` (shared final judging).
- Species evolution (`breed` -> `species` -> `prompt R <species> g1_<species>` -> `fitness`) is an option, not default:
  in A/B it cut repeats of earlier findings by 15 pp but lowered O and V (a technique's recurring niche can be its value peak).
- Re-running a question and want NEW ground (coverage, not best ideas)? Before gen 1: `import-basins R <previous run> --source visited --as prior`.

## Launching subagents
Generator / judge prompt files are produced by `ce.py`. Launch each with the Agent tool:
> Your task is in the file `<prompt path>`. Read it with the Read tool - that single Read is the only tool call you may make (no other tools, no sessions, no files written). Then follow it exactly and reply with text only.

Judge, family, concretize and breed prompts point to a second file (`blind.txt` of the set). For them, say so explicitly,
otherwise the agent stops on the "single Read" rule:
> Your task is in the file `<prompt path>`. Read it with the Read tool, then read the file of anonymous answers it points to (`<set dir>/blind.txt`). Those two Reads are the only tool calls you may make (no other tools, no sessions, no files written). Then follow the task exactly and reply with text only.

Literature checks use `subagent_type: general-purpose` (they need WebSearch) with the set's `prompt_lit.txt`.
After an agent finishes, ingest from its transcript: `--transcript <output_file from the Agent launch result>`.
Launch independent agents in one message; never read transcripts into your own context.

## Default: engine v1.8 = layers A -> B -> C (research/stage1-creativity/06-engine-v17.md §9-10)
- Layer A (originality): `python3 engine/ce.py portfolio` gives the gen-1 portfolio (bandit over all past runs);
  run the procedure below without the crux in generators.
- Crux: `set R s00c --labels map_1,map_2,map_3`, one agent on `prompt_crux.txt`, then `family R s00c ...`.
- Layer B (genius): split the final engine ideas into sets of ~8 (`set R s97a --ids ...`), one agent per set on
  `prompt_valorize.txt`, `valorize R s97a --arm EB --transcript ...`.
- Layer C (value): same on the EB ideas with `prompt_value.txt` (`set R s96a --ids ...`), `valorize R s96a --arm EC ...`.
- Judging: one judge on a set built with `--crux --genius` plus one PLAIN judge (set without them); report paired
  child-vs-parent deltas (each layer's ideas keep a `parent` link) and `ce.py futurematch R` for literature-checked ideas.
- Measured: B gives O +0.7, G +1.0; C gives V +0.2..+0.3; no idea ever lost V, almost none lost O. A->B->C matches
  v1.7 on V and G with O +1.4. Biggest remaining lever: the crux decides what all ideas are about, so do the intent check.

## v1.9: add layer D (fermi) after C for questions about the physical world (07-v18-full-run.md)
- `set R t01a --ids <EC ids> --prefix D` (batches of ~8), one agent per set on `prompt_fermi.txt`,
  `valorize R t01a --arm ED --transcript ...` (stores `verdict` PASS/FIX/FAIL and `estimate`).
- Judging: add one judge on a set built with `--feasible` (column F = order-of-magnitude feasibility); report O·V·F.
  V alone cannot see D's gain: V means "if it worked". Measured: F +1.0, C +2.3, O -0.2, V -0.1 (FIX ideas: V +0.3;
  FAIL ideas shrink their claims honestly, V -1.0), O·V·F +31%. Judges alone put ideas that fail by orders of
  magnitude in their TOP3, so never report physical-world winners without D or an F judge.

## Tested and NOT better (07-v18-full-run.md, v2.0-v2.1) - do not use by default
- Principles as the search unit (`pr_assume`, `pr_transfer`, `pr_dissolve`, `pr_tail` + `prompt_truth` + `prompt_derive`):
  69% of principles already known, 0 of 8 best were new and true.
- Verbalized tail sampling of designs (`tail`): O 3.25 vs layer A 5.61, 8/8 known (rare-to-propose != unknown).
  Self-reported typicality P only weakly predicts O (-0.3..-0.5).
- Second D pass (D2): F +0.17 only. One D pass gives most of the repair.
- The judge column P (`--principle`, single principle) measures form, not novelty (corr with O 0.04).

## Option (not default): count -> law -> invent loop
- `laws R --arm ED` + one agent on `laws/prompt_laws.txt` + `laws R --transcript ...`; then `prompt R law g3_law1`.
- Measured on energy: V +0.8 and (after D) F +0.5, but O -1.8: a law's favorable regime is usually already occupied by
  known technology. Use it when value and feasibility matter more than originality.
- After any user interrupt, check that running agents are still alive before waiting on them.

## v1.7 option (crux in generation: best V, but O -1.0 vs layered)
- Gen 1 portfolio: neg, core, loop, mech, genius. Gen 2: `prompt R evo_simple g2_evo1|g2_evo2 ...` (simplifying crossover) + immigrant of the best technique. Parents: `select ... --drop-known-basins --diverse --by ovg`. Screening/final sets: `--crux --genius`.
- ALWAYS add one plain judge (a set built without `--crux --genius`) to any A/B: the crux column primes judges' V (about half of the V gain in the v1.7 A/B was priming).
- Crux: the family judge now also outputs `CRUX | ...` (or use `sets/<s>/prompt_crux.txt` on an existing map); `setcfg R use_crux 1` makes every generator attack it; final sets with `--crux` get a column X (attacks the crux: Y/N).
- `select ... --diverse`: near-duplicates (same closest work) share one slot. Fragments (ideas citing "Idea 1") are never selected.
- Portfolio by cross-run fitness: neg, core, core2, mech, loop (`mechneg` lost selection on 2 new questions).
- Intent check: before gen 1, show the user 2-3 contrasting readings of the question from the map and confirm (a literal reading cost a whole run on arch_spec).

## Procedure (R = run name, E = engine arm, C = control arm)
0. `python3 engine/ce.py init R --question "<question>"`
1. **Attractor map.** `prompt R plain map_1` (… `map_3`); run 3 generators; `ingest R map_k --arm C --gen 0 --transcript …`.
   `set R s00 --labels map_1,map_2,map_3 --prefix M`; run one judge on `sets/s00/prompt_family.txt`; `family R s00 --transcript …`.
2. **Variation (gen 1).** `prompt R <tech> g1_<tech>` for neg, core, mech, loop, plus a second core run as `g1_core2`
   (v1.5: REFRAME was the weakest technique in three runs); run 5 generators; `ingest … --arm E --gen 1`.
3. **Screening.** `set R s01 --labels g1_neg,g1_core,g1_core2,g1_mech,g1_loop --prefix A`; run 2 judges on `sets/s01/prompt_judge.txt`;
   `judge R s01 J1 …`, `judge R s01 J2 …`; `select R g1 --labels <gen1 labels> --k 6 --drop-known-basins`.
4. **Literature.** `set R s02 --ids <survivor ids> --prefix L`; run one lit agent on `sets/s02/prompt_lit.txt`; `lit R s02 …`.
   `remember R --labels <gen1 labels>` (attractor memory: next generation is repelled from what was just found).
5. **Evolution (gen 2).** `pairs R g1 --n 6`; `prompt R evo g2_evo1 --pairs 3 --pair-from 0`, `prompt R evo g2_evo2 --pairs 3 --pair-from 3`;
   immigration: re-run the best gen-1 technique as `g2_imm` (fresh prompt picks up the updated basin map). Ingest with `--arm E --gen 2`.
   **Concretize (v1.5):** `set R s03 --labels g2_evo1,g2_evo2,g2_imm --prefix K`; one agent on `sets/s03/prompt_concretize.txt`;
   `concretize R s03 --transcript …` (adds a first decisive test to each offspring; gen-2 concreteness +2.4…+3.1 in A/B).
   Optional: `setcfg R thoughts 1` before gen 1 and `thoughts R` before gen 2 (self-reported first thoughts; small effect, primed by the basin list).
6. **Control (best-of-N).** Plain prompts until the control arm has as many generator calls as the engine arm
   (map runs count): `prompt R plain ctrl_k`, `ingest … --arm C`.
7. **Final judging.** `set R s99 --arms E,C --prefix F`; 2 judges on `sets/s99/prompt_judge.txt`; `report R`.
8. **Winners' literature.** `set R s99L --ids <top ideas> --prefix W`; lit agent; `lit R s99L …`; `report R` again.
Report to the user: arm table (engine vs control), top ideas with literature verdicts, and what the judges' NOTEs say.
