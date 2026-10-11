"""Cross-run analysis of the engine (no agents): technique leaderboard across questions, gen2 vs gen1,
novelty-value trade-off and recurring judge critiques. Usage: python3 research/stage1-creativity/cross_run.py"""
import glob, json, os, re, statistics as st
from collections import defaultdict

R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "engine", "runs")
RUNS = ["final", "meta1", "ab1_v1", "ab1_v2", "ab1_v15", "ab1_v16", "arch_llm", "arch_spec"]


def agg(scores, iid):
    s = scores.get(iid, {})
    if not s: return None
    last = sorted({k.split(":")[0] for k in s})[-1]; js = [v for k, v in s.items() if k.startswith(last + ":")]
    O = st.mean(j["O"] for j in js); V = st.mean(j["V"] for j in js); C = st.mean(j["C"] for j in js)
    return O, C, V, O * V


def tech(label):
    t = label.split(":")[-1]
    t = re.sub(r"^g\d_", "", t); return re.sub(r"\d+$", "", t) if t not in ("core2",) else "core"


def main():
    board = defaultdict(list); gen = defaultdict(list); ov = []
    for run in RUNS:
        ideas = json.load(open(os.path.join(R, run, "ideas.json"))); sc = json.load(open(os.path.join(R, run, "scores.json")))
        rows = [(i, agg(sc, i["id"])) for i in ideas]; rows = [(i, a) for i, a in rows if a]
        g1 = [(i, a) for i, a in rows if i["gen"] == 1]
        if not g1: continue
        m = st.mean(a[3] for _, a in g1)
        by = defaultdict(list)
        for i, a in g1: by[tech(i["label"])].append(a[3])
        ranked = sorted(by, key=lambda t: -st.mean(by[t]))
        for k, t in enumerate(ranked): board[t].append((run, round(st.mean(by[t]) / m, 2), k + 1, len(ranked)))
        g2 = [a[3] for i, a in rows if i["gen"] == 2]
        if g2: gen["gen2/gen1"].append((run, round(st.mean(g2) / m, 2)))
        ctrl = [a for i, a in rows if i["arm"] == "control"]; eng = [a for i, a in rows if i["gen"] >= 1]
        if ctrl and eng:
            ov.append((run, round(st.mean(a[0] for a in eng) - st.mean(a[0] for a in ctrl), 2), round(st.mean(a[2] for a in eng) - st.mean(a[2] for a in ctrl), 2)))
    print("TECHNIQUE LEADERBOARD (gen1 O*V / run gen1 mean; rank of n)")
    for t, v in sorted(board.items(), key=lambda kv: -st.mean(x[1] for x in kv[1])):
        print(f"  {t:12s} mean {st.mean(x[1] for x in v):.2f}  " + "  ".join(f"{r}:{x}({k}/{n})" for r, x, k, n in v))
    print("GEN2 / GEN1 O*V:", gen["gen2/gen1"])
    print("ENGINE - CONTROL (dO, dV) where the control was judged in the same set:", ov)
    print("\nJUDGE NOTES")
    for f in sorted(glob.glob(os.path.join(R, "*", "sets", "*", "judge_*.md"))):
        txt = open(f).read(); n = re.search(r"NOTE:?\s*(.+)", txt, re.S)
        if n: print(f"- [{f.split('runs/')[1].split('/sets')[0]}/{os.path.basename(os.path.dirname(f))}] " + " ".join(n.group(1).split())[:400])


if __name__ == "__main__":
    main()
