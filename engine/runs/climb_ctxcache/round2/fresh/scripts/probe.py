# Are Bailian hash_ids chained (prefix-dependent) or per-block content hashes?
import json, sys, collections
for fn in sys.argv[1:]:
    pred = {}; multi_pred = set(); pos = {}; multi_pos = set(); n = 0; types = collections.Counter()
    for line in open(fn):
        r = json.loads(line); h = r["hash_ids"]; n += 1; types[r["type"]] += 1
        for i, b in enumerate(h):
            p = h[i-1] if i else None
            if b in pred and pred[b] != p: multi_pred.add(b)
            pred.setdefault(b, p)
            if b in pos and pos[b] != i: multi_pos.add(b)
            pos.setdefault(b, i)
    print(fn, n, dict(types), "ids", len(pred), "ids w/ >1 predecessor", len(multi_pred), "ids at >1 position", len(multi_pos))
