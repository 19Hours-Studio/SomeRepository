"""Слепой набор раунда 4: EVO (9) + CTRL (3) + DIFF-ENF (2) + 6 якорей с известными оценками J3."""
import json, secrets
from score import ideas
if __name__ == "__main__":
    items = []
    for c in ["EVO1", "EVO2", "EVO3", "CTRL_CORE2", "DIFF_T1", "DIFF_T2"]:
        for i, d in enumerate(ideas(open(f"raw/r4/{c}.md").read()), 1): items.append((f"{c}#{i}", d))
    for f, c, i in [("raw/opus/OPUS_BASE_b.md","OPUS_BASE_b",1), ("raw/NEG.md","NEG",1), ("raw/r3/CORE_a.md","CORE_a",3),
                    ("raw/B1.md","B1",1), ("raw/opus/OPUS_MECH.md","OPUS_MECH",2), ("raw/DIFF.md","DIFF",1)]:
        items.append((f"ANCHOR:{c}#{i}", ideas(open(f).read())[i-1]))
    secrets.SystemRandom().shuffle(items); key = {}
    with open("blind_set_r4.txt", "w") as f:
        for j, (lab, d) in enumerate(items, 1):
            key[f"W{j:02d}"] = lab; f.write(f"W{j:02d}\nMECHANISM: {d['mech']}\nDIFFERENCE: {d['diff']}\n\n")
    json.dump(key, open("blind_key_r4.json", "w"), indent=1); print(len(items), "items:", sorted(set(v.split('#')[0] for v in key.values())))
