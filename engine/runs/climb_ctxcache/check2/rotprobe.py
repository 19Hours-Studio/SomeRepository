# check2 probe: what does the splice's key re-rotation cost if counted as memory traffic (read+write K of
# every re-rotated token, BF16) instead of 6 flops/element? And alternatives: rotate the shorter side
# (prefix right instead of tail left: same relative positions), or RoPE applied in-kernel (zero extra).
# Also: splices per trace (quality test covers <=9), output share of bill.
import sys, os; F = sys.argv[1]; sys.path.insert(0, F)
import traces as T
sys.argv = [sys.argv[0], F + "/data/traces.jsonl"]
src = open(F + "/billing2.py").read().replace("main(sys.argv[1])", "")
exec(compile(src, "billing2", "exec"))
KB = NL * DKV * 2            # K bytes per token per full model, BF16
BW = HBM * HBMU
tot = {}
def add(k, v): tot[k] = tot.get(k, 0) + v
nspl = []; Tr = T.load(F + "/data/traces.jsonl")
for tr in Tr:
    ntok = [T.tok(s) for s in tr["text"]]; A = T.requests(tr)
    for name, seq in (("sliding", T.policy_seq(tr, ntok, "sliding", W, R)), ("polling10", polling_seq(tr, ntok, 10, 5))):
        prev = []; ns = 0
        for s in seq:
            pk = set(k for k, _ in prev)
            first = next((i for i, (x, y) in enumerate(zip(prev, s)) if x != y), min(len(prev), len(s)))
            if first < len(prev):
                ns += 1
                tail = sum(t for k, t in s[first:] if k in pk); pre = sum(t for _, t in s[:first])
                add(name + ":tail", tail); add(name + ":short", min(tail, pre))
            prev = s
        if name == "sliding": nspl.append(ns)
        add(name + ":nspl", ns)
    add("out", sum(ntok[a] for a in A))
for name in ("sliding", "polling10"):
    for side in ("tail", "short"):
        b = tot[name + ":" + side] * 2 * KB   # read + write
        print(f"{name:10s} rotate {side:5s}: {tot[name+':'+side]/1e6:8.1f} M token-rotations  memory-bound {b/BW/3600:5.2f} GPU-h"
              f"  (flop-count used in billing2: {tot[name+':'+side]*NL*DKV*6/(PEAK*MFU)/3600:.3f} GPU-h)")
import statistics as st
print(f"splice events per trace, sliding keep5: mean {st.mean(nspl):.1f} median {st.median(nspl)} max {max(nspl)}; polling10 total {tot['polling10:nspl']}")
