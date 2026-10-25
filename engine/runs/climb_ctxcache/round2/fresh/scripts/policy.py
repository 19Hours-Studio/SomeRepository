# Per-request cache-control choice on Anthropic-style pricing, replayed on Bailian sessions:
#   skip  : breakpoint stays at the end of the already-cached prefix (new tokens billed 1.0, not written)
#   w5    : breakpoint at the end, 5-min TTL (the default, 1.25 on new tokens)
#   w60   : breakpoint at the end, 1-h TTL (2.0 on new tokens)
#   pings : w5 plus keep-alive re-sends every 4.5 min (0.1 x prompt each) until the user returns
# The online rule estimates P(next turn within 5 min) and P(within 5-60 min) per (turn, type) bucket
# on sessions with an even root id, and is scored on the odd ones.
import sys, os, math, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from retain import load, replay, R, W5, W60, DT
def bucket(r): return (min(r["turn"], 6), r["type"])
def main(fn):
    rs = load(fn); t_end = max(r["timestamp"] for r in rs); par = {r["chat_id"]: r for r in rs}
    for r in rs:
        q = r
        while q["parent_chat_id"] in par: q = par[q["parent_chat_id"]]
        r["root"] = q["chat_id"]
        p = par.get(r["parent_chat_id"]); r["nn"] = max(1, len(r["hash_ids"]) - (len(p["hash_ids"]) - 1 if p else 0))
    train = [r for r in rs if r["root"] % 2 == 0 and r["timestamp"] < t_end - 3600]   # outcome fully observed
    cnt = collections.Counter(); c5 = collections.Counter(); c60 = collections.Counter()
    for r in train:
        g = r["next"] - r["timestamp"]; b = bucket(r); cnt[b] += 1; c5[b] += g <= 300; c60[b] += 300 < g <= 3600
    P = {b: (c5[b] / cnt[b], c60[b] / cnt[b]) for b in cnt}
    def choose(n, nn, p5, pm):
        e = {"skip": 1.0 * nn + p5 * (R * (n - nn) + W5 * nn) + pm * W5 * n,
             "w5": W5 * nn + p5 * R * n + pm * W5 * n,
             "w60": W60 * nn + (p5 + pm) * R * n}
        return min(e, key=e.get)
    code = {"skip": (0, 0), "w5": (300, 0), "w60": (3600, 0)}
    def online(r):
        p5, pm = P.get(bucket(r), (0.0, 0.0)); return code[choose(len(r["hash_ids"]), r["nn"], p5, pm)]
    def oracle(r):
        g = r["next"] - r["timestamp"]; n = len(r["hash_ids"]); nn = r["nn"]
        if g <= 300: return (300, 0)
        if g == math.inf or g > 3600: return (0, 0)
        opts = {(0, 0): 1.0 * nn + W5 * n, (300, 0): W5 * nn + W5 * n, (3600, 0): W60 * nn + R * n}
        k = math.ceil((g - 300) / DT); opts[(300, k)] = W5 * nn + k * (R * n + 0.3) + R * n
        return min(opts, key=opts.get)
    test = lambda r: r["root"] % 2 == 1
    pols = [("default: 5-min breakpoint at end", lambda r: (300, 0)),
            ("never write new tokens", lambda r: (0, 0)),
            ("1-h TTL on every write", lambda r: (3600, 0)),
            ("online per-request choice", online),
            ("oracle per-request choice", oracle)]
    out = {}
    for name, p in pols: out[name] = replay(rs, p, t_end, test)
    b = out[pols[0][0]][0]; bi = b["input"]; bt = bi + b["output"]
    print(f"{fn.split('/')[-1]}  (held-out sessions; output is {b['output']/bt:.0%} of the default bill)")
    for name, (c, hr) in out.items():
        inp = c["input"] + c["ping"]
        print(f"  {name:34s} token hit {hr:5.1%}  billed input {inp/bi-1:+6.1%}  whole bill {(inp + c['output'])/bt-1:+6.1%}")
    mix = collections.Counter(online(r) for r in rs if test(r))
    print("  online choices:", {({(0,0):'skip',(300,0):'w5',(3600,0):'w60'})[k]: f"{v/sum(mix.values()):.0%}" for k, v in mix.items()})
for fn in sys.argv[1:]: main(fn)
