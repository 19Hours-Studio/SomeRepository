"""Восстанавливает соответствие X-ID -> условие по тексту, который судья реально прочитал (из транскрипта),
а не по blind_key.json (устойчиво к перезаписи файла)."""
import json, re, sys, glob, os
from score import ideas
tr = sys.argv[1]
seen = None
for line in open(tr):
    ev = json.loads(line); m = ev.get("message") or {}
    if m.get("role") == "user" and isinstance(m.get("content"), list):
        for p in m["content"]:
            if p.get("type") == "tool_result":
                c = p.get("content"); c = c if isinstance(c, str) else "".join(x.get("text", "") for x in c)
                if "MECHANISM:" in c: seen = c
idx = {}
for p in glob.glob("raw/*.md"):
    for i, d in enumerate(ideas(open(p).read()), 1):
        idx[d["mech"][:80]] = f"{os.path.basename(p)[:-3]}#{i}"
key = {}
for blk in re.split(r"\n(?=\s*\d*→?\s*X\d\d\s*\n)", seen):
    mid = re.search(r"(X\d\d)\s*\n", blk); mm = re.search(r"MECHANISM: (.{80})", blk)
    if mid and mm: key[mid.group(1)] = idx.get(mm.group(1), "?")
json.dump(key, open(sys.argv[2], "w"), indent=1); print(len(key), "mapped;", sum(v == "?" for v in key.values()), "unmatched")
