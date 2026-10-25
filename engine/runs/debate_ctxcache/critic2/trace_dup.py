# Fraction of observation text in a SWE-agent trajectory that re-displays lines already in context
# (line-number prefix stripped). Usage: python3 -I trace_dup.py <file.traj>   (n=1 public demo; illustrative)
import json, sys
t = json.load(open(sys.argv[1]))["trajectory"]; seen = set(); tot = dup = 0
for s in t:
    ls = [l.split(":", 1)[-1] for l in s["observation"].splitlines() if l.strip()]
    tot += sum(map(len, ls)); dup += sum(len(l) for l in ls if l in seen); seen |= set(ls)
print(f"steps={len(t)} obs_chars={tot} redisplayed={dup} frac={dup/tot:.3f}")
