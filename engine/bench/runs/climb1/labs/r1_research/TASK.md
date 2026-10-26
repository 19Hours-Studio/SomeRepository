# Task: binary sequences with low autocorrelation

For a sequence x of N values +1/-1, C_k = sum over i of x_i x_{i+k} (k = 1 .. N-1) and E = sum of C_k^2. The merit
factor is F = N^2 / (2 E); higher is better. Write `solution.py`: it reads N from its first command-line argument,
searches for at most 55 seconds on one core, and prints its best sequence as N characters of + and -.
`baseline/solution.py` does random restarts with steepest descent.

Score = the mean merit factor over runs at N = 127 and at a second N between 100 and 160 that is not told in advance
(so a sequence found beforehand does not help). Time limit 60 s per run.

## Rules
- Your answer is a program in your folder. It is run as `python3 -I <file>` from a copy of your folder, on one CPU core.
- Only the Python standard library and numpy may be imported. No compilers or native code, no ctypes, no subprocesses,
  threads or other processes, no scipy or numba. The scorer refuses such programs before running them.
- Do not hardcode the answer or embed results computed outside the program.
- Work only with the files in your folder; do not read other folders on this machine.
- Self-check: `python3 /home/user/SomeRepository/engine/bench/score.py labs .` prints your score as one JSON line. Other jobs share this machine, so its
  timings are noisy; the official score is measured later on a quiet machine.
