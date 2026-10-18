"""v3.2 (10-genius-engine.md): blind-audit defects of the evolved children vs their parents (audit_final).
Run from the repo root: python3 engine/runs/permafrost/genius/evo_stats.py [<audit_evo_1 transcript> <audit_evo_2 transcript>]
With transcripts, the REVIEW sections are saved to audit_evo_k/REVIEW.md first."""
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

for j, tr in enumerate(sys.argv[1:3], 1):
    t = ce.transcript_text(tr); t = t[t.find("=== REVIEW ==="):]
    open(os.path.join(HERE, f"audit_evo_{j}", "REVIEW.md"), "w").write(t)
par = counts("audit_final"); kids = {**counts("audit_evo_1"), **counts("audit_evo_2")}
for name, g in (("parents (audit_final)", par), ("children (v3.2)", kids)):
    n = len(g) or 1
    print(f"{name:22s} n={len(g)}  FATAL {sum(c['FATAL'] for c in g.values())/n:.2f}  MAJOR {sum(c['MAJOR'] for c in g.values())/n:.2f}"
          f"  MINOR {sum(c['MINOR'] for c in g.values())/n:.2f}  zero-FATAL {sum(c['FATAL'] == 0 for c in g.values())}/{len(g)}")
print("\nper idea (FATAL/MAJOR/MINOR):")
for i, c in sorted({**par, **kids}.items()):
    print(f"  {i:12s} {c['FATAL']}/{c['MAJOR']}/{c['MINOR']}  {ideas.get(i, {}).get('name', '?')[:60]}")
json.dump({"parents": par, "children": kids}, open(os.path.join(HERE, "evo_counts.json"), "w"), indent=1)
