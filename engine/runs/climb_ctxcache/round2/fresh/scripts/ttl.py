# Global prefix cache over each Bailian trace with per-entry last-use times: what share of the
# reusable prefix (infinite cache) is still hit under a TTL that refreshes on every use.
import json, sys
TTLS = [300, 600, 1800, 3600, float("inf")]
for fn in sys.argv[1:]:
    last = {}; tot = 0; hit = [0] * len(TTLS); rows = 0; t_end = 0
    for line in open(fn):
        r = json.loads(line); t = r["timestamp"]; h = r["hash_ids"]; tot += len(h)
        key = 0; ages = []
        for b in h:
            key = hash((key, b)); lu = last.get(key)
            if lu is None: break
            ages.append(t - lu)
        for j, T in enumerate(TTLS):
            # ages along the matched path are non-decreasing; count the leading run within TTL
            k = 0
            while k < len(ages) and ages[k] <= T: k += 1
            hit[j] += k
        key = 0
        for b in h:
            key = hash((key, b)); last[key] = t
    s = "  ".join(f"TTL {('%dm' % (T/60)) if T != float('inf') else 'inf'}: {x/tot:5.1%}" for T, x in zip(TTLS, hit))
    print(f"{fn.split('/')[-1]:30s} prefix-hit share of input blocks  {s}")
