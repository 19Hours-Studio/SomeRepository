# Idea 2: exact-prefix document-token reuse for top-k RAG sets under different canonical orders.
# Same setup as eval_g0/c1/gate.py (FACT 5): 100k-chunk corpus, top-5 drawn Zipf(a), 20k queries,
# unbounded prefix tree. Adds: popularity-descending order (global rank, as a frequency counter
# would learn it) and a bounded LRU tree (capacity in chunks-of-KV).
import hashlib, collections, numpy as np
M, K, Q = 100_000, 5, 20_000

def draw(rng, a):
    s = set()
    while len(s) < K:
        x = rng.zipf(a) - 1
        if x < M: s.add(int(x))
    return s

def run(a, order, cap=None, seed=0):
    rng = np.random.default_rng(seed)
    tree = collections.OrderedDict(); hit = 0
    freq = collections.Counter()
    for _ in range(Q):
        s = draw(rng, a)
        if order == 'hash':
            o = sorted(s, key=lambda c: hashlib.md5(str(c).encode()).hexdigest())
        elif order == 'pop_oracle':           # true global rank (Zipf rank = id)
            o = sorted(s)
        elif order == 'random':               # relevance order ~ arbitrary w.r.t. cache
            o = list(s); rng.shuffle(o)
        elif order == 'greedy':               # CacheWeaver-like: follow existing trie path,
            rest = sorted(s, key=lambda c: (-freq[c], c)); o = []; pre = ()   # else popularity
            while rest:
                nxt = next((c for c in rest if pre + (c,) in tree), rest[0])
                o.append(nxt); rest.remove(nxt); pre += (nxt,)
        else:                                  # online learned popularity, ties by id
            o = sorted(s, key=lambda c: (-freq[c], c))
        pre = (); miss = False; h = 0
        for c in o:
            pre += (c,)
            if not miss and pre in tree:
                h += 1; tree.move_to_end(pre)
            else:
                miss = True; tree[pre] = 1
                if cap and len(tree) > cap: tree.popitem(last=False)
        for c in s: freq[c] += 1
        hit += h / K
    return hit / Q

if __name__ == '__main__':
    for a in (1.05, 1.2, 1.5):
        r = {o: run(a, o) for o in ('random', 'hash', 'pop_learned', 'pop_oracle', 'greedy')}
        rc = run(a, 'pop_learned', cap=20_000)
        print('zipf %.2f ' % a + ' '.join('%s %.3f' % kv for kv in r.items()) + '  pop_learned@LRU20k %.3f' % rc)
        # Archetype C chain (eval_g0/c1): prefill 55% of cost; per request system 1k (cached),
        # docs 4k, question 0.2k. Prefill tokens = docs*(1-reuse)+question.
        pf = lambda u: (4 * (1 - u) + 0.2) / (4 * (1 - r['random']) + 0.2)
        for o in ('hash', 'pop_learned', 'greedy'):
            print('   %-12s prefill vs relevance-order prefix cache %.3f -> bill ratio %.2fx'
                  % (o, pf(r[o]), 1 / (0.45 + 0.55 * pf(r[o]))))
