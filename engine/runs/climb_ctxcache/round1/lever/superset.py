# Checks that the ski-rental batch mask never hides an observation that SWE-agent's shipped roll-5 policy showed:
# at every call, masked set S (batch, with and without delta) is a subset of the roll-5 masked set.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import replay as rp
orig = rp.run; bad = n = 0
for t in rp.T:
    m, calls, obs, roll, c = rp.prep(t)
    for d in (False, True):
        # re-run batch logic, recording S per call via a wrapped close()
        Ss = []
        def run_rec():
            S = frozenset(); rent = 0.0; prev = []
            full = {j: m[j]["chars"] / c for j in range(len(m))}
            dsz, refs = rp.delta_tokens(m, c, lambda k: set(range(k))) if d else ({}, {})
            size = lambda j: dsz.get(j, full[j])
            for i in calls:
                X = set(roll(i))
                while True:
                    keep = {r for k in range(i) if k not in X for r in refs.get(k, ())} & X
                    if not keep: break
                    X -= keep
                E = frozenset(X) - S
                if E:
                    cand = S | E; ids = [(j, j in cand) for j in range(i)]
                    p = next(q for q in range(len(ids)) if q >= len(prev) or ids[q] != prev[q])
                    buy = (1.25 - 0.10) * sum((rp.PH if mk else size(j)) for j, mk in ids[p:len(prev)])
                    rent += 0.10 * sum(size(j) - rp.PH for j in E)
                    if rent >= buy: S = cand; rent = 0.0
                prev = [(j, j in S) for j in range(i)]; Ss.append((S, roll(i)))
        run_rec()
        for S, Rl in Ss:
            n += 1; bad += not S <= Rl
print(f"calls checked={n}  calls where batch mask hid something roll-5 showed: {bad}")
