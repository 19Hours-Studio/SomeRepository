import numpy as np
from math import isqrt

N, M = 10**13, 1_000_000_007
r = isqrt(N)
inv6 = pow(6, M - 2, M)


def f(v):
    a = v % M
    b = (v + 1) % M
    c = (2 * v + 1) % M
    return ((a * b % M) * c % M * inv6 - 1) % M


S = f(np.arange(r + 1, dtype=np.int64))
S[0] = 0
S[1] = 0
idx = np.arange(1, r + 1, dtype=np.int64)
L = np.zeros(r + 1, dtype=np.int64)
L[1:] = f(N // idx)

for p in range(2, r + 1):
    if S[p] == S[p - 1]:
        continue
    pp = p * p
    if pp > N:
        break
    sp = int(S[p - 1])
    p2 = pp % M
    lim = min(r, N // pp)
    k1 = min(lim, r // p)
    L[1:k1 + 1] = (L[1:k1 + 1] - p2 * ((L[p:k1 * p + 1:p] - sp) % M)) % M
    if lim > k1:
        q = N // (idx[k1:lim] * p)
        L[k1 + 1:lim + 1] = (L[k1 + 1:lim + 1] - p2 * ((S[q] - sp) % M)) % M
    if pp <= r:
        t = np.repeat(S[p:r // p + 1], p)[:r + 1 - pp]
        S[pp:] = (S[pp:] - p2 * ((t - sp) % M)) % M

print(int(L[1]) % M)
