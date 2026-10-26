import numpy as np
from math import isqrt

M = 1_000_000_007


def solve(N):
    r = isqrt(N)
    inv6 = pow(6, M - 2, M)

    # primes up to r
    isp = np.ones(r + 1, dtype=np.bool_)
    isp[:2] = False
    for i in range(2, isqrt(r) + 1):
        if isp[i]:
            isp[i * i::i] = False
    primes = np.nonzero(isp)[0]

    # S[v] ~ sum_{2<=i<=v} i^2, lazily reduced
    ar = np.arange(r + 1, dtype=np.int64)
    a = ar % M
    b = (ar + 1) % M
    c = (2 * ar + 1) % M
    S = ((a * b % M) * c % M * inv6 - 1) % M
    S[0] = 0

    # L[i] ~ f(N // i), lazily reduced
    V = np.zeros(r + 1, dtype=np.int64)
    V[1:] = N // ar[1:]
    a = V % M
    b = (V + 1) % M
    c = (2 * V + 1) % M
    L = ((a * b % M) * c % M * inv6 - 1) % M
    del a, b, c

    def mulmod(z, p2, cf):
        # z * p2 mod M, result in (-M, M) roughly; int64 wraparound is exact
        q = (z * cf).astype(np.int64)
        z *= p2
        q *= M
        z -= q
        return z

    np.seterr(over='ignore')
    pi_list = primes.tolist()
    for p in pi_list:
        pp = p * p
        if pp * p > N:
            break
        sp = int(S[p - 1])
        p2 = pp % M
        cf = p2 / M
        lim = min(r, N // pp)
        k1 = min(lim, r // p)
        # part A: i in [1, k1], uses L[i*p]
        z = L[p:k1 * p + 1:p] - sp
        L[1:k1 + 1] -= mulmod(z, p2, cf)
        if lim > k1:
            Np = N // p
            B = isqrt(Np)
            i1 = min(max(B, k1), lim)
            if i1 > k1:
                idx = V[k1 + 1:i1 + 1] // p
                z = S[idx] - sp
                L[k1 + 1:i1 + 1] -= mulmod(z, p2, cf)
            if lim > i1:
                i0 = i1 + 1
                qmax = Np // i0
                qmin = Np // lim
                z = S[qmin:qmax + 1] - sp
                m = mulmod(z, p2, cf)
                qs = np.arange(qmin, qmax + 1, dtype=np.int64)
                hi = np.minimum(Np // qs, lim)
                lo = np.maximum(Np // (qs + 1), i0 - 1)
                cnt = hi - lo
                L[i0:lim + 1] -= np.repeat(m[::-1], cnt[::-1])
        if pp <= r:
            # S[v] -= p2 * (S[v // p] - sp) for v >= p^2
            kh = r // p
            m = mulmod(S[p:kh + 1] - sp, p2, cf)
            blk = S[pp:kh * p].reshape(-1, p)
            if p < 48:
                mm = m[:-1]
                for c in range(p):
                    blk[:, c] -= mm
            else:
                blk -= m[:-1, None]
            S[kh * p:] -= m[-1]

    # primes with p^3 > N: all needed values are final; batch over (i, p) pairs
    c3 = round(N ** (1 / 3))
    while c3 ** 3 > N:
        c3 -= 1
    while (c3 + 1) ** 3 <= N:
        c3 += 1
    big = primes[primes > c3]
    if len(big):
        cnts = N // (big * big)
        imax = int(cnts[0])
        acc = np.zeros(imax + 1, dtype=np.float64)
        CH = 1 << 22
        start = 0
        nb = len(big)
        while start < nb:
            cs = np.cumsum(cnts[start:])
            end = start + max(1, int(np.searchsorted(cs, CH)))
            end = min(end, nb)
            pg = big[start:end]
            cg = cnts[start:end]
            tot = int(cg.sum())
            pr = np.repeat(pg, cg)
            off = np.repeat(np.cumsum(cg) - cg, cg)
            ii = np.arange(1, tot + 1, dtype=np.int64) - off
            j = ii * pr
            sm = j <= r
            F = np.empty(tot, dtype=np.int64)
            F[sm] = L[j[sm]]
            nm = ~sm
            F[nm] = S[N // j[nm]]
            F -= S[pr - 1]
            p2 = pr * pr % M
            q = (F * (p2 / M)).astype(np.int64)
            F *= p2
            q *= M
            F -= q
            acc += np.bincount(ii, weights=F.astype(np.float64), minlength=imax + 1)
            start = end
        L[1:imax + 1] -= acc[1:].astype(np.int64)

    return int(L[1]) % M


if __name__ == "__main__":
    print(solve(10**13))
