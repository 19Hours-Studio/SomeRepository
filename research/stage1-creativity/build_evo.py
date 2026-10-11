"""Раунд 4, эволюция: скрещивание выживших идей из РАЗНЫХ бассейнов + отталкивание от всех известных семейств
и от найденной литературы. Только под __main__ (урок §5)."""
from score import ideas
from build_prompts import FORMAT
def idea(path, i): d = ideas(open(path).read())[i-1]; return f"MECHANISM: {d['mech']}\n   DIFFERENCE: {d['diff']}"
P = {  # родитель: (файл, номер, ближайшая литература из lit_check_finalists.md)
 "sheaf": ("raw/opus/OPUS_BASE_b.md", 1, "sheaf neural nets / local-to-global computation (Bosca & Ghrist 2026), LWPR"),
 "tracer": ("raw/opus/OPUS_CORE2.md", 1, "GFlowNet flow-conservation credit, RTRL / forward-mode sensitivities"),
 "scaling": ("raw/opus/OPUS_CORE2.md", 3, "BuckiNet (Bakarji 2022), AI Feynman"),
 "nucleation": ("raw/r3/CORE_b.md", 2, "SUSTAIN, latent-cause models, ART vigilance"),
 "homology": ("raw/opus/OPUS_NEG.md", 3, "hippocampal place-cell simplicial maps (Dabaghian 2015), topology layers"),
 "eprocess": ("raw/NEG.md", 1, "anytime-valid LLM stopping rules / testing by betting for self-consistency (2025-2026)"),
 "dla": ("raw/r3/CORE_b.md", 3, "frontier/count-based exploration"),
 "rewrite": ("raw/opus/OPUS_BASE_b.md", 3, "DreamCoder, Stitch, babble library learning"),
}
PAIRS = {"EVO1": [("sheaf","nucleation"),("tracer","homology"),("scaling","rewrite")],
         "EVO2": [("eprocess","dla"),("sheaf","tracer"),("nucleation","scaling")],
         "EVO3": [("homology","rewrite"),("dla","sheaf"),("eprocess","tracer")]}
BASINS = """Known idea families (offspring must NOT fall into any of them, including re-skins):
L1: active hypothesis/world-model populations choosing experiments by information gain; libraries of verified programs / MDL program induction; fast episodic store + slow consolidation; markets/coalitions of specialist modules that bid, split, get pruned; self-testing retractable beliefs / provenance ledgers; fast weights / adapters as memory; graphs of intermediate results with local repair.
L2: coupled oscillators/synchrony; cellular automata / morphogenetic or reaction-diffusion substrates; invertible networks; wave/optical/physical computing; linear-recurrent state memories; permutation-invariant set pooling.
L3 (already over-visited escape routes): computation as conserved flow (fluids, reactions, max-flow, Physarum); scaling/renormalization variable discovery; AI with its own aesthetic desires."""
if __name__ == "__main__":
    for agent, pairs in PAIRS.items():
        body = ["Propose 3 fundamentally new AI architecture ideas by EVOLVING existing candidates.",
                "You get 3 parent pairs. For each pair produce ONE offspring:",
                "1. CROSSOVER: fuse the two parents' core mechanisms into one mechanism (a genuine fusion where each parent's mechanism changes the other's behaviour - not two modules side by side).",
                "2. MUTATE AWAY: the offspring must be clearly different from the parents' nearest published work (listed) and from every known family below.",
                "3. KEEP IT IMPORTANT: it must serve a problem that genuinely matters for more capable intelligence.",
                "4. HONESTY CHECK: before the final section, for each offspring name the closest existing work you know; if the offspring is essentially that, mutate again.",
                "Describe mechanisms in plain quantities, update rules and driving signals; name last.", "", BASINS, ""]
        for k, (a, b) in enumerate(pairs, 1):
            body += [f"PAIR {k}", f" Parent A: {idea(*P[a][:2])}", f"   nearest published work: {P[a][2]}",
                     f" Parent B: {idea(*P[b][:2])}", f"   nearest published work: {P[b][2]}", ""]
        open(f"prompts/r4/{agent}.txt", "w").write("\n".join(body) + FORMAT)
        print(agent, len("\n".join(body).split()), "words")
