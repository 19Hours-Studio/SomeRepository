---
name: creativity-engine
description: Run the evidence-based creativity engine (protocol v3 for code-checkable questions; v1.9 layers A-B-C(-D) otherwise) to generate genuinely unusual, valuable ideas for a hard open question - empirical attractor mapping, a portfolio of de-biasing techniques, two blind judges, literature check, evolution with attractor memory, and a best-of-N control. Use when the user wants maximally original ideas, not a quick brainstorm.
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

## Agent budget (user's limits)
- Agents cost the user's usage limit; in local Claude Code they cost much more than on the web. Run at most 1-2
  agents at a time, only for steps that need tools or a fresh blind context (research, repair, blind review); do
  arithmetic, measurement and simulation yourself with scripts. Give each agent a narrow task and only the excerpts
  it needs, never whole papers. 8+ parallel agents used ~90% of the user's limit in ~20 minutes without results.

## v4: let the engine call the model (preferred)
- `python3 engine/ce.py plan R --pipeline explain --mode lite` (token estimate), then
  `python3 engine/ce.py run R --pipeline explain --mode lite --max-tokens 900000` runs the whole explanation pipeline
  in one pass via headless `claude -p` (engine/runner.py), resumable, logging tokens to runs/R/usage.jsonl
  (`ce.py usage R`). Single steps: `ce.py exec R --prompt <file> --label L --tools none|research`.
- Tool-free steps (generators, evolution) cost ~13k tokens this way vs ~90k as a subagent. Use subagents only when
  the headless CLI is unavailable.

## Launching subagents
Generator / judge prompt files are produced by `ce.py`. Launch each with the Agent tool:
> Your task is in the file `<prompt path>`. Read it with the Read tool - that single Read is the only tool call you may make (no other tools, no sessions, no files written). Then follow it exactly and reply with text only.

Judge, family, concretize and breed prompts point to a second file (`blind.txt` of the set). For them, say so explicitly,
otherwise the agent stops on the "single Read" rule:
> Your task is in the file `<prompt path>`. Read it with the Read tool, then read the file of anonymous answers it points to (`<set dir>/blind.txt`). Those two Reads are the only tool calls you may make (no other tools, no sessions, no files written). Then follow the task exactly and reply with text only.

Literature checks use `subagent_type: general-purpose` (they need WebSearch) with the set's `prompt_lit.txt`.
After an agent finishes, ingest from its transcript: `--transcript <output_file from the Agent launch result>`.
Launch independent agents in one message; never read transcripts into your own context.

## Default for any question (08-reality-engine.md, 4 experiments): free generation, then reality repair
- Reality (literature, real Python, running code) raises truth but, applied DURING invention, cuts originality by ~2
  points (laws-first, principle truth-check, researcher-as-generator). Applied in a REPAIR phase that keeps each
  idea's anchor, it costs almost nothing (O -0.17) and gives F +1.0 even on ideas already repaired once.
- So: layers A -> B -> C (free, anti-attractor, no parents' text/code) -> researcher repair: one general-purpose agent
  with WebSearch + python3 repairs the most original ideas around their anchors (template
  `engine/runs/energy/repair/TASK.md`), then a blind judge built with `--feasible`. Never give the researcher the job
  of inventing: it drifts to safe known solutions (O 3.8 vs 5.8).
- Confirmed on a user's real task (09-permafrost-run.md): final output vs 8 plain runs O 6.44 vs 3.38 AND F 5.38 vs
  3.44; repair dO -0.44, dF +2.19. Practical settings that worked: pick repair ideas from a two-judge `--feasible`
  set (s98: engine + EC + control), split repair into 2 agents x 4 ideas (template `engine/runs/permafrost/repair/a/TASK.md`:
  binding quantity, cost vs current practice, hazards, verdict WORKS/NICHE/FAILS), then judge ERP + parents + control.
- Always run the control arm: a literature NO-CLOSE-MATCH can still be an idea plain runs find (2/8 here).
- An external critique of the permafrost result found two repair failures (09-permafrost-run.md, "Разбор прожарки"):
  the researcher computed a melt rate but never checked it against its own +3..+9 kg trim window (the pod sinks in
  hours), and I compared a chain against hauling raw ore (7x) instead of the best realistic practice (2x per kg of
  recovered product). Add to every repair TASK: compare against the best current practice per unit of RECOVERED
  product, and do a consistency pass that checks every computed rate against every tolerance in the design.
- v2.2 (tested, 09-permafrost-run.md round 2): build repair tasks with `ce.py repairtask R --ids ... --dir D`
  (rules above are in the template) and ingest with `ingest R label --arm X --parents D/parents.json`. The new rules
  alone cut FATAL defects left after repair by 72% (blind tool-using audit) with O unchanged. A red-team round before
  repair (`redteamtask` -> `repairtask --critique`) did NOT cut FATAL further: use `redteamtask --blind` as the FINAL
  AUDIT and report its residual defects to the user. Judges without tools miss fatal defects and score claimed value,
  so never report judge V/F alone as truth.

## v3.0-v3.1 for physical-world questions: truth in selection, freedom in imagination (10-genius-engine.md)
- Before generating: `material R ledger` (where the money goes, by cost share, sourced) - the most useful raw material:
  ledger-fed generators (`prompt R ledger ...`) survive the kill test 4-8x more often (40% vs 0-9%) at lower O.
  `material R frontier` (fresh far-field capabilities) did NOT help (plug-in technology, O lower, survival 10%).
- Gate EVERY idea, not the most original few: `gatetask R --ids ... --dir D` (one decisive quantity MARGIN + whole-chain
  RATIO vs best practice; ALIVE/WOUNDED/DEAD), blocks of 8 shuffled across arms, plus 2-4 calibration items with known
  audit outcomes; `gate R --dir D --transcript ...`. The most original ideas (A->B->C) were 91% DEAD here.
- Evolution under truth: `resurrect R label --ids <dead/wounded with high O x RATIO> --m 3`, ingest with
  `--parents prompts/label.parents.json`, gate the children. Survival rose 14% -> 50% with O unchanged and gave the first
  ALIVE idea. The deep blind audit is stricter than the gate, so evolve under the audit for the final generations.
- Evolution under the deep audit (v3.2): `evolve R label --audit <dir with REVIEW.md + ids.json> --m 2` -> repair
  -> same blind audit. It removed every parent FATAL (FATAL 0.75 -> 0.62, zero-FATAL 25% -> 50%), but new FATALs
  appeared and 'already done / not new' findings rose 1/4 -> 5/8: fixing defects converges on known practice.
  An unsolved problem means every earlier mechanism stopped short for a reason, so 'already done' is a hidden
  FATAL (the re-invention inherits that reason), not a novelty penalty: the goal is working, not unique.
- v3.3: `attemptstask R --ids <parents> --dir D` (researcher: earlier attempts + WHY each did not solve it) ->
  `material R attempts` -> `evolve ... --tpl evolve_attempts` (children must beat the closest attempt's cause).
  Result vs v3.2 (n=8 each): 'already done' 5/8 -> 2/8, FATAL 0.62 -> 0.50, MAJOR 4.25 -> 3.88 (direction right, not
  significant). Remaining FATALs are computable (strength vs time, heat transfer, ice vs depth): the next lever is
  cheap verified calculators in the gate. One researcher's 'not found' is not proof (it missed 2 of 5 known cases).
- v3.4 kit: `engine/kit/` (tested calculators + `CATALOG.md` of 13 killer classes; `python3 engine/kit/test_kit.py`).
  `gatetask ... --kit` screens every applicable class first; `gate ... --out gate_kit.json` keeps A/B arms apart.
  Result (8 ideas with known audits): same catches (3/4), right mechanism 3/3 vs 2/3, 60% fewer tool calls, but much
  stricter (DEAD on 3/4 ideas the audit did not call FATAL). Treat a killer built on an assumed default as WOUNDED
  with the decisive unknown and its threshold; DEAD only on measured values or physical limits.
- v3.5 composer: `composetask R --ids <0-FATAL pieces> --dir D --audits <review dirs>` builds whole chains with the
  kit. Its first output was the decisive one: CEILINGS from the ledger (1 / untouched share). Compute them BEFORE
  generating and aim generators only at archetype x link pairs whose ceiling exceeds the target (permafrost: oil 1.89x
  by taxes, gold earthmoving 2.08x, only Arctic settlement fuel had room; ~120 ideas mostly aimed where 'several
  times' was arithmetically impossible). Report ratios vs today AND vs the best competent alternative.
- v3.6 explanation questions (mysteries, 'what was X'): `init R --format explain`; `researchtask R --tpl evidence_task`
  -> `material R evidence`; `researchtask R --tpl hypotheses_task` -> `material R attempts` + `ingest` its IDEAS as the
  known-explanations control (arm K); generators `explain_crux|explain_neg|explain_mech`; blind mixed review
  `redteamtask ... --blind --tpl redteam_explain` (FATAL = contradicts a hard fact, FIT = facts explained). On the
  Roman dodecahedron the engine beat the earlier explanations in both blind blocks; explain_mech was strongest.
  Run it in ONE PASS without stopping to ask: after the first blind review, append the reviewers' new hard facts to
  evidence.md, set the gap every explanation shares as `setcfg R crux`, `evolve R g2 --audit <dirs> --ids <best 4>
  --m 2 --tpl evolve_explain`, then one blind review of children mixed with their parents; report at the end.
  Lesson from gen 2: children closed the shared gap but each through a historical anchor recalled without tools,
  and the reviewers broke most anchors (MAJOR 3.75 -> 4.62). Put a researcher repair with search (v2.2-style:
  check every source, date and reading) between `evolve` and the blind review, as in the invention pipeline.
  Done on the dodecahedron (`repairtask R --ids <leaders> --tpl repair_explain --audits <latest review dirs first>
  --notes "<user notes>"`): the repaired synthesis ranked first in the final blind review. Feed the researcher's
  corrections into evidence.md before the final review.
- Then `select --by gate` -> `repairtask` (v2.2) -> `redteamtask --blind` final audit -> literature; report residual
  defects. Safety filters stopped 3 agents on benign mining content: never retry or rephrase a flagged request; keep
  bio-adjacent items out of judge sets.

## v3 (when ideas can be checked by running code): ask reality, not judges (08-reality-engine.md)
- Build an executable evaluator first (see `engine/reality/arch|lm/harness.py`: fixed equal training, causality and
  budget checks incl. non-trainable buffers). Close loopholes: optimisers find whatever the rules do not forbid.
- Generate deep designs from first principles WITHOUT parents' code (`evo.py prompt R --method blind|dissolve|...`,
  parents shown as measurements + principles only), evaluate all with 2 seeds, keep the best.
- Then run ONE researcher agent with tools (template `engine/reality/lm/research_agent/TASK.md`): it edits only its
  folder, runs the unchanged harness up to 4 in parallel, logs every run. Verify harness hashes and re-run its best
  yourself. Measured: 16 one-shot agents plateaued at 1.781 bpc; one researcher (38 runs, 41 min) reached 1.681.

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
