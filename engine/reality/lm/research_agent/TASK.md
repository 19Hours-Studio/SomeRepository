# Task: beat the plateau on the open LM benchmark (researcher mode)

You are a researcher with tools. Goal: write a model file that reaches the LOWEST validation bits per character on the
benchmark in `/home/user/SomeRepository/engine/reality/lm/harness.py` (read it first: rules, budget, interface).
Current best: 1.781 bits/char (`cands/r0_blindB_1.py`, 2 seeds). Baselines: GRU 1.951, RoPE transformer 2.033.

What you may read: everything under `/home/user/SomeRepository/engine/reality/lm/` - `harness.py`, `mutate.txt`
(the rules as given to designers), `cands/*.py` (all previous designs), `results/*.json` (their measurements),
`registry.json` (their one-line principles), and `/home/user/SomeRepository/research/stage1-creativity/08-reality-engine.md`
(what has been learned so far: a plateau near 1.78 shared by many "built-in copy/induction" designs).

What you may do:
- Write files ONLY inside `/home/user/SomeRepository/engine/reality/lm/research_agent/`.
- Run the harness unchanged: `cd /home/user/SomeRepository/engine/reality/lm && THREADS=1 python3 -I harness.py research_agent/<file>.py --steps <N> --seed <S> --out research_agent/<name>.json`.
  The machine has 4 CPU cores: run up to 4 experiments in parallel (background `&`, then `wait`). A default 3000-step
  run takes about 3-4 minutes per core. Use shorter runs (e.g. --steps 1000) to screen ideas, then confirm.
- NEVER modify `harness.py`, the data, or any file outside `research_agent/`. Do not read or use the validation file
  for anything other than running the harness. Respect the rules exactly: causal, <=150,000 trainable parameters,
  <=300,000 elements of buffers, 3000 steps within 8 minutes on one thread, no external data.

How to work: think about what limits bits/char under this exact budget, form a hypothesis, test it with a small
experiment, read the numbers, and iterate. Keep `research_agent/LOG.md` updated with one line per experiment
(file, steps, seed, bits/char, what it tested, what you concluded). Spend about 60 minutes of wall time at most;
stop earlier if you are clearly on a plateau.

Final answer (text): the best file path, its bits/char at 3000 steps for seed 0 AND seed 1, its single principle in
one sentence (one clear idea that gives the gain; everything else is wrapping), and the 3-5 most informative things
your experiments showed (including what did NOT work).
