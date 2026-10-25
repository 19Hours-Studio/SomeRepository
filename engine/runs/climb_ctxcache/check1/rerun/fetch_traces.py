# Fetch a fixed random sample of SWE-agent (Claude Sonnet 4, SWE-bench Verified) trajectories from the
# public swe-bench-submissions S3 bucket and keep only the message history (role, text length, text).
# Usage: python3 -I fetch_traces.py data/ids_all.txt data/traces.jsonl 80
import json, random, sys, urllib.request, concurrent.futures as cf
RUN = "20250522_sweagent_claude-4-sonnet-20250514"
BASE = f"https://swe-bench-submissions.s3.amazonaws.com/verified/{RUN}/trajs"
ids = [l.strip() for l in open(sys.argv[1]) if l.strip()]
n = int(sys.argv[3]); sample = sorted(random.Random(0).sample(ids, n))
def text(c):
    if isinstance(c, str): return c
    return "".join(p.get("text", "") for p in c if isinstance(p, dict))
def get(i):
    d = json.load(urllib.request.urlopen(f"{BASE}/{i}/{i}.traj", timeout=120))
    msgs = [{"role": m["role"], "text": text(m.get("content", "")),
             "tool": bool(m.get("tool_calls"))} for m in d["history"]]
    # keep assistant tool-call arguments: they are part of the prompt too
    for m, raw in zip(msgs, d["history"]):
        for tc in raw.get("tool_calls") or []:
            m["text"] += json.dumps(tc.get("function", tc))
    return {"id": i, "steps": len(d["trajectory"]), "msgs": msgs}
with cf.ThreadPoolExecutor(8) as ex, open(sys.argv[2], "w") as out:
    for r in ex.map(get, sample): out.write(json.dumps(r) + "\n")
