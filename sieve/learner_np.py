"""Verdict head for the CPU prototype: hashed structural features -> MLP -> P(true).

Same learner in every ablation arm; arms differ only in which labels it sees and in the coherence term.
Loss = log loss on labeled nodes (proper scoring rule -> calibrated probabilities)
     + lam * sum over lattice edges relu(p_i - p_j)^2 (coherence; uses unlabeled nodes too).
"""
import zlib
import numpy as np
from bitworld import tokens

H = 4096


def _h(s): return zlib.crc32(s.encode()) % H


def _edges(e, side, out):
    if e[0] in ("x", "y", "c"): return
    for a in e[1:]:
        out.append(f"{side}:{e[0]}>{tokens(a)[0]}"); _edges(a, side, out)


def featurize(stmts):
    F = np.zeros((len(stmts), H), dtype=np.float32)
    for r, s in enumerate(stmts):
        tl, tr = tokens(s.lhs), tokens(s.rhs); f = []
        f += ["L:" + t for t in tl] + ["R:" + t for t in tr]
        _edges(s.lhs, "L", f); _edges(s.rhs, "R", f)
        root = f"ROOT:{tl[0]}|{tr[0]}"; f.append(root)
        f += ["D+:" + t for t in set(tl) - set(tr)] + ["D-:" + t for t in set(tr) - set(tl)]
        pre, inst = f"PRE:{s.pre}", f"INST:{s.inst}"
        f += [pre, inst, pre + "|" + inst, pre + "|" + root, inst + "|" + root]
        for t in f: F[r, _h(t)] = 1.0
    return F


class MLP:
    def __init__(self, hidden=64, lr=3e-3, seed=0, wd=1e-4):
        g = np.random.default_rng(seed)
        self.W1 = (g.standard_normal((H, hidden)) * 0.02).astype(np.float32); self.b1 = np.zeros(hidden, np.float32)
        self.w2 = (g.standard_normal(hidden) * 0.02).astype(np.float32); self.b2 = np.float32(0)
        self.lr, self.wd, self.T = lr, wd, 1.0; self.m = [np.zeros_like(p) for p in self.params()]; self.v = [np.zeros_like(p) for p in self.params()]; self.t = 0

    def params(self): return [self.W1, self.b1, self.w2, np.array(self.b2, dtype=np.float32)]

    def forward(self, F):
        h = np.maximum(F @ self.W1 + self.b1, 0); z = h @ self.w2 + self.b2
        return z, h

    def predict(self, F):
        z, _ = self.forward(F); return 1 / (1 + np.exp(-np.clip(z / self.T, -30, 30)))

    def snapshot(self): return [p.copy() for p in (self.W1, self.b1, self.w2)] + [self.b2]

    def restore(self, s): self.W1, self.b1, self.w2, self.b2 = [x.copy() if hasattr(x, "copy") else x for x in s]

    def _step(self, F, h, dz):
        """Backprop dL/dz for rows of F; Adam update."""
        g_w2 = h.T @ dz; g_b2 = dz.sum()
        dh = np.outer(dz, self.w2) * (h > 0)
        g_W1 = F.T @ dh; g_b1 = dh.sum(0)
        grads = [g_W1 + self.wd * self.W1, g_b1, g_w2 + self.wd * self.w2, np.array(g_b2, dtype=np.float32)]
        self.t += 1; b1, b2, eps = 0.9, 0.999, 1e-8
        ps = self.params()
        for k, (p, g) in enumerate(zip(ps, grads)):
            self.m[k] = b1 * self.m[k] + (1 - b1) * g; self.v[k] = b2 * self.v[k] + (1 - b2) * g * g
            upd = self.lr * (self.m[k] / (1 - b1 ** self.t)) / (np.sqrt(self.v[k] / (1 - b2 ** self.t)) + eps)
            p -= upd.astype(p.dtype)
        self.b2 = ps[3].item()

    def fit(self, F, y, epochs=30, edges=None, Fall=None, lam=0.0, batch=64, rng=None, w=None):
        rng = rng or np.random.default_rng(0); n = len(y)
        w = np.ones(n, np.float32) if w is None else w / w.mean()
        for _ in range(epochs):
            for idx in np.array_split(rng.permutation(n), max(1, n // batch)):
                z, h = self.forward(F[idx]); p = 1 / (1 + np.exp(-np.clip(z, -30, 30)))
                self._step(F[idx], h, w[idx] * (p - y[idx]) / len(idx))
            if lam > 0 and edges is not None and len(edges):
                sel = edges[rng.choice(len(edges), size=min(256, len(edges)), replace=False)]
                nodes, inv = np.unique(sel, return_inverse=True); inv = inv.reshape(-1, 2)
                z, h = self.forward(Fall[nodes]); p = 1 / (1 + np.exp(-np.clip(z, -30, 30)))
                viol = np.maximum(p[inv[:, 0]] - p[inv[:, 1]], 0)
                dp = np.zeros(len(nodes)); np.add.at(dp, inv[:, 0], 2 * viol); np.add.at(dp, inv[:, 1], -2 * viol)
                self._step(Fall[nodes], h, lam * dp * p * (1 - p) / len(sel))


def _ll(p, y):
    q = np.clip(p, 1e-6, 1 - 1e-6); return float(-(y * np.log(q) + (1 - y) * np.log(1 - q)).mean())


def train_rfree(F, y, fam, edges=None, Fall=None, lam=0.0, seed=0, max_epochs=40, hold=0.2, w=None):
    """Train a fresh verdict head with an R-free split: whole families held out for early stopping
    and temperature calibration (labels inside a family are correlated, so the split is by family)."""
    rng = np.random.default_rng(seed); fams = np.unique(fam); m = MLP(seed=seed)
    if len(fams) < 5:
        m.fit(F, y, epochs=10, edges=edges, Fall=Fall, lam=lam, rng=rng, w=w); return m
    val_f = rng.choice(fams, max(1, int(round(hold * len(fams)))), replace=False)
    va = np.isin(fam, val_f); tr = ~va
    best, best_ll, bad = m.snapshot(), np.inf, 0
    for _ in range(max_epochs):
        m.fit(F[tr], y[tr], epochs=1, edges=edges, Fall=Fall, lam=lam, rng=rng, w=None if w is None else w[tr])
        ll = _ll(m.predict(F[va]), y[va])
        if ll < best_ll - 1e-4: best, best_ll, bad = m.snapshot(), ll, 0
        else:
            bad += 1
            if bad >= 5: break
    m.restore(best)
    z, _ = m.forward(F[va]); grid = np.exp(np.linspace(np.log(0.5), np.log(8), 25))
    m.T = float(min(grid, key=lambda T: _ll(1 / (1 + np.exp(-np.clip(z / T, -30, 30))), y[va])))
    return m
