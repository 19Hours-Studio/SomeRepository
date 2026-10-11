"""Полная аналитика: все идеи всех раундов -> единая таксономия, оценки на шкале Opus-судьи (J3) через якоря."""
import json, re, collections
FAM = {  # единая таксономия (моя разметка, сверена с семействами судей r1/r3)
 "B1#1":"A","B1#2":"B","B1#3":"NCA","B2#1":"C","B2#2":"A","B2#3":"B",
 "NOISE#1":"S:lease","NOISE#2":"F","NOISE#3":"S:hashchain","DIFF#1":"B","DIFF#2":"D","DIFF#3":"E",
 "NEG#1":"S:eprocess","NEG#2":"S:tropical","NEG#3":"FLOW","AXIOM#1":"F","AXIOM#2":"A","AXIOM#3":"D",
 "MECH#1":"E","MECH#2":"D","MECH#3":"B","ANOMALY#1":"B","ANOMALY#2":"G","ANOMALY#3":"F",
 "ABSURD#1":"C","ABSURD#2":"B","ABSURD#3":"G",
 "MAP#1":"OSC","MAP#2":"INV","MAP#3":"NCA","MSC#1":"LINRNN","MSC#2":"WAVE","MSC#3":"LINRNN",
 "LOCK#1":"C","LOCK#2":"B","LOCK#3":"SET","REFRAME#1":"OSC","REFRAME#2":"AGENCY","REFRAME#3":"AGENCY",
 "STACK#1":"S:lipschitz","STACK#2":"S:pontryagin","STACK#3":"S:coupling",
 "CORE_a#1":"FLOW","CORE_a#2":"S:rigidity","CORE_a#3":"SCALE","CORE_b#1":"E","CORE_b#2":"S:nucleation","CORE_b#3":"S:dla",
 "OPUS_BASE_a#1":"E","OPUS_BASE_a#2":"NCA","OPUS_BASE_a#3":"D","OPUS_BASE_b#1":"S:sheaf","OPUS_BASE_b#2":"NCA","OPUS_BASE_b#3":"B",
 "OPUS_NEG#1":"S:probes","OPUS_NEG#2":"S:iterated","OPUS_NEG#3":"S:homology",
 "OPUS_MECH#1":"FLOW","OPUS_MECH#2":"D","OPUS_MECH#3":"S:cbr","OPUS_CORE2#1":"FLOW","OPUS_CORE2#2":"FLOW","OPUS_CORE2#3":"SCALE"}
L1, L2, L3B = set("ABCDEFG"), {"OSC","NCA","INV","WAVE","LINRNN","SET"}, {"FLOW","SCALE","AGENCY"}
layer = lambda f: "L1" if f in L1 else "L2" if f in L2 else "L3-basin" if f in L3B else "L3-single"
def load(md, key, pat):
    k = json.load(open(key)); out = {}
    for m in re.findall(pat, open(md).read(), re.M):
        lab = k[m[0]].replace("ANCHOR:", "").replace("HAIKU_", ""); out[lab] = m[1:]
    return out
J1 = load("judge_r1.md", "judge_r1_key.json", r"^(X\d\d) \| (\d+) \| (\d+) \| (.+)$")
J2 = load("judge_r2.md", "blind_key_r2.json", r"^(Y\d\d) \| (\d+) \| (\d+) \| (\d+) \| ([YN]) \| (.+)$")
J3 = load("judge_r3.md", "blind_key_r3.json", r"^(Z\d\d) \| (\d+) \| (\d+) \| (\d+) \| ([YN]) \| (.+)$")
anch = ["B1#1","B2#1","NEG#1","NEG#3","MECH#2","DIFF#1"]
mean = lambda xs: sum(xs)/len(xs) if xs else float("nan")
dO1 = mean([int(J3[a][0]) - int(J1[a][0]) for a in anch]); dO2 = mean([int(J3[a][0]) - int(J2[a][0]) for a in anch])
dV2 = mean([int(J3[a][2]) - int(J2[a][2]) for a in anch])
rows = []
for lab, fam in FAM.items():
    if lab in J3: O, V, R, src = int(J3[lab][0]), int(J3[lab][2]), J3[lab][3], "J3"
    elif lab in J2: O, V, R, src = int(J2[lab][0]) + dO2, int(J2[lab][2]) + dV2, J2[lab][3], "J2"
    else: O, V, R, src = int(J1[lab][0]) + dO1, None, None, "J1"
    cond = re.sub(r"_[ab]$", "", lab.split("#")[0])
    model = "Opus" if cond.startswith("OPUS") else "Haiku"
    rows.append(dict(id=lab, cond=cond, model=model, fam=fam, layer=layer(fam), O=round(O,2), V=None if V is None else round(V,2), R=R, judge=src))
