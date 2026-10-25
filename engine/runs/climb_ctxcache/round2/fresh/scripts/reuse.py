# Infinite-cache upper bounds on real Bailian traffic: how many input blocks are prefix hits,
# and how many more are content seen before but sitting after the first differing block.
import json, sys, collections
def run(fn, minrun):
    seen_pref = set(); seen_blk = set()
    tot = pre = nonpre = nonpre_run = 0; by_type = collections.defaultdict(lambda: [0, 0, 0, 0])
    for line in open(fn):
        r = json.loads(line); h = r["hash_ids"]; n = len(h)
        k = 0; key = 0; i = 0
        while i < n:
            key = hash((key, h[i]))
            if key not in seen_pref: break
            i += 1
        p = i
        # re-insert all prefix keys
        key = 0
        for b in h:
            key = hash((key, b)); seen_pref.add(key)
        rest = h[p:]
        flags = [b in seen_blk for b in rest]
        np_ = sum(flags)
        # count only reused runs of length >= minrun
        nr = 0; c = 0
        for f in flags + [False]:
            if f: c += 1
            else:
                if c >= minrun: nr += c
                c = 0
        seen_blk.update(h)
        tot += n; pre += p; nonpre += np_; nonpre_run += nr
        t = by_type[r["type"]]; t[0] += n; t[1] += p; t[2] += np_; t[3] += nr
    print(f"{fn.split('/')[-1]}: blocks {tot}  prefix-hit {pre/tot:.1%}  non-prefix seen-before {nonpre/tot:.1%}  (in runs>={minrun}: {nonpre_run/tot:.1%})")
    for ty, t in sorted(by_type.items()):
        print(f"   {ty:9s} share {t[0]/tot:5.1%}  prefix {t[1]/t[0]:.1%}  nonprefix {t[2]/t[0]:.1%}  runs {t[3]/t[0]:.1%}")
for fn in sys.argv[1:]: run(fn, 4)
