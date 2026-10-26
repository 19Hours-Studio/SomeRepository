"""Scorer for the code bench: the answer to each task is a program, and the score comes from running it.

Each program runs on one core (taskset -c 0), with BLAS threads at 1, under a time limit, from its own folder. Only the
standard library and numpy may be imported; compilers, ctypes, subprocesses and parallelism are refused before the run.

Usage: python3 score.py <task> <solution dir> [--runs 2]   -> prints one JSON line: {"task", "ok", "score", ...}
       python3 score.py <task> --baseline                  -> measures the baseline (speed tasks store its time)
Tasks: ca, queens, primesum (speed: score = baseline time / program time), compress (score = xz bytes / (compressed +
xz'd decoder source) bytes), labs (score = merit factor of the sequence found within the time limit).
"""
import ast, hashlib, json, lzma, os, shutil, subprocess, sys, tempfile, time

HERE = os.path.dirname(os.path.abspath(__file__)); TASKS = os.path.join(HERE, "tasks")
FORBIDDEN = {"ctypes", "cffi", "subprocess", "multiprocessing", "concurrent", "threading", "_thread", "scipy", "numba",
             "cython", "pyximport", "setuptools", "distutils", "importlib", "sysconfig", "pty", "signal", "socket"}
BAD_CALLS = ("os.system", "os.popen", "os.exec", "os.fork", "os.spawn", "os.posix_spawn", "__import__", "exec(", "eval(")
LIMIT = {"ca": 300, "queens": 300, "primesum": 300, "compress": 120, "labs": 60}


ENTRY = {"compress": ["compress.py", "decompress.py"]}


def program_files(task, d):
    """The entry files and the local modules they import (test and helper scripts in the folder are not checked)."""
    todo, seen = list(ENTRY.get(task, ["solution.py"])), []
    while todo:
        f = todo.pop()
        if f in seen or not os.path.exists(os.path.join(d, f)): continue
        seen.append(f)
        for node in ast.walk(ast.parse(open(os.path.join(d, f)).read())):
            mods = [a.name for a in node.names] if isinstance(node, ast.Import) else [node.module or ""] if isinstance(node, ast.ImportFrom) else []
            todo += [m.split(".")[0] + ".py" for m in mods if os.path.exists(os.path.join(d, m.split(".")[0] + ".py"))]
    return seen


def check_source(task, d):
    for f in program_files(task, d):
        src = open(os.path.join(d, f)).read()
        for node in ast.walk(ast.parse(src)):
            mods = [a.name for a in node.names] if isinstance(node, ast.Import) else [node.module or ""] if isinstance(node, ast.ImportFrom) else []
            for m in mods:
                if m.split(".")[0] in FORBIDDEN: return f"{f}: import {m} is not allowed"
        for b in BAD_CALLS:
            if b in src: return f"{f}: {b} is not allowed"
    for root, _, fs in os.walk(d):
        for f in fs:
            if f.endswith((".so", ".pyx", ".dll", ".dylib")): return f"{f}: native code is not allowed"
    return None


