# Adds the policy-independent decode cost that billing2.py (c) leaves out (weights' 2*NP flops per output
# token), to show how much it dilutes the own-stack GPU-hour percentages. Reads billing2.out for GPU-h.
# Usage: python3 -I decode_dilute.py data/traces.jsonl billing2.out
import sys, os, json, re; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import traces as T
NP = 70.6e9; PEAK, MFU = 989e12, 0.45
nout = 0
for line in open(sys.argv[1]):
    t = json.loads(line); nout += sum(T.tok(m["text"]) for m in t["msgs"] if m["role"] == "assistant")
for mfu in (MFU, 0.15):   # 0.15: decode at modest batch is far below prefill MFU
    dec = nout * 2 * NP / (PEAK * mfu) / 3600
    print(f"output tokens {nout:,}  decode weight compute at {mfu:.0%} MFU: {dec:.2f} GPU-h")
    rows = {}
    for l in open(sys.argv[2]):
        m = re.match(r"\s+(\S+)\s+[\d.]+\s+\S+\s+[\d.]+\s+\S+\s+([\d.]+)\s+\S+\s+[\d.]+x", l)
        if m: rows[m.group(1)] = float(m.group(2))
    a = rows["append"] + dec
    for k, g in rows.items(): print(f"  {k:24s} GPU-h {g + dec:6.2f}  vs append {(g + dec) / a - 1:+.1%}")
