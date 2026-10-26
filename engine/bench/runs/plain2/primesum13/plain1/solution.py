import sys
import numpy as np
from math import isqrt

# Sum of p^2 over primes p <= N, mod M, via Lucy-Hedgehog, restructured:
#  * the small table S(v), v <= sqrt(N), comes from a sieve: stage values are
#    prefix sums of the partially sieved weights, final values are P below,
#  * reads that only see final values (v < p^3) are deferred and processed
#    for groups of primes chunk by chunk (cache resident),
#  * lazy modular reduction (exact p^2 * x products, or sums of products
#    < M^2, accumulated in uint64),
#  * primes > N^(1/3) handled in one vectorised "pull" pass.

N = int(sys.argv[1]) if len(sys.argv) > 1 else 10**13
M = 1_000_000_007
U = np.uint64
UM = U(M)
r = isqrt(N)
CH = 1 << 14                     # chunk length for cache-friendly passes
OFF = U(M * (2 ** 62 // M + 1))  # multiple of M above 2^62 (signed lift)
BB = 8                           # log2 block size of the two-level prefix
BS = 1 << BB


def icbrt(n):
    c = int(round(n ** (1 / 3)))
    while c ** 3 > n:
        c -= 1
    while (c + 1) ** 3 <= n:
        c += 1
    return c


def modu(a):
    return a - (a // UM) * UM


def modu_(a):
    np.subtract(a, (a // UM) * UM, out=a)


# ---- primes up to r and final prime-square prefix sums P[w], w <= r
sv = np.ones(r + 1, dtype=np.bool_)
sv[:2] = False
for i in range(2, isqrt(r) + 1):
    if sv[i]:
        sv[i * i::i] = False
primes = np.nonzero(sv)[0]
nn = np.arange(r + 1, dtype=U)
sq = nn * nn
modu_(sq)                                   # n^2 mod M
P = np.cumsum(np.where(sv, sq, U(0)))
modu_(P)
P_i = P.view(np.int64)

# ---- large table T[i] ~ S(N // i), i = 1..r
Vu = np.zeros(r + 1, dtype=U)
Vu[1:] = U(N) // nn[1:]
V = Vu.view(np.int64)
inv6 = pow(6, M - 2, M)
T = modu(Vu)
T *= modu(Vu + U(1))
modu_(T)
T *= modu(U(2) * Vu + U(1))
modu_(T)
T *= U(inv6)
T += U(M - 1)
modu_(T)
T[0] = 0

nW = ((r >> BB) + 1) << BB
W = np.zeros(nW, dtype=U)
W[:r + 1] = sq
W[:2] = 0
del sq, nn

qb = np.empty(CH, dtype=np.int64)
qbu = qb.view(U)
xb = np.empty(CH, dtype=U)
yb = np.empty(CH, dtype=U)


def reduce_range(lo, hi, lift):
    for s in range(lo, hi + 1, CH):
        e = min(hi + 1, s + CH)
        t = T[s:e]
        if lift:
            t += OFF
        modu_(t)


def add_consts(ranges):
    # ranges: list of (lo, hi, c): T[lo+1 .. hi] += c
    if not ranges:
        return
    d = {}
    for lo, hi, c in ranges:
        d[lo] = (d.get(lo, 0) + c) % M
        d[hi] = (d.get(hi, 0) - c) % M
    pts = sorted(d)
    acc = 0
    for k in range(len(pts) - 1):
        acc = (acc + d[pts[k]]) % M
        if acc:
            T[pts[k] + 1:pts[k + 1] + 1] += U(acc)


def pending(j, defs, sign):
    # true value (mod M) of deferred updates at indices j
    out = np.zeros(len(j), dtype=U)
    for (lo, hi, p, m, c) in defs:
        cnt = np.searchsorted(j, hi, side='right')
        st = np.searchsorted(j, lo, side='right')
        if cnt > st:
            jj = j[st:cnt]
            x = modu(P[Vu[jj] // U(p)] * U(m))
            if sign < 0:
                x = UM - x
            out[st:cnt] += modu(x + U(c))
    return out


def run_deferred(defs, sub):
    lo_all = min(d[0] for d in defs)
    hi_all = max(d[1] for d in defs)
    op = np.subtract if sub else np.add
    for s0 in range(lo_all + 1, hi_all + 1, CH):
        e0 = min(hi_all + 1, s0 + CH)
        tt = T[s0:e0]
        for (lo, hi, p, m, c) in defs:
            s = max(s0, lo + 1)
            e = min(e0, hi + 1)
            if s >= e:
                continue
            n = e - s
            q = qbu[:n]
            np.floor_divide(Vu[s:e], U(p), out=q)
            xx = xb[:n]
            np.take(P, qb[:n], out=xx)
            xx *= U(m)
            t = tt[s - s0:e - s0]
            op(t, xx, out=t)


c3 = icbrt(N)
pa = icbrt(r)               # p <= pa: every small read is a stage value
pb = isqrt(r)               # p <= pb: small table still being sieved
plist = [int(p) for p in primes if p <= c3]
pidx = 0

# ---- phase A: p <= r^(1/3); dense stage prefix sums, exact p^2 * x terms
# (no reduction until the end: each prime subtracts < 2^45 per entry)
constsA = []
while pidx < len(plist) and plist[pidx] <= pa:
    p = plist[pidx]
    pidx += 1
    pp = p * p
    lim = min(r, N // pp)
    k1 = min(lim, r // p)
    sp = int(P[p - 1])
    c = pp * sp % M
    # strided reads of the large table: lift, add pending constants
    x = T[p:k1 * p + 1:p] + OFF
    for (lo, hi, c2) in constsA:
        st = lo // p           # i*p > lo  <=>  i > lo // p
        if st < k1:
            x[st:] += U(c2)
    x = modu(x)
    x = modu(modu(x) * U(pp))
    T[1:k1 + 1] += modu(U(M + c) - x)
    if lim > k1:
        C = np.cumsum(W[:r + 1])
        modu_(C)
        for s in range(k1 + 1, lim + 1, CH):
            e = min(lim + 1, s + CH)
            n = e - s
            np.floor_divide(Vu[s:e], U(p), out=qbu[:n])
            xx = xb[:n]
            np.take(C, qb[:n], out=xx)
            xx *= U(pp)
            t = T[s:e]
            t -= xx
        constsA.append((k1, lim, c))
    W[pp::p] = 0
add_consts(constsA)
reduce_range(1, r, True)

# ---- phase B: r^(1/3) < p <= r^(1/2); two-level prefix sums of the sieve
W2 = W.reshape(-1, BS)
WP = np.cumsum(W2, axis=1)                # within-block inclusive prefix
bsum = WP[:, -1].copy()
WPf = WP.reshape(-1)
GB = 64
while pidx < len(plist) and plist[pidx] <= pb:
    grp = []
    while pidx < len(plist) and plist[pidx] <= pb and len(grp) < GB:
        grp.append(plist[pidx])
        pidx += 1
    defs = []
    consts = []
    top = 0
    for p in grp:
        pp = p * p
        lim = min(r, N // pp)
        k1 = min(lim, r // p)
        top = max(top, lim)
        sp = int(P[p - 1])
        c = pp * sp % M
        # strided reads: T (possibly lifted negative) + deferred pending
        j = np.arange(p, k1 * p + 1, p, dtype=np.int64)
        x = T[j] + OFF + pending(j, defs, -1)
        x = modu(modu(x) * U(pp))
        x = modu(U(M + c) - x)
        T[1:k1 + 1] += x
        i0 = max(k1, min(lim, N // (pp * p)))
        if i0 > k1:
            bc = np.cumsum(bsum)
            bc -= bsum
            for s in range(k1 + 1, i0 + 1, CH):
                e = min(i0 + 1, s + CH)
                n = e - s
                q = qb[:n]
                np.floor_divide(Vu[s:e], U(p), out=qbu[:n])
                xx = xb[:n]
                yy = yb[:n]
                np.take(WPf, q, out=xx)
                np.right_shift(q, BB, out=q)
                np.take(bc, q, out=yy)
                xx += yy
                modu_(xx)
                xx *= U(pp)
                t = T[s:e]
                t -= xx
            T[k1 + 1:i0 + 1] += U(c)        # read later by strided reads
        # sieve out multiples of p with least prime factor p
        idx = np.arange(pp, r + 1, p, dtype=np.int64)
        w = W[idx]
        nz = w != 0
        idx = idx[nz]
        w = w[nz]
        if len(idx):
            W[idx] = 0
            blk = idx >> BB
            ub, inv = np.unique(blk, return_inverse=True)
            D = np.zeros((len(ub), BS), dtype=U)
            D[inv, idx & (BS - 1)] = w
            np.cumsum(D, axis=1, out=D)
            WP[ub] -= D
            bsum[ub] -= D[:, -1]
        if lim > i0:
            defs.append((i0, lim, p, pp, c))
            consts.append((i0, lim, c))
    if defs:
        run_deferred(defs, True)
    add_consts(consts)
    reduce_range(1, top, True)

# ---- phase C: r^(1/2) < p <= N^(1/3); small reads all final
GC = 16
while pidx < len(plist):
    grp = plist[pidx:pidx + GC]
    pidx += len(grp)
    defs = []
    consts = []
    top = 0
    for p in grp:
        pp = p * p
        lim = min(r, N // pp)
        k1 = min(lim, r // p)
        top = max(top, lim)
        m = M - pp % M
        k = M - int(P[p - 1])
        c = m * k % M
        j = np.arange(p, k1 * p + 1, p, dtype=np.int64)
        x = T[j] + pending(j, defs, 1) + U(k)
        x = modu(modu(x) * U(m))
        T[1:k1 + 1] += x
        if lim > k1:
            defs.append((k1, lim, p, m, c))
            consts.append((k1, lim, c))
    if defs:
        run_deferred(defs, False)
    add_consts(consts)
    reduce_range(1, top, False)

T_i = T.view(np.int64)

# ---- phase D: primes p > N^(1/3); every read is final (v < p^3), pull per i
p_hi = c3
big = primes[primes > p_hi].astype(np.int64)
imax = min(r, N // (p_hi + 1) ** 2)
if len(big) and imax >= 1:
    bmu = (M - (big * big) % M).astype(U)                       # multiplier
    cst = (bmu.view(np.int64) * (M - P_i[big - 1])) % M         # constant
    ccum = np.concatenate(([0], np.cumsum(cst) % M))
    bf = big.astype(np.float64)
    Vf = V.astype(np.float64)
    vv = V[1:imax + 1]
    sr = np.sqrt(vv.astype(np.float64)).astype(np.int64)
    sr -= (sr * sr > vv)
    sr += ((sr + 1) * (sr + 1) <= vv)
    cnt = np.zeros(imax + 1, dtype=np.int64)
    cnt[1:] = np.searchsorted(big, sr, side='right')
    i_small = min(imax, r // (p_hi + 1))   # i <= i_small may read T[i*p]
    LIM = 1 << 18
    # i > i_small: reads only from P; rectangular blocks [a, b] of i
    a = imax
    while a > i_small:
        b = a
        K = int(cnt[a])
        while b - 1 > i_small and cnt[b - 1] * 25 <= K * 26 + 25 and (a - b + 2) * int(cnt[b - 1]) <= LIM:
            b -= 1
        K = int(cnt[b])
        if K:
            q = (Vf[b:a + 1, None] / bf[None, :K]).astype(np.int64)
            q = np.minimum(q, r, out=q)
            xv = P[q]
            xv *= bmu[None, :K]
            modu_(xv)
            cs = np.cumsum(xv, axis=1)
            cc = cnt[b:a + 1]
            sel = cs[np.arange(a + 1 - b), np.maximum(cc - 1, 0)]
            sel = np.where(cc > 0, sel % UM, U(0))
            T[b:a + 1] = modu(T[b:a + 1] + sel + ccum[cc].astype(U))
        a = b - 1
    # i <= i_small: ragged, mixed reads, high to low
    i = i_small
    LIM = 1 << 20
    bm = bmu.view(np.int64)
    while i >= 1:
        # block [j, i]: reads T[i'*p] need i'*p > i (already final)
        j = i
        tot = int(cnt[i])
        while j > 1 and tot + int(cnt[j - 1]) <= LIM and (j - 1) * (p_hi + 1) > i:
            j -= 1
            tot += int(cnt[j])
        if tot:
            cc = cnt[j:i + 1]
            ends = np.cumsum(cc)
            start = ends - cc
            rep = np.repeat(np.arange(j, i + 1), cc)
            pk = np.arange(tot) - np.repeat(start, cc)
            q = (Vf[rep] / bf[pk]).astype(np.int64)
            ip = rep * big[pk]
            xv = np.where(ip <= r, T_i[np.minimum(ip, r)], P_i[np.minimum(q, r)])
            xv *= bm[pk]
            xv %= M
            cs = np.concatenate(([0], np.cumsum(xv)))
            seg = cs[ends] - cs[start]
            T_i[j:i + 1] = (T_i[j:i + 1] + seg % M + ccum[cc]) % M
        i = j - 1

print(int(T[1]) % M)
