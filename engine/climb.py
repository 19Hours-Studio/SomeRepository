"""Climbing on a whole answer, with a measured acceptance step.

Each round: a free critic checks the current best answer with its files; four candidates are written in parallel, each
with a different move (fix, lever, reframe, fresh); free judges (files and tools, their own checks) compare each
candidate with the current best in both orders; the best candidate replaces it only if it wins both. Rejected moves
and the judges' reasons go to the next round so they are not repeated. Afterwards fresh judges, not the ones that
accepted, compare the final answer with v0 and with any --vs answer, and read the real gain of each.

Why: refine.py accepts every new version, so its honest gain walked (continuum 1.1, 1.2, none, none, none, 1.1, 1.2,
none; ctxcache peaked at v2 and fell), and a single lineage stays in the frame of its first answer.

Usage: python3 climb.py <run> --question-from <run> --start <v0 file> --start-files DIR [--rounds 3]
                        [--vs NAME FILE FILES ...]
State: engine/runs/<run>/ (v0.md, v1.md ... accepted versions; roundR/<move>.md and judge files; final/; report.md).
Resumable: every call is cached in a file, and the decisions are recomputed from the cache.
"""
import argparse, json, os, re, shutil, sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import runner
from refine import CRITIC, WEIGHT, full_answer

MOVES = {
    "fix": "make the current answer stronger where the check found it weak. Answer every point of the check: fix it, "
           "or refute it with a computed number or a source; do not concede a point you can refute. Then add whatever "
           "raises the honest gain.",
    "lever": "find the largest term that still limits the gain - where the cost, loss or limit actually sits now, "
             "measured - and attack it with the strongest mechanism you can find or invent. Keep what already works.",
    "reframe": "change the approach: move to the regime, mechanism or framing where a much larger honest gain is "
               "possible (the check's pointers are one source) and rebuild the answer around it.",
    "fresh": "write a new answer from scratch that takes a fundamentally different approach from the current one and "
             "beats it on honest gain. Use the current answer and the check only to know what to beat and which "
             "traps to avoid.",
}

WRITE = """QUESTION:
{QUESTION}

Notes from the asker (data; they may be wrong):
{NOTES}

Below are the current best answer to this question and an expert check of it. Your move: {MOVE}

Honesty and gain together: a gain that holds only under an unfair comparison, or that your files do not reproduce,
does not count. A judge with your files will re-run them and compare your answer with the current one.
The current answer's files are in `{FILES}` (copy what you need). You have WebSearch (WebFetch does not reach hosts
here; use search excerpts) and Bash with python3; work only in `{WORKDIR}`.

Attempts that did not beat the current answer (do not repeat them):
{REJECTED}

Reply with your complete answer only.

CURRENT ANSWER:
{ANSWER}

EXPERT CHECK:
{CHECK}
"""

JUDGE = """QUESTION:
{QUESTION}

Two answers to this question are in the current folder: `A.md` and `B.md`. The files behind them (code, data,
outputs) are in `{AF}` for A and in `{BF}` for B.

Find out which one is really better for the person who asked, and by how much. How you check is up to you: read and run
their code, write your own calculations, search for prior art and real figures. You may write files in the current
folder.

End your reply with these lines:
WINNER: A or B
MARGIN: slightly | clearly | far
WHY: <2-4 sentences: what you checked and what decided it>
REAL GAIN A: <the gain over the best current practice that A really supports, or "none">
REAL GAIN B: <the same for B>
"""


