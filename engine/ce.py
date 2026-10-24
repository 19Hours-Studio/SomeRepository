#!/usr/bin/env python3
"""Creativity Engine (ce) — детерминированное ядро протокола v2 из research/stage1-creativity.

Модели здесь не вызываются. Скрипт хранит состояние прогона, собирает промпты и слепые
наборы, разбирает ответы субагентов и судей, ведёт карту бассейнов («память
аттракторов»), делает отбор и пары для скрещивания, пишет отчёт. Субагентов запускает
Claude по .claude/skills/creativity-engine/SKILL.md.

Состояние: engine/runs/<RUN>/
  config.json  ideas.json  basins.json  scores.json  lit.json  prompts/  outputs/  sets/
"""
import argparse, math, json, os, re, secrets, sys, time
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
FEASIBLE_RUBRIC = ("- F = feasibility 1-10: do a quick order-of-magnitude check of the ONE quantity that decides whether it works "
                   "at the scale it claims (useful rate per area or volume under the allowed loss, leak against useful rate, stress the "
                   "containment must carry, energy or information per unit of material, cost of the dominating part); 10 = the numbers "
                   "clearly work; 5 = off by about 3-10x but fixable; 1 = off by orders of magnitude. Judge the physics, not the tone.")
PRINCIPLE_RUBRIC = ("- P = single principle 1-10: 10 = one clear, statable principle produces the gain and every part of the "
                    "answer follows from it or is minimal wrapping; 5 = a principle is there but the answer is mostly a combination "
                    "of independent tricks; 1 = a bag of tricks with no central principle.")
FRAG = re.compile(r"\b(?:idea|answer|offspring)\s*#?\s*\d\b|\b(?:as|see) above\b|\bthe above\b|\bprevious (?:idea|answer)\b", re.I)

def parse_principles(text):
    """v2.0: one-line principles with self-reported typicality P (verbalized sampling)."""
    out = []
    for nm, cl, ov, gn, pp in re.findall(r"^\**PRINCIPLE\** \| (.+?) \| (.+?) \| OVERTURNS:\s*(.+?) \| GAIN:\s*(.+?) \| P:\s*([0-9.]+)", text, re.M):
        out.append({"name": nm.strip(), "mech": f"{cl.strip()} (Overturns: {ov.strip()})", "value": gn.strip(),
                    "principle": cl.strip(), "overturns": ov.strip(), "p": float(pp)})
    return out

def parse_ideas(text):
    if "=== PRINCIPLES ===" in text: return parse_principles(text.split("=== PRINCIPLES ===", 1)[1])
    if "=== IDEAS ===" not in text: return []
    body = text.split("=== IDEAS ===", 1)[1]
    out = []
    for c in re.split(r"\n\**IDEA\s*\d+\**", "\n" + body):
        m = re.search(r"MECHANISM:\**\s*(.+?)\n\s*\**(?:VALUE|DIFFERENCE):\**\s*(.+?)(?:\n\s*\n|\Z)", c, re.S)
        if not m: continue
        n = re.search(r"NAME:\**\s*(.+)", c); pp = re.search(r"\n\s*\**P:\**\s*([0-9.]+)", c)
        out.append({"name": n.group(1).strip() if n else "", "mech": " ".join(m.group(1).split()),
                    "value": " ".join(m.group(2).split()), **({"p": float(pp.group(1))} if pp else {})})
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
    fmt = fmt.replace("under 500 words", f"under {max(500, 110 * n)} words")  # many-idea prompts (resurrect) need room
    if cfg.get("thoughts"): fmt = tpl("_thoughts") + fmt
    if cfg.get("use_crux") and cfg.get("crux"): fmt = tpl("_crux") + fmt  # v1.7: generators must attack the crux
    s = body.replace("{QUESTION}", cfg["question"]).replace("{FORMAT}", fmt).replace("{N}", str(n))
    s = s.replace("{CRUX}", cfg.get("crux", "(no crux recorded)"))
    s = s.replace("{PFORMAT}", tpl("_format_principle").replace("{N}", str(n)))
    s = s.replace("{BASINS}", basins_block(run, sources))
    s = s.replace("{LAWS}", "\n".join(f"- {l['law']} (rules out: {l['out']}; opens: {l['opens']})" for l in cfg.get("laws", [])) or "(no laws recorded)")
    gaps = load(run, "gaps.json", [])
    s = s.replace("{GAPS}", "\n".join(f"{g['code']}: {g['desc']}" for g in gaps) if gaps else "(no gaps recorded)")
    s = s.replace("{PLAINFILE}", path(run, "sets", "s00", "blind.txt"))
    for key in ("FRONTIER", "LEDGER", "ATTEMPTS", "EVIDENCE", "CEILINGS", "REFRAMES"):  # v3.0-5: raw material (`material`, `ceilings`, reframe step)
        if extra and key in extra: continue  # e.g. a fact slice instead of the whole ledger
        f = path(run, key.lower() + ".md")
        s = s.replace("{" + key + "}", open(f).read().strip() if os.path.exists(f) else "(none recorded)")
    if "{LESSONS}" in s: s = s.replace("{LESSONS}", lessons_block(cfg))  # v5: memory between runs
    if "{MATERIAL}" in s: s = s.replace("{MATERIAL}", material_block(run, cfg))
    for k, v in (extra or {}).items(): s = s.replace("{" + k + "}", v)
    s = s.replace("{NOTES}", cfg.get("notes") or "(none)")  # v5: notes from the user and about the environment, for every step
    return s.replace("{REFRAME}", (cfg.get("reframes") or ["(no reformulation recorded)"])[0]).replace("{TECH}", "")

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
    if getattr(a, "n", None): n = a.n
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
    parents = getattr(a, "parents", None)
    if parents:  # repair/red-team rounds: the k-th parsed idea descends from the k-th listed id
        parents = parents.split(",") if "," in parents or not os.path.exists(parents) else json.load(open(parents))
        if len(parents) != len(new): sys.exit(f"--parents lists {len(parents)} ids but {len(new)} ideas were parsed")
        for k, par in enumerate(parents, 1):
            next(i for i in ideas if i["id"] == f"{a.label}#{k}")["parent"] = par
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
    for kind in ("judge", "family", "lit", "gapwalk", "strip", "audit", "concretize", "crux", "valorize", "value", "fermi", "truth", "derive", "intent"):
        s = fill(a.run, tpl(kind), 0, {"SETFILE": os.path.join(d, "blind.txt")}, a.basin_sources and a.basin_sources.split(","))
        if kind == "judge" and getattr(a, "crux", False):
            crux = load(a.run, "config.json", {}).get("crux") or sys.exit("no crux recorded: run `family` with the v1.7 template first")
            s = s.replace("- closest = ", f"- X = Y if the answer attacks this crux directly with its own mechanism: \"{crux}\"; N if it delegates, assumes away or ignores it.\n- closest = ")
            s = s.replace("ID | O | C | V | R | BASIN | closest", "ID | O | C | V | R | BASIN | X | closest")
        if kind == "judge" and getattr(a, "genius", False):
            s = s.replace("- R = ", GENIUS_RUBRIC + "\n- R = ")
            s = s.replace("ID | O | C | V | R | BASIN", "ID | O | C | V | G | R | BASIN")
        if kind == "judge" and getattr(a, "feasible", False):
            s = s.replace("- R = ", FEASIBLE_RUBRIC + "\n- R = ")
            s = re.sub(r"(ID \| O \| C \| V(?: \| G)?)", r"\1 | F", s, count=1)
        if kind == "judge" and getattr(a, "principle", False):
            s = s.replace("- R = ", PRINCIPLE_RUBRIC + "\n- R = ")
            s = re.sub(r"(ID \| O \| C \| V(?: \| G)?(?: \| F)?)", r"\1 | P", s, count=1)
        open(os.path.join(d, f"prompt_{kind}.txt"), "w").write(s)
    json.dump([c for c, f in (("G", "genius"), ("F", "feasible"), ("P", "principle")) if getattr(a, f, False)], open(os.path.join(d, "extra_cols.json"), "w"))
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
    xf = path(a.run, "sets", a.set, "extra_cols.json"); cols = json.load(open(xf)) if os.path.exists(xf) else ["G"]
    for sid, o, c, v, e1, e2, e3, r, b, x, cl in re.findall(r"^([A-Z]+\d\d) \| (\d+) \| (\d+) \| (\d+) \| (?:(\d+) \| )?(?:(\d+) \| )?(?:(\d+) \| )?([YN]) \| ([A-Z0-9_]+)(?: \([^|]*\))? \| (?:([YN]) \| )?(.+)$", text, re.M):  # "NEW (note)" accepted
        if sid not in key: continue
        extra = {k: int(e) for k, e in zip(cols, [e for e in (e1, e2, e3) if e])}
        sc.setdefault(key[sid], {})[f"{a.set}:{a.judge}"] = {"O": int(o), "C": int(c), "V": int(v), "R": r, "B": b, "closest": cl.strip(),
                                                           **({"X": x} if x else {}), **extra}
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
            "G": (sum(j["G"] for j in js if "G" in j) / sum("G" in j for j in js)) if any("G" in j for j in js) else None,
            "F": (sum(j["F"] for j in js if "F" in j) / sum("F" in j for j in js)) if any("F" in j for j in js) else None}

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
        by = getattr(a, "by", "ov"); w = {"ovg": g["G"], "ovf": g["F"]}.get(by)
        if by == "gate":  # v3.0: originality x real headroom (kill test), not judged value
            gt = load(a.run, "gate.json", {}).get(i["id"])
            if not gt: continue
            pool.append((g["O"] * GATE_W.get(gt["verdict"], 0) * min(gt.get("ratio", 1.0), 5.0), i["id"], g)); continue
        pool.append((g["OV"] * (w if w is not None else 1), i["id"], g))
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
        if (i["id"] in a.ids.split(",")) if getattr(a, "ids", None) else i["gen"] >= 1:
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
    """Layers B, C (v1.8) and D (v1.9): each idea rebuilt around its anchor - for genius (prompt_valorize), value
    (prompt_value) or a quantitative check (prompt_fermi) -> a new arm whose ideas keep a `parent` link."""
    text = read_source(a); key = setkey(a.run, a.set)
    open(path(a.run, "sets", a.set, f"valorize_{a.arm}.md"), "w").write(text)
    ideas = load(a.run, "ideas.json", []); byid = {i["id"]: i for i in ideas}; n = 0
    for sid, body in re.findall(r"=== (?:VALORIZED|VALUED|CHECKED|DERIVED) ([A-Z]+\d\d) ===\n(.*?)(?=\n=== (?:VALORIZED|VALUED|CHECKED|DERIVED)|\Z)", text, re.S):
        if sid not in key: continue
        par = byid[key[sid]]
        m = re.search(r"MECHANISM:\**\s*(.+?)\n\s*\**VALUE:\**\s*(.+)", body, re.S)
        if not m: continue
        nm = re.search(r"NAME:\**\s*(.+)", body); an = re.search(r"ANCHOR:\**\s*(.+)", body)
        nid = f"{a.arm}:{par['id']}"; ideas = [i for i in ideas if i["id"] != nid]
        ideas.append({"id": nid, "label": f"{a.arm}:{par['label']}", "arm": a.arm, "gen": par["gen"], "parent": par["id"],
                      "name": nm.group(1).strip() if nm else "", "anchor": an.group(1).strip() if an else "",
                      "mech": " ".join(m.group(1).split()), "value": " ".join(m.group(2).split())}); n += 1
        vd = re.search(r"VERDICT:\**\s*(PASS|FIX|FAIL|TRUE|REGIME|FALSE)", body); es = re.search(r"ESTIMATE:\**\s*(.+?)\n\s*\**NAME:", body, re.S)
        if vd: ideas[-1]["verdict"] = vd.group(1)
        if es: ideas[-1]["estimate"] = " ".join(es.group(1).split())
    save(a.run, "ideas.json", ideas); vs = Counter(i.get("verdict") for i in ideas if i["arm"] == a.arm and i.get("verdict"))
    print(f"valorized {n}/{len(key)} -> arm {a.arm}" + (f"  verdicts {dict(vs)}" if vs else ""))

