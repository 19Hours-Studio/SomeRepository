My `solution.py` prints 659676487, and the self-check scored it **≈197×** faster than the baseline (0.42 s, value accepted).

**Approach:** Instead of sieving all 10^10 numbers, I used the Lucy_Hedgehog prime-sum algorithm, vectorized with numpy.
- It keeps the sum of k² (mod 1e9+7) only for the values ⌊N/i⌋, about 2·10⁵ of them. These start from the closed-form formula v(v+1)(2v+1)/6 − 1.
- For each prime p ≤ 10⁵, it updates every entry with v ≥ p² by S(v) −= p²·(S(v/p) − S(p−1)). Each update is one numpy array operation.
- All arithmetic is mod 1e9+7. Products of two reduced values stay below about 10¹⁸, so int64 never overflows.

**Check:** At N = 10⁷ it gives the same result as a direct sieve (304918885). The official timing on a quiet machine may differ from my noisy run, and most of the 0.42 s is Python and numpy startup.