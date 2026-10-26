import sys, time
import numpy as np

T0 = time.time()


def corr_energy(x):
    n = len(x)
    c = np.correlate(x, x, 'full')[n:]
    return int(c @ c)


class Skew:
    """Self-avoiding walk over skew-symmetric sequences of odd length N (only the m=(N+1)/2 first bits are free)."""

    def __init__(self, N):
        self.N = N
        m = self.m = (N + 1) // 2
        c0 = m - 1
        K = self.K = (N - 1) // 2
        self.sgn = np.array([(-1) ** abs(i - c0) for i in range(N)])
        iv = np.arange(m); jv = N - 1 - iv
        s = self.s = self.sgn[iv]
        ks = np.arange(2, N, 2)
        # G[r, t] = x[r+k] + x[r-k] + s_r (x[j+k] + x[j-k]), k = 2(t+1), j = N-1-r; out of range terms are 0
        # the centre row is a single flip: drop its mirrored terms
        refs = [[]for _ in range(N)]
        for r in range(m):
            j = N - 1 - r
            for t, k in enumerate(ks):
                f = r * K + t
                terms = [(r + k, 1), (r - k, 1)]
                if r != c0:
                    terms += [(j + k, int(s[r])), (j - k, int(s[r]))]
                for p, cf in terms:
                    if 0 <= p < N:
                        refs[p].append((f, cf))
        self.U, self.W = [], []
        for b in range(m):
            acc = {}
            for f, cf in refs[b]:
                acc[f] = acc.get(f, 0) + cf
            if b != c0:
                for f, cf in refs[N - 1 - b]:
                    acc[f] = acc.get(f, 0) + cf * int(s[b])
            items = [(f, w) for f, w in acc.items() if w != 0]
            self.U.append(np.array([f for f, _ in items], dtype=np.intp))
            self.W.append(np.array([w for _, w in items], dtype=np.float64))
        self.kr = (jv - iv) // 2 - 1  # column of lag j-r
        self.kr[c0] = 0
        self.cv = (4 * s).astype(np.float64)
        self.cv[c0] = 0.0
        self.BITS = [1 << i for i in range(m)]

    def full(self, f):
        N, m = self.N, self.m
        x = np.empty(N, dtype=np.int64); x[:m] = f
        x[m:] = f[:m - 1][::-1] * self.sgn[m:]
        return x

    def walk(self, f, steps, deadline, vis=None):
        N, m, K = self.N, self.m, self.K
        if vis is None:
            vis = set()
        f = np.array(f, dtype=np.float64)
        x = self.full(f.astype(np.int64))
        c = np.correlate(x, x, 'full')[N + 1::2].astype(np.float64)
        G = np.zeros((m, K))
        Gf = G.reshape(-1)
        xs = x.astype(np.float64)
        for r in range(m):
            j = N - 1 - r
            for t in range(K):
                k = 2 * (t + 1)
                v = 0.0
                for p in (r + k, r - k):
                    if 0 <= p < N: v += xs[p]
                if r != m - 1:
                    for p in (j + k, j - k):
                        if 0 <= p < N: v += self.s[r] * xs[p]
                G[r, t] = v
        h = 0
        for i in range(m):
            if f[i] > 0: h |= self.BITS[i]
        vis.add(h)
        e = float(c @ c)
        wb, wbf = e, f.copy()
        kr, cv, U, W, BITS = self.kr, self.cv, self.U, self.W, self.BITS
        ar = np.arange(m)
        cv2 = cv * cv
        einsum = np.einsum
        for st in range(steps):
            if (st & 255) == 0 and time.time() > deadline:
                break
            # cand_r = E + 2 D_r.c + |D_r|^2, D_r = -2 f_r G_r + cv_r e_kr
            Gc = G @ c
            g2 = einsum('ij,ij->i', G, G)
            Gk = G[ar, kr]
            cand = (e + cv * (2 * c[kr] - 4 * f * Gk) + cv2) + 4 * (g2 - f * Gc)
            i = int(cand.argmin()); nh = h ^ BITS[i]
            if nh in vis:
                for i in np.argsort(cand):
                    i = int(i); nh = h ^ BITS[i]
                    if nh not in vis: break
                else:
                    break
            h = nh; vis.add(h)
            fi = f[i]
            c += (-2 * fi) * G[i]
            c[kr[i]] += cv[i]
            Gf[U[i]] += (-2 * fi) * W[i]
            f[i] = -fi
            e = float(cand[i])
            if e < wb:
                wb, wbf = e, f.copy()
        return int(round(wb)), self.full(wbf.astype(np.int64))



