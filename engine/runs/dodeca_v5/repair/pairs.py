"""Independent recheck of the opposite-hole pairing test (written fresh, not reusing holes.py).

Statistic: sum over the six axes of |d_a - d_b|. Null: all perfect matchings of the
same holes (10,395 for 12 holes, 945 for 10). p = share of matchings with sum <= observed.
"""
import itertools

def matchings(items):
    if not items:
        yield []
        return
    a = items[0]
    for i in range(1, len(items)):
        b = items[i]
        rest = items[1:i] + items[i + 1:]
        for m in matchings(rest):
            yield [(a, b)] + m

def test(pairs, label):
    holes = [h for p in pairs for h in p]
    obs = sum(abs(a - b) for a, b in pairs)
    sums = [sum(abs(a - b) for a, b in m) for m in matchings(holes)]
    n = len(sums)
    p = sum(s <= obs + 1e-9 for s in sums) / n
    mean = sum(sums) / n
    print(f"{label:52s} obs={obs:5.1f} chance mean={mean:5.1f} n={n:6d} p={p:.4f}")
    return p

tongeren = [(10.6, 13.0), (13.8, 14.0), (25.2, 27.0), (23.0, 26.3), (15.6, 17.8), (20.3, 20.5)]
# Sparavigna 1204.6497, pairs as published: (1',1),(2',6),(3',5),(5',3),(4',4),(6',2)
spar_long = [(25.5, 26.0), (10.5, 17.0), (15.5, 11.5), (17.0, 16.5), (22.0, 21.0), (22.0, 21.5)]
spar_short = [(21.5, 21.5)] + spar_long[1:]

test(tongeren, "Tongeren, all 12")
test(spar_long, "Sparavigna, ovals by long axis")
test(spar_short, "Sparavigna, ovals by short axis")
# Type 2a's large opposite pair is already a known corpus feature; does the signal
# survive once that pair is removed?
test(spar_long[1:], "Sparavigna, 10 round holes only")
test(tongeren[:2] + tongeren[4:], "Tongeren minus the two largest pairs (8 holes)")
test([p for p in tongeren if p != (25.2, 27.0)], "Tongeren minus largest pair (10 holes)")
# Labelling-slip check: swap 6 and 5 partners
test([(25.5, 26.0), (10.5, 11.5), (15.5, 17.0), (17.0, 16.5), (22.0, 21.0), (22.0, 21.5)],
     "Sparavigna if 2'/3' partners swapped")

# Discrimination classes: greedy grouping of sorted sizes, new class when step > tol*size
def classes(sizes, tol):
    s = sorted(sizes)
    n, start = 1, s[0]
    for x in s[1:]:
        if x - start > tol * start:
            n += 1
            start = x
    return n

for name, pr in [("Tongeren", tongeren), ("Sparavigna(long)", spar_long)]:
    hs = [h for p in pr for h in p]
    print(name, {t: classes(hs, t) for t in (0.02, 0.05, 0.10)})
