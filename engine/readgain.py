"""A fresh reader's real gain for any answers: a free reader (files and tools, its own checks, no history of the chain)
reads each answer once. Used to check a chain's in-loop critics from outside (debate_foldcrease: critics 8-250x ->
50-800x, fresh readers "none").

Usage: python3 readgain.py <run> --question-from <run> --answer NAME FILE FILES [--answer ...]
State: engine/runs/<run>/<NAME>/ and <NAME>.md, usage.jsonl, report.md. Resumable.
"""
import argparse, json, os, re, shutil, sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import runner
from refine import FREE_GAIN


def main():
    p = argparse.ArgumentParser(); p.add_argument("run"); p.add_argument("--question-from", required=True)
    p.add_argument("--answer", nargs=3, action="append", required=True, metavar=("NAME", "FILE", "FILES")); p.add_argument("--model", default="opus")
    a = p.parse_args()
    D = os.path.join(HERE, "runs", a.run); os.makedirs(D, exist_ok=True)
    q = json.load(open(os.path.join(HERE, "runs", a.question_from, "config.json")))["question"]

    def read(x):
        n, f, ff = x; out = os.path.join(D, f"{n}.md")
        if not os.path.exists(out):
            wd = os.path.join(D, n); os.makedirs(wd, exist_ok=True); shutil.copy(f, os.path.join(wd, "answer.md"))
            text, u = runner.call(FREE_GAIN.replace("{QUESTION}", q).replace("{AF}", os.path.abspath(ff) + "/"), model=a.model, tools="Read,Bash,WebSearch", cwd=wd)
            runner.log(D, n, u); open(out, "w").write(text); print(f"  {n}: ${u['cost_usd']:.2f}", flush=True)
        return n, (re.findall(r"^\W*HONEST GAIN\W*:\s*(.+)$", open(out).read(), re.M | re.I) or ["?"])[-1].strip()

    with ThreadPoolExecutor(runner.slots()) as ex: res = list(ex.map(read, a.answer))
    out = [f"# {a.run}: real gain read by fresh free readers", "", "| answer | real gain |", "|---|---|"] + [f"| {n} | {g} |" for n, g in res]
    open(os.path.join(D, "report.md"), "w").write("\n".join(out) + "\n"); print("\n".join(out)); print(f"spent ${runner.summary(D)[2]:.2f}")


if __name__ == "__main__":
    main()
