"""Replay Mooncake FAST25 traces: exact-prefix block reuse vs position-independent block reuse.
Usage: python3 -I replay_mooncake.py <trace.jsonl> [...]
Blocks are 512 tokens. Infinite cache (upper bound) and LRU with a block capacity."""
import json, sys
from collections import OrderedDict, defaultdict

BLK = 512

def load(p):
    with open(p) as f:
        return [json.loads(l) for l in f if l.strip()]

def replay(reqs, cap=None):
    seen = OrderedDict()
    tot = pre = anyp = 0
    for r in reqs:
        h = r["hash_ids"]; n = r["input_length"]
        sizes = [BLK] * (len(h) - 1) + [n - BLK * (len(h) - 1)]
        tot += n
        prefix_ok = True
        for b, s in zip(h, sizes):
            hit = b in seen
            if hit:
                anyp += s
                seen.move_to_end(b)
            if prefix_ok and hit:
                pre += s
            else:
                prefix_ok = False
            if not hit:
                seen[b] = 1
                if cap and len(seen) > cap:
                    seen.popitem(last=False)
    return tot, pre / tot, anyp / tot

def structure(reqs):
    pos = defaultdict(set); pred = defaultdict(set)
    for r in reqs:
        h = r["hash_ids"]
        for i, b in enumerate(h):
            pos[b].add(i); pred[b].add(h[i - 1] if i else None)
    multi_pos = sum(1 for b in pos if len(pos[b]) > 1)
    multi_pred = sum(1 for b in pred if len(pred[b]) > 1)
    return len(pos), multi_pos, multi_pred

for p in sys.argv[1:]:
    reqs = load(p)
    nb, mp, mpr = structure(reqs)
    print(f"== {p.split('/')[-1]}: {len(reqs)} reqs, {nb} distinct blocks, "
          f"blocks seen at >1 position: {mp}, with >1 predecessor: {mpr}")
    for cap in (None, 100000, 20000, 5000):
        tot, a, b = replay(reqs, cap)
        print(f"  cap={cap}: prefix-hit {a:.4f}  any-position hit {b:.4f}  "
              f"extra {b - a:+.4f}  miss prefix {1-a:.4f} vs PIC {1-b:.4f}")
