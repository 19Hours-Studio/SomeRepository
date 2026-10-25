# Real re-view statistics from the 200 SWE-agent traces: when the agent views a file region it has
# already seen, how large is a line diff against the previous view, relative to the full re-view?
# This calibrates the "diff erratum" size e used in replay_v1.py. Usage: python3 -I diffstat.py data/traces.jsonl
import json, sys, re, difflib, statistics as st
VIEW = re.compile(r"Here's the result of running `cat -n` on (\S+?):\r?\n")
LN = re.compile(r"^\s*(\d+)\t")
ratios = []; full = []; same = 0; nre = 0; totobs = 0; edits = 0
for l in open(sys.argv[1]):
    t = json.loads(l); seen = {}
    for m in t["msgs"]:
        if m["role"] != "tool": continue
        totobs += 1
        if "has been edited" in m["text"]: edits += 1
        mm = VIEW.search(m["text"])
        if not mm: continue
        body = mm.string[mm.end():].splitlines()
        lines = {}
        for x in body:
            g = LN.match(x)
            if g: lines[int(g.group(1))] = x[g.end():]
        p = mm.group(1)
        if p in seen and lines:
            prev = seen[p]; ov = set(lines) & set(prev)
            if len(ov) >= 0.5 * len(lines):          # region largely seen before
                nre += 1
                a = [prev[k] for k in sorted(prev) if k in ov or True]
                d = [x for x in difflib.unified_diff([prev[k] for k in sorted(prev) if min(lines) <= k <= max(lines)],
                                                     [lines[k] for k in sorted(lines)], lineterm="", n=1)][2:]
                r = len("\n".join(d)) / max(1, len(m["text"]))
                if not d: same += 1
                ratios.append(min(r, 1.0)); full.append(len(m["text"]) / 3.5)
        seen.setdefault(p, {}).update(lines)
print(f"tool observations={totobs}  edit confirmations={edits}  re-views of a mostly-seen region={nre} ({nre/totobs:.1%} of observations)")
print(f"  identical to what is already in context: {same} ({same/nre:.1%})")
q = sorted(ratios)
print(f"  diff/full size ratio: median={st.median(q):.3f}  p75={q[int(.75*len(q))]:.3f}  mean={st.mean(q):.3f}")
print(f"  re-view size tokens: median={st.median(full):.0f}  mean={st.mean(full):.0f}")
print(f"  token-weighted saving if re-views were sent as diffs: {1-sum(r*f for r,f in zip(ratios,full))/sum(full):.1%} of re-view tokens")
