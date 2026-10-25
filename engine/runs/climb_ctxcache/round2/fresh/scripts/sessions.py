# Parent -> child structure in Bailian traces: how much of what the session already sent is lost
# to a mid-prompt change, and how long the gaps between turns are.
import json, sys, collections
def lcp(a, b):
    n = min(len(a), len(b)); i = 0
    while i < n and a[i] == b[i]: i += 1
    return i
for fn in sys.argv[1:]:
    reqs = {}; tot = 0; child = 0; child_blocks = 0; resent = 0; lost = 0; nbroken = 0
    gaps = []; brk_pos = []; lost_w = []
    for line in open(fn):
        r = json.loads(line); h = r["hash_ids"]; tot += len(h)
        reqs[r["chat_id"]] = (r["timestamp"], h)
        p = r["parent_chat_id"]
        if p < 0 or p not in reqs: continue
        tp, hp = reqs[p]; child += 1; child_blocks += len(h)
        m = lcp(hp, h); full = len(hp) - 1          # last parent block may hold padding
        resent += min(full, len(h)); l = max(0, min(full, len(h)) - m); lost += l
        gaps.append((r["timestamp"] - tp, m * 16))
        if l > 0:
            nbroken += 1; brk_pos.append(m / max(1, full)); lost_w.append(l)
    gaps.sort()
    if not gaps: print(f"{fn.split('/')[-1]}: requests {len(reqs)}, no parent links"); continue
    def frac_after(s): return sum(w for g, w in gaps if g > s) / max(1, sum(w for g, w in gaps))
    brk_pos.sort()
    print(f"{fn.split('/')[-1]}: requests {len(reqs)} children {child} ({child_blocks/tot:.1%} of input blocks)")
    print(f"   parent blocks re-sent by child: {resent/tot:.1%} of all input; lost to a mid-prompt change: {lost/tot:.2%} of all input ({lost/max(1,resent):.1%} of re-sent); broken children {nbroken/max(1,child):.1%}")
    if brk_pos: print(f"   break position (fraction of parent): p10 {brk_pos[len(brk_pos)//10]:.2f} median {brk_pos[len(brk_pos)//2]:.2f} p90 {brk_pos[9*len(brk_pos)//10]:.2f}")
    print(f"   turn gap median {gaps[len(gaps)//2][0]:.0f}s p90 {gaps[9*len(gaps)//10][0]:.0f}s; reusable-prefix tokens arriving after 5 min {frac_after(300):.1%}, after 1 h {frac_after(3600):.1%}")
