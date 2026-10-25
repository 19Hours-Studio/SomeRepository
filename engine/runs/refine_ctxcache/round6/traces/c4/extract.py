"""Reduce SWE-agent 1.x .traj files to per-step message lists (role, chars) -> compact json."""
import json, sys, os, glob
src, dst = sys.argv[1], sys.argv[2]
out = {}
def text(m):
    c = m.get('content')
    s = c if isinstance(c, str) else ''.join(x.get('text', '') for x in c) if isinstance(c, list) else ''
    if m.get('tool_calls'): s += json.dumps(m['tool_calls'], sort_keys=True)
    return s
for f in sorted(glob.glob(os.path.join(src, '*.traj'))):
    d = json.load(open(f))
    steps = []
    for st in d['trajectory']:
        q = [(m.get('role', 'none'), text(m)) for m in st['query']]
        steps.append({'q': q, 'resp': len(st.get('response') or '')})
    # store as message hashes + sizes to keep it small but exact for LCP tests
    import hashlib
    out[os.path.basename(f)[:-5]] = [{'m': [(r, len(t), hashlib.sha1((r + t).encode()).hexdigest()[:12]) for r, t in s['q']], 'resp': s['resp']} for s in steps]
json.dump(out, open(dst, 'w'))
print(len(out), 'trajectories')
