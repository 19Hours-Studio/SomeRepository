# Long-chain mode (LONG=1): does splice error accumulate as cleared observations pile up?
# Usage: python3 -I analyze_long.py spliceq_long.jsonl
import sys, json, statistics as st
R = [json.loads(l) for l in open(sys.argv[1])]
print(f"traces={len({r['id'] for r in R})}  eval points={len(R)}  sliding prompt mean={st.mean(r['sliding_len'] for r in R):,.0f} tok")
print(f"{'trace':24s} {'req':>4s} {'cleared':>7s} {'slid len':>8s} {'S0 KL':>7s} {'S0 top1':>7s} {'S128 KL':>8s} {'S128 top1':>9s} {'dNLL S0':>8s}")
for r in R:
    print(f"{r['id'][:24]:24s} {r['req']:4d} {r['n_cleared']:7d} {r['sliding_len']:8d} {r['S0']['kl']:7.4f} {r['S0']['top1']:7.3f} "
          f"{r['S128']['kl']:8.4f} {r['S128']['top1']:9.3f} {r['S0']['nll'] - r['ref']['nll']:+8.4f}")
for lo, hi in ((1, 10), (11, 20), (21, 35), (36, 99)):
    rs = [r for r in R if lo <= r["n_cleared"] <= hi]
    if rs: print(f"cleared {lo}-{hi}: n={len(rs)}  S0 KL={st.mean(r['S0']['kl'] for r in rs):.4f}  S128 KL={st.mean(r['S128']['kl'] for r in rs):.4f}  "
                 f"S0 top1={st.mean(r['S0']['top1'] for r in rs):.3f}")
