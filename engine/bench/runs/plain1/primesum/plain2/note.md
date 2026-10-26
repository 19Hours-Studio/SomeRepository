I wrote `solution.py`, and it runs in about 0.33 s. The self-check (`score.py primesum .`) reports `ok: true` and a score of about **251**. The machine is shared, so that timing is noisy.

**Approach:** instead of sieving all 10^10 numbers like the baseline, I used the Lucy_Hedgehog prime-sum method, vectorized with numpy. It only needs sums at the values ⌊N/k⌋, which is about 2·10^5 of them:
- Each value v starts as the sum of i² for 2 ≤ i ≤ v, worked out mod 1,000,000,007 from the closed formula with a modular inverse of 6.
- Then, for each prime p up to √N (about 9,600 primes), every sum with v ≥ p² is reduced by p²·(S(⌊v/p⌋) − S(p−1)), so multiples of p drop out.
- Two numpy arrays hold the sums: one for small v ≤ 10^5 and one for the large values N//i. Each prime's update is a handful of slice operations. The small-array update uses `np.repeat` because ⌊v/p⌋ stays the same for runs of p consecutive values.
- All arithmetic stays in int64 mod M, so nothing overflows.

**Checks:** for N = 100, 1000, 99,999 and 10^6, the same code gives exactly the same results as a brute-force sieve. For N = 10^10 it prints 659676487, and the self-check scorer marked that value correct.

Most of the 0.33 s is probably Python and numpy start-up, so I didn't try to make it faster.