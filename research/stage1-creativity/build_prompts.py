"""Собирает промпты для 9 условий. Вся случайность — из secrets (внешняя энтропия, не модель)."""
import secrets, json, sys
rng = secrets.SystemRandom()
pool = open("wordpool.txt").read().split()

FORMAT = """
Finish your reply with a section that starts with the exact line `=== IDEAS ===` and contains exactly 3 ideas in this format:
IDEA 1
NAME: (max 5 words)
MECHANISM: (2-4 sentences: what is computed, what is stored, how it learns/adapts)
DIFFERENCE: (1 sentence: what it can do that current architectures fundamentally cannot)
(same for IDEA 2, IDEA 3)
Do not use any tools. Reply with text only. Keep everything under 450 words."""

TASK = "Propose 3 fundamentally new AI architecture ideas (not incremental tweaks of transformers)."

AXIOMS = [
 "training and inference are separate phases",
 "the model is a fixed function between updates",
 "learning is driven by minimizing a loss via gradients",
 "information is represented as vectors of real numbers",
 "computation proceeds in discrete synchronous steps/layers",
 "a model is a single entity with one set of parameters",
 "input is processed as a sequence of discrete tokens",
 "memory and computation are separate (weights vs. context)",
 "more parameters/data = more capability",
 "the model does not choose what data it learns from",
 "outputs are produced once; there is no revision of committed outputs",
 "the architecture is designed by humans, not grown",
]
ANOMALIES = [
 "the reversal curse: a model trained on 'A is B' often cannot answer 'B is A'",
 "grokking: generalization appears suddenly long after the training loss reached zero",
 "attention sinks: models dump huge attention mass on the first token, which carries no meaning",
 "in-context learning: models learn new tasks from examples without any weight update",
 "superposition: networks store far more features than they have neurons",
 "double descent: test error falls, rises, then falls again as model size grows",
 "catastrophic forgetting: learning a new task erases old ones, while brains do not suffer this",
 "lottery tickets: tiny sparse subnetworks inside big nets train as well as the whole net",
 "chain-of-thought helps even when the written reasoning is partly wrong",
 "humans learn language from ~100M words; LLMs need ~10T",
]

def words(n): return " ".join(rng.choice(pool) for _ in range(n))

P = {}
P["B1"] = P["B2"] = TASK + "\n" + FORMAT
P["NOISE"] = TASK + "\nEach idea MUST be built from a mechanism genuinely derived from the random seed words given for it (not just decorated with them). Seed words were drawn at random from unrelated system files.\n" + \
  "\n".join(f"Seeds for idea {i+1}: {words(4)}" for i in range(3)) + "\n" + FORMAT
P["DIFF"] = TASK + """
Use a "text diffusion" process instead of writing ideas directly. For each idea you get a NOISE sequence of random words.
Run 4 denoising steps. At each step rewrite the previous text so it becomes a bit more coherent, changing at most ~35% of the words; keep the global shape and surprising word choices from the noise where possible. Step 4 must be a coherent architecture idea. Show all steps briefly (one line each), then extract the ideas.
""" + "\n".join(f"NOISE {i+1}: {words(30)}" for i in range(3)) + "\n" + FORMAT
P["NEG"] = TASK + """
First, honestly list the 12 ideas that you (and most AI researchers) would propose FIRST for this question - your own most obvious, most probable answers. Then treat all of them, and anything adjacent to them, as forbidden. Only then propose ideas that lie outside that whole region.
""" + FORMAT
ax = rng.sample(AXIOMS, 6)
P["AXIOM"] = TASK + "\nEach idea must be built by INVERTING two fundamental assumptions of current AI (assume the opposite is true and design what follows):\n" + \
  "\n".join(f"Idea {i+1}: invert '{ax[2*i]}' AND '{ax[2*i+1]}'" for i in range(3)) + "\n" + FORMAT
P["MECH"] = TASK + """
Hard constraint: you may NOT use any named concept, method or buzzword from ML/neuroscience (no 'attention', 'transformer', 'memory network', 'neuro-symbolic', 'world model', 'hierarchical', 'brain-inspired', 'meta-learning', 'experts', 'graph', 'spiking', 'energy', 'quantum', etc.). Describe each idea ONLY in terms of: what quantities exist, how they flow, what update rule changes them, and what signal drives the update. Think in plain mechanics first; give the NAME last, after the mechanism is fixed.
""" + FORMAT
an = rng.sample(ANOMALIES, 3)
P["ANOMALY"] = TASK + "\nDerive each idea from a real, unexplained empirical phenomenon of current models. Assume the phenomenon is a clue revealing what the RIGHT architecture would be, and design that architecture.\n" + \
  "\n".join(f"Idea {i+1} clue: {a}" for i, a in enumerate(an)) + "\n" + FORMAT
P["ABSURD"] = TASK + """
Process: first write 5 deliberately absurd, stupid or 'wrong' architecture ideas (one line each, the sillier the better - do not filter). Then for each, ask: what is the hidden kernel that would actually work? Pick the 3 most promising kernels and turn them into serious ideas.
""" + FORMAT

for k, v in P.items():
    open(f"prompts/{k}.txt", "w").write(v)
print(json.dumps({"axioms": ax, "anomalies": an}, ensure_ascii=False, indent=1))
