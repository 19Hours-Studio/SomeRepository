#!/usr/bin/env python3
"""Creativity Engine (ce) — детерминированное ядро протокола v2 из research/stage1-creativity.

Модели здесь не вызываются. Скрипт хранит состояние прогона, собирает промпты и слепые
наборы, разбирает ответы субагентов и судей, ведёт карту бассейнов («память
аттракторов»), делает отбор и пары для скрещивания, пишет отчёт. Субагентов запускает
Claude по .claude/skills/creativity-engine/SKILL.md.

Состояние: engine/runs/<RUN>/
  config.json  ideas.json  basins.json  scores.json  lit.json  prompts/  outputs/  sets/
"""
import argparse, json, os, re, secrets, sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.join(HERE, "templates")
TECHS = ["plain", "neg", "core", "reframe", "mech", "loop", "evo"]
VERDICT_ORDER = {"KNOWN": 0, "PARTIAL": 1, "NO-CLOSE-MATCH": 2}


# ---------- хранилище ----------
def rdir(run): return os.path.join(HERE, "runs", run)
def path(run, *p): return os.path.join(rdir(run), *p)
def load(run, name, default):
    f = path(run, name)
    return json.load(open(f)) if os.path.exists(f) else default
def save(run, name, obj):
    json.dump(obj, open(path(run, name), "w"), indent=1, ensure_ascii=False)
def tpl(name): return open(os.path.join(TPL, name + ".txt")).read()


# ---------- разбор текста ----------
def transcript_text(p):
    """Последний ответ субагента из JSONL-транскрипта (текст или SubagentHandback)."""
    last = ""
    for line in open(p):
        try: ev = json.loads(line)
        except ValueError: continue
        m = ev.get("message") or {}
        if m.get("role") != "assistant" or not isinstance(m.get("content"), list): continue
        t = "".join(x.get("text", "") for x in m["content"] if isinstance(x, dict) and x.get("type") == "text")
        t += "".join((x.get("input") or {}).get("message", "") for x in m["content"]
                     if isinstance(x, dict) and x.get("type") == "tool_use" and x.get("name") == "SubagentHandback")
        if t.strip(): last = t
    return last

def read_source(a):
    return transcript_text(a.transcript) if a.transcript else open(a.file).read()

def parse_ideas(text):
    if "=== IDEAS ===" not in text: return []
    body = text.split("=== IDEAS ===", 1)[1]
    out = []
    for c in re.split(r"\n\**IDEA\s*\d+\**", "\n" + body):
        m = re.search(r"MECHANISM:\**\s*(.+?)\n\s*\**(?:VALUE|DIFFERENCE):\**\s*(.+?)(?:\n\s*\n|\Z)", c, re.S)
        if not m: continue
        n = re.search(r"NAME:\**\s*(.+)", c)
        out.append({"name": n.group(1).strip() if n else "", "mech": " ".join(m.group(1).split()),
                    "value": " ".join(m.group(2).split())})
    return out

def basins_block(run, sources=None):
    b = [x for x in load(run, "basins.json", []) if not sources or x.get("source") in sources]
    return "\n".join(f"{x['code']}: {x['desc']}" for x in b) if b else "(none recorded yet)"


# ---------- команды ----------
def cmd_init(a):
    os.makedirs(path(a.run, "prompts"), exist_ok=True); os.makedirs(path(a.run, "outputs"), exist_ok=True)
    os.makedirs(path(a.run, "sets"), exist_ok=True)
    if os.path.exists(path(a.run, "config.json")) and not a.force: sys.exit("run exists (use --force)")
    save(a.run, "config.json", {"question": a.question, "format": a.format, "n": a.n})
    for f, v in [("ideas.json", []), ("basins.json", []), ("scores.json", {}), ("lit.json", {})]: save(a.run, f, v)
    print("initialized", rdir(a.run))

