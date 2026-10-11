#!/usr/bin/env python3
"""Creativity Engine (ce) — детерминированное ядро протокола v2 из research/stage1-creativity.

Модели здесь не вызываются. Скрипт хранит состояние прогона, собирает промпты и слепые
наборы, разбирает ответы субагентов и судей, ведёт карту бассейнов («память
аттракторов»), делает отбор и пары для скрещивания, пишет отчёт. Субагентов запускает
Claude по .claude/skills/creativity-engine/SKILL.md.

Состояние: engine/runs/<RUN>/
  config.json  ideas.json  basins.json  scores.json  lit.json  prompts/  outputs/  sets/
"""
import argparse, math, json, os, re, secrets, sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.join(HERE, "templates")
SPECIES = os.path.join(HERE, "species")  # эволюционирующие техники («виды»): шаблоны + species.json (родословная, приспособленность)
TECHS = ["plain", "neg", "core", "reframe", "mech", "loop", "evo", "gap"]
VERDICT_ORDER = {"KNOWN": 0, "PARTIAL": 1, "NO-CLOSE-MATCH": 2}


# ---------- хранилище ----------
def rdir(run): return os.path.join(HERE, "runs", run)
def path(run, *p): return os.path.join(rdir(run), *p)
def load(run, name, default):
    f = path(run, name)
    return json.load(open(f)) if os.path.exists(f) else default
def save(run, name, obj):
    json.dump(obj, open(path(run, name), "w"), indent=1, ensure_ascii=False)
def tpl(name):
    for d in (TPL, SPECIES):
        f = os.path.join(d, name + ".txt")
        if os.path.exists(f): return open(f).read()
    sys.exit(f"no template or species named {name!r}")


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

GENIUS_RUBRIC = ("- G = genius 1-10: 10 = one simple central move that makes the hard part of the question easy or dissolves it, "
                 "surprising to experts yet obvious once seen, with consequences far beyond the question; 5 = clever but complicated, "
                 "partial or built around the hard part; 1 = a pile of machinery or a re-skin. Be harsh: most answers should be <=4.")
FRAG = re.compile(r"\b(?:idea|answer|offspring)\s*#?\s*\d\b|\b(?:as|see) above\b|\bthe above\b|\bprevious (?:idea|answer)\b", re.I)

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
    if cfg.get("thoughts"): fmt = tpl("_thoughts") + fmt
    if cfg.get("use_crux") and cfg.get("crux"): fmt = tpl("_crux") + fmt  # v1.7: generators must attack the crux
    s = body.replace("{QUESTION}", cfg["question"]).replace("{FORMAT}", fmt).replace("{N}", str(n))
    s = s.replace("{CRUX}", cfg.get("crux", "(no crux recorded)"))
    s = s.replace("{BASINS}", basins_block(run, sources))
    gaps = load(run, "gaps.json", [])
    s = s.replace("{GAPS}", "\n".join(f"{g['code']}: {g['desc']}" for g in gaps) if gaps else "(no gaps recorded)")
    s = s.replace("{PLAINFILE}", path(run, "sets", "s00", "blind.txt"))
    for k, v in (extra or {}).items(): s = s.replace("{" + k + "}", v)
    return s

