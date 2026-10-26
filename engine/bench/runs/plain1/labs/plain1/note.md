I measured a score of **6.96** with the official self-check (merit factors 6.958 and 6.955). My first version scored 6.05 on the same check, and I didn't measure the baseline. The machine is shared and was busy, so this probably understates the quiet-machine score. On a quieter run my solution reached 7.76 at N=127.

**Approach** (`solution.py`, numpy only, one core, 54-second budget):
- **Search method:** a memetic algorithm in the MATS style. It keeps a population, recombines two parents with a one-point crossover, mutates the child, and improves each child with a short tabu search.
- **Fast step:** I keep a table S[j,k] = x_{j+k} + x_{j−k} and the correlations C. The gain from flipping each bit is then 4·R − 4·x·(S·C), one BLAS matrix-vector product per step. A flip updates only O(N) entries. A tabu step takes about 11 µs at N=127, about 2× faster than my first version. I checked the energies against brute force.
- **Odd N:** the search is limited to skew-symmetric sequences, which halves the number of free variables, and all odd-lag correlations are then zero. A move flips a mirrored pair and is scored incrementally using only the even lags. This was the biggest gain: N=127 went from about 6.0 to 7.0–7.8.
- **Even N:** it runs the skew search on N−1 for 95% of the time, extends the best results by one bit at either end, and then runs the full search on those seeds. In my tests that last phase never improved on the best extended seed, so even N relies entirely on the skew result.
- **Typical results:** about 7.0–7.8 at N=127, about 6.6–7.3 at N=139/140, and about 7.0 at N=158.

Parameter tuning (walk length, tenure, population) was very noisy, so the settings I chose are only roughly best. I left optional command-line arguments in the program for these parameters; the scorer passes only N, so the defaults apply. A one-line diagnostic also goes to stderr, which doesn't affect the printed sequence.

Sources:
- [Low-Autocorrelation Binary Sequences (arXiv:1406.5301)](https://ar5iv.arxiv.org/html/1406.5301)
- [Computational Search of Long Skew-symmetric Binary Sequences with High Merit Factors](https://ar5iv.org/html/2011.00068)
- [In Searching of Long Skew-symmetric Binary Sequences with High Merit Factors](https://deepai.org/publication/in-searching-of-long-skew-symmetric-binary-sequences-with-high-merit-factors)