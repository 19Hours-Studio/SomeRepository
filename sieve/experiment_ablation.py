"""Ablation of SIEVE's core claim on CPU: how much verified knowledge per verifier call.

Arms (same learner, same verifier budget):
  A random     random statements verified, learner sees only verified labels
  B +prop      + label propagation through the implication lattice
  C +coh       + coherence loss on lattice edges
  E +unc       B with classic uncertainty sampling (entropy only) - standard active learning baseline
  D full       B + C + acquisition = entropy x (1 + misclosure) x expected reach
Test: held-out families, exact labels. Usage: python3 experiment_ablation.py [--seeds 3] [--quick]
"""
import argparse, json, os, time
import numpy as np
from bitworld import build_pool, RULES
from lattice import Lattice
from learner_np import featurize, MLP, train_rfree

ARMS = {"A_random": dict(prop=False, coh=0.0, acq="random"),
        "B_prop": dict(prop=True, coh=0.0, acq="random"),
        "C_prop_coh": dict(prop=True, coh=1.0, acq="random"),
        "E_prop_unc": dict(prop=True, coh=0.0, acq="entropy"),
        "D_full": dict(prop=True, coh=1.0, acq="lattice")}
NEAR = {r[0] for r in RULES if not r[3]}


def metrics(p, y, near):
    q = np.clip(p, 1e-6, 1 - 1e-6)
    ll = float(-(y * np.log(q) + (1 - y) * np.log(1 - q)).mean())
    acc = float(((p > 0.5) == y).mean()); acc_near = float(((p[near] > 0.5) == y[near]).mean())
    pos, neg = p[y == 1], p[y == 0]
    auc = float((pos[:, None] > neg[None, :]).mean() + 0.5 * (pos[:, None] == neg[None, :]).mean())
    return dict(logloss=round(ll, 4), acc=round(acc, 4), acc_near=round(acc_near, 4), auc=round(auc, 4))


def family_weights(lat, lab, fam_of):
    """One verifier call = one unit of weight, spread over the labels of its family (propagated labels are
    correct but come in correlated cones; without this the learner overweights families with big cones)."""
    calls = np.bincount(fam_of[np.flatnonzero(lat.verified)], minlength=fam_of.max() + 1)
    nlab = np.bincount(fam_of[lab], minlength=fam_of.max() + 1)
    f = fam_of[lab]; return (calls[f] / nlab[f]).astype(np.float32)


def run_arm(cfg, pool, test, seed, budgets, step):
    stmts, edges, truth, Fp = pool; Ft, yt, near_t = test
    rng = np.random.default_rng(seed); lat = Lattice(len(stmts), edges)
    model = MLP(seed=seed); E = np.array(edges); fam_of = np.array([s.fam for s in stmts])
    first = rng.choice(len(stmts), 10, replace=False)  # identical warm start for all arms (same seed)
    calls = 0; out = []
    for i in first: lat.observe(i, truth[i], cfg["prop"]); calls += 1
    while calls < budgets[-1]:
        lab = np.flatnonzero(lat.label >= 0)
        model.fit(Fp[lab], lat.label[lab].astype(np.float32), epochs=8, edges=E if cfg["coh"] else None,
                  Fall=Fp, lam=cfg["coh"], rng=rng, w=family_weights(lat, lab, fam_of))
        p = model.predict(Fp)
        k = min(step, budgets[-1] - calls); unl = np.flatnonzero(lat.label < 0)
        if cfg["acq"] == "random":
            pick = rng.choice(unl, min(k, len(unl)), replace=False)
        elif cfg["acq"] == "entropy":
            q = np.clip(p[unl], 1e-6, 1 - 1e-6); ent = -(q * np.log(q) + (1 - q) * np.log(1 - q))
            pick = unl[np.argsort(-ent)[:k]]
        else:
            pick = lat.acquire(p, k, rng)
        for i in pick:
            lat.observe(i, truth[i], cfg["prop"]); calls += 1
            if calls in budgets:
                lab = np.flatnonzero(lat.label >= 0)
                # evaluation model: fresh, R-free early stopping + temperature, family weights
                m = train_rfree(Fp[lab], lat.label[lab].astype(np.float32), fam_of[lab], edges=E if cfg["coh"] else None,
                                Fall=Fp, lam=cfg["coh"], seed=seed + 7, w=family_weights(lat, lab, fam_of))
                r = metrics(m.predict(Ft), yt, near_t); r.update(calls=calls, labels=int((lat.label >= 0).sum()),
                                                                 wrong_labels=int((lat.label[lab] != truth[lab]).sum()),
                         label_true_share=round(float(lat.label[lab].mean()), 3), families=int(len(np.unique(fam_of[lab]))))
                out.append(r)
    return out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--seeds", type=int, default=3); ap.add_argument("--quick", action="store_true")
    a = ap.parse_args()
    nf, budgets = (120, [30, 60, 120]) if a.quick else (300, [25, 50, 100, 200, 400])
    t0 = time.time(); res = {k: [] for k in ARMS}
    test_s, _, test_y = build_pool(100, seed=10_000)
    Ft = featurize(test_s); near_t = np.array([s.rule in NEAR for s in test_s])
    for seed in range(a.seeds):
        stmts, edges, truth = build_pool(nf, seed=seed)
        pool = (stmts, edges, truth, featurize(stmts))
        for name, cfg in ARMS.items():
            res[name].append(run_arm(cfg, pool, (Ft, test_y.astype(np.float32), near_t), seed, budgets, step=10))
            print(f"seed {seed} {name:12s} " + " | ".join(f"{r['calls']}:{r['logloss']:.3f}/{r['acc']:.3f}" for r in res[name][-1]), flush=True)
    summary = {}
    for name, runs in res.items():
        summary[name] = []
        for b_i, b in enumerate(budgets):
            rows = [r[b_i] for r in runs]
            summary[name].append({k: round(float(np.mean([r[k] for r in rows])), 4) for k in rows[0]})
    base = float(test_y.mean()); prior_ll = -(base * np.log(base) + (1 - base) * np.log(1 - base))
    out = dict(budgets=budgets, seeds=a.seeds, pool_families=nf, test_size=len(test_s), test_true_share=round(base, 3),
               prior_logloss=round(float(prior_ll), 4), summary=summary, runs=res, seconds=round(time.time() - t0, 1))
    os.makedirs("results", exist_ok=True)
    fn = "results/ablation_quick.json" if a.quick else "results/ablation.json"
    json.dump(out, open(fn, "w"), indent=1)
    print(f"\nprior logloss {prior_ll:.3f}; test true share {base:.2f}; {out['seconds']} s")
    print(f"{'arm':12s} " + " ".join(f"{b:>18d}" for b in budgets))
    for name, rows in summary.items():
        print(f"{name:12s} " + " ".join(f"{r['logloss']:.3f}/{r['acc']:.3f}/{r['labels']:5.0f}" for r in rows))


if __name__ == "__main__":
    main()
