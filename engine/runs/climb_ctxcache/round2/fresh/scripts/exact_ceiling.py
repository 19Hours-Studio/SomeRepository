# Exact-KV levers on Bailian chat/coder/thinking sessions, billed Anthropic-style
# (read 0.1, write 1.25, output 5). All of these keep the prompt and the KV bit-for-bit what a full
# recompute would use, so output quality is unchanged by construction.
#   carry : the server keeps the KV it produced while decoding a reply; the child request's blocks
#           right after the parent prompt (floor(parent output/16) blocks) hit while the parent's
#           entry is alive. Requires the client to re-send the reply token-identically.
#   keep1h: the provider retains prefixes 1 h (CPU/SSD tier) at no extra price.
import json, sys, os, collections
R, OUT, B = 0.1, 5.0, 16
W = float(os.environ.get("W", 1.25))       # W=1.0: OpenAI-style (no write premium)
ROWS = os.environ.get("ROWS", "anthropic")
def run(fn, ttl, carry):
    rs = [json.loads(l) for l in open(fn)]; par = {}
    exp = {}; cost = 0.0; out = 0.0; hit = tot = 0
    for r in rs:
        t = r["timestamp"]; h = r["hash_ids"]; ks = []; k = 0
        for b in h: k = hash((k, b)); ks.append(k)
        m = 0
        while m < len(ks) and exp.get(ks[m], -1) >= t: m += 1
        p = par.get(r["parent_chat_id"])
        if carry and p and m >= p[1] - 1 and t <= p[0] + ttl:
            m = max(m, min(len(ks), p[1] - 1 + p[2] // B))       # parent's reply blocks are already in KV
        cost += R * m * B + W * (len(ks) - m) * B; out += OUT * r["output_length"]; hit += m; tot += len(ks)
        for k in ks: exp[k] = t + ttl
        par[r["chat_id"]] = (t, len(ks), r["output_length"])
    return cost, out, hit / tot
for fn in sys.argv[1:]:
    base = None; print(fn.split("/")[-1])
    rows = [("5-min TTL (default)", 300, False), ("+ output carry-over", 300, True),
            ("provider keeps 1 h, no premium", 3600, False), ("both", 3600, True)]
    if ROWS == "openai":
        rows = [("in-memory, 5 min", 300, False), ("in-memory, 10 min", 600, False), ("prompt_cache_retention=24h", 86400, False)]
    for name, ttl, carry in rows:
        c, o, hr = run(fn, ttl, carry)
        if base is None: base = (c, c + o)
        print(f"  {name:32s} token hit {hr:5.1%}  billed input {c/base[0]-1:+6.1%}  whole bill {(c+o)/base[1]-1:+6.1%}")
