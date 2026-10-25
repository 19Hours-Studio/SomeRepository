# Anthropic ~20-block lookback (check1 item 3): does a second, persistent cache breakpoint at the
# start of the kept window restore the exact-LCP savings of batch clearing?
# Cache model: an entry is written at every breakpoint of every request (TTL ignored, as elsewhere).
# A request hits the longest cached prefix that ends at a block boundary at most LB blocks before one
# of its own breakpoints. Breakpoints: after the tool schema (always), at the end of the prompt, and
# (lb2) right after the last placeholder = start of the kept window, and (lb4) also at the previous
# request's window start, whose prefix a new clear leaves unchanged -> 4 breakpoints, Anthropic's maximum.
# Blocks: 1 per message, 2 per assistant message (text + tool_use), as in check1.
# Usage: python3 -I bp2.py data/traces.jsonl
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import traces as T
from ownstack import horizon_seq
W, R = T.PRICES["anthropic"]; LB = 20

def polling_seq(tr, ntok, P):  # SWE-agent LastNObservations(n=5, polling=P), as emulated in check1
    seq = []
    for a in T.requests(tr):
        obs = [i for i in range(a) if T.is_obs(tr, i)]
        m = max(0, len(obs) - T.KEEP); m = (m // P) * P
        seq.append(T.ctx(tr, ntok, a, set(obs[:m])))
    return seq

def bill(seq, nblk, mode):
    cache = set(); cost = 0; prev = []; prev_ws = None
    for s in seq:
        keys = [k for k, _ in s]; toks = [t for _, t in s]
        bnd = [0]                                   # bnd[j] = block index at the end of segment j-1
        for k in keys: bnd.append(bnd[-1] + nblk.get(k, 1))
        L = sum(toks)
        if mode == "lcp": c = T.lcp(prev, s)
        else:
            bps = {1, len(keys)}                    # segment counts at breakpoints: after tools, end
            ph = [j for j, k in enumerate(keys) if isinstance(k, tuple) and k[0] == "ph"]
            ws = ph[-1] + 1 if ph else None             # start of the kept window
            if mode in ("lb2", "lb4") and ws: bps.add(ws)
            if mode == "lb4" and prev_ws: bps.add(prev_ws)  # previous window start: its prefix is unchanged by this clear
            prev_ws = ws
            best = 0
            for b in bps:
                for j in range(b, 0, -1):
                    if bnd[b] - bnd[j] > LB: break
                    if tuple(keys[:j]) in cache: best = max(best, j); break
            c = sum(toks[:best])
            for b in bps: cache.add(tuple(keys[:b]))
        cost += R * c + W * (L - c); prev = s
    return cost

def main(path):
    tot = {}
    for tr in T.load(path):
        ntok = [T.tok(x) for x in tr["text"]]
        nblk = {(i, 0): 2 if r == "assistant" else 1 for i, r in enumerate(tr["role"])}
        pols = {"append": T.policy_seq(tr, ntok, "append", W, R), "sliding": T.policy_seq(tr, ntok, "sliding", W, R),
                "batch5k": T.policy_seq(tr, ntok, "batch", W, R, 5000), "horizon": horizon_seq(tr, ntok, W, R),
                "polling10": polling_seq(tr, ntok, 10)}
        for k, seq in pols.items():
            for mode in ("lcp", "lb1", "lb2", "lb4"):
                tot[(k, mode)] = tot.get((k, mode), 0) + bill(seq, nblk, mode)
    ap = tot[("append", "lcp")]
    print(f"{'policy':10s} {'exact LCP':>12s} {'1 bp':>12s} {'+window bp':>12s} {'4 bp':>12s}   (lookback 20)  4bp vs append  4bp vs exact LCP")
    for k in ("append", "sliding", "batch5k", "horizon", "polling10"):
        a, b, c, d = (tot[(k, m)] for m in ("lcp", "lb1", "lb2", "lb4"))
        print(f"{k:10s} {a:12,.0f} {b:12,.0f} {c:12,.0f} {d:12,.0f}   {d/ap-1:+.1%}   {d/a-1:+.2%}")

if __name__ == "__main__":
    main(sys.argv[1])
