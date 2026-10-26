"""Model calls for the engine: headless Claude Code (`claude -p`) with per-step model, tools and budget, and a usage
log per run (tokens and cost from the CLI's JSON output).

Why: a Claude Code subagent costs ~90-230k tokens even for a tool-free generator (system prompt, tool schemas, tool
loop). A headless call with --tools "" costs ~0.7k tokens of overhead, so generators and judges run ~100x cheaper;
only research, repair and review steps need tools.
Set CE_FAKE_LLM=<file> to return that file's text instead of calling a model (tests, dry runs).
"""
import fcntl, json, os, subprocess, time

TOOL_SETS = {"none": "", "research": "WebSearch,Bash,Read,Write", "write": "Read,Write,Bash"}


SLOTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".slots")


def slots():
    return max(1, int(os.environ.get("CE_SLOTS", "8")))


def slot():
    """v5.2: at most CE_SLOTS (default 8; `run --slots`) model calls at once across every engine process on this machine,
    however many parts of a split question run in parallel. Returns the held lock file."""
    n = slots(); os.makedirs(SLOTS, exist_ok=True)
    while True:
        for k in range(n):
            f = open(os.path.join(SLOTS, f"{k}.lock"), "w")
            try:
                fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB); return f
            except BlockingIOError:
                f.close()
        time.sleep(2)


def call(prompt, model="opus", tools="none", cwd=None, effort=None, budget_usd=None, timeout=7200):
    """Run one step; returns (text, usage dict). tools: a TOOL_SETS key or a comma list of tool names."""
    tl = TOOL_SETS.get(tools, tools)
    fake = os.environ.get("CE_FAKE_LLM")
    if fake:
        return open(fake).read(), {"model": model, "tools": tl, "tokens": 0, "cost_usd": 0.0, "seconds": 0.0, "fake": True}
    cmd = ["claude", "-p", "--output-format", "json", "--no-session-persistence", "--model", model, "--tools", tl]
    if os.environ.get("CE_CPUS"): cmd = ["taskset", "-c", os.environ["CE_CPUS"]] + cmd  # bench: keep a core free for timing
    if tl: cmd += ["--allowedTools", tl]
    if effort: cmd += ["--effort", effort]
    if budget_usd: cmd += ["--max-budget-usd", str(budget_usd)]
    lock = slot(); t0 = time.time()
    try:
        p = subprocess.run(cmd, input=prompt, capture_output=True, text=True, cwd=cwd, timeout=timeout)
    finally:
        lock.close()
    try:
        d = json.loads(p.stdout)
    except json.JSONDecodeError:
        raise RuntimeError(f"claude -p failed (exit {p.returncode}): {p.stderr[-500:] or p.stdout[-500:]}")
    if d.get("is_error"): raise RuntimeError(f"claude -p error: {d.get('result')}")
    u = d.get("usage", {})
    tok = sum(u.get(k, 0) for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens"))
    return d.get("result", ""), {"model": model, "tools": tl, "tokens": tok, "output_tokens": u.get("output_tokens", 0),
                                 "cache_read": u.get("cache_read_input_tokens", 0), "fresh_input": u.get("input_tokens", 0) + u.get("cache_creation_input_tokens", 0),
                                 "cost_usd": d.get("total_cost_usd", 0.0), "turns": d.get("num_turns"),
                                 "seconds": round(time.time() - t0, 1)}


def log(run_dir, step, usage):
    """Append one step's usage to <run>/usage.jsonl."""
    with open(os.path.join(run_dir, "usage.jsonl"), "a") as f:
        f.write(json.dumps({"step": step, "time": time.strftime("%Y-%m-%d %H:%M:%S"), **usage}) + "\n")


def summary(run_dir):
    """Rows (step, model, tools, tokens, cost) and totals from <run>/usage.jsonl."""
    f = os.path.join(run_dir, "usage.jsonl")
    rows = [json.loads(l) for l in open(f)] if os.path.exists(f) else []
    return rows, sum(r.get("tokens", 0) for r in rows), sum(r.get("cost_usd", 0.0) for r in rows)
