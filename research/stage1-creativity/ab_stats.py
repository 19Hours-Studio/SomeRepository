"""Статистика A/B по плечам для прогонов финального судейства движка (ab1_final15, ab1_final16, ...).

Использование: python3 research/stage1-creativity/ab_stats.py RUN [--prior-prefix PV] [--paired]
--paired: парные разности «потомок слоя минус родитель» (по полю parent) для каждой руки слоёв B/C,
и разность «C минус исходная идея A» по всей цепочке родителей.
Для каждого плеча и каждой группы судей (s99 = судьи с картой, s98c = чистый судья):
O, C, V, O×V (среднее по идеям от средних O и V), топ-3 O×V, переоткрытия (R=Y хоть у одного),
доля оценок в бассейне «ранее найденного» (код начинается с --prior-prefix), и разбивка по технике.
"""
import json, os, sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
RUNS = os.path.join(HERE, "..", "..", "engine", "runs")


def stats(run, prior_prefix="PV"):
    S = json.load(open(os.path.join(RUNS, run, "scores.json")))
    ideas = {i["id"]: i for i in json.load(open(os.path.join(RUNS, run, "ideas.json")))}
    groups = sorted({k.split(":")[0] for s in S.values() for k in s})
    out = {}
    for g in groups:
        by_arm, by_tech = defaultdict(list), defaultdict(list)
        for iid, s in S.items():
            js = [v for k, v in s.items() if k.startswith(g + ":")]
            if not js or iid not in ideas: continue
            m = lambda f: sum(j[f] for j in js) / len(js)
            row = {"id": iid, "O": m("O"), "C": m("C"), "V": m("V"), "OV": m("O") * m("V"),
                   "R": any(j["R"] == "Y" for j in js),
                   "prior": sum(str(j["B"]).startswith(prior_prefix) for j in js) / len(js),
                   "name": ideas[iid]["name"],
                   "G": mean([j["G"] for j in js if "G" in j]) if any("G" in j for j in js) else float("nan"),
                   "X": mean([j["X"] == "Y" for j in js if "X" in j]) if any("X" in j for j in js) else float("nan"),
                   "F": mean([j["F"] for j in js if "F" in j]) if any("F" in j for j in js) else float("nan")}
            arm = ideas[iid]["arm"]; by_arm[arm].append(row)
            by_tech[(arm, ideas[iid]["label"].split(":")[-1])].append(row)
        out[g] = (by_arm, by_tech)
    return out


def mean(xs): return sum(xs) / len(xs) if xs else float("nan")


def paired(run):
    S = json.load(open(os.path.join(RUNS, run, "scores.json")))
    ideas = {i["id"]: i for i in json.load(open(os.path.join(RUNS, run, "ideas.json")))}
    groups = sorted({k.split(":")[0] for s in S.values() for k in s})
    def sc(iid, g, f):
        js = [v for k, v in S.get(iid, {}).items() if k.startswith(g + ":") and f in v]
        return mean([j[f] for j in js]) if js else None
    def root(iid):
        while ideas[iid].get("parent") in ideas: iid = ideas[iid]["parent"]
        return iid
    for g in groups:
        print(f"== {g} paired (child - parent): n, dO, dC, dV, dG, share dO<0, share dV<0")
        arms = sorted({i["arm"] for i in ideas.values() if i.get("parent")})
        for arm in arms:
            for name, ref in (("parent", lambda i: i["parent"]), ("root", lambda i: root(i["id"]))):
                if name == "root" and all(ideas.get(i["parent"], {}).get("parent") is None for i in ideas.values() if i["arm"] == arm): continue
                d = defaultdict(list)
                for i in ideas.values():
                    if i["arm"] != arm or not i.get("parent"): continue
                    r = ref(i)
                    for f in "OCVGF":
                        a, b = sc(i["id"], g, f), sc(r, g, f)
                        if a is not None and b is not None: d[f].append(a - b)
                if not d["O"]: continue
                print(f"   {arm:4s} vs {name:6s} n={len(d['O']):2d} dO {mean(d['O']):+.2f} dC {mean(d['C']):+.2f} dV {mean(d['V']):+.2f} "
                      f"dG {mean(d['G']):+.2f} dF {mean(d['F']):+.2f}  O<0 {sum(x < 0 for x in d['O'])}/{len(d['O'])}  V<0 {sum(x < 0 for x in d['V'])}/{len(d['V'])}")


def main():
    if "--paired" in sys.argv: return paired(sys.argv[1])
    run = sys.argv[1]; pp = sys.argv[sys.argv.index("--prior-prefix") + 1] if "--prior-prefix" in sys.argv else "PV"
    for g, (by_arm, by_tech) in stats(run, pp).items():
        print(f"== {g}")
        print(f"{'arm':10s} {'n':>3s} {'O':>5s} {'C':>5s} {'V':>5s} {'OxV':>6s} {'top3':>6s} {'R':>3s} {'prior%':>7s} {'G':>5s} {'X%':>4s} {'OVG3':>6s} {'F':>5s}")
        for arm, rows in sorted(by_arm.items()):
            top = sorted((r["OV"] for r in rows), reverse=True)[:3]
            print(f"{arm:10s} {len(rows):3d} {mean([r['O'] for r in rows]):5.2f} {mean([r['C'] for r in rows]):5.2f} "
                  f"{mean([r['V'] for r in rows]):5.2f} {mean([r['OV'] for r in rows]):6.1f} {mean(top):6.1f} "
                  f"{sum(r['R'] for r in rows):3d} {100 * mean([r['prior'] for r in rows]):6.0f}% {mean([r['G'] for r in rows]):5.2f} "
                  f"{100 * mean([r['X'] for r in rows]):3.0f}% {mean(sorted((r['OV'] * r['G'] for r in rows), reverse=True)[:3]):6.1f} {mean([r['F'] for r in rows]):5.2f}")
        print("-- by technique (arm:label  n  O  C  V  OxV  prior%  G)")
        for (arm, lab), rows in sorted(by_tech.items(), key=lambda kv: -mean([r["OV"] for r in kv[1]])):
            print(f"   {arm + ':' + lab:24s} {len(rows)} {mean([r['O'] for r in rows]):5.2f} {mean([r['C'] for r in rows]):5.2f} "
                  f"{mean([r['V'] for r in rows]):5.2f} {mean([r['OV'] for r in rows]):6.1f} {100 * mean([r['prior'] for r in rows]):5.0f}% {mean([r['G'] for r in rows]):5.2f}")
        print("-- top 6")
        allr = sorted((r for rows in by_arm.values() for r in rows), key=lambda r: -r["OV"])[:6]
        for r in allr: print(f"   {r['OV']:5.1f} O{r['O']:.1f} V{r['V']:.1f} G{r['G']:.1f} {r['id']:24s} {r['name']}")


if __name__ == "__main__":
    main()
