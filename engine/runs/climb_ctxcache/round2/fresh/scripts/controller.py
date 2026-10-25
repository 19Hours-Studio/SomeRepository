# Provider-side, cost-based retention for session KV, replayed on Bailian sessions.
# After each request, its prompt KV (plus the reply KV it just decoded: "carry-over") stays in the
# hot tier (HBM/DRAM) for 5 min, as today. The controller then decides how long T to keep it on
# NVMe: T is chosen per (turn bucket, request type) to minimise recompute + storage cost on training
# sessions (even root id) and scored on held-out sessions (odd root id).
# Cost of a child request = prefill FLOPs of its blocks not served from cache; storage = KV bytes x
# NVMe $/GB-h x time on NVMe. Prices as in keep_cost.py. Cross-session prefix sharing (system
# prompts) is left out: it is the same under every policy here.
import json, sys, collections, math
GPU = 2.0 / 3600 / (0.45 * 989e12); NVME = 0.00014; B = 16
MODELS = {"dense 72B (BF16 KV)": (327680, 144e9), "MoE 30B-A3B (BF16 KV)": (98304, 6.6e9)}
TS = [0, 300, 600, 1200, 1800, 3300]          # NVMe keep time after the 5-min hot window
def lcp(a, b):
    n = min(len(a), len(b)); i = 0
    while i < n and a[i] == b[i]: i += 1
    return i
def sessions(fn):
    rs = {}; ev = []
    for line in open(fn):
        r = json.loads(line); rs[r["chat_id"]] = r
    for r in rs.values():
        q = r
        while q["parent_chat_id"] in rs: q = rs[q["parent_chat_id"]]
        r["root"] = q["chat_id"]; r["kids"] = []
    for r in rs.values():
        p = rs.get(r["parent_chat_id"])
        if p: p["kids"].append(r)
    t_end = max(r["timestamp"] for r in rs.values())
    # today's prefill (5-min global prefix cache, every request) of each held-out session, the denominator
    last = {}; miss = collections.Counter()
    for r in sorted(rs.values(), key=lambda r: r["timestamp"]):
        k = 0; m = 0; alive = True
        for b in r["hash_ids"]:
            k = hash((k, b)); alive = alive and last.get(k, -1e9) >= r["timestamp"] - 300; m += alive; last[k] = r["timestamp"]
        miss[r["root"] % 2] += len(r["hash_ids"]) - m
    global MISS; MISS = miss
    for r in rs.values():
        if r["timestamp"] > t_end - 3600 - 300: continue       # outcome not fully observed
        L = len(r["hash_ids"]); carry = r["output_length"] // B
        k = min(r["kids"], key=lambda c: c["timestamp"]) if r["kids"] else None
        g = k["timestamp"] - r["timestamp"] if k else math.inf
        m = lcp(r["hash_ids"], k["hash_ids"]) if k else 0
        reuse = min(len(k["hash_ids"]), m + (carry if m >= L - 1 else 0)) if k else 0
        ev.append(dict(root=r["root"], cat=(min(r["turn"], 6), r["type"]), L=L + carry, g=g, reuse=reuse, reuse_plain=m))
    return ev
def cost(e, T, kvb, fl, carry=True):
    """recompute + storage for the child's reuse of this request's KV, keep time T on NVMe"""
    need = e["reuse"]                                     # session tokens the child re-sends (incl. the reply)
    g = e["g"]; hit = g <= 300 or (g <= 300 + T)
    reuse = (e["reuse"] if carry else e["reuse_plain"]) if hit else 0
    rec = (need - reuse) * B * fl * GPU
    held = 0.0 if g <= 300 else min(g - 300, T)
    return rec + e["L"] * B * kvb / 1e9 * NVME * held / 3600, reuse
for fn in sys.argv[1:]:
    ev = sessions(fn); tr = [e for e in ev if e["root"] % 2 == 0]; te = [e for e in ev if e["root"] % 2 == 1]
    reuse_te = sum(e["reuse"] for e in te)
    print(f"{fn.split('/')[-1]}: {len(te)} held-out requests; re-sent session tokens {16*reuse_te/1e6:.1f}M; held-out sessions' 5-min-cache prefill {16*MISS[1]/1e6:.1f}M tokens")
    for mn, (kvb, fl) in MODELS.items():
        best = {}
        for c in {e["cat"] for e in tr}:
            ec = [e for e in tr if e["cat"] == c]
            best[c] = min(TS, key=lambda T: sum(cost(e, T, kvb, fl)[0] for e in ec))
        rows = [("today: 5-min hot tier, no carry-over", lambda e: 0, False),
                ("+ carry-over of reply KV", lambda e: 0, True),
                ("+ keep everything 1 h on NVMe", lambda e: 3300, True),
                ("+ per-category keep time (trained)", lambda e: best.get(e["cat"], 0), True),
                ("oracle keep time", None, True)]
        base = None
        print(f"  {mn}")
        for name, pol, carry in rows:
            c = h = 0.0
            for e in te:
                if pol is None:
                    x = min((cost(e, T, kvb, fl, carry) for T in TS), key=lambda z: z[0])
                else: x = cost(e, pol(e), kvb, fl, carry)
                c += x[0]; h += x[1]
            if base is None: base = c; tot = MISS[1] * B * fl * GPU
            print(f"    {name:40s} session-reuse hit {h/reuse_te:5.1%}  recompute+storage ${c:7.3f}  change in the sessions' whole prefill bill {(c-base)/tot:+6.1%}")
        print(f"    trained keep times (s): {dict(sorted(collections.Counter(best.values()).items()))}")
