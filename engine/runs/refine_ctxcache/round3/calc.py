"""Exact arithmetic and replays for the context-caching answer.

Run: python3 -I calc.py   (stdlib only; traces/ holds the SWE-agent trajectories)
Prices are multipliers of the base input price unless stated (Anthropic: write 1.25x for
5-min TTL, 2x for 1-h TTL, read 0.1x; output 5x base for Sonnet-class pricing).
"""
import itertools, json, math, os, random, statistics

W5, W1H, R, OUT = 1.25, 2.0, 0.10, 5.0
HERE = os.path.dirname(os.path.abspath(__file__))


def section(t):
    print("\n" + "=" * 8, t)


# ---------------------------------------------------------------- A. cost breakdown
section("A. 50-turn agent bill at 100% hit (sys 10k, +2k tool, +300 out per turn)")
def agent_bill(turns=50, sys=10_000, tool=2_000, out=300, clear_after=None, keep=None):
    """clear_after: delete tool results older than `keep` turns via server splice (Idea 2)."""
    reads = writes = outs = 0
    hist = []  # list of (tool, out) per finished turn
    for t in range(turns):
        live = hist if keep is None else hist[-keep:] if len(hist) > keep else hist
        ctx = sys + sum(a + b for a, b in live)
        if t == 0:
            writes += sys + tool
        else:
            reads += ctx
            writes += tool + out   # previous assistant output is new to the cache too
        outs += out
        hist.append((tool, out))
    return reads * R, writes * W5, outs * OUT

r, w, o = agent_bill()
tot = r + w + o
print(f"reads {r/tot:.0%}  writes {w/tot:.0%}  output {o/tot:.0%}")
r2, w2, o2 = agent_bill(keep=10)
print(f"keep only last 10 tool results (splice): input bill x{(r2+w2)/(r+w):.2f}, total x{(r2+w2+o2)/tot:.2f}")


# ---------------------------------------------------------------- B. compaction break-even
section("B. errata vs in-place rewrite break-even (ski rental)")
def tstar(S, e, w=W5, r=R):
    # rewrite: pay (w-r)*S once; errata: pay w*e once + r*e per later turn
    return ((w - r) * S - w * e) / (r * e)
for S, e in [(50_000, 500), (10_000, 2_000), (2_000, 2_000)]:
    print(f"S={S:>6} e={e:>5}: T* = {tstar(S, e):8.1f} turns")


# ---------------------------------------------------------------- C. layout ordering
section("C. block ordering: odds/size rule vs Smith p/size, brute force")
def exp_miss(order, blocks, tail_new):
    """Independent Bernoulli changes; miss = suffix from first changed block + new tokens."""
    total = sum(blocks[b][0] for b in order)
    miss, p_none, pos = 0.0, 1.0, 0
    for b in order:
        s, p = blocks[b]
        miss += p_none * p * (total - pos)
        p_none *= 1 - p
        pos += s
    return miss + tail_new

random.seed(1)
worse_smith = 0; gap = []
for trial in range(3000):
    n = 6
    blocks = {i: (random.choice([200, 500, 2000, 8000, 20000]), random.choice([0.01, 0.05, 0.2, 0.5, 0.8, 0.95])) for i in range(n)}
    best = min(exp_miss(o, blocks, 0) for o in itertools.permutations(range(n)))
    smith = exp_miss(sorted(blocks, key=lambda b: blocks[b][1] / blocks[b][0]), blocks, 0)
    odds = exp_miss(sorted(blocks, key=lambda b: blocks[b][1] / ((1 - blocks[b][1]) * blocks[b][0])), blocks, 0)
    assert abs(odds - best) < 1e-6 * max(1, best), (blocks, odds, best)
    if smith > best + 1e-9:
        worse_smith += 1; gap.append(smith / best - 1)
print(f"odds/size rule optimal in 3000/3000 random 6-block cases; p/size (Smith) suboptimal in {worse_smith}, "
      f"median excess {statistics.median(gap):.1%}, max {max(gap):.1%}")

# agent layout: name -> (tokens, P(change per turn)); conversation appends g tokens/turn
g = 1_000
blocks = {"sys": (3000, 0.0), "memory": (2000, 0.10), "todo": (500, 0.50), "tools": (8000, 0.0),
          "docs": (20000, 0.02), "conv": (40000, 0.0)}
