"""v3.2/v3.3 (10-genius-engine.md): blind-audit defects of the evolved children vs their parents (audit_final).
Run from the repo root: python3 engine/runs/permafrost/genius/evo_stats.py [<audit dir>=<agent transcript> ...]
Each audit dir=transcript pair first saves that transcript's REVIEW section to <audit dir>/REVIEW.md."""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..")); import ce  # noqa: E402
ideas = {i["id"]: i for i in json.load(open(os.path.join(HERE, "..", "ideas.json")))}

def counts(d):
    ids = json.load(open(os.path.join(HERE, d, "ids.json"))); text = open(os.path.join(HERE, d, "REVIEW.md")).read()
    blocks = re.split(r"^IDEA (\d+)\s*:", text, flags=re.M)[1:]
    out = {}
    for k, body in zip(blocks[0::2], blocks[1::2]):
        sev = re.findall(r"^DEFECT \| (FATAL|MAJOR|MINOR)", body, flags=re.M)
        out[ids[int(k) - 1]] = {s: sev.count(s) for s in ("FATAL", "MAJOR", "MINOR")}
    return out

for arg in sys.argv[1:]:
    d, tr = arg.split("=", 1); t = ce.transcript_text(tr); t = t[t.find("=== REVIEW ==="):]
    open(os.path.join(HERE, d, "REVIEW.md"), "w").write(t)
have = lambda d: os.path.exists(os.path.join(HERE, d, "REVIEW.md"))
groups = [("parents (audit_final)", ["audit_final"]), ("children v3.2 (evolve)", ["audit_evo_1", "audit_evo_2"]),
          ("children v3.3 (attempts)", ["audit_att_1", "audit_att_2"])]
res = {name: {k: v for d in ds if have(d) for k, v in counts(d).items()} for name, ds in groups}
for name, g in res.items():
    if not g: continue
    n = len(g) or 1
    print(f"{name:22s} n={len(g)}  FATAL {sum(c['FATAL'] for c in g.values())/n:.2f}  MAJOR {sum(c['MAJOR'] for c in g.values())/n:.2f}"
          f"  MINOR {sum(c['MINOR'] for c in g.values())/n:.2f}  zero-FATAL {sum(c['FATAL'] == 0 for c in g.values())}/{len(g)}")
print("\nper idea (FATAL/MAJOR/MINOR):")
for i, c in sorted(x for g in res.values() for x in g.items()):
    print(f"  {i:12s} {c['FATAL']}/{c['MAJOR']}/{c['MINOR']}  {ideas.get(i, {}).get('name', '?')[:60]}")
json.dump(res, open(os.path.join(HERE, "evo_counts.json"), "w"), indent=1)
