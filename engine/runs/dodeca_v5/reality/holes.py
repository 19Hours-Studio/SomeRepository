"""Per-object hole-diameter tests for Roman dodecahedra.

Data (mm), opposite pairs as published:
  S = Sparavigna 2012 table (arxiv 1204.6497 / 1206.0946; object attributed
      variously to Jublains / Avenches; same numbers as the "Newhall"/Gellep
      descriptions: ten 10.5-22 mm, two ovals ~26x21.5). Ovals entered as major axis.
  T = Tongeren (wingarden.de/wing/dodekaeder.html), six opposite pairs.

Test 1 (lot idea): how many faces are distinguishable by eye, given a Weber
  fraction w for diameter discrimination. Faces are merged when neighbouring
  sorted sizes differ by < w * size.
Test 2 (free variation vs paired design): are opposite holes more alike than a
  random pairing of the same 12 values? Statistic = sum |a-b| over the 6
  opposite pairs; exact null over all 10395 perfect matchings.
"""
import itertools, random

S = [(25.5, 26.0), (10.5, 17.0), (15.5, 11.5), (17.0, 16.5), (22.0, 21.0), (22.0, 21.5)]
S_mean_oval = [(23.5, 23.75)] + S[1:]
T = [(10.6, 13.0), (13.8, 14.0), (25.2, 27.0), (23.0, 26.3), (15.6, 17.8), (20.3, 20.5)]


def classes(sizes, w):
    s = sorted(sizes)
    n = 1
    for a, b in zip(s, s[1:]):
        if b - a >= w * a:
            n += 1
    return n


def matchings(items):
    if not items:
        yield []
        return
    a = items[0]
    for i in range(1, len(items)):
        rest = items[1:i] + items[i + 1:]
        for m in matchings(rest):
            yield [(a, items[i])] + m


def stat(pairs):
    return sum(abs(a - b) for a, b in pairs)


def pair_test(pairs):
    vals = [v for p in pairs for v in p]
    obs = stat(pairs)
    null = [stat(m) for m in matchings(vals)]
    p = sum(x <= obs + 1e-9 for x in null) / len(null)
    return obs, sum(null) / len(null), p, len(null)


def validate():
    # Test 1: synthetic object with sizes spaced by a known 8% -> 12 classes at w<=8%, merges above
    syn = [10 * 1.08 ** k for k in range(12)]
    assert classes(syn, 0.05) == 12 and classes(syn, 0.10) == 1
    assert classes([20.0] * 12, 0.03) == 1
    # Test 2: null calibration - random objects with random pairing, alpha=0.05
    rng = random.Random(1)
    rej = 0
    N = 300
    for _ in range(N):
        v = [rng.uniform(8, 30) for _ in range(12)]
        rej += pair_test(list(zip(v[::2], v[1::2])))[2] <= 0.05
    # power: designed pairs (axis size + N(0,1 mm) jitter)
    hit = 0
    for _ in range(N // 3):
        ax = [rng.uniform(8, 30) for _ in range(6)]
        hit += pair_test([(a + rng.gauss(0, 1), a + rng.gauss(0, 1)) for a in ax])[2] <= 0.05
    return rej / N, hit / (N // 3)


if __name__ == "__main__":
    fa, pw = validate()
    print(f"VALIDATION test1 synthetic OK; test2 null false-positive rate {fa:.3f} (alpha .05), power on paired design {pw:.2f}")
    for name, obj in [("S (ovals major axis)", S), ("S (ovals mean axis)", S_mean_oval), ("Tongeren", T)]:
        vals = [v for p in obj for v in p]
        cl = {w: classes(vals, w) for w in (0.02, 0.03, 0.05, 0.08, 0.10)}
        obs, mu, p, n = pair_test(obj)
        print(f"{name}: sizes {sorted(vals)}")
        print(f"  distinguishable classes by Weber fraction {cl}")
        print(f"  opposite-pair |diff| sum {obs:.1f} mm vs random-pairing mean {mu:.1f}; exact p={p:.4f} over {n} matchings")
        print(f"  per-pair diffs {[round(abs(a-b),1) for a,b in obj]}")