tot_in = sum(s for s, _ in blocks.values()) + g
def hit(miss): return 1 - miss / tot_in
authoring = ["sys", "memory", "todo", "tools", "docs", "conv"]
fixed = [b for b in blocks if b != "conv"]
best_fixed = min(itertools.permutations(fixed), key=lambda o: exp_miss(list(o) + ["conv"], blocks, g))
print(f"authoring order                  hit {hit(exp_miss(authoring, blocks, g)):.1%}")
print(f"optimal order, conversation last hit {hit(exp_miss(list(best_fixed) + ['conv'], blocks, g)):.1%}  {best_fixed}")
# volatile tail: memory+todo re-sent after the conversation every turn (always missed)
tail = blocks["memory"][0] + blocks["todo"][0]
vt = {k: v for k, v in blocks.items() if k not in ("memory", "todo")}
m_vt = exp_miss(["sys", "tools", "docs", "conv"], vt, g + tail)
print(f"volatile tail after conversation  hit {hit(m_vt):.1%}")
m_err = g + tail + 0.02 * 500   # doc change -> ~500-token erratum appended
print(f"+ doc changes as errata           hit {hit(m_err):.1%}")
# conditional tail: re-send memory/todo only when they changed (as errata), else nothing
m_cond = g + 0.10 * 2000 + 0.5 * 500 + 0.02 * 500
print(f"+ tail sent only on change (diff)  hit {hit(m_cond):.1%}")


