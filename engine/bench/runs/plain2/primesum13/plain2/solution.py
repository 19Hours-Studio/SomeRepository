import numpy as np
from math import isqrt

M = 1_000_000_007
CH = 1 << 15
PL = 200
GF = 1.0
PB = 300
CAP = 1 << 22
C1 = 1.5


def solve(N):
    np.seterr(over='ignore')
    r = isqrt(N)
    inv6 = pow(6, M - 2, M)

    # primes up to r
    isp = np.ones(r + 1, dtype=np.bool_)
    isp[:2] = False
    for i in range(2, isqrt(r) + 1):
        if isp[i]:
            isp[i * i::i] = False
    primes = np.nonzero(isp)[0]

    def f(v):
        a = v % M
        b = (v + 1) % M
        c = (2 * v + 1) % M
        return ((a * b % M) * c % M * inv6 - 1) % M

    # Lucy tables, lazily reduced mod M (|values| stay well below 2^53):
    # S[v] ~ Phi(v) for v <= r, L[i] ~ Phi(N // i) for i <= r
    ar = np.arange(r + 1, dtype=np.int64)
    S = f(ar)
    S[0] = 0
    V = np.zeros(r + 1, dtype=np.int64)
    V[1:] = N // ar[1:]
    L = f(V)
    L[0] = 0

    def mulsub(dst, z, p2, cf):
        # dst -= z * p2 (mod M); z is consumed. int64 wraparound keeps it exact.
        q = (z * cf).astype(np.int64)
        z *= p2
        dst -= z
        q *= M
        dst += q

    def mulmod(z, p2, cf):
        q = (z * cf).astype(np.int64)
        z *= p2
        q *= M
        z -= q
        return z

    # greatest prime factor for i <= sqrt(N / PB)
    G = min(r, int(C1 * isqrt(N // PB))) + 2
    gpf = np.arange(G, dtype=np.int64)
    for p in primes[primes < G].tolist():
        gpf[p::p] = p
    gpf[1] = N

    c3 = round(N ** (1 / 3))
    while c3 ** 3 > N:
        c3 -= 1
    while (c3 + 1) ** 3 <= N:
        c3 += 1

    # Lazy step-function updates of L: true L = L - cumsum(D) - (pending corrections).
    Vf = V.astype(np.float64)
    D = np.zeros(r + 2, dtype=np.int64)
    Mbuf = np.zeros(1 << 20, dtype=np.int64)
    Vf_tmp = np.empty(r + 1, dtype=np.float64)
    pend = []  # (p, i0, lim, qmax + off)
    st = {'mp': 1, 'lo': r + 1, 'hi': 0}

    def flush():
        lo, hi = st['lo'], st['hi']
        carry = 0
        for a in range(lo, hi + 1, CH):
            b = min(a + CH, hi + 1)
            t = np.cumsum(D[a:b])
            t += carry
            carry = int(t[-1])
            L[a:b] -= t
        D[lo:hi + 2] = 0
        pend.clear()
        st['mp'] = 1
        st['lo'] = r + 1
        st['hi'] = 0

    for p in primes[primes <= c3].tolist():
        pp = p * p
        sp = int(S[p - 1])
        p2 = pp % M
        cf = p2 / M
        lim = min(r, N // pp)
        k1 = min(lim, r // p)
        if pend and (st['mp'] > CAP or (pp <= r and len(pend) >= GF * p ** 0.5)):
            flush()
        # part A: i in {1} u (p, k1], uses L[i*p]; other i are p-smooth and never read again
        if k1 > p:
            if p >= PB:
                ia = np.flatnonzero(gpf[p + 1:k1 + 1] > p)
                ia += p + 1
            else:
                ia = np.arange(p + 1, k1 + 1, dtype=np.int64)
            ia = np.concatenate((np.ones(1, dtype=np.int64), ia))
        else:
            ia = np.ones(1, dtype=np.int64)
        if pend:
            pa = np.array(pend, dtype=np.int64)
            pf = pa[:, 0].astype(np.float64)[:, None]
            pi0 = pa[:, 1:2]
            plim = pa[:, 2:3]
            pqo = pa[:, 3:4]
            rows = max(1, CH // len(pend))
        else:
            rows = CH
        for a in range(0, len(ia), rows):
            I = ia[a:a + rows]
            J = I * p
            z = L[J] - sp
            if pend:
                Q = (Vf[J] / pf).astype(np.int64)
                Q += pqo
                Q[(J < pi0) | (J > plim)] = 0
                z -= Mbuf[Q].sum(axis=0)
            L[I] -= mulmod(z, p2, cf)
        if lim > k1:
            Np = N // p
            i1 = min(max(int(C1 * isqrt(Np)) if p >= PB else isqrt(Np), k1), lim)
            # part B direct: i in (k1, i1], uses S[N // (i*p)]
            if p >= PB:
                # only i with a prime factor > p are ever read again
                for a in range(k1 + 1, i1 + 1, CH):
                    b = min(a + CH, i1 + 1)
                    idx = np.flatnonzero(gpf[a:b] > p)
                    idx += a
                    L[idx] -= mulmod(S[V[idx] // p] - sp, p2, cf)
            else:
                for a in range(k1 + 1, i1 + 1, CH):
                    b = min(a + CH, i1 + 1)
                    mulsub(L[a:b], S[V[a:b] // p] - sp, p2, cf)
            # part B expanded: i in (i1, lim], N // (i*p) = q takes few values
            if lim > i1:
                i0 = i1 + 1
                qmax = Np // i0
                qmin = Np // lim
                if p >= PL:
                    m = mulmod(S[qmin:qmax + 1] - sp, p2, cf)
                    nm = len(m)
                    mp = st['mp']
                    if mp + nm > len(Mbuf):
                        Mbuf = np.concatenate((Mbuf, np.zeros(max(nm, len(Mbuf)), dtype=np.int64)))
                    Mbuf[mp:mp + nm] = m
                    pend.append((p, i0, lim, mp - qmin))
                    st['mp'] = mp + nm
                    st['lo'] = min(st['lo'], i0)
                    st['hi'] = max(st['hi'], lim)
                    # step value m[q] on i in [N//(p(q+1)) + 1, N//(pq)]
                    starts = np.empty(nm, dtype=np.int64)
                    np.divide(float(Np), np.arange(qmin + 1, qmax + 1, dtype=np.float64), out=Vf_tmp[:nm - 1])
                    starts[:-1] = Vf_tmp[:nm - 1]
                    starts[:-1] += 1
                    starts[-1] = i0
                    m[:-1] -= m[1:]
                    D[starts] += m
                    D[lim + 1] -= int(Mbuf[mp])
                else:
                    m = mulmod(S[qmin:qmax + 1] - sp, p2, cf)[::-1].copy()
                    qs = np.arange(qmax, qmin - 1, -1, dtype=np.int64)
                    cs = np.empty(len(qs) + 1, dtype=np.int64)
                    cs[0] = i0
                    cs[1:] = np.minimum(Np // qs, lim) + 1
                    cnt = cs[1:] - cs[:-1]
                    bl = np.searchsorted(cs, np.arange(i0, lim + 1, CH), 'right') - 1
                    bl = bl.tolist()
                    bl.append(len(qs))
                    csl = cs.tolist()
                    for x, y in zip(bl[:-1], bl[1:]):
                        if x < y:
                            L[csl[x]:csl[y]] -= np.repeat(m[x:y], cnt[x:y])
        if pp <= r:
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

    if pend:
        flush()

    # primes with p^3 > N: every value they read is already final
    big = primes[primes > c3]
    if len(big):
        bp2 = big * big % M
        bcf = bp2 / M
        bsp = S[big - 1]
        bf = big.astype(np.float64)
        imax = N // (int(big[0]) ** 2)
        I0 = min(imax, 1500)
        acc = np.zeros(imax + 1, dtype=np.int64)
        MM = np.int64(M)
        # small i: vectorize over primes p in (c3, sqrt(N/i)]
        for i in range(1, I0 + 1):
            e = int(np.searchsorted(big, isqrt(N // i), 'right'))
            if e == 0:
                break
            c = min(e, int(np.searchsorted(big, r // i, 'right')))
            tot = np.int64(0)
            if c:
                z = L[big[:c] * i] - bsp[:c]
                q = (z * bcf[:c]).astype(np.int64)
                tot += np.dot(z, bp2[:c]) - MM * q.sum()
            if e > c:
                idx = (float(V[i]) / bf[c:e]).astype(np.int64)
                z = S[idx] - bsp[c:e]
                q = (z * bcf[c:e]).astype(np.int64)
                tot += np.dot(z, bp2[c:e]) - MM * q.sum()
            acc[i] = -(int(tot) % M)
        # larger i: vectorize over i in (I0, N/p^2] for each p
        e = int(np.searchsorted(big, isqrt(N // (I0 + 1)), 'right'))
        for t in range(e):
            p = int(big[t])
            lim = N // (p * p)
            if lim <= I0:
                break
            sp = int(bsp[t])
            p2 = int(bp2[t])
            cf = float(bcf[t])
            k1 = min(lim, r // p)
            a = I0 + 1
            if k1 >= a:
                mulsub(acc[a:k1 + 1], L[a * p:k1 * p + 1:p] - sp, p2, cf)
                a = k1 + 1
            if lim >= a:
                idx = (Vf[a:lim + 1] / p).astype(np.int64)
                mulsub(acc[a:lim + 1], S[idx] - sp, p2, cf)
        L[1:imax + 1] += acc[1:]

    return int(L[1]) % M


if __name__ == "__main__":
    print(solve(10**13))
