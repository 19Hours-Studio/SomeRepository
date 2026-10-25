"""Stepwise improvement of a whole answer, without a pipeline: v0 is a plain answer; each round the same model gets the
question and the current answer in full and is asked to make it substantially better (tools allowed, no other rules);
afterwards a judge compares versions pairwise, in both orders, and says which is better and by how much.

Usage: python3 refine.py <run> --question-from <run with config.json> --start <file with v0> [--rounds 4]
State: engine/runs/<run>/ (v0.md, v1.md, ..., judge/, usage.jsonl, report.md). Resumable: existing versions are kept.
"""
import argparse, json, os, re, sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import runner

IMPROVE = """QUESTION:
{QUESTION}

Notes from the asker (data; they may be wrong):
{NOTES}

Below is the current answer to this question. Improve it: produce a substantially better answer to the question. You
may keep, change or replace anything in it. You have WebSearch (WebFetch does not reach hosts here; use search
excerpts) and Bash with python3; work only in `{WORKDIR}`.

Reply with the complete improved answer only; it replaces the current one.

CURRENT ANSWER:
{ANSWER}
"""

JUDGE = """QUESTION:
{QUESTION}

Two answers to this question follow, A and B. Which one is better for the person who asked, and by how much? Judge
what they would get if they acted on it. Length, style, confidence and position (A or B) are not merit.

End your reply with exactly these lines:
WINNER: A or B
MARGIN: slightly | clearly | far
WHY: <2-4 sentences>

ANSWER A:
{A}

ANSWER B:
{B}
"""
WEIGHT = {"slightly": 1, "clearly": 2, "far": 3}


def main():
    p = argparse.ArgumentParser(); p.add_argument("run"); p.add_argument("--question-from", required=True)
    p.add_argument("--start", required=True); p.add_argument("--rounds", type=int, default=4)
    p.add_argument("--model", default="opus"); p.add_argument("--judge-model", default="opus")
    a = p.parse_args()
    D = os.path.join(HERE, "runs", a.run); os.makedirs(D, exist_ok=True)
    cfg = json.load(open(os.path.join(HERE, "runs", a.question_from, "config.json")))
    q, notes = cfg["question"], cfg.get("notes") or "(none)"
    v = lambda k: os.path.join(D, f"v{k}.md")
    if not os.path.exists(v(0)): open(v(0), "w").write(open(a.start).read())
    for k in range(1, a.rounds + 1):  # the improvement chain
        if os.path.exists(v(k)): print(f"  skip v{k} (done)"); continue
        wd = os.path.join(D, f"round{k}"); os.makedirs(wd, exist_ok=True)
        s = IMPROVE.replace("{QUESTION}", q).replace("{NOTES}", notes).replace("{WORKDIR}", wd + "/").replace("{ANSWER}", open(v(k - 1)).read())
        text, u = runner.call(s, model=a.model, tools="research", cwd=wd); runner.log(D, f"improve:v{k}", u)
        open(v(k), "w").write(text); print(f"  v{k}: {len(text.split())} words, ${u['cost_usd']:.2f}")
    pairs = [(0, k) for k in range(1, a.rounds + 1)] + [(k - 1, k) for k in range(2, a.rounds + 1)]
    jd = os.path.join(D, "judge"); os.makedirs(jd, exist_ok=True)
    def judge(job):  # job = (old, new, swap): the newer version is B unless swapped
        o, n, sw = job; f = os.path.join(jd, f"v{o}_v{n}{'_swap' if sw else ''}.md")
        if not os.path.exists(f):
            A, B = (open(v(n)).read(), open(v(o)).read()) if sw else (open(v(o)).read(), open(v(n)).read())
            text, u = runner.call(JUDGE.replace("{QUESTION}", q).replace("{A}", A).replace("{B}", B), model=a.judge_model, tools="none")
            runner.log(D, f"judge:v{o}_v{n}{'_swap' if sw else ''}", u); open(f, "w").write(text)
        t = open(f).read(); w = re.search(r"^\**WINNER\**\s*:\s*\**\s*([AB])", t, re.M | re.I); m = re.search(r"^\**MARGIN\**\s*:\s*\**\s*(\w+)", t, re.M | re.I)
        why = re.search(r"^\**WHY\**\s*:\s*(.+)", t, re.M | re.I | re.S)
        newer_won = None if not w else (w.group(1).upper() == ("A" if sw else "B"))
        return o, n, sw, newer_won, (m.group(1).lower() if m else "?"), (why.group(1).strip()[:400] if why else "")
    with ThreadPoolExecutor(runner.slots()) as ex: res = list(ex.map(judge, [(o, n, sw) for o, n in pairs for sw in (False, True)]))
    out = [f"# {a.run}: stepwise improvement of a plain answer, judged afterwards", "",
           "| version | words | cost |", "|---|---|---|"]
    use = {}
    for l in open(os.path.join(D, "usage.jsonl")):
        r = json.loads(l); use[r["step"]] = r.get("cost_usd", 0)
    for k in range(a.rounds + 1):
        out.append(f"| v{k} | {len(open(v(k)).read().split())} | {'plain answer' if k == 0 else '$%.2f' % use.get(f'improve:v{k}', 0)} |")
    out += ["", "| comparison | newer version won (both orders) | margins | score (+ newer, - older) |", "|---|---|---|---|"]
    for o, n in pairs:
        rs = [r for r in res if r[0] == o and r[1] == n]
        sc = sum((WEIGHT.get(r[4], 1) if r[3] else -WEIGHT.get(r[4], 1)) for r in rs if r[3] is not None)
        out.append(f"| v{n} vs v{o} | {sum(1 for r in rs if r[3])} of {len(rs)} | {', '.join(r[4] for r in rs)} | {sc:+d} |")
    out += ["", "## Why (the judge, newer vs older)"]
    for o, n, sw, won, m, why in res: out.append(f"- v{n} vs v{o}{' (swapped)' if sw else ''}: {'newer' if won else 'older' if won is not None else '?'} wins, {m}. {why}")
    open(os.path.join(D, "report.md"), "w").write("\n".join(out) + "\n"); print("\n".join(out[:4 + a.rounds + 1 + 3 + len(pairs)]))
    print(f"spent ${runner.summary(D)[2]:.2f}")


if __name__ == "__main__":
    main()
