# critic3 checks on the real traces. Usage: python3 -I check3.py <trajs_dir> <round3_code_dir>
import sys, glob, random, re, statistics as st
sys.path.insert(0, sys.argv[2]); import trace4 as T
F = sorted(glob.glob(sys.argv[1] + "/*.json")); TR = [T.load(f) for f in F]
base = sum(T.cost(t) for t, _ in TR)

# 1. back-references: only runs of >= k consecutive re-shown lines count (a real re-show, not a generic line)
def dup_runs(steps, kmin):
    shown = set(); saved = {}; dt = nt = 0
    for j, s in enumerate(steps):
        lines = s["obs"].split("\n"); toks = [len(l) / 3.6 + 0.5 for l in lines]; nt += sum(toks)
        flags = [len(l.strip()) >= 20 and l in shown for l in lines]; net = 0; i = 0
        while i < len(lines):
            if flags[i]:
                k = i
                while k < len(lines) and flags[k]: k += 1
                if k - i >= kmin: d = sum(toks[i:k]); dt += d; net += max(0, d - 12)
                i = k
            else: i += 1
        for l in lines:
            if len(l.strip()) >= 20: shown.add(l)
        if net > 0 and j + 1 < len(steps): saved[j + 1] = int(net)
    return saved, dt, nt
print("== 1. back-references, by minimum run length ==")
for kmin in (1, 3, 5):
    c = 0; D = N = 0
    for t, _ in TR:
        sv, d, n = dup_runs(t, kmin); D += d; N += n; c += T.cost(t, saved_tok=sv)
    print(f"runs >= {kmin} lines: dup share {D/N:.1%}, cost {c/base-1:+.1%}")

# 2. batching: also drop part of the merged-away request's output (one reasoning pass fewer)
print("\n== 2. batching (STRICT cap 4, any non-write) with output of merged requests reduced ==")
drops = [T.groups(t, task, 4, False, True) for t, task in TR]
for keep in (1.0, 0.75, 0.5):
    c = 0
    for (t, _), d in zip(TR, drops):
        t2 = [dict(s, out=s["out"] * keep) if j in d else s for j, s in enumerate(t)]
        c += T.cost(t2, d)
    print(f"merged requests keep {keep:.0%} of output: {c/base-1:+.1%}")
c = 0
for (t, _), d in zip(TR, drops):
    sv, _, _ = T.dup_lines(t); c += T.cost(t, d, sv)
print(f"combined (author) {c/base-1:+.1%}; precision-scaled 0.77-0.90 of batching part:"
      f" {0.77*-0.087-0.037:+.1%} .. {0.90*-0.087-0.037:+.1%}")

# 3. sample strict merges for a hand check
print("\n== 3. random strict merges (seed 3) ==")
rng = random.Random(3); pool = [(i, j) for i, d in enumerate(drops) for j in d]
for i, j in rng.sample(pool, 20):
    t = TR[i][0]; p, s = t[j - 1], t[j]
    o = re.sub(r"\s+", " ", p["obs"])[:260]
    print(f"--- {F[i].split('/')[-1]} step {j}\n PREV: {p['cmd'][:200]}\n OBS : {o}\n NEXT: {s['cmd'][:200]}")
