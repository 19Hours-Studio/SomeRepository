# Summarise clearq.py output (KL(append || cleared), top-1 agreement, dNLL), only at points where the
# policy actually cleared something. Usage: python3 -I clearq_sum.py out/clearq.jsonl
import sys, json, statistics as st
rows = [json.loads(l) for l in open(sys.argv[1]) if l.startswith("{")]
print(f"eval points={len(rows)} traces={len({r['id'] for r in rows})} mean append prompt={st.mean(r['ctx_append'] for r in rows):,.0f}")
for k in ("keep5", "keep3"):
    g = [r for r in rows if r[k]["ctx"] < r["ctx_append"]]
    if not g: continue
    print(f"{k}: points that cleared={len(g)}  prompt {st.mean(r[k]['ctx'] for r in g):,.0f} vs append {st.mean(r['ctx_append'] for r in g):,.0f}"
          f"  KL={st.mean(r[k]['kl'] for r in g):.5f} (median {st.median(r[k]['kl'] for r in g):.5f})"
          f"  top1={st.mean(r[k]['top1'] for r in g):.4f}  dNLL={st.mean(r[k]['dnll'] for r in g):+.4f}")