def run(cmd, cwd, limit, stdin=None):
    env = dict(os.environ, OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", MKL_NUM_THREADS="1", PYTHONHASHSEED="0")
    t = time.perf_counter()
    try:
        p = subprocess.run(["taskset", "-c", os.environ.get("SCORE_CORE", "0"), sys.executable, "-I"] + cmd, cwd=cwd, env=env, capture_output=True,
                           timeout=limit, stdin=stdin)
    except subprocess.TimeoutExpired: return None, limit, "time limit"
    dt = time.perf_counter() - t
    return p, dt, (None if p.returncode == 0 else p.stderr.decode(errors="replace")[-600:])


def expected(task):
    return json.load(open(os.path.join(TASKS, task, "expected.json")))


def score_speed(task, d, runs):
    exp = expected(task); best, out = None, None
    for f in program_files(task, d):
        if exp["answer"] in open(os.path.join(d, f), errors="replace").read(): return {"ok": False, "error": f"{f} contains the answer"}
    for _ in range(runs):
        p, dt, err = run(["solution.py"], d, LIMIT[task])
        if err: return {"ok": False, "error": err}
        out = p.stdout.decode().strip().split()[-1] if p.stdout.strip() else ""
        if out != exp["answer"]: return {"ok": False, "error": f"wrong answer {out[:80]!r}"}
        best = dt if best is None else min(best, dt)
    return {"ok": True, "seconds": round(best, 3), "score": round(exp["baseline_seconds"] / best, 2)}


def score_compress(d, runs):
    data = os.path.join(TASKS, "compress", "data.log")
    if not os.path.exists(data): subprocess.run([sys.executable, os.path.join(TASKS, "compress", "gen.py")], check=True)
    raw = open(data, "rb").read(); xz = len(lzma.compress(raw, preset=9 | lzma.PRESET_EXTREME))
    with tempfile.TemporaryDirectory() as w:
        for f in ("compress.py", "decompress.py"):
            if not os.path.exists(os.path.join(d, f)): return {"ok": False, "error": f"{f} missing"}
        shutil.copytree(d, os.path.join(w, "sol")); s = os.path.join(w, "sol")
        p, dt1, err = run(["compress.py"], s, LIMIT["compress"], stdin=open(data, "rb"))
        if err: return {"ok": False, "error": "compress: " + err}
        open(os.path.join(w, "packed"), "wb").write(p.stdout)
        os.makedirs(os.path.join(w, "dec")); shutil.copy(os.path.join(d, "decompress.py"), os.path.join(w, "dec"))
        q, dt2, err = run(["decompress.py"], os.path.join(w, "dec"), LIMIT["compress"], stdin=open(os.path.join(w, "packed"), "rb"))
        if err: return {"ok": False, "error": "decompress: " + err}
        if q.stdout != raw: return {"ok": False, "error": "decompressed output differs from the input"}
        dec = len(lzma.compress(open(os.path.join(d, "decompress.py"), "rb").read(), preset=9))
        total = len(p.stdout) + dec
        return {"ok": True, "bytes": total, "packed": len(p.stdout), "decoder_xz": dec, "xz_bytes": xz,
                "seconds": [round(dt1, 1), round(dt2, 1)], "score": round(xz / total, 3)}


LABS_N = (127, 139)  # the second N is not told to the solver


def score_labs(d, runs):
    vals = []
    for n in LABS_N:
        p, dt, err = run(["solution.py", str(n)], d, LIMIT["labs"] + 5)
        if err: return {"ok": False, "error": err}
        s = (p.stdout.decode().strip().split() or [""])[-1]
        if len(s) != n or set(s) - set("+-"): return {"ok": False, "error": f"need {n} characters of + and -, got {s[:60]!r}"}
        x = [1 if c == "+" else -1 for c in s]
        e = sum(sum(x[i] * x[i + k] for i in range(n - k)) ** 2 for k in range(1, n))
        vals.append(n * n / (2 * e))
    return {"ok": True, "merit": [round(v, 3) for v in vals], "score": round(sum(vals) / len(vals), 3)}


def main():
    task = sys.argv[1]; runs = int(sys.argv[sys.argv.index("--runs") + 1]) if "--runs" in sys.argv else 2
    if "--baseline" in sys.argv:
        d = os.path.join(TASKS, task, "baseline")
    else:
        d = os.path.abspath(sys.argv[2])
    err = check_source(task, d)
    if err: print(json.dumps({"task": task, "ok": False, "error": err})); return
    if task == "compress": r = score_compress(d, runs)
    elif task == "labs": r = score_labs(d, runs)
    elif "--baseline" in sys.argv:  # measure the baseline and store its answer and time
        p, dt, e = run(["solution.py"], d, 3600)
        if e: sys.exit(e)
        ans = p.stdout.decode().strip().split()[-1]; f = os.path.join(TASKS, task, "expected.json")
        json.dump({"answer": ans, "baseline_seconds": round(dt, 2)}, open(f, "w")); r = {"ok": True, "answer": ans, "seconds": round(dt, 2), "score": 1.0}
    else: r = score_speed(task, d, runs)
    print(json.dumps({"task": task, **r}))


if __name__ == "__main__":
    main()
