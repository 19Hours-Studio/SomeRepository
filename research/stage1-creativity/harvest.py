"""Собирает пул слов из случайных текстов системы (не курируется моделью)."""
import os, re, random, collections, sys
roots = ["/usr/share/doc", "/usr/share/common-licenses", "/usr/lib/python3"]
cnt = collections.Counter(); df = collections.Counter()
files = []
for r in roots:
    for d, _, fs in os.walk(r):
        for f in fs:
            if f.endswith((".txt", ".py", "copyright", "README", ".md", ".rst")) or "." not in f:
                files.append(os.path.join(d, f))
random.seed(0)
random.shuffle(files)
for p in files[:4000]:
    try:
        t = open(p, errors="ignore").read(200_000)
    except Exception:
        continue
    ws = re.findall(r"\b[a-z]{5,12}\b", t)
    cnt.update(ws); df.update(set(ws))
# убираем самые частые (служебные/программистские) и редкие опечатки
common = {w for w, _ in cnt.most_common(400)}
pool = sorted(w for w, c in cnt.items() if df[w] >= 4 and w not in common and re.search(r'[aeiou].*[aeiou]', w))
open("wordpool.txt", "w").write("\n".join(pool))
print(len(files), "files;", len(pool), "words in pool")
