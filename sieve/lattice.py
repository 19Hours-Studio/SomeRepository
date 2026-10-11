"""Conjecture lattice: label propagation along implication edges, misclosure, acquisition score.

Edge (i, j) means stmt i => stmt j (j is weaker). A verified TRUE node makes every descendant TRUE;
a verified FALSE node makes every ancestor FALSE. One verifier call therefore labels a whole cone.
Misclosure of a belief vector p: sum over edges of relu(p_i - p_j) - beliefs that do not respect
implication (like a surveying network whose loops do not close).
"""
from collections import defaultdict
import numpy as np


class Lattice:
    def __init__(self, n, edges):
        self.n = n
        self.edges = np.array(edges, dtype=np.int64).reshape(-1, 2)
        self.down, self.up = defaultdict(list), defaultdict(list)
        for i, j in edges:
            self.down[i].append(j); self.up[j].append(i)
        self.label = np.full(n, -1, dtype=np.int8)   # -1 unknown, 0 false, 1 true
        self.verified = np.zeros(n, dtype=bool)
        self._cd, self._ca = {}, {}  # cone caches (the DAG is fixed)

    def _cone(self, i, nbr):
        cache = self._cd if nbr is self.down else self._ca
        if i in cache: return cache[i]
        seen, stack = set(), [i]
        while stack:
            k = stack.pop()
            for m in nbr[k]:
                if m not in seen: seen.add(m); stack.append(m)
        cache[i] = np.fromiter(seen, dtype=np.int64, count=len(seen)); return cache[i]

    def descendants(self, i): return self._cone(i, self.down)
    def ancestors(self, i): return self._cone(i, self.up)

    def observe(self, i, truth, propagate=True):
        """Record a verified verdict; with propagate, label the implied cone. Returns #new labels."""
        new = int(self.label[i] < 0); self.label[i] = int(truth); self.verified[i] = True
        if propagate:
            cone = self.descendants(i) if truth else self.ancestors(i)
            fresh = cone[self.label[cone] < 0]; self.label[fresh] = int(truth); new += len(fresh)
        return new

    def misclosure(self, p):
        """Per-node misclosure: sum of relu(p_i - p_j) over incident edges."""
        if not len(self.edges): return np.zeros(self.n)
        i, j = self.edges[:, 0], self.edges[:, 1]
        v = np.maximum(p[i] - p[j], 0.0)
        m = np.zeros(self.n); np.add.at(m, i, v); np.add.at(m, j, v)
        return m

    def expected_reach(self, p, cand):
        """Expected entropy removed if candidate is verified: its own entropy plus the entropy of every
        unlabeled node its outcome would label (descendants if TRUE, ancestors if FALSE)."""
        unl = self.label < 0
        q = np.clip(p, 1e-6, 1 - 1e-6); h = -(q * np.log(q) + (1 - q) * np.log(1 - q)); h[~unl] = 0
        out = np.empty(len(cand))
        for t, i in enumerate(cand):
            d = h[self.descendants(i)].sum(); a = h[self.ancestors(i)].sum()
            out[t] = h[i] + q[i] * d + (1 - q[i]) * a
        return out

    def acquire(self, p, k, rng, beta=2.0):
        """Pick k unlabeled nodes maximizing expected entropy removed x (1 + beta * misclosure)."""
        cand = np.flatnonzero(self.label < 0)
        if len(cand) <= k: return cand
        score = (1 + beta * self.misclosure(p)[cand]) * self.expected_reach(p, cand)
        score += 1e-9 * rng.random(len(cand))  # tie-break
        return cand[np.argsort(-score)[:k]]