def cmd_laws(a):
    """v2.0 loop "count -> law -> invent": without a source, write the layer-D estimates of --arm to laws/blind.txt and
    build laws/prompt_laws.txt; with --transcript/--file, store the distilled LAW lines in config (used by `prompt R law`)."""
    cfg = load(a.run, "config.json", {})
    if a.transcript or a.file:
        laws = [{"law": l.strip(), "out": o.strip(), "opens": p.strip()} for l, o, p in
                re.findall(r"^\**LAW\** \| (.+?) \| RULES OUT:\s*(.+?) \| OPENS:\s*(.+)$", read_source(a), re.M)]
        if not laws: sys.exit("no LAW lines found")
        cfg["laws"] = laws; save(a.run, "config.json", cfg); print(f"laws: {len(laws)} stored"); return
    est = [i for i in load(a.run, "ideas.json", []) if i["arm"] == a.arm and i.get("estimate")]
    if not est: sys.exit(f"no estimates in arm {a.arm}: run layer D (prompt_fermi + valorize --arm {a.arm}) first")
    d = path(a.run, "laws"); os.makedirs(d, exist_ok=True); bf = os.path.join(d, "blind.txt")
    with open(bf, "w") as f:
        for k, i in enumerate(secrets.SystemRandom().sample(est, len(est)), 1):
            f.write(f"E{k:02d} ({i.get('verdict', '?')})\nESTIMATE: {i['estimate']}\n\n")
    open(os.path.join(d, "prompt_laws.txt"), "w").write(fill(a.run, tpl("laws"), 0, {"SETFILE": bf}))
    print(f"laws: {len(est)} estimates -> {bf} (+ prompt_laws.txt)")

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

def task_ideas(run, ids, scores=True):
    """Numbered idea blocks with the latest judges' mean O and F (for repair and red-team tasks)."""
    allx = {i["id"]: i for i in load(run, "ideas.json", [])}; out = []
    for k, iid in enumerate(ids, 1):
        if iid not in allx: sys.exit(f"unknown idea {iid}")
        i, g = allx[iid], agg(run, iid)
        sc = f" (mean originality {g['O']:.1f}/10, mean feasibility {g['F']:.1f}/10)" if scores and g and g.get("F") is not None else ""
        out.append(f"IDEA {k}{sc}\nNAME: {i['name']}\nMECHANISM: {i['mech']}\nVALUE: {i['value']}\n")
    return "\n".join(out)

def idea_blocks(run, ids, extras, scores=True):
    """task_ideas with extra lines (reviews, kill tests) appended to each idea's block."""
    parts = [x for x in re.split(r"(?m)^(?=IDEA \d+)", task_ideas(run, ids, scores)) if x.strip()]
    return "\n".join(p.rstrip("\n") + "".join("\n" + l for l in extras.get(iid, [])) + "\n" for p, iid in zip(parts, ids))

def latest_review(dirs, iid):
    """Review lines (defects, what survived, fit, ratio, known) from the first listed review dir that reviewed the idea."""
    r = next((r for d in dirs if (r := review_lines(d, iid, survives=True)) is not None), None)
    return ["- (not reviewed)"] if r is None else (r or ["- no FATAL or MAJOR defect found"])

def cmd_repairtask(a):
    """v2.2: researcher repair (best-practice baseline per unit of recovered product + rate-vs-tolerance
    consistency pass); --critique adds a red-team review the researcher must answer point by point."""
    ids = a.ids.split(","); os.makedirs(a.dir, exist_ok=True); wd = os.path.abspath(a.dir)
    crit = ""
    if a.critique:
        crit = ("\nAn adversarial reviewer has examined the current versions. Answer EVERY defect it lists: fix it in\n"
                "the design, refute it with a computed number, or concede it in the verdict. Its review:\n<<<REVIEW\n"
                + read_source(argparse.Namespace(transcript=a.critique if a.critique.endswith(".output") else None,
                                                 file=None if a.critique.endswith(".output") else a.critique))
                + "\nREVIEW>>>\n")
    extras = {iid: [] for iid in ids}
    if a.audits:  # v3.6: each idea carries its latest blind review (first listed dir that has it)
        for iid in ids: extras[iid] += ["BLIND REVIEW:"] + latest_review(a.audits.split(","), iid)
    if getattr(a, "gate", None):  # v5: and its kill-test result
        g = load(a.run, a.gate, {})
        for iid in ids:
            if (r := g.get(iid)): extras[iid].append(f"KILL TEST: killer {r.get('killer', '?')} | margin {r.get('margin', '?')} | "
                                                     f"whole-chain ratio {r.get('ratio', '?')} | {r.get('verdict')}: {r.get('why', '')}")
    ideas = idea_blocks(a.run, ids, extras)
    s = fill(a.run, tpl(a.tpl), len(ids), {"WORKDIR": wd + "/", "IDEAS": ideas, "CRITIQUE": crit, "NOTES": a.notes or "(none)",
                                           "EVIDENCE": fact_slice(a.run, [ideas])})
    open(os.path.join(a.dir, "TASK.md"), "w").write(s); json.dump(ids, open(os.path.join(a.dir, "parents.json"), "w"))
    print(os.path.join(a.dir, "TASK.md"))

def cmd_redteamtask(a):
    """v2.2: adversarial reviewer with tools; its review feeds `repairtask --critique`."""
    ids = a.ids.split(","); os.makedirs(a.dir, exist_ok=True); wd = os.path.abspath(a.dir)
    ideas = task_ideas(a.run, ids, scores=not a.blind)
    s = fill(a.run, tpl(a.tpl), len(ids), {"WORKDIR": wd + "/", "IDEAS": ideas, "EVIDENCE": fact_slice(a.run, [ideas])})
    open(os.path.join(a.dir, "TASK.md"), "w").write(s); json.dump(ids, open(os.path.join(a.dir, "ids.json"), "w"))
    print(os.path.join(a.dir, "TASK.md"))

def cmd_attemptstask(a):
    """v3.3: ledger of earlier attempts - what was already tried near these designs and why the problem stayed unsolved
    (an unsolved problem means every earlier mechanism stopped short for a reason a re-invention would inherit)."""
    ids = a.ids.split(","); os.makedirs(a.dir, exist_ok=True); wd = os.path.abspath(a.dir)
    s = fill(a.run, tpl("attempts_task"), len(ids), {"WORKDIR": wd + "/", "IDEAS": task_ideas(a.run, ids, scores=False)})
    open(os.path.join(a.dir, "TASK.md"), "w").write(s); json.dump(ids, open(os.path.join(a.dir, "ids.json"), "w"))
    print(os.path.join(a.dir, "TASK.md"))

def cmd_researchtask(a):
    """v3.6 (explanation questions): a researcher with search builds raw material - the evidence ledger of hard facts
    (`evidence_task`) or the ledger of earlier explanations and why each failed (`hypotheses_task`)."""
    os.makedirs(a.dir, exist_ok=True)
    s = fill(a.run, tpl(a.tpl), 0, {"WORKDIR": os.path.abspath(a.dir) + "/"})
    open(os.path.join(a.dir, "TASK.md"), "w").write(s); print(os.path.join(a.dir, "TASK.md"))

def cmd_material(a):
    """v3.0: store raw material for generators and the gate: the frontier scout's capabilities, the value ledger,
    or (v3.3) the ledger of earlier attempts."""
    text = read_source(a); tag = "=== " + a.kind.upper() + " ==="
    if tag not in text: sys.exit(f"no '{tag}' section found")
    body = re.split(r"\n=== [A-Z]+ ===", text.split(tag, 1)[1])[0].strip()  # up to the next section
    open(path(a.run, a.kind + ".md"), "w").write(body + "\n"); print(f"{a.kind}: {len(body.split())} words")

def cmd_gatetask(a):
    """v3.0: tool-using kill test (decisive quantity MARGIN + whole-chain cost RATIO) for many ideas at once."""
    ids = a.ids.split(","); os.makedirs(a.dir, exist_ok=True); wd = os.path.abspath(a.dir)
    extra = {"WORKDIR": wd + "/", "IDEAS": task_ideas(a.run, ids, scores=False)}
    if a.kit:  # v3.4: verified calculation kit + catalog of killer classes from earlier audits
        kd = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kit"); cat = os.path.join(kd, "CATALOG.md")
        if not os.path.exists(cat): sys.exit("no kit/CATALOG.md")
        extra.update({"KITDIR": kd + "/", "KIT": open(cat).read().strip()})
    s = fill(a.run, tpl("gate_task_kit" if a.kit else "gate_task"), len(ids), extra)
    open(os.path.join(a.dir, "TASK.md"), "w").write(s); json.dump(ids, open(os.path.join(a.dir, "ids.json"), "w"))
    print(os.path.join(a.dir, "TASK.md"))

GATE_NUM = re.compile(r"(MARGIN|RATIO)\s*[:=]?\s*~?\s*([0-9]*\.?[0-9]+(?:e-?[0-9]+)?)", re.I)

def cmd_gate(a):
    """Parse a kill-test transcript into gate.json: {id: {margin, ratio, verdict, killer, why}}."""
    ids = json.load(open(os.path.join(a.dir, "ids.json"))); text = read_source(a)
    text = text[text.find("=== GATE ==="):] if "=== GATE ===" in text else text
    out = a.out or "gate.json"; gate = load(a.run, out, {}); n = 0
    for k, body in zip(*[iter(re.split(r"^IDEA (\d+)\s*:", text, flags=re.M)[1:])] * 2):
        k = int(k)
        if not 1 <= k <= len(ids): continue
        rec = {"killer": "", "why": ""}
        for line in body.splitlines():
            parts = [x.strip() for x in line.split("|")]
            if parts[0] == "KILLER": rec["killer"] = parts[1] if len(parts) > 1 else ""
            if parts[0] == "SCREEN": rec["screen"] = parts[1] if len(parts) > 1 else ""
            if parts[0] == "VERDICT" and len(parts) > 1:
                rec["verdict"] = parts[1].upper(); rec["why"] = parts[2] if len(parts) > 2 else ""
            for name, val in GATE_NUM.findall(line):
                if parts[0] in ("KILLER", "CHAIN"): rec[name.lower()] = float(val)
        if rec.get("verdict") in ("ALIVE", "WOUNDED", "DEAD"):
            gate[ids[k - 1]] = rec; n += 1
    save(a.run, out, gate)
    from collections import Counter
    print(f"gate: {n}/{len(ids)} parsed", dict(Counter(gate[i]["verdict"] for i in ids if i in gate)))

GATE_W = {"ALIVE": 1.0, "WOUNDED": 0.4, "DEAD": 0.0}

def cmd_evolve(a):
    """v3.2: evolution under the deep audit - a free generator (no tools) gets audited designs with their FATAL/MAJOR
    review findings (from `redteamtask` + its REVIEW.md) and must build children the defects no longer apply to.
    --audit may list several review dirs; --ids picks the parents (default: every idea in the review dirs)."""
    dirs = a.audit.split(",")
    ids = a.ids.split(",") if a.ids else [i for d in dirs for i in json.load(open(os.path.join(d, "ids.json")))]
    allx = {i["id"]: i for i in load(a.run, "ideas.json", [])}; blocks = []
    for k, iid in enumerate(ids, 1):
        i = allx[iid]
        rev = next((r for d in dirs if (r := review_lines(d, iid)) is not None), None)
        if not rev: sys.exit(f"no FATAL/MAJOR findings for {iid} in {a.audit}")
        blocks.append(f"DESIGN {k}\nNAME: {i['name']}\nMECHANISM: {i['mech']}\nVALUE: {i['value']}\nREVIEW FINDINGS:\n" + "\n".join(rev[:a.max_defects]) + "\n")
    if a.tpl == "evolve_attempts" and not os.path.exists(path(a.run, "attempts.md")): sys.exit("no attempts.md: run `material R attempts`")
    s = fill(a.run, tpl(a.tpl), len(ids) * a.m, {"PARENTS": "\n".join(blocks), "M": str(a.m)})
    p = path(a.run, "prompts", a.label + ".txt"); open(p, "w").write(s)
    json.dump([iid for iid in ids for _ in range(a.m)], open(path(a.run, "prompts", a.label + ".parents.json"), "w"))
    print(p)

