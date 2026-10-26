I wrote `solution.py`, and the official self-check scored it **7.69** (merit 7.76 and 7.61 on its two runs). The machine was busy with other jobs while it ran, so the timing on a quiet machine should be a bit better. The baseline gets about 5.7.

**Approach**
- **Odd N (including 127):** the program only searches skew-symmetric sequences. In these the second half mirrors the first with alternating signs, so it only has to choose about half the bits. The search takes the best single-bit change at each step and never returns to a sequence it has already visited. Each walk runs for 10,000 steps, then restarts from a random sequence. 32 walks run side by side in numpy, and the score of every possible change is updated cheaply after each step instead of being recomputed. Each step costs about 2.8 µs, roughly 20 times faster than the first plain version.
- **Even N:** it runs the same search at N−1 for 90% of the time. It then tries adding one bit at either end of up to 3,000 of the best results and keeps the best one. The last 10% runs an ordinary single-bit search from those sequences. In my tests that last step never improved the result, so it is only a fallback.
- **Correctness:** each new best sequence's energy is recalculated from scratch and checked against the running total.

**Self-measured results** (50–54 s runs, several in parallel, so pessimistic)

| N | Merit factor |
|---|---|
| 127 | mean ≈ 8.0 over 12 runs, range 7.47–8.70 |
| 100 | 8.65 |
| 128 | 7.67–8.13 |
| 160 | 7.16–7.37 |

Results vary a lot from run to run because the search is random. Changing the walk length between 3,000 and 40,000 steps made no clear difference.