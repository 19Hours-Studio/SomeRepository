"""Architecture discovery loop: engine agents propose code, the harness measures it, a MAP-Elites archive keeps the
best candidate per behaviour cell.  python3 evo.py status | prompt LABEL --method M [--parents a,b] [--n 2]
| ingest LABEL --transcript T | eval CAND [CAND ...] [--seeds 0]"""
import argparse, json, os, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__)); C = os.path.join(HERE, "cands"); R = os.path.join(HERE, "results")
REG = os.path.join(HERE, "registry.json"); TASKS = ["mqar", "copy", "parity", "hop"]

METHODS = {
 "dissolve": "Look at the measured profiles above. Pick the capability that the best candidates fail (or fail at 2x "
   "length). Name the hidden assumption in their computation that makes that capability hard to learn or to extend "
   "to longer inputs - something taken for granted so deeply that nobody writes it down. Dissolve it with ONE move: "
   "drop the assumption, or show the capability is an already-solved problem in disguise, or remove a component "
   "everyone considers essential. The fix must not break what already works.",
 "transfer": "Pick the capability the best candidates fail. Find a DISTANT field (biology, physics, chemistry, "
   "neuroscience, classical algorithms and data structures, signal processing, economics) that solves the same abstract "
   "problem (exact lookup by content, faithful replay of an ordered list, a state that flips, chaining two lookups, "
   "behaving the same on longer inputs) with a specific mechanism. Turn that mechanism into differentiable computation. "
   "Say in the principle what the mapping is and what does not map.",
 "cross": "Take the two parents above, which have complementary measured strengths. Find the ONE shared move that "
   "would give both strengths, and build an offspring that is SIMPLER than either parent, not a stack of both.",
 "count": "Work from first principles. For each task, state privately the minimal computation it needs (what must be "
   "stored, compared, counted or composed, and what must not depend on absolute position so that it works at 2x length). "
   "Then design the smallest mechanism that provides ALL of them at once, and count its parameters and per-step cost so "
   "it fits the budget. Use the measurements to check your reasoning about why current candidates fail.",
 "blind": "Propose architectures that you expect to score well on all four tasks, including at 2x length.",
}


def reg(): return json.load(open(REG)) if os.path.exists(REG) else {}
def save_reg(r): json.dump(r, open(REG, "w"), indent=1)


def results():
    out = {}
    for f in sorted(os.listdir(R)):
        if not f.endswith(".json"): continue
        r = json.load(open(os.path.join(R, f))); name = r["cand"][:-3]
        out.setdefault(name, []).append(r)
    agg = {}
    for name, rs in out.items():
        ok = [r for r in rs if "tasks" in r]
        if not ok: agg[name] = {"fitness": 0.0, "error": rs[0].get("error", "?"), "n": len(rs)}; continue
        t = {k: {m: sum(r["tasks"][k][m] for r in ok) / len(ok) for m in ("id", "ood")} for k in TASKS}
        fit = sum(r["fitness"] for r in ok) / len(ok)
        cell = "".join(str(2 if v["ood"] >= 0.8 else 1 if v["id"] >= 0.8 else 0) for v in t.values())
        agg[name] = {"fitness": round(fit, 4), "tasks": t, "cell": cell, "n": len(ok), "params": ok[0].get("params")}
    return agg


def profile(name, a):
    if "tasks" not in a: return f"{name}: FAILED ({a.get('error', '')[:160]})"
    return (f"{name}: fitness {a['fitness']:.3f}, cell {a['cell']}, " +
            ", ".join(f"{k} {v['id']:.2f}/{v['ood']:.2f}" for k, v in a["tasks"].items()) + f" (ID/2x), {a['params']} params")


def archive_text(agg, rg, top=8):
    elites = {}
    for n, a in agg.items():
        if "cell" in a and (a["cell"] not in elites or a["fitness"] > agg[elites[a["cell"]]]["fitness"]): elites[a["cell"]] = n
    lines = [f"{len(agg)} candidates measured; {len(elites)} distinct profile cells filled: {', '.join(sorted(elites))}.",
             "Best per task (ID / 2x): " + "; ".join(
                 f"{t} {max((a['tasks'][t]['id'] for a in agg.values() if 'tasks' in a), default=0):.2f} / "
                 f"{max((a['tasks'][t]['ood'] for a in agg.values() if 'tasks' in a), default=0):.2f}" for t in TASKS),
             "Top candidates (principle -> measurement):"]
    for n in sorted(agg, key=lambda n: -agg[n]["fitness"])[:top]:
        lines.append(f"- {profile(n, agg[n])}. PRINCIPLE: {rg.get(n, {}).get('principle', 'known-family seed')}")
    fails = [n for n in agg if "error" in agg[n]]
    if fails: lines.append("Failed to run: " + "; ".join(f"{n} ({agg[n]['error'][:80]})" for n in fails[-6:]))
    return "\n".join(lines)


