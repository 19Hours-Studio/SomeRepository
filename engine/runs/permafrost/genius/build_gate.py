"""Build the v3.0 kill-test blocks and the O/G judge set for the genius experiment (10-genius-engine.md).
Run from the repo root after the six v3.0 generators are ingested: python3 engine/runs/permafrost/genius/build_gate.py"""
import json, os, secrets, subprocess
R = "permafrost"; RD = os.path.join("engine", "runs", R); G = os.path.join(RD, "genius")
ideas = json.load(open(os.path.join(RD, "ideas.json")))
new = [i["id"] for i in ideas if i["label"].startswith("gx_")]
g1 = [i["id"] for i in ideas if i["label"].startswith("g1_")]
ec = [i["id"] for i in ideas if i["arm"] == "EC"]
calib = ["erp2_b#4", "erp2_a#1", "erp2_b#2", "erp2_a#3"]
pool = new + g1 + ec + calib
rnd = secrets.SystemRandom(); rnd.shuffle(pool)
k = 9; blocks = [pool[j::k] for j in range(k)]
for j, b in enumerate(blocks, 1):
    subprocess.run(["python3", "engine/ce.py", "gatetask", R, "--ids", ",".join(b), "--dir", os.path.join(G, f"gate_{j}")], check=True)
ctrl = [i["id"] for i in ideas if i["arm"] == "control"]; rnd.shuffle(ctrl)
judge = new + g1 + ec + ctrl[:12]
subprocess.run(["python3", "engine/ce.py", "set", R, "s99s", "--ids", ",".join(judge), "--prefix", "Q", "--crux", "--genius",
                "--basin-sources", "observed,predicted"], check=True)
json.dump({"new": new, "g1": g1, "ec": ec, "calib": calib, "ctrl12": ctrl[:12], "blocks": blocks},
          open(os.path.join(G, "pools.json"), "w"), indent=1)
print(f"pool {len(pool)} ideas in {k} blocks; judge set {len(judge)} ideas")