def cmd_prompt(a):
    cfg = load(a.run, "config.json", None) or sys.exit("no run")
    extra = {}
    n = cfg["n"]
    if a.tech.startswith("evo"):
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
        frag = bool(FRAG.search(d["mech"] + " " + d["value"]))
        if frag: print(f"WARNING: {a.label}#{k} is a fragment (refers to another idea) - excluded from selection")
        ideas.append({"id": f"{a.label}#{k}", "label": a.label, "arm": a.arm, "gen": a.gen, **d, **({"fragment": True} if frag else {})})
    save(a.run, "ideas.json", ideas); print(f"{a.label}: {len(new)} ideas ({len(text.split())} words)")
    if "FIRST THOUGHTS" in text:
        block = text.split("FIRST THOUGHTS", 1)[1].split("=== IDEAS ===", 1)[0]
        th = load(a.run, "thoughts.json", {}); th[a.label] = [l.strip()[2:].strip() for l in block.splitlines() if l.strip().startswith("- ")]
        save(a.run, "thoughts.json", th); print(f"  first thoughts: {len(th[a.label])}")
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
    for kind in ("judge", "family", "lit", "gapwalk", "strip", "audit", "concretize", "crux", "valorize", "value", "intent"):
        s = fill(a.run, tpl(kind), 0, {"SETFILE": os.path.join(d, "blind.txt")}, a.basin_sources and a.basin_sources.split(","))
        if kind == "judge" and getattr(a, "crux", False):
            crux = load(a.run, "config.json", {}).get("crux") or sys.exit("no crux recorded: run `family` with the v1.7 template first")
            s = s.replace("- closest = ", f"- X = Y if the answer attacks this crux directly with its own mechanism: \"{crux}\"; N if it delegates, assumes away or ignores it.\n- closest = ")
            s = s.replace("ID | O | C | V | R | BASIN | closest", "ID | O | C | V | R | BASIN | X | closest")
        if kind == "judge" and getattr(a, "genius", False):
            s = s.replace("- R = ", GENIUS_RUBRIC + "\n- R = ")
            s = s.replace("ID | O | C | V | R | BASIN", "ID | O | C | V | G | R | BASIN")
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
    m = re.search(r"^CRUX \| (.+)$", text, re.M)
    if m:
        cfg = load(a.run, "config.json", {}); cfg["crux"] = m.group(1).strip(); save(a.run, "config.json", cfg)
        print("crux:", cfg["crux"])

def cmd_judge(a):
    text = read_source(a); key = setkey(a.run, a.set)
    open(path(a.run, "sets", a.set, f"judge_{a.judge}.md"), "w").write(text)
    sc = load(a.run, "scores.json", {}); n = 0
    for sid, o, c, v, g, r, b, x, cl in re.findall(r"^([A-Z]+\d\d) \| (\d+) \| (\d+) \| (\d+) \| (?:(\d+) \| )?([YN]) \| ([A-Z0-9_]+) \| (?:([YN]) \| )?(.+)$", text, re.M):
        if sid not in key: continue
        sc.setdefault(key[sid], {})[f"{a.set}:{a.judge}"] = {"O": int(o), "C": int(c), "V": int(v), "R": r, "B": b, "closest": cl.strip(),
                                                           **({"X": x} if x else {}), **({"G": int(g)} if g else {})}
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
            "basins": [j["B"] for j in js], "closest": js[0]["closest"], "closest_all": " ".join(j["closest"] for j in js),
            "crux": (sum(j["X"] == "Y" for j in js if "X" in j) / sum("X" in j for j in js)) if any("X" in j for j in js) else None,
            "G": (sum(j["G"] for j in js if "G" in j) / sum("G" in j for j in js)) if any("G" in j for j in js) else None}

def cmd_select(a):
    lit = load(a.run, "lit.json", {}); pool = []
    for i in select_ids(a.run, a.labels and a.labels.split(","), None, a.arms and a.arms.split(",")):
        g = agg(a.run, i["id"])
        if not g: continue
        known_basin = all(b != "NEW" for b in g["basins"]) and len(set(g["basins"])) == 1
        if g["R_all"] or (a.drop_known_basins and known_basin) or lit.get(i["id"], {}).get("verdict") == "KNOWN": continue
        if i.get("fragment"): continue
        if a.v2:
            au = load(a.run, "audit.json", {}).get(i["id"])
            if not au: continue
            if au["spec"] is not None and au["spec"] <= 0: continue  # «подходит к любому вопросу» — отсев
            pool.append((g["OV"] * (0.5 + 0.5 * au["carried"]), i["id"], g)); continue
        pool.append((g["OV"] * (g["G"] if getattr(a, "by", "ov") == "ovg" and g["G"] is not None else 1), i["id"], g))
    pool.sort(key=lambda t: -t[0])
    if getattr(a, "diverse", False):  # v1.7: near-duplicates (same closest work) take one slot
        words = lambda g: set(re.findall(r"[a-z]{4,}", g["closest_all"].lower()))
        top = []
        for t in pool:
            if all(len(words(t[2]) & words(u[2])) / max(1, len(words(t[2]) | words(u[2]))) < 0.5 for u in top): top.append(t)
            if len(top) == a.k: break
    else:
        top = pool[:a.k]
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

