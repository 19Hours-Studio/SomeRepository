# Non-prefix reuse across agent sessions: share of tool-output tokens whose text already appeared
# in an EARLIER trajectory (another SWE-bench instance, often the same repo). Content is matched in
# 8-line windows anchored at line starts, so the match does not depend on token offsets.
# Also the same within a trajectory (re-views of text already in context but at another position).
import json, sys, hashlib, collections
CH = 3.5
def tok(s): return len(s) / CH
seen_x = set(); tot = cross = within = 0.0; by_repo = collections.Counter(); tot_repo = collections.Counter()
for line in open(sys.argv[1]):
    t = json.loads(line); repo = t["id"].split("__")[0]; seen_w = set(); new_x = set()
    for m in t["msgs"]:
        if m["role"] not in ("tool", "user"): continue
        L = m["text"].split("\n")
        for i in range(0, len(L), 8):
            w = "\n".join(L[i:i + 8]); n = tok(w)
            if n < 20: continue
            h = hashlib.blake2b(w.encode(), digest_size=8).digest()
            tot += n; tot_repo[repo] += n
            if h in seen_w: within += n
            elif h in seen_x: cross += n; by_repo[repo] += n
            seen_w.add(h); new_x.add(h)
    seen_x |= new_x
print(f"tool/user-output tokens {tot/1e6:.1f}M: already seen in an earlier trajectory {cross/tot:.1%}; repeated within the same trajectory {within/tot:.1%}")
for r, v in sorted(tot_repo.items(), key=lambda x: -x[1])[:6]: print(f"   {r:14s} {v/tot:5.1%} of tokens, cross-trajectory repeats {by_repo[r]/v:.1%}")
