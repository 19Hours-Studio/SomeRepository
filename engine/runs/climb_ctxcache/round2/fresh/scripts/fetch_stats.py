# Fetch the recorded billing stats (litellm cost with real cache usage) for the 200 SWE-agent traces
# replayed in round1/fix, so the replay's billing model can be calibrated against real dollars.
import json, sys, urllib.request, concurrent.futures as cf
RUN = "20250522_sweagent_claude-4-sonnet-20250514"
BASE = f"https://swe-bench-submissions.s3.amazonaws.com/verified/{RUN}/trajs"
ids = [json.loads(l)["id"] for l in open(sys.argv[1])]
def get(i):
    d = json.load(urllib.request.urlopen(f"{BASE}/{i}/{i}.traj", timeout=180))
    t = d["trajectory"]
    return {"id": i, "stats": d["info"].get("model_stats"), "exec_s": [s.get("execution_time") for s in t],
            "hp": d["replay_config"] if isinstance(d["replay_config"], str) else json.dumps(d["replay_config"])}
with cf.ThreadPoolExecutor(8) as ex, open(sys.argv[2], "w") as out:
    for r in ex.map(get, ids):
        hp = json.loads(r.pop("hp"))["agent"]["history_processors"]; r["history_processors"] = hp
        out.write(json.dumps(r) + "\n")