def review_lines(audit_dir, iid, sev=("FATAL", "MAJOR"), survives=False):
    """Blind-review findings for one idea from a redteamtask dir (ids.json + REVIEW.md); None if not reviewed there."""
    ids = json.load(open(os.path.join(audit_dir, "ids.json")))
    if iid not in ids or not os.path.exists(os.path.join(audit_dir, "REVIEW.md")): return None
    found = dict(zip(*[iter(re.split(r"^IDEA (\d+)\s*:", open(os.path.join(audit_dir, "REVIEW.md")).read(), flags=re.M)[1:])] * 2))
    out = []
    for l in found.get(str(ids.index(iid) + 1), "").splitlines():
        d = [x.strip() for x in l.split("|")]
        if d[0] == "DEFECT" and len(d) > 2 and d[1] in sev: out.append(f"- {d[1]}: {d[2]} ({d[3] if len(d) > 3 else ''})")
        if survives and d[0] in ("SURVIVES", "FIT", "RATIO", "KNOWN") and len(d) > 1: out.append(f"- {d[0]}: {' | '.join(d[1:])}")
    return out

def cmd_composetask(a):
    """v3.5: chain composer - surviving pieces (with their blind reviews) + best practice -> whole chains whose link
    gains multiply; computed with the calculation kit against current practice and the best competent alternative."""
    ids = a.ids.split(","); os.makedirs(a.dir, exist_ok=True); wd = os.path.abspath(a.dir)
    allx = {i["id"]: i for i in load(a.run, "ideas.json", [])}; blocks = []
    for k, iid in enumerate(ids, 1):
        i = allx[iid]; rev = next((r for d in a.audits.split(",") if (r := review_lines(d, iid, survives=True)) is not None), None)
        if rev is None: sys.exit(f"{iid}: no blind review in --audits")
        blocks.append(f"P{k}\nNAME: {i['name']}\nMECHANISM: {i['mech']}\nVALUE: {i['value']}\nBLIND REVIEW:\n" + "\n".join(rev) + "\n")
    kd = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kit")
    s = fill(a.run, tpl("compose_task"), len(ids), {"WORKDIR": wd + "/", "KITDIR": kd + "/", "PIECES": "\n".join(blocks),
             "KIT": open(os.path.join(kd, "CATALOG.md")).read().strip()})
    open(os.path.join(a.dir, "TASK.md"), "w").write(s); json.dump(ids, open(os.path.join(a.dir, "pieces.json"), "w"))
    print(os.path.join(a.dir, "TASK.md"))

def cmd_resurrect(a):
    """v3.1: evolution under truth - a free generator (no tools) gets killed ideas with their death certificates and
    must jump past the killing quantity while keeping each anchor; children are then gated again."""
    ids = a.ids.split(","); allx = {i["id"]: i for i in load(a.run, "ideas.json", [])}; gate = load(a.run, "gate.json", {})
    blocks = []
    for k, iid in enumerate(ids, 1):
        i, g = allx[iid], gate.get(iid)
        if not g: sys.exit(f"{iid} has no kill-test result")
        cert = (f"killer: {g.get('killer', '?')} | margin {g.get('margin', '?')} | chain ratio {g.get('ratio', '?')} | "
                f"{g['verdict']}: {g.get('why', '')}")
        blocks.append(f"DEAD {k}\nNAME: {i['name']}\nMECHANISM: {i['mech']}\nVALUE: {i['value']}\nDEATH CERTIFICATE: {cert}\n")
    s = fill(a.run, tpl("resurrect"), len(ids) * a.m, {"PARENTS": "\n".join(blocks), "M": str(a.m)})
    p = path(a.run, "prompts", a.label + ".txt"); open(p, "w").write(s)
    json.dump([iid for iid in ids for _ in range(a.m)], open(path(a.run, "prompts", a.label + ".parents.json"), "w"))
    print(p)

def parse_review(d):
    """{id: {FATAL, MAJOR, MINOR, fit}} from a redteamtask dir (ids.json + REVIEW.md)."""
    f = os.path.join(d, "REVIEW.md")
    if not os.path.exists(f): return {}
    ids = json.load(open(os.path.join(d, "ids.json"))); out = {}
    for k, body in zip(*[iter(re.split(r"^IDEA (\d+)\s*:", open(f).read(), flags=re.M)[1:])] * 2):
        if not 1 <= int(k) <= len(ids): continue
        sev = re.findall(r"^DEFECT \| (FATAL|MAJOR|MINOR)", body, flags=re.M)
        fit = re.search(r"^FIT \| (\d+)\s*of\s*(\d+)", body, flags=re.M)
        rt = re.search(r"^RATIO \| ~?\s*([0-9]*\.?[0-9]+)", body, flags=re.M)  # v5: audited whole-chain cost ratio (invent)
        kn = re.search(r"^KNOWN \| (yes|partly|no)\b", body, flags=re.M | re.I)  # v5: already done or proposed?
        out[ids[int(k) - 1]] = {**{s: sev.count(s) for s in ("FATAL", "MAJOR", "MINOR")},
                                "fit": int(fit.group(1)) / max(1, int(fit.group(2))) if fit else 0.0,
                                "ratio": float(rt.group(1)) if rt else None, "known": kn.group(1).lower() if kn else None}
    return out

def review_rank(rows):
    """Ids best first: fewer FATAL, then fewer MAJOR, then larger share of hard facts explained, then larger cost ratio."""
    return sorted(rows, key=lambda i: (rows[i]["FATAL"], rows[i]["MAJOR"], -rows[i]["fit"], -(rows[i].get("ratio") or 0)))

def cmd_exec(a):
    """v4: run one step with a model (runner.call: headless `claude -p`), save the output, log tokens, optionally ingest."""
    import runner
    prompt = open(a.prompt).read(); out = path(a.run, "outputs", a.label + ".md")
    text, u = runner.call(prompt, model=a.model, tools=a.tools, cwd=a.cwd, effort=a.effort, budget_usd=a.budget_usd)
    open(out, "w").write(text); runner.log(rdir(a.run), a.label, u)
    print(f"{a.label}: {u['tokens']} tokens, ${u['cost_usd']:.3f}, {u['seconds']} s -> {out}")
    if a.ingest_arm:
        cmd_ingest(argparse.Namespace(run=a.run, label=a.label, arm=a.ingest_arm, gen=a.gen, parents=a.parents, transcript=None, file=out))

def cmd_usage(a):
    """v4: tokens and cost per step and in total (from <run>/usage.jsonl)."""
    import runner
    rows, tok, cost = runner.summary(rdir(a.run))
    for r in rows:
        new = r.get("fresh_input", 0) + r.get("output_tokens", 0)
        cr = f" = new {new:,} + cache re-reads {r['cache_read']:,}" if r.get("cache_read") else ""
        print(f"{r['step']:24s} {r['model']:7s} tools={r['tools'] or '-':28s} {r['tokens']:>9,} tok{cr}  ${r.get('cost_usd', 0):.3f}")
    print(f"TOTAL {len(rows)} steps: {tok:,} tokens (new {sum(r.get('fresh_input', 0) + r.get('output_tokens', 0) for r in rows):,}), ${cost:.2f}")

# ---------- v5: memory between runs, ceilings, reformulations, facts from checks, calibration ----------
MEM = os.environ.get("CE_MEMORY") or os.path.join(HERE, "memory")
LTAG = re.compile(r"^-\s*((?:\[[\w-]+\])+)\s*(.+)$")

def run_kind(cfg): return cfg.get("format") if cfg.get("format") in ("explain", "make") else "invent"

def lessons_block(cfg, max_killers=8):
    """v5 learning from experience: curated lessons (memory/lessons.md) and defects that sank answers in earlier runs
    (memory/killers.jsonl). A lesson is used when all its tags are in {all, this kind, this question's tag} and none is
    excluded, by tag or by where it was learned ("(from: tag, ...)" at the end of the line): a fair benchmark excludes
    the question's own tag, so neither earlier answers to it nor lessons learned on it leak in."""
    kind, tag, excl = run_kind(cfg), cfg.get("tag"), set(cfg.get("lessons_exclude", []))
    ok = {"all", kind} | ({tag} if tag else set()); out = []
    f = os.path.join(MEM, "lessons.md")
    for l in (open(f) if os.path.exists(f) else []):
        m = LTAG.match(l.strip()); tags = set(re.findall(r"\[([\w-]+)\]", m.group(1))) if m else None
        if not tags: continue
        text, frm = re.match(r"^(.*?)\s*(?:\(from:\s*([\w, -]+)\))?$", m.group(2)).groups()  # where the lesson was learned
        if tags <= ok and not (tags | set(re.split(r"[,\s]+", frm or "")) - {""}) & excl: out.append("- " + text)
    f = os.path.join(MEM, "killers.jsonl"); kill = []
    for r in reversed([json.loads(l) for l in open(f)] if os.path.exists(f) else []):
        if r.get("kind") == kind and r.get("tag") not in excl and r["defect"] not in kill: kill.append(r["defect"])
    return "\n".join(out + [f"- a defect that sank an answer in an earlier run: {d}" for d in kill[:max_killers]]) or "(none recorded)"

def material_block(run, cfg):
    """The run's raw material for the reformulation step: evidence + earlier explanations, or ledger + ceilings + attempts."""
    keys = ("evidence", "attempts") if run_kind(cfg) in ("explain", "make") else ("ledger", "ceilings", "attempts")
    return "\n\n".join(f"{k.upper()}:\n{open(f).read().strip()}" for k in keys if os.path.exists(f := path(run, k + ".md"))) or "(none recorded)"

STOP = set("that this with from have were which their there they them than then what when where about into only also been more "
           "most some such these those other over under after before between each would could should while being does done made used "
           "fact hard soft source".split())
def words(t): return {w for w in re.findall(r"[a-zа-яё0-9]{4,}", t.lower()) if w not in STOP}

