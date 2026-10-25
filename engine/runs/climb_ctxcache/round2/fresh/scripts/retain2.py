# Retention policies that decide per request: an oracle that knows when (and whether) the user
# comes back, and an online rule trained on even chat_ids and scored on odd ones.
import sys, math, collections
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from retain import load, replay, keys, R, W5, W60, DT
def bucket(r): return min(r["turn"], 6)
def hazards(train):
    """P(child in (300, 3600] s) and per-ping-window conditional hazards, by turn bucket"""
    n = collections.Counter(); mid = collections.Counter(); win = collections.defaultdict(lambda: collections.Counter())
    for r in train:
        b = bucket(r); g = r["next"] - r["timestamp"]; n[b] += 1
        if 300 < g <= 3600: mid[b] += 1
        for k in range(1, 13):                    # window k: child arrives in (k*DT, k*DT+300] given none by k*DT
            if g > k * DT: win[b][(k, 0)] += 1; win[b][(k, 1)] += (g <= k * DT + 300)
    pm = {b: mid[b] / n[b] for b in n}
    hz = {b: [win[b][(k, 1)] / max(1, win[b][(k, 0)]) for k in range(1, 13)] for b in n}
    return pm, hz
def main(fn):
    rs = load(fn); t_end = max(r["timestamp"] for r in rs)
    par = {r["chat_id"]: r for r in rs}
    for r in rs:                                    # session root, for a train/test split by session
        q = r
        while q["parent_chat_id"] in par: q = par[q["parent_chat_id"]]
        r["root"] = q["chat_id"]
    pm, hz = hazards([r for r in rs if r["root"] % 2 == 0])
    def new_blocks(r):
        p = par.get(r["parent_chat_id"]); return len(r["hash_ids"]) - (len(p["hash_ids"]) - 1 if p else 0)
    def oracle(r):
        g = r["next"] - r["timestamp"]; n = len(r["hash_ids"]); nn = max(1, new_blocks(r))
        if g <= 300 or g == math.inf: return (300, 0)
        pings = math.ceil((g - 300) / DT); miss = (W5 - R) * n
        c60 = (W60 - W5) * nn if g <= 3600 else miss; cp = pings * (R * n + 0.3)
        best = min(miss, c60, cp)
        return (3600, 0) if best == c60 and c60 < miss else ((300, pings) if best == cp and cp < miss else (300, 0))
    def online(r):
        b = bucket(r); n = len(r["hash_ids"]); nn = max(1, new_blocks(r))
        if pm.get(b, 0) * (W5 - R) * n > (W60 - W5) * nn: return (3600, 0)
        k = 0                                      # ping while the conditional return hazard pays for the ping
        while k < 12 and hz.get(b, [0] * 12)[k] * (W5 - R) * n > R * n + 0.3: k += 1
        return (300, k)
    print(fn.split("/")[-1], " turn buckets P(return 5-60 min):", {b: round(v, 3) for b, v in sorted(pm.items())})
    test = lambda r: r["root"] % 2 == 1
    res = {}
    for name, p in [("5-min TTL (default)", lambda r: (300, 0)), ("1-h TTL on every write", lambda r: (3600, 0)),
                    ("online insurance rule", lambda r: online(r) if test(r) else (300, 0)),
                    ("oracle (knows return time)", lambda r: oracle(r) if test(r) else (300, 0))]:
        c, hr = replay(rs, p, t_end, test); res[name] = (c, hr)
    b = res["5-min TTL (default)"][0]; bi = b["input"]; bt = bi + b["output"]
    for name, (c, hr) in res.items():
        inp = c["input"] + c["ping"]
        print(f"  {name:28s} hit {hr:5.1%}  input+pings {inp/bi-1:+6.1%}  total incl. output {(inp+c['output'])/bt-1:+6.1%}")
    print("  (rule trained on sessions with even root id; all numbers are for the held-out odd-root sessions)")
for fn in sys.argv[1:]: main(fn)
