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
        for x, y in json.load(open(os.path.join(rd, "pairs.json"))): assert x.split("#")[0] != y.split("#")[0]
        pr = open(ce("prompt", RUN, "evo", "e1", "--pairs", "2").strip()).read()
        assert pr.count("Parent A") >= 1 and "AA: aa" in pr and "{" not in pr.replace("{N}", "")
        for t in ["plain", "neg", "core", "reframe", "mech", "loop"]:
            s = open(ce("prompt", RUN, t, "t_" + t).strip()).read(); assert "{" not in s and "=== IDEAS ===" in s, t
        ce("remember", RUN); assert "| engine |" in ce("report", RUN)
        print("OK: all engine commands passed")
    finally:
        shutil.rmtree(rd, ignore_errors=True); shutil.rmtree(tmp, ignore_errors=True)
if __name__ == "__main__":
    main()
