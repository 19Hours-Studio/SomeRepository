"""Summarise exp_edit.py output: per edit case and reuse variant, divergence from exact
recompute, top-1 agreement, NLL of the real next action, and recompute share.
Usage: python3 -I analyze.py out/edit_*.jsonl
"""
import json, sys, random, statistics as st

R = list({r["id"]: r for r in (json.loads(l) for f in sys.argv[1:] for l in open(f))}.values())  # dedupe resumed runs
rng = random.Random(0)


def boot(xs, n=2000):
    m = [st.mean(rng.choices(xs, k=len(xs))) for _ in range(n)]
    m.sort(); return m[int(.025 * n)], m[int(.975 * n)]


print(f"traces: {len(R)}   prompt tokens: mean {st.mean(r['ntok'] for r in R):,.0f}, max {max(r['ntok'] for r in R):,}")
print("Model SmolLM2-135M-Instruct (Q4_1). Target: first <=96 tokens of the real next assistant message.")
print("KL = KL(exact || variant) per target token, nats. 'edit size' = KL(exact || unedited context).")
print("dNLL = NLL(variant) - NLL(exact) on the real tokens (negative = predicts the real action better), 95% bootstrap CI.")
for case in ("clear", "replace", "insert", "reorder"):
    rs = [r["cases"][case] for r in R if case in r["cases"]]
    if not rs:
        continue
    after = st.mean(x["ntok"] - x["first_change"] for x in rs)
    print(f"\n== {case}: n={len(rs)}  prompt {st.mean(x['ntok'] for x in rs):,.0f} tok, "
          f"{after:,.0f} tok after first change, {st.mean(x['n_new'] for x in rs):,.0f} new tok")
    print(f"{'variant':16s} {'meanKL':>8s} {'medKL':>8s} {'p90KL':>8s} {'KL/edit':>8s} {'top1':>6s} {'NLL':>6s} "
          f"{'dNLL [95% CI]':>24s} {'recomp/after':>12s} {'KL(unedited||v)':>15s}")
    ed = st.mean(x["FULL"]["kl"] for x in rs)
    names = [k for k in rs[0] if isinstance(rs[0][k], dict)]
    for k in names:
        kl = [x[k]["kl"] for x in rs]; s = sorted(kl)
        dn = [x[k]["nll"] - x["EXACT"]["nll"] for x in rs]; lo, hi = boot(dn)
        rec = (f"{st.mean(x[k]['recompute'] / max(1, x['ntok'] - x['first_change']) for x in rs):.1%}"
               if "recompute" in rs[0][k] else ("100%" if k == "EXACT" else "-"))
        klf = f"{st.mean(x[k]['kl_full'] for x in rs):.4f}" if "kl_full" in rs[0][k] else ("0" if k == "FULL" else "-")
        print(f"{k:16s} {st.mean(kl):8.4f} {st.median(kl):8.4f} {s[int(.9 * (len(s) - 1))]:8.4f} "
              f"{st.mean(kl) / ed:8.2f} {st.mean(x[k]['top1'] for x in rs):6.3f} {st.mean(x[k]['nll'] for x in rs):6.3f} "
              f"{st.mean(dn):+8.3f} [{lo:+.3f},{hi:+.3f}] {rec:>12s} {klf:>15s}")
