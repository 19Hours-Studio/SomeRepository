# Cost model: per-session and per-request-served cost on a hosted API with prefix caching.
# Prices: Anthropic Sonnet-class $3/M input, $15/M output; 5-min write 1.25x, 1-h write 2x, read 0.1x
# (docs.claude.com prompt-caching; Manus blog quotes $0.30 vs $3 cached/uncached).
import random, statistics as st
PIN, POUT = 3e-6, 15e-6
W5, W1H, RD = 1.25, 2.0, 0.10

def session(doc, turns, edits, patch, q=60, ans=400, sysp=3000, mode="inline",
            W=W5, compact="ski", share_cap=0.05, seed=0):
    """mode: inline (rewrite doc in place), chain (append patches to history),
       ledger (floating depth-1 ledger after the question, never cached into history),
       doclast (doc placed after history every turn)."""
    rng = random.Random(seed)
    edit_turns = set(rng.sample(range(1, turns), edits)) if edits else set()
    hist = 0              # tokens of history after doc
    cost = 0.0
    # turn 0 write of system+doc
    cached = 0            # tokens currently cached in prefix
    ledger = {}           # section_pos -> patch tokens (depth-1)
    ledger_spend = 0.0
    chain = 0             # patch tokens in history (chain mode)
    stale_keys = {}
    first = True
    for t in range(turns):
        if t in edit_turns:
            pos = rng.randint(0, doc - 1)
            sec = pos // 500
            if mode == "inline":
                # invalidate from edit position onward
                cached = min(cached, sysp + pos)
            elif mode == "chain":
                hist += patch  # patch appended as new content (billed as new tokens below)
                stale_keys[sec] = stale_keys.get(sec, 0) + 1
                cost += patch * PIN * W
            elif mode == "ledger":
                ledger[sec] = (patch, pos)
            elif mode == "doclast":
                pass
        if mode == "doclast":
            # [sys, hist, doc, q]; hist grows by previous turn, doc always after it => doc never re-hit
            total = sysp + hist + doc + q
            hitp = sysp + hist  # prefix through history hits (previous turn wrote it)
            cost += hitp * PIN * RD + (doc + q) * PIN * W if not first else total * PIN * W
        else:
            total = sysp + doc + hist + q
            if first:
                cost += total * PIN * W
            else:
                cost += cached * PIN * RD + (total - cached) * PIN * W
            if mode == "ledger":
                L = sum(p for p, _ in ledger.values())
                cost += L * PIN * 1.0          # uncached tail, rewritten every turn
                ledger_spend += L * PIN
                if ledger:
                    pmin = min(p for _, p in ledger.values())
                    R = (doc - pmin + hist) * PIN * W
                    over = L > share_cap * (doc + hist)
                    if (compact == "ski" and ledger_spend >= R) or over:
                        cost += R             # fold patches in, rewrite from earliest edit
                        ledger.clear(); ledger_spend = 0.0
        cached = total
        first = False
        cost += ans * POUT
        hist += q + ans                        # answer becomes input next turn (written then)
    return cost, max(stale_keys.values()) if stale_keys else 0

def per_request(**kw):
    turns = kw["turns"]
    c, d = session(**kw)
    return c / turns, d

if __name__ == "__main__":
    scen = {
      "C 25k doc, 10 q, 3 edits":      dict(doc=25_000, turns=10, edits=3, patch=500),
      "C 25k doc, 10 q, 1 edit":       dict(doc=25_000, turns=10, edits=1, patch=500),
      "D copilot 120k, 30 q, 15 edits":dict(doc=120_000, turns=30, edits=15, patch=300),
      "D' 120k, 30 q, 5 edits":        dict(doc=120_000, turns=30, edits=5, patch=300),
      "E mutable-state 8k at front of 150k agent, 40 calls, 20 edits":
                                       dict(doc=150_000, turns=40, edits=20, patch=200),
    }
    for name, kw in scen.items():
        print(name)
        res = {}
        for m in ["inline", "doclast", "chain", "ledger"]:
            vals = [per_request(mode=m, seed=s, **kw) for s in range(200)]
            res[m] = st.mean(v[0] for v in vals)
            depth = max(v[1] for v in vals)
            print(f"  {m:8s} ${res[m]*1000:7.2f} per 1k requests? -> ${res[m]:.4f}/request  max patch depth {depth}")
        best_base = min(res["inline"], res["doclast"])
        print(f"  ratio best-baseline/ledger = {best_base/res['ledger']:.2f}   inline/chain = {res['inline']/res['chain']:.2f}")
