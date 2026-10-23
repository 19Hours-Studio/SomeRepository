# Round 2: positions configurable, TTL expiry, Idea-2 policy (chain + depth cap + ski-rental + free fold on expiry)
import random, statistics as st
PIN, POUT = 3e-6, 15e-6
W5, RD = 1.25, 0.10

def run(doc, turns, edits, patch, mode, pos_lo=0, pos_hi=None, q=60, ans=400, sysp=3000,
        p_expire=0.0, share_cap=0.05, depth_cap=1, seed=0):
    rng = random.Random(seed)
    pos_hi = doc if pos_hi is None else pos_hi
    et = set(rng.sample(range(1, turns), edits)) if edits else set()
    hist = cost = 0.0; cached = 0
    ledger = {}; spend = 0.0
    chainkeys = {}; chain_tok = 0; chain_first = None; maxdepth = 0; fullrebuilds = 0
    for t in range(turns):
        expired = t > 0 and rng.random() < p_expire
        if expired: cached = 0
        if t in et:
            pos = rng.randint(pos_lo, pos_hi - 1); sec = pos // 500
            if mode == "inline":
                cached = min(cached, sysp + pos)
            elif mode == "ledger":
                ledger[sec] = (patch, pos)
            elif mode in ("chain", "idea2"):
                chainkeys[sec] = chainkeys.get(sec, 0) + 1
                chain_first = pos if chain_first is None else min(chain_first, pos)
                hist += patch; chain_tok += patch
                if mode == "idea2" and chainkeys[sec] > depth_cap:
                    # second edit of same key -> fold (rewrite from earliest edited pos)
                    cached = min(cached, sysp + chain_first); hist -= chain_tok
                    chain_tok = 0; chainkeys = {}; chain_first = None; fullrebuilds += 1
        total = sysp + doc + hist + q
        if mode == "idea2" and chain_tok and expired:
            # cache already gone: fold patches into the doc for free
            hist -= chain_tok; total -= chain_tok; chain_tok = 0; chainkeys = {}; chain_first = None
        cost += cached * PIN * RD + (total - cached) * PIN * W5
        if mode == "ledger" and ledger:
            L = sum(p for p, _ in ledger.values()); cost += L * PIN; spend += L * PIN
            pmin = min(p for _, p in ledger.values())
            R = (doc - pmin + hist) * PIN * W5
            if expired or spend >= R or L > share_cap * (doc + hist):
                # fold: next request rewrites from pmin (free if expired: we are writing anyway)
                if not expired: cost += R
                ledger.clear(); spend = 0.0; fullrebuilds += 1
        if mode == "idea2" and chain_tok:
            spend += chain_tok * PIN * RD
            # ski rental: fold once cumulative extra reads of patch tokens exceed a rewrite
            R = (doc - chain_first + hist) * PIN * W5
            if spend >= R:
                cost += R; hist -= chain_tok; chain_tok = 0; chainkeys = {}; chain_first = None; spend = 0
        maxdepth = max([maxdepth] + list(chainkeys.values()))
        cached = total
        cost += ans * POUT; hist += q + ans
    return cost / turns, maxdepth

def table(name, kw, modes=("noedit", "inline", "chain", "ledger", "idea2")):
    out = {}
    for m in modes:
        k = dict(kw); 
        if m == "noedit": k["edits"] = 0; mm = "inline"
        else: mm = m
        v = [run(mode=mm, seed=s, **k) for s in range(300)]
        out[m] = (st.mean(x[0] for x in v), max(x[1] for x in v))
    s = "  ".join(f"{m}=${c:.4f}(d{d})" for m, (c, d) in out.items())
    print(f"{name}\n  {s}\n  inline/ledger={out['inline'][0]/out['ledger'][0]:.2f} inline/idea2={out['inline'][0]/out['idea2'][0]:.2f} "
          f"chain/ledger={out['chain'][0]/out['ledger'][0]:.2f} floor(noedit)/ledger={out['noedit'][0]/out['ledger'][0]:.2f}")
    return out

if __name__ == "__main__":
    S = {
     "C 25k,10q,3 edits uniform": dict(doc=25_000, turns=10, edits=3, patch=500),
     "C 25k,10q,3 edits, 30% gaps>TTL": dict(doc=25_000, turns=10, edits=3, patch=500, p_expire=0.3),
     "D copilot 120k,30q,15 edits uniform": dict(doc=120_000, turns=30, edits=15, patch=300),
     "D copilot 120k,30q,15 edits, 30% gaps>TTL": dict(doc=120_000, turns=30, edits=15, patch=300, p_expire=0.3),
     "E agent: mutable 8k state at front of 150k, 40 calls, 20 edits": dict(doc=150_000, turns=40, edits=20, patch=200, pos_lo=0, pos_hi=8000),
     "F RAG: edits in last 10% of 25k (tail)": dict(doc=25_000, turns=10, edits=3, patch=500, pos_lo=22_500),
    }
    for n, kw in S.items(): table(n, kw)
