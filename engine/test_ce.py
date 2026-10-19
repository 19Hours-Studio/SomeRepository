"""Холостой прогон движка на сохранённых ответах и синтетических судьях (без вызовов моделей).
Запуск: python3 engine/test_ce.py"""
import json, os, random, shutil, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); RAW = os.path.join(HERE, "..", "research", "stage1-creativity", "raw")
RUN = "_selftest"
def ce(*args):
    r = subprocess.run([sys.executable, os.path.join(HERE, "ce.py"), *args], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr; return r.stdout
def main():
    tmp = tempfile.mkdtemp(); rd = os.path.join(HERE, "runs", RUN)
    try:
        ce("init", RUN, "--question", "Q?", "--force")
        for lab, f, arm in [("B1", "B1.md", "control"), ("NEG", "NEG.md", "control"), ("MECH", "MECH.md", "control"), ("EVO2", "r4/EVO2.md", "engine")]:
            assert "3 ideas" in ce("ingest", RUN, lab, "--arm", arm, "--file", os.path.join(RAW, f))
        ce("set", RUN, "s01", "--prefix", "S"); key = json.load(open(os.path.join(rd, "sets", "s01", "key.json")))
        assert len(key) == 12
        random.seed(0)
        for j in "AB":
            p = os.path.join(tmp, j); open(p, "w").write("SCORES\n" + "\n".join(
                f"{k} | {random.randint(2,7)} | 5 | {random.randint(2,7)} | N | {random.choice(['NEW','AA','BB'])} | w" for k in key) + "\nTOP3: -\n")
            assert "12/12" in ce("judge", RUN, "s01", j, "--file", p)
        p = os.path.join(tmp, "fam"); open(p, "w").write(f"FAMILY | AA | aa | {list(key)[0]}\nFAMILY | BB | bb | predicted\n")
        assert "+2" in ce("family", RUN, "s01", "--file", p)
        p = os.path.join(tmp, "lit"); open(p, "w").write("LIT\n" + "\n".join(
            f"{k} | {'KNOWN' if i == 0 else 'PARTIAL'} | closest work: P{i} (2020) u ; o | new" for i, k in enumerate(key)))
        assert "12/12" in ce("lit", RUN, "s01", "--file", p)
        out = ce("select", RUN, "g1", "--k", "6"); assert key[list(key)[0]] not in out  # KNOWN отсеян
        ce("pairs", RUN, "g1", "--n", "3")
        pairs = json.load(open(os.path.join(rd, "pairs.json")))
        for x, y in pairs: assert x.split("#")[0] != y.split("#")[0]
        sys.path.insert(0, HERE); import ce as cem
        from collections import Counter
        surv = json.load(open(os.path.join(rd, "survivors_g1.json")))
        def fam(x):
            known = [b for b in cem.agg(RUN, x)["basins"] if b != "NEW"]
            return Counter(known).most_common(1)[0][0] if known else "NEW:" + x
        uses = Counter(p for pr in pairs for p in pr)
        for x in surv:  # непокрытый родитель допустим, только если у него нет допустимого партнёра со свободной ёмкостью
            if uses[x] == 0 and len(pairs) < 3:
                assert not [y for y in surv if y != x and fam(y) != fam(x) and y.split("#")[0] != x.split("#")[0] and uses[y] < 2], "parent starved: " + x
        pr = open(ce("prompt", RUN, "evo", "e1", "--pairs", "2").strip()).read()
        assert pr.count("Parent A") >= 1 and "AA: aa" in pr and "{" not in pr.replace("{N}", "")
        for t in ["plain", "neg", "core", "reframe", "mech", "loop"]:
            s = open(ce("prompt", RUN, t, "t_" + t).strip()).read(); assert "{" not in s and "=== IDEAS ===" in s, t
        ce("remember", RUN); assert "| engine |" in ce("report", RUN)
        # --- v2: fork, gapwalk, gap-техника, strip, audit, select --v2, import
        RUN2 = RUN + "_v2"; rd2 = os.path.join(HERE, "runs", RUN2)
        try:
            ce("fork", RUN, RUN2)
            assert all(b["source"] != "visited" for b in json.load(open(os.path.join(rd2, "basins.json"))))
            p = os.path.join(tmp, "gw"); open(p, "w").write("GAP | G1 | plans never say how X is measured | M01,M02\nGAP | G2 | cost of Y explodes | M03\n")
            ce("set", RUN2, "s00", "--prefix", "M")
            assert "gaps: 2" in ce("gapwalk", RUN2, "s00", "--file", p)
            g = open(ce("prompt", RUN2, "gap", "g1_gap").strip()).read(); assert "G1: plans never say" in g and "{" not in g
            ce("set", RUN2, "s01", "--prefix", "A"); k2 = json.load(open(os.path.join(rd2, "sets", "s01", "key.json")))
            p = os.path.join(tmp, "st"); open(p, "w").write("\n".join(f"STRIP | {k} | flat text {k}" for k in list(k2)[:-1]))
            out = ce("strip", RUN2, "s01", "--file", p); assert "WARNING" in out and "prompt_judge_stripped" in out
            pj = open(os.path.join(rd2, "sets", "s01", "prompt_judge_stripped.txt")).read(); assert "blind_stripped.txt" in pj
            for j in "AB":
                q = os.path.join(tmp, "j2" + j); open(q, "w").write("SCORES\n" + "\n".join(f"{k} | 5 | 5 | 5 | N | NEW | w" for k in k2))
                ce("judge", RUN2, "s01", j, "--file", q)
            ks = list(k2); p = os.path.join(tmp, "au")
            open(p, "w").write(f"SLOT | {ks[0]} | part a | N | 3\nSLOT | {ks[0]} | part b | Y | 1\nDECOY | {ks[0]} | 7 | 3 | 4 | 2\n"
                               f"SLOT | {ks[1]} | part c | Y | 3\nDECOY | {ks[1]} | 5 | 6 | 6 | 6\n")
            assert "audit: 2 ideas" in ce("audit", RUN2, "s01", "--file", p)
            au = json.load(open(os.path.join(rd2, "audit.json"))); assert au[k2[ks[0]]]["carried"] == 0.75 and au[k2[ks[1]]]["spec"] < 0
            out = ce("select", RUN2, "v2sel", "--k", "6", "--v2")
            assert k2[ks[0]] in out and k2[ks[1]] not in out  # отрицательная специфичность отсеяна
            ce("ingest", RUN2, "g1_x", "--arm", "engine", "--gen", "1", "--file", os.path.join(RAW, "r4/EVO1.md"))
            assert "imported 3 ideas" in ce("import", RUN, RUN2, "--arm", "v2x")
            assert any(i["id"].startswith("v2x:") for i in json.load(open(os.path.join(rd, "ideas.json"))))
            # --- v1.5: первые мысли, самоотчёт -> бассейны, конкретизация
            ce("setcfg", RUN2, "thoughts", "1")
            pr = open(ce("prompt", RUN2, "core", "g1_c").strip()).read(); assert "FIRST THOUGHTS:" in pr and "{" not in pr
            ft = os.path.join(tmp, "ft"); open(ft, "w").write("intro\nFIRST THOUGHTS:\n- obvious one\n- obvious two\n" + open(os.path.join(RAW, "r4/EVO1.md")).read())
            out = ce("ingest", RUN2, "g1_c", "--arm", "engine", "--gen", "1", "--file", ft); assert "first thoughts: 2" in out
            assert "-> 2 basins" in ce("thoughts", RUN2, "--labels", "g1_c")
            assert "T" in open(ce("prompt", RUN2, "loop", "g2_t").strip()).read().split("obvious one")[0][-6:]
            ce("set", RUN2, "s05", "--labels", "g1_c", "--prefix", "C"); k5 = json.load(open(os.path.join(rd2, "sets", "s05", "key.json")))
            cz = os.path.join(tmp, "cz"); open(cz, "w").write("\n".join(f"TEST | {k} | First test: run X, metric Y." for k in k5))
            assert f"concretized {len(k5)}/{len(k5)}" in ce("concretize", RUN2, "s05", "--file", cz)
            ii = [i for i in json.load(open(os.path.join(rd2, "ideas.json"))) if i["label"] == "g1_c"]
            assert all(i["mech"].endswith("metric Y.") and "mech_orig" in i for i in ii)
            # --- v1.6: эволюция видов
            bp = open(ce("breed", RUN2, "--from-runs", RUN2, "--ops", "cross:loop+core", "mutate:loop").strip()).read()
            assert "PARENT loop" in bp and "PARENT core" in bp and "{QUESTION}" in bp and "Observed outputs" in bp
            sp = os.path.join(tmp, "sp"); open(sp, "w").write(
                "=== SPECIES _test_sp ===\n{QUESTION}\nPropose {N} answers. Forbidden: {BASINS}\n{FORMAT}\n=== END ===\n"
                "=== SPECIES _test_bad ===\nno placeholders here\n=== END ===\n")
            out = ce("species", RUN2, "--file", sp); assert "accepted 1/2" in out and "REJECTED _test_bad" in out
            g = open(ce("prompt", RUN2, "_test_sp", "g1__test_sp").strip()).read(); assert "=== IDEAS ===" in g and "{" not in g
            ce("fitness", RUN2)
        finally:
            spd = os.path.join(HERE, "species")
            for f in ("_test_sp.txt", "_test_bad.txt"):
                if os.path.exists(os.path.join(spd, f)): os.remove(os.path.join(spd, f))
            reg = os.path.join(spd, "species.json")
            if os.path.exists(reg):
                r = json.load(open(reg)); r.pop("_test_sp", None)
                if r: json.dump(r, open(reg, "w"), indent=1)
                else: os.remove(reg)
            shutil.rmtree(rd2, ignore_errors=True)
        # v1.7: crux, judge X column, fragments, diverse selection
        R7 = "_selftest17"; rd7 = os.path.join(HERE, "runs", R7)
        try:
            ce("init", R7, "--question", "Q?", "--force")
            ideas = "=== IDEAS ===\n" + "\n".join(f"IDEA {k}\nNAME: n{k}\nMECHANISM: {m}\nVALUE: v{k}\n" for k, m in
                    [(1, "alpha mechanism"), (2, "beta mechanism"), (3, "gamma mechanism"), (4, "extends Idea 1 with delta")])
            p = os.path.join(tmp, "g7"); open(p, "w").write(ideas)
            out = ce("ingest", R7, "g1_x", "--arm", "engine", "--gen", "1", "--file", p)
            assert "4 ideas" in out and "fragment" in out
            ce("set", R7, "s00", "--labels", "g1_x", "--prefix", "M"); k0 = json.load(open(os.path.join(rd7, "sets", "s00", "key.json")))
            p = os.path.join(tmp, "f7"); open(p, "w").write(f"FAMILY | AA | aa | {list(k0)[0]}\nCRUX | judging validity of the unprecedented\n")
            assert "crux:" in ce("family", R7, "s00", "--file", p)
            ce("setcfg", R7, "use_crux", "1"); ce("prompt", R7, "neg", "g1_neg")
            assert "judging validity of the unprecedented" in open(os.path.join(rd7, "prompts", "g1_neg.txt")).read()
            ce("set", R7, "s01", "--labels", "g1_x", "--prefix", "A", "--crux", "--genius"); k1 = json.load(open(os.path.join(rd7, "sets", "s01", "key.json")))
            pj = open(os.path.join(rd7, "sets", "s01", "prompt_judge.txt")).read()
            assert "ID | O | C | V | G | R | BASIN | X | closest" in pj and "G = genius" in pj
            assert "CRUX |" in open(os.path.join(rd7, "sets", "s01", "prompt_crux.txt")).read()
            closest = {"g1_x#1": "geodetic network adjustment", "g1_x#2": "geodetic network adjustment", "g1_x#3": "kinetic proofreading", "g1_x#4": "other thing"}
            gen = {"g1_x#1": 2, "g1_x#2": 3, "g1_x#3": 9, "g1_x#4": 9}
            p = os.path.join(tmp, "j7"); open(p, "w").write("SCORES\n" + "\n".join(f"{sid} | 6 | 5 | 5 | {gen[iid]} | N | NEW | Y | {closest[iid]}" for sid, iid in k1.items()))
            assert "4/4" in ce("judge", R7, "s01", "J1", "--file", p)
            sys.path.insert(0, HERE); import ce as cem7
            assert cem7.agg(R7, "g1_x#1")["crux"] == 1.0 and cem7.agg(R7, "g1_x#3")["G"] == 9
            ce("set", R7, "s02f", "--labels", "g1_x", "--prefix", "A", "--genius", "--feasible"); k2 = json.load(open(os.path.join(rd7, "sets", "s02f", "key.json")))
            assert "ID | O | C | V | G | F | R | BASIN | closest" in open(os.path.join(rd7, "sets", "s02f", "prompt_judge.txt")).read()
            open(p, "w").write("SCORES\n" + "\n".join(f"{sid} | 6 | 5 | 5 | 7 | 2 | N | NEW | x" for sid in k2))
            assert "4/4" in ce("judge", R7, "s02f", "J9", "--file", p)
            j9 = json.load(open(os.path.join(rd7, "scores.json")))["g1_x#1"]["s02f:J9"]; assert j9["G"] == 7 and j9["F"] == 2, j9
            ce("set", R7, "s03f", "--labels", "g1_x", "--prefix", "A", "--feasible"); k3 = json.load(open(os.path.join(rd7, "sets", "s03f", "key.json")))
            assert "ID | O | C | V | F | R | BASIN | closest" in open(os.path.join(rd7, "sets", "s03f", "prompt_judge.txt")).read()
            open(p, "w").write("SCORES\n" + "\n".join(f"{sid} | 6 | 5 | 5 | 3 | N | NEW | x" for sid in k3))
            assert "4/4" in ce("judge", R7, "s03f", "J9", "--file", p)
            j9 = json.load(open(os.path.join(rd7, "scores.json")))["g1_x#1"]["s03f:J9"]; assert j9["F"] == 3 and "G" not in j9, j9
            sc7 = json.load(open(os.path.join(rd7, "scores.json")))  # keep later selection on the s01 scores
            for v in sc7.values(): v.pop("s02f:J9", None); v.pop("s03f:J9", None)
            json.dump(sc7, open(os.path.join(rd7, "scores.json"), "w"))
            ce("select", R7, "g1", "--k", "4", "--diverse", "--by", "ovg")
            surv7 = json.load(open(os.path.join(rd7, "survivors_g1.json")))
            assert "g1_x#4" not in surv7 and len(surv7) == 2, surv7  # fragment dropped, near-duplicates share one slot
            assert surv7[0] == "g1_x#3" and surv7[1] == "g1_x#2", surv7  # ranked by O*V*G; of the duplicates the more genial one stays
            ce("prompt", R7, "genius", "g1_genius"); ce("pairs", R7, "g1", "--n", "1")
            ce("prompt", R7, "evo_simple", "g2_evo1", "--pairs", "1")
            assert "SIMPLER than either parent" in open(os.path.join(rd7, "prompts", "g2_evo1.txt")).read()
            assert "ANCHOR" in open(os.path.join(rd7, "sets", "s01", "prompt_valorize.txt")).read()
            p = os.path.join(tmp, "v7"); sid0, pid0 = list(k1.items())[0]
            open(p, "w").write(f"=== VALORIZED {sid0} ===\nANCHOR: alpha\nNAME: better\nMECHANISM: alpha made simple\nVALUE: new ability\n")
            assert "valorized 1/4" in ce("valorize", R7, "s01", "--arm", "v7V", "--file", p)
            vi = [i for i in json.load(open(os.path.join(rd7, "ideas.json"))) if i["arm"] == "v7V"]
            assert len(vi) == 1 and vi[0]["parent"] == pid0 and vi[0]["anchor"] == "alpha"
            assert "BOTTLENECK" in open(os.path.join(rd7, "sets", "s01", "prompt_value.txt")).read()
            open(p, "w").write(f"=== VALUED {sid0} ===\nANCHOR: alpha\nNAME: valuable\nMECHANISM: alpha at the core\nVALUE: big gain\n")
            assert "valorized 1/4" in ce("valorize", R7, "s01", "--arm", "v7C", "--file", p)
            assert "the layer that COUNTS" in open(os.path.join(rd7, "sets", "s01", "prompt_fermi.txt")).read()
            open(p, "w").write(f"=== CHECKED {sid0} ===\nANCHOR: alpha\nVERDICT: FIX\nESTIMATE: 1 W/m2 vs 100 needed; thinner gap\nNAME: counted\nMECHANISM: alpha at 100 W/m2\nVALUE: real gain\n")
            out = ce("valorize", R7, "s01", "--arm", "v7D", "--file", p)
            assert "valorized 1/4" in out and "'FIX': 1" in out, out
            vd = [i for i in json.load(open(os.path.join(rd7, "ideas.json"))) if i["arm"] == "v7D"][0]
            assert vd["verdict"] == "FIX" and vd["estimate"].startswith("1 W/m2"), vd
            ce("laws", R7, "--arm", "v7D"); assert "COUNTS" not in open(os.path.join(rd7, "laws", "prompt_laws.txt")).read()
            assert "ESTIMATE: 1 W/m2" in open(os.path.join(rd7, "laws", "blind.txt")).read()
            open(p, "w").write("LAW | gap cancels: leak x loss = nFDc/s, membraneless cells | RULES OUT: thick gaps | OPENS: slow carriers\n")
            assert "laws: 1 stored" in ce("laws", R7, "--file", p)
            ce("prompt", R7, "law", "g3_law"); assert "gap cancels" in open(os.path.join(rd7, "prompts", "g3_law.txt")).read()
            ce("prompt", R7, "pr_tail", "pr_t", "--n", "12"); pt = open(os.path.join(rd7, "prompts", "pr_t.txt")).read()
            assert "=== PRINCIPLES ===" in pt and "exactly 12 lines" in pt and "{" not in pt.replace("{N}", ""), pt[-400:]
            open(p, "w").write("x\n=== PRINCIPLES ===\nPRINCIPLE | Mobility splits | Mobility ratio, not distance, separates | OVERTURNS: barriers separate | GAIN: no membrane | P: 0.04\n"
                               "**PRINCIPLE** | Second one | Claim two | OVERTURNS: a | GAIN: b | P: 0.2\n")
            assert "2 ideas" in ce("ingest", R7, "pr_t", "--arm", "v7P0", "--gen", "1", "--file", p)
            pr = [i for i in json.load(open(os.path.join(rd7, "ideas.json"))) if i["label"] == "pr_t"]
            assert pr[0]["p"] == 0.04 and pr[0]["principle"].startswith("Mobility") and "Overturns" in pr[0]["mech"], pr
            ce("set", R7, "s04p", "--ids", "pr_t#1,pr_t#2", "--prefix", "T", "--feasible", "--principle"); k4 = json.load(open(os.path.join(rd7, "sets", "s04p", "key.json")))
            assert "ID | O | C | V | F | P | R | BASIN | closest" in open(os.path.join(rd7, "sets", "s04p", "prompt_judge.txt")).read()
            assert "TRUE (holds" in open(os.path.join(rd7, "sets", "s04p", "prompt_truth.txt")).read()
            assert "=== DERIVED" in open(os.path.join(rd7, "sets", "s04p", "prompt_derive.txt")).read()
            open(p, "w").write("SCORES\n" + "\n".join(f"{sid} | 7 | 4 | 6 | 3 | 9 | N | NEW | x" for sid in k4))
            assert "2/2" in ce("judge", R7, "s04p", "J8", "--file", p)
            j8 = json.load(open(os.path.join(rd7, "scores.json")))["pr_t#1"]["s04p:J8"]; assert j8["F"] == 3 and j8["P"] == 9, j8
            t1 = [k for k, v in k4.items() if v == "pr_t#1"][0]
            open(p, "w").write(f"=== CHECKED {t1} ===\nANCHOR: mobility\nVERDICT: REGIME\nESTIMATE: r = 1e-3 for D 1e-12\nNAME: m\nMECHANISM: holds for slow carriers\nVALUE: v\n")
            assert "'REGIME': 1" in ce("valorize", R7, "s04p", "--arm", "v7PT", "--file", p)
            open(p, "w").write("=== IDEAS ===\nIDEA 1\nNAME: tail one\nP: 0.02\nMECHANISM: rare thing\nVALUE: big\n")
            ce("ingest", R7, "tl", "--arm", "v7T", "--gen", "1", "--file", p)
            assert [i for i in json.load(open(os.path.join(rd7, "ideas.json"))) if i["label"] == "tl"][0]["p"] == 0.02
            sc7 = json.load(open(os.path.join(rd7, "scores.json")))
            for v in sc7.values(): v.pop("s04p:J8", None)
            json.dump(sc7, open(os.path.join(rd7, "scores.json"), "w"))
            json.dump({"g1_x#1": {"verdict": "PARTIAL", "closest": "Some work https://arxiv.org/abs/2608.01234"}}, open(os.path.join(rd7, "lit.json"), "w"))
            assert "future-match 1/1" in ce("futurematch", R7)
            json.dump({"g1_x#1": {"verdict": "PARTIAL", "closest": "Journal work (2026-09) https://doi.org/x ; older (2019-03)"},
                       "g1_x#2": {"verdict": "KNOWN", "closest": "Old work (2024-05) https://doi.org/y"}}, open(os.path.join(rd7, "lit.json"), "w"))
            assert "future-match 1/2" in ce("futurematch", R7)
            assert "portfolio:" in ce("portfolio")
            open(p, "w").write("READING | alpha | deliver a | CRUX: crux a\nREADING | beta | deliver b | CRUX: crux b\nREADING | gamma | deliver c | CRUX: crux c\n")
            assert "[2] gamma" in ce("intent", R7, "s01", "--file", p)
            assert "crux b" in ce("intent", R7, "--pick", "1")
            assert json.load(open(os.path.join(rd7, "config.json")))["crux"] == "crux b"
            # v2.2: red-team task, repair task with critique, ingest with parent links
            dr = os.path.join(tmp, "rt"); ce("redteamtask", R7, "--ids", "tl#1", "--dir", dr)
            t = open(os.path.join(dr, "TASK.md")).read(); assert "=== REVIEW ===" in t and "tail one" in t and dr in t
            open(p, "w").write("=== REVIEW ===\nIDEA 1: tail one\nDEFECT | FATAL | melts | 3 kg/day\n")
            dp = os.path.join(tmp, "rp"); ce("repairtask", R7, "--ids", "tl#1", "--dir", dp, "--critique", p)
            t = open(os.path.join(dp, "TASK.md")).read(); assert "melts | 3 kg/day" in t and "CONSISTENCY PASS" in t
            open(p, "w").write("=== IDEAS ===\nIDEA 1\nNAME: fixed tail\nMECHANISM: rare thing fixed\nVALUE: big\n")
            ce("ingest", R7, "rp", "--arm", "v7R", "--gen", "3", "--parents", os.path.join(dp, "parents.json"), "--file", p)
            assert [i for i in json.load(open(os.path.join(rd7, "ideas.json"))) if i["label"] == "rp"][0]["parent"] == "tl#1"
            # v3.0: raw material, frontier/ledger techniques, kill-test gate, selection by O x headroom
            open(p, "w").write("notes\n=== FRONTIER ===\nCAP 1 | glass foam | materials | floats | 0.1 g/cc (2024) | TRL 6 | u\n")
            assert "frontier:" in ce("material", R7, "frontier", "--file", p)
            open(p, "w").write("=== LEDGER ===\nARCHETYPE A: x | delivered cost 1 | price 2\n")
            ce("material", R7, "ledger", "--file", p)
            for tech in ("frontier", "ledger", "frontier_ledger"):
                t = open(ce("prompt", R7, tech, "t_" + tech).strip()).read()
                assert "{" not in t.replace("{N}", ""), t[:200]
            assert "glass foam" in open(os.path.join(rd7, "prompts", "t_frontier_ledger.txt")).read()
            dg = os.path.join(tmp, "gt"); ce("gatetask", R7, "--ids", "tl#1,rp#1", "--dir", dg)
            t = open(os.path.join(dg, "TASK.md")).read(); assert "ARCHETYPE A" in t and "fixed tail" in t and "mean originality" not in t
            open(p, "w").write("=== GATE ===\nIDEA 1: tail one\nKILLER | melt | required 9 kg | available 0.5 kg (src) | MARGIN 0.05\n"
                               "CHAIN | road | now 80 | with idea 70 | RATIO 1.14\nVERDICT | DEAD | melts\n"
                               "IDEA 2: fixed tail\nKILLER | flux | required 1 | available 3 (src) | MARGIN 3\n"
                               "CHAIN | road | now 80 | with idea 20 | RATIO 4.0\nVERDICT | ALIVE | ok\n")
            assert "2/2" in ce("gate", R7, "--dir", dg, "--file", p)
            gj = json.load(open(os.path.join(rd7, "gate.json"))); assert gj["rp#1"]["ratio"] == 4.0 and gj["tl#1"]["margin"] == 0.05
            t = open(ce("resurrect", R7, "rz", "--ids", "tl#1,rp#1", "--m", "2").strip()).read()
            assert "DEATH CERTIFICATE: killer: melt | margin 0.05" in t and "exactly 4 ideas" in t and "{" not in t.replace("{N}", "")
            assert json.load(open(os.path.join(rd7, "prompts", "rz.parents.json"))) == ["tl#1", "tl#1", "rp#1", "rp#1"]
            open(os.path.join(dr, "REVIEW.md"), "w").write("=== REVIEW ===\nIDEA 1: tail one\nDEFECT | FATAL | melts | 3 kg/day\nDEFECT | MINOR | x | y\n")
            t = open(ce("evolve", R7, "ev", "--audit", dr, "--m", "2").strip()).read()
            assert "- FATAL: melts (3 kg/day)" in t and "MINOR" not in t.split("REVIEW FINDINGS")[1].split("Where")[0] and "exactly 2 ideas" in t
            # v3.3: ledger of earlier attempts, evolution that must beat the reason the closest attempt stopped short
            da = os.path.join(tmp, "at"); ce("attemptstask", R7, "--ids", "tl#1", "--dir", da)
            t = open(os.path.join(da, "TASK.md")).read(); assert "=== ATTEMPTS ===" in t and "tail one" in t and "{" not in t
            open(p, "w").write("x\n=== ATTEMPTS ===\nATTEMPT 1: ice cellar | Yukon 1900 | niche | WHY IT DID NOT SOLVE IT: melts by July | u\n")
            assert "attempts:" in ce("material", R7, "attempts", "--file", p)
            t = open(ce("evolve", R7, "ev2", "--audit", dr, "--m", "1", "--tpl", "evolve_attempts").strip()).read()
            assert "ice cellar" in t and "- FATAL: melts" in t and "{" not in t.replace("{N}", "")
            # v3.4: kill test with the verified calculation kit; A/B arms keep separate result files
            dk = os.path.join(tmp, "gk"); ce("gatetask", R7, "--ids", "tl#1", "--dir", dk, "--kit")
            t = open(os.path.join(dk, "TASK.md")).read(); assert "Kit catalog: killer classes" in t and "SCREEN |" in t and "{" not in t
            open(p, "w").write("=== GATE ===\nIDEA 1: tail one\nSCREEN | ice: 0.4; heat: 2\nKILLER | ice | required 2 m | available 0.8 m (x) | MARGIN 0.4\n"
                               "CHAIN | road | now 80 | with idea 60 | RATIO 1.3\nVERDICT | WOUNDED | thin ice\n")
            ce("gate", R7, "--dir", dk, "--out", "gate_kit.json", "--file", p)
            gk = json.load(open(os.path.join(rd7, "gate_kit.json")))["tl#1"]; assert gk["screen"] == "ice: 0.4; heat: 2" and gk["margin"] == 0.4
        finally:
            shutil.rmtree(rd7, ignore_errors=True)
        print("OK: all engine commands passed")
    finally:
        shutil.rmtree(rd, ignore_errors=True); shutil.rmtree(tmp, ignore_errors=True)
if __name__ == "__main__":
    main()
