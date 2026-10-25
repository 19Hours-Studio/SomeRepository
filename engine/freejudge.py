"""Free judges against the usual ones. A free judge gets the question, two answers and the files behind them, and
decides on its own how to check (read and run the code, its own calculations, search); the usual judge reads the two
texts with no tools. Each pair is judged in both orders.

A planted pair has a known answer: B is a copy of A whose headline numbers were made better than its own files give,
so the honest original must win.

Usage: python3 freejudge.py <run> --pair NAME QUESTION_RUN A_FILE A_FILES B_FILE B_FILES [--pair ...] [--truth NAME=A]
State: engine/runs/<run>/<pair>/{free,blind}[_swap]/, usage.jsonl, report.md. Resumable.
"""
import argparse, json, os, re, shutil, sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import runner
from refine import JUDGE

FREE = """QUESTION:
{QUESTION}

Two answers to this question are in the current folder: `A.md` and `B.md`. The files behind them (code, data,
outputs) are in `{AF}` for A and in `{BF}` for B.

Find out which one is really better for the person who asked, and by how much. How you check is up to you: read and run
their code, write your own calculations, search for prior art and real figures. You may write files in the current
folder.

End your reply with these lines:
WINNER: A or B
HOW MUCH BETTER: <in your own words>
REAL GAIN A: <the gain over the best current practice that A really supports, or "none">
REAL GAIN B: <the same for B>
"""


def main():
    p = argparse.ArgumentParser(); p.add_argument("run")
    p.add_argument("--pair", nargs=6, action="append", required=True, metavar=("NAME", "QRUN", "A", "AFILES", "B", "BFILES"))
    p.add_argument("--truth", action="append", default=[], help="NAME=A or NAME=B for a planted pair")
    p.add_argument("--model", default="opus")
    a = p.parse_args()
    D = os.path.join(HERE, "runs", a.run); os.makedirs(D, exist_ok=True)
    truth = dict(t.split("=") for t in a.truth)
    pairs = {n: (json.load(open(os.path.join(HERE, "runs", qr, "config.json")))["question"], A, os.path.abspath(af), B, os.path.abspath(bf))
             for n, qr, A, af, B, bf in a.pair}

    def job(j):  # (pair, kind, swap): swapped puts the second answer first
        n, kind, sw = j; q, A, af, B, bf = pairs[n]
        if sw: A, af, B, bf = B, bf, A, af
        wd = os.path.join(D, n, kind + ("_swap" if sw else "")); os.makedirs(wd, exist_ok=True); f = os.path.join(wd, "verdict.md")
        if not os.path.exists(f):
            if kind == "free":
                shutil.copy(A, os.path.join(wd, "A.md")); shutil.copy(B, os.path.join(wd, "B.md"))
                s = FREE.replace("{QUESTION}", q).replace("{AF}", af + "/").replace("{BF}", bf + "/")
                text, u = runner.call(s, model=a.model, tools="Read,Bash,WebSearch", cwd=wd)
            else:
                s = JUDGE.replace("{QUESTION}", q).replace("{A}", open(A).read()).replace("{B}", open(B).read())
                text, u = runner.call(s, model=a.model, tools="none")
            runner.log(D, f"{n}:{kind}{'_swap' if sw else ''}", u); open(f, "w").write(text)
            print(f"  {n} {kind}{' swap' if sw else ''}: ${u['cost_usd']:.2f}", flush=True)
        t = open(f).read(); w = re.findall(r"^\W*WINNER\W*:\W*([AB])\b", t, re.M | re.I)
        win = None if not w else ({"A": "B", "B": "A"}[w[-1].upper()] if sw else w[-1].upper())  # in the pair's own labels
        grab = lambda key: ((re.findall(rf"^\W*{key}\W*:\s*(.+)$", t, re.M | re.I) or ["-"])[-1].strip())
        how = grab("HOW MUCH BETTER") if kind == "free" else grab("MARGIN")
        ga, gb = (grab("REAL GAIN A"), grab("REAL GAIN B")) if kind == "free" else ("-", "-")
        if sw: ga, gb = gb, ga
        return n, kind, sw, win, how, ga, gb

    jobs = [(n, k, sw) for n in pairs for k in ("free", "blind") for sw in (False, True)]
    with ThreadPoolExecutor(runner.slots()) as ex: res = list(ex.map(job, jobs))
    out = [f"# {a.run}: free judges (tools, their own checks) against blind judges (two texts, no tools)", "",
           "| pair | judge | order | winner | known answer | how much | real gain of the first answer | real gain of the second |", "|---|---|---|---|---|---|---|---|"]
    for n, kind, sw, win, how, ga, gb in res:
        tr = truth.get(n, ""); ok = "" if not tr else (" ✓" if win == tr else " ✗")
        out.append(f"| {n} | {kind} | {'swapped' if sw else 'as given'} | {win or '?'}{ok} | {tr or '-'} | {how[:200]} | {ga[:200]} | {gb[:200]} |")
    out += ["", "First answer = A as given on the command line, second = B; winners are in those labels in both orders."]
    open(os.path.join(D, "report.md"), "w").write("\n".join(out) + "\n"); print("\n".join(out))
    print(f"spent ${runner.summary(D)[2]:.2f}")


if __name__ == "__main__":
    main()
