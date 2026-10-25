import json, random, statistics as st, sys
from sim import run, eoq_K, PRICES

def mean_runs(sessions, **kw):
    r = [run(s, p, **kw) for s, p in sessions]
    tot = sum(x["cost"] for x in r)
    return dict(hit=sum(x["hit"]*x["sent"] for x in r)/sum(x["sent"] for x in r),
                cost=tot/len(r), peak=max(x["peak"] for x in r))

def table(title, sessions, W, R, n=5, edits_fn=None, ref="none"):
    print(f"\n== {title}  (W={W}, R={R}, window n={n}) ==")
    steps_all = [x for s, _ in sessions for x in s]
    K = eoq_K(steps_all, n, W, R)
    rows = {}
    def ed(mode, e=None):
        return None if edits_fn is None else [edits_fn(i, mode, e) for i in range(len(sessions))]
    def go(name, **kw):
        if edits_fn is None:
            rows[name] = mean_runs(sessions, W=W, R=R, n=n, **kw)
        else:
            mode = kw.pop("mode", "erratum")
            r = [run(s, p, W=W, R=R, n=n, edits=edits_fn(i, mode), **kw) for i, (s, p) in enumerate(sessions)]
            rows[name] = dict(hit=sum(x["hit"]*x["sent"] for x in r)/sum(x["sent"] for x in r),
                              cost=sum(x["cost"] for x in r)/len(r), peak=max(x["peak"] for x in r))
    if edits_fn is not None: go("in-place edits (prefix caching)", policy="none", mode="inplace")
    go("append-only / errata (baseline Idea 1)", policy="none")
    go("mask every turn (SWE-agent 0.7, polling=1)", policy="poll", K=1)
    best = min(range(1, 60), key=lambda k: mean_runs(sessions, W=W, R=R, n=n, policy="poll", K=k)["cost"]
               if edits_fn is None else
               sum(run(s, p, W=W, R=R, n=n, policy="poll", K=k, edits=edits_fn(i, "erratum"))["cost"] for i, (s, p) in enumerate(sessions)))
    go(f"mask, EOQ batch K*={K} (closed form)", policy="poll", K=K)
    go("mask, online ski-rental trigger", policy="balance")
    go(f"mask, oracle best fixed K={best}", policy="poll", K=best)
    go("Anthropic-style clear_tool_uses(100k, keep 3, >=20k)", policy="clear_tool_uses")
    base = rows["in-place edits (prefix caching)" if edits_fn is not None else "append-only / errata (baseline Idea 1)"]
    errata = rows["append-only / errata (baseline Idea 1)"]
    for k, v in rows.items():
        print(f"  {k:52s} hit={v['hit']:.3f}  cost/session={v['cost']:>10,.0f}  peak ctx={v['peak']:>8,}  "
              f"vs ref {1-v['cost']/base['cost']:+.1%}  vs errata {1-v['cost']/errata['cost']:+.1%}")
    return rows

if __name__ == "__main__":
    # ---- W1: the baseline's synthetic agent workload (sys 10k, 2000-tok tool result + 300-tok output, 50 turns,
    #      one earlier tool output changes every 5 turns, position uniform; 200 seeds), full-size 2300-tok errata.
    for T in (50, 100):
        sess = [([(300, 2000)]*T, 10_000) for _ in range(200)]
        def edits_fn(i, mode, e=None, T=T):
            rng = random.Random(i)
            return {t: (rng.random(), 2300, mode) for t in range(5, T, 5)}
        for pr in ("anthropic", "openai"):
            table(f"W1 synthetic, {T} turns, {pr}", sess, *PRICES[pr], edits_fn=edits_fn)
    # ---- W2: real SWE-agent trajectories (19 unique public demos, token sizes = chars/4)
    D = json.load(open("data/swea_steps.json"))
    real = [([tuple(x) for x in d["steps"]], d["prompt_tok"]) for d in D]
    print("\nreal trajectories: steps", [len(s) for s, _ in real], "mean obs tok",
          round(st.mean(o for s, _ in real for _, o in s)), "mean asst tok", round(st.mean(a for s, _ in real for a, _ in s)),
          "median prompt tok", st.median(p for _, p in real))
    for pr in ("anthropic", "openai"):
        table(f"W2a real trajectories as recorded, {pr}", real, *PRICES[pr])
    pool = [x for s, _ in real for x in s]; prompt = int(st.median(p for _, p in real))
    for T in (50, 100):
        rng = random.Random(1)
        boot = [([rng.choice(pool) for _ in range(T)], prompt) for _ in range(200)]
        for pr in ("anthropic", "openai"):
            for n in ((5, 10) if pr == "anthropic" else (5,)):
                table(f"W2b bootstrapped from real steps, {T} steps, {pr}", boot, *PRICES[pr], n=n)
