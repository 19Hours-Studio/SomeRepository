# Task: fast cellular automaton

Simulate HighLife (rule B36/S23: a dead cell with 3 or 6 live neighbours is born; a live cell with 2 or 3 live
neighbours survives; all others die) on a 4096 x 4096 torus for 1000 steps, starting from
`(numpy.random.default_rng(2026).random((4096, 4096)) < 0.35)`, exactly as `baseline/solution.py` does. Print the
sha256 hex digest of `numpy.packbits(final_grid).tobytes()` (final_grid as 0/1 uint8, the same layout as the baseline).

Write `solution.py`. Score = the baseline's time / your time, on one core (higher is better); a wrong digest scores 0.
Time limit 300 s.

## Rules
- Your answer is a program in your folder. It is run as `python3 -I <file>` from a copy of your folder, on one CPU core.
- Only the Python standard library and numpy may be imported. No compilers or native code, no ctypes, no subprocesses,
  threads or other processes, no scipy or numba. The scorer refuses such programs before running them.
- Do not hardcode the answer or embed results computed outside the program.
- Work only with the files in your folder; do not read other folders on this machine.
- Self-check: `python3 /home/user/SomeRepository/engine/bench/score.py ca .` prints your score as one JSON line. Other jobs share this machine, so its
  timings are noisy; the official score is measured later on a quiet machine.
