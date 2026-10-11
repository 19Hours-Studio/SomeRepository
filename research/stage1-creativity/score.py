"""Гравитация аттракторов + перемешанный слепой набор для судьи."""
import re, glob, json, os, secrets
CLUSTERS = {  # кластеры из пре-регистрации (H1) + «второй слой» клише (P5)
 "world_model/planning": r"world.?model|predictive model of the world|planning|simulat",
 "neuro_symbolic": r"symbolic|logic|rule.?based|program synthes",
 "memory/continual": r"long.?term memory|episodic|continual|lifelong|catastrophic forgetting|consolidat",
 "moe/modular/routing": r"mixture|expert|modular|routing|router",
 "meta_learning": r"meta.?learn|learn(s|ing)? to learn|hypernet",
 "predictive_coding/free_energy": r"predictive coding|free.?energy|active inference|prediction error|surprise",
 "spiking/neuromorphic": r"spik|neuromorph|dendrit|synap",
 "system1_2/hierarchy": r"system ?1|system ?2|hierarch|fast and slow",
 "multi_agent/society": r"multi.?agent|society|swarm|colony|ensemble of agents",
 "brain_bio_analogy": r"brain|cortex|hippocamp|neuron|biolog|evolution|genetic",
 "energy/diffusion": r"energy.?based|diffusion|annealing",
 "causal/graph": r"causal|graph",
 "2nd_layer:physics_quantum_holo": r"quantum|holograph|fractal|cellular automat|reservoir|oscillat|wave|resonan|crystal|field",
}
def ideas(text):
    if "=== IDEAS ===" not in text: return []
    body = text.split("=== IDEAS ===", 1)[1]
    chunks = re.split(r"\n\**IDEA\s*\d\**", "\n" + body)
    out = []
    for c in chunks:
        m = re.search(r"MECHANISM:\**\s*(.+?)\n\s*\**DIFFERENCE:\**\s*(.+?)(\n\n|\Z)", c, re.S)
        n = re.search(r"NAME:\**\s*(.+)", c)
        if m: out.append({"name": n.group(1).strip() if n else "", "mech": m.group(1).strip(), "diff": m.group(2).strip()})
    return out
if __name__ == "__main__":
    rows, blind = {}, []
    for p in sorted(glob.glob("raw/*.md")):
        cond = os.path.basename(p)[:-3]
        ids = ideas(open(p).read())
        hits = []
        for i, d in enumerate(ids):
            t = (d["name"] + " " + d["mech"] + " " + d["diff"]).lower()
            h = [k for k, rx in CLUSTERS.items() if re.search(rx, t)]
            hits.append(h)
            blind.append({"cond": cond, "i": i + 1, **d})
        allh = sorted({x for h in hits for x in h})
        rows[cond] = {"n_ideas": len(ids), "avg_clusters_per_idea": round(sum(map(len, hits)) / max(1, len(ids)), 2), "clusters": allh, "per_idea": hits}
    json.dump(rows, open("attractor_scores.json", "w"), ensure_ascii=False, indent=1)
    for k, v in rows.items(): print(f"{k:8s} ideas={v['n_ideas']} avg={v['avg_clusters_per_idea']}  {v['clusters']}")
    # слепой набор: перемешиваем, убираем имена и метки условий
    rng = secrets.SystemRandom(); rng.shuffle(blind)
    key = {}
    with open("blind_set.txt", "w") as f:
        for j, d in enumerate(blind, 1):
            key[f"X{j:02d}"] = f"{d['cond']}#{d['i']}"
            f.write(f"X{j:02d}\nMECHANISM: {d['mech']}\nDIFFERENCE: {d['diff']}\n\n")
    json.dump(key, open("blind_key.json", "w"), indent=1)
    print(len(blind), "ideas in blind set")
