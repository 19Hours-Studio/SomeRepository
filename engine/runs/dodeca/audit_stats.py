"""Blind evidence review of the dodecahedron explanations (14-dodecahedron.md): engine (E) vs earlier (K).
Run from the repo root: python3 engine/runs/dodeca/audit_stats.py [audit_k=<agent transcript> ...]
Each audit_k=transcript pair first saves that transcript's REVIEW section to audit_k/REVIEW.md."""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..")); import ce  # noqa: E402
ideas = {i["id"]: i for i in json.load(open(os.path.join(HERE, "ideas.json")))}
for arg in sys.argv[1:]:
    d, tr = arg.split("=", 1); t = ce.transcript_text(tr); t = t[t.find("=== REVIEW ==="):]
    open(os.path.join(HERE, d, "REVIEW.md"), "w").write(t)
rows = {}
for d in sorted(x for x in os.listdir(HERE) if x.startswith("audit_") and os.path.isdir(os.path.join(HERE, x))):
    f = os.path.join(HERE, d, "REVIEW.md")
    if not os.path.exists(f): continue
    ids = json.load(open(os.path.join(HERE, d, "ids.json"))); text = open(f).read()
    blocks = re.split(r"^IDEA (\d+)\s*:", text, flags=re.M)[1:]
    for k, body in zip(blocks[0::2], blocks[1::2]):
        sev = re.findall(r"^DEFECT \| (FATAL|MAJOR|MINOR)", body, flags=re.M)
        fit = re.search(r"^FIT \| (\d+)\s*of\s*(\d+)", body, flags=re.M)
        rows[ids[int(k) - 1]] = {**{s: sev.count(s) for s in ("FATAL", "MAJOR", "MINOR")},
                                 "fit": (int(fit.group(1)), int(fit.group(2))) if fit else None}
key = lambda i: (rows[i]["FATAL"], rows[i]["MAJOR"], -(rows[i]["fit"][0] / rows[i]["fit"][1] if rows[i]["fit"] else 0))
print(f"{'rank':4s} {'id':10s} {'arm':3s} F/M/m   FIT     name")
for r, i in enumerate(sorted(rows, key=key), 1):
    c = rows[i]; f = f"{c['fit'][0]}/{c['fit'][1]}" if c["fit"] else "-"
    print(f"{r:4d} {i:10s} {ideas[i]['arm']:3s} {c['FATAL']}/{c['MAJOR']}/{c['MINOR']}  {f:7s} {ideas[i]['name'][:45]}")
for arm in ("E", "K"):
    L = [rows[i] for i in rows if ideas[i]["arm"] == arm]
    if L: print(f"arm {arm}: n={len(L)} FATAL {sum(c['FATAL'] for c in L)/len(L):.2f} MAJOR {sum(c['MAJOR'] for c in L)/len(L):.2f}"
                f" zero-FATAL {sum(c['FATAL'] == 0 for c in L)}/{len(L)}")
json.dump(rows, open(os.path.join(HERE, "audit_counts.json"), "w"), indent=1)
