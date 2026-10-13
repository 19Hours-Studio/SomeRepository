"""Deterministic character corpus: top-level .py files of the CPython 3.13 stdlib (sorted), ASCII only.
Files are split by name hash into train (90%) and validation (10%), so validation is unseen code."""
import hashlib, os, sys
SRC = "/usr/lib/python3.13"; OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(OUT, exist_ok=True); tr, va = [], []
for f in sorted(os.listdir(SRC)):
    if not f.endswith(".py"): continue
    t = open(os.path.join(SRC, f), encoding="utf-8", errors="ignore").read()
    t = "".join(c for c in t if c == "\n" or 32 <= ord(c) < 127)
    (va if int(hashlib.md5(f.encode()).hexdigest(), 16) % 10 == 0 else tr).append(t)
open(os.path.join(OUT, "train.txt"), "w").write("\n".join(tr)); open(os.path.join(OUT, "val.txt"), "w").write("\n".join(va))
print(len("\n".join(tr)), len("\n".join(va)))
