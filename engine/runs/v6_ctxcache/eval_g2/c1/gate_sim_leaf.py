"""Gate replay for ideas 1, 3, 4 (RAG doc ordering under Anthropic prompt caching).
Units: base-input-token cost (1.0 = $3/MTok). Request = 1k system + 5x800 doc + 200 question + 300 output(5x).
Baseline (best current practice): system cached (0.1), docs uncached (1.0) -> 5800 units = $0.0174 (ledger B).
Retrieval: 5 distinct chunks drawn Zipf(s) from 100k corpus, Poisson arrivals R per 5 min.
Order = descending global popularity (true rank; oracle counter, optimistic for the ideas).
Cache: entry per (path prefix of depth d) with expiry; read refreshes TTL. Read longest live prefix.
"""
import numpy as np, sys, math
N, K, DOC, SYS, Q, OUT = 100_000, 5, 800, 1000, 200, 300
FIXED = 0.1 * SYS + Q + 5 * OUT  # system read + question + output
BASE = FIXED + K * DOC

def draw(rng, s, n):
    p = 1.0 / np.arange(1, N + 1) ** s; p /= p.sum()
    out = []
    while len(out) < n:
        x = rng.choice(N, size=(n, 8), p=p)
        for row in x:
            u = sorted(set(row.tolist()))[:K] if len(set(row.tolist())) >= K else None
            # keep first 5 distinct draws, then sort by rank (= popularity order)
            seen = []
            for v in row.tolist():
                if v not in seen: seen.append(v)
                if len(seen) == K: break
            if len(seen) == K: out.append(tuple(sorted(seen)))
            if len(out) == n: break
    return out, p

def run(policy, s, R, nreq=40_000, seed=1, ttl_min=5.0, wmult=1.25, pings=False):
    rng = np.random.default_rng(seed)
    reqs, p = draw(rng, s, nreq)
    t = np.cumsum(rng.exponential(5.0 / R, nreq))  # minutes
    exp = {}   # prefix tuple -> expiry
    seen = {}  # prefix tuple -> last seen time (second-sighting list)
    cost = 0.0; hit_doc = 0; ping_cost = 0.0
    lam_doc = p * R  # true per-doc arrivals per 5-min (approx: 5 draws/request)
    lam_doc = lam_doc * K
    if pings:
        # oracle path rates from the whole stream
        from collections import Counter
        cnt = Counter()
        for r in reqs:
            cnt[r] += 1
        windows = t[-1] / 5.0
        warm = {k for k, c in cnt.items() if (1 - math.exp(-c / windows)) * 1.25 > 0.1}
        first_write = {}
    for r, ti in zip(reqs, t):
        # longest live cached prefix
        h = 0
        for d in range(K, 0, -1):
            e = exp.get(r[:d])
            if e is not None and (e >= ti or (pings and r[:d] in first_write)):
                h = d; break
        if policy == 'always':      # breakpoints at depths 2..5 (4 bps)
            bps = [2, 3, 4, 5]
        elif policy == 'second':    # idea 3: bp only at depths seen within TTL
            bps = [d for d in range(2, K + 1) if seen.get(r[:d], -1e9) >= ti - ttl_min]
        elif policy == 'single':    # idea 1: one bp after last doc with per-doc P>0.217
            k = sum(1 for v in r if 1 - math.exp(-lam_doc[v]) > 0.217)
            bps = [k] if k >= 1 else []
        last = max(bps) if bps else 0
        last = max(last, h)
        c = FIXED + 0.1 * DOC * h + wmult * DOC * max(0, last - h) + 1.0 * DOC * (K - last)
        cost += c; hit_doc += h
        for d in range(1, K + 1):
            if d <= h or d in bps: exp[r[:d]] = ti + ttl_min
            seen[r[:d]] = ti
        if pings:
            for d in bps:
                if r[:d] in warm and r[:d] not in first_write: first_write[r[:d]] = ti
    if pings:
        T = t[-1]
        for k, t0 in first_write.items():
            ping_cost += (T - t0) / 5.0 * (0.1 * (SYS + DOC * len(k)) + 5 * 1)
        cost += ping_cost
    n = len(reqs)
    return BASE / (cost / n), hit_doc / (K * n), ping_cost / n

if __name__ == '__main__':
    for s in (1.05, 1.2, 1.5):
        for R in (10, 100, 1000):
            ttl, wm = (60.0, 2.0) if R < 1000 else (5.0, 1.25)
            a = run('always', s, R)
            i1 = run('single', s, R)
            i3 = run('second', s, R, ttl_min=ttl, wmult=wm)
            i3_5m = run('second', s, R)
            i4 = run('always', s, R, pings=True)
            print(f"s={s} R={R}: always {a[0]:.3f}(hit {a[1]:.2f}) | I1 {i1[0]:.3f}(hit {i1[1]:.2f}) | "
                  f"I3 {i3[0]:.3f}(hit {i3[1]:.2f}) I3-5m {i3_5m[0]:.3f} | I4 {i4[0]:.3f}(hit {i4[1]:.2f}, ping/req {i4[2]:.0f})",
                  flush=True)