def cmd_fork(a):
    """Новый прогон с общей картой аттракторов (gen0, наблюдённые/предсказанные бассейны, s00): плечи A/B не загрязняют друг друга."""
    import shutil
    os.makedirs(path(a.dst, "prompts"), exist_ok=True); os.makedirs(path(a.dst, "outputs"), exist_ok=True)
    save(a.dst, "config.json", load(a.src, "config.json", {}))
    save(a.dst, "ideas.json", [i for i in load(a.src, "ideas.json", []) if i["gen"] == 0])
    save(a.dst, "basins.json", [b for b in load(a.src, "basins.json", []) if b.get("source") in ("observed", "predicted")])
    for f, v in [("scores.json", {}), ("lit.json", {})]: save(a.dst, f, v)
    if os.path.exists(path(a.src, "gaps.json")): shutil.copy(path(a.src, "gaps.json"), path(a.dst, "gaps.json"))
    if os.path.isdir(path(a.src, "sets", "s00")):
        shutil.copytree(path(a.src, "sets", "s00"), path(a.dst, "sets", "s00"), dirs_exist_ok=True)
        for f in os.listdir(path(a.dst, "sets", "s00")):  # пути в промптах — на новый прогон
            fp = path(a.dst, "sets", "s00", f)
            if f.startswith("prompt_"): open(fp, "w").write(open(fp).read().replace(rdir(a.src) + "/", rdir(a.dst) + "/"))
    os.makedirs(path(a.dst, "sets"), exist_ok=True)
    print(f"forked {a.src} -> {a.dst}")

def cmd_import(a):
    """Импорт идей gen>=1 из другого прогона под меткой плеча (id получают префикс плеча)."""
    ideas = [i for i in load(a.dst, "ideas.json", []) if not i["id"].startswith(a.arm + ":")]
    n = 0
    for i in load(a.src, "ideas.json", []):
        if i["gen"] >= 1:
            ideas.append({**i, "id": f"{a.arm}:{i['id']}", "label": f"{a.arm}:{i['label']}", "arm": a.arm}); n += 1
    save(a.dst, "ideas.json", ideas); print(f"imported {n} ideas from {a.src} as arm {a.arm}")

def cmd_gapwalk(a):
    text = read_source(a); open(path(a.run, "sets", a.set, "gapwalk.md"), "w").write(text)
    gaps = [{"code": c, "desc": d.strip(), "where": w.strip()} for c, d, w in re.findall(r"^GAP \| (G\d+) \| (.+?) \| (.+)$", text, re.M)]
    save(a.run, "gaps.json", gaps); print(f"gaps: {len(gaps)}")
    if not gaps: print("WARNING: no GAP lines parsed")

