# Round-4 multi-turn RAG model (critic3 rag_check.py model, same parameters: 30 turns, top-10 of 60 docs x 800 tokens,
# relevance drift 0.1/0.3, system 2000, question 200, answer 300 at 5x). Prices: read 0.1, write 1.25, output 5.
# Layouts:
#  sysctx    : LangChain how-to layout - this turn's docs inside the system prompt, BEFORE chat_history (baseline)
#  tail      : history first, this turn's docs at the tail, dropped next turn (same visible information as sysctx)
#  tail_new  : docs stay in history; only docs not already in context are appended (union grows)
#  tail_cap C: tail_new, but when the union exceeds C docs, rebuild with only the current top-k (client compaction)
#  tail_span : tail_new + provider delete_span of docs that left the top-k (visible docs == this turn's top-k,
#              same set as sysctx; 32 boundary tokens recomputed per hole)
import random
W, Rd, O = 1.25, 0.10, 5.0
def rag(lay, turns=30, k=10, size=800, pool=60, drift=0.3, sys=2000, q=200, out=300, seed=0, cap=None, kb=32):
    rng = random.Random(seed); rel = {d: rng.random() for d in range(pool)}; prev = []; c = 0.0; hist = []; Ls = []
    for t in range(turns):
        for d in rel: rel[d] = (1 - drift) * rel[d] + drift * rng.random()
        top = sorted(rel, key=rel.get, reverse=True)[:k]; holes = 0
        if lay == "sysctx":
            blocks = [("sys", sys)] + [(("doc", d), size) for d in top] + hist + [(("q", t), q)]
        elif lay == "tail":
            blocks = [("sys", sys)] + hist + [(("doc", d, t), size) for d in top] + [(("q", t), q)]
        else:
            have = {b[0][1] for b in hist if b[0][0] == "doc"}
            if lay == "tail_cap" and len(have | set(top)) > cap:          # compaction: drop docs not in top-k
                hist = [b for b in hist if b[0][0] != "doc" or b[0][1] in top]; have = {b[0][1] for b in hist if b[0][0] == "doc"}
            if lay == "tail_span":
                gone = [b for b in hist if b[0][0] == "doc" and b[0][1] not in top]; holes = len(gone)
                hist = [b for b in hist if b not in gone]; have -= {b[0][1] for b in gone}
            new = [(("doc", d), size) for d in top if d not in have]
            blocks = [("sys", sys)] + hist + new + [(("rank", t), 5 * k), (("q", t), q)]
        if lay == "tail_span":
            pk = {b[0] for b in prev}; hit = max(0, sum(x for key, x in blocks if key in pk) - kb * holes)
        else:
            hit = 0
            for a, b in zip(blocks, prev):
                if a != b: break
                hit += a[1]
        L = sum(x for _, x in blocks); Ls.append(L); c += Rd * hit + W * (L - hit) + O * out; prev = blocks
        if lay in ("sysctx", "tail"): hist = hist + [(("turn", t), q + out)]
        else: hist = blocks[1:-2] + [(("turn", t), q + out)]            # docs + turns kept; rank list is transient
    return c, sum(Ls) / len(Ls)
for drift in (0.1, 0.3):
    r = {o: rag(o, drift=drift) for o in ("sysctx", "tail", "tail_new", "tail_span")}
    for C in (12, 15, 20, 30): r[f"tail_cap{C}"] = rag("tail_cap", drift=drift, cap=C)
    b = r["sysctx"][0]; t = r["tail"][0]
    print(f"drift {drift}:")
    for o, (c, L) in r.items():
        print(f"   {o:11s} {c:9,.0f}  vs sysctx {c/b-1:+6.1%}  vs tail {c/t-1:+6.1%}  mean ctx {L:7,.0f}")
    # output share of the baseline bill
    print(f"   output share of sysctx bill {30*300*5/b:.1%}, of tail_span bill {30*300*5/r['tail_span'][0]:.1%}")
