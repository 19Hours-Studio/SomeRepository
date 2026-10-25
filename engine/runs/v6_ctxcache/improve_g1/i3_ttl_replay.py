# Idea 3: replay Mooncake FAST25 traces (github.com/kvcache-ai/Mooncake, FAST25-release/traces,
# ~1 h each, 512-token hash blocks). Prices as multiples of base input (Anthropic prompt caching
# docs): 5m write 1.25, 1h write 2.0, cache read 0.1, output 5.0 (Sonnet $3 in / $15 out).
# A keep-alive ping re-reads one request's whole prefix just before expiry (cost 0.1 x its input,
# + 1 output token) and refreshes every ancestor block. A session "returns" when a later request
# contains this request's last block.
import json, sys, heapq, collections
W5, W1H, RD, OUT, TTL, BLK = 1.25, 2.0, 0.1, 5.0, 300.0, 512

def load(f):
    R = [json.loads(l) for l in open(f)]
    for r in R: r['t'] = r['timestamp'] / 1000
    return sorted(R, key=lambda r: r['t'])

def leaf_episodes(R):
    """Idle time from each request to the next request that extends its leaf (None = never)."""
    nxt = {}
    out = [None] * len(R)
    for i in range(len(R) - 1, -1, -1):
        r = R[i]
        L = r['hash_ids'][-1]
        out[i] = nxt.get(L)
        for b in r['hash_ids']: nxt[b] = r['t']
    return [None if n is None else n - R[i]['t'] for i, n in enumerate(out)], R[-1]['t']

def hazard(R):
    eps, end = leaf_episodes(R)
    h = []
    for k in range(1, 12):
        lo, hi = TTL * k, TTL * (k + 1)
        # at risk: idle past lo and observable through hi (censor episodes cut by end of trace)
        risk = [g for g, r in zip(eps, R) if (g is None or g > lo) and r['t'] + hi <= end]
        ret = sum(1 for g in risk if g is not None and g <= hi)
        h.append(ret / max(1, len(risk)))
    return h

def bill(R, policy):
    """policy(k) -> True if the k-th ping (k=1..) after idle should be sent."""
    touch = {}                       # block -> last touch time
    seen = set()
    cost = w = rew = 0.0
    pend = []                         # heap of (time, req index, k)
    alive_req = {}
    def drain(t):
        nonlocal cost
        while pend and pend[0][0] < t:
            tp, i, k = heapq.heappop(pend)
            r = R[i]
            if alive_req.get(r['hash_ids'][-1]) != i: continue   # session moved on
            cost_ping = RD * r['input_length'] + OUT * 1
            cost += cost_ping
            for b in r['hash_ids']: touch[b] = max(touch.get(b, -1e9), tp)
            if policy(k + 1): heapq.heappush(pend, (tp + TTL - 1, i, k + 1))
    for i, r in enumerate(R):
        drain(r['t'])
        for j, b in enumerate(r['hash_ids']):
            n = BLK if j < len(r['hash_ids']) - 1 else r['input_length'] - BLK * j
            n = max(n, 0)
            if b in touch and r['t'] - touch[b] <= TTL:
                cost += RD * n
            else:
                cost += W5 * n; w += n
                if b in seen: rew += n
            seen.add(b); touch[b] = r['t']
        cost += OUT * r['output_length']
        alive_req[r['hash_ids'][-1]] = i
        if policy(1): heapq.heappush(pend, (r['t'] + TTL - 1, i, 1))
    drain(1e18)
    return cost, rew / max(w, 1), w

def bill_1h(R):
    touch = {}; cost = 0.0
    for r in R:
        for j, b in enumerate(r['hash_ids']):
            n = max(BLK if j < len(r['hash_ids']) - 1 else r['input_length'] - BLK * j, 0)
            cost += (RD if b in touch and r['t'] - touch[b] <= 3600 else W1H) * n
            touch[b] = r['t']
        cost += OUT * r['output_length']
    return cost

for f in sys.argv[1:]:
    R = load(f)
    h = hazard(R)
    print(f)
    print('  leaf hazard per 5-min window (k=1..):', ' '.join('%.3f' % x for x in h))
    base, f0, _ = bill(R, lambda k: False)
    print('  plain 5m: rewrite share of writes f=%.3f' % f0)
    for name, pol in [('ping always, 1x', lambda k: k <= 1), ('ping always, 3x', lambda k: k <= 3),
                      ('hazard>0.08 rule', lambda k: k <= len(h) and h[k - 1] > RD / W5)]:
        c, f1, _ = bill(R, pol)
        print('  %-18s f=%.3f bill ratio vs plain 5m = %.3f' % (name, f1, base / c))
    print('  1h TTL on all writes: ratio = %.3f' % (base / bill_1h(R)))
