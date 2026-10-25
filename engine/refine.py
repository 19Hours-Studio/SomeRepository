"""Stepwise improvement of a whole answer, without a pipeline: v0 is a plain answer; each round the same model gets the
question and the current answer in full and is asked to make it substantially better (tools allowed, no other rules);
afterwards a judge compares versions pairwise, in both orders, and says which is better and by how much.

Usage: python3 refine.py <run> --question-from <run with config.json> --start <file with v0> [--rounds 4]
State: engine/runs/<run>/ (v0.md, v1.md, ..., judge/, usage.jsonl, report.md). Resumable: existing versions are kept.
"""
import argparse, json, os, re, shutil, sys
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

HONEST = """QUESTION:
{QUESTION}

Notes from the asker (data; they may be wrong):
{NOTES}

Below is the current answer to this question. Make it substantially better on two things at once:
1. Honest: every comparison is fair (competitors at their own best settings and current versions), every decisive
   number is measured or sourced, and the limits are stated.
2. More effective: raise the real gain the answer gives the asker over the best current practice. Where honest
   accounting shows a small gain, do not stop at saying so: change the design, use the lever that is still unused, or
   move to the regime where the gain is large, until the honest number goes up, and show the calculation.
A gain that holds only under an unfair comparison does not count. You may keep, change or replace anything. You have
WebSearch (WebFetch does not reach hosts here; use search excerpts) and Bash with python3; work only in `{WORKDIR}`.

Reply with the complete improved answer only; it replaces the current one.

CURRENT ANSWER:
{ANSWER}
"""

CRITIC = """QUESTION:
{QUESTION}

Below is an answer to this question. Its author's files (code, data, outputs) are in `{FILES}`: read them and run them.
Check the answer as a demanding but fair expert who wants it to succeed:
1. Re-run or re-derive every decisive number and say which hold.
2. List every unfair or unsupported point, each with the number it changes and by how much. Check both directions:
   also say where the answer undersells itself, or concedes something it could defend.
3. Say where a larger honest gain is most likely to be found: a design change, an unused lever, a regime.
Tools: Read and Bash with python3, and WebSearch (WebFetch does not reach hosts here; use excerpts). Work only in
`{WORKDIR}`: write files only there.

End your reply with exactly this line:
HONEST GAIN: <the gain the answer supports after your check, in its own measure, or "none">

ANSWER:
{ANSWER}
"""

DEBATE = """QUESTION:
{QUESTION}

Notes from the asker (data; they may be wrong):
{NOTES}

Below are the current answer to this question and an expert check of it. Make the answer substantially better on
honesty and effectiveness at once:
- Answer every point of the check: fix it, or refute it with a computed number or a source. Do not concede a point
  you can refute, and do not keep a point you cannot defend.
- Then raise the honest gain: use the check's pointers and your own ideas - change the design, use an unused lever,
  move to the regime where the gain is large - until the honest number goes up, and show the calculation. A gain that
  holds only under an unfair comparison does not count.
The previous round's files are in `{FILES}` (copy what you need). You have WebSearch (WebFetch does not reach hosts
here; use search excerpts) and Bash with python3; work only in `{WORKDIR}`.

Reply with the complete improved answer only; it replaces the current one.

CURRENT ANSWER:
{ANSWER}

EXPERT CHECK:
{CHECK}
"""

GAIN = """QUESTION:
{QUESTION}

Read the answer below and check it. What real gain over the best current practice does it support, after you
correct anything unfair or unsupported in its own comparison? Give the gain in the answer's own measure.

End your reply with exactly this line:
HONEST GAIN: <the gain, e.g. "1.3x lower cost per token at 300 tok/s/user", or "none">

ANSWER:
{A}
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

FREE = """QUESTION:
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
"""
FREE_GAIN = """QUESTION:
{QUESTION}

The answer to check is `answer.md` in the current folder; the files behind it (code, data, outputs) are in `{AF}`.
What real gain over the best current practice does it support? How you check is up to you: read and run its code,
write your own calculations, search for prior art and real figures. You may write files in the current folder.

