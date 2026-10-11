"""Статистика A/B по плечам для прогонов финального судейства движка (ab1_final15, ab1_final16, ...).

Использование: python3 research/stage1-creativity/ab_stats.py RUN [--prior-prefix PV]
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
                   "name": ideas[iid]["name"]}
            arm = ideas[iid]["arm"]; by_arm[arm].append(row)
            by_tech[(arm, ideas[iid]["label"].split(":")[-1])].append(row)
        out[g] = (by_arm, by_tech)
    return out


def mean(xs): return sum(xs) / len(xs) if xs else float("nan")


def main():
    run = sys.argv[1]; pp = sys.argv[sys.argv.index("--prior-prefix") + 1] if "--prior-prefix" in sys.argv else "PV"
    for g, (by_arm, by_tech) in stats(run, pp).items():
        print(f"== {g}")
        print(f"{'arm':10s} {'n':>3s} {'O':>5s} {'C':>5s} {'V':>5s} {'OxV':>6s} {'top3':>6s} {'R':>3s} {'prior%':>7s}")
        for arm, rows in sorted(by_arm.items()):
            top = sorted((r["OV"] for r in rows), reverse=True)[:3]
            print(f"{arm:10s} {len(rows):3d} {mean([r['O'] for r in rows]):5.2f} {mean([r['C'] for r in rows]):5.2f} "
                  f"{mean([r['V'] for r in rows]):5.2f} {mean([r['OV'] for r in rows]):6.1f} {mean(top):6.1f} "
                  f"{sum(r['R'] for r in rows):3d} {100 * mean([r['prior'] for r in rows]):6.0f}%")
        print("-- by technique (arm:label  n  O  C  V  OxV  prior%)")
        for (arm, lab), rows in sorted(by_tech.items(), key=lambda kv: -mean([r["OV"] for r in kv[1]])):
            print(f"   {arm + ':' + lab:24s} {len(rows)} {mean([r['O'] for r in rows]):5.2f} {mean([r['C'] for r in rows]):5.2f} "
                  f"{mean([r['V'] for r in rows]):5.2f} {mean([r['OV'] for r in rows]):6.1f} {100 * mean([r['prior'] for r in rows]):5.0f}%")
        print("-- top 6")
        allr = sorted((r for rows in by_arm.values() for r in rows), key=lambda r: -r["OV"])[:6]
        for r in allr: print(f"   {r['OV']:5.1f} O{r['O']:.1f} V{r['V']:.1f} {r['id']:24s} {r['name']}")


if __name__ == "__main__":
    main()