def cmd_strip(a):
    """Очищенные от риторики версии -> blind_stripped.txt с теми же ID + prompt_judge_stripped.txt."""
    text = read_source(a); d = path(a.run, "sets", a.set); key = setkey(a.run, a.set)
    got = dict(re.findall(r"^STRIP \| ([A-Z]+\d\d) \| (.+)$", text, re.M))
    missing = [k for k in key if k not in got]
    if missing: print("WARNING: not stripped (original kept):", missing)
    orig = dict(re.findall(r"^([A-Z]+\d\d)\n(MECHANISM: .+?\nVALUE: .+?)\n", open(os.path.join(d, "blind.txt")).read(), re.S))
    with open(os.path.join(d, "blind_stripped.txt"), "w") as f:
        for k in key: f.write(f"{k}\n" + (f"MECHANISM: {got[k]}\n\n" if k in got else orig.get(k, "") + "\n\n"))
    open(os.path.join(d, "prompt_judge_stripped.txt"), "w").write(
        open(os.path.join(d, "prompt_judge.txt")).read().replace(os.path.join(d, "blind.txt"), os.path.join(d, "blind_stripped.txt")))
    print(f"stripped {len(got)}/{len(key)} -> {d}/prompt_judge_stripped.txt")

def cmd_audit(a):
    text = read_source(a); key = setkey(a.run, a.set); au = load(a.run, "audit.json", {})
    open(path(a.run, "sets", a.set, "audit.md"), "w").write(text)
    slots = defaultdict(list)
    for sid, st, dd, ll in re.findall(r"^SLOT \| ([A-Z]+\d\d) \| (.+?) \| ([YN]) \| (\d)$", text, re.M):
        if sid in key: slots[key[sid]].append({"slot": st.strip(), "D": dd, "L": int(ll)})
    dec = {key[s]: tuple(map(int, v)) for s, *v in re.findall(r"^DECOY \| ([A-Z]+\d\d) \| (\d+) \| (\d+) \| (\d+) \| (\d+)$", text, re.M) if s in key}
    for iid in set(slots) | set(dec):
        L = slots.get(iid, []); tot = sum(x["L"] for x in L)
        carried = sum(x["L"] for x in L if x["D"] == "N") / tot if tot else 0.0
        v = dec.get(iid); spec = (v[0] - sum(v[1:]) / 3) if v else None
        au[iid] = {"slots": L, "carried": round(carried, 2), "decoy": v, "spec": None if spec is None else round(spec, 2)}
    save(a.run, "audit.json", au); print(f"audit: {len(au)} ideas ({len(slots)} with slots, {len(dec)} with decoys)")

def cmd_valorize(a):
    """Layers B and C (v1.8): each idea rebuilt around its anchor - for genius (prompt_valorize) or for value
    (prompt_value) -> a new arm whose ideas keep a `parent` link."""
    text = read_source(a); key = setkey(a.run, a.set)
    open(path(a.run, "sets", a.set, f"valorize_{a.arm}.md"), "w").write(text)
    ideas = load(a.run, "ideas.json", []); byid = {i["id"]: i for i in ideas}; n = 0
    for sid, body in re.findall(r"=== (?:VALORIZED|VALUED) ([A-Z]+\d\d) ===\n(.*?)(?=\n=== (?:VALORIZED|VALUED)|\Z)", text, re.S):
        if sid not in key: continue
        par = byid[key[sid]]
        m = re.search(r"MECHANISM:\**\s*(.+?)\n\s*\**VALUE:\**\s*(.+)", body, re.S)
        if not m: continue
        nm = re.search(r"NAME:\**\s*(.+)", body); an = re.search(r"ANCHOR:\**\s*(.+)", body)
        nid = f"{a.arm}:{par['id']}"; ideas = [i for i in ideas if i["id"] != nid]
        ideas.append({"id": nid, "label": f"{a.arm}:{par['label']}", "arm": a.arm, "gen": par["gen"], "parent": par["id"],
                      "name": nm.group(1).strip() if nm else "", "anchor": an.group(1).strip() if an else "",
                      "mech": " ".join(m.group(1).split()), "value": " ".join(m.group(2).split())}); n += 1
    save(a.run, "ideas.json", ideas); print(f"valorized {n}/{len(key)} -> arm {a.arm}")

