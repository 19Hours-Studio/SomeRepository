# Anthropic-style billing replay of Bailian sessions under retention policies.
# Units: input-token equivalents (base input price = 1). Read 0.1, 5-min write 1.25, 1-h write 2.0,
# output 5.0 (Sonnet/Opus ratio). A ping re-sends the leaf prompt with max_tokens=1.
# write_ttl 0 = the cache breakpoint stays at the end of the already-cached prefix, so new tokens
# are billed at 1.0 and not written.
import json, sys, heapq, collections
R, W5, W60, OUT = 0.1, 1.25, 2.0, 5.0
B = 16                               # tokens per block
DT = 270                             # ping every 4.5 min
def load(fn):
    rs = [json.loads(l) for l in open(fn)]
    kids = collections.defaultdict(list)
    for r in rs:
        if r["parent_chat_id"] >= 0: kids[r["parent_chat_id"]].append(r["timestamp"])
    for r in rs: r["next"] = min(kids.get(r["chat_id"], [float("inf")]))
    return rs
def keys(h):
    k = 0; out = []
    for b in h: k = hash((k, b)); out.append(k)
    return out
def replay(rs, policy, t_end, group=lambda r: True):
    """policy(r) -> (write_ttl, n_pings); costs and hit rate are summed over requests with group(r)"""
    exp = {}; ttl = {}; cost = collections.Counter(); hitb = totb = 0
    def serve(ks, t, wttl, is_ping):
        nonlocal hitb, totb
        m = 0
        while m < len(ks) and exp.get(ks[m], -1) >= t: m += 1
        w = W60 if wttl == 3600 else (W5 if wttl else 1.0)
        c = R * m * B + w * (len(ks) - m) * B
        for i, k in enumerate(ks):
            if i >= m and not wttl: break                           # breakpoint left at the cached boundary: new tokens not written
            if i < m and wttl != 3600: exp[k] = t + ttl[k]          # refresh with its own TTL
            else: ttl[k] = wttl; exp[k] = t + wttl                  # write, or upgrade to 1 h
        return c, m
    ev = []
    for i, r in enumerate(rs): heapq.heappush(ev, (r["timestamp"], 0, i, 0))
    while ev:
        t, kind, i, k = heapq.heappop(ev); r = rs[i]
        if kind == 0:
            ks = keys(r["hash_ids"]); r["_k"] = ks
            wttl, n = policy(r)
            c, m = serve(ks, t, wttl, False)
            if group(r): cost["input"] += c; cost["output"] += OUT * r["output_length"]; hitb += m; totb += len(ks)
            if n: heapq.heappush(ev, (t + DT, 1, i, 1))
        else:
            if r["next"] <= t or t > t_end: continue               # user came back, or trace window over
            c, m = serve(r["_k"], t, 300, True)
            if group(r): cost["ping"] += c + OUT * 1
            if k < policy(r)[1]: heapq.heappush(ev, (t + DT, 1, i, k + 1))
    return cost, hitb / max(1, totb)
if __name__ == "__main__":
    for fn in sys.argv[1:]:
        rs = load(fn); t_end = max(r["timestamp"] for r in rs)
        pols = {"5-min TTL (default)": lambda r: (300, 0),
                "1-h TTL on every write": lambda r: (3600, 0),
                "5-min + 2 pings (Aider-style)": lambda r: (300, 2),
                "5-min + 11 pings": lambda r: (300, 11)}
        base = None
        print(fn.split("/")[-1])
        for name, p in pols.items():
            c, hr = replay(rs, p, t_end); inp = c["input"] + c["ping"]
            if base is None: base = (inp, inp + c["output"])
            print(f"  {name:32s} hit {hr:5.1%}  input+pings {inp/1e6:8.1f}M ({inp/base[0]-1:+6.1%})  total incl. output {(inp+c['output'])/base[1]-1:+6.1%}  [pings {c['ping']/1e6:.1f}M]")
