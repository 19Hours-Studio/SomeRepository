# sim4 section-4 RAG model, plus baselines the answer omits: docs placed AFTER the history (per-turn retrieval at the
# tail, a common multi-turn RAG layout), and first-seen with a union cap (the compaction the answer recommends).
import random
W, Rd, O = 1.25, 0.10, 5.0
def rag(order, turns=30, k=10, size=800, pool=60, drift=0.3, sys=2000, q=200, out=300, seed=0, cap=None):
    rng = random.Random(seed); rel = {d: rng.random() for d in range(pool)}; prev = []; c = 0.0; seen = []; hist = []
    for t in range(turns):
        for d in rel: rel[d] = (1 - drift) * rel[d] + drift * rng.random()
        top = sorted(rel, key=rel.get, reverse=True)[:k]
        if order == "first":
            for d in top:
                if d not in seen: seen.append(d)
            if cap and len(seen) > cap:          # compaction: keep only the current top-k, in first-seen order
                seen = [d for d in seen if d in top]
            blocks = [("sys", sys)] + [(("doc", d), size) for d in seen] + [("rank", 5 * k)] + hist + [(("q", t), q)]
        elif order == "relevance":
            blocks = [("sys", sys)] + [(("doc", d), size) for d in top] + hist + [(("q", t), q)]
        elif order == "tail":                    # history first, this turn's docs at the tail, dropped next turn
            blocks = [("sys", sys)] + hist + [(("doc", d, t), size) for d in top] + [(("q", t), q)]
        elif order == "tail_new":                # docs kept in history; only docs not already in context are added
            new = [d for d in top if d not in seen]; seen += new
            blocks = [("sys", sys)] + hist + [(("doc", d), size) for d in new] + [("rank", 5 * k), (("q", t), q)]
        hit = 0
        for a, b in zip(blocks, prev):
            if a != b: break
            hit += a[1]
        L = sum(b for _, b in blocks); c += Rd * hit + W * (L - hit) + O * out; prev = blocks
        if order == "tail_new": hist = blocks[1:] + [(("a", t), out)]
        else: hist = hist + [(("turn", t), q + out)]
    return c, L
for drift in (0.1, 0.3):
    r = {o: rag(o, drift=drift) for o in ("relevance", "first", "tail", "tail_new")}
    r["first_cap20"] = rag("first", drift=drift, cap=20)
    b = r["relevance"][0]
    print(f"drift {drift}: " + "  ".join(f"{o} {v[0]:,.0f} ({v[0]/b-1:+.1%}, final ctx {v[1]:,})" for o, v in r.items()))
    print(f"   first-seen vs tail: {r['first'][0]/r['tail'][0]-1:+.1%}")
