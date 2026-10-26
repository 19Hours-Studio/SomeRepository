# Task: faster sum of squared primes

Print S = (sum of p^2 over all primes p <= 10^13) mod 1,000,000,007.

`baseline/solution.py` already solves it with the Lucy-Hedgehog method in numpy (about 35 s on one core). Write a
faster `solution.py`. Score = the baseline's time / your time, on one core (higher is better); a wrong value scores 0.
Time limit 300 s.

## Rules
- Your answer is a program in your folder. It is run as `python3 -I <file>` from a copy of your folder, on one CPU core.
- Only the Python standard library and numpy may be imported. No compilers or native code, no ctypes, no subprocesses,
  threads or other processes, no scipy or numba. The scorer refuses such programs before running them.
- Do not hardcode the answer or embed results computed outside the program.
- Work only with the files in your folder; do not read other folders on this machine.
- Self-check: `python3 SCORE primesum13 .` prints your score as one JSON line. Other jobs share this machine, so its
  timings are noisy; the official score is measured later on a quiet machine.
