# C3-style delta views (runs >=3 known lines, same path, constant offset, vs ANY earlier view) on C4's 200 Sonnet-4 traces
import json, re, sys
sys.path.insert(0, sys.argv[2]); import traces as TR
HDR = re.compile(r"Here's the result of running `cat -n` on (?:a snippet of )?(\S+?):\r?\n")
LN = re.compile(r"^\s*(\d+)\t(.*)$")
T = TR.load(sys.argv[1]); base = new = 0; tokb = tokn = 0
for tr in T:
    text = list(tr["text"]); seen = {}   # path -> {lineno: hash}, and hash->linenos
    for i, s in enumerate(text):
        if not TR.is_obs(tr, i): continue
        m = HDR.search(s)
        if not m: continue
        p = m.group(1); lines = s[m.end():].splitlines(); L = []
        for x in lines:
            g = LN.match(x)
            if g: L.append((int(g.group(1)), hash(g.group(2)), len(x) + 1))
        prev = seen.setdefault(p, [])
        cov = [False] * len(L); runs = 0; q = 0
        while q < len(L):
            best = 0
            for byln, byh in prev:
                for n0 in byh.get(L[q][1], ()):
                    off = L[q][0] - n0; r = 0
                    while q + r < len(L) and byln.get(L[q + r][0] - off) == L[q + r][1]: r += 1
                    best = max(best, r)
            if best >= 3:
                for z in range(q, q + best): cov[z] = True
                runs += 1; q += best
            else: q += 1
        saved = sum(L[z][2] for z in range(len(L)) if cov[z])
        byln = {a: b for a, b, _ in L}; byh = {}
        for a, b, _ in L: byh.setdefault(b, []).append(a)
        prev.append((byln, byh))
        if saved: text[i] = "x" * max(0, len(s) - saved + int(runs * 12 * 3.5))  # 12-token back-ref per run
    for W, R in [(1.25, 0.1)]:
        n0 = [TR.tok(s) for s in tr["text"]]; n1 = [TR.tok(s) for s in text]
        base += TR.bill(TR.policy_seq(tr, n0, "append", W, R), W, R)[0]
        new += TR.bill(TR.policy_seq({"role": tr["role"], "text": text}, n1, "append", W, R), W, R)[0]
        tokb += sum(n0); tokn += sum(n1)
print(f"append-only cost {base:,.0f} -> delta(C3-style) {new:,.0f}: {new/base-1:+.1%}; message tokens {tokn/tokb-1:+.1%}")
