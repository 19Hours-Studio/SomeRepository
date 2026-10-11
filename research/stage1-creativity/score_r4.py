"""Итоги раунда 4: два независимых Opus-судьи -> по плечам (EVO/CTRL/DIFF-ENF/якоря), бассейны, согласие судей."""
import json, re, collections
key = json.load(open("blind_key_r4.json"))
def load(f):
    out = {}
    for w, o, c, v, r, b, cl in re.findall(r"^(W\d\d) \| (\d+) \| (\d+) \| (\d+) \| ([YN]) \| ([A-Z]+) \| (.+)$", open(f).read(), re.M):
        out[key[w]] = dict(O=int(o), C=int(c), V=int(v), R=r, B=b, cl=cl.strip())
    return out
A, B = load("judge_r4_A.md"), load("judge_r4_B.md")
ids = sorted(set(A) & set(B)); assert len(ids) == len(key), (len(ids), len(key))
def rank(xs):
    s = sorted(range(len(xs)), key=lambda i: xs[i]); r = [0]*len(xs); i = 0
    while i < len(s):
        j = i
        while j + 1 < len(s) and xs[s[j+1]] == xs[s[i]]: j += 1
        for k in range(i, j+1): r[s[k]] = (i + j) / 2
        i = j + 1
    return r
def spearman(x, y):
    rx, ry = rank(x), rank(y); n = len(x); mx, my = sum(rx)/n, sum(ry)/n
    num = sum((a-mx)*(b-my) for a, b in zip(rx, ry)); den = (sum((a-mx)**2 for a in rx)*sum((b-my)**2 for b in ry))**.5
    return num/den
for m in "OCV": print(f"Spearman судей по {m}: {spearman([A[i][m] for i in ids], [B[i][m] for i in ids]):.2f}")
agreeB = sum(A[i]['B'] == B[i]['B'] for i in ids); agreeR = sum(A[i]['R'] == B[i]['R'] for i in ids)
print(f"совпадение BASIN: {agreeB}/{len(ids)}, R: {agreeR}/{len(ids)}")
arm = lambda i: "ANCHOR" if i.startswith("ANCHOR") else "EVO" if i.startswith("EVO") else "DIFF-ENF" if i.startswith("DIFF_T") else "CTRL"
by = collections.defaultdict(list)
for i in ids: by[arm(i)].append(i)
print(f"\n{'arm':9s} n   O     C     V    O*V  NEW-basin  R=Y   (среднее двух судей)")
summ = {}
for a in ["EVO", "CTRL", "DIFF-ENF", "ANCHOR"]:
    L = by[a]; n = len(L); m = lambda k: sum((A[i][k] + B[i][k]) / 2 for i in L) / n
    ov = sum(((A[i]['O']+B[i]['O'])/2) * ((A[i]['V']+B[i]['V'])/2) for i in L) / n
    new = sum((A[i]['B'] == 'NEW') + (B[i]['B'] == 'NEW') for i in L) / (2*n); ry = sum((A[i]['R'] == 'Y') + (B[i]['R'] == 'Y') for i in L) / (2*n)
    summ[a] = dict(n=n, O=round(m('O'),2), C=round(m('C'),2), V=round(m('V'),2), OV=round(ov,1), NEW=round(new,2), RY=round(ry,2))
    print(f"{a:9s} {n:2d} {m('O'):5.2f} {m('C'):5.2f} {m('V'):5.2f} {ov:5.1f}   {new:4.2f}     {ry:4.2f}")
j3 = {"ANCHOR:OPUS_BASE_b#1": (5,5), "ANCHOR:NEG#1": (4,5), "ANCHOR:CORE_a#3": (6,4), "ANCHOR:B1#1": (1,6), "ANCHOR:OPUS_MECH#2": (2,4), "ANCHOR:DIFF#1": (2,5)}
print("\nякоря: J3(O,V) -> A(O,V) / B(O,V)")
for i in sorted(j3): print(f"  {i:22s} {j3[i]} -> ({A[i]['O']},{A[i]['V']}) / ({B[i]['O']},{B[i]['V']})")
print("\nвсе идеи (среднее O, V; бассейны A/B; R A/B):")
rows = sorted(ids, key=lambda i: -(A[i]['O']+B[i]['O'])*(A[i]['V']+B[i]['V']))
for i in rows: print(f"  {i:22s} O{(A[i]['O']+B[i]['O'])/2:.1f} V{(A[i]['V']+B[i]['V'])/2:.1f} {A[i]['B']:>6s}/{B[i]['B']:<6s} R {A[i]['R']}/{B[i]['R']}  | {A[i]['cl'][:40]}")
json.dump(dict(summary=summ, A=A, B=B), open("judge_r4_summary.json", "w"), indent=1, ensure_ascii=False)
