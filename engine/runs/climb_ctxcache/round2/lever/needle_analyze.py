# Summarise needle.jsonl. s = log P(NEW) - log P(OLD) for the answer to "what is the port?".
# Correction: does the spliced cache still answer the NEW value like exact recompute does?
# Clearing:  how much of the deleted OLD value leaks back through downstream KV that was not recomputed?
#            leak fraction = (s_exact_cleared - s_splice) / (s_exact_cleared - s_exact_old): 0 = forgets like exact, 1 = remembers fully.
# Usage: python3 -I needle_analyze.py needle.jsonl
import sys, json, statistics as st
R = [json.loads(l) for l in open(sys.argv[1])]
ks = sorted({int(k.split("_k")[1]) for k in R[0] if "_k" in k})
print(f"trials={len(R)}  downstream tokens mean={st.mean(r['down'] for r in R):,.0f}")
print("correction (port changed OLD -> NEW in place):")
for name in ["exact_new", "exact_old"] + [f"corr_splice_k{k}" for k in ks]:
    print(f"  {name:18s} answers NEW in {sum(r[name] > 0 for r in R):2d}/{len(R)}  mean s={st.mean(r[name] for r in R):+.2f}"
          + ("" if name.startswith("exact") else f"  shift toward OLD vs exact_new={st.mean(r['exact_new'] - r[name] for r in R):+.2f} nats"))
print("clearing (port line replaced by a placeholder):")
for name in ["exact_cleared"] + [f"clear_splice_k{k}" for k in ks]:
    lf = st.mean((r["exact_cleared"] - r[name]) / (r["exact_cleared"] - r["exact_old"]) for r in R)
    print(f"  {name:18s} mean s={st.mean(r[name] for r in R):+.2f}  P(OLD)>P(NEW) in {sum(r[name] < 0 for r in R):2d}/{len(R)}  leak fraction={lf:+.3f}")
print(f"  (exact_old, full memory: mean s={st.mean(r['exact_old'] for r in R):+.2f})")
