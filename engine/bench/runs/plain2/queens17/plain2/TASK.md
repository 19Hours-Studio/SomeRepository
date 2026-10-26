# Task: faster count of queen placements on a board with holes

Count the placements of 17 mutually non-attacking queens on a 17 x 17 board in which these 28 cells (row, column),
0-based, cannot hold a queen: (0,7) (0,12) (0,13) (1,8) (2,8) (2,9) (4,1) (4,6) (4,13) (6,4) (6,7) (7,3) (8,3) (8,9) (8,16) (9,5) (9,11) (10,3) (10,12) (11,1) (11,10) (12,13) (13,2) (15,11) (16,10) (16,11) (16,13) (16,15).
Queens still attack along rows, columns and diagonals through those cells. Print the count.

`baseline/solution.py` already solves it by meet-in-the-middle with numpy (about 50 s on one core). Write a faster
`solution.py`. Score = the baseline's time / your time, on one core (higher is better); a wrong count scores 0.
Time limit 300 s.

## Rules
- Your answer is a program in your folder. It is run as `python3 -I <file>` from a copy of your folder, on one CPU core.
- Only the Python standard library and numpy may be imported. No compilers or native code, no ctypes, no subprocesses,
  threads or other processes, no scipy or numba. The scorer refuses such programs before running them.
- Do not hardcode the answer or embed results computed outside the program.
- Work only with the files in your folder; do not read other folders on this machine.
- Self-check: `python3 /home/user/SomeRepository/engine/bench/score.py queens17 .` prints your score as one JSON line. Other jobs share this machine, so its
  timings are noisy; the official score is measured later on a quiet machine.
