"""Merge spec8b.py shard outputs: python3 -I merge8b.py OUT_JSON SHARD_JSON..."""
import json, sys
dst, srcs = sys.argv[1], sys.argv[2:]
res = None
for f in srcs:
    d = json.load(open(f))
    if res is None: res = d; continue
    for k, steps in d.items():
        for a, b in zip(res[k], steps):
            assert a["out"] == b["out"]; a.update(b)
json.dump(res, open(dst, "w"))
print(sorted(k for k in next(iter(res.values()))[0] if k != "out"))
