# Round-3: replay REAL agent trajectories instead of synthetic sessions.
# Data: 441 mini-SWE-agent v2.4.2 + gemini-3-5-flash trajectories on SWE-bench Verified
#   (github.com/john-b-yang/20260901_mini-v2.4.2_gemini-3-5-flash, trajs/*.traj.json), with real per-request
#   usage (prompt_tokens, completion_tokens, reasoning_tokens) and timestamps; plus one claude-opus-4-6
#   trajectory with real cache fields (SWE-bench/experiments analysis/test_data/claude-4-6-opus.json).
# Prices in units of base input: Anthropic r=0.1 read, w=1.25 write (5m), o=5 output.
# Usage: python3 -I trace4.py <trajs_dir> <claude_json>
import json, glob, re, sys, statistics as st, collections
R, W, O = 0.10, 1.25, 5.0
TOK0 = re.compile(r"[A-Za-z_][A-Za-z0-9_]{3,}|\d{2,}")
class _T:  # identifier components (paths/dotted names split), so a.b.ddl_references matches ddl_references.py
    @staticmethod
    def findall(x): return TOK0.findall(x)
TOK = _T()
READONLY = re.compile(r"^\s*(cd [^;&|]+(&&|;)\s*)?(grep|rg|find|cat|ls|head|tail|nl|wc|sed -n|awk|git (log|show|diff|status|grep|blame)|python3? -c|tree|file|stat|which)\b")
WRITES = re.compile(r"(>|git (checkout|reset|stash|commit|add)|sed -i|tee |\bpatch\b|git apply|\bmv\b|\bcp\b|\brm\b|pip install|cat <<|EOF|touch|mkdir|\.write)")

def load(path):
    d = json.load(open(path)); msgs = d["messages"]; steps = []; ctx_text = ""
    for i, m in enumerate(msgs):
        if m["role"] != "assistant": continue
        u = m["extra"]["response"]["usage"]
        out = (u.get("completion_tokens") or 0) + ((u.get("completion_tokens_details") or {}).get("reasoning_tokens") or 0)
        cmd = " ".join(a["command"] for a in m["extra"].get("actions", []))
        obs = msgs[i + 1]["content"] if i + 1 < len(msgs) and msgs[i + 1]["role"] in ("tool", "user") else ""
        if isinstance(obs, list): obs = " ".join(x.get("text", "") for x in obs)
        steps.append(dict(L=u["prompt_tokens"], out=out, cmd=cmd, obs=obs, ts=m["extra"].get("timestamp"),
                          cr=u.get("cache_read_input_tokens"), cw=u.get("cache_creation_input_tokens")))
    task = " ".join(str(m["content"]) for m in msgs[:2])
    return steps, task

def cost(steps, drop=frozenset(), saved_tok=None):
    """append-only: request j reads prompt_{j-1}' and writes the rest. drop = merged-away requests.
    saved_tok[j] = tokens removed from the context from request j on (diff tool outputs)."""
    c = 0.0; prev = 0; cum = 0
    for j, s in enumerate(steps):
        cum += (saved_tok or {}).get(j, 0); L = s["L"] - cum
        if j not in drop:
            c += R * min(prev, L) + W * max(L - prev, 0); prev = L
        c += O * s["out"]
    return c

NUM = re.compile(r"\d{2,}")
def semantic_dep(p, s):
    """extra rules for dependence the lexical test misses (from a hand check of 30 merged pairs):
    empty/failed result -> next call reacts to it; next call's line numbers fall within +-60 of a number shown in
    the observation; python/test run followed by another run (iterating an experiment); traceback in observation;
    adjacent/overlapping re-read of the same file (continuing to read is a decision taken after reading)."""
    o = p["obs"]
    if "<returncode>0</returncode>" not in o or len(o) < 60 or "Traceback" in o or "Error" in o: return True
    shown = {int(x) for x in NUM.findall(o)[:400]}
    if any(abs(int(n) - m) <= 60 for n in NUM.findall(s["cmd"]) for m in shown): return True
    if re.search(r"python|pytest", p["cmd"]) and re.search(r"python|pytest", s["cmd"]): return True
    fp = set(re.findall(r"[\w/.-]+\.\w+", p["cmd"])); fs = set(re.findall(r"[\w/.-]+\.\w+", s["cmd"]))
    if fp & fs and re.search(r"sed -n|head|tail|nl|cat", s["cmd"]): return True
    return False

def groups(steps, task, cap, readonly_cur=False, strict=False):
    """Greedy merge: call j joins the current turn if every call already in the turn is read-only, call j is not a
    write/submit, and call j's command uses no token that first appeared in any observation inside the turn
    (strict lexical dependency test; misses purely semantic dependence -> optimistic for batching)."""
    drop = set(); seen = set(TOK.findall(task)); novel_in_group = set(); size = 1
    for j, s in enumerate(steps):
        seen |= set(TOK.findall(s["cmd"]))
        if j:
            p = steps[j - 1]
            ok = (size < cap and READONLY.search(p["cmd"]) and not WRITES.search(p["cmd"])
                  and not WRITES.search(s["cmd"]) and "submit" not in s["cmd"].lower() and "COMPLETE_TASK" not in s["cmd"]
                  and not (set(TOK.findall(s["cmd"])) & novel_in_group))
            if readonly_cur: ok = ok and bool(READONLY.search(s["cmd"]))
            if strict and ok: ok = not semantic_dep(p, s)
            if ok: drop.add(j); size += 1
            else: size = 1; novel_in_group = set()
        nv = set(TOK.findall(s["obs"])) - seen; novel_in_group |= nv; seen |= nv
    return drop

