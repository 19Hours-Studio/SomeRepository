"""Извлекает финальный текст субагента из JSONL-транскрипта в raw/<COND>.md."""
import json, sys
cond, path = sys.argv[1], sys.argv[2]
last = ""
for line in open(path):
    try: ev = json.loads(line)
    except Exception: continue
    msg = ev.get("message") or {}
    if msg.get("role") == "assistant":
        parts = msg.get("content")
        if isinstance(parts, list):
            t = "".join(p.get("text", "") for p in parts if isinstance(p, dict) and p.get("type") == "text")
            if t.strip(): last = t
open(f"raw/{cond}.md", "w").write(last)
print(cond, len(last.split()), "words")