# ---------------------------------------------------------------- D. real agent traces
section("D. SWE-agent trajectories: observation elision policies (real sizes, chars/4)")
def load_sizes(f):
    d = json.load(open(os.path.join(HERE, "traces", f)))
    h = d["history"]
    def L(m):
        c = m.get("content"); c = c if isinstance(c, str) else json.dumps(c)
        return max(1, len(c) // 4 + (len(json.dumps(m["tool_calls"])) // 4 if m.get("tool_calls") else 0))
    return L(h[0]) + L(h[1]), [L(m) for m in h[2:]]
traces = {f: load_sizes(f) for f in ["marshmallow.traj", "humanevalfix.traj", "testrepo.traj"]}
acts, obs = [], []
for pre, rest in traces.values():
    acts += rest[0::2]; obs += rest[1::2]
print(f"pooled: {len(acts)} actions (median {statistics.median(acts)}), {len(obs)} observations "
      f"(median {statistics.median(obs)}, max {max(obs)})")

def replay(prefix, steps, policy, n=5, polling=1, ph=12):
    """steps: list of (act, obs). policy: 'append' | 'elide' (client rewrite) | 'splice' (server delete).
    Returns (token hit rate, input cost in base-price units, total input tokens processed)."""
    prev = None; hits = tot = 0; cost = 0.0
    for t in range(1, len(steps) + 1):
        hist = steps[:t]
        if policy == "append":
            elided = 0
        else:
            elided = max(0, (t // polling) * polling - n)
        msgs = [prefix]
        for i, (a, o) in enumerate(hist):
            msgs += [a, ph if i < elided else o]
        # cached prefix length vs previous request (block granularity = message)
        if prev is None:
            hit_t = 0
        elif policy == "splice":
            hit_t = sum(msgs[:-2])  # server drops elided KV in place; only new act+obs computed
        else:
            k = 0  # compare message identity (index, elided or not), not sizes
            for i in range(min(len(prev), len(msgs))):
                if prev_id[i] != ids(i, t, elided): break
                k += 1
            hit_t = sum(msgs[:k])
        T = sum(msgs)
        hits += hit_t; tot += T
        cost += hit_t * R + (T - hit_t) * W5
        prev = msgs; prev_id = [ids(i, t, elided) for i in range(len(msgs))]
    return hits / tot, cost, tot

def ids(i, t, elided):
    if i == 0: return ("p",)
    j = (i - 1) // 2
    return ("a", j) if (i - 1) % 2 == 0 else (("ph", j) if j < elided else ("o", j))

random.seed(7)
for L in (30, 80):
    res = {}
    for rep in range(200):
        prefix = random.choice([p for p, _ in traces.values()])
        steps = [(random.choice(acts), random.choice(obs)) for _ in range(L)]
        for name, kw in [("append", dict(policy="append")),
                         ("elide n=5 polling=1", dict(policy="elide", polling=1)),
                         ("elide n=5 polling=5", dict(policy="elide", polling=5)),
                         ("elide n=5 polling=15", dict(policy="elide", polling=15)),
                         ("splice n=5", dict(policy="splice"))]:
            h, c, tt = replay(prefix, steps, **kw)
            res.setdefault(name, []).append((h, c, tt))
    base = statistics.mean(c for _, c, _ in res["append"])
    print(f"-- {L}-step sessions (bootstrap of real step sizes, 200 reps)")
    for name, v in res.items():
        print(f"{name:22s} hit {statistics.mean(h for h,_,_ in v):6.1%}  input cost x{statistics.mean(c for _,c,_ in v)/base:.2f} vs append-only")


# ---------------------------------------------------------------- E. RAG ordering replay
section("E. RAG: 2,000 docs x 500 tok, k=5 per query, sys 2k, query 50 tok, Zipf popularity")
class Trie:
    def __init__(self): self.c = {}; self.n = 0
def walk_insert(root, seq):
    node, hit = root, 0
    for x in seq:
        if x in node.c:
            hit += 1
        node = node.c.setdefault(x, Trie()); node.n += 1
    return hit
def walk_hit(root, seq):
    node, hit = root, 0
    for x in seq:
        if x not in node.c: break
        node = node.c[x]; hit += 1
    return hit
def greedy_order(root, docset):
    """CacheWeaver/RAGBoost-style: follow the cached path that covers the most of this set."""
    node, order, rest = root, [], set(docset)
    while rest:
        cand = [d for d in rest if d in node.c]
        if not cand: break
        d = max(cand, key=lambda d: node.c[d].n)
        order.append(d); rest.remove(d); node = node.c[d]
    return order + sorted(rest)   # remainder in canonical (popularity) order

def rag(s, Q=20_000, N=2000, k=5, doc=500, sysl=2000, ql=50, seed=0):
    rng = random.Random(seed)
    w = [1 / (i + 1) ** s for i in range(N)]
    out = {}
    for mode in ("relevance", "hash", "popularity", "greedy"):
        rng = random.Random(seed); root = Trie(); seen = set(); hit = tot = seg_ok = seg_tot = 0
        for q in range(Q):
            ds = []
            while len(ds) < k:
                d = rng.choices(range(N), weights=w)[0]
                if d not in ds: ds.append(d)
            if mode == "relevance": order = ds                       # retrieval order ~ random wrt id
            elif mode == "hash": order = sorted(ds, key=lambda d: hash((d, 99)))
            elif mode == "popularity": order = sorted(ds)            # id == popularity rank
            else: order = greedy_order(root, ds)
            h = walk_hit(root, order); walk_insert(root, order)
            hit += sysl * (q > 0) + h * doc; tot += sysl + k * doc + ql
            seg_ok += sum(d in seen for d in ds); seg_tot += k; seen.update(ds)
        out[mode] = hit / tot
    out["segment ceiling"] = (seg_ok * doc + sysl * (Q - 1)) / (Q * (sysl + k * doc + ql))
    out["doc occurrences seen before"] = seg_ok / seg_tot
    return out
for s in (0.8, 1.0, 1.2):
    o = rag(s)
    print(f"s={s}: " + "  ".join(f"{k} {v:.1%}" for k, v in o.items()))
print("(doc-only hit rate, excluding the 2k system prompt:)")
for s in (0.8, 1.2):
    o = rag(s, sysl=0)
    print(f"s={s}: " + "  ".join(f"{k} {v:.1%}" for k, v in o.items()))


# ---------------------------------------------------------------- F. storage & bandwidth
section("F. retention break-even and bandwidth (Llama-3-70B, assumptions marked)")
kv_bf16 = 2 * 80 * 8 * 128 * 2           # bytes/token: K+V, 80 layers, 8 KV heads, d=128
print(f"KV/token BF16 {kv_bf16/1024:.0f} KiB, FP8 {kv_bf16/2048:.0f} KiB")
gpu_h, n_gpu, mfu, flops = 2.0, 8, 0.45, 989e12   # ASSUMED $/GPU-h, utilization; H100 dense BF16
flop_tok = 2 * 70e9                        # linear layers; attention extra at long context
def attn_flop(ctx): return 4 * 80 * 8192 * ctx / 2  # causal average
for ctx in (8_000, 32_000, 128_000):
    tps = n_gpu * flops * mfu / (flop_tok + attn_flop(ctx))
    print(f"ctx {ctx:>6}: recompute {tps/1e3:5.1f}k tok/s, ${n_gpu*gpu_h/(tps*3600)*1e6:.3f}/M tok")
tps8k = n_gpu * flops * mfu / (flop_tok + attn_flop(8000))
cost_tok = n_gpu * gpu_h / (tps8k * 3600)
tiers = {"HBM": 2.0 / 80, "DRAM": 0.005, "NVMe": 0.00022}   # $/GB/h, ASSUMED
for tname, p in tiers.items():
    hold = kv_bf16 / 1e9 * p              # $/token/h
    print(f"{tname:5s}: keep only if reused within {cost_tok/hold*60:7.1f} min (BF16)")
for name, bw in [("1 NVMe 7 GB/s", 7e9), ("4 NVMe", 28e9), ("400 Gb/s RDMA", 50e9)]:
    print(f"{name:14s}: load {bw/kv_bf16/1e3:6.1f}k tok/s BF16, {2*bw/kv_bf16/1e3:6.1f}k FP8")
print(f"=> provider cost of recomputing a token at 8k ctx (${cost_tok*1e6:.3f}/M) vs a $3/M list model's "
      f"cache-read price ($0.30/M): price, not cost, sets the hit discount")


# ---------------------------------------------------------------- G. TTL choice
section("G. 5-min vs 1-h TTL, context reused every 6-60 min, N reuses")
for N in (1, 2, 5, 20):
    c5 = W5 * (N + 1)           # every reuse after >5 min is a fresh write
    c1 = W1H + R * N
    print(f"N={N:>2}: 5-min {c5:5.2f}x  1-h {c1:5.2f}x  per cached token")


# ---------------------------------------------------------------- H. reasoning stripped by chat template
section("H. template strips earlier reasoning at each new user message (Qwen3/gpt-oss style)")
def strip_replay(U=10, k=20, think=300, act=100, obs=1000, user=200, sysl=10_000, strip=True):
    """U user queries, each followed by k tool steps. Generated think+act are cached (decode KV kept);
    each step's new tokens are the tool output. With strip=True the rendered history drops reasoning of
    earlier queries' assistant turns, so the first step after a new user message diverges at the first
    assistant turn of the previous query and recomputes that whole query span."""
    hits = tot = 0
    hist = sysl                                   # rendered history length before current query
    for u in range(U):
        q = 0                                     # tokens of the current query so far
        for j in range(k):
            T = hist + user + q
            if j == 0:
                miss = user if (u == 0 or not strip) else user + prev_span
                miss = T if u == 0 else miss
            else:
                miss = obs
            q += think + act + obs
            hits += T - miss; tot += T
        prev_span = k * (act + obs)               # previous query as re-rendered without reasoning
        hist += user + (k * (act + obs) if strip else q)
    return hits / tot
for k in (5, 20, 50):
    a = strip_replay(k=k, strip=False); b = strip_replay(k=k, strip=True)
    ca, cb = a * R + (1 - a) * W5, b * R + (1 - b) * W5
    print(f"k={k:>2} tool steps/query: keep reasoning hit {a:.1%}   strip reasoning hit {b:.1%}   "
          f"per-token input cost x{cb/ca:.2f} (before the shorter context is counted)")


# ---------------------------------------------------------------- I. gate fallback break-even (Idea 3)
section("I. segment cache with gate: saving vs gate fallback rate f")
load, refr, shadow = 0.10, 0.15, 0.01
for s, pfx_hit, seg_cov in [(0.8, 0.339, 0.961), (1.2, 0.596, 0.961)]:
    pfx = pfx_hit * R + (1 - pfx_hit) * 1.0
    seg = seg_cov * (load + refr) + (1 - seg_cov) * 1.0
    row = []
    for f in (0.0, 0.1, 0.3, 0.5):
        # fallback = exact path, which still gets the exact prefix hit
        c = (1 - f) * seg + f * pfx + shadow
        row.append(f"f={f:.0%}: x{pfx/c:.2f}")
    print(f"s={s}: prefix {pfx:.3f}/doc tok, segment {seg:.3f}; saving " + "  ".join(row))


# ---------------------------------------------------------------- J. breakpoint placement
section("J. Anthropic breakpoints: volatile tail after last breakpoint; 20-block lookback")
tail, turns = 2_500, 50
print(f"tail {tail} tok/turn billed as plain input (1.0x) not write (1.25x): saves {0.25*tail*turns:,.0f} "
      f"base-token units over {turns} turns (= {0.25*tail*turns/(tail*turns*1.25):.0%} of tail cost)")
# one breakpoint at end vs explicit breakpoints at stable boundaries, edit at block b of B
B, blk = 200, 400   # 200 content blocks of ~400 tokens after a 13k system+tools prefix
sysl = 13_000
for b in (150, 185, 195):
    single = sysl + b * blk if (B - b) <= 20 else 0          # lookback only finds entries <=20 blocks back
    multi = sysl + (b * blk if (B - b) <= 20 else 0)       # explicit breakpoint after system+tools
    print(f"edit at block {b}/{B}: one end breakpoint reuses {single:,} tok; + breakpoint after tools reuses {max(single, multi):,} tok")