def dup_lines(steps):
    """tokens of observation lines (len>=20 chars) already shown verbatim in an earlier observation; a diff-style
    tool wrapper would replace each run with a ~12-token back-reference."""
    shown = set(); saved = {}; dup_tok = new_tok = 0
    for j, s in enumerate(steps):
        lines = s["obs"].split("\n"); run = 0; d = 0; runs = 0; tot = 0
        for ln in lines:
            t = len(ln) / 3.6 + 0.5; tot += t
            if len(ln.strip()) >= 20 and ln in shown:
                d += t
                if not run: runs += 1
                run = 1
            else: run = 0
        for ln in lines:
            if len(ln.strip()) >= 20: shown.add(ln)
        net = max(0.0, d - 12 * runs); dup_tok += d; new_tok += tot
        if net > 0 and j + 1 < len(steps): saved[j + 1] = int(net)
    return saved, dup_tok, new_tok

if __name__ == "__main__":
    files = sorted(glob.glob(sys.argv[1] + "/*.json")); T = [load(f) for f in files]
    nreq = sum(len(s) for s, _ in T)
    print(f"== real traces: {len(T)} trajectories, {nreq} requests, mean {nreq/len(T):.1f}/task ==")
    Ls = [s["L"] for t, _ in T for s in t]; outs = [s["out"] for t, _ in T for s in t]
    new = [t[j]["L"] - t[j - 1]["L"] for t, _ in T for j in range(1, len(t))]
    print(f"prompt tokens/request mean {st.mean(Ls):,.0f} median {st.median(Ls):,.0f}; new input tokens/request mean"
          f" {st.mean(new):,.0f} median {st.median(new):,.0f}; output(+reasoning)/request mean {st.mean(outs):,.0f}")
    base = sum(cost(t) for t, _ in T)
    rd = sum(R * min(t[j-1]["L"], t[j]["L"]) for t, _ in T for j in range(1, len(t)))
    wr = sum(W * (t[0]["L"] + sum(max(t[j]["L"] - t[j-1]["L"], 0) for j in range(1, len(t)))) for t, _ in T)
    ou = sum(O * s["out"] for t, _ in T for s in t)
    print(f"append-only baseline cost {base:,.0f} units: reads {rd/base:.1%}  writes {wr/base:.1%}  output {ou/base:.1%}")
    nocache = sum(sum(s["L"] for s in t) + O * sum(s["out"] for s in t) for t, _ in T)
    print(f"  no caching at all would cost {nocache:,.0f} ({nocache/base:.2f}x) -> exact prefix caching already saves {1-base/nocache:.1%}")

    print("\n== A. batching: share of calls pairable with the previous call (strict lexical test) ==")
    for cap, ro, strict in ((2, True, False), (4, True, False), (4, False, False), (8, False, False),
                            (2, True, True), (4, True, True), (4, False, True), (8, False, True)):
            drops = [groups(t, task, cap, ro, strict) for t, task in T]
            c = sum(cost(t, d) for (t, _), d in zip(T, drops)); nd = sum(len(d) for d in drops)
            print(f"{'STRICT ' if strict else 'lexical'} cap {cap} {'read-only follow-ups' if ro else 'any non-write follow-up'}: {nd/nreq:5.1%} of requests merged away,"
                  f" cost {c/base-1:+.1%} (output priced, all output tokens kept)")

    print("\n== B. diff-style tool outputs: lines re-shown verbatim from an earlier observation ==")
    tot_d = tot_n = 0; cs = 0
    for t, _ in T:
        sv, d, n = dup_lines(t); tot_d += d; tot_n += n; cs += cost(t, saved_tok=sv)
    print(f"duplicate share of observation tokens {tot_d/tot_n:.1%}; cost with back-references {cs/base-1:+.1%}")
    drops = [groups(t, task, 4, False, True) for t, task in T]
    cb = 0
    for (t, task), d in zip(T, drops):
        sv, _, _ = dup_lines(t); cb += cost(t, d, sv)
    print(f"combined (STRICT cap-4 batching + back-references): {cb/base-1:+.1%}")

    print("\n== C. gaps between consecutive requests (tool runtime + model latency) ==")
    gaps = [t[j]["ts"] - t[j-1]["ts"] for t, _ in T for j in range(1, len(t)) if t[j]["ts"] and t[j-1]["ts"]]
    q = sorted(gaps)
    print(f"n={len(q)} median {st.median(q):.1f}s p99 {q[int(.99*len(q))]:.0f}s max {q[-1]:.0f}s;"
          f" >300s: {sum(g > 300 for g in q)} ({sum(g > 300 for g in q)/len(q):.3%})")

    print("\n== D. one real Claude Opus 4.6 trajectory (provider cache fields) ==")
    c = json.load(open(sys.argv[2])); steps = []
    for m in c["messages"]:
        if m["role"] == "assistant":
            u = m["extra"]["response"]["usage"]; steps.append((u["prompt_tokens"], u.get("cache_read_input_tokens") or 0,
                                                              u.get("cache_creation_input_tokens") or 0, u["completion_tokens"]))
    resent = sum(steps[j - 1][0] for j in range(1, len(steps))); hit = sum(s[1] for s in steps[1:])
    P = sum(s[0] for s in steps); Rr = sum(s[1] for s in steps); Ww = sum(s[2] for s in steps); Oo = sum(s[3] for s in steps)
    print(f"{len(steps)} requests; hit on re-sent tokens {hit/resent:.4f}; token hit rate {Rr/P:.4f};"
          f" cost split reads {R*Rr:,.0f} writes {W*Ww:,.0f} uncached {P-Rr-Ww:,} output {O*Oo:,.0f} units"
          f" -> output share {O*Oo/(R*Rr+W*Ww+(P-Rr-Ww)+O*Oo):.1%}; logged cost ${c['info']['model_stats']['instance_cost']:.4f}")