End your reply with exactly this line:
HONEST GAIN: <the gain, in the answer's own measure, or "none">
"""


def full_answer(text, wd, prev_words):
    """The final reply is sometimes a short note written after a background job, with the answer saved in a file
    (refine_ctxcache v8: 42 words, answer in round8/answer.md). Then the largest .md written in the round folder is the answer."""
    if len(text.split()) >= 0.3 * prev_words: return text
    mds = sorted((os.path.getsize(os.path.join(wd, f)), f) for f in os.listdir(wd) if f.endswith(".md"))
    if mds and len(open(os.path.join(wd, mds[-1][1])).read().split()) >= 0.3 * prev_words:
        print(f"  short reply ({len(text.split())} words); using {mds[-1][1]} from the round folder"); return open(os.path.join(wd, mds[-1][1])).read()
    sys.exit(f"round reply is {len(text.split())} words against {prev_words} before, and no saved answer was found in {wd}")


def main():
    p = argparse.ArgumentParser(); p.add_argument("run"); p.add_argument("--question-from", required=True)
    p.add_argument("--start", required=True); p.add_argument("--rounds", type=int, default=4)
    p.add_argument("--model", default="opus"); p.add_argument("--judge-model", default="opus")
    p.add_argument("--prompt", choices=["improve", "honest", "debate"], default="improve", help="honest: honesty and a higher real gain at once; "
                   "debate: a critic with the author's files checks each version, the author answers every point and raises the honest gain")
    p.add_argument("--start-files", help="folder with the files behind v0 (code, data), for the critic and the final reader")
    p.add_argument("--judge", choices=["free", "blind"], default="free", help="free: judges get the files and tools and check as they "
                   "see fit (freejudge run: same verdicts as blind on 3 pairs, but grounded gains from re-runs, $0.2-0.7 each); blind: two texts, no tools")
    a = p.parse_args()
    D = os.path.join(HERE, "runs", a.run); os.makedirs(D, exist_ok=True)
    cfg = json.load(open(os.path.join(HERE, "runs", a.question_from, "config.json")))
    q, notes = cfg["question"], cfg.get("notes") or "(none)"
    v = lambda k: os.path.join(D, f"v{k}.md")
    files = lambda k: (os.path.abspath(a.start_files) if a.start_files else D) if k == 0 else os.path.join(D, f"round{k}")
    if not os.path.exists(v(0)): open(v(0), "w").write(open(a.start).read())
    meta = json.load(open(os.path.join(D, "meta.json"))) if os.path.exists(os.path.join(D, "meta.json")) else {}
    for k in range(1, a.rounds + 1):  # the improvement chain (continues from the last existing version)
        if os.path.exists(v(k)): print(f"  skip v{k} (done)"); continue
        meta[f"v{k}"] = a.prompt; json.dump(meta, open(os.path.join(D, "meta.json"), "w"))
        wd = os.path.join(D, f"round{k}"); os.makedirs(wd, exist_ok=True); prev = files(k - 1)
        if a.prompt == "debate":
            cd = os.path.join(D, f"critic{k - 1}"); os.makedirs(cd, exist_ok=True); cf = os.path.join(D, f"critic_v{k - 1}.md")
            if not os.path.exists(cf):
                c = CRITIC.replace("{QUESTION}", q).replace("{FILES}", prev + "/").replace("{WORKDIR}", cd + "/").replace("{ANSWER}", open(v(k - 1)).read())
                text, u = runner.call(c, model=a.model, tools="Read,Bash,WebSearch", cwd=cd); runner.log(D, f"critic:v{k - 1}", u); open(cf, "w").write(text)
                print(f"  critic of v{k - 1}: ${u['cost_usd']:.2f}; {(re.findall(r'HONEST GAIN:(.+)', text) or ['?'])[-1].strip()[:160]}")
            s = DEBATE.replace("{QUESTION}", q).replace("{NOTES}", notes).replace("{FILES}", prev + "/").replace("{WORKDIR}", wd + "/")
            s = s.replace("{ANSWER}", open(v(k - 1)).read()).replace("{CHECK}", open(cf).read())
            text, u = runner.call(s, model=a.model, tools="research", cwd=wd); runner.log(D, f"improve:v{k}", u)
            text = full_answer(text, wd, len(open(v(k - 1)).read().split()))
            open(v(k), "w").write(text); print(f"  v{k}: {len(text.split())} words, ${u['cost_usd']:.2f}"); continue
        s = (HONEST if a.prompt == "honest" else IMPROVE).replace("{QUESTION}", q).replace("{NOTES}", notes).replace("{WORKDIR}", wd + "/").replace("{ANSWER}", open(v(k - 1)).read())
        text, u = runner.call(s, model=a.model, tools="research", cwd=wd); runner.log(D, f"improve:v{k}", u)
        text = full_answer(text, wd, len(open(v(k - 1)).read().split()))
        open(v(k), "w").write(text); print(f"  v{k}: {len(text.split())} words, ${u['cost_usd']:.2f}")
    pairs = [(0, k) for k in range(1, a.rounds + 1)] + [(k - 1, k) for k in range(2, a.rounds + 1)]
    pairs += [(4, k) for k in range(6, a.rounds + 1) if a.rounds > 5]  # the honest-gain rounds against where they started
    jd = os.path.join(D, "judge" if a.judge == "blind" else "judge_free"); os.makedirs(jd, exist_ok=True)
    def judge(job):  # job = (old, new, swap): the newer version is B unless swapped
        o, n, sw = job; f = os.path.join(jd, f"v{o}_v{n}{'_swap' if sw else ''}.md")
        if not os.path.exists(f) and a.judge == "free":
            (A, af), (B, bf) = ((n, files(n)), (o, files(o))) if sw else ((o, files(o)), (n, files(n)))
            wd = f[:-3]; os.makedirs(wd, exist_ok=True); shutil.copy(v(A), os.path.join(wd, "A.md")); shutil.copy(v(B), os.path.join(wd, "B.md"))
            s = FREE.replace("{QUESTION}", q).replace("{AF}", os.path.abspath(af) + "/").replace("{BF}", os.path.abspath(bf) + "/")
            text, u = runner.call(s, model=a.judge_model, tools="Read,Bash,WebSearch", cwd=wd)
            runner.log(D, f"judge:v{o}_v{n}{'_swap' if sw else ''}", u); open(f, "w").write(text)
        if not os.path.exists(f):
            A, B = (open(v(n)).read(), open(v(o)).read()) if sw else (open(v(o)).read(), open(v(n)).read())
            text, u = runner.call(JUDGE.replace("{QUESTION}", q).replace("{A}", A).replace("{B}", B), model=a.judge_model, tools="none")
            runner.log(D, f"judge:v{o}_v{n}{'_swap' if sw else ''}", u); open(f, "w").write(text)
        t = open(f).read(); w = re.search(r"^\**WINNER\**\s*:\s*\**\s*([AB])", t, re.M | re.I); m = re.search(r"^\**MARGIN\**\s*:\s*\**\s*(\w+)", t, re.M | re.I)
        why = re.search(r"^\**WHY\**\s*:\s*(.+)", t, re.M | re.I | re.S)
        newer_won = None if not w else (w.group(1).upper() == ("A" if sw else "B"))
        return o, n, sw, newer_won, (m.group(1).lower() if m else "?"), (why.group(1).strip()[:400] if why else "")
    with ThreadPoolExecutor(runner.slots()) as ex: res = list(ex.map(judge, [(o, n, sw) for o, n in pairs for sw in (False, True)]))
    def gain(k):  # the honest gain each version supports, read by the judge model after its own check
        f = os.path.join(jd, f"gain_v{k}.md")
        if not os.path.exists(f) and a.judge == "free":
            wd = f[:-3]; os.makedirs(wd, exist_ok=True); shutil.copy(v(k), os.path.join(wd, "answer.md"))
            g = FREE_GAIN.replace("{QUESTION}", q).replace("{AF}", os.path.abspath(files(k)) + "/")
            text, u = runner.call(g, model=a.judge_model, tools="Read,Bash,WebSearch", cwd=wd); runner.log(D, f"gain:v{k}", u); open(f, "w").write(text)
        if not os.path.exists(f):
            g = GAIN.replace("{QUESTION}", q).replace("{A}", open(v(k)).read())
            if a.prompt == "debate":  # the final reader may open and run the files behind each version too
                g = g.replace("Read the answer below and check it.", f"Read the answer below and check it. Its files (code, data, outputs) are in `{files(k)}/`; read and run them as needed.")
            text, u = runner.call(g, model=a.judge_model, tools="Read,Bash" if a.prompt == "debate" else "none", cwd=files(k) if a.prompt == "debate" else None)
            runner.log(D, f"gain:v{k}", u); open(f, "w").write(text)
        m = re.search(r"^\**HONEST GAIN\**\s*:\s*(.+)$", open(f).read(), re.M | re.I); return k, (m.group(1).strip() if m else "?")
    with ThreadPoolExecutor(runner.slots()) as ex: gains = dict(ex.map(gain, range(a.rounds + 1)))
    out = [f"# {a.run}: stepwise improvement of a plain answer, judged afterwards", "",
           "| version | round prompt | words | cost | honest gain (judge, after its own check) |", "|---|---|---|---|---|"]
    use = {}
    for l in open(os.path.join(D, "usage.jsonl")):
        r = json.loads(l); use[r["step"]] = r.get("cost_usd", 0)
    for k in range(a.rounds + 1):
        out.append(f"| v{k} | {meta.get(f'v{k}', 'improve') if k else '-'} | {len(open(v(k)).read().split())} | "
                   f"{'plain answer' if k == 0 else '$%.2f' % use.get(f'improve:v{k}', 0)} | {gains.get(k, '?')} |")
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
