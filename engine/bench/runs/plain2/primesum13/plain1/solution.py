import sys
import numpy as np
from math import isqrt

# Sum of p^2 over primes p <= N, mod M, via Lucy-Hedgehog where only the
# needed states are computed.
#
# Lucy: T(v) <- T(v) - p^2 (S_{p-1}(v/p) - S(p-1)) for v = N//i >= p^2.  The
# entry for v = N//i is read again only at stage p by i/p (p | i).  Hence
# entry i (> 1) is needed iff i is squarefree, and then only the updates of
# primes p < lpf(i) matter (the entry is read at stage lpf(i)); entry 1 needs
# all.  This keeps ~1e8 of the ~2e9 updates.  The small table S_{p-1}(w),
# w <= sqrt(N), is a sieve: stage values are prefix sums of the partially
# sieved weights (dense for tiny p, two-level blocks later) and the final
# prime-square prefix sums P (when w < p^2).  Primes > N^(1/3) only update
# entry 1, done in one vectorised sum at the end.  Updates are accumulated
# lazily (< 16 products < M^2 per uint64) and reduced in batches.

N = int(sys.argv[1]) if len(sys.argv) > 1 else 10**13
M = 1_000_000_007
U = np.uint64
UM = U(M)
r = isqrt(N)
BB = 5                           # log2 block size of the two-level prefix
BS = 1 << BB
P_DENSE = 64                     # p < P_DENSE: rebuild prefix sums after sieving
CH = 1 << 15                     # chunk length for cache-friendly passes
WIN = 16                         # lazy terms < M^2 per entry before reduction


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


# ---- sieve to r: primes, least prime factors, squarefree flags
lpf = np.zeros(r + 1, dtype=np.int32)
sqf = np.ones(r + 1, dtype=np.bool_)
for i in range(2, isqrt(r) + 1):
    if lpf[i] == 0:
        seg = lpf[i * i::i]
        seg[seg == 0] = i
        sqf[i * i::i * i] = False
isp = lpf == 0
isp[:2] = False
primes = np.nonzero(isp)[0]
nW = ((r >> BB) + 1) << BB
W = np.zeros(nW, dtype=U)                   # sieve weights n^2 mod M
nn = np.arange(r + 1, dtype=U)
np.multiply(nn, nn, out=W[:r + 1])
del nn
modu_(W)
W[:2] = 0
P = np.cumsum(np.where(isp[:r + 1], W[:r + 1], U(0)))
modu_(P)

# ---- needed large-table entries (squarefree i), sorted by i
Ic = np.flatnonzero(sqf).astype(np.int32)[1:]          # drop 0
Lc = lpf[Ic]
np.copyto(Lc, Ic, where=Lc == 0)            # primes: lpf = itself
Lc[0] = 2 ** 31 - 1                         # entry 1 never dies
del lpf, sqf, isp
Vc = (float(N) / Ic.astype(np.float64)).astype(U)     # exact floor
inv6 = pow(6, M - 2, M)
Tc = modu(Vc)
Tc *= modu(Vc + U(1))
modu_(Tc)
Tc *= modu(U(2) * Vc + U(1))
modu_(Tc)
Tc *= U(inv6)
Tc += U(M - 1)
modu_(Tc)
pos = np.zeros(r + 1, dtype=np.int32)
pos[Ic] = np.arange(len(Ic), dtype=np.int32)

qb = np.empty(CH, dtype=np.int64)
qbu = qb.view(U)
xb = np.empty(CH, dtype=U)
yb = np.empty(CH, dtype=U)
window = []           # (n_lim, const) since the last reduction


def flush():
    # add pending constants (prefix ranges) and reduce
    global window
    if not window:
        return
    window.sort(key=lambda w: -w[0])
    acc = 0
    for k in range(len(window)):
        acc = (acc + window[k][1]) % M
        hi = window[k][0]
        lo = window[k + 1][0] if k + 1 < len(window) else 0
        if hi > lo and acc:
            Tc[lo:hi] += U(acc)
    top = window[0][0]
    for s in range(0, top, CH):
        t = Tc[s:min(top, s + CH)]
        modu_(t)
    window = []