def cmd_intent(a):
    """Intent check (v1.8): store 3 readings of the question, each with its crux; `--pick N` makes reading N the crux."""
    cfg = load(a.run, "config.json", {})
    if a.pick is not None:
        r = cfg.get("readings") or sys.exit("no readings stored: run `intent R <set> --transcript ...` first")
        k = a.pick
        if k == "auto":  # the asker does not care: take the reading whose crux best matches the family judge's crux
            ws = lambda t: set(re.findall(r"[a-z]{4,}", t.lower())); ref = ws(cfg.get("crux", ""))
            k = max(range(len(r)), key=lambda i: len(ws(r[i]["crux"]) & ref) / max(1, len(ws(r[i]["crux"]) | ref)))
        k = int(k); cfg["crux"] = r[k]["crux"]; cfg["reading"] = r[k]["label"]; save(a.run, "config.json", cfg)
        print(f"crux <- reading {k} ({r[k]['label']}): {cfg['crux']}"); return
    text = read_source(a); open(path(a.run, "sets", a.set, "intent.md"), "w").write(text)
    rs = [{"label": l.strip(), "goal": g.strip(), "crux": c.strip()}
          for l, g, c in re.findall(r"^READING \| (.+?) \| (.+?) \| CRUX:\s*(.+)$", text, re.M)]
    cfg["readings"] = rs; save(a.run, "config.json", cfg)
    for k, r in enumerate(rs): print(f"[{k}] {r['label']}: {r['goal']}\n    CRUX: {r['crux']}")

def cmd_futurematch(a):
    """External validity: share of literature-checked ideas whose closest work appeared after the model's knowledge
    cutoff (arXiv ids YYMM >= --after). Such ideas could not be copied, yet people later found them worth doing."""
    ideas = {i["id"]: i for i in load(a.run, "ideas.json", [])}; lit = load(a.run, "lit.json", {}); by = defaultdict(lambda: [0, 0])
    for iid, v in lit.items():
        arm = ideas.get(iid, {}).get("arm", "?"); t = json.dumps(v); late = [x for x in re.findall(r"arxiv\.org/(?:abs|pdf|html)/(\d{4})\.\d{4,5}", t) if x >= a.after]
        late += [y[2:] + m for y, m in re.findall(r"\((20\d\d)-(\d\d)\)", t) if y[2:] + m >= a.after]  # dated journal work
        by[arm][0] += 1; by[arm][1] += bool(late)
    for arm, (n, k) in sorted(by.items()): print(f"  {arm:10s} future-match {k}/{n} = {k / n:.0%}")

def cmd_portfolio(a):
    """Technique bandit across all runs: fitness = gen-1 O*V relative to the run's gen-1 mean; UCB bonus for rarely
    tried techniques; the best one gets a second slot."""
    stats = defaultdict(list)
    for r in sorted(os.listdir(os.path.join(HERE, "runs"))):
        if r.startswith("_") or not os.path.exists(path(r, "ideas.json")): continue
        g1 = [(i, agg(r, i["id"])) for i in load(r, "ideas.json", []) if i["gen"] == 1]; g1 = [(i, g) for i, g in g1 if g]
        if len(g1) < 6: continue
        m = sum(g["OV"] for _, g in g1) / len(g1); by = defaultdict(list)
        for i, g in g1: by[re.sub(r"\d+$", "", i["label"].split(":")[-1].replace("g1_", ""))].append(g["OV"])
        for t, v in by.items(): stats[t].append(sum(v) / len(v) / m)
    total = sum(len(v) for v in stats.values())
    ucb = {t: sum(v) / len(v) + a.c * math.sqrt(math.log(total) / len(v)) for t, v in stats.items() if t not in a.exclude.split(",")}
    order = sorted(ucb, key=lambda t: -ucb[t]); pick = order[:a.slots - 1] + order[:1]
    for t in order: print(f"  {t:12s} runs {len(stats[t]):2d}  mean {sum(stats[t]) / len(stats[t]):.2f}  ucb {ucb[t]:.2f}")
    print("portfolio:", " ".join(f"g1_{t}" + ("2" if k == a.slots - 1 else "") for k, t in enumerate(pick)))

