"""Проверка LOCK: все 8 слов в MECHANISM по порядку (машинная проверка ограничения)."""
import json, re
from score import ideas
locks = json.load(open("prompts/r2/draws.json"))["LOCK"]
for i, (d, l) in enumerate(zip(ideas(open("raw/LOCK.md").read()), locks), 1):
    toks = re.findall(r"[a-z]+", d["mech"].lower()); pos = 0; kept = 0
    for w in l.split():
        try: pos = toks.index(w, pos) + 1; kept += 1
        except ValueError: pass
    print(f"LOCK idea {i}: {kept}/8 locked words in order; present anywhere: {sum(w in toks for w in l.split())}/8")