def fill(run, body, n, extra=None, sources=None):
    cfg = load(run, "config.json", {})
    fmt = tpl("_format_" + cfg["format"]).replace("{N}", str(n))
    s = body.replace("{QUESTION}", cfg["question"]).replace("{FORMAT}", fmt).replace("{N}", str(n))
    s = s.replace("{BASINS}", basins_block(run, sources))
    for k, v in (extra or {}).items(): s = s.replace("{" + k + "}", v)
    return s

def cmd_prompt(a):
    cfg = load(a.run, "config.json", None) or sys.exit("no run")
    extra = {}
    n = cfg["n"]
    if a.tech == "evo":
        pairs = load(a.run, "pairs.json", [])[a.pair_from:a.pair_from + a.pairs]
        if not pairs: sys.exit("no pairs: run `pairs` first")
        ideas = {i["id"]: i for i in load(a.run, "ideas.json", [])}; lit = load(a.run, "lit.json", {})
        blocks = []
        for k, (x, y) in enumerate(pairs, 1):
            blocks.append(f"PAIR {k}")
            for tag, iid in (("A", x), ("B", y)):
                i = ideas[iid]; near = lit.get(iid, {}).get("closest", "unknown")
                blocks += [f" Parent {tag}: MECHANISM: {i['mech']}", f"   VALUE: {i['value']}", f"   nearest published work: {near}"]
            blocks.append("")
        extra["PAIRS"] = "\n".join(blocks); n = len(pairs)
    s = fill(a.run, tpl(a.tech), n, extra)
    p = path(a.run, "prompts", a.label + ".txt"); open(p, "w").write(s); print(p)

def cmd_ingest(a):
    text = read_source(a)
    open(path(a.run, "outputs", a.label + ".md"), "w").write(text)
    ideas = load(a.run, "ideas.json", [])
    ideas = [i for i in ideas if i["label"] != a.label]  # повторный ingest заменяет
    new = parse_ideas(text)
    for k, d in enumerate(new, 1):
        ideas.append({"id": f"{a.label}#{k}", "label": a.label, "arm": a.arm, "gen": a.gen, **d})
    save(a.run, "ideas.json", ideas); print(f"{a.label}: {len(new)} ideas ({len(text.split())} words)")
    if not new: print("WARNING: no ideas parsed — check outputs/" + a.label + ".md")

def select_ids(run, labels=None, ids=None, arms=None):
    allx = load(run, "ideas.json", [])
    if not (labels or ids or arms): return allx  # без фильтров — все идеи
    return [i for i in allx if (ids and i["id"] in ids) or (labels and i["label"] in labels) or (arms and i["arm"] in arms)]

def cmd_set(a):
    items = select_ids(a.run, a.labels and a.labels.split(","), a.ids and a.ids.split(","), a.arms and a.arms.split(","))
    if not items: sys.exit("empty set")
    secrets.SystemRandom().shuffle(items)
    d = path(a.run, "sets", a.set); os.makedirs(d, exist_ok=True)
    key = {}
    with open(os.path.join(d, "blind.txt"), "w") as f:
        for j, i in enumerate(items, 1):
            sid = f"{a.prefix}{j:02d}"; key[sid] = i["id"]
            f.write(f"{sid}\nMECHANISM: {i['mech']}\nVALUE: {i['value']}\n\n")
    json.dump(key, open(os.path.join(d, "key.json"), "w"), indent=1)
    for kind in ("judge", "family", "lit"):
        s = fill(a.run, tpl(kind), 0, {"SETFILE": os.path.join(d, "blind.txt")}, a.basin_sources and a.basin_sources.split(","))
        open(os.path.join(d, f"prompt_{kind}.txt"), "w").write(s)
    print(f"set {a.set}: {len(items)} items -> {d}/blind.txt (+ prompt_judge/family/lit.txt)")

def setkey(run, s): return json.load(open(path(run, "sets", s, "key.json")))