famcount = collections.Counter(r["fam"] for r in rows)
by = collections.defaultdict(list)
for r in rows: by[r["cond"]].append(r)
print(f"сдвиги к шкале J3: O(J1){dO1:+.2f} O(J2){dO2:+.2f} V(J2){dV2:+.2f}\n")
hdr = f"{'cond':11s} {'n':>2s} {'O':>5s} {'V':>5s} {'O*V':>5s} {'L1':>4s} {'L2':>4s} {'L3':>4s} {'uniq':>4s} {'R=Y':>5s} fams/n"
print(hdr); summ = {}
for c, L in sorted(by.items(), key=lambda kv: -mean([r["O"] for r in kv[1]])):
    n = len(L); Vs = [r["V"] for r in L if r["V"] is not None]; OVs = [r["O"]*r["V"] for r in L if r["V"] is not None]
    sh = lambda lay: sum(r["layer"] == lay for r in L)/n
    l3 = sum(r["layer"].startswith("L3") for r in L)/n
    uniq = sum(famcount[r["fam"]] == 1 for r in L)/n  # семейство встретилось во всём датасете 1 раз
    Rk = [r["R"] for r in L if r["R"]]; rr = f"{sum(x=='Y' for x in Rk)}/{len(Rk)}" if Rk else "-"
    s = dict(n=n, O=round(mean([r["O"] for r in L]),2), V=round(mean(Vs),2) if Vs else None, OV=round(mean(OVs),1) if OVs else None,
             L1=round(sh("L1"),2), L2=round(sh("L2"),2), L3=round(l3,2), uniq=round(uniq,2), R=rr, fams_per_n=round(len({r['fam'] for r in L})/n,2))
    summ[c] = s
    f = lambda x: "  -  " if x is None else f"{x:5.2f}" if isinstance(x, float) and x < 10 else f"{x:5.1f}"
    print(f"{c:11s} {n:2d} {s['O']:5.2f} {f(s['V'])} {f(s['OV'])} {s['L1']:4.2f} {s['L2']:4.2f} {s['L3']:4.2f} {s['uniq']:4.2f} {rr:>5s} {s['fams_per_n']}")
# повторы одного и того же промпта: сколько семейств общих
pairs = {"Haiku база B1/B2": ("B1","B2"), "Haiku CORE a/b": ("CORE_a","CORE_b"), "Opus база a/b": ("OPUS_BASE_a","OPUS_BASE_b")}
print("\nколлапс между повторами:")
for k, (a, b) in pairs.items():
    fa = {r["fam"] for r in rows if r["id"].startswith(a+"#")}; fb = {r["fam"] for r in rows if r["id"].startswith(b+"#")}
    print(f"  {k}: общих семейств {len(fa & fb)} из 3 -> {sorted(fa & fb)}")
lay = collections.Counter(r["layer"] for r in rows)
print("\nслои по всему датасету:", dict(lay), "| семейств всего:", len(famcount), "| из них одиночек:", sum(v == 1 for v in famcount.values()))
print("крупнейшие бассейны:", famcount.most_common(8))
top = sorted([r for r in rows if r["V"] is not None], key=lambda r: -r["O"]*r["V"])[:8]
print("\nтоп по O*V (шкала J3):"); [print(f"  {r['id']:15s} {r['fam']:12s} O{r['O']:.1f} V{r['V']:.1f} R={r['R']}") for r in top]
unusual = sorted([r for r in rows if r["layer"].startswith("L3") and r["R"] != "Y"], key=lambda r: -r["O"])[:10]
print("\nсамые необычные (L3, не переоткрытие), по O:"); [print(f"  {r['id']:15s} {r['fam']:12s} O{r['O']:.1f} V{r['V']} [{r['judge']}]") for r in unusual]
json.dump({"rows": rows, "by_condition": summ, "shifts": dict(O_J1=dO1, O_J2=dO2, V_J2=dV2)}, open("analytics.json", "w"), indent=1, ensure_ascii=False)
