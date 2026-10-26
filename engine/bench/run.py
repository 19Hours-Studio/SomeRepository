"""Code bench: plain Claude against the climbing harness, with every score measured by running the program
(bench/score.py), so no judge has to be persuaded.

plain: one Claude Code call per attempt gets the task folder (TASK.md, baseline, the scorer's command) and writes its
solution; --n attempts per task give a best-of-n control.
climb: starts from a solution (a plain attempt, or the baseline) and runs rounds; each round K candidates start from a
copy of the current best, each with a different move, and see every earlier attempt with its official score; the
official scorer measures them one after another on a core the agents do not use, and the best replaces the current
one if it scores at least 3% higher.
score: official scores of every attempt in a run, one after another (run it on a quiet machine).

Usage: python3 run.py plain <run> [--tasks ca,queens,...] [--n 1]
       python3 run.py climb <run> --start <plain runs, comma-separated> [--tasks ...] [--rounds 3] [--k 4]
       python3 run.py score <run>
State: engine/bench/runs/<run>/<task>/<attempt>/ (the agent's folder, note.md, score.json), usage.jsonl, report.md.
"""
import argparse, fcntl, json, os, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import runner

TASKS = ["ca", "queens17", "primesum13", "compress", "labs"]  # queens and primesum (plain1 run) were too small: plain Claude hit Python start-up
SCORE = os.path.join(HERE, "score.py")
FILES = {"compress": ["compress.py", "decompress.py"], "heat": ["design.txt"], "optics": ["design.json"]}
os.environ.setdefault("CE_CPUS", "1-3"); os.environ.setdefault("SCORE_CORE", "1")  # agents and their self-checks; core 0 is for official scores

PLAIN = """Your task is in `TASK.md` in the current folder. Solve it as well as you can; only the score counts. You have
Bash with python3 and numpy, Read, Write and WebSearch. Work only in the current folder.
When you are done, reply with a short note: your approach and your self-measured score."""

MOVES = {
    "tune": "keep the current approach and push it much further: profile it, find where the time (or the loss) goes, and remove it.",
    "algorithm": "replace the core idea - the mechanism, the design concept, the algorithm or the representation - with a "
                 "fundamentally better one; the answer must stay valid.",
    "research": "search for the best known methods and designs for this problem (papers, patents, records, known tricks) and "
                "build the strongest one that fits the rules, or go beyond it.",
    "fresh": "write a new solution from scratch with a different approach from the current one, aiming to beat its score by a large factor.",
}

CLIMB = """Your task is in `TASK.md` in the current folder. The current best solution is already in this folder; its
official score is {SCORE}. Your move: {MOVE}

Attempts so far (official scores; 0 = wrong or broke the rules):
{HISTORY}

Only the score counts. Work only in the current folder and leave your complete solution in it ({FILES}). You have Bash
with python3 and numpy, Read, Write and WebSearch.
When you are done, reply with a short note: what you changed and your self-measured score."""


def prepare(task, dst, src=None):
    """A working folder: TASK.md with the scorer's command, the baseline, the data; and src's solution files."""
    os.makedirs(dst, exist_ok=True); T = os.path.join(HERE, "tasks", task)
    open(os.path.join(dst, "TASK.md"), "w").write(open(os.path.join(T, "TASK.md")).read().replace("SCORE", SCORE))
    if not os.path.exists(os.path.join(dst, "baseline")): shutil.copytree(os.path.join(T, "baseline"), os.path.join(dst, "baseline"))
    if task == "compress" and not os.path.exists(os.path.join(dst, "data.log")): shutil.copy(os.path.join(T, "data.log"), dst)
    if os.path.exists(os.path.join(T, "sim.py")): shutil.copy(os.path.join(T, "sim.py"), dst)
    if src:
        for f in os.listdir(src):
            if f in ("TASK.md", "baseline", "data.log", "note.md", "score.json", "__pycache__"): continue
            s, t = os.path.join(src, f), os.path.join(dst, f)
            if os.path.isdir(s): shutil.copytree(s, t, dirs_exist_ok=True)
            elif os.path.getsize(s) < 4_000_000: shutil.copy(s, t)


def official(task, d, cache=True):
    """The official score, measured on core 0 and cached in d/score.json."""
    f = os.path.join(d, "score.json")
    if cache and os.path.exists(f): return json.load(open(f))
    env = dict(os.environ, SCORE_CORE="0")
    with open(os.path.join(HERE, ".scoring.lock"), "w") as lk:  # one official measurement at a time, across processes
        fcntl.flock(lk, fcntl.LOCK_EX); p = subprocess.run([sys.executable, SCORE, task, d], capture_output=True, text=True, env=env)
    try: r = json.loads(p.stdout.strip().splitlines()[-1])
    except Exception: r = {"task": task, "ok": False, "error": (p.stderr or p.stdout)[-400:]}
    r["score"] = r.get("score", 0) if r.get("ok") else 0; json.dump(r, open(f, "w")); return r


