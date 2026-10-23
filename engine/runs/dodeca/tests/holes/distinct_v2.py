"""How many faces can be told apart by hole size alone, on the verified objects (data.py v2 + scans)?
Threshold: a size difference of about 5% is reliably seen when two objects are compared
(Eerkens & de Voogt 2022, Archaeol. Anthropol. Sci. 14:134, p. 1, citing Eerkens 2000 and Norwich 1983),
as used in ../h1_practice/distinct.py. levels = the largest set of holes pairwise >= 5% apart (exact search);
confusable = holes within 5% of another hole. Ringed holes only; the unringed pair adds at most one more
outcome class ('pole'), because its two holes are told apart from each other only by size.
Run: python distinct_v2.py > distinct_v2.txt
"""
import itertools
from data import OBJECTS


def d(v):
    return (v[0] + v[1]) / 2 if isinstance(v, tuple) else float(v)


def levels(x, th):
    x = sorted(x)
    for k in range(len(x), 0, -1):
        for c in itertools.combinations(x, k):
            if all(c[i + 1] / c[i] - 1 >= th for i in range(k - 1)):
                return k
    return 0


for th in (0.05, 0.10):
    print(f"--- threshold {th:.0%}")
    for name, o in OBJECTS.items():
        poles = o.get("poles")
        vals = [d(v) for k, v in (o["faces"].items() if "faces" in o else [])] if "faces" in o else \
            [v for p in o["pairs"] for v in p]
        ringed = [d(v) for k, v in o["faces"].items() if not poles or k not in poles] if "faces" in o and poles else None
        x = ringed if ringed else vals
        conf = sum(any(abs(a / b - 1) < th for j, b in enumerate(x) if j != i) for i, a in enumerate(x))
        tag = "10 ringed" if ringed else "all 12 (ring info unknown)"
        print(f"  {name}: {tag}: distinguishable levels {levels(x, th)}, confusable {conf} of {len(x)}"
              + (f"; + pole class -> at most {levels(x, th) + 1} readable outcomes of 12" if ringed else ""))
