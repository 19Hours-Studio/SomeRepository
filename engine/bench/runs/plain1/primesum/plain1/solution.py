import numpy as np

def main():
    N = 10**10
    M = 1000000007
    r = int(N**0.5)
    while r * r > N: r -= 1
    while (r + 1) * (r + 1) <= N: r += 1
    inv6 = pow(6, M - 2, M)

    def f(v):
        # sum_{k=2}^{v} k^2 mod M, v as int64 array
        a = v % M
        return (a * ((v + 1) % M) % M * ((2 * v + 1) % M) % M * inv6 - 1) % M

    small = f(np.arange(r + 1, dtype=np.int64))
    small[0] = 0
    small[1] = 0
    idx = np.arange(r + 1, dtype=np.int64)
    idx[0] = 1
    large = f(N // idx)
    large[0] = 0

    sieve = np.ones(r + 1, dtype=bool)
    sieve[:2] = False
    for i in range(2, int(r**0.5) + 1):
        if sieve[i]:
            sieve[i*i::i] = False
    primes = np.nonzero(sieve)[0].tolist()

    for p in primes:
        p2 = p * p
        if p2 > N:
            break
        sp = int(small[p - 1])
        pp = p2 % M
        L = min(r, N // p2)
        k = min(L, r // p)
        # i in 1..k: large[i*p]
        t = large[p:k * p + 1:p] - sp
        t %= M
        t *= pp
        t %= M
        seg = large[1:k + 1]
        seg -= t
        seg %= M
        if L > k:
            ii = np.arange(k + 1, L + 1, dtype=np.int64)
            t = small[(N // p) // ii] - sp
            t %= M
            t *= pp
            t %= M
            seg = large[k + 1:L + 1]
            seg -= t
            seg %= M
        if p2 <= r:
            v = np.arange(p2, r + 1, dtype=np.int64)
            t = small[v // p] - sp
            t %= M
            t *= pp
            t %= M
            seg = small[p2:r + 1]
            seg -= t
            seg %= M
    print(int(large[1]) % M)

main()
