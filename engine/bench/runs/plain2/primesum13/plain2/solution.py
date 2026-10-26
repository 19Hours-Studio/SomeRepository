import numpy as np
from math import isqrt

M = 1_000_000_007
CH = 1 << 15
FT = 0.2


def solve(N):
    # Lucy-Hedgehog for sum of p^2, restricted to the table entries that the final
    # answer actually depends on.  L[i] ~ Phi(N // i), S[v] ~ Phi(v).  At stage p,
    # L[i] is read later only if i == 1 or i is squarefree with all prime factors > p
    # (it is read at stage q = lpf(i) as L[(i/q) * q]); every other write is dead.
    np.seterr(over='ignore')
    r = isqrt(N)
    inv6 = pow(6, M - 2, M)
    rr = isqrt(r)

    # smallest prime factor, squarefree flag, primes up to r
    lpf = np.zeros(r + 1, dtype=np.int32)
    small = [p for p in range(2, rr + 1) if all(p % d for d in range(2, isqrt(p) + 1))]
    for p in reversed(small):
        lpf[p::p] = p
    ar = np.arange(r + 1, dtype=np.int64)
    pm = lpf == 0
    lpf[pm] = ar[pm]
    pm = lpf == ar
    pm[:2] = False
    primes = np.flatnonzero(pm)
    sqf = np.ones(r + 1, dtype=np.bool_)
    for p in small:
        sqf[p * p::p * p] = False

    def f(v):
        a = v % M
        b = (v + 1) % M
        c = (2 * v + 1) % M
        return ((a * b % M) * c % M * inv6 - 1) % M

    # values are kept lazily reduced mod M; |values| stay far below 2^53
    S = ar * ar
    S %= M
    S[1] = 0
    np.cumsum(S, out=S)
    del pm

    def mulmod(z, p2, cf):
        # z * p2 mod M up to a small multiple of M; int64 wraparound keeps it exact
        q = (z * cf).astype(np.int64)
        z *= p2
        q *= M
        z -= q
        return z

    c3 = round(N ** (1 / 3))
    while c3 ** 3 > N:
        c3 -= 1
    while (c3 + 1) ** 3 <= N:
        c3 += 1

    plist = primes.tolist()
    np_ = len(plist)
    L1 = int(f(np.array([N], dtype=np.int64))[0])

    # phase 1: p^2 <= r.  Needed indices: squarefree i > 1 with lpf(i) > p, stored
    # compactly: I (indices), lI (their lpf), LI = L[I], VI = N // I.
    I = np.flatnonzero(sqf[2:]) + 2
    lI = lpf[I]
    VI = N // I
    LI = f(VI)
    pos = np.zeros(r + 1, dtype=np.int32)
    pos[I] = np.arange(len(I), dtype=np.int32)
    t = 0
    dead = 0.0
    while t < np_ and plist[t] * plist[t] <= r and plist[t] ** 3 <= N:
        p = plist[t]
        pp = p * p
        sp = int(S[p - 1])
        p2 = pp % M
        cf = p2 / M
        k1 = r // p
        # reads of L[i*p] (lpf(i*p) == p) happen before anything is dropped or written
        L1 -= (int(LI[pos[p]]) - sp) * p2 % M
        a = int(np.searchsorted(I, k1, 'right'))
        IA = I[:a]
        rd = np.take(LI, pos[IA * p], mode='clip')
        dead += 1 / p
        if dead > FT:
            # drop entries with lpf <= p (dead from now on); they stay harmless otherwise
            dead = 0.0
            keep = lI > p
            rd = rd[keep[:a]]
            I = I[keep]
            lI = lI[keep]
            LI = LI[keep]
            VI = VI[keep]
            pos[I] = np.arange(len(I), dtype=np.int32)
            a = int(np.searchsorted(I, k1, 'right'))
        if a:
            LI[:a] -= mulmod(rd - sp, p2, cf)
        for x in range(a, len(I), CH):
            y = x + CH
            LI[x:y] -= mulmod(np.take(S, VI[x:y] // p) - sp, p2, cf)
        # S[v] -= p2 * (S[v // p] - sp) for v >= p^2
        kh = r // p
        m = mulmod(S[p:kh + 1] - sp, p2, cf)
        rows = max(1, CH // p)
        for k in range(p, kh, rows):
            e = min(k + rows, kh)
            blk = S[k * p:e * p]
            if p < 48:
                blk -= np.repeat(m[k - p:e - p], p)
            else:
                blk.reshape(-1, p)[...] -= m[k - p:e - p, None]
        S[kh * p:] -= m[-1]
        t += 1

    # phase 2: S is final, needed indices > 1 are primes in (p, N/p^2]; keep L at primes only
    LP = LI[np.searchsorted(I, primes)]
    VP = N // primes
    while t < np_ and plist[t] ** 3 <= N:
        p = plist[t]
        pp = p * p
        sp = int(S[p - 1])
        p2 = pp % M
        cf = p2 / M
        L1 -= (int(LP[t]) - sp) * p2 % M
        e = int(np.searchsorted(primes, N // pp, 'right'))
        for x in range(t + 1, e, CH):
            y = min(x + CH, e)
            LP[x:y] -= mulmod(np.take(S, VP[x:y] // p) - sp, p2, cf)
        t += 1

    # phase 3: p^3 > N only touches dead entries besides L[1]; all reads are final
    if t < np_:
        big = primes[t:]
        bp2 = big * big % M
        z = LP[t:] - S[big - 1]
        q = (z * (bp2 / M)).astype(np.int64)
        z *= bp2
        q *= M
        z -= q
        L1 -= int(z.sum())

    return L1 % M


if __name__ == "__main__":
    print(solve(10**13))
