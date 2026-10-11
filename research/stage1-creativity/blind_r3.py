"""Слепой набор Opus-раунда: 15 идей Opus + 6 идей CORE (Haiku) + 6 якорей из раунда 1."""
import json, secrets
from score import ideas
items = []
for c in ["OPUS_BASE_a", "OPUS_BASE_b", "OPUS_NEG", "OPUS_MECH", "OPUS_CORE2"]:
    for i, d in enumerate(ideas(open(f"raw/opus/{c}.md").read()), 1): items.append((f"{c}#{i}", d))
for c in ["CORE_a", "CORE_b"]:
    for i, d in enumerate(ideas(open(f"raw/r3/{c}.md").read()), 1): items.append((f"HAIKU_{c}#{i}", d))
for a in ["B1#1", "B2#1", "NEG#1", "NEG#3", "MECH#2", "DIFF#1"]:
    c, i = a.split("#"); items.append((f"ANCHOR:{a}", ideas(open(f"raw/{c}.md").read())[int(i) - 1]))
secrets.SystemRandom().shuffle(items)
key = {}
with open("blind_set_r3.txt", "w") as f:
    for j, (lab, d) in enumerate(items, 1):
        key[f"Z{j:02d}"] = lab
        f.write(f"Z{j:02d}\nMECHANISM: {d['mech']}\nDIFFERENCE: {d['diff']}\n\n")
json.dump(key, open("blind_key_r3.json", "w"), indent=1); print(len(items), "items")