def agent(D, d, prompt, step):
    """One Claude Code call in folder d; its reply goes to d/note.md. Returns False if it failed or timed out."""
    if os.path.exists(os.path.join(d, "note.md")): return True
    try: text, u = runner.call(prompt, model="opus", tools="research", cwd=d)
    except Exception as e:
        print(f"  {step}: failed ({str(e)[:120]})", flush=True); open(os.path.join(d, "note.md"), "w").write(f"(failed: {e})\n"); return False
    runner.log(D, step, u); open(os.path.join(d, "note.md"), "w").write(text)
    print(f"  {step}: ${u['cost_usd']:.2f}, {u['seconds']:.0f} s", flush=True); return True


def plain(a, D):
    jobs = [(t, i) for t in a.tasks for i in range(1, a.n + 1)]
    def one(j):
        t, i = j; d = os.path.join(D, t, f"plain{i}"); prepare(t, d); agent(D, d, PLAIN, f"{t}:plain{i}")
    with ThreadPoolExecutor(len(jobs)) as ex: list(ex.map(one, jobs))
    for t, i in jobs: print(f"  {t} plain{i}: {official(t, os.path.join(D, t, f'plain{i}'))}", flush=True)


def climb(a, D):
    def task_climb(t):
        tries = [os.path.join(os.path.dirname(D), s, t, f) for s in (a.start or "").split(",") if os.path.isdir(os.path.join(os.path.dirname(D), s, t))
                 for f in os.listdir(os.path.join(os.path.dirname(D), s, t)) if f.startswith("plain")]
        start = max(tries, key=lambda d: official(t, d)["score"]) if tries else ""  # the best plain attempt
        cur = os.path.join(D, t, "start"); prepare(t, cur, start or None)
        if not start:  # no plain attempt: start from the baseline
            for f in os.listdir(os.path.join(cur, "baseline")): shutil.copy(os.path.join(cur, "baseline", f), cur)
        best = official(t, cur)["score"]; hist = [f"- start ({'the best plain attempt' if start else 'baseline'}): {best}"]
        for r in range(1, a.rounds + 1):
            moves = list(MOVES)[:a.k]
            def write(m):
                d = os.path.join(D, t, f"r{r}_{m}"); prepare(t, d, cur)
                s = CLIMB.replace("{SCORE}", str(best)).replace("{MOVE}", MOVES[m]).replace("{HISTORY}", "\n".join(hist))
                s = s.replace("{FILES}", ", ".join(FILES.get(t, ["solution.py"]))); agent(D, d, s, f"{t}:r{r}_{m}"); return d
            with ThreadPoolExecutor(len(moves)) as ex: ds = list(ex.map(write, moves))
            res = [(m, d, official(t, d)) for m, d in zip(moves, ds)]  # one after another, on core 0
            for m, d, sc in res:
                note = open(os.path.join(d, "note.md")).read().strip().replace("\n", " ")[:300]
                hist.append(f"- round {r}, {m}: {sc['score']}" + (f" ({sc.get('error', '')[:120]})" if not sc.get("ok") else "") + f" - {note}")
                print(f"  {t} r{r} {m}: {sc['score']}", flush=True)
            m, d, sc = max(res, key=lambda x: x[2]["score"])
            if sc["score"] >= best * 1.03: cur, best = d, sc["score"]; print(f"  {t} round {r}: {m} -> {best}", flush=True)
            else: print(f"  {t} round {r}: kept {best}", flush=True)
        json.dump({"best": os.path.relpath(cur, D), "score": best, "history": hist}, open(os.path.join(D, t, "climb.json"), "w"), indent=1)
    with ThreadPoolExecutor(len(a.tasks)) as ex: list(ex.map(task_climb, a.tasks))


def report(D):
    out = [f"# {os.path.basename(D)}: official scores (measured by running the programs)", "", "| task | attempt | score | detail |", "|---|---|---|---|"]
    for t in sorted(os.listdir(D)):
        if not os.path.isdir(os.path.join(D, t)): continue
        for at in sorted(os.listdir(os.path.join(D, t))):
            d = os.path.join(D, t, at)
            if not os.path.isdir(d): continue
            r = official(t, d); det = {k: v for k, v in r.items() if k not in ("task", "ok", "score")}
            out.append(f"| {t} | {at} | {r['score']} | {json.dumps(det)[:160]} |")
    use = [json.loads(l) for l in open(os.path.join(D, "usage.jsonl"))] if os.path.exists(os.path.join(D, "usage.jsonl")) else []
    out += ["", f"Model calls: {len(use)}, cost ${sum(u.get('cost_usd', 0) for u in use):.2f}"]
    open(os.path.join(D, "report.md"), "w").write("\n".join(out) + "\n"); print("\n".join(out))


def main():
    p = argparse.ArgumentParser(); p.add_argument("mode", choices=["plain", "climb", "score"]); p.add_argument("run")
    p.add_argument("--tasks", default=",".join(TASKS)); p.add_argument("--n", type=int, default=1)
    p.add_argument("--rounds", type=int, default=3); p.add_argument("--k", type=int, default=4); p.add_argument("--start")
    a = p.parse_args(); a.tasks = a.tasks.split(","); D = os.path.join(HERE, "runs", a.run); os.makedirs(D, exist_ok=True)
    if a.mode == "plain": plain(a, D)
    elif a.mode == "climb": climb(a, D)
    report(D)


if __name__ == "__main__":
    main()
