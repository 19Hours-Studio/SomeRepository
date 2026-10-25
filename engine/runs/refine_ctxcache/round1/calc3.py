"""C (Monte Carlo): hit rate of authoring order vs volatility-sorted (Smith's rule) layout."""
import random
random.seed(0)
def hit(order, blocks, reqs=4000):
    N = sum(b[0] for b in blocks); h = 0
    for _ in range(reqs):
        pos = 0
        for i in order:
            if random.random() < blocks[i][1]: break
            pos += blocks[i][0]
        h += pos / N
    return h / reqs
# concrete agent layout, authoring order typical of agent frameworks
agent = [("system prompt", 3000, 0.0), ("memory/CLAUDE.md", 2000, 0.10), ("todo list", 500, 0.50),
         ("tool schemas", 8000, 0.002), ("project docs", 20000, 0.02), ("conversation", 40000, 0.0)]
blocks = [(s, l) for _, s, l in agent]
auth = list(range(len(agent)))
smith = sorted(auth, key=lambda i: blocks[i][1] / blocks[i][0])
print("agent example: authoring", f"{hit(auth, blocks):.1%}", "-> sorted", f"{hit(smith, blocks):.1%}",
      "order:", [agent[i][0] for i in smith])
# NB: conversation must stay last in practice (it grows); its lam=0 refers to in-place edits only
fixed = [0, 3, 1, 4, 2, 5]  # Smith order restricted to 'conversation last'
print("with conversation pinned last:", f"{hit(fixed, blocks):.1%}", [agent[i][0] for i in fixed])
# random populations
ratios = []; a_s = []; b_s = []
for t in range(300):
    bl = [(random.choice([500, 2000, 8000, 20000]), random.choice([0.0, 0.01, 0.05, 0.2])) for _ in range(10)]
    o = list(range(10)); random.shuffle(o)
    s = sorted(range(10), key=lambda i: bl[i][1] / bl[i][0])
    a, b = hit(o, bl, 800), hit(s, bl, 800)
    a_s.append(a); b_s.append(b)
print(f"random 10-block layouts: mean hit {sum(a_s)/300:.1%} -> {sum(b_s)/300:.1%}; "
      f"mean miss {1-sum(a_s)/300:.1%} -> {1-sum(b_s)/300:.1%}")
fixed = [0, 3, 4, 1, 2, 5]
print("Smith order, conversation pinned last:", f"{hit(fixed, blocks):.1%}")
# volatile tail: memory+todo re-sent after the conversation every turn (always rewritten)
tail = 2500; N = sum(b[0] for b in blocks)
stable = [0, 3, 4, 5]
h_stable = hit(stable, blocks)  # hit() already normalises by full N
print(f"volatile-tail layout (memory+todo always re-sent last): token hit {h_stable:.1%}")
print(f"volatile tail + doc changes as errata: {(N-tail)/N:.1%} (tail is the only miss)")