def cmd_family(a):
    text = read_source(a); key = setkey(a.run, a.set)
    open(path(a.run, "sets", a.set, "family.md"), "w").write(text)
    basins = load(a.run, "basins.json", []); have = {b["code"] for b in basins}; added = 0
    fam_lines = [l for l in text.splitlines() if l.startswith("FAMILY |")]
    parsed = re.findall(r"^FAMILY \| ([A-Z0-9_]{2,16}) \| (.+?) \| (.+)$", text, re.M)
    if len(parsed) < len(fam_lines): print(f"WARNING: {len(fam_lines) - len(parsed)} FAMILY lines not parsed")
    for code, desc, mem in parsed:
        if code in have: continue
        members = [] if mem.strip().lower().startswith("predicted") else [key.get(x.strip(), x.strip()) for x in mem.split(",")]
        basins.append({"code": code, "desc": desc.strip(), "source": "predicted" if not members else "observed", "members": members})
        have.add(code); added += 1
    save(a.run, "basins.json", basins); print(f"basins: +{added} (total {len(basins)})")

def cmd_judge(a):
    text = read_source(a); key = setkey(a.run, a.set)
    open(path(a.run, "sets", a.set, f"judge_{a.judge}.md"), "w").write(text)
    sc = load(a.run, "scores.json", {}); n = 0
    for sid, o, c, v, r, b, cl in re.findall(r"^([A-Z]+\d\d) \| (\d+) \| (\d+) \| (\d+) \| ([YN]) \| ([A-Z0-9_]+) \| (.+)$", text, re.M):
        if sid not in key: continue
        sc.setdefault(key[sid], {})[f"{a.set}:{a.judge}"] = {"O": int(o), "C": int(c), "V": int(v), "R": r, "B": b, "closest": cl.strip()}
        n += 1
    save(a.run, "scores.json", sc); print(f"judge {a.judge} on {a.set}: {n}/{len(key)} parsed")
    if n < len(key): print("WARNING: missing lines — check sets/" + a.set + f"/judge_{a.judge}.md")

def agg(run, iid):
    """Среднее по всем судьям (последний набор, где идея оценивалась)."""
    s = load(run, "scores.json", {}).get(iid, {})
    if not s: return None
    last_set = sorted({k.split(":")[0] for k in s})[-1]
    js = [v for k, v in s.items() if k.startswith(last_set + ":")]
    m = lambda f: sum(j[f] for j in js) / len(js)
    return {"O": m("O"), "C": m("C"), "V": m("V"), "OV": m("O") * m("V"), "n_judges": len(js),
            "R_all": all(j["R"] == "Y" for j in js), "R_any": any(j["R"] == "Y" for j in js),
            "new_all": all(j["B"] == "NEW" for j in js), "new_frac": sum(j["B"] == "NEW" for j in js) / len(js),
            "basins": [j["B"] for j in js], "closest": js[0]["closest"]}

def cmd_select(a):
    lit = load(a.run, "lit.json", {}); pool = []
    for i in select_ids(a.run, a.labels and a.labels.split(","), None, a.arms and a.arms.split(",")):
        g = agg(a.run, i["id"])
        if not g: continue
        known_basin = all(b != "NEW" for b in g["basins"]) and len(set(g["basins"])) == 1
        if g["R_all"] or (a.drop_known_basins and known_basin) or lit.get(i["id"], {}).get("verdict") == "KNOWN": continue
        pool.append((g["OV"], i["id"], g))
    pool.sort(key=lambda t: -t[0]); top = pool[:a.k]
    save(a.run, f"survivors_{a.name}.json", [t[1] for t in top])
    for ov, iid, g in top: print(f"{iid:18s} O{g['O']:.1f} V{g['V']:.1f} OV{ov:5.1f} basins={g['basins']}")
    print(f"-> survivors_{a.name}.json ({len(top)} of {len(pool)} eligible)")

