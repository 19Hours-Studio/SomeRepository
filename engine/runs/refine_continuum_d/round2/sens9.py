"""Continuum-9 sensitivities: every single adverse assumption and every pair (128K), singles at 1M.
Base design model9.BASE (EP split, W-tier omega 0.7, 64 lanes, g <= 14). Rubin trimmed 150 W unless the case says.
Usage: python3 sens9.py > sens9.txt"""
import itertools, sys
from multiprocessing import Pool
import model9 as e9
q, e8 = e9.q, e9.e8

SINGLES = {
    "same node (C-die compute energy x1.25)": dict(parts_over={"comp_w": 1.25}),
    "eta 0.5 (Continuum only)": dict(base_over={"F4": 5 / 6, "F8": 5 / 6}),
    "W-tier 0.30 pJ/bit (dynamic x2)": dict(wt_dyn=2.0),
    "leakage x2": dict(parts_over={"leak_w": 2.0}),
    "SRAM static 200 W (not 100)": dict(s_static=200.0),
    "no hot-expert replicas (imb 1.12)": dict(imb_fixed=1.12),
    "tile imbalance 1.25": dict(imb_fixed=1.25),
    "EP package imbalance >= 1.15": dict(_ep=1.15),
    "collectives 12 us (Continuum only)": dict(_coll=12),
    "usable SRAM 80% (not 90%)": dict(_fill=0.8),
    "Vmin floor 0.60 V for both": dict(labels=("0.60V wt",), _r=dict(floor=True)),
    "two-phase (no overlap), both": dict(two_phase=True, _r=dict(tp=True)),
    "Rubin trimmed 250 W (not 150)": dict(_r=dict(trim=250)),
    "hot spares 3% at full power (Continuum only)": dict(spares=0.03, spare_mode="hot"),
}
EXCL = {frozenset(("no hot-expert replicas (imb 1.12)", "tile imbalance 1.25"))}


def merge(a, b):
    out = dict(a)
    for k, v in b.items():
        if k in ("parts_over", "base_over"): out[k] = {**out.get(k, {}), **v}
        elif k == "_r": out[k] = {**out.get(k, {}), **v}
        elif k == "imb_fixed": out[k] = max(out.get(k, 0), v)
        else: out[k] = v
    return out


def rubin_env(ctx, trim=150, floor=False, tp=False):
    profs = e8.rubin_prof(trim)
    if floor: profs = [p for p in profs if p[0] in ("0.75V", "0.65V", "0.60V", "MaxQ")]
    return e8.gpu_env(profs, ctx, two_phase=tp)


def run(args):
    name, kw, ctx = args
    kw = dict(kw); r = kw.pop("_r", {})
    e9.IMB_EP = kw.pop("_ep", None)
    e8.FILL = kw.pop("_fill", 0.9)
    coll = kw.pop("_coll", None)
    if coll: kw["tau_fn"] = lambda f, c=coll: (c + 3 / f) * 1e-6
    A = e9.env(ctx, **{**e9.BASE, **kw})
    R = rubin_env(ctx, **r)
    return name, ctx, e8.rat(A, R), e8.fmt(A)


if __name__ == "__main__":
    jobs = [("base", {}, q.C128), ("base", {}, q.C1M)]
    jobs += [(n, kw, c) for n, kw in SINGLES.items() for c in (q.C128, q.C1M)]
    for a, b in itertools.combinations(SINGLES, 2):
        if frozenset((a, b)) in EXCL: continue
        jobs.append((f"PAIR {a} + {b}", merge(SINGLES[a], SINGLES[b]), q.C128))
    print(" " * 92 + " ".join(f"{t:>6}" for t in q.T), flush=True)
    with Pool(4) as p:
        for name, ctx, r, v in p.imap(run, jobs):
            print(f"{ctx//1024:>5}K {name:<85}{r}   (C9 {v})", flush=True)