def cmd_setcfg(a):
    cfg = load(a.run, "config.json", {}); cfg[a.key] = json.loads(a.value) if a.value[:1] in "[{0123456789tf" else a.value
    save(a.run, "config.json", cfg); print(a.key, "=", cfg[a.key])

def cmd_thoughts(a):
    """Самоотчёт о первых мыслях -> посещённые бассейны (source=self): следующее поколение отталкивается и от них."""
    th = load(a.run, "thoughts.json", {}); basins = load(a.run, "basins.json", []); k = 0
    have = {b["desc"] for b in basins}
    for lab in (a.labels.split(",") if a.labels else th):
        for t in th.get(lab, []):
            if t not in have:
                basins.append({"code": f"T{len(basins)+1:02d}", "desc": t[:200], "source": "self", "members": []}); have.add(t); k += 1
    save(a.run, "basins.json", basins); print(f"self-reported first thoughts -> {k} basins (total {len(basins)})")

def cmd_concretize(a):
    """Добавляет «первый тест» к механизму идей набора (оригинал сохраняется в mech_orig)."""
    text = read_source(a); key = setkey(a.run, a.set); open(path(a.run, "sets", a.set, "concretize.md"), "w").write(text)
    got = {key[s]: t.strip() for s, t in re.findall(r"^TEST \| ([A-Z]+\d\d) \| (.+)$", text, re.M) if s in key}
    ideas = load(a.run, "ideas.json", [])
    for i in ideas:
        if i["id"] in got:
            i.setdefault("mech_orig", i["mech"]); i["mech"] = i["mech_orig"] + " " + got[i["id"]]
    save(a.run, "ideas.json", ideas); print(f"concretized {len(got)}/{len(key)}")

BREED = """You design idea-generation TECHNIQUES: prompt templates that make a language model produce fundamentally new answers to a hard question. Each parent technique below is followed by what it actually produced on past runs of the same question. Those recurring outputs are the technique's niche (its attractor), which we want to escape.

{PARENTS}
Create exactly these new techniques:
{OPS}

Rules:
- crossover A+B: fuse the parents' core moves into ONE procedure in which each parent's move changes how the other's works (not two steps glued in sequence).
- mutate A: keep what made A productive, but change its procedure so that it cannot land in A's observed niche.
- Each template must contain these four literal placeholders exactly as written: {Q}, {N}, {B} (where the list of forbidden known idea families will be inserted) and {F} (put it last; it holds the answer format).
- Do NOT put example answers, example fields, example mechanisms or names of specific theories into the templates: examples get copied verbatim.
- At most 220 words per template.

Output ONLY, for each technique:
=== SPECIES <short_lowercase_name> ===
<template text>
=== END ===
"""

def cmd_breed(a):
    """Промпт селекционера: родители (шаблоны) + что они выдавали в прошлых прогонах (их аттрактор)."""
    names = defaultdict(list)
    for r in a.from_runs.split(","):
        for i in load(r, "ideas.json", []):
            if i["gen"] == 1: names[i["label"].split(":")[-1].replace("g1_", "").rstrip("0123456789")].append(i["name"])
    parents = sorted({p for op in a.ops for p in re.split(r"[:+]", op)[1:]})
    blocks = []
    for p in parents:
        seen = sorted(set(names.get(p, [])))
        blocks.append(f"--- PARENT {p} ---\n{tpl(p)}\nObserved outputs on past runs ({len(seen)}): " + "; ".join(seen) + "\n")
    ops = "\n".join(f"- {op.replace(':', ' ')}" for op in a.ops)
    s = BREED.replace("{PARENTS}", "\n".join(blocks)).replace("{OPS}", ops)
    s = s.replace("{Q}", "{QUESTION}").replace("{N}", "{N}").replace("{B}", "{BASINS}").replace("{F}", "{FORMAT}")
    p = path(a.run, "prompts", "breed.txt"); open(p, "w").write(s); print(p)

