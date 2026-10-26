"""Low-autocorrelation binary sequences: memetic algorithm + batched tabu search.

Odd N: search skew-symmetric sequences (m = (N+1)/2 free bits, odd lags vanish).
Even N: skew search on N-1, extend by one bit, then the same machinery is not
applicable, so a general batched tabu polish is used.

All W tabu walkers advance in lockstep with numpy; a walker that finishes its
tabu run offers its best to the population and is restarted from a child of
two population members (crossover + mutation).
"""
import sys, time
import numpy as np

T0 = time.time()


def energy(x):
    n = len(x)
    c = np.correlate(x, x, 'full')[n:]
    return int(c @ c)


def to_str(x):
    return "".join("+" if v > 0 else "-" for v in x)


class Space:
    """Flip moves on a sequence family. A state is a vector f of free bits.

    For each free bit r we keep G[r, :] such that flipping r changes the
    relevant correlations by D_r = -2 f_r G_r + cv_r e_{kr_r}.
    """

    def __init__(self, N, skew):
        self.N, self.skew = N, skew
        if skew:
            m = (N + 1) // 2; c0 = m - 1
            lags = np.arange(2, N, 2)
            sgn = np.array([(-1) ** abs(i - c0) for i in range(N)])
            # full sequence position p -> (free bit, sign)
            src = np.array([p if p < m else N - 1 - p for p in range(N)])
            psg = np.array([1 if p < m else sgn[p] for p in range(N)])
            s = np.array([sgn[N - 1 - r] if r != c0 else 0 for r in range(m)])
        else:
            m = N; lags = np.arange(1, N)
            src = np.arange(N); psg = np.ones(N, dtype=int); s = np.zeros(N, dtype=int)
        K = len(lags)
        self.m, self.K, self.lags, self.src, self.psg = m, K, lags, src, psg
        # rows of G: G[r,t] = sum over terms (p, coef) of coef * x_p
        lagpos = {int(k): t for t, k in enumerate(lags)}
        terms = []  # (r, t, p, coef)
        for r in range(m):
            j = N - 1 - r
            for t, k in enumerate(lags):
                for p in (r + k, r - k):
                    if 0 <= p < N: terms.append((r, t, p, 1))
                if s[r] != 0:
                    for p in (j + k, j - k):
                        if 0 <= p < N: terms.append((r, t, p, int(s[r])))
        T = np.array(terms)
        self.T = T
        # dependency of G entries on free bits: x_p = psg[p] * f[src[p]]
        acc = {}
        for r, t, p, cf in terms:
            b = src[p]; key = (b, r * K + t)
            acc[key] = acc.get(key, 0) + cf * psg[p]
        per = [[] for _ in range(m)]
        for (b, fi), w in acc.items():
            if w: per[b].append((fi, w))
        L = max(len(v) for v in per)
        self.L = L
        mk = m * K
        self.Up = np.full((m, L), mk, dtype=np.intp)
        self.Wp = np.zeros((m, L), dtype=np.float32)
        for b in range(m):
            for q, (fi, w) in enumerate(per[b]):
                self.Up[b, q] = fi; self.Wp[b, q] = w
        self.Rp = np.minimum(self.Up // K, m - 1)
        kr = np.zeros(m, dtype=np.intp); cv = np.zeros(m, dtype=np.float32)
        for r in range(m):
            if s[r] != 0:
                kr[r] = lagpos[N - 1 - 2 * r]; cv[r] = 4 * s[r]
        self.kr, self.cv, self.cv2 = kr, cv, cv * cv
        # dense build of G from x: indices into padded x
        self.Tr = T[:, 0] * K + T[:, 1]; self.Tp = T[:, 2]; self.Tc = T[:, 3].astype(np.float32)

    def full(self, f):
        return (self.psg * np.asarray(f)[self.src]).astype(np.int64)

    def init_state(self, f):
        x = self.full(f)
        G = np.bincount(self.Tr, self.Tc * x[self.Tp], self.m * self.K).astype(np.float32)
        cfull = np.correlate(x, x, 'full')[self.N:]
        c = cfull[self.lags - 1].astype(np.float32)
        return G, c, float(c.astype(np.float64) @ c)


class Batch:
    def __init__(self, sp, W, rng):
        self.sp, self.W, self.rng = sp, W, rng
        m, K = sp.m, sp.K
        self.mk = mk = m * K
        self.store = np.zeros(W * (mk + 1), dtype=np.float32)
        self.G = self.store.reshape(W, mk + 1)[:, :mk].reshape(W, m, K)
        self.base = (np.arange(W) * (mk + 1))[:, None]
        self.rbase = (np.arange(W) * m)[:, None]
        self.f = np.ones((W, m), dtype=np.float32)
        self.c = np.zeros((W, K), dtype=np.float32)
        self.e = np.zeros(W, dtype=np.float32)
        self.g2 = np.zeros((W, m), dtype=np.float32)
        self.tabu = np.zeros((W, m), dtype=np.int64)
        self.wb = np.full(W, np.inf, dtype=np.float32)
        self.wbf = np.ones((W, m), dtype=np.float32)
        self.end = np.zeros(W, dtype=np.int64)
        self.wr = np.arange(W)
        self.gk = self.base + np.arange(m) * K + sp.kr

    def reset(self, w, f, iters, step):
        sp = self.sp
        G, c, e = sp.init_state(f)
        self.G[w] = G.reshape(sp.m, sp.K)
        self.g2[w] = (self.G[w] ** 2).sum(1)
        self.c[w] = c; self.e[w] = e; self.f[w] = f
        self.tabu[w] = 0
        self.wb[w] = e; self.wbf[w] = f
        self.end[w] = step + iters

    def step(self, step, ten):
        sp, W, m = self.sp, self.W, self.sp.m
        G, f, c, store, g2 = self.G, self.f, self.c, self.store, self.g2
        wr = self.wr
        Gc = np.matmul(G, c[:, :, None])[:, :, 0]
        Gc += sp.cv * store.take(self.gk)
        cand = (4 * g2 + 2 * sp.cv * c.take(sp.kr, 1) + self.e[:, None] + sp.cv2) - 4 * f * Gc
        # tabu moves are forbidden unless they beat the walker's best
        cm = np.where((self.tabu > step) & (cand >= self.wb[:, None]), np.float32(1e30), cand)
        sel = cm.argmin(1)
        fi = f[wr, sel]
        m2 = -2 * fi
        c += m2[:, None] * G[wr, sel]
        c[wr, sp.kr[sel]] += sp.cv[sel]
        idx = self.base + sp.Up[sel]
        old = store.take(idx)
        new = old + m2[:, None] * sp.Wp[sel]
        store[idx] = new
        g2 += np.bincount((self.rbase + sp.Rp[sel]).ravel(), (new * new - old * old).ravel(),
                          W * m).reshape(W, m)
        f[wr, sel] = -fi
        self.tabu[wr, sel] = step + ten
        e = cand[wr, sel]; self.e = e
        imp = e < self.wb
        if imp.any():
            self.wb[imp] = e[imp]; self.wbf[imp] = f[imp]


def memetic(sp, deadline, rng, W=64, P=64, verbose=False, seeds=None, itl=0.5, ith=1.5, tdiv=8, stall=12, pmut=1.0, rand=0, tlo=0, pert=0.0, pk=0.125):
    m = sp.m
    B = Batch(sp, W, rng)
    it_lo, it_hi = max(8, int(itl * m)), int(ith * m) + 8
    ten_hi = max(2, m // tdiv); ten_lo = max(1, int(tlo * ten_hi))
    pop_f = []; pop_e = []; keys = set()
    best_e, best_f = None, None
    pool = []

    def offer(e, f):
        nonlocal best_e, best_f
        e = int(round(float(e)))
        if best_e is None or e < best_e:
            best_e, best_f = e, f.copy()
            if verbose:
                print(e, sp.N ** 2 / 2 / e, round(time.time() - T0, 1), file=sys.stderr, flush=True)
        if seeds is not None: pool.append((e, f.copy()))
        k = (f > 0).tobytes()
        if k in keys: return
        if len(pop_e) < P:
            pop_f.append(f.copy()); pop_e.append(e); keys.add(k); return
        wi = int(np.argmax(pop_e))
        if e < pop_e[wi]:
            keys.discard((pop_f[wi] > 0).tobytes())
            pop_f[wi] = f.copy(); pop_e[wi] = e; keys.add(k)

    def child():
        if pert and best_f is not None and rng.random() < pert:
            ch = best_f.copy()
            ch[rng.choice(m, max(2, int(pk * m)), replace=False)] *= -1
            return ch
        if rand or len(pop_e) < P:
            return rng.choice(np.array([-1.0, 1.0], dtype=np.float32), m)
        def tour():
            a, b = rng.integers(0, P, 2)
            return pop_f[a] if pop_e[a] <= pop_e[b] else pop_f[b]
        pa, pb = tour(), tour()
        cut = int(rng.integers(1, m))
        ch = np.concatenate([pa[:cut], pb[cut:]]).astype(np.float32)
        mut = rng.random(m) < pmut / m
        ch[mut] = -ch[mut]
        return ch

    step = 0
    for w in range(W):
        B.reset(w, child(), int(rng.integers(it_lo, it_hi + 1)), step)
    stall_best, stall_t = None, time.time()
    while True:
        step += 1
        if (step & 31) == 0:
            now = time.time()
            if now > deadline: break
            if best_e != stall_best:
                stall_best, stall_t = best_e, now
            elif now - stall_t > stall and len(pop_e) >= P:
                # population converged: restart it, keeping the best
                pop_f.clear(); pop_e.clear(); keys.clear()
                stall_t = now
        if (step & 1023) == 1:
            tens = rng.integers(ten_lo, ten_hi + 1, (1024, W))
        B.step(step, tens[step & 1023])
        done = np.flatnonzero(B.end == step)
        for w in done.tolist():
            offer(B.wb[w], B.wbf[w])
            B.reset(w, child(), int(rng.integers(it_lo, it_hi + 1)), step)
    for w in range(W):
        offer(B.wb[w], B.wbf[w])
    return best_e, sp.full(best_f), pool


def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 127
    budget = float(sys.argv[2]) if len(sys.argv) > 2 else 54.0
    verbose = len(sys.argv) > 3
    deadline = T0 + budget
    rng = np.random.default_rng()
    if N < 14:
        best = None
        for v in range(1 << N):
            x = np.array([1 if (v >> i) & 1 else -1 for i in range(N)])
            e = energy(x)
            if best is None or e < best[0]: best = (e, x)
        print(to_str(best[1])); return
    if N % 2 == 1:
        e, x, _ = memetic(Space(N, True), deadline, rng, verbose=verbose)
        assert energy(x) == e
        print(to_str(x)); return
    # even N: skew search on N-1, extend by one bit, then a general memetic polish seeded by those
    sk = Space(N - 1, True)
    e, x, _ = memetic(sk, T0 + budget * 0.75, rng, verbose=verbose)
    cands = [np.append(x, 1), np.append(x, -1), np.insert(x, 0, 1), np.insert(x, 0, -1)]
    bx = min(cands, key=energy); be = energy(bx)
    gs = Space(N, False)
    e2, x2, _ = memetic(gs, deadline, rng, W=16, P=24, verbose=verbose)
    if e2 < be: bx = x2
    print(to_str(bx))


main()
