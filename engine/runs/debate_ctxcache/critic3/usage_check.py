# Is reasoning_tokens already inside completion_tokens? (trace4.load adds them -> possible double count)
import json, glob, sys, collections
n = gt = eq0 = 0; C = R = 0; keys = collections.Counter(); ex = None; costs = []; acts = collections.Counter()
for f in sorted(glob.glob(sys.argv[1] + "/*.json")):
    d = json.load(open(f))
    costs.append(d.get("info", {}).get("model_stats", {}).get("instance_cost"))
    for m in d["messages"]:
        if m["role"] != "assistant": continue
        u = m["extra"]["response"]["usage"]; keys.update(u.keys())
        c = u.get("completion_tokens") or 0; r = ((u.get("completion_tokens_details") or {}).get("reasoning_tokens") or 0)
        n += 1; C += c; R += r; gt += r > c; eq0 += r == 0
        acts[len(m["extra"].get("actions", []))] += 1
        if ex is None and r: ex = u
print("requests", n, "sum completion", C, "sum reasoning", R, "reasoning>completion in", gt, "reasoning==0 in", eq0)
print("usage keys", dict(keys)); print("example", json.dumps(ex)[:900]); print("actions per turn", dict(acts))
print("logged instance_cost total", sum(c for c in costs if c), "n", sum(1 for c in costs if c))