def cmd_lit(a):
    text = read_source(a); key = setkey(a.run, a.set); lit = load(a.run, "lit.json", {}); n = 0
    open(path(a.run, "sets", a.set, "lit.md"), "w").write(text)
    for sid, verdict, rest in re.findall(r"^([A-Z]+\d\d) \| (KNOWN|PARTIAL|NO-CLOSE-MATCH)[^|]*\| (.+)$", text, re.M):
        if sid not in key: continue
        parts = rest.split(" | "); lit[key[sid]] = {"verdict": verdict, "closest": parts[0].replace("closest work:", "").strip(),
                                                   "new": parts[1].strip() if len(parts) > 1 else ""}
        n += 1
    save(a.run, "lit.json", lit); print(f"lit: {n}/{len(key)} parsed")

def cmd_pairs(a):
    surv = load(a.run, f"survivors_{a.name}.json", []); lit = load(a.run, "lit.json", {})
    surv = [s for s in surv if lit.get(s, {}).get("verdict") != "KNOWN"]
    def family(s):  # консервативно: если хоть один судья видит известный бассейн — идея в нём
        known = [b for b in (agg(a.run, s) or {}).get("basins", []) if b != "NEW"]
        return Counter(known).most_common(1)[0][0] if known else "NEW:" + s
    fam = {s: family(s) for s in surv}; label = {s: s.split("#")[0] for s in surv}
    # приоритет родителя: сначала вердикт литературы (новее — лучше), затем O×V
    prio = {s: (VERDICT_ORDER.get(lit.get(s, {}).get("verdict"), 1), (agg(a.run, s) or {}).get("OV", 0)) for s in surv}
    surv = sorted(surv, key=lambda s: prio[s], reverse=True)
    ok = lambda x, y: x != y and fam[x] != fam[y] and label[x] != label[y]
    uses, pairs, seen = Counter(), [], set()
    def add(x, y):
        pairs.append([x, y]); seen.add(frozenset((x, y))); uses[x] += 1; uses[y] += 1
    # 1) покрытие: каждый родитель (по приоритету) получает пару с наименее использованным допустимым партнёром
    for x in surv:
        if uses[x] or len(pairs) >= a.n: continue
        cand = [y for y in surv if ok(x, y) and uses[y] < 2 and frozenset((x, y)) not in seen]
        if cand: add(x, min(cand, key=lambda y: (uses[y], surv.index(y))))
    # 2) добор лучшими оставшимися парами; каждый родитель не более 2 раз
    for x in surv:
        for y in surv:
            if len(pairs) >= a.n: break
            if ok(x, y) and uses[x] < 2 and uses[y] < 2 and frozenset((x, y)) not in seen: add(x, y)
    # 3) если пар не хватает: разрешаем пары из одного запуска, но только между разными семействами
    for x in surv:
        for y in surv:
            if len(pairs) >= a.n: break
            if x != y and fam[x] != fam[y] and uses[x] < 2 and uses[y] < 2 and frozenset((x, y)) not in seen: add(x, y)
    unpaired = [s for s in surv if not uses[s]]
    if unpaired: print("WARNING: no valid partner for", unpaired)
    save(a.run, "pairs.json", pairs); [print(" x ".join(p)) for p in pairs]; print(f"-> pairs.json ({len(pairs)})")

def cmd_remember(a):
    """Память аттракторов: идеи, которые судьи единогласно сочли NEW, становятся посещёнными
    семействами — следующее поколение от них отталкивается."""
    basins = load(a.run, "basins.json", []); have = {m for b in basins for m in b.get("members", [])}; k = 0
    for i in select_ids(a.run, a.labels and a.labels.split(","), None, a.arms and a.arms.split(",")):
        g = agg(a.run, i["id"])
        if g and g["new_all"] and i["id"] not in have:
            k += 1; basins.append({"code": f"V{len(basins)+1:02d}", "desc": f"{i['name']} — {i['mech'][:160]}",
                                   "source": "visited", "members": [i["id"]]})
    save(a.run, "basins.json", basins); print(f"remembered {k} visited families (total {len(basins)})")

