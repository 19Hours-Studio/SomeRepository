"""Слепой набор раунда 2: 15 новых идей + 6 якорей из раунда 1 (для калибровки судьи)."""
import json, secrets
from score import ideas
items = []
for c in ["MAP", "MSC", "LOCK", "REFRAME", "STACK"]:
    for i, d in enumerate(ideas(open(f"raw/r2/{c}.md").read()), 1): items.append((f"{c}#{i}", d))
for a in ["B1#1", "B2#1", "NEG#1", "NEG#3", "MECH#2", "DIFF#1"]:
    c, i = a.split("#"); items.append((f"ANCHOR:{a}", ideas(open(f"raw/{c}.md").read())[int(i) - 1]))
secrets.SystemRandom().shuffle(items)
key = {}
with open("blind_set_r2.txt", "w") as f:
    for j, (lab, d) in enumerate(items, 1):
        key[f"Y{j:02d}"] = lab
        f.write(f"Y{j:02d}\nMECHANISM: {d['mech']}\nDIFFERENCE: {d['diff']}\n\n")
json.dump(key, open("blind_key_r2.json", "w"), indent=1); print(len(items), "items")
