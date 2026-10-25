# Fetch a 1-in-8 sample (63) of SWE-agent + Claude-3.5-Sonnet trajectories on SWE-bench Verified from the public
# S3 bucket named in SWE-bench/experiments metadata.yaml, and reduce each to a compact message list:
# role, chars, is_demo, and for file views the (path, lineno, sha1(line)) triples, plus model_stats.
# Usage: python3 -I extract.py <download_dir>   -> writes traces.json next to this script.
import json, os, re, sys, hashlib, subprocess
dl = sys.argv[1]; os.makedirs(dl, exist_ok=True)
B = "https://swe-bench-submissions.s3.amazonaws.com"
P = "verified/20240620_sweagent_claude3.5sonnet/trajs/"
lst = os.path.join(dl, "list.xml")
if not os.path.exists(lst):
    subprocess.run(["curl", "-sS", "-o", lst, f"{B}/?list-type=2&prefix={P}&max-keys=1000"], check=True)
keys = re.findall(r"<Key>(.*?\.traj)</Key>", open(lst).read())[::8]
HDR = re.compile(r"^\[File: (.*?) \(\d+ lines total\)\]", re.M)
LN = re.compile(r"^(\d+):(.*)$")
out = []
for k in keys:
    f = os.path.join(dl, os.path.basename(k))
    if not os.path.exists(f):
        subprocess.run(["curl", "-sS", "--max-time", "60", "-o", f, f"{B}/{k}"], check=True)
    d = json.load(open(f)); msgs = []
    for m in d["history"]:
        c = m["content"]; e = {"role": m["role"], "chars": len(c), "demo": bool(m.get("is_demo"))}
        h = HDR.search(c)
        if m["role"] == "user" and h:
            e["path"] = h.group(1)
            e["lines"] = [[int(a), hashlib.sha1(b.encode()).hexdigest()[:12], len(b) + len(a) + 2]
                          for a, b in (LN.match(x).groups() for x in c.splitlines() if LN.match(x))]
        msgs.append(e)
    out.append({"id": os.path.basename(k)[:-5], "stats": d["info"]["model_stats"], "msgs": msgs})
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "traces.json"), "w"))
print(len(out), "traces")