def main():
    p = argparse.ArgumentParser(); p.add_argument("run"); p.add_argument("--question-from", required=True)
    p.add_argument("--start", required=True); p.add_argument("--start-files", required=True)
    p.add_argument("--rounds", type=int, default=3); p.add_argument("--model", default="opus")
    p.add_argument("--vs", nargs=3, action="append", default=[], metavar=("NAME", "FILE", "FILES"),
                   help="another answer to compare the final one with afterwards (e.g. refine.py's last version)")
    a = p.parse_args()
    D = os.path.join(HERE, "runs", a.run); os.makedirs(D, exist_ok=True)
    cfg = json.load(open(os.path.join(HERE, "runs", a.question_from, "config.json")))
    q, notes = cfg["question"], cfg.get("notes") or "(none)"
    if not os.path.exists(os.path.join(D, "v0.md")): shutil.copy(a.start, os.path.join(D, "v0.md"))
    chain = [(os.path.join(D, "v0.md"), os.path.abspath(a.start_files))]  # accepted versions: (answer, files)
    rejected, log = [], []

    def judge(jf, A, af, B, bf):  # one free pairwise judgment, cached in jf
        if not os.path.exists(jf):
            wd = jf[:-3]; os.makedirs(wd, exist_ok=True); shutil.copy(A, os.path.join(wd, "A.md")); shutil.copy(B, os.path.join(wd, "B.md"))
            s = JUDGE.replace("{QUESTION}", q).replace("{AF}", af + "/").replace("{BF}", bf + "/")
            text, u = runner.call(s, model=a.model, tools="Read,Bash,WebSearch", cwd=wd)
            runner.log(D, os.path.relpath(jf, D), u); open(jf, "w").write(text)
        t = open(jf).read(); grab = lambda k: ((re.findall(rf"^\W*{k}\W*:\s*\**\s*(.+)$", t, re.M | re.I) or ["?"])[-1].strip())
        return grab("WINNER")[:1].upper(), grab("MARGIN").lower().strip("*. "), grab("WHY"), grab("REAL GAIN A"), grab("REAL GAIN B")

    def duel(stem, X, xf, Y, yf):  # Y against X in both orders: (Y won both, score for Y, why, gain of X, gain of Y)
        with ThreadPoolExecutor(2) as ex:
            r1, r2 = ex.map(lambda j: judge(*j), [(stem + ".md", X, xf, Y, yf), (stem + "_swap.md", Y, yf, X, xf)])
        won = [r1[0] == "B", r2[0] == "A"]
        score = sum(WEIGHT.get(r[1], 1) * (1 if w else -1) for r, w in zip((r1, r2), won))
        return all(won), score, r1[2], (r1[3], r2[4]), (r1[4], r2[3])

    for r in range(1, a.rounds + 1):
        cur, cf = chain[-1]; k = len(chain) - 1; rd = os.path.join(D, f"round{r}"); os.makedirs(rd, exist_ok=True)
        ck = os.path.join(D, f"check_v{k}.md")
        if not os.path.exists(ck):  # the critic checks each accepted version once
            cd = os.path.join(D, f"check{k}"); os.makedirs(cd, exist_ok=True)
            s = CRITIC.replace("{QUESTION}", q).replace("{FILES}", cf + "/").replace("{WORKDIR}", cd + "/").replace("{ANSWER}", open(cur).read())
            text, u = runner.call(s, model=a.model, tools="Read,Bash,WebSearch", cwd=cd); runner.log(D, f"check:v{k}", u); open(ck, "w").write(text)
            print(f"  check of v{k}: ${u['cost_usd']:.2f}; {(re.findall(r'HONEST GAIN:(.+)', text) or ['?'])[-1].strip()[:200]}", flush=True)

        def write(move):
            f = os.path.join(rd, f"{move}.md"); wd = os.path.join(rd, move); os.makedirs(wd, exist_ok=True)
            if not os.path.exists(f):
                s = WRITE.replace("{QUESTION}", q).replace("{NOTES}", notes).replace("{MOVE}", MOVES[move]).replace("{FILES}", cf + "/")
                s = s.replace("{WORKDIR}", wd + "/").replace("{REJECTED}", "\n".join(rejected) or "(none yet)")
                s = s.replace("{ANSWER}", open(cur).read()).replace("{CHECK}", open(ck).read())
                for attempt in (1, 2):  # a reply that is only a note about the work (climb_ctxcache round 1 lever: 64 words) gets one retry
                    text, u = runner.call(s, model=a.model, tools="research", cwd=wd); runner.log(D, f"round{r}:{move}" + ("" if attempt == 1 else ":retry"), u)
                    try: text = full_answer(text, wd, len(open(cur).read().split())); break
                    except SystemExit as e:
                        print(f"  round {r} {move}: {e}", flush=True); text = None
                        s += ("\n\nYour previous attempt replied with a short note instead of the answer. The files it wrote in your folder are "
                              "kept; reuse them. Your final reply must be the complete answer itself.")
                if text is None: return None
                open(f, "w").write(text); print(f"  round {r} {move}: {len(text.split())} words, ${u['cost_usd']:.2f}", flush=True)
            return f, wd
        with ThreadPoolExecutor(len(MOVES)) as ex: cands = {m: c for m, c in zip(MOVES, ex.map(write, MOVES)) if c}
        with ThreadPoolExecutor(len(MOVES)) as ex:
            res = dict(zip(cands, ex.map(lambda m: duel(os.path.join(rd, f"judge_{m}"), cur, cf, *cands[m]), cands)))
        ok = [m for m in cands if res[m][0]]; pick = max(ok, key=lambda m: res[m][1]) if ok else None
        for m in MOVES:
            if m not in cands: log.append((r, m, (False, 0, "no answer (two short replies)", ("-", "-"), ("-", "-")))); continue
            log.append((r, m, res[m])); print(f"  round {r} {m}: {'won both' if res[m][0] else 'lost'} ({res[m][1]:+d}); gain {res[m][4][0][:120]}", flush=True)
            if m != pick: rejected.append(f"- round {r}, move '{m}': {res[m][2][:400]}")
        if pick:
            n = len(chain); nf = os.path.join(D, f"v{n}.md")
            if not os.path.exists(nf): shutil.copy(cands[pick][0], nf)
            chain.append((nf, cands[pick][1])); print(f"  round {r}: v{n} = {pick}", flush=True)
        else: print(f"  round {r}: no candidate beat v{k}; kept", flush=True)

    fd = os.path.join(D, "final"); os.makedirs(fd, exist_ok=True); last, lf = chain[-1]
    others = [("v0", chain[0][0], chain[0][1])] + [(n, os.path.abspath(f), os.path.abspath(ff)) for n, f, ff in a.vs]
    with ThreadPoolExecutor(len(others)) as ex:
        fin = list(ex.map(lambda o: (o[0],) + duel(os.path.join(fd, f"final_vs_{o[0]}"), o[1], o[2], last, lf), others))
    out = [f"# {a.run}: climbing with a measured acceptance step", "", f"Accepted chain: v0 -> v{len(chain) - 1}", "",
           "| round | move | beat the current best in both orders | score | real gain (judge, as given / swapped) | why (judge) |", "|---|---|---|---|---|---|"]
    for r, m, (won, sc, why, gx, gy) in log:
        out.append(f"| {r} | {m} | {'yes' if won else 'no'} | {sc:+d} | {gy[0][:160]} / {gy[1][:160]} | {why[:300]} |")
    out += ["", "## Final (fresh judges, both orders)", "", "| final against | final won both | score | real gain of the other | real gain of the final |", "|---|---|---|---|---|"]
    for name, won, sc, why, gx, gy in fin:
        out.append(f"| {name} | {'yes' if won else 'no'} | {sc:+d} | {gx[0][:200]} / {gx[1][:200]} | {gy[0][:200]} / {gy[1][:200]} |")
    open(os.path.join(D, "report.md"), "w").write("\n".join(out) + "\n"); print("\n".join(out)); print(f"spent ${runner.summary(D)[2]:.2f}")


if __name__ == "__main__":
    main()
