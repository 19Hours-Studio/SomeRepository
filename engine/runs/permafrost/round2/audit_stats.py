"""Count the blind auditors' remaining defects per arm (ERP = round-1 repair, ERP2 = new rules, ERPR = red-team + new rules).
Run: python3 audit_stats.py <audit_a transcript> <audit_b transcript>"""
import json, os, re, sys
from collections import defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..")); import ce  # noqa: E402

ARM = {"repair": "ERP", "erp2": "ERP2", "rt": "ERPR"}
per_arm = defaultdict(lambda: defaultdict(int)); per_idea = {}
for g, tr in zip("ab", sys.argv[1:3]):
    ids = json.load(open(os.path.join(HERE, f"audit_{g}", "ids.json")))
    text = ce.transcript_text(tr); text = text[text.find("=== REVIEW ==="):]
    open(os.path.join(HERE, f"audit_{g}", "REVIEW.md"), "w").write(text)
    blocks = re.split(r"^IDEA (\d+):", text, flags=re.M)[1:]
    for k, body in zip(blocks[0::2], blocks[1::2]):
        iid = ids[int(k) - 1]; arm = ARM[iid.split("_")[0]]
        sev = re.findall(r"^DEFECT \| (FATAL|MAJOR|MINOR)", body, flags=re.M)
        c = {s: sev.count(s) for s in ("FATAL", "MAJOR", "MINOR")}
        per_idea[iid] = c
        for s, n in c.items(): per_arm[arm][s] += n
        per_arm[arm]["n"] += 1
print(f"{'arm':5s} {'n':>2s} {'FATAL':>6s} {'MAJOR':>6s} {'MINOR':>6s}  (per idea)")
for arm in ("ERP", "ERP2", "ERPR"):
    d = per_arm[arm]; n = d["n"] or 1
    print(f"{arm:5s} {d['n']:2d} {d['FATAL']/n:6.2f} {d['MAJOR']/n:6.2f} {d['MINOR']/n:6.2f}")
print("\nper idea (FATAL/MAJOR/MINOR):")
for base in sorted({i.split("#")[1] + i.split("_")[1][0] for i in per_idea}):
    k, g = base[0], base[1]
    row = [f"{a}:{per_idea.get(f'{p}_{g}#{k}', {}).get('FATAL','-')}/{per_idea.get(f'{p}_{g}#{k}', {}).get('MAJOR','-')}/{per_idea.get(f'{p}_{g}#{k}', {}).get('MINOR','-')}"
           for p, a in ARM.items()]
    print(f"  {g}#{k}: " + "  ".join(row))
json.dump(per_idea, open(os.path.join(HERE, "audit_counts.json"), "w"), indent=1)
