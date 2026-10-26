import sys, time
import numpy as np
from heapq import heappush, heappop

T0 = time.time()
N = int(sys.argv[1]) if len(sys.argv) > 1 else 127
BUDGET = float(sys.argv[2]) if len(sys.argv) > 2 else 54.0
rng = np.random.default_rng()
LEN = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
TEN = float(sys.argv[4]) if len(sys.argv) > 4 else 0.1

K = N - 1
J = np.arange(N)[:, None]
KS = np.arange(1, N)[None, :]
IP = N + J + KS            # index of x_{j+k} in padded array
IM = N + J - KS            # index of x_{j-k}
# flat positions in S changed when bit m flips: S[j, |j-m|-1] for j != m
FLAT = []
for m in range(N):
    js = np.array([j for j in range(N) if j != m])
    FLAT.append(js * K + np.abs(js - m) - 1)
ROWS = [np.array([j for j in range(N) if j != m]) for m in range(N)]


def energy(x):
    c = np.array([x[:N - k] @ x[k:] for k in range(1, N)])
    return int(c @ c)


def build(x):
    xp = np.zeros(3 * N)
    xp[N:2 * N] = x
    S = xp[IP] + xp[IM]
    C = np.array([x[:N - k] @ x[k:] for k in range(1, N)], dtype=float)
    R = (S * S).sum(1)
    return S, C, R


def tabu(x, iters):
    """Tabu search from x (float array, copied); returns best sequence and its energy."""
    x = x.copy()
    S, C, R = build(x)
    Sf = S.reshape(-1)
    R4 = 4.0 * R
    xm4 = -4.0 * x
    E = float(C @ C)
    bx, bE = x.copy(), E
    pen = np.zeros(N)
    until = [0] * N
    heap = []
    mn = max(1, int(iters * TEN))
    ex = max(1, int(iters * TEN / 5))
    ten = (mn + rng.integers(0, ex + 1, iters)).tolist()
    dot = np.dot
    BIG = 1e18
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


def main():
    pop_size = 100
    pop, pe = [], []
    best, best_e = None, None
    deadline = T0 + BUDGET
    for _ in range(pop_size):
        if time.time() > deadline:
            break
        x = rng.choice([-1.0, 1.0], N)
        x, e = tabu(x, int(LEN * rng.integers(N // 2, 3 * N // 2 + 1)))
        pop.append(x); pe.append(e)
        if best_e is None or e < best_e:
            best, best_e = x.copy(), e
    while time.time() < deadline:
        def pick():
            a, b = rng.integers(0, len(pop), 2)
            return a if pe[a] < pe[b] else b
        if rng.random() < 0.9:
            p1, p2 = pop[pick()], pop[pick()]
            cut = int(rng.integers(1, N))
            child = np.concatenate([p1[:cut], p2[cut:]])
        else:
            child = pop[pick()].copy()
        mask = rng.random(N) < 1.0 / N
        child[mask] = -child[mask]
        child, e = tabu(child, int(LEN * rng.integers(N // 2, 3 * N // 2 + 1)))
        if e < best_e:
            best, best_e = child.copy(), e
        w = int(np.argmax(pe))
        if e <= pe[w] and not any(e == pe[i] and np.array_equal(child, pop[i]) for i in range(len(pop))):
            pop[w] = child; pe[w] = e
    sys.stderr.write("E=%d F=%.4f\n" % (best_e, N * N / (2.0 * best_e)))
    print("".join("+" if v > 0 else "-" for v in best))


main()
