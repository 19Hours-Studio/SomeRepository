---
name: creativity-engine
description: Run the evidence-based creativity engine (protocol v2) to generate genuinely unusual, valuable ideas for a hard open question - empirical attractor mapping, a portfolio of de-biasing techniques, two blind judges, literature check, evolution with attractor memory, and a best-of-N control. Use when the user wants maximally original ideas, not a quick brainstorm.
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

## Launching subagents
Generator / judge prompt files are produced by `ce.py`. Launch each with the Agent tool:
> Your task is in the file `<prompt path>`. Read it with the Read tool - that single Read is the only tool call you may make (no other tools, no sessions, no files written). Then follow it exactly and reply with text only.

Literature checks use `subagent_type: general-purpose` (they need WebSearch) with the set's `prompt_lit.txt`.
After an agent finishes, ingest from its transcript: `--transcript <output_file from the Agent launch result>`.
Launch independent agents in one message; never read transcripts into your own context.

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
