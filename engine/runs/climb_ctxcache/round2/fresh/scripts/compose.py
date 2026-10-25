# Composition of each trace's input tokens: re-sent parent prompt, parent's own output carried
# over, and genuinely new tokens (user turn, documents).
import json, sys
for fn in sys.argv[1:]:
    rq = {}; tot = 0; resent = 0; carried = 0; roots = 0
    for line in open(fn):
        r = json.loads(line); n = r["input_length"]; tot += n
        rq[r["chat_id"]] = (r["input_length"], r["output_length"])
        p = r["parent_chat_id"]
        if p in rq:
            pi, po = rq[p]; a = min(pi, n); resent += a; carried += min(po, max(0, n - a))
        else: roots += n
    print(f"{fn.split('/')[-1]:30s} input tokens {tot/1e6:6.1f}M  root requests {roots/tot:5.1%}  re-sent parent prompt {resent/tot:5.1%}  parent output carried {carried/tot:5.1%}  other new {(tot-roots-resent-carried)/tot:5.1%}")