def cmd_species(a):
    """Принять новые виды от селекционера: проверка плейсхолдеров, запись шаблона и родословной."""
    text = read_source(a); os.makedirs(SPECIES, exist_ok=True)
    reg = json.load(open(os.path.join(SPECIES, "species.json"))) if os.path.exists(os.path.join(SPECIES, "species.json")) else {}
    got = re.findall(r"=== SPECIES ([a-z0-9_]+) ===\n(.+?)\n=== END ===", text, re.S); ok = 0
    ops = a.ops.split()  # селекционер выдаёт виды в порядке операций: k-й вид рождён k-й операцией
    for k, (name, body) in enumerate(got):
        missing = [ph for ph in ("{QUESTION}", "{N}", "{BASINS}", "{FORMAT}") if ph not in body]
        if missing: print(f"REJECTED {name}: missing {missing}"); continue
        open(os.path.join(SPECIES, name + ".txt"), "w").write(body.strip() + "\n")
        reg[name] = {"born_in": a.run, "ops": ops[k] if len(ops) == len(got) else a.ops, "fitness": reg.get(name, {}).get("fitness", [])}; ok += 1
        print(f"species {name}: {len(body.split())} words")
    json.dump(reg, open(os.path.join(SPECIES, "species.json"), "w"), indent=1); print(f"accepted {ok}/{len(got)}")

def cmd_fitness(a):
    """Приспособленность вида = средний O×V его идей gen1 в этом прогоне (по последнему набору судей)."""
    regf = os.path.join(SPECIES, "species.json"); reg = json.load(open(regf)) if os.path.exists(regf) else {}
    by = defaultdict(list)
    for i in load(a.run, "ideas.json", []):
        g = agg(a.run, i["id"])
        if i["gen"] == 1 and g: by[i["label"].replace("g1_", "")].append(g["OV"])
    for sp_, v in sorted(by.items(), key=lambda kv: -sum(kv[1]) / len(kv[1])):
        f = round(sum(v) / len(v), 1); print(f"  {sp_:14s} fitness {f}")
        if sp_ in reg: reg[sp_]["fitness"].append({"run": a.run, "OV": f})
    json.dump(reg, open(regf, "w"), indent=1)