def cmd_report(a):
    arms = defaultdict(list)
    for i in load(a.run, "ideas.json", []):
        g = agg(a.run, i["id"])
        if g: arms[i["arm"]].append((i, g))
    lit = load(a.run, "lit.json", {}); out = [f"# Отчёт прогона `{a.run}`\n", f"Вопрос: {load(a.run, 'config.json', {})['question']}\n",
          "| arm | n | O | C | V | O×V | top3 O×V | NEW-доля | R=Y (все судьи) |", "|---|---|---|---|---|---|---|---|---|"]
    for arm, L in sorted(arms.items()):
        n = len(L); m = lambda f: sum(g[f] for _, g in L) / n
        top3 = sorted((g["OV"] for _, g in L), reverse=True)[:3]
        out.append(f"| {arm} | {n} | {m('O'):.2f} | {m('C'):.2f} | {m('V'):.2f} | {m('OV'):.1f} | {sum(top3)/len(top3):.1f} | "
                   f"{m('new_frac'):.2f} | {sum(g['R_all'] for _, g in L)}/{n} |")
    out += ["", "## Лучшие идеи", "", "| id | arm | O | V | O×V | бассейны | литература | name |", "|---|---|---|---|---|---|---|---|"]
    allg = sorted(((i, g) for L in arms.values() for i, g in L), key=lambda t: -t[1]["OV"])[:a.top]
    for i, g in allg:
        out.append(f"| {i['id']} | {i['arm']} | {g['O']:.1f} | {g['V']:.1f} | {g['OV']:.1f} | {'/'.join(g['basins'])} | "
                   f"{lit.get(i['id'], {}).get('verdict', '—')} | {i['name']} |")
    s = "\n".join(out) + "\n"; open(path(a.run, "report.md"), "w").write(s); print(s)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = p.add_subparsers(dest="cmd", required=True)
    def src(x): x.add_argument("--transcript"); x.add_argument("--file")
    x = sp.add_parser("init"); x.add_argument("run"); x.add_argument("--question", required=True)
    x.add_argument("--format", default="value", choices=["value", "difference"]); x.add_argument("--n", type=int, default=3)
    x.add_argument("--force", action="store_true")
    x = sp.add_parser("prompt"); x.add_argument("run"); x.add_argument("tech", choices=TECHS); x.add_argument("label")
    x.add_argument("--pairs", type=int, default=3); x.add_argument("--pair-from", type=int, default=0)
    x = sp.add_parser("ingest"); x.add_argument("run"); x.add_argument("label"); x.add_argument("--arm", required=True)
    x.add_argument("--gen", type=int, default=0); src(x)
    x = sp.add_parser("set"); x.add_argument("run"); x.add_argument("set"); x.add_argument("--labels"); x.add_argument("--ids")
    x.add_argument("--arms"); x.add_argument("--prefix", default="S")
    x.add_argument("--basin-sources", help="e.g. observed,predicted — exclude visited families from judge prompts (fair final comparison)")
    x = sp.add_parser("family"); x.add_argument("run"); x.add_argument("set"); src(x)
    x = sp.add_parser("judge"); x.add_argument("run"); x.add_argument("set"); x.add_argument("judge"); src(x)
    x = sp.add_parser("select"); x.add_argument("run"); x.add_argument("name"); x.add_argument("--labels"); x.add_argument("--arms")
    x.add_argument("--k", type=int, default=6); x.add_argument("--drop-known-basins", action="store_true")
    x = sp.add_parser("lit"); x.add_argument("run"); x.add_argument("set"); src(x)
    x = sp.add_parser("pairs"); x.add_argument("run"); x.add_argument("name"); x.add_argument("--n", type=int, default=6)
    x = sp.add_parser("remember"); x.add_argument("run"); x.add_argument("--labels"); x.add_argument("--arms")
    x = sp.add_parser("report"); x.add_argument("run"); x.add_argument("--top", type=int, default=10)
    a = p.parse_args()
    if getattr(a, "transcript", None) is None and getattr(a, "file", None) is None and a.cmd in ("ingest", "family", "judge", "lit"):
        sys.exit("need --transcript or --file")
    globals()["cmd_" + a.cmd](a)


if __name__ == "__main__":
    main()