c3 = icbrt(N)
garbage = 0
W2 = W.reshape(-1, BS)
WP = np.cumsum(W2, axis=1)                  # within-block inclusive prefix
bsum = WP[:, -1].copy()
WPf = WP.reshape(-1)
for p in primes:
    p = int(p)
    if p > c3:
        break
    pp = p * p
    lim = min(r, N // pp)
    k1 = min(lim, r // p)
    i0 = max(k1, min(lim, N // (pp * p)))   # i <= i0: small read is a stage value
    sp = int(P[p - 1])
    m = M - pp % M
    um = U(m)
    # compact away dead entries (lpf < p) once they pile up
    if garbage * 4 > len(Ic):
        flush()
        keep = Lc >= p
        Ic = Ic[keep]
        Lc = Lc[keep]
        Vc = Vc[keep]
        Tc = Tc[keep]
        pos[Ic] = np.arange(len(Ic), dtype=np.int32)
        garbage = 0
    n_lim = int(np.searchsorted(Ic, np.int32(lim), side='right'))
    n_k1 = int(np.searchsorted(Ic, np.int32(k1), side='right'))
    n_i0 = int(np.searchsorted(Ic, np.int32(i0), side='right'))
    # large-table reads: entry i*p (squarefree with lpf p when i is alive)
    if n_k1:
        ps_ = pos[Ic[:n_k1] * p]
        x = Tc[ps_]
        if window:                      # pending constants at those positions
            cnt = np.searchsorted(ps_, np.array([w[0] for w in window], dtype=np.int32))
            d = np.bincount(cnt, weights=[w[1] for w in window], minlength=n_k1 + 1)
            x += np.cumsum(d[::-1])[n_k1 - 1::-1].astype(U)
        x = modu(x)
        x *= um
        Tc[:n_k1] += x
    # small-table stage values
    if n_i0 > n_k1:
        bc = np.cumsum(bsum)
        bc -= bsum
        for s in range(n_k1, n_i0, CH):
            e = min(n_i0, s + CH)
            n = e - s
            q = qb[:n]
            np.floor_divide(Vc[s:e], U(p), out=qbu[:n])
            xx = xb[:n]
            yy = yb[:n]
            np.take(WPf, q, out=xx)
            np.right_shift(q, BB, out=q)
            np.take(bc, q, out=yy)
            xx += yy
            modu_(xx)
            xx *= um
            t = Tc[s:e]
            t += xx
    # final small-table values
    for s in range(n_i0, n_lim, CH):
        e = min(n_lim, s + CH)
        n = e - s
        q = qb[:n]
        np.floor_divide(Vc[s:e], U(p), out=qbu[:n])
        xx = xb[:n]
        np.take(P, q, out=xx)
        xx *= um
        t = Tc[s:e]
        t += xx
    window.append((n_lim, m * (M - sp) % M))
    if len(window) >= WIN:
        flush()
    garbage += n_k1          # entries i*p (lpf p) are dead from now on
    # sieve the small table by p
    if pp > r:
        continue
    if p < P_DENSE:
        W[pp::p] = 0
        np.cumsum(W2, axis=1, out=WP)
        bsum[:] = WP[:, -1]
        continue
    idx = np.arange(pp, r + 1, p, dtype=np.int64)
    w = W[idx]
    nz = np.flatnonzero(w)
    if len(nz):
        idx = idx[nz]
        w = w[nz]
        W[idx] = 0
        blk = idx >> BB
        ch = np.empty(len(blk), dtype=np.bool_)
        ch[0] = True
        np.not_equal(blk[1:], blk[:-1], out=ch[1:])
        ub = blk[ch]
        inv = np.cumsum(ch) - 1
        D = np.zeros((len(ub), BS), dtype=U)
        D[inv, idx & (BS - 1)] = w
        np.cumsum(D, axis=1, out=D)
        WP[ub] -= D
        bsum[ub] -= D[:, -1]
flush()

# ---- primes p > N^(1/3): only entry 1 is updated, reading final T[p]
big = primes[primes > c3]
res = int(Tc[0])
if len(big):
    tp = Tc[pos[big]].view(np.int64)
    bm = (big.astype(np.int64) ** 2) % M
    d = (tp - P[big - 1].view(np.int64)) % M
    res = (res - int(np.sum((d * bm) % M))) % M
print(res)
