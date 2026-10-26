"""Low-autocorrelation binary sequences: memetic tabu search (MATS-style) in numpy.

For odd N the search runs over skew-symmetric sequences (half the variables). For even N a skew-symmetric search on
N-1 seeds a full search on N. Flip gains are computed incrementally from a table S[j, k] = x_{j+k} + x_{j-k}.
"""
import sys, time
import numpy as np
from heapq import heappush, heappop

T0 = time.time()
N = int(sys.argv[1]) if len(sys.argv) > 1 else 127
BUDGET = float(sys.argv[2]) if len(sys.argv) > 2 else 54.0
LEN = float(sys.argv[3]) if len(sys.argv) > 3 else 4.0
TEN = float(sys.argv[4]) if len(sys.argv) > 4 else 0.1
POP = int(sys.argv[5]) if len(sys.argv) > 5 else 30
SKEW_FRAC = float(sys.argv[6]) if len(sys.argv) > 6 else 0.95
SEEDS = int(sys.argv[7]) if len(sys.argv) > 7 else 40
rng = np.random.default_rng()
BIG = 1e18


def corr(x, ks):
    n = len(x)
    return np.array([x[:n - k] @ x[k:] for k in ks], dtype=float)


def energy(x):
    c = corr(x, range(1, len(x)))
    return int(c @ c)


def tenures(iters):
    mn = max(1, int(iters * TEN))
    ex = max(1, int(iters * TEN / 5))
    return (mn + rng.integers(0, ex + 1, iters)).tolist()


def make_full(N):
    """Tabu search over all single flips of a length-N sequence."""
    K = N - 1
    J = np.arange(N)[:, None]
    KS = np.arange(1, N)[None, :]
    IP, IM = N + J + KS, N + J - KS
    # flat positions in S changed when bit m flips: S[j, |j-m|-1] for j != m
    ROWS = [np.array([j for j in range(N) if j != m], dtype=np.int64) for m in range(N)]
    FLAT = [r * K + np.abs(r - m) - 1 for m, r in enumerate(ROWS)]

    def tabu(x, iters):
        x = x.copy()
        xp = np.zeros(3 * N)
        xp[N:2 * N] = x
        S = xp[IP] + xp[IM]
        Sf = S.reshape(-1)
        C = corr(x, range(1, N))
        R4 = 4.0 * (S * S).sum(1)
        xm4 = -4.0 * x
        E = float(C @ C)
        bx, bE = x.copy(), E
        pen = np.zeros(N)
        until = [0] * N
        heap = []
        ten = tenures(iters)
        dot = np.dot
        for it in range(iters):
            while heap and heap[0][0] <= it:
                u, j = heappop(heap)
                if until[j] == u:
                    pen[j] = 0.0
            d = dot(S, C)
            d *= xm4
            d += R4
            m = int((d + pen).argmin())
            if pen[m] or E + d[m] >= bE:
                m2 = int(d.argmin())
                if E + d[m2] < bE:
                    m = m2
            xo = x[m]
            C -= (2.0 * xo) * S[m]
            f = FLAT[m]
            old = Sf[f]
            R4[ROWS[m]] += 16.0 - (16.0 * xo) * old
            Sf[f] = old - 2.0 * xo
            x[m] = -xo
            xm4[m] = 4.0 * xo
            E += d[m]
            u = it + ten[it]
            until[m] = u
            pen[m] = BIG
            heappush(heap, (u, m))
            if E < bE:
                bE = E
                bx = x.copy()
        return bx, int(round(bE))

    return tabu, (lambda y: y), N


