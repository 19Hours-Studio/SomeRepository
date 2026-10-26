import sys, time
import numpy as np

T0 = time.time()


def corr_energy(x):
    n = len(x)
    c = np.correlate(x, x, 'full')[n:]
    return int(c @ c)


class SkewTabu:
    """Many tabu-search walkers over skew-symmetric sequences of odd length N, advanced together with numpy.

    Free bits f[0..m-1]; the full sequence is x[:m] = f, x[m+t] = f[m-2-t] * sgn.  Only odd lags matter... the even
    lags k = 2, 4, .. carry the energy (odd lags are 0 for skew sequences).  For every walker we keep the correlations
    c (K values) and G[r, t], the change of c_{2(t+1)} per unit of -f_r when bit r flips (plus the centre fix-up).
    """

    def __init__(self, N, W, rng):
        self.N, self.W, self.rng = N, W, rng
        m = self.m = (N + 1) // 2
        c0 = m - 1
        K = self.K = (N - 1) // 2
        self.sgn = np.array([(-1) ** abs(i - c0) for i in range(N)])
        iv = np.arange(m); jv = N - 1 - iv
        s = self.sgn[iv]
        ks = np.arange(2, N, 2)
        refs = [[] for _ in range(N)]
        for r in range(m):
            j = N - 1 - r
            for t, k in enumerate(ks):
                fl = r * K + t
                terms = [(r + k, 1), (r - k, 1)]
                if r != c0:
                    terms += [(j + k, int(s[r])), (j - k, int(s[r]))]
                for p, cf in terms:
                    if 0 <= p < N:
                        refs[p].append((fl, cf))
        U, Wt = [], []
        for b in range(m):
            acc = {}
            for fl, cf in refs[b]:
                acc[fl] = acc.get(fl, 0) + cf
            if b != c0:
                for fl, cf in refs[N - 1 - b]:
                    acc[fl] = acc.get(fl, 0) + cf * int(s[b])
            items = [(fl, w) for fl, w in acc.items() if w != 0]
            U.append([fl for fl, _ in items]); Wt.append([w for _, w in items])
        self.kr = (jv - iv) // 2 - 1
        self.kr[c0] = 0
        cv = (4 * s).astype(np.float32); cv[c0] = 0.0
        self.cv = cv
        mk = m * K
        Lmax = max(len(u) for u in U)
        self.Up = np.full((m, Lmax), mk, dtype=np.intp)
        self.Wp = np.zeros((m, Lmax), dtype=np.float32)
        for b in range(m):
            self.Up[b, :len(U[b])] = U[b]; self.Wp[b, :len(Wt[b])] = Wt[b]
        self.Rp = np.minimum(self.Up // K, m - 1)
        self.store = np.zeros(W * (mk + 1), dtype=np.float32)
        self.G = self.store.reshape(W, mk + 1)[:, :mk].reshape(W, m, K)
        self.base = (np.arange(W) * (mk + 1))[:, None]
        self.rbase = (np.arange(W) * m)[:, None]
        ii = np.arange(m)[:, None]; jj = N - 1 - ii; kk = np.arange(2, N, 2)[None, :]
        self.gi = [N + ii + kk, N + ii - kk, N + jj + kk, N + jj - kk]
        self.gs = np.where(np.arange(m) == c0, 0, s)[:, None].astype(np.float32)
        self.f = np.zeros((W, m), dtype=np.float32)
        self.c = np.zeros((W, K), dtype=np.float32)
        self.g2 = np.zeros((W, m), dtype=np.float32)
        self.e = np.zeros(W, dtype=np.float32)
        self.tabu = np.zeros((W, m), dtype=np.int64)
        self.wb = np.full(W, np.inf, dtype=np.float32)   # best of the current walk
        self.wbf = np.zeros((W, m), dtype=np.float32)
        self.age = np.zeros(W, dtype=np.int64)          # steps since the walk started
        self.length = np.zeros(W, dtype=np.int64)
        self.best_e, self.best_f = None, None

    def full(self, f):
        N, m = self.N, self.m
        f = np.asarray(f).astype(np.int64)
        x = np.empty(N, dtype=np.int64); x[:m] = f
        x[m:] = f[:m - 1][::-1] * self.sgn[m:]
        return x

    def fulls(self, F):
        """Full sequences for a batch of free-bit vectors."""
        N, m = self.N, self.m
        X = np.empty((len(F), N), dtype=np.float32); X[:, :m] = F
        X[:, m:] = F[:, :m - 1][:, ::-1] * self.sgn[m:]
        return X

    def reset(self, ws, F, lengths):
        """Start walkers ws from the free-bit rows F."""
        N, K = self.N, self.K
        X = self.fulls(F)
        n = len(ws)
        P = np.zeros((n, 3 * N), dtype=np.float32); P[:, N:2 * N] = X
        gi = self.gi
        G = P[:, gi[0]] + P[:, gi[1]] + self.gs * (P[:, gi[2]] + P[:, gi[3]])
        self.G[ws] = G
        self.g2[ws] = (G * G).sum(2)
        # even-lag correlations via FFT-free direct products
        Xd = X.astype(np.float64)
        c = np.empty((n, K))
        for t in range(K):
            k = 2 * (t + 1)
            c[:, t] = (Xd[:, :N - k] * Xd[:, k:]).sum(1)
        self.c[ws] = c
        self.e[ws] = (c * c).sum(1)
        self.f[ws] = F
        self.tabu[ws] = 0
        self.wb[ws] = self.e[ws]; self.wbf[ws] = F
        self.age[ws] = 0
        self.length[ws] = lengths

    def run(self, deadline, newstarts, tmin, tmax, lmin, lmax, verbose=False):
        rng, W, m = self.rng, self.W, self.m
        self.reset(np.arange(W), newstarts(W), rng.integers(lmin, lmax + 1, W))
        G, f, c, store, g2 = self.G, self.f, self.c, self.store, self.g2
        kr, cv = self.kr, self.cv; cv2 = cv * cv
        ar = np.arange(m); wr = np.arange(W)
        Up, Wp, base, Rp, rbase, Wm = self.Up, self.Wp, self.base, self.Rp, self.rbase, W * m
        matmul, bincount = np.matmul, np.bincount
        tabu = self.tabu
        inf = np.float32(np.inf)
        it = 0
        steps = 0
        RT = rng.integers(tmin, tmax + 1, (997, W))
        e4 = np.empty((W, m), dtype=np.float32)
        while True:
            it += 1
            if (it & 31) == 0:
                if time.time() > deadline:
                    break
            Gc = matmul(G, c[:, :, None])[:, :, 0]
            Gc += cv * G[:, ar, kr]
            Gc *= f
            cand = g2 - Gc
            cand *= 4
            cand += cv2 + 2 * cv * c[:, kr]
            cand += self.e[:, None]
            ok = (tabu <= it) | (cand < self.wb[:, None])
            sel = np.where(ok, cand, inf).argmin(1)
            fi = f[wr, sel]
            m2 = -2 * fi
            c += m2[:, None] * G[wr, sel]
            c[wr, kr[sel]] += cv[sel]
            idx = base + Up[sel]
            old = store[idx]
            new = old + m2[:, None] * Wp[sel]
            store[idx] = new
            g2 += bincount((rbase + Rp[sel]).ravel(), (new * new - old * old).ravel(), Wm).reshape(W, m).astype(np.float32)
            f[wr, sel] = -fi
            tabu[wr, sel] = it + RT[it % 997]
            e = cand[wr, sel]; self.e = e
            imp = e < self.wb
            if imp.any():
                self.wb[imp] = e[imp]; self.wbf[imp] = f[imp]
            self.age += 1
            steps += W
            done = np.nonzero(self.age >= self.length)[0]
            if len(done):
                self.finish(done, verbose)
                self.reset(done, newstarts(len(done)), rng.integers(lmin, lmax + 1, len(done)))
        self.finish(wr, verbose)
        return steps

    def finish(self, ws, verbose):
        for w in ws:
            e = int(round(float(self.wb[w])))
            self.on_result(e, self.wbf[w].copy())
            if self.best_e is None or e < self.best_e:
                self.best_e, self.best_f = e, self.wbf[w].copy()
                if verbose:
                    print(e, self.N ** 2 / 2 / e, round(time.time() - T0, 1), file=sys.stderr, flush=True)

    def on_result(self, e, f):
        pass


class Memetic:
    """Elite pool of walk results; new starts are crossovers + mutations of elites (or random while filling)."""

    def __init__(self, S, P, rng, prand=0.0):
        self.S, self.P, self.rng, self.prand = S, P, rng, prand
        self.pool_e, self.pool_f, self.keys = [], [], set()
        S.on_result = self.add

    def add(self, e, f):
        k = f.tobytes()
        if k in self.keys: return
        if len(self.pool_e) < self.P:
            self.pool_e.append(e); self.pool_f.append(f); self.keys.add(k); return
        j = int(np.argmax(self.pool_e))
        if e < self.pool_e[j] or (e == self.pool_e[j] and self.rng.random() < 0.5):
            self.keys.discard(self.pool_f[j].tobytes())
            self.pool_e[j] = e; self.pool_f[j] = f; self.keys.add(k)

    def starts(self, n):
        rng, m = self.rng, self.S.m
        F = rng.choice(np.array([-1.0, 1.0], dtype=np.float32), (n, m))
        if len(self.pool_e) < self.P:
            return F
        pe = np.array(self.pool_e); pf = np.array(self.pool_f)
        for r in range(n):
            if rng.random() < self.prand: continue
            # binary tournaments
            a = rng.integers(0, len(pe), 2); a = a[np.argmin(pe[a])]
            b = rng.integers(0, len(pe), 2); b = b[np.argmin(pe[b])]
            mask = rng.random(m) < 0.5
            ch = np.where(mask, pf[a], pf[b])
            mu = rng.random(m) < 1.0 / m
            ch[mu] = -ch[mu]
            F[r] = ch
        return F


def to_str(x):
    return "".join("+" if v > 0 else "-" for v in x)
