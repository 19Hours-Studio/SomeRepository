# Multi-turn RAG chat: the retrieved set changes and re-orders every turn.
# A  "rebuild": sys + chat history + this turn's docs (relevance order) + question   (common practice)
# B  "pin":     docs are appended to the conversation at first retrieval and later only referenced by id
# C  "pin+evict": B, plus docs not retrieved in the last m turns are masked to a stub in EOQ/ski-rental batches
import random, statistics as st, sys
sys.path.insert(0, ".")
from sim import Ctx, STUB, PRICES

def session(policy, seed, W, R, turns=50, k=5, doc=600, q=50, ans=300, p_reuse=0.6, m=5, sys_tok=2000):
    rng = random.Random(seed); c = Ctx(sys_tok); used = []; last_use = {}; seg_of = {}; nxt = 0
    acc = 0.0; H = T = C = 0
    for t in range(turns):
        ret = []
        while len(ret) < k:                      # topic locality: reuse a recently used doc with p_reuse
            if used and rng.random() < p_reuse:
                d = rng.choice(used[-15:])
            else:
                d = nxt; nxt += 1
            if d not in ret: ret.append(d)
        for d in ret: last_use[d] = t
        if policy == "rebuild":
            tail = [next(c._ids) for _ in ret]       # fresh segments every turn: never cached
            c.seg += [[i, doc, False, False] for i in tail]
        else:
            for d in ret:
                if d not in seg_of or c.seg[seg_of[d]][3]:   # not in context (or evicted): append it
                    c.add(doc, True); seg_of[d] = len(c.seg)-1
            if policy == "pin+evict":
                stale = [i for d, i in seg_of.items() if not c.seg[i][3] and t - last_use[d] >= m]
                if stale:
                    acc += R*sum(c.seg[i][1]-STUB for i in stale)
                    s0 = min(stale); ss = set(stale)
                    suffix = sum(STUB if i in ss else c.seg[i][1] for i in range(s0, len(c.seg)))
                    if acc >= (W-R)*suffix:
                        for i in stale:
                            c.seg[i][0] = next(c._ids); c.seg[i][1] = STUB; c.seg[i][3] = True
                        acc = 0.0
        c.add(q + (k*4 if policy != "rebuild" else 0), False)   # question (+ doc-id references)
        h, tot, cost = c.bill(W, R); H += h; T += tot; C += cost
        if policy == "rebuild":                   # drop this turn's docs from the history afterwards
            cut = [x[0] for x in c.seg].index(tail[0])
            c.seg = [x for x in c.seg if x[0] not in tail]
            c.prev = [x[0] for x in c.seg[:cut]]  # cached prefix = sys+history; the question sat after the docs
        c.add(ans, False)
        used += [d for d in ret if d not in used[-15:]]
    return H/T, C, T/turns

if __name__ == "__main__":
    for pr in ("anthropic", "openai"):
        W, R = PRICES[pr]
        for p in (0.3, 0.6, 0.8):
            res = {pol: [session(pol, s, W, R, p_reuse=p) for s in range(200)] for pol in ("rebuild", "pin", "pin+evict")}
            base = st.mean(x[1] for x in res["rebuild"])
            line = "  ".join(f"{pol}: hit={st.mean(x[0] for x in r):.3f} cost={st.mean(x[1] for x in r):>8,.0f} "
                             f"({1-st.mean(x[1] for x in r)/base:+.1%}) avg_sent={st.mean(x[2] for x in r):>6,.0f}"
                             for pol, r in res.items())
            print(f"{pr:9s} p_reuse={p}: {line}")