def make_skew(N):
    """Tabu search over skew-symmetric sequences of odd length N = 2n-1, free variables x_0..x_{n-1}.

    Odd-lag correlations vanish, so only even lags are tracked; flipping free variable a < c also flips x_{2c-a}.
    """
    n = (N + 1) // 2
    c = n - 1
    ks = np.arange(2, N, 2)
    W = len(ks)
    J = np.arange(c + 1)[:, None]
    IP, IM = N + J + ks[None, :], N + J - ks[None, :]
    FE, RE = [], []
    for m in range(N):
        js = np.array([j for j in range(c + 1) if j != m and abs(j - m) % 2 == 0], dtype=np.int64)
        FE.append(js * W + np.abs(js - m) // 2 - 1)
        RE.append(js)
    A = np.arange(c)
    T0i = c - 1 - A            # lag index of the pair (a, 2c-a)
    FL0 = A * W + T0i
    B = 2 * c - A
    sgn = np.array([(-1) ** l for l in range(1, n)], dtype=float)
    wR = np.full(c + 1, 16.0)
    wR[c] = 4.0

    def expand(y):
        x = np.empty(N)
        x[:c + 1] = y
        x[c + 1:] = sgn * y[c - 1::-1]
        return x

    def tabu(y, iters):
        x = expand(y)
        xp = np.zeros(3 * N)
        xp[N:2 * N] = x
        Se = xp[IP] + xp[IM]
        Sef = Se.reshape(-1)
        Ce = corr(x, ks)
        Re = (Se * Se).sum(1)
        coef = -8.0 * x[:c + 1]
        coef[c] *= 0.5
        E = float(Ce @ Ce)
        bx, bE = x[:c + 1].copy(), E
        pen = np.zeros(c + 1)
        until = [0] * (c + 1)
        heap = []
        ten = tenures(iters)
        dot = np.dot
        xa = x[:c]
        xb = x[B]
        for it in range(iters):
            while heap and heap[0][0] <= it:
                u, j = heappop(heap)
                if until[j] == u:
                    pen[j] = 0.0
            d = dot(Se, Ce)
            d *= coef
            d += wR * Re
            d[:c] += (8.0 * Ce[T0i]) * (xb * xa) - (32.0 * Sef[FL0]) * xb + 16.0
            m = int((d + pen).argmin())
            if pen[m] or E + d[m] >= bE:
                m2 = int(d.argmin())
                if E + d[m2] < bE:
                    m = m2
            xo = x[m]
            if m < c:
                b = 2 * c - m
                xbo = x[b]
                Ce -= (4.0 * xo) * Se[m]
                Ce[c - 1 - m] += 4.0 * xo * xbo
                for mm in (m, b):
                    xv = x[mm]
                    f = FE[mm]
                    if len(f):
                        old = Sef[f]
                        Re[RE[mm]] += 4.0 - (4.0 * xv) * old
                        Sef[f] = old - 2.0 * xv
                    x[mm] = -xv
                xb[m] = -xbo
            else:
                Ce -= (2.0 * xo) * Se[m]
                f = FE[m]
                old = Sef[f]
                Re[RE[m]] += 4.0 - (4.0 * xo) * old
                Sef[f] = old - 2.0 * xo
                x[m] = -xo
            coef[m] = -coef[m]
            E += d[m]
            u = it + ten[it]
            until[m] = u
            pen[m] = BIG
            heappush(heap, (u, m))
            if E < bE:
                bE = E
                bx = x[:c + 1].copy()
        return bx, int(round(bE))

    return tabu, expand, n


def memetic(tabu, n, deadline, seeds=(), size=POP):
    """Steady-state memetic algorithm; returns population sorted by energy."""
    lo, hi = n // 2, 3 * n // 2 + 1
    pop, pe = [], []

    def add(y):
        y, e = tabu(y, int(LEN * rng.integers(lo, hi)))
        pop.append(y)
        pe.append(e)

    for y in seeds:
        if time.time() > deadline or len(pop) >= size:
            break
        add(y)
    while len(pop) < size and time.time() < deadline:
        add(rng.choice([-1.0, 1.0], n))

    def pick():
        a, b = rng.integers(0, len(pop), 2)
        return a if pe[a] < pe[b] else b

    while time.time() < deadline:
        if rng.random() < 0.9:
            p1, p2 = pop[pick()], pop[pick()]
            cut = int(rng.integers(1, n))
            child = np.concatenate([p1[:cut], p2[cut:]])
        else:
            child = pop[pick()].copy()
        mask = rng.random(n) < 1.0 / n
        child[mask] = -child[mask]
        child, e = tabu(child, int(LEN * rng.integers(lo, hi)))
        w = int(np.argmax(pe))
        if e <= pe[w] and not any(e == pe[i] and np.array_equal(child, pop[i]) for i in range(len(pop))):
            pop[w] = child
            pe[w] = e
    order = np.argsort(pe)
    return [pop[i] for i in order], [pe[i] for i in order]


def main():
    deadline = T0 + BUDGET
    cands = []
    if N % 2 == 1 and N >= 5:
        tabu, expand, n = make_skew(N)
        pop, pe = memetic(tabu, n, deadline)
        cands = [expand(y) for y in pop[:5]]
    else:
        seeds = []
        if N >= 6:
            M = N - 1
            tabu, expand, n = make_skew(M)
            pop, pe = memetic(tabu, n, T0 + SKEW_FRAC * BUDGET)
            for y in pop:
                x = expand(y)
                for s in (1.0, -1.0):
                    seeds.append(np.append(x, s))
                    seeds.append(np.insert(x, 0, s))
        if seeds:
            sys.stderr.write('seedE=%d ' % min(energy(z) for z in seeds))
        tabu, _, n = make_full(N)
        pop, pe = memetic(tabu, n, deadline, seeds, SEEDS if seeds else POP)
        cands = pop[:5]
    best = min(cands, key=energy)
    e = energy(best)
    sys.stderr.write("E=%d F=%.4f\n" % (e, N * N / (2.0 * e)))
    print("".join("+" if v > 0 else "-" for v in best))


main()
