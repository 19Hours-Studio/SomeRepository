"""H1 check: how many faces of a measured dodecahedron could be told apart by hole size alone?

Input: per-hole diameters already in engine/runs/dodeca/tests/holes/data.py (copied here, not re-measured).
Threshold: humans reliably see a size difference of about 5% or more when comparing two objects
(Eerkens & de Voogt 2022, Archaeol. Anthropol. Sci. 14:134, p. 1, citing Eerkens 2000 and Norwich 1983).
Outputs (derived, INFERENCE):
  confusable  = faces whose hole is within 5% of at least one other hole on the same object
  levels      = largest number of holes that are pairwise >=5% apart (greedy from the smallest), i.e. an
                upper bound on outcomes readable from hole size alone, ignoring rings and neighbour context.
"""
import itertools

OBJ = {
    # Jublains: ten ringed (Sparavigna 2012 table, FACT 31) + two oval unringed poles, mean of axes
    "Jublains (10 ringed + 2 poles, pole = mean axis)": [21.5, 16.5, 21.0, 11.5, 17.0, 10.5, 15.5, 22.0, 17.0, 22.0,
                                                          (26.0 + 21.5) / 2, (25.5 + 21.5) / 2],
    "Jublains (10 ringed only)": [21.5, 16.5, 21.0, 11.5, 17.0, 10.5, 15.5, 22.0, 17.0, 22.0],
    "Tongeren (12)": [10.6, 13.0, 13.8, 14.0, 25.2, 27.0, 23.0, 26.3, 15.6, 17.8, 20.3, 20.5],
    "Romford (9 of 12, mean of two axes)": [(22.31 + 22.46) / 2, (12.29 + 12.23) / 2, (15.92 + 16.11) / 2, 15.85,
                                            (18.75 + 18.77) / 2, (11.31 + 11.44) / 2, (18.95 + 19.03) / 2,
                                            (13.61 + 13.56) / 2, (16.04 + 15.99) / 2],
}

def close(a, b, thr):
    return abs(a - b) / min(a, b) < thr

for thr in (0.05, 0.10):
    print(f"--- threshold {thr:.0%}")
    for name, d in OBJ.items():
        conf = sum(1 for i, a in enumerate(d) if any(close(a, b, thr) for j, b in enumerate(d) if j != i))
        levels, last = 0, None
        for x in sorted(d):
            if last is None or (x - last) / last >= thr:
                levels += 1
                last = x
        pairs = [(a, b) for a, b in itertools.combinations(sorted(d), 2) if close(a, b, thr)]
        print(f"{name}: n={len(d)} confusable={conf} levels<={levels} close pairs={len(pairs)}")
