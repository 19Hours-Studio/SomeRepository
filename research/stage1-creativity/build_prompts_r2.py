"""Раунд 2: условия, построенные из находок раунда 1. Случайность — secrets."""
import secrets, json
from build_prompts import FORMAT, TASK, words, rng  # те же шаблоны и пул
MSC = ["03 Mathematical logic and foundations","05 Combinatorics","06 Order, lattices, ordered algebraic structures",
"08 General algebraic systems","11 Number theory","12 Field theory and polynomials","13 Commutative algebra",
"14 Algebraic geometry","15 Linear and multilinear algebra","16 Associative rings and algebras","17 Nonassociative rings and algebras",
"18 Category theory; homological algebra","19 K-theory","20 Group theory","22 Topological groups, Lie groups","26 Real functions",
"28 Measure and integration","30 Functions of a complex variable","31 Potential theory","32 Several complex variables",
"33 Special functions","34 Ordinary differential equations","35 Partial differential equations","37 Dynamical systems and ergodic theory",
"39 Difference and functional equations","40 Sequences, series, summability","41 Approximations and expansions",
"42 Harmonic analysis on Euclidean spaces","43 Abstract harmonic analysis","44 Integral transforms","45 Integral equations",
"46 Functional analysis","47 Operator theory","49 Calculus of variations and optimal control","51 Geometry",
"52 Convex and discrete geometry","53 Differential geometry","54 General topology","55 Algebraic topology",
"57 Manifolds and cell complexes","58 Global analysis","60 Probability theory","62 Statistics","65 Numerical analysis",
"70 Mechanics of particles and systems","74 Mechanics of deformable solids","76 Fluid mechanics","78 Optics, electromagnetic theory",
"80 Classical thermodynamics, heat transfer","81 Quantum theory","82 Statistical mechanics","83 Relativity and gravitational theory",
"85 Astronomy and astrophysics","86 Geophysics","90 Operations research, mathematical programming","91 Game theory, economics",
"92 Biology and other natural sciences","93 Systems theory; control","94 Information and communication theory, circuits"]
ATTRACTOR_MAP = """Empirically, models like you converge on these idea families (forbidden, including re-skins and recombinations):
A. population of hypotheses/world models + choosing experiments by information gain (active causal inference)
B. library of verified executable programs / MDL program induction / rewrite rules
C. fast episodic store + slow offline consolidation into weights
D. market/coalition of specialist modules that bid, split and get pruned
E. self-testing, retractable beliefs; editable knowledge
F. fast weights / adapters / plasticity as memory
G. graph of intermediate results with local verification and repair"""
WEAKNESS_BAN = """Do NOT justify any idea by fixing a known weakness of current AI (catastrophic forgetting, interpretability/auditability, editability, context length/cost, verification/guarantees, efficiency, sample efficiency). Instead, the DIFFERENCE line must name a genuinely new capability or behaviour that nobody is currently asking AI for."""
P = {}
P["MAP"] = TASK + "\n" + ATTRACTOR_MAP + "\n" + FORMAT
fields = rng.sample(MSC, 3)
P["MSC"] = TASK + "\nEach idea's core computational primitive (its state, its update rule and its learning signal) must come from the mathematical/scientific field drawn at random for it - not as a metaphor, as the actual mechanism.\n" + \
  "\n".join(f"Idea {i+1} field: MSC {f}" for i, f in enumerate(fields)) + "\n" + FORMAT
locks = [words(8) for _ in range(3)]
P["LOCK"] = TASK + "\nHard, machine-checked constraint: the MECHANISM text of idea i must contain ALL 8 locked words of LOCK i, exactly as written, in the given order (fill the gaps between them with your own words). The locked words were drawn at random from unrelated files. A script will reject ideas that violate this, and the idea must still be a coherent, buildable architecture, with the locked words doing real work in it.\n" + \
  "\n".join(f"LOCK {i+1}: {l}" for i, l in enumerate(locks)) + "\n" + FORMAT
P["REFRAME"] = TASK + "\n" + WEAKNESS_BAN + "\n" + FORMAT
f2 = rng.sample([f for f in MSC if f not in fields], 3)
P["STACK"] = TASK + """
Pipeline you must follow:
1. Write one sentence naming the paradigm all mainstream AI shares, then forbid that whole paradigm (not a list of methods - the paradigm).
2. """ + ATTRACTOR_MAP.replace("\n", "\n   ") + """
3. Each idea's core primitive must come from its randomly drawn field (as the actual mechanism, not as a metaphor):
""" + "\n".join(f"   Idea {i+1} field: MSC {f}" for i, f in enumerate(f2)) + """
4. Describe the mechanism in plain quantities, flows, update rules and driving signals; no ML buzzwords; name it last.
5. """ + WEAKNESS_BAN + "\n" + FORMAT
P["SELFPRED"] = """A model like you (a Claude model) was asked the following prompt twice, in two independent sessions:
---
""" + TASK + """
---
Predict, for EACH of the two runs, the 3 core mechanisms it most likely produced (one line each). Then estimate how many of the 3 ideas the two runs share in substance. Be specific about mechanisms, not just field names. Do not use tools. Under 200 words."""
for k, v in P.items(): open(f"prompts/r2/{k}.txt", "w").write(v)
json.dump({"MSC": fields, "STACK_MSC": f2, "LOCK": locks}, open("prompts/r2/draws.json", "w"), indent=1)
print(json.dumps({"MSC": fields, "STACK_MSC": f2, "LOCK": locks}, indent=1))
