"""Statistics for the v3.0 genius experiment (10-genius-engine.md): kill-test verdicts per pool and technique,
calibration items, judges' O on set s99s, and the O x headroom selection.
Run from the repo root: python3 engine/runs/permafrost/genius/gate_stats.py"""
import json, os, sys
from collections import defaultdict
sys.path.insert(0, "engine"); import ce  # noqa: E402
R = "permafrost"; RD = os.path.join("engine", "runs", R)
ideas = {i["id"]: i for i in json.load(open(os.path.join(RD, "ideas.json")))}
gate = json.load(open(os.path.join(RD, "gate.json")))
pools = json.load(open(os.path.join(RD, "genius", "pools.json")))
S = json.load(open(os.path.join(RD, "scores.json")))

def o_s99s(i):
    js = [v for k, v in S.get(i, {}).items() if k.startswith("s99s:")]
    return sum(j["O"] for j in js) / len(js) if js else None

def group(i):
    if i in pools["calib"]: return "calib"
    a = ideas[i]["arm"]
    return {"GF": "new:frontier", "GL": "new:ledger", "GFL": "new:frontier+ledger", "EC": "EC (round 1, A->B->C)"}.get(a, "g1 raw (round 1)")

rows = defaultdict(list)
for i, g in gate.items():
    if i in ideas: rows[group(i)].append((i, g))
print(f"{'pool':26s} {'n':>3s} {'ALIVE':>6s} {'WOUND':>6s} {'DEAD':>5s} {'med RATIO':>9s} {'med MARGIN':>10s} {'O s99s':>7s}")
def med(x):
    x = sorted(v for v in x if v is not None); return x[len(x) // 2] if x else float("nan")
for name in ("new:frontier", "new:ledger", "new:frontier+ledger", "g1 raw (round 1)", "EC (round 1, A->B->C)", "calib"):
    L = rows.get(name, []); n = len(L) or 1
    c = lambda v: sum(g["verdict"] == v for _, g in L)
    os_ = [o_s99s(i) for i, _ in L if o_s99s(i) is not None]
    print(f"{name:26s} {len(L):3d} {c('ALIVE')/n:6.0%} {c('WOUNDED')/n:6.0%} {c('DEAD')/n:5.0%} {med([g.get('ratio') for _, g in L]):9.2f} "
          f"{med([g.get('margin') for _, g in L]):10.2f} {(sum(os_)/len(os_) if os_ else float('nan')):7.2f}")
new = [x for k in ("new:frontier", "new:ledger", "new:frontier+ledger") for x in rows.get(k, [])]
print(f"{'new (all v3.0)':26s} {len(new):3d} {sum(g['verdict']=='ALIVE' for _, g in new)/max(1,len(new)):6.0%}")
print("\ncalibration (known audit outcome):")
for i, g in rows.get("calib", []):
    print(f"  {i:10s} {g['verdict']:8s} margin {g.get('margin')} ratio {g.get('ratio')} | {g['why'][:90]}")
print("\nALIVE ideas (O s99s, ratio, margin):")
alive = sorted(((o_s99s(i) or 0, i, g) for L in rows.values() for i, g in L if g["verdict"] == "ALIVE"), reverse=True)
for o, i, g in alive:
    print(f"  O{o:4.1f} r{g.get('ratio', 0):5.2f} m{g.get('margin', 0):6.2f} {group(i):24s} {ideas[i]['name'][:45]}")
print("\nselection by O x weight x min(ratio,5) (top 10):")
W = {"ALIVE": 1.0, "WOUNDED": 0.4, "DEAD": 0.0}
sel = sorted((((o_s99s(i) or 0) * W[g["verdict"]] * min(g.get("ratio", 1.0), 5.0), i) for L in rows.values() for i, g in L
              if group(i) != "calib"), reverse=True)[:10]
r1_top8 = set(json.load(open(os.path.join(RD, "repair", "a", "parents.json"))) + json.load(open(os.path.join(RD, "repair", "b", "parents.json"))))
for sc, i in sel:
    print(f"  {sc:5.1f} {i:22s} {group(i):24s} {'(was in round-1 top-8)' if i in r1_top8 else ''} {ideas[i]['name'][:45]}")