def cmd_status(a):
    agg, rg = results(), reg(); print(archive_text(agg, rg, top=30))


def cmd_prompt(a):
    agg, rg = results(), reg(); s = open(os.path.join(HERE, "mutate.txt")).read()
    s = s.replace("{KNOWN}", open(os.path.join(HERE, "known_families.txt")).read().strip())
    if a.method == "blind":
        s = s.replace("{ARCHIVE}", "(nothing yet - you work blind, as a plain idea generator would)").replace("{PARENTS}", "")
    else:
        s = s.replace("{ARCHIVE}", archive_text(agg, rg))
        par = []
        for p in (a.parents.split(",") if a.parents else []):
            par += [f"PARENT {p} - {profile(p, agg[p])}", "```python", open(os.path.join(C, p + ".py")).read().strip(), "```"]
        s = s.replace("{PARENTS}", ("PARENTS (their code; build on them or against them):\n" + "\n".join(par)) if par else "")
    s = s.replace("{METHOD}", METHODS[a.method]).replace("{N}", str(a.n))
    p = os.path.join(HERE, "prompts", a.label + ".txt"); os.makedirs(os.path.dirname(p), exist_ok=True); open(p, "w").write(s)
    rg.setdefault("_prompts", {})[a.label] = {"method": a.method, "parents": a.parents, "round": a.round}; save_reg(rg); print(p)


sys.path.insert(0, os.path.join(HERE, "..", ".."))
from ce import transcript_text  # final reply incl. SubagentHandback


def cmd_ingest(a):
    text = transcript_text(a.transcript) if a.transcript else open(a.file).read()
    rg = reg(); meta = rg.get("_prompts", {}).get(a.label, {}); names = []
    for k, (body) in enumerate(re.split(r"=== CANDIDATE \d+ ===", text)[1:], 1):
        pr = re.search(r"PRINCIPLE:\s*(.+)", body); code = re.search(r"```python\n(.*?)```", body, re.S)
        if not code: print(f"WARNING {a.label}#{k}: no code block"); continue
        name = f"{a.label}_{k}"; open(os.path.join(C, name + ".py"), "w").write(code.group(1))
        rg[name] = {"principle": pr.group(1).strip() if pr else "", **meta}; names.append(name)
    save_reg(rg); print(" ".join(names))


def run_one(job):
    name, seed = job; out = os.path.join(R, f"{name}.s{seed}.json")
    if os.path.exists(out): return name
    env = dict(os.environ, THREADS="1")
    try:
        subprocess.run([sys.executable, "-I", os.path.join(HERE, "harness.py"), os.path.join(C, name + ".py"), "--out", out,
                        "--seed", str(seed)], env=env, timeout=600, capture_output=True)
    except subprocess.TimeoutExpired:
        json.dump({"cand": name + ".py", "seed": seed, "fitness": 0.0, "error": "TimeoutExpired: >600s wall"}, open(out, "w"))
    if not os.path.exists(out):
        json.dump({"cand": name + ".py", "seed": seed, "fitness": 0.0, "error": "harness crashed"}, open(out, "w"))
    return name


def cmd_eval(a):
    jobs = [(n, s) for n in a.cands for s in map(int, a.seeds.split(","))]
    with ThreadPoolExecutor(4) as ex: list(ex.map(run_one, jobs))
    agg = results()
    for n in a.cands: print(profile(n, agg[n]))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("status")
    x = sp.add_parser("prompt"); x.add_argument("label"); x.add_argument("--method", required=True, choices=list(METHODS))
    x.add_argument("--parents", default=""); x.add_argument("--n", type=int, default=2); x.add_argument("--round", type=int, default=0)
    x = sp.add_parser("ingest"); x.add_argument("label"); x.add_argument("--transcript"); x.add_argument("--file")
    x = sp.add_parser("eval"); x.add_argument("cands", nargs="+"); x.add_argument("--seeds", default="0")
    a = ap.parse_args(); globals()["cmd_" + a.cmd](a)
