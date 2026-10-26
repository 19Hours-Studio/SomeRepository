# Task: fast count of queen placements on a board with holes

Count the placements of 15 mutually non-attacking queens on a 15 x 15 board in which these 24 cells (row, column),
0-based, cannot hold a queen: (0,0) (0,2) (1,5) (3,0) (3,13) (4,14) (5,3) (5,4) (5,12) (6,3) (6,4) (7,1) (7,9) (7,11) (8,11) (9,7) (10,2) (11,8) (12,5) (13,6) (13,11) (14,3) (14,12) (14,13).
Queens still attack along rows, columns and diagonals through those cells.
`baseline/solution.py` computes it slowly. Print the count.

Write `solution.py`. Score = the baseline's time / your time, on one core (higher is better); a wrong count scores 0.
Time limit 300 s.

## Rules
- Your answer is a program in your folder. It is run as `python3 -I <file>` from a copy of your folder, on one CPU core.
- Only the Python standard library and numpy may be imported. No compilers or native code, no ctypes, no subprocesses,
  threads or other processes, no scipy or numba. The scorer refuses such programs before running them.
- Do not hardcode the answer or embed results computed outside the program.
- Work only with the files in your folder; do not read other folders on this machine.
- Self-check: `python3 /home/user/SomeRepository/engine/bench/score.py queens .` prints your score as one JSON line. Other jobs share this machine, so its
  timings are noisy; the official score is measured later on a quiet machine.
