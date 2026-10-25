# Idea 1 fix: popularity-first order + "write on second sighting" breakpoint admission + per-regime TTL.
# Setup as eval_g1/c1/pop_order_ttl.py: 100k chunks, top-5 Zipf, docs 4k tok (5 x 0.8k), system 1k cached (0.1),
# question 0.2k, output 0.3k @5x. Anthropic multipliers: 5m write 1.25, 1h write 2.0, read 0.1, uncached 1.0.
# Baseline = best current API practice: docs sent uncached (5.8 units per request).
# Old rule: breakpoints at docs 2..5 always (every miss is written at 1.25).
# New rule: prefix depth k is written only if the same prefix was already SEEN (ghost entry, no KV) within the TTL
# window; depths not admitted are sent after the last breakpoint at 1.0x. At most 4 breakpoints: depths {2,3,4,5}.
import numpy as np, sys
rng = np.random.default_rng(0)
C, K, N = 100_000, 5, int(sys.argv[1]) if len(sys.argv) > 1 else 100_000
BASE = 0.1 + 4 + 0.2 + 1.5
def draws(s):
    p = 1 / np.arange(1, C + 1) ** s; p /= p.sum()
    out = []
    for row in rng.choice(C, size=(N, 12), p=p):
        u = list(dict.fromkeys(row.tolist()))[:K]
        while len(u) < K:
            u = list(dict.fromkeys(u + [int(rng.choice(C, p=p))]))
        out.append(sorted(u))            # id = Zipf rank = what the online counter converges to
    return out
def replay(R, W, wcost, admit):
    cache, ghost, tot = {}, {}, 0.0
    for t, o in enumerate(R):
        hit = 0
        for k in (2, 3, 4, 5):           # lookback finds the deepest alive entry
            key = tuple(o[:k])
            if key in cache and t - cache[key] <= W: hit = k
        wd = hit
        for k in (2, 3, 4, 5):
            if k <= hit: continue
            key = tuple(o[:k])
            if (not admit) or (key in ghost and t - ghost[key] <= W): wd = k
            ghost[key] = t
        for k in (2, 3, 4, 5):
            if k <= wd: cache[tuple(o[:k])] = t   # read refreshes TTL; write creates
        d = 0.8  # k tokens per doc
        tot += d * (hit * 0.1 + (wd - hit) * wcost + (K - wd) * 1.0) + 1.8
    return BASE * len(R) / tot
for s in (1.05, 1.2, 1.5):
    R = draws(s)
    for W in (1000, 100, 10):          # requests per 5 minutes in one org's cache
        old = replay(R, W, 1.25, False)
        new5 = replay(R, W, 1.25, True)
        new1h = replay(R, 12 * W, 2.0, True)
        print("zipf %.2f W=%4d/5min: old always-write %.3fx | admit 5m %.3fx | admit 1h %.3fx | best %.3fx"
              % (s, W, old, new5, new1h, max(new5, new1h)), flush=True)