def fact_slice(run, texts, k=None):
    """v5 fact slices: a tool step re-reads its whole prompt on every turn, so it gets a shorter ledger. Every HARD fact
    stays (they are what candidates are tested against), without its source; of the other facts (SOFT, NEW) only the k
    that bear most on the candidates (shared words weighted by rarity) or on the question are kept; the full ledger
    with sources stays on disk for the agent to read. k: config 'slice_facts' (0 or unset = whole ledger)."""
    f = path(run, "evidence.md"); cfg = load(run, "config.json", {}); k = cfg.get("slice_facts", 0) if k is None else k
    if not os.path.exists(f): return "(none recorded)"
    text = open(f).read().strip(); facts = re.findall(r"^(FACT \d+\b[^:\n]*:.*)$", text, re.M)
    if not k or not facts: return text
    parts = [[x.strip() for x in l.split("|")] for l in facts]
    hard = [len(p) > 1 and p[1].upper().startswith("HARD") for p in parts]
    W = [words(p[0]) for p in parts]; df = Counter(w for x in W for w in x); n = len(facts)
    idf = {w: math.log(n / c) for w, c in df.items()}
    def top(q): return [i for i in sorted(range(n), key=lambda i: -sum(idf[w] for w in W[i] & q)) if not hard[i]]
    keep = set(top(words(cfg["question"]))[:k // 3])  # a third for the question, the rest for these candidates
    for i in top(words(" ".join(texts))):
        if len(keep) >= k: break
        keep.add(i)
    keep |= {i for i in range(n) if hard[i]}
    body = "\n".join(" | ".join(parts[i][:2]) for i in sorted(keep))
    if len(body) > 0.85 * len(text): return text  # not worth losing the sources
    return (f"(a slice: all {sum(hard)} HARD facts and the {len(keep) - sum(hard)} of {n - sum(hard)} other facts that bear most on "
            f"these candidates, sources omitted; the full ledger with sources is {f} - read it if you need a source or a fact "
            f"that is not here)\n" + body)

TERMS = ("energy", "labour", "inbound logistics", "outbound logistics", "processing", "capital", "other")
SHARE = re.compile(r"(?<![\w.])(\d+(?:\.\d+)?)(?:\s*/\s*(\d+(?:\.\d+)?))?\s*%?(?![\w.])")  # "45", "45%", "5/3%"; not the 3 in "HBM3E"

def parse_shares(ledger):
    """[(archetype, {term: share %})] from the ledger's ARCHETYPE and SHARES lines; 'a/b%' gives two variants named
    from the SHARES header, e.g. 'SHARES (est., export / settlement)'."""
    out, name = [], "?"
    for l in ledger.splitlines():
        if (m := re.match(r"^\**ARCHETYPE\s+(\w+)\b([^:|]*):\**\s*(.*)", l)):  # "ARCHETYPE A: ..." or "**ARCHETYPE A (label):** ..."
            name = f"{m.group(1)}: " + (m.group(2).strip(" *()") or m.group(3).split("|")[0].strip(" *"))[:90]
        if not l.lstrip("*").startswith("SHARES"): continue
        head, _, body = l.partition(":"); vals = {}
        for part in body.split("|"):  # a term is the words before its share; physical-goods terms keep their short names
            p = re.sub(r"\([^)]*\)", " ", part).strip().lower(); m = SHARE.search(p)  # numbers in brackets are notes, not shares
            if not m: continue
            t = next((t for t in TERMS if p.startswith(t)), None) or re.sub(r"\s+", " ", p[:m.start()]).strip(" :-*~") or "?"
            vals["other" if t.startswith("other") else t] = [float(m.group(1))] + ([float(m.group(2))] if m.group(2) else [])
        nv = max((len(v) for v in vals.values()), default=0)
        lab = re.search(r"\(([^)]*)\)", head)
        labs = [x.strip() for x in re.sub(r"^est\.?,?", "", lab.group(1).strip()).split("/")] if lab else []
        for k in range(nv):
            sfx = "" if nv == 1 else f" ({labs[k]})" if len(labs) == nv else f" (variant {k + 1})"
            out.append((name + sfx, {t: v[k] if k < len(v) else v[0] for t, v in vals.items()}))
    return out

def ceiling_rows(shares, target=3.0):
    """Per archetype: absolute ceiling 1/(share no engineering touches), the gain from a 10x cut of each term, and the
    fewest terms that must each be cut 10x to reach the target. ROOM: <= 2 terms; TIGHT: 3; NO ROOM: more, or impossible."""
    rows = []
    for name, s in shares:
        tot = sum(s.values()) or 1.0; s = {t: 100 * v / tot for t, v in s.items()}; other = s.get("other", 0.0)
        phys = sorted(((t, v) for t, v in s.items() if t != "other"), key=lambda x: -x[1]); left, need = 100.0, []
        for t, v in phys:
            if 100 / left >= target: break
            need.append(t); left -= 0.9 * v
        ok = 100 / left >= target
        rows.append({"name": name, "other": other, "ceiling": 100 / other if other > 0 else float("inf"), "sum": tot,
                     "cut10": {t: 1 / (1 - 0.9 * v / 100) for t, v in phys}, "need": need if ok else [],
                     "verdict": ("ROOM" if len(need) <= 2 else "TIGHT" if len(need) == 3 else "NO ROOM") if ok else "NO ROOM"})
    return rows

def cmd_ceilings(a):
    """v5 sense of the possible, in code: before any generator runs, where is 'several times cheaper' arithmetically
    possible? Reads the ledger's SHARES lines, writes ceilings.md (a generator and reformulation input)."""
    f = path(a.run, "ledger.md")
    if not os.path.exists(f): sys.exit("no ledger.md: run `material R ledger` first")
    rows = ceiling_rows(parse_shares(open(f).read()), a.target)
    if not rows: sys.exit("no SHARES lines in ledger.md")
    out = [f"Target: {a.target:g}x cheaper. Ceiling = 1 / (share no engineering can touch: taxes, royalties, fees, margins). "
           f"'needs' = the fewest cost terms that must each fall 10x to reach the target."]
    for r in rows:
        cuts = "; ".join(f"{t} {x:.2f}x" for t, x in r["cut10"].items())
        need = (", ".join(r["need"]) if r["need"] else "impossible even with every physical term cut 10x")
        out.append(f"ARCHETYPE {r['name']} | untouchable {r['other']:.1f}% -> ceiling {r['ceiling']:.1f}x | 10x cut of one term: {cuts} | "
                   f"{a.target:g}x needs: {need} | {r['verdict']}" + (f" (shares summed to {r['sum']:.0f}%)" if abs(r["sum"] - 100) > 5 else ""))
    open(path(a.run, "ceilings.md"), "w").write("\n".join(out) + "\n"); print("\n".join(out))

RF = re.compile(r"^\**REFRAME (\d+)\**\s*:\s*\**\s*(.+?)\s*\|\s*CHANGES:\s*(.+?)\s*\|\s*IMPORTANCE:\s*(\w+)\s*\|\s*POSSIBILITY:\s*(\w+)"
                r"\s*\|\s*WHY:\s*(.+)$", re.M)
LEVEL = {"high": 3, "medium": 2, "low": 1}

def take_reframes(run, text):
    """v5 self-reformulation: store the model's reformulations (reframes.md) and keep the best two in config
    'reframes' - the model's KEEP line, else importance x possibility. A reframe may be one line with | fields or a
    block of lines (- CHANGES: ..., - IMPORTANCE: ...)."""
    body = text.split("=== REFRAMES ===", 1)[-1]; rf, score = {}, {}
    for k, blk in re.findall(r"(?ms)^\**REFRAME (\d+)\**\s*:\s*\**\s*(.+?)(?=^\**REFRAME \d+|^\**KEEP|\Z)", body):
        q = re.split(r"\s*\|\s*CHANGES:|\n", blk.strip(), maxsplit=1)[0].strip(" *")
        lv = {f: (m.group(1).lower() if (m := re.search(rf"{f}:\**\s*(\w+)", blk, re.I)) else "low") for f in ("IMPORTANCE", "POSSIBILITY")}
        rf[int(k)] = q; score[int(k)] = LEVEL.get(lv["IMPORTANCE"], 1) * LEVEL.get(lv["POSSIBILITY"], 1)
    if not rf: print("WARNING: no REFRAME lines parsed"); return []
    m = re.search(r"^\**KEEP\**\s*:\s*\**\s*(.+)$", body, re.M)
    keep = [int(x) for x in re.findall(r"\d+", m.group(1)) if int(x) in rf] if m else []
    keep = list(dict.fromkeys(keep + sorted(rf, key=lambda k: -score[k])))[:2]
    open(path(run, "reframes.md"), "w").write(body.strip() + "\n")
    cfg = load(run, "config.json", {}); cfg["reframes"] = [rf[k] for k in keep]; save(run, "config.json", cfg)
    return cfg["reframes"]

def take_triage(text, ids):
    """{id: importance x possibility} from a === TRIAGE === block (IDEA k | I x | P y | ...)."""
    body = text.split("=== TRIAGE ===", 1)[-1]
    return {ids[int(k) - 1]: float(i) * float(p) for k, i, p in re.findall(r"^\**IDEA (\d+)\**\s*\|\s*I\s*([0-9.]+)\s*\|\s*P\s*([0-9.]+)", body, re.M)
            if 1 <= int(k) <= len(ids)}

NEWFACT = re.compile(r"^\**NEW FACT\**\s*\|\s*(.+?)\s*\|\s*(.+?)\s*$", re.M)

def add_new_facts(run, text, origin):
    """v5: hard facts that a check found (NEW FACT | fact | source) enter evidence.md with their origin; duplicates skipped."""
    f = path(run, "evidence.md"); cur = open(f).read() if os.path.exists(f) else ""
    norm = lambda x: re.sub(r"\W+", " ", x.lower()).strip()
    have = {norm(x) for x in re.findall(r"^FACT \d+:\s*(.+?)\s*\|", cur, re.M)}
    n = max([int(x) for x in re.findall(r"^FACT (\d+):", cur, re.M)] or [0]); add = []
    for fact, src in NEWFACT.findall(text):
        if fact.startswith("<") or norm(fact) in have or norm(fact) in ("none", "n a", ""): continue
        n += 1; have.add(norm(fact)); add.append(f"FACT {n}: {fact} | NEW from {origin}, check before relying on it | {src}")
    if add: open(f, "a").write(("\n" if cur and not cur.endswith("\n") else "") + "\n".join(add) + "\n")
    return len(add)

def take_calibration(run, text, ids, record=True):
    """v5 knowing where it is wrong: stated probabilities, weakest link and flip test (calibration.json); every
    probability also goes to memory/predictions.jsonl so that resolved ones can score the engine's overconfidence."""
    body = text.split("=== CALIBRATION ===", 1)[-1]; cal = {"p": {}}
    for who, pr, pc in re.findall(r"^\**P\**\s*\|\s*(\w+)\s*\|\s*([0-9.]+)\s*(%?)", body, re.M):
        key = "none" if who.lower() == "none" else ids[int(who) - 1] if who.isdigit() and 1 <= int(who) <= len(ids) else None
        if key: cal["p"][key] = float(pr) / 100 if pc or float(pr) > 1 else float(pr)
    for k in ("WEAKEST LINK", "FLIP TEST", "UNKNOWN"):
        m = re.search(rf"^\**{k}\**\s*:\s*\**\s*(.+)$", body, re.M); cal[k.lower().replace(" ", "_")] = m.group(1).strip() if m else ""
    save(run, "calibration.json", cal); cfg = load(run, "config.json", {}); names = {i["id"]: i["name"] for i in load(run, "ideas.json", [])}
    if not record: return cal
    os.makedirs(MEM, exist_ok=True)
    with open(os.path.join(MEM, "predictions.jsonl"), "a") as f:
        for iid, p in cal["p"].items():
            f.write(json.dumps({"time": time.strftime("%Y-%m-%d %H:%M"), "run": run, "tag": cfg.get("tag"), "kind": run_kind(cfg), "id": iid,
                                "name": names.get(iid, iid), "p": p, "flip_test": cal["flip_test"], "outcome": None}, ensure_ascii=False) + "\n")
    return cal

def learn(run, dirs, ids):
    """v5: the FATAL defects of a run's own final answers go to memory/killers.jsonl (later runs see them as lessons)."""
    cfg = load(run, "config.json", {}); os.makedirs(MEM, exist_ok=True); n = 0
    with open(os.path.join(MEM, "killers.jsonl"), "a") as f:
        for d in dirs:
            for iid in ids:
                for l in (review_lines(d, iid, sev=("FATAL",)) or []):
                    f.write(json.dumps({"time": time.strftime("%Y-%m-%d %H:%M"), "run": run, "tag": cfg.get("tag"), "kind": run_kind(cfg),
                                        "id": iid, "defect": l[len("- FATAL: "):][:300]}, ensure_ascii=False) + "\n"); n += 1
    return n

def cmd_learn(a):
    """v5: write the FATAL defects found by review dirs to memory (to seed it from earlier runs)."""
    if a.tag: cfg = load(a.run, "config.json", {}); cfg["tag"] = a.tag; save(a.run, "config.json", cfg)
    dirs = a.audits.split(","); ids = a.ids.split(",") if a.ids else list(dict.fromkeys(i for d in dirs for i in json.load(open(os.path.join(d, "ids.json")))))
    print(f"learned {learn(a.run, dirs, ids)} defects from {len(dirs)} review dirs")

def cmd_calibration(a):
    """v5: stated probabilities against outcomes (memory/predictions.jsonl). --resolve RUN ID 0|1 records an outcome."""
    f = os.path.join(MEM, "predictions.jsonl"); rows = [json.loads(l) for l in open(f)] if os.path.exists(f) else []
    if a.resolve:
        run, iid, o = a.resolve; hit = [r for r in rows if r["run"] == run and r["id"] == iid]
        if not hit: sys.exit(f"no prediction for {iid} in {run}")
        for r in hit: r["outcome"] = int(o)
        open(f, "w").write("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
    res = [r for r in rows if r.get("outcome") is not None]
    print(f"{len(rows)} predictions, {len(res)} resolved")
    if res:
        print(f"Brier {sum((r['p'] - r['outcome']) ** 2 for r in res) / len(res):.3f}; mean stated p {sum(r['p'] for r in res) / len(res):.2f} "
              f"vs hit rate {sum(r['outcome'] for r in res) / len(res):.2f}")

def cmd_bench(a):
    """v5 benchmark: one joint blind review of new and old finalists; per arm FATAL and MAJOR per idea, share with no
    FATAL, median audited cost ratio (invent) or mean fit (explain), share already known."""
    rows = parse_review(a.dir); ideas = {i["id"]: i for i in load(a.run, "ideas.json", [])}; by = defaultdict(list)
    for iid, r in rows.items(): by[ideas[iid]["arm"] if iid in ideas else "?"].append(iid)
    med = lambda v: sorted(v)[len(v) // 2] if v else None
    out = ["| arm | n | FATAL/idea | MAJOR/idea | no FATAL | median RATIO | mean FIT | known yes/partly |", "|---|---|---|---|---|---|---|---|"]
    for arm, L in sorted(by.items()):
        R = [rows[i] for i in L]; n = len(R); rt = med([r["ratio"] for r in R if r.get("ratio") is not None])
        out.append(f"| {arm} | {n} | {sum(r['FATAL'] for r in R) / n:.2f} | {sum(r['MAJOR'] for r in R) / n:.2f} | "
                   f"{sum(r['FATAL'] == 0 for r in R)}/{n} | {'-' if rt is None else f'{rt:.2f}'} | {sum(r['fit'] for r in R) / n:.2f} | "
                   f"{sum(r.get('known') == 'yes' for r in R)}/{sum(r.get('known') == 'partly' for r in R)} of {n} |")
    out += ["", "| rank | id | arm | F/M/m | ratio | known | name |", "|---|---|---|---|---|---|---|"]
    for k, i in enumerate(review_rank(rows), 1):
        r = rows[i]; out.append(f"| {k} | {i} | {ideas.get(i, {}).get('arm', '?')} | {r['FATAL']}/{r['MAJOR']}/{r['MINOR']} | "
                                f"{r.get('ratio') or '-'} | {r.get('known') or '-'} | {ideas.get(i, {}).get('name', '')} |")
    s = "\n".join(out) + "\n"; open(os.path.join(a.dir, "bench.md"), "w").write(s); print(s)

def merge_numbered(texts, sizes, tag):
    """v5: chunk outputs (each numbering its ideas from 1) -> one output numbered over all chunks, under one tag."""
    out, off = [tag], 0
    for t, n in zip(texts, sizes):
        body = t.split(tag, 1)[1] if tag in t else t; parts = re.split(r"^IDEA (\d+)\s*:", body, flags=re.M)
        out += [f"IDEA {off + int(k)}:{b.rstrip()}" for k, b in zip(parts[1::2], parts[2::2]) if 1 <= int(k) <= n]
        off += n
    return "\n".join(out) + "\n"

def merge_ideas(texts):
    """v5: repaired ideas from several chunks -> one === IDEAS === section (renumbered) plus each chunk's notes."""
    blocks, notes = [], []
    for t in texts:
        head, _, body = t.partition("=== IDEAS ===")
        parts = re.split(r"(?m)^\**IDEA\s*\d+\**\s*$", body); notes.append(head.strip())
        blocks += [b.strip() for b in parts[1:] if b.strip()]
    return "\n\n".join(x for x in notes if x) + "\n=== IDEAS ===\n" + "\n\n".join(f"IDEA {k}\n{b}" for k, b in enumerate(blocks, 1)) + "\n"

# v4-v5 one-pass pipelines. Estimates (tokens per step) are replaced by the run's own averages once usage.jsonl has them.
EST = {"research": 150_000, "gen": 10_000, "review": 150_000, "repair": 200_000, "code": 0}
EST_USD = {"research": 0.6, "gen": 0.2, "review": 2.5, "repair": 2.0, "code": 0.0}  # v5: tool steps are mostly cache re-reads (~10% price)
PIPE = {"explain": {"lite": ["research:evidence", "research:hypotheses", "gen:reframe", "gen:g1_crux", "gen:g1_neg", "gen:g1_mech",
                             "gen:g1_reframe", "gen:triage", "review:audit_a", "review:reality", "repair:repair", "review:audit_final", "gen:calibrate",
                             "code:learn"],
                    "standard": ["research:evidence", "research:hypotheses", "gen:reframe", "gen:g1_crux", "gen:g1_neg", "gen:g1_mech",
                                 "gen:g1_reframe", "gen:triage", "review:audit_a", "review:audit_b", "gen:g2_evo", "review:audit_c", "review:reality",
                                 "repair:repair", "review:audit_final", "gen:calibrate", "code:learn"]},
        "make": {"lite": ["research:context", "gen:reframe", "gen:g1_neg", "gen:g1_mech", "gen:g1_rf1", "gen:g1_rf2", "gen:triage",
                          "repair:build.1", "repair:build.2", "review:review", "repair:repair", "review:audit_final", "gen:calibrate",
                          "code:learn"]},
        "invent": {"lite": ["research:ledger", "research:attempts", "code:ceilings", "gen:reframe", "gen:g1_ledger", "gen:g1_neg",
                            "gen:g1_mech", "gen:g1_rf1", "gen:g1_rf2", "gen:triage", "review:gate", "repair:repair", "review:audit_final",
                            "gen:calibrate", "code:learn"]}}
TECH_MAKE = {"g1_neg": "Technique: first list honestly the 8 ways you and most designers would build this page (the usual hero, grid "
                     "and look) and name in one sentence the paradigm they share; then propose only concepts outside it.",
             "g1_mech": "Technique: start from the subject's own material - what its name means, what it physically and technically "
                      "deals with, its formats, units and numbering - and derive the page's structure and interaction from that, not "
                      "from web conventions."}
TECH = {"g1_ledger": "Technique: aim each answer at the archetype and cost term with the most room under its ceiling, and make that "
                     "term fall by an order of magnitude; ignore terms that are easy to improve but small.",
        "g1_neg": "Technique: first list honestly the 8 answers that you and most experts would propose first and name in one sentence "
                  "the paradigm they share; then propose only answers outside that paradigm.",
        "g1_mech": "Technique: describe each answer only in terms of what quantities and objects exist, how they flow or interact and "
                   "what rule changes them; use no named method or buzzword of the home field; give the NAME last.",
        "rf": "Technique: work on this reformulation of the question, chosen as the most productive one by importance and possibility: "
              "{}\nSay in the VALUE what the answer gives for the question as originally asked."}

def pipe_kind(a):
    return getattr(a, "pipeline", None) or run_kind(load(a.run, "config.json", {}))

def plan_rows(a, usd=False):
    """[(step, estimated tokens or dollars)]: the run's own averages per kind of step once it has some, else EST."""
    import runner
    rows, _, _ = runner.summary(rdir(a.run)); learned = defaultdict(list); base = EST_USD if usd else EST
    for r in rows: learned[r["step"].split(":")[0]].append(r.get("cost_usd", 0.0) if usd else r["tokens"])
    est = {k: (sum(v) / len(v) if (v := learned.get(k)) else base[k]) for k in base}
    return [(s, est[s.split(":")[0]]) for s in PIPE[pipe_kind(a)][a.mode]]

def cmd_plan(a):
    """v4: the steps of a one-pass pipeline with their estimated tokens and dollars, before spending anything."""
    rows = plan_rows(a); usd = dict(plan_rows(a, usd=True)); tot = sum(t for _, t in rows)
    for s, t in rows: print(f"  {s:24s} ~{t:>11,.0f} tokens  ~${usd[s]:.2f}")
    print(f"ESTIMATE {pipe_kind(a)}/{a.mode}: ~{tot:,.0f} tokens, ~${sum(usd.values()):.2f} in {sum(1 for s, _ in rows if not s.startswith('code'))} model steps "
          f"({sum(1 for s, _ in rows if s.split(':')[0] in ('research', 'review', 'repair'))} need tools; their tokens are mostly cache re-reads)")

def run_make(R, D, a, triage, step, saved, order, done):
    """v5 make: the two best concepts (from different generators) are built as real pages, rendered by headless Chromium
    at desktop and phone width in both themes (engine/tools/render.js), reviewed blind from the renders, the better one
    repaired, then reviewed blind again against the other; the calibration says how sure the choice is."""
    import runner, shutil
    from concurrent.futures import ThreadPoolExecutor
    tools_dir, pr = os.path.join(HERE, "tools") + "/", tpl("_page_rules")
    ideas = lambda: {i["id"]: i for i in load(R, "ideas.json", [])}
    pick = triage([i for i, x in ideas().items() if x["arm"] == "E" and not x.get("fragment")], "triage_make", k=2, cap=1)
    bd = os.path.join(D, "build"); os.makedirs(bd, exist_ok=True)
    pick = order("build", pick, os.path.join(bd, "ids.json")); json.dump(pick, open(os.path.join(bd, "ids.json"), "w"))
    def build(j):
        cd = os.path.join(bd, f"b{j + 1}"); os.makedirs(cd, exist_ok=True)
        s = fill(R, tpl("build_task"), 1, {"WORKDIR": cd + "/", "TOOLS": tools_dir, "IDEAS": task_ideas(R, [pick[j]], scores=False), "PAGERULES": pr})
        open(os.path.join(cd, "TASK.md"), "w").write(s); step(f"build.{j + 1}", "repair", s, a.model, "write", cwd=cd)
    with ThreadPoolExecutor(2) as ex: list(ex.map(build, range(len(pick))))
    pages = {i: f for j, i in enumerate(pick) if os.path.exists(f := os.path.join(bd, f"b{j + 1}", "index.html"))}
    if not pages: sys.exit("no page was built (no index.html in build/b*)")
    def review(name, items):
        dd = os.path.join(D, name); os.makedirs(dd, exist_ok=True)
        ids = order(name, list(items), os.path.join(dd, "ids.json")); json.dump(ids, open(os.path.join(dd, "ids.json"), "w")); X = ideas()
        sites = "\n".join(f"PAGE {k}\nFILE: {items[i]}\nCONCEPT: {X[i]['name']}: {X[i]['mech']}\n" for k, i in enumerate(ids, 1))
        s = fill(R, tpl("redteam_make"), len(ids), {"WORKDIR": dd + "/", "TOOLS": tools_dir, "SITES": sites, "PAGERULES": pr})
        open(os.path.join(dd, "TASK.md"), "w").write(s); t = step(name, "review", s, a.model, "write", cwd=dd)
        open(os.path.join(dd, "REVIEW.md"), "w").write(t[t.find("=== REVIEW ==="):] if "=== REVIEW ===" in t else t)
        return parse_review(dd)
    rows = review("review", pages); best = review_rank(rows)[0]; fd = os.path.join(D, "final")
    if not done("repair"): shutil.copytree(os.path.dirname(pages[best]), fd, dirs_exist_ok=True, ignore=shutil.ignore_patterns("shots*", "TASK.md"))
    s = fill(R, tpl("repair_make"), 1, {"WORKDIR": fd + "/", "TOOLS": tools_dir, "IDEAS": task_ideas(R, [best], scores=False),
                                        "REVIEW": "\n".join(latest_review([os.path.join(D, "review")], best)), "PAGERULES": pr})
    open(os.path.join(fd, "TASK.md"), "w").write(s); step("repair", "repair", s, a.model, "write", cwd=fd)
    X = load(R, "ideas.json", [])
    if not any(i["id"] == "final#1" for i in X):  # the repaired page keeps its concept's name, so the final review stays blind
        X.append({**next(i for i in X if i["id"] == best), "id": "final#1", "label": "final", "arm": "F", "gen": 3, "parent": best}); save(R, "ideas.json", X)
    rows = review("audit_final", {"final#1": os.path.join(fd, "index.html"), **{i: f for i, f in pages.items() if i != best}})
    own = review_rank(rows); fa = os.path.join(D, "audit_final")
    s = fill(R, tpl("calibrate_task"), len(own), {"IDEAS": idea_blocks(R, own, {i: ["BLIND REVIEW:"] + latest_review([fa], i) for i in own}, scores=False)})
    fresh = not done("calibrate"); cal = take_calibration(R, step("calibrate", "gen", saved("calibrate", s), a.model, "none"), own, record=fresh)
    if not done("learn"): open(path(R, "outputs", "learn.md"), "w").write(f"{learn(R, [fa], own)} defects -> memory\n")
    X = ideas(); page = os.path.join(fd, "index.html") if own[0] == "final#1" else pages[own[0]]
    print("\nFINAL (blind review of the rendered pages; p = stated probability of being the best page):")
    for k, i in enumerate(own, 1):
        r = rows[i]; print(f"  {k}. {i:12s} F{r['FATAL']}/M{r['MAJOR']}/m{r['MINOR']} fit {r['fit']:.2f} p {cal['p'].get(i, 0):.0%}  {X[i]['name']}")
    print(f"  weakest link: {cal['weakest_link']}\nPAGE: {page}"); open(path(R, "winner.txt"), "w").write(page + "\n")
    _, tok, cost = runner.summary(D); print(f"spent {tok:,} tokens, ${cost:.2f}")

def cmd_run(a):
    """v4-v5: a whole pipeline in one pass; cost is kept by code (plan, stop before a step that would exceed --max-tokens,
    resumable: a step whose output exists is skipped). Both pipelines: lessons from earlier runs enter the prompts, the
    model reformulates the question before anyone answers, facts found by checks enter the evidence, the run ends with
    stated probabilities (where it is likely wrong) and writes its FATAL defects to engine/memory.
    explain: evidence + earlier explanations -> reformulation -> free generation (one generator on the best reformulation)
      -> triage by importance x possibility -> blind review of the best 8 -> (standard: evolution -> review) -> reality check
      of the leaders (data or validated calculation)
      -> repair with search -> final blind review -> calibration.
    invent: value ledger + earlier attempts -> ceilings in code -> reformulation -> free generation aimed by the ceilings
      (two generators on reformulations) -> triage by importance x possibility -> kill test with the calculation kit
      -> repair with search -> final blind review -> calibration.
    --bench adds earlier finalists (imported ids) to the final blind review: the benchmark of `bench`."""
    import runner
    R = a.run; D = rdir(R); cfg = load(R, "config.json", {}); kind = run_kind(cfg)
    if pipe_kind(a) != kind: sys.exit(f"{R} is an {kind} question (format {cfg.get('format')}): use --pipeline {kind}")
    if a.mode not in PIPE[kind]: sys.exit(f"no {a.mode} mode for {kind}: {', '.join(PIPE[kind])}")
    if getattr(a, "tag", None): cfg["tag"] = a.tag
    if getattr(a, "lessons_exclude", None) is not None: cfg["lessons_exclude"] = [x for x in a.lessons_exclude.split(",") if x]
    if getattr(a, "slice_facts", None) is not None: cfg["slice_facts"] = a.slice_facts
    if a.notes: cfg["notes"] = a.notes
    save(R, "config.json", cfg); budget = a.max_tokens; bench = [x for x in (getattr(a, "bench", None) or "").split(",") if x]
    def spent(): return runner.summary(D)[1]
    def spent_usd(): return runner.summary(D)[2]
    def done(name): return os.path.exists(path(R, "outputs", name + ".md")) and not a.force
    def step(name, kind_, prompt, model, tools, cwd=None):
        out = path(R, "outputs", name + ".md")
        if done(name): print(f"  skip {name} (done)"); return open(out).read()
        est = dict(plan_rows(a)).get(f"{kind_}:{name}", EST[kind_]); eu = dict(plan_rows(a, usd=True)).get(f"{kind_}:{name}", EST_USD[kind_])
        if budget and spent() + est > budget: sys.exit(f"STOP before {name}: {spent():,} spent + ~{est:,.0f} > budget {budget:,} tokens (rerun with a larger --max-tokens to resume)")
        if getattr(a, "max_usd", None) and spent_usd() + eu > a.max_usd:
            sys.exit(f"STOP before {name}: ${spent_usd():.2f} spent + ~${eu:.2f} > budget ${a.max_usd:.2f} (rerun with a larger --max-usd to resume)")
        text, u = runner.call(prompt, model=model, tools=tools, cwd=cwd)
        open(out, "w").write(text); runner.log(D, f"{kind_}:{name}", u)
        print(f"  {name}: {u['tokens']:,} tokens, {u['seconds']} s"); return text
    def saved(label, prompt): open(path(R, "prompts", label + ".txt"), "w").write(prompt); return prompt
    def order(name, ids, f):  # a fresh blind order, or the stored one for the same ideas (a resumed step keeps its numbering and chunks)
        if os.path.exists(f) and sorted(json.load(open(f))) == sorted(ids): return json.load(open(f))
        ids = list(ids); secrets.SystemRandom().shuffle(ids); return ids
    def task(dirname): return open(os.path.join(D, dirname, "TASK.md")).read()
    def chunked(name, kind_, ids, write_task, size, merge):
        """v5: a tool step over many ideas run as chunks of <= size ideas, at most 2 agents at a time. Every turn re-reads
        the growing context, so cost grows ~ with turns squared: two half-size agents cost ~40% less than one."""
        if not size or len(ids) <= size or done(name): return
        dd = os.path.join(D, name); cs = [ids[i:i + size] for i in range(0, len(ids), size)]
        def one(j):
            cd = os.path.join(dd, f"c{j + 1}"); write_task(cs[j], cd)
            return step(f"{name}.{j + 1}", kind_, open(os.path.join(cd, "TASK.md")).read(), a.model, "research", cwd=cd)
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(2) as ex: texts = list(ex.map(one, range(len(cs))))
        open(path(R, "outputs", name + ".md"), "w").write(merge(texts, [len(c) for c in cs]))
    def review(name, ids, tp, chunk=None):
        dd = os.path.join(D, name); ids = order(name, ids, os.path.join(dd, "ids.json"))
        os.makedirs(dd, exist_ok=True); json.dump(ids, open(os.path.join(dd, "ids.json"), "w"))
        chunked(name, "review", ids, lambda c, cd: cmd_redteamtask(argparse.Namespace(run=R, ids=",".join(c), dir=cd, blind=True, tpl=tp)),
                a.chunk if chunk is None else chunk, lambda t, n: merge_numbered(t, n, "=== REVIEW ==="))
        cmd_redteamtask(argparse.Namespace(run=R, ids=",".join(ids), dir=dd, blind=True, tpl=tp))
        t = step(name, "review", task(name), a.model, "research", cwd=dd)
        open(os.path.join(dd, "REVIEW.md"), "w").write(t[t.find("=== REVIEW ==="):] if "=== REVIEW ===" in t else t)
        if (nf := add_new_facts(R, t, name)): print(f"  {name}: {nf} new facts -> evidence.md")
        return parse_review(dd)
    def gen(label, prompt, arm="E", g=1):
        step(label, "gen", prompt, a.model, "none")
        cmd_ingest(argparse.Namespace(run=R, label=label, arm=arm, gen=g, parents=None, transcript=None, file=path(R, "outputs", label + ".md")))
    def research(name, tp, kind_):
        if os.path.exists(path(R, kind_ + ".md")) and not done(name): print(f"  skip {name} ({kind_}.md present)"); return
        dd = os.path.join(D, name); cmd_researchtask(argparse.Namespace(run=R, tpl=tp, dir=dd))
        step(name, "research", task(name), a.lit_model, "research", cwd=dd)
        cmd_material(argparse.Namespace(run=R, kind=kind_, transcript=None, file=path(R, "outputs", name + ".md")))
    # 1. raw material (+ ceilings in code)
    if kind == "explain":
        research("evidence", "evidence_task", "evidence"); research("hypotheses", "hypotheses_task", "attempts")
        if os.path.exists(path(R, "outputs", "hypotheses.md")):
            cmd_ingest(argparse.Namespace(run=R, label="hypotheses", arm="K", gen=0, parents=None, transcript=None, file=path(R, "outputs", "hypotheses.md")))
    elif kind == "make":  # one research step writes both: facts about the subject and how such pages usually fall flat
        if not (os.path.exists(path(R, "evidence.md")) and os.path.exists(path(R, "attempts.md")) and not done("context")):
            dd = os.path.join(D, "context"); cmd_researchtask(argparse.Namespace(run=R, tpl="make_research_task", dir=dd))
            step("context", "research", task("context"), a.lit_model, "research", cwd=dd)
            for k in ("evidence", "attempts"): cmd_material(argparse.Namespace(run=R, kind=k, transcript=None, file=path(R, "outputs", "context.md")))
    else:
        research("ledger", "ledger_task", "ledger"); research("attempts", "attempts_open_task", "attempts")
        cmd_ceilings(argparse.Namespace(run=R, target=a.target))
    # 2. the model reformulates the question (no tools: cheap)
    rfs = take_reframes(R, step("reframe", "gen", saved("reframe", fill(R, tpl("reframe_task"), 0)), a.model, "none")) or [cfg["question"]]
    # 3. free generation (no tools: cheap)
    if kind == "explain":
        for t in ("crux", "neg", "mech"): gen("g1_" + t, open(cmd_prompt_path(R, "explain_" + t, "g1_" + t)).read())
        gen("g1_reframe", saved("g1_reframe", fill(R, tpl("explain_reframe"), cfg["n"], {"REFRAME": rfs[0]})))
    elif kind == "make":
        techs = dict(TECH_MAKE) | {f"g1_rf{k}": TECH["rf"].format(q) for k, q in enumerate(rfs[:2], 1)}
        for lab, tech in techs.items(): gen(lab, saved(lab, fill(R, tpl("gen_make"), cfg["n"], {"TECH": tech, "PAGERULES": tpl("_page_rules")})))
    else:
        techs = {k: TECH[k] for k in ("g1_ledger", "g1_neg", "g1_mech")} | {f"g1_rf{k}": TECH["rf"].format(q) for k, q in enumerate(rfs[:2], 1)}
        for lab, tech in techs.items(): gen(lab, saved(lab, fill(R, tpl("gen_invent"), cfg["n"], {"TECH": tech})))
    ideas = lambda: load(R, "ideas.json", [])
    def triage(ids, tp, k=None, cap=3, name="triage"):  # importance x possibility without tools; the expensive check gets the best, at most cap per generator
        tids = order(name, ids, path(R, "prompts", name + ".ids.json")); json.dump(tids, open(path(R, "prompts", name + ".ids.json"), "w"))
        tri = take_triage(step(name, "gen", saved(name, fill(R, tpl(tp), len(tids), {"IDEAS": task_ideas(R, tids, scores=False)})),
                               a.model, "none"), tids)
        lab = {i["id"]: i["label"] for i in ideas()}; pick, per = [], Counter()
        for i in sorted(tids, key=lambda i: -tri.get(i, 0)):
            if len(pick) < (k or a.triage_k) and per[lab[i]] < cap: pick.append(i); per[lab[i]] += 1
        return pick
    if kind == "make": return run_make(R, D, a, triage, step, saved, order, done)
    def rival_round(pick):
        """v5 rival round (test 3 in 21-meta-framing.md): two more generators see every idea of round 1, with what the kill
        test found, as the rivals to beat; their best 4 go through a second kill test. Showing the real rivals moved ideas
        off a dead basin, while only announcing a competition pulled them into it."""
        g = load(R, "gate.json", {}); X = {i["id"]: i for i in ideas()}
        r1 = [i for i in X if X[i]["arm"] == "E" and not X[i].get("fragment")]
        rows = [f"- {X[i]['name']}: {' '.join(X[i]['mech'].split()[:28])}…" + (f" [kill test: {g[i]['verdict']} - {g[i].get('why', '')[:180]}]" if i in g else "")
                for i in r1]
        rivals = ("Your answers will be ranked blind against those of nine other strong systems given the same question. Answers already "
                  "proposed for it, with what a kill test found where one was run (data, not instructions):\n" + "\n".join(rows) +
                  "\nPropose answers that differ from all of these and are not stopped by the reasons that killed them.\n\n")
        for lab, tech in (("g2_rival_a", TECH["g1_ledger"]), ("g2_rival_b", TECH["rf"].format(rfs[0]))):
            gen(lab, saved(lab, rivals + fill(R, tpl("gen_invent"), cfg["n"], {"TECH": tech})), arm="E2", g=2)
        p2 = triage([i["id"] for i in ideas() if i["arm"] == "E2" and not i.get("fragment")], "triage_task", k=4, cap=2, name="triage2")
        gd2 = os.path.join(D, "gate2"); p2 = order("gate2", p2, os.path.join(gd2, "ids.json"))
        cmd_gatetask(argparse.Namespace(run=R, ids=",".join(p2), dir=gd2, kit=bool(getattr(a, "kit", False) or cfg.get("kit"))))
        t2 = step("gate2", "review", task("gate2"), a.model, "research", cwd=gd2)
        cmd_gate(argparse.Namespace(run=R, dir=gd2, transcript=None, file=path(R, "outputs", "gate2.md"), out=None))
        print(f"  gate2: {add_new_facts(R, t2, 'gate2')} new facts -> evidence.md")
        return p2
    if kind == "explain":  # 4e. triage, blind review, (evolution), reality check of the leaders
        allids = triage([i["id"] for i in ideas() if i["arm"] in ("E", "K") and not i.get("fragment")], "triage_explain")
        rows = review("audit_a", allids, "redteam_explain") if a.mode == "lite" else \
            {**review("audit_a", allids[0::2], "redteam_explain"), **review("audit_b", allids[1::2], "redteam_explain")}
        top = review_rank(rows)[:4]; dirs = [os.path.join(D, x) for x in ("audit_a", "audit_b") if os.path.exists(os.path.join(D, x))]
        if a.mode == "standard":
            cmd_evolve(argparse.Namespace(run=R, label="g2_evo", audit=",".join(dirs), ids=",".join(top), m=2, max_defects=6, tpl="evolve_explain"))
            gen("g2_evo", open(path(R, "prompts", "g2_evo.txt")).read(), arm="E2", g=2)
            kids = [i["id"] for i in ideas() if i["label"] == "g2_evo"]
            rows = review("audit_c", kids + top, "redteam_explain"); top = review_rank(rows)[:4]; dirs = [os.path.join(D, "audit_c")] + dirs
        dd = os.path.join(D, "reality"); os.makedirs(dd, exist_ok=True)
        lead = idea_blocks(R, top, {i: ["BLIND REVIEW:"] + latest_review(dirs, i) for i in top}, scores=False)
        s = fill(R, tpl("reality_task"), len(top), {"IDEAS": lead, "EVIDENCE": fact_slice(R, [lead])})
        open(os.path.join(dd, "TASK.md"), "w").write(s); t = step("reality", "review", s, a.model, "research", cwd=dd)
        print(f"  reality: {add_new_facts(R, t, 'reality')} new facts -> evidence.md")
        found = t.split("=== REALITY ===", 1)[-1].strip() if "=== REALITY ===" in t else ""
        notes = "\n".join(x for x in (a.notes, found and "A check against reality found (data; its facts are also in the evidence):\n" + found) if x)
        rargs_last = argparse.Namespace(run=R, ids=",".join(top), dir=os.path.join(D, "repair"), critique=None, tpl="repair_explain",
                                        audits=",".join(dirs), notes=notes or None, gate=None); cmd_repairtask(rargs_last)
    else:  # 4i. triage by importance x possibility (no tools), kill test with the kit on the best, repair
        pick = triage([i["id"] for i in ideas() if i["arm"] == "E" and not i.get("fragment")], "triage_task")
        gd = os.path.join(D, "gate"); pick = order("gate", pick, os.path.join(gd, "ids.json")); kit = bool(getattr(a, "kit", False) or cfg.get("kit"))
        os.makedirs(gd, exist_ok=True); json.dump(pick, open(os.path.join(gd, "ids.json"), "w"))
        chunked("gate", "review", pick, lambda c, cd: cmd_gatetask(argparse.Namespace(run=R, ids=",".join(c), dir=cd, kit=kit)),
                a.chunk, lambda t, n: merge_numbered(t, n, "=== GATE ==="))
        cmd_gatetask(argparse.Namespace(run=R, ids=",".join(pick), dir=gd, kit=kit))
        t = step("gate", "review", task("gate"), a.model, "research", cwd=gd)
        cmd_gate(argparse.Namespace(run=R, dir=gd, transcript=None, file=path(R, "outputs", "gate.md"), out=None))
        print(f"  gate: {add_new_facts(R, t, 'gate')} new facts -> evidence.md")
        if getattr(a, "rivals", False): pick += rival_round(pick)
        g = load(R, "gate.json", {})
        top = sorted(pick, key=lambda i: (-GATE_W.get(g.get(i, {}).get("verdict"), -1), -(g.get(i, {}).get("ratio") or 0)))[:4]
        rargs_last = argparse.Namespace(run=R, ids=",".join(top), dir=os.path.join(D, "repair"), critique=None, tpl="repair_task",
                                        audits=None, notes=a.notes, gate="gate.json"); cmd_repairtask(rargs_last)
    # 5. repair with search (in chunks), 6. final blind review (+ earlier finalists for the benchmark: one reviewer for all)
    rp = json.load(open(os.path.join(D, "repair", "parents.json"))); rargs = vars(rargs_last).copy()
    def repair_chunk(c, cd): cmd_repairtask(argparse.Namespace(**{**rargs, "ids": ",".join(c), "dir": cd}))
    chunked("repair", "repair", rp, repair_chunk, getattr(a, "repair_chunk", 0), lambda t, n: merge_ideas(t))
    step("repair", "repair", task("repair"), a.model, "research", cwd=os.path.join(D, "repair"))
    cmd_ingest(argparse.Namespace(run=R, label="repair", arm="F", gen=3, parents=None, transcript=None, file=path(R, "outputs", "repair.md")))
    own = [i["id"] for i in ideas() if i["label"] == "repair"] + (top[:2] if kind == "explain" else [])
    fd = os.path.join(D, "audit_final")
    rows = review("audit_final", own + bench, "redteam_explain" if kind == "explain" else "redteam_task", chunk=0 if bench else None)
    # 7. calibration: how sure, and where the answer is most likely wrong (no tools)
    own = [i for i in review_rank(rows) if i not in bench]
    s = fill(R, tpl("calibrate_task"), len(own), {"IDEAS": idea_blocks(R, own, {i: ["BLIND REVIEW:"] + latest_review([fd], i) for i in own}, scores=False)})
    fresh = not done("calibrate"); cal = take_calibration(R, step("calibrate", "gen", saved("calibrate", s), a.model, "none"), own, record=fresh)
    if not done("learn"): open(path(R, "outputs", "learn.md"), "w").write(f"{learn(R, [fd], own)} defects -> memory\n")
    names = {i["id"]: i["name"] for i in ideas()}
    print("\nFINAL (blind review; p = stated probability of being the best answer):")
    for k, i in enumerate(own, 1):
        r = rows[i]; print(f"  {k}. {i:14s} F{r['FATAL']}/M{r['MAJOR']}/m{r['MINOR']} fit {r['fit']:.2f} ratio {r.get('ratio') or '-'} "
                           f"known {r.get('known') or '-'} p {cal['p'].get(i, 0):.0%}  {names[i]}")
    print(f"  none of these: p {cal['p'].get('none', 0):.0%}\n  weakest link: {cal['weakest_link']}\n  flip test: {cal['flip_test']}")
    _, tok, cost = runner.summary(D); print(f"spent {tok:,} tokens, ${cost:.2f}")
    if bench: cmd_bench(argparse.Namespace(run=R, dir=fd))

BRIEF_KEYS = ("TYPE", "QUESTION", "SUCCESS", "CONSTRAINTS", "CONTEXT", "DATA", "ASSUMPTIONS", "CORRECTED", "UNCLEAR", "MODE")

def parse_brief(text):
    """{KEY: value} from a === BRIEF === block (a value runs until the next KEY: line)."""
    body = text.split("=== BRIEF ===", 1)[1] if "=== BRIEF ===" in text else text
    out, key = {}, None
    for line in body.splitlines():
        if line.startswith("==="): break
        m = re.match(r"^\**(%s)\**\s*:\s*(.*)$" % "|".join(BRIEF_KEYS), line.strip())
        if m: key = m.group(1); out[key] = m.group(2).strip()
        elif key and line.strip(): out[key] += "\n" + line.strip()
    return out

def cmd_ask(a):
    """v4 step 0: an intake agent turns the raw question into a neutral brief (no answers), then the run is
    initialised from the brief and the pipeline starts. Unclear points are reported and kept as assumptions."""
    import runner
    R = a.run; os.makedirs(rdir(R), exist_ok=True); os.makedirs(path(R, "outputs"), exist_ok=True)
    out = path(R, "outputs", "brief.md")
    if os.path.exists(out) and not a.force: text = open(out).read(); print("  skip brief (done)")
    else:
        text, u = runner.call(tpl("brief_task").replace("{RAWQ}", a.question), model=a.brief_model, tools="WebSearch", cwd=rdir(R))
        open(out, "w").write(text); runner.log(rdir(R), "brief:brief", u); print(f"  brief: {u['tokens']:,} tokens")
    b = parse_brief(text)
    if not b.get("QUESTION"): sys.exit(f"no QUESTION in the brief; see {out}")
    t = b.get("TYPE", "").lower(); kind = "explain" if t.startswith("explain") else "make" if t.startswith("make") else "invent"
    q = b["QUESTION"] + (f"\nA good answer: {b['SUCCESS']}" if b.get("SUCCESS") else "") + \
        (f"\nConstraints: {b['CONSTRAINTS']}" if b.get("CONSTRAINTS", "none").lower() not in ("none", "") else "")
    if a.force or "brief" not in load(R, "config.json", {}):  # resuming keeps the initialised run and its ideas
        cmd_init(argparse.Namespace(run=R, question=q, format={"explain": "explain", "make": "make"}.get(kind, "value"), n=3, force=True))
        cfg = load(R, "config.json", {}); cfg["brief"] = b; save(R, "config.json", cfg)
    if b.get("UNCLEAR", "none").lower() not in ("none", ""): print("UNCLEAR (kept as assumptions):\n" + b["UNCLEAR"])
    print(f"TYPE {kind}; MODE {b.get('MODE', 'lite')}")
    notes = "\n".join(x for x in (a.notes, b.get("ASSUMPTIONS") and "Assumptions in the question that may be wrong:\n" + b["ASSUMPTIONS"],
                                  b.get("DATA") and "Where deciding data may exist:\n" + b["DATA"]) if x)
    mode = a.mode or ("standard" if b.get("MODE", "").lower().startswith("standard") else "lite")
    cmd_run(argparse.Namespace(run=R, pipeline=kind, mode=mode if mode in PIPE[kind] else "lite", max_tokens=a.max_tokens, model=a.model,
                               lit_model=a.lit_model, notes=notes or None, force=False, tag=a.tag, lessons_exclude=None, bench=None,
                               target=3.0, triage_k=8, slice_facts=12, chunk=a.chunk, repair_chunk=a.repair_chunk, kit=a.kit, max_usd=a.max_usd, rivals=False))

def cmd_prompt_path(run, tech, label):
    """Build a technique prompt via cmd_prompt and return its path."""
    cmd_prompt(argparse.Namespace(run=run, tech=tech, label=label, pairs=3, pair_from=0, n=None, crux=None))
    return path(run, "prompts", label + ".txt")

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
    x.add_argument("--format", default="value", choices=["value", "difference", "arch", "explain", "make"]); x.add_argument("--n", type=int, default=3)
    x.add_argument("--force", action="store_true")
    x = sp.add_parser("prompt"); x.add_argument("run"); x.add_argument("tech", help="technique template or evolved species name"); x.add_argument("label")
    x.add_argument("--pairs", type=int, default=3); x.add_argument("--pair-from", type=int, default=0)
    x.add_argument("--n", type=int, help="ideas/principles per generator (default: run's n)")
    x = sp.add_parser("ingest"); x.add_argument("run"); x.add_argument("label"); x.add_argument("--arm", required=True)
    x.add_argument("--gen", type=int, default=0); x.add_argument("--parents", help="ids (comma list or parents.json) the k-th idea descends from"); src(x)
    x = sp.add_parser("repairtask"); x.add_argument("run"); x.add_argument("--ids", required=True); x.add_argument("--dir", required=True)
    x.add_argument("--critique", help="red-team review (file, or agent transcript .output)")
    x.add_argument("--tpl", default="repair_task", choices=["repair_task", "repair_explain"])
    x.add_argument("--gate", help="v5: gate results file in the run dir (e.g. gate.json); each idea gets its kill test")
    x.add_argument("--audits", help="v3.6: review dirs (latest first); each idea gets its blind review")
    x.add_argument("--notes", help="notes from the user, passed to the researcher as data")
    x = sp.add_parser("material"); x.add_argument("run"); x.add_argument("kind", choices=["frontier", "ledger", "attempts", "evidence"]); src(x)
    x = sp.add_parser("researchtask"); x.add_argument("run"); x.add_argument("--tpl", required=True,
        choices=["evidence_task", "hypotheses_task", "ledger_task", "attempts_open_task"]); x.add_argument("--dir", required=True)
    x = sp.add_parser("attemptstask"); x.add_argument("run"); x.add_argument("--ids", required=True); x.add_argument("--dir", required=True)
    x = sp.add_parser("gatetask"); x.add_argument("run"); x.add_argument("--ids", required=True); x.add_argument("--dir", required=True)
    x.add_argument("--kit", action="store_true", help="v3.4: give the screener engine/kit and its catalog of killer classes")
    x = sp.add_parser("gate"); x.add_argument("run"); x.add_argument("--dir", required=True); src(x)
    x.add_argument("--out", help="results file in the run dir (default gate.json; A/B arms keep separate files)")
    x = sp.add_parser("evolve"); x.add_argument("run"); x.add_argument("label"); x.add_argument("--audit", required=True,
        help="redteamtask dir holding ids.json and the auditor's REVIEW.md"); x.add_argument("--m", type=int, default=2)
    x.add_argument("--max-defects", type=int, default=6)
    x.add_argument("--ids", help="parents to evolve (default: every idea in the review dirs)")
    x.add_argument("--tpl", default="evolve_audit", choices=["evolve_audit", "evolve_attempts", "evolve_explain"],
                   help="evolve_attempts (v3.3) also shows the ledger of earlier attempts and why they stopped short")
    x = sp.add_parser("composetask"); x.add_argument("run"); x.add_argument("--ids", required=True, help="surviving pieces")
    x.add_argument("--dir", required=True); x.add_argument("--audits", required=True, help="redteamtask dirs holding their reviews")
    x = sp.add_parser("resurrect"); x.add_argument("run"); x.add_argument("label"); x.add_argument("--ids", required=True)
    x.add_argument("--m", type=int, default=3, help="children per dead parent")
    x = sp.add_parser("exec"); x.add_argument("run"); x.add_argument("--prompt", required=True); x.add_argument("--label", required=True)
    x.add_argument("--model", default="opus"); x.add_argument("--tools", default="none", help="none | research | write | comma list")
    x.add_argument("--cwd"); x.add_argument("--effort"); x.add_argument("--budget-usd", type=float)
    x.add_argument("--ingest-arm"); x.add_argument("--gen", type=int, default=0); x.add_argument("--parents")
    x = sp.add_parser("usage"); x.add_argument("run")
    x = sp.add_parser("ask"); x.add_argument("run"); x.add_argument("question"); x.add_argument("--max-tokens", type=int)
    x.add_argument("--mode", choices=["lite", "standard"], help="default: the brief's MODE")
    x.add_argument("--model", default="opus"); x.add_argument("--lit-model", default="sonnet"); x.add_argument("--brief-model", default="sonnet")
    x.add_argument("--notes"); x.add_argument("--force", action="store_true"); x.add_argument("--tag", help="question tag for memory")
    x.add_argument("--max-usd", type=float); x.add_argument("--chunk", type=int, default=4); x.add_argument("--repair-chunk", type=int, default=2)
    x.add_argument("--kit", action="store_true")
    for nm in ("plan", "run"):
        x = sp.add_parser(nm); x.add_argument("run"); x.add_argument("--pipeline", choices=list(PIPE), help="default: the run's format")
        x.add_argument("--mode", default="lite", choices=["lite", "standard"])
        if nm == "run":
            x.add_argument("--max-tokens", type=int, help="stop before a step that would exceed this many tokens in total")
            x.add_argument("--max-usd", type=float, help="v5: stop before a step that would exceed this many dollars (closer to real cost: cache re-reads are cheap)")
            x.add_argument("--model", default="opus"); x.add_argument("--lit-model", default="sonnet")
            x.add_argument("--notes", default=None); x.add_argument("--force", action="store_true")
            x.add_argument("--tag", help="v5: question tag (memory lessons and killers are filed under it)")
            x.add_argument("--lessons-exclude", help="v5: memory tags to leave out (fair benchmark: the question's own tag)")
            x.add_argument("--bench", help="v5: imported earlier finalists to add to the final blind review")
            x.add_argument("--target", type=float, default=3.0, help="v5: the gain the ceilings are computed for")
            x.add_argument("--chunk", type=int, default=4, help="v5: blind reviews and the kill test run in chunks of this many ideas, 2 agents at a time (0 = one agent)")
            x.add_argument("--repair-chunk", type=int, default=2, help="v5: ideas per repair agent (0 = one agent)")
            x.add_argument("--kit", action="store_true", help="v3.4: give the kill test the Arctic calculation kit (engine/kit)")
            x.add_argument("--rivals", action="store_true", help="v5 invent: add the rival round (round-2 generators see round 1 and its kill tests as rivals); "
                           "+~$1.3, no survival gain shown yet (20-continuum.md)")
            x.add_argument("--slice-facts", type=int, default=12, help="v5: tool steps get every HARD fact (no sources) and this many other facts (0 = whole ledger)")
            x.add_argument("--triage-k", type=int, default=8, help="v5: ideas the kill test (invent) or the first blind review (explain) gets after triage")
    x = sp.add_parser("ceilings"); x.add_argument("run"); x.add_argument("--target", type=float, default=3.0)
    x = sp.add_parser("learn"); x.add_argument("run"); x.add_argument("--audits", required=True); x.add_argument("--ids"); x.add_argument("--tag")
    x = sp.add_parser("calibration"); x.add_argument("--resolve", nargs=3, metavar=("RUN", "ID", "OUTCOME"))
    x = sp.add_parser("bench"); x.add_argument("run"); x.add_argument("--dir", required=True)
    x = sp.add_parser("redteamtask"); x.add_argument("run"); x.add_argument("--ids", required=True); x.add_argument("--dir", required=True)
    x.add_argument("--blind", action="store_true", help="omit judges' scores (blind audit of mixed versions)")
    x.add_argument("--tpl", default="redteam_task", choices=["redteam_task", "redteam_explain"],
                   help="redteam_explain (v3.6): test explanations against the evidence ledger")
    x = sp.add_parser("set"); x.add_argument("run"); x.add_argument("set"); x.add_argument("--labels"); x.add_argument("--ids")
    x.add_argument("--arms"); x.add_argument("--prefix", default="S")
    x.add_argument("--basin-sources", help="e.g. observed,predicted — exclude visited families from judge prompts (fair final comparison)")
    x.add_argument("--crux", action="store_true", help="v1.7: add the crux column X to the judge prompt")
    x.add_argument("--genius", action="store_true", help="v1.7: add the genius score G to the judge prompt")
    x.add_argument("--principle", action="store_true", help="v2.0: add the single-principle score P to the judge prompt")
    x.add_argument("--feasible", action="store_true", help="v1.9: add the feasibility score F (order-of-magnitude check) to the judge prompt")
    x = sp.add_parser("family"); x.add_argument("run"); x.add_argument("set"); src(x)
    x = sp.add_parser("valorize"); x.add_argument("run"); x.add_argument("set"); x.add_argument("--arm", required=True); src(x)
    x = sp.add_parser("intent"); x.add_argument("run"); x.add_argument("set", nargs="?"); x.add_argument("--pick", help="reading number, or auto"); src(x)
    x = sp.add_parser("laws"); x.add_argument("run"); x.add_argument("--arm", default="ED"); src(x)
    x = sp.add_parser("futurematch"); x.add_argument("run"); x.add_argument("--after", default="2607", help="arXiv YYMM after the knowledge cutoff")
    x = sp.add_parser("portfolio"); x.add_argument("--slots", type=int, default=5); x.add_argument("--c", type=float, default=0.15)
    x.add_argument("--exclude", default="mechneg,symptomport,backloop,reframe,gap", help="techniques retired by selection")
    x = sp.add_parser("judge"); x.add_argument("run"); x.add_argument("set"); x.add_argument("judge"); src(x)
    x = sp.add_parser("select"); x.add_argument("run"); x.add_argument("name"); x.add_argument("--labels"); x.add_argument("--arms")
    x.add_argument("--k", type=int, default=6); x.add_argument("--drop-known-basins", action="store_true")
    x.add_argument("--diverse", action="store_true", help="v1.7: near-duplicates (same closest work) take one slot")
    x.add_argument("--by", default="ov", choices=["ov", "ovg", "ovf", "gate"], help="ovg: O*V*G (v1.7); ovf: O*V*F, feasibility (v1.9); gate: O x kill-test headroom (v3.0)")
    x.add_argument("--v2", action="store_true", help="score = O*V*(0.5+0.5*carried); drop ideas with decoy specificity <= 0 (needs audit)")
    x = sp.add_parser("lit"); x.add_argument("run"); x.add_argument("set"); src(x)
    x = sp.add_parser("pairs"); x.add_argument("run"); x.add_argument("name"); x.add_argument("--n", type=int, default=6)
    x = sp.add_parser("remember"); x.add_argument("run"); x.add_argument("--labels"); x.add_argument("--arms")
    x = sp.add_parser("report"); x.add_argument("run"); x.add_argument("--top", type=int, default=10)
    x = sp.add_parser("fork"); x.add_argument("src"); x.add_argument("dst")
    x = sp.add_parser("import"); x.add_argument("dst"); x.add_argument("src"); x.add_argument("--arm", required=True)
    x.add_argument("--ids", help="only these source ids (any generation)")
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
    needs_src = a.cmd in ("ingest", "family", "judge", "lit", "gapwalk", "strip", "audit", "concretize", "species", "valorize", "material", "gate") or (a.cmd == "intent" and a.pick is None)
    if getattr(a, "transcript", None) is None and getattr(a, "file", None) is None and needs_src:
        sys.exit("need --transcript or --file")
    globals()["cmd_" + a.cmd.replace("-", "_")](a)


if __name__ == "__main__":
    main()