def cmd_import_basins(a):
    """Перенести семейства одного прогона в другой под новым источником (например, найденное ранее -> prior)."""
    dst = load(a.dst, "basins.json", []); have = {b["code"] for b in dst}; k = 0
    for b in load(a.src, "basins.json", []):
        if b.get("source") == a.source:
            code = "P" + b["code"]
            if code not in have: dst.append({**b, "code": code, "source": a.as_}); k += 1
    save(a.dst, "basins.json", dst); print(f"imported {k} basins as {a.as_}")

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
    x.add_argument("--format", default="value", choices=["value", "difference", "arch"]); x.add_argument("--n", type=int, default=3)
    x.add_argument("--force", action="store_true")
    x = sp.add_parser("prompt"); x.add_argument("run"); x.add_argument("tech", help="technique template or evolved species name"); x.add_argument("label")
    x.add_argument("--pairs", type=int, default=3); x.add_argument("--pair-from", type=int, default=0)
    x = sp.add_parser("ingest"); x.add_argument("run"); x.add_argument("label"); x.add_argument("--arm", required=True)
    x.add_argument("--gen", type=int, default=0); src(x)
    x = sp.add_parser("set"); x.add_argument("run"); x.add_argument("set"); x.add_argument("--labels"); x.add_argument("--ids")
    x.add_argument("--arms"); x.add_argument("--prefix", default="S")
    x.add_argument("--basin-sources", help="e.g. observed,predicted — exclude visited families from judge prompts (fair final comparison)")
    x.add_argument("--crux", action="store_true", help="v1.7: add the crux column X to the judge prompt")
    x.add_argument("--genius", action="store_true", help="v1.7: add the genius score G to the judge prompt")
    x = sp.add_parser("family"); x.add_argument("run"); x.add_argument("set"); src(x)
    x = sp.add_parser("valorize"); x.add_argument("run"); x.add_argument("set"); x.add_argument("--arm", required=True); src(x)
    x = sp.add_parser("intent"); x.add_argument("run"); x.add_argument("set", nargs="?"); x.add_argument("--pick", help="reading number, or auto"); src(x)
    x = sp.add_parser("futurematch"); x.add_argument("run"); x.add_argument("--after", default="2607", help="arXiv YYMM after the knowledge cutoff")
    x = sp.add_parser("portfolio"); x.add_argument("--slots", type=int, default=5); x.add_argument("--c", type=float, default=0.15)
    x.add_argument("--exclude", default="mechneg,symptomport,backloop,reframe,gap", help="techniques retired by selection")
    x = sp.add_parser("judge"); x.add_argument("run"); x.add_argument("set"); x.add_argument("judge"); src(x)
    x = sp.add_parser("select"); x.add_argument("run"); x.add_argument("name"); x.add_argument("--labels"); x.add_argument("--arms")
    x.add_argument("--k", type=int, default=6); x.add_argument("--drop-known-basins", action="store_true")
    x.add_argument("--diverse", action="store_true", help="v1.7: near-duplicates (same closest work) take one slot")
    x.add_argument("--by", default="ov", choices=["ov", "ovg"], help="v1.7: ovg ranks by O*V*G (genius) when judges gave G")
    x.add_argument("--v2", action="store_true", help="score = O*V*(0.5+0.5*carried); drop ideas with decoy specificity <= 0 (needs audit)")
    x = sp.add_parser("lit"); x.add_argument("run"); x.add_argument("set"); src(x)
    x = sp.add_parser("pairs"); x.add_argument("run"); x.add_argument("name"); x.add_argument("--n", type=int, default=6)
    x = sp.add_parser("remember"); x.add_argument("run"); x.add_argument("--labels"); x.add_argument("--arms")
    x = sp.add_parser("report"); x.add_argument("run"); x.add_argument("--top", type=int, default=10)
    x = sp.add_parser("fork"); x.add_argument("src"); x.add_argument("dst")
    x = sp.add_parser("import"); x.add_argument("dst"); x.add_argument("src"); x.add_argument("--arm", required=True)
    x = sp.add_parser("breed"); x.add_argument("run"); x.add_argument("--from-runs", required=True)
    x.add_argument("--ops", nargs="+", required=True, help='e.g. cross:loop+core mutate:loop')
    x = sp.add_parser("species"); x.add_argument("run"); x.add_argument("--ops", default=""); src(x)
    x = sp.add_parser("fitness"); x.add_argument("run")
    x = sp.add_parser("import-basins"); x.add_argument("dst"); x.add_argument("src"); x.add_argument("--source", default="visited")
    x.add_argument("--as", dest="as_", default="prior")
    x = sp.add_parser("setcfg"); x.add_argument("run"); x.add_argument("key"); x.add_argument("value")
    x = sp.add_parser("thoughts"); x.add_argument("run"); x.add_argument("--labels")
    for name in ("gapwalk", "strip", "audit", "concretize"):
        x = sp.add_parser(name); x.add_argument("run"); x.add_argument("set"); src(x)
    a = p.parse_args()
    needs_src = a.cmd in ("ingest", "family", "judge", "lit", "gapwalk", "strip", "audit", "concretize", "species", "valorize") or (a.cmd == "intent" and a.pick is None)
    if getattr(a, "transcript", None) is None and getattr(a, "file", None) is None and needs_src:
        sys.exit("need --transcript or --file")
    globals()["cmd_" + a.cmd.replace("-", "_")](a)


if __name__ == "__main__":
    main()