class BatchSkew:
    def __init__(self, N, W, rng):
        self.S = S = Skew(N)
        self.N, self.m, self.K, self.W, self.rng = N, S.m, S.K, W, rng
        m, K = S.m, S.K
        Lmax = max(len(u) for u in S.U)
        mk = m * K
        # pad update lists with a dummy slot at index mk (extra column in flat storage)
        self.Up = np.full((m, Lmax), mk, dtype=np.intp)
        self.Wp = np.zeros((m, Lmax), dtype=np.float32)
        for b in range(m):
            self.Up[b, :len(S.U[b])] = S.U[b]; self.Wp[b, :len(S.W[b])] = S.W[b]
        self.Rp = np.minimum(self.Up // K, m - 1)
        self.g2 = np.zeros((W, m), dtype=np.float32)
        self.store = np.zeros(W * (mk + 1), dtype=np.float32)
        self.G = self.store.reshape(W, mk + 1)[:, :mk].reshape(W, m, K)  # view
        assert np.shares_memory(self.G, self.store)
        self.base = (np.arange(W) * (mk + 1))[:, None]
        self.f = np.zeros((W, m), dtype=np.float32); self.c = np.zeros((W, K), dtype=np.float32); self.e = np.zeros(W, dtype=np.float32)
        self.h = [0] * W; self.vis = [set() for _ in range(W)]; self.steps = [0] * W
        self.wb = np.full(W, np.inf); self.wbf = np.zeros((W, m))
        # gather indices to build G from x
        N = self.N; s = S.s
        ii = np.arange(m)[:, None]; jj = N - 1 - ii; ks = np.arange(2, N, 2)[None, :]
        self.gi = [N + ii + ks, N + ii - ks, N + jj + ks, N + jj - ks]
        self.gs = np.where(np.arange(m) == m - 1, 0, s)[:, None].astype(np.float64)
        self.best_e, self.best_x = None, None

    def reset(self, w, f):
        S, N, m = self.S, self.N, self.m
        f = np.asarray(f, dtype=np.float64)
        x = S.full(f.astype(np.int64))
        P = np.zeros(3 * N); P[N:2 * N] = x
        gi = self.gi
        self.G[w] = P[gi[0]] + P[gi[1]] + self.gs * (P[gi[2]] + P[gi[3]])
        self.g2[w] = (self.G[w] ** 2).sum(1)
        c = np.correlate(x, x, 'full')[N + 1::2]
        self.c[w] = c; self.e[w] = float(c @ c); self.f[w] = f
        h = 0
        for i in range(m):
            if f[i] > 0: h |= S.BITS[i]
        self.h[w] = h; self.vis[w] = {h}; self.steps[w] = 0
        self.wb[w] = self.e[w]; self.wbf[w] = f

    def harvest(self, w):
        e = int(round(self.wb[w]))
        if self.best_e is None or e < self.best_e:
            self.best_e = e; self.best_x = self.S.full(self.wbf[w].astype(np.int64))
            assert corr_energy(self.best_x) == e
            return True
        return False

    def run(self, L, deadline, newstart, verbose=True):
        per = max(1, L // self.W)
        S, W, m = self.S, self.W, self.m
        for w in range(W):
            self.reset(w, newstart())
        G, f, c, store = self.G, self.f, self.c, self.store
        kr, cv = S.kr, S.cv.astype(np.float32); cv2 = cv * cv
        ar = np.arange(m); wr = np.arange(W)
        BITS = S.BITS; Up, Wp, base = self.Up, self.Wp, self.base
        Rp, g2, bincount, Wm = self.Rp, self.g2, np.bincount, W * m
        rbase = (np.arange(W) * m)[:, None]
        einsum = np.einsum; matmul = np.matmul; argsort = np.argsort
        it = 0
        while True:
            it += 1
            if (it & 63) == 0 and time.time() > deadline:
                break
            Gc = matmul(G, c[:, :, None])[:, :, 0]
            Gk = G[:, ar, kr]
            cand = self.e[:, None] + cv2 + cv * (2 * c[:, kr] - 4 * f * Gk) + 4 * (g2 - f * Gc)
            order = argsort(cand, axis=1)[:, :3].tolist()
            sel = []
            hs = self.h; viss = self.vis
            for w in range(W):
                h = hs[w]; vis = viss[w]
                o = order[w]
                i = o[0]; nh = h ^ BITS[i]
                if nh in vis:
                    i = o[1]; nh = h ^ BITS[i]
                    if nh in vis:
                        i = o[2]; nh = h ^ BITS[i]
                        if nh in vis:
                            i = -1
                            for i2 in argsort(cand[w]).tolist():
                                nh = h ^ BITS[i2]
                                if nh not in vis: i = i2; break
                            if i < 0: i = 0; nh = h ^ BITS[0]
                hs[w] = nh; vis.add(nh)
                sel.append(i)
            sel = np.array(sel)
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
            e = cand[wr, sel]; self.e = e
            imp = e < self.wb
            if imp.any():
                self.wb[imp] = e[imp]; self.wbf[imp] = f[imp]
            if it % per == 0:
                w = (it // per) % W
                if self.harvest(w) and verbose:
                    print(self.best_e, self.N ** 2 / 2 / self.best_e, round(time.time() - T0, 1), file=sys.stderr, flush=True)
                self.reset(w, newstart())
        for w in range(W):
            self.harvest(w)
        return it



class General:
    """Self-avoiding walk over all sequences of length N with single flips."""

    def __init__(self, N):
        self.N = N
        K = N - 1
        U = [[] for _ in range(N)]; W = [[] for _ in range(N)]
        # G[i, k-1] = x[i+k] + x[i-k]; position p is referenced by (p-k, k) and (p+k, k)
        for p in range(N):
            for k in range(1, N):
                for i in (p - k, p + k):
                    if 0 <= i < N:
                        U[p].append(i * K + k - 1); W[p].append(1.0)
        self.U = [np.array(u, dtype=np.intp) for u in U]
        self.W = [np.array(w) for w in W]
        self.BITS = [1 << i for i in range(N)]

    def walk(self, x0, steps, deadline, vis=None):
        N = self.N
        if vis is None:
            vis = set()
        f = np.array(x0, dtype=np.float64)
        xi = f.astype(np.int64)
        c = np.correlate(xi, xi, 'full')[N:].astype(np.float64)
        P = np.zeros(3 * N); P[N:2 * N] = f
        ii = np.arange(N)[:, None]; kk = np.arange(1, N)[None, :]
        G = P[N + ii + kk] + P[N + ii - kk]
        Gf = G.reshape(-1)
        h = 0
        for i in range(N):
            if f[i] > 0: h |= self.BITS[i]
        vis.add(h)
        e = float(c @ c)
        wb, wbf = e, f.copy()
        U, W, BITS = self.U, self.W, self.BITS
        einsum = np.einsum
        for st in range(steps):
            if (st & 255) == 0 and time.time() > deadline:
                break
            cand = e + 4 * (einsum('ij,ij->i', G, G) - f * (G @ c))
            i = int(cand.argmin()); nh = h ^ BITS[i]
            if nh in vis:
                for i in np.argsort(cand):
                    i = int(i); nh = h ^ BITS[i]
                    if nh not in vis: break
                else:
                    break
            h = nh; vis.add(h)
            fi = f[i]
            c += (-2 * fi) * G[i]
            Gf[U[i]] += (-2 * fi) * W[i]
            f[i] = -fi
            e = float(cand[i])
            if e < wb:
                wb, wbf = e, f.copy()
        return int(round(wb)), wbf.astype(np.int64)



def to_str(x):
    return "".join("+" if v > 0 else "-" for v in x)


def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 127
    budget = float(sys.argv[2]) if len(sys.argv) > 2 else 54.0
    verbose = len(sys.argv) > 3
    deadline = T0 + budget
    rng = np.random.default_rng()
    W = int(sys.argv[5]) if len(sys.argv) > 5 else 32
    L = int(sys.argv[4]) if len(sys.argv) > 4 else 10000
    if N < 12:
        best = None
        for v in range(1 << N):
            x = np.array([1 if (v >> i) & 1 else -1 for i in range(N)])
            e = corr_energy(x)
            if best is None or e < best[0]: best = (e, x)
        print(to_str(best[1])); return
    if N % 2 == 1:
        B = BatchSkew(N, W, rng)
        B.run(L, deadline, lambda: rng.choice(np.array([-1.0, 1.0]), B.m), verbose)
        print(to_str(B.best_x)); return
    # even N: skew-symmetric search on N-1, then extend by one bit and polish with general single-flip walks
    split = T0 + budget * 0.7
    B = BatchSkew(N - 1, W, rng)
    pool = []
    orig = B.harvest
    def harvest(w):
        pool.append((int(round(B.wb[w])), B.S.full(B.wbf[w].astype(np.int64))))
        return orig(w)
    B.harvest = harvest
    B.run(L, split, lambda: rng.choice(np.array([-1.0, 1.0]), B.m), verbose)
    pool.sort(key=lambda t: t[0])
    seeds, seen = [], set()
    for e, x in pool:
        k = x.tobytes()
        if k in seen: continue
        seen.add(k)
        for y in (np.append(x, 1), np.append(x, -1), np.insert(x, 0, 1), np.insert(x, 0, -1)):
            seeds.append((corr_energy(y), y))
        if len(seen) >= 50: break
    seeds.sort(key=lambda t: t[0])
    best_e, best_x = seeds[0]
    if verbose: print('skew', pool[0][0], 'seed', best_e, N * N / 2 / best_e, file=sys.stderr)
    Gn = General(N)
    for e0, y in seeds:
        if time.time() > deadline: break
        e, x = Gn.walk(y, 3000, deadline)
        if e < best_e:
            best_e, best_x = e, x
            if verbose: print(e, N * N / 2 / e, round(time.time() - T0, 1), file=sys.stderr)
    print(to_str(best_x))


main()
