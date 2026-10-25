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


# ---------------------------------------------------------------- K. parallel fan-out
section("K. parallel fan-out on a shared prefix P: all-at-once vs one warm-up request first")
# Anthropic: a cache entry becomes available only after the first response begins.
for N in (2, 5, 10, 50):
    cold = N * W5                       # every concurrent request misses and writes P
    warm = W5 + (N - 1) * R             # first request writes, the rest read
    print(f"N={N:>2}: concurrent x{cold:.2f}P  warm-up first x{warm:.2f}P  -> {cold/warm:.1f}x cheaper on P, "
          f"+1 TTFT of latency")


# ---------------------------------------------------------------- L. batch stacking
section("L. batch discount (0.5x) stacked on caching, best-effort hits h inside the batch")
# Anthropic: batch halves every token price and stacks with cache multipliers.
P, out_b, n_b = 20_000, 500, 1000       # shared 20k prefix, 1,000 requests, 500 output tokens each
def batch_cost(h, warm=True, batch=0.5, ttl_write=W1H):
    pre = ttl_write * P if warm else 0  # synchronous warm-up with 1-h TTL
    per = h * R * P + (1 - h) * W5 * P + out_b * OUT
    return pre + n_b * batch * per
base = n_b * (R * P + out_b * OUT)      # interactive, 100% hits
for h in (0.3, 0.7, 0.98):
    print(f"h={h:.0%}: batch cost x{batch_cost(h)/base:.2f} of interactive at 100% hits")
print(f"(batch at 100% hits: x{batch_cost(1.0)/base:.2f}; cached read becomes 0.05x base)")


# ---------------------------------------------------------------- M. clearing period (square-root rule)
section("M. API-side clearing of old tool results: choose the clear period T (prefix kept exactly)")
def clear_bill(turns=200, sys=10_000, tool=2_000, out=300, ph=20, keep=3, T=None, anchor=True):
    """Tool results older than `keep` turns become ph-token placeholders, in batches every T turns.
    anchor=True: the prefix up to the first newly cleared block is still cached (vLLM/OpenAI-style
    block caching). anchor=False: only the system prompt survives (Anthropic with no breakpoint there)."""
    st = []            # per turn: current tool size
    prev = None        # previous request's block list
    cost = 0.0
    for t in range(turns):
        if T and t and t % T == 0:
            for i in range(len(st) - keep):
                st[i] = ph
        blocks = [("sys", sys)] + [(f"t{i}:{s}", s + out) for i, s in enumerate(st)] + [("new", tool)]
        if prev is None:
            cost += W5 * sum(s for _, s in blocks)
        else:
            lcp = 0
            for a, b in zip(prev[:-1], blocks):
                if a != b: break
                lcp += 1
            if not anchor and lcp < len(prev) - 1:
                lcp = 1
            hit = sum(s for _, s in blocks[:lcp])
            cost += R * hit + W5 * (sum(s for _, s in blocks) - hit)
        cost += OUT * out
        prev = blocks[:-1] + [(f"t{len(st)}:{tool}", tool + out)]
        st.append(tool)
    return cost
never = clear_bill()
print(f"never clear: x1.00 (200 turns)")
best = min(range(1, 101), key=lambda T: clear_bill(T=T))
for T in (1, 5, 10, best, 40, 100):
    print(f"clear every {T:>3} turns: x{clear_bill(T=T)/never:.2f}" + ("  <- best" if T == best else ""))
print(f"same, no cache anchor at the clear point, T={best}: x{clear_bill(T=best, anchor=False)/never:.2f}; "
      f"best T then {min(range(1,101), key=lambda T: clear_bill(T=T, anchor=False))}: "
      f"x{min(clear_bill(T=T, anchor=False) for T in range(1,101))/never:.2f}")
g, keep_tok = 2_000 - 20, 3 * 2_300
print(f"square-root estimate T* ~ sqrt(2*{W5}*K/({R}*g)) with K = rewritten tokens per clear "
      f"(~keep window + sys if unanchored): anchored {math.sqrt(2*W5*keep_tok/(R*g)):.0f}, "
      f"unanchored {math.sqrt(2*W5*(keep_tok+10_000)/(R*g)):.0f}")


# ---------------------------------------------------------------- N. real agent traces
section("N. REAL traces: 42 SWE-agent runs, Claude Sonnet 4 (SWE-bench Verified, every 12th instance), exact per-step queries")
TOOLS = 1_500   # assumed tool-schema tokens; tools are passed separately and are not in the stored queries
DR = json.load(open(os.path.join(HERE, "traces", "c4", "steps.json")))
def real_replay(S, policy, T=None, keep=3, ph=20, trigger=100_000, hook=None, minsz=0):
    """Blocks are messages (tokens = chars/4). policy:
    append  - what the agent actually sent (append-only, cache_control on the last 2 messages)
    clear   - client replaces tool results older than `keep` with ph-token placeholders every T steps (persisted)
    ctxedit - server re-applies 'clear all but keep' whenever the full input exceeds trigger (Anthropic default 100k)
    splice  - server drops old tool results every step without rewriting the suffix (Idea 2, approximate)"""
    prev, cleared, reads, writes, hit_t, tot_t = None, set(), 0.0, 0.0, 0.0, 0.0
    for i, s in enumerate(S):
        msgs = [(m[0], m[1] / 4, m[2]) for m in s["m"]]
        tidx = [j for j, m in enumerate(msgs) if m[0] == "tool"]
        old = {j for j in (tidx[:-keep] if len(tidx) > keep else []) if msgs[j][1] > minsz}
        if policy == "clear" and T and i and i % T == 0: cleared |= old
        if policy == "splice": cleared = old
        if policy == "ctxedit": cleared = old if TOOLS + sum(m[1] for m in msgs) > trigger else set()
        blocks = [("tools", TOOLS, "t")] + [(m[0], ph if j in cleared else m[1], ("X" if j in cleared else "") + m[2])
                                            for j, m in enumerate(msgs)]
        tot = sum(b[1] for b in blocks)
        if prev is None: hit = 0.0
        elif policy == "splice":
            keys = {p[2] for p in prev}; hit = sum(b[1] for b in blocks if b[2] in keys)
        else:
            l = 0
            while l < min(len(prev), len(blocks)) and prev[l][2] == blocks[l][2]: l += 1
            hit = sum(b[1] for b in blocks[:l])
        reads += R * hit; writes += W5 * (tot - hit); hit_t += hit; tot_t += tot
        if hook: hook(i, S, hit, tot)
        prev = blocks
    outs = OUT * sum(m[1] / 4 for m in S[-1]["m"] if m[0] == "assistant")
    return reads, writes, outs, hit_t, tot_t
def real_agg(policy, **kw):
    acc = [0.0] * 5
    for S in DR.values():
        acc = [a + b for a, b in zip(acc, real_replay(S, policy, **kw))]
    return acc
steps = [len(S) for S in DR.values()]
fin = [TOOLS + sum(m[1] for m in S[-1]["m"]) / 4 for S in DR.values()]
appendonly = sum(1 for S in DR.values() for i in range(1, len(S))
                 if [m[2] for m in S[i]["m"][:len(S[i-1]["m"])]] == [m[2] for m in S[i-1]["m"]])
obs = [m[1] / 4 for S in DR.values() for m in S[-1]["m"] if m[0] == "tool"]
print(f"steps/session median {statistics.median(steps)} max {max(steps)}; final context median {statistics.median(fin):,.0f} "
      f"max {max(fin):,.0f} tok; observation median {statistics.median(obs):.0f} p90 {sorted(obs)[int(.9*len(obs))]:.0f} tok")
print(f"append-only step transitions: {appendonly}/{sum(steps)-len(steps)} (the rest are re-queries that replace the last turn)")
r, w, o, h, t = real_agg("append"); base = r + w + o
print(f"as sent: token hit rate {h/t:.1%}; bill reads {r/base:.0%} writes {w/base:.0%} output {o/base:.0%}")
res = {T: sum(real_agg("clear", T=T)[:3]) / base for T in range(1, 41)}
bestT = min(res, key=res.get)
for T in (1, 3, 5, bestT, 20, 40):
    print(f"clear every {T:>2} steps (keep 3): x{res[T]:.3f}" + ("  <- best" if T == bestT else ""))
rr = real_agg("clear", T=bestT); print(f"   hit rate at best T: {rr[3]/rr[4]:.1%}")
print(f"Anthropic context editing, default trigger 100k, keep 3: x{sum(real_agg('ctxedit')[:3])/base:.3f}; "
      f"trigger 30k: x{sum(real_agg('ctxedit', trigger=30_000)[:3])/base:.3f}")
sp = real_agg("splice"); print(f"server splice keep 3 (runner only): x{sum(sp[:3])/base:.3f}, hit {sp[3]/sp[4]:.1%}")
g = statistics.mean(obs) - 20; Kk = 3 * (statistics.mean(obs) + 60)
print(f"square-root rule with real g={g:.0f}, K~{Kk:.0f}: T* ~ {math.sqrt(2*W5*Kk/(R*g)):.0f} (replay best {bestT})")

print("-- sweep: keep window and 'clear only results larger than X tokens' (best T for each)")
for keep in (1, 3, 5, 10):
    for minsz in (0, 500):
        rs = {T: sum(real_agg("clear", T=T, keep=keep, minsz=minsz)[:3]) / base for T in range(1, 41)}
        bt = min(rs, key=rs.get)
        sp = sum(real_agg("splice", keep=keep, minsz=minsz)[:3]) / base
        print(f"keep {keep:>2}, clear only > {minsz:>3} tok: periodic best T={bt:>2} x{rs[bt]:.3f}   server splice x{sp:.3f}")


# ---------------------------------------------------------------- O. runner GPU time on the real traces
section("O. Runner's GPU time on the same 42 real sessions (roofline model; assumptions marked)")
# ASSUMPTIONS: Llama-3-70B-class dense model on 8xH100; FP8 weights (70 GB) and FP8 KV (160 KiB/token) as the
# baseline (current best practice); prefill at 45% of 8x989 TFLOPS; decode at 70% of 8x3.35 TB/s with 32
# concurrent sequences sharing the weight reads; cached KV is resident (agent steps are seconds apart).
PF, BW, WB, B = 0.45 * 8 * 989e12, 0.70 * 8 * 3.35e12, 70e9, 32
ATT = 4 * 80 * 8192          # attention FLOPs per (query, key) pair across layers
def out_sizes(S):
    m = []
    for i in range(len(S)):
        if i + 1 < len(S):
            new = S[i + 1]["m"][len(S[i]["m"]):]
            m.append(sum(x[1] / 4 for x in new if x[0] == "assistant") or 150)
        else:
            m.append(150)
    return m
def gpu_session(S, policy, kvb=163_840, **kw):
    per = []
    real_replay(S, policy, hook=lambda i, S_, h, t: per.append((h, t)), **kw)
    m = out_sizes(S)
    pre = dec = ctx_part = 0.0
    for (h, t), mo in zip(per, m):
        n = t - h
        pre += (2 * 70e9 * n + ATT * n * (h + n / 2)) / PF
        ctx_part += ATT * n * h / PF
        for j in range(int(mo)):
            C = t + j
            dec += (WB / B + kvb * C) / BW
            ctx_part += kvb * C / BW
    return pre, dec, ctx_part
def gpu_agg(policy, **kw):
    acc = [0.0, 0.0, 0.0]
    for S in DR.values():
        acc = [a + b for a, b in zip(acc, gpu_session(S, policy, **kw))]
    return acc
def nocache(S):
    pre = dec = 0.0
    m = out_sizes(S)
    for i, s in enumerate(S):
        t = TOOLS + sum(x[1] for x in s["m"]) / 4
        pre += (2 * 70e9 * t + ATT * t * t / 2) / PF
        dec += sum((WB / B + 163_840 * (t + j)) / BW for j in range(int(m[i])))
    return pre + dec
nc = sum(nocache(S) for S in DR.values())
pb, db, cb = gpu_agg("append"); bb = pb + db
print(f"no prefix cache: x{nc/bb:.2f} of the prefix-cached baseline")
print(f"prefix-cached baseline: prefill {pb/bb:.0%}, decode {db/bb:.0%}; work attributable to cached context "
      f"(attention over cached keys + decode KV reads) {cb/bb:.0%}; node-seconds/session {bb/len(DR):.1f}, "
      f"${bb/len(DR)*8*2/3600:.3f} at $2/GPU-h")
for name, pol, kw in [("periodic clear keep 3, T=9 (exact)", "clear", dict(T=9)),
                      ("clear keep 1 every step (exact)", "clear", dict(T=1, keep=1)),
                      ("server splice keep 3 (approximate)", "splice", {}),
                      ("4-bit KV, no clearing (approximate)", "append", dict(kvb=81_920)),
                      ("periodic clear T=9 + 4-bit KV", "clear", dict(T=9, kvb=81_920)),
                      ("splice keep 3 + 4-bit KV", "splice", dict(kvb=81_920))]:
    p, d, c = gpu_agg(pol, **kw)
    print(f"{name:<38} GPU time x{(p+d)/bb:.3f}  (prefill x{p/pb:.2f}, decode x{d/db:.2f})")


section("N2. rolling masking (Complexity-Trap style, window 10, every step) vs the same masking batched; long sessions")
r10 = sum(real_agg("clear", T=1, keep=10)[:3]) / base
print(f"keep 10, clear every step: x{r10:.3f}; best batched (T=18): x{sum(real_agg('clear', T=18, keep=10)[:3])/base:.3f}")
long = {k: S for k, S in DR.items() if len(S) >= 80}
def sub_agg(D_, policy, **kw):
    acc = [0.0] * 5
    for S in D_.values(): acc = [a + b for a, b in zip(acc, real_replay(S, policy, **kw))]
    return sum(acc[:3])
lb = sub_agg(long, "append")
rs = {T: sub_agg(long, "clear", T=T) / lb for T in range(1, 41)}
bt = min(rs, key=rs.get)
print(f"{len(long)} sessions with >= 80 steps: periodic keep 3 best T={bt} x{rs[bt]:.3f}; splice keep 3 x{sub_agg(long, 'splice')/lb:.3f}")

# ---------------------------------------------------------------- P. round 6: same 42 sessions, real tokenizer, full text
section("P. Round 6: same 42 sessions re-extracted from full text (legacy Claude tokenizer, tool inputs split out)")
# steps2.json from traces/c4/extract2.py: messages [role, tokens, hash, kind], kind in system/user/thought/args/tool;
# 'out' = generated tokens; 'pl'/'pg' = speculative-decoding passes (proposed k, accepted a) replayed on real outputs.
D2 = {k: v for k, v in json.load(open(os.path.join(HERE, "traces", "c4", "steps2.json"))).items()}
SON = dict(inp=3.0, w=3.75, r=0.30, out=15.0)   # Claude Sonnet 4 list prices, $/M tokens
def replay2(S, policy="append", T=None, keep=3, kinds=("tool",), ph=20, minsz=0, hook=None, trigger=100_000):
    """policy: append (as sent) | clear (client clears kinds older than the last `keep` of each kind every T steps,
    persisted; breakpoint at the first uncleared block) | splice (server drops them every step, no suffix rewrite)."""
    prev, cleared, reads, writes, hit_t, tot_t, outs = None, set(), 0.0, 0.0, 0.0, 0.0, 0.0
    for i, s in enumerate(S):
        msgs = s["m"]
        old = set()
        for kd in kinds:
            idx = [j for j, m in enumerate(msgs) if m[3] == kd]
            old |= {j for j in (idx[:-keep] if len(idx) > keep else []) if msgs[j][1] > minsz}
        if policy == "clear" and T and i and i % T == 0: cleared |= old
        if policy == "splice": cleared = old
        if policy == "ctxedit": cleared = old if TOOLS + sum(m[1] for m in msgs) > trigger else set()
        blocks = [("tools", TOOLS, "t")] + [(m[0], min(ph, m[1]) if j in cleared else m[1], ("X" if j in cleared else "") + m[2])
                                            for j, m in enumerate(msgs)]
        tot = sum(b[1] for b in blocks)
        if prev is None: hit = 0.0
        elif policy == "splice":
            keys = {p[2] for p in prev}; hit = sum(b[1] for b in blocks if b[2] in keys)
        else:
            l = 0
            while l < min(len(prev), len(blocks)) and prev[l][2] == blocks[l][2]: l += 1
            hit = sum(b[1] for b in blocks[:l])
        reads += R * hit; writes += W5 * (tot - hit); hit_t += hit; tot_t += tot; outs += OUT * s["out"]
        if hook: hook(i, s, hit, tot)
        prev = blocks
    return reads, writes, outs, hit_t, tot_t
def agg2(policy="append", D_=None, **kw):
    acc = [0.0] * 5
    for S in (D_ or D2).values(): acc = [a + b for a, b in zip(acc, replay2(S["steps"], policy, **kw))]
    return acc
comp = {}
for v in D2.values():
    for m in v["steps"][-1]["m"]: comp[m[3]] = comp.get(m[3], 0) + m[1]
ct = sum(comp.values())
print("final-context composition: " + ", ".join(f"{k} {x/ct:.1%}" for k, x in sorted(comp.items(), key=lambda z: -z[1]) if x)
      + f"; mean final context {ct/len(D2)+TOOLS:,.0f} tok (round 5 chars/4: 43,780 + tools)")
r2, w2, o2, h2, t2 = agg2(); b2 = r2 + w2 + o2
print(f"as sent: hit {h2/t2:.1%}; bill reads {r2/b2:.0%} writes {w2/b2:.0%} output {o2/b2:.0%}")
# check the bill model against SWE-agent's own logged cost (litellm, Sonnet 4 list prices incl. cache pricing)
model_usd = sum((r2 / R * SON["r"] + w2 / W5 * SON["w"] + o2 / OUT * SON["out"]) / 1e6 for _ in [0])
logged = sum(v["cost"] for v in D2.values())
print(f"bill-model check: modelled ${model_usd:.2f} vs logged instance_cost ${logged:.2f} for 42 sessions "
      f"(ratio {model_usd/logged:.2f}; tokenizer proxy, 1.5k tool schema assumed, output counted from the next request)")
def best(policy, kinds=("tool",), keep=3, minsz=0, D_=None, base_=None):
    base_ = base_ or b2
    rs = {T: sum(agg2(policy, D_=D_, T=T, keep=keep, kinds=kinds, minsz=minsz)[:3]) / base_ for T in range(1, 41)}
    bt = min(rs, key=rs.get); return bt, rs[bt], rs
print("-- API-side, exact KV; content dropped on purpose. Bill relative to 'as sent'.")
rows = [("results, keep 3", ("tool",), 3, 0), ("results, keep 10 (Complexity-Trap window)", ("tool",), 10, 0),
        ("results + tool inputs, keep 3", ("tool", "args"), 3, 0), ("results + tool inputs, keep 10", ("tool", "args"), 10, 0),
        ("results + tool inputs >200 tok, keep 3", ("tool", "args"), 3, 200), ("results + inputs, keep 1", ("tool", "args"), 1, 0)]
for name, kd, kp, mz in rows:
    bt, v, rs = best("clear", kd, kp, mz)
    sp = sum(agg2("splice", keep=kp, kinds=kd, minsz=mz)[:3]) / b2
    print(f"{name:<42} rolling (T=1) x{rs[1]:.3f}   batched best T={bt:>2} x{v:.3f}   server splice x{sp:.3f}")
# provider-side context editing at its best settings: server re-applies clearing to the full history on every request
# over the trigger (stateless), so the cleared set rolls forward one turn per step
ce = {(tr, kd): sum(agg2("ctxedit", trigger=tr, kinds=kd)[:3]) / b2
      for tr in (20_000, 30_000, 50_000, 100_000) for kd in (("tool",), ("tool", "args"))}
print("Anthropic-style context editing (stateless, keep 3): " + "; ".join(
      f"trigger {tr//1000}k{' +inputs' if len(kd) > 1 else ''} x{v:.3f}" for (tr, kd), v in ce.items()))
# floor: what any context-reduction policy can reach -- only the new tokens are written, context = sys+task+last turn
fl = 0.0
for v in D2.values():
    for i, s in enumerate(v["steps"]):
        fl += OUT * s["out"] + W5 * (s["m"][-1][1] + (s["m"][-2][1] if len(s["m"]) > 2 else 0)) + R * (TOOLS + sum(m[1] for m in s["m"][:2]))
print(f"floor (keep nothing but system+task+newest turn, all hits): x{fl/b2:.3f}; output alone x{o2/b2:.3f}")
long2 = {k: v for k, v in D2.items() if len(v["steps"]) >= 80}
lb2 = sum(agg2(D_=long2)[:3])
for name, kd, kp in [("results, keep 3", ("tool",), 3), ("results + inputs, keep 3", ("tool", "args"), 3),
                     ("results + inputs, keep 10", ("tool", "args"), 10)]:
    bt, v, _ = best("clear", kd, kp, D_=long2, base_=lb2)
    print(f"{len(long2)} sessions >= 80 steps, {name:<26}: batched best T={bt} x{v:.3f}")


# ---------------------------------------------------------------- Q. runner: lossless speculative decoding on real outputs
section("Q. Runner: decode passes with model-free drafts (prompt lookup / + cross-session corpus), replayed on real outputs")
# A deterministic draft d is accepted with prob p(d) under speculative sampling; 'sample y ~ p, accept iff y == d' is the
# same algorithm, so replaying the realized outputs gives the exact accepted-length distribution (for this tokenizer).
def spec_stats(key):
    T_ = P_ = K_ = 0
    for v in D2.values():
        for s in v["steps"]:
            T_ += s["out"]; P_ += len(s[key]); K_ += sum(p[0] for p in s[key])
    return T_, P_, K_
for key, name in [("pl", "prompt lookup (n<=4, k<=8)"), ("pg", "+ earlier sessions' outputs"),
                  ("pk", "pg, old results cleared"), ("pk2", "pg, old results+inputs cleared")]:
    T_, P_, K_ = spec_stats(key)
    print(f"{name:<30}: {T_:,} output tokens in {P_:,} passes -> {T_/P_:.2f} tokens/pass; mean draft {K_/P_:.1f}, "
          f"draft acceptance {(T_-P_)/max(K_,1):.0%}")
def decoded_credit(S, orig):
    """Round 7 fix: a self-hosted runner keeps the KV of the tokens it just generated (vLLM caches full blocks of decoded
    tokens), so the previous turn's thought + tool input need no prefill next turn, unless the client rewrote them.
    Returns per-step tokens to subtract from the miss (0 for step 0 and for non-append transitions)."""
    cr = [0]
    for i in range(1, len(S)):
        a, b = S[i - 1]["m"], S[i]["m"]
        if len(b) > len(a) and [m[2] for m in b[:len(a)]] == [m[2] for m in a]:
            cr.append(sum(m[1] for m, o in zip(b[len(a):], orig[i]["m"][len(a):]) if m[3] in ("thought", "args") and m[1] == o[1]))
        else: cr.append(0)
    return cr
REUSE_DECODED = True
def gpu2(S, policy="append", kvb=163_840, spec=None, cap=False, orig=None, **kw):
    per = []
    replay2(S, policy, hook=lambda i, s, h, t: per.append((h, t, s)), **kw)
    cr = decoded_credit(S, orig or S) if REUSE_DECODED else [0] * len(S)
    pre = dec = ctxp = 0.0
    for (h, t, s), c in zip(per, cr):
        n = max(0, t - h - c); h = t - n
        pre += (2 * 70e9 * n + ATT * n * (h + n / 2)) / PF; ctxp += ATT * n * h / PF
        passes = s[spec] if spec else [(0, 0)] * s["out"]
        C = t
        for k, a in passes:
            mem = (WB / B + kvb * C) / BW
            ftok = (2 * 70e9 + ATT * C) / PF
            if cap:   # truncate drafts to c tokens; a run of a accepted tokens then takes ceil((a+1)/(c+1)) passes
                c = max(0, min(k, int(mem / ftok) - 1))
                n_p = -(-(a + 1) // (c + 1)) if c < k else 1
                dec += n_p * max(mem, (c + 1) * ftok); ctxp += n_p * kvb * C / BW
            else:
                dec += max(mem, (k + 1) * ftok); ctxp += kvb * C / BW
            C += a + 1
    return pre, dec, ctxp
def gpu2agg(**kw):
    acc = [0.0] * 3
    for v in D2.values(): acc = [a + b for a, b in zip(acc, gpu2(v["steps"], **kw))]
    return acc
REUSE_DECODED = False   # round-6 accounting (decoded tokens re-prefilled), kept for comparison
pb6, db6, cb6 = gpu2agg(); _q6 = {kk: sum(gpu2agg(**kw)[:2]) / (pb6 + db6) for kk, kw in
       [("spec", dict(spec="pg", cap=True)), ("4bit", dict(kvb=81_920))]}
REUSE_DECODED = True
print(f"round-6 accounting (re-prefill own output): prefill {pb6/(pb6+db6):.0%}; capped speculation x{_q6['spec']:.3f}, 4-bit KV x{_q6['4bit']:.3f}")
print("round-7 accounting (runner reuses KV of its own decoded tokens; below):")
pb2, db2, cb2 = gpu2agg(); bb2 = pb2 + db2
print(f"baseline (prefix cache, FP8 KV, no speculation): prefill {pb2/bb2:.0%}, decode {db2/bb2:.0%}, "
      f"cached-context work {cb2/bb2:.0%}")
for name, kw in [("prompt-lookup speculation (exact)", dict(spec="pl")),
                 ("+ cross-session corpus (exact)", dict(spec="pg")),
                 ("+ draft capped to stay memory-bound (exact)", dict(spec="pg", cap=True)),
                 ("4-bit KV (approx)", dict(kvb=81_920)),
                 ("speculation + 4-bit KV (approx KV)", dict(spec="pg", cap=True, kvb=81_920)),
                 ("batched clear results keep 3 (content dropped)", dict(policy="clear", T=9)),
                 ("speculation + batched clear results keep 3", dict(spec="pk", cap=True, policy="clear", T=9)),
                 ("speculation + batched clear results+inputs keep 3", dict(spec="pk2", cap=True, policy="clear", T=9, kinds=("tool", "args"))),
                 ("speculation + splice results+inputs keep 3 + 4-bit", dict(spec="pk2", cap=True, policy="splice", kinds=("tool", "args"), kvb=81_920))]:
    p_, d_, c_ = gpu2agg(**kw)
    print(f"{name:<52} GPU time x{(p_+d_)/bb2:.3f} (prefill x{p_/pb2:.2f}, decode x{d_/db2:.2f})")
# sensitivity: concurrency B (weights amortised over B sequences; speculation's verify FLOPs grow with B)
for Bx in (8, 32, 128):
    Bsave = B
    globals()["B"] = Bx
    pa, da, _ = gpu2agg(); ps, ds, _ = gpu2agg(spec="pg"); pc, dc, _ = gpu2agg(spec="pg", cap=True)
    globals()["B"] = Bsave
    print(f"B={Bx:>3} concurrent sequences: speculation GPU time x{(ps+ds)/(pa+da):.3f}, capped x{(pc+dc)/(pa+da):.3f}")

# ---------------------------------------------------------------- R. round 7: reference, don't repeat (exact information)
section("R. Round 7: client rewrites repeated line runs (>= MINRUN lines, verbatim incl. line numbers) as references")
# traces/c4/dedup<MINRUN>.json from traces/c4/dedup.py: rewritten token count per message, applied once on arrival and
# persisted, so the history stays append-only. Scope 'all' = may reference anything earlier (no clearing); 'k3'/'k10' =
# only what stays visible when old results/inputs beyond the last 3/10 are cleared (lower bound under batching).
def with_sizes(dd, scope):
    out = {}
    for k, v in D2.items():
        st = []
        for s, r in zip(v["steps"], dd[k]):
            s2 = dict(s); s2["m"] = [[m[0], r[scope][j], m[2], m[3]] for j, m in enumerate(s["m"])]; st.append(s2)
        out[k] = {"steps": st, "cost": v["cost"]}
    return out
DD = {mr: json.load(open(os.path.join(HERE, "traces", "c4", f"dedup{mr}.json"))) for mr in (2, 4, 8)}
for mr in (2, 4, 8):
    Da = with_sizes(DD[mr], "all")
    fin = sum(sum(m[1] for m in v["steps"][-1]["m"]) for v in Da.values()); fin0 = sum(sum(m[1] for m in v["steps"][-1]["m"]) for v in D2.values())
    ra, wa, oa, ha, ta = agg2(D_=Da)
    print(f"MINRUN={mr}: final context -{1-fin/fin0:.1%}; keep everything, references only: bill x{(ra+wa+oa)/b2:.3f} (hit {ha/ta:.1%})")
Da = with_sizes(DD[4], "all")
for scope, kp, kd, name in [("k3", 3, ("tool", "args"), "clear results+inputs keep 3"),
                            ("k10", 10, ("tool", "args"), "clear results+inputs keep 10"),
                            ("k10", 10, ("tool",), "clear results keep 10")]:
    Dk = with_sizes(DD[4], scope)
    bt, v, _ = best("clear", kd, kp, D_=Dk)
    bt0, v0, _ = best("clear", kd, kp)
    print(f"references + batched {name:<30}: best T={bt:>2} x{v:.3f}   (without references x{v0:.3f})")
# runner: same rewrite shrinks prefill and the KV re-read by decode (drafts still see the earlier copy, so 'pg' kept)
for name, kw, D_ in [("references only (exact information)", dict(spec=None), Da),
                     ("speculation, capped (exact)", dict(spec="pg", cap=True), D2),
                     ("speculation + references (exact information)", dict(spec="pg", cap=True), Da),
                     ("speculation + references + 4-bit KV (approx KV)", dict(spec="pg", cap=True, kvb=81_920), Da)]:
    acc = [0.0] * 3
    for k, v in D_.items(): acc = [a + b for a, b in zip(acc, gpu2(v["steps"], orig=D2[k]["steps"], **kw))]
    print(f"{name:<52} GPU time x{(acc[0]+acc[1])/bb2:.3f} (prefill x{acc[0]/pb2:.2f}, decode x{acc[1]/db2:.2f})")

# ---------------------------------------------------------------- S. fair competitors at their best settings
section("S. Competitors at their best settings: provider context editing (full sweep) and an MTP-equipped runner")
# Anthropic clear_tool_uses: stateless (client keeps full history), fires when input > trigger, clears all tool results
# older than the last `keep`, skipped if fewer than clear_at_least tokens would be cleared. Sweep everything.
def ctx_edit(S, trigger, keep, kinds, cal):
    prev, reads, writes, outs = None, 0.0, 0.0, 0.0
    for s in S:
        msgs = s["m"]; old = set()
        for kd in kinds:
            idx = [j for j, m in enumerate(msgs) if m[3] == kd]
            old |= set(idx[:-keep] if len(idx) > keep else [])
        freed = sum(msgs[j][1] - min(20, msgs[j][1]) for j in old)
        cl = old if (TOOLS + sum(m[1] for m in msgs) > trigger and freed >= cal) else set()
        blocks = [("t", TOOLS)] + [(("X" if j in cl else "") + m[2], min(20, m[1]) if j in cl else m[1]) for j, m in enumerate(msgs)]
        tot = sum(b[1] for b in blocks); l = 0
        if prev:
            while l < min(len(prev), len(blocks)) and prev[l][0] == blocks[l][0]: l += 1
        hit = sum(b[1] for b in blocks[:l]) if prev else 0
        reads += R * hit; writes += W5 * (tot - hit); outs += OUT * s["out"]; prev = blocks
    return reads + writes + outs
grid = {}
for tr in (5_000, 10_000, 20_000, 30_000, 50_000, 100_000):
    for kp in (1, 3, 10):
        for kd in (("tool",), ("tool", "args")):
            for cal in (0, 5_000, 20_000, 40_000):
                grid[(tr, kp, kd, cal)] = sum(ctx_edit(v["steps"], tr, kp, kd, cal) for v in D2.values()) / b2
for kp in (1, 3, 10):
    for kd in (("tool",), ("tool", "args")):
        k_ = min((k for k in grid if k[1] == kp and k[2] == kd), key=grid.get)
        bt, v, _ = best("clear", kd, kp)
        print(f"keep {kp:>2} {'results+inputs' if len(kd) > 1 else 'results':<14}: provider best x{grid[k_]:.3f} "
              f"(trigger {k_[0]//1000}k, clear_at_least {k_[3]//1000}k)   client batched x{v:.3f} (T={bt})   ratio {v/grid[k_]:.3f}")
# MTP-equipped runner (DeepSeek-V3-style, 1 draft token accepted with p): the fair speculative baseline for models that
# ship MTP heads. Modelled, not replayed: acceptance p from the DeepSeek-V3 report (85-90%), independent per pass.
# Hybrid: n-gram/suffix draft where one exists (replayed), else the MTP token (modelled).
def gpu_mtp(S, p=0.85, hybrid=False, kvb=163_840, orig=None):
    per = []; replay2(S, hook=lambda i, s, h, t: per.append((h, t, s)))
    cr = decoded_credit(S, orig or S)
    pre = dec = 0.0
    for (h, t, s), c in zip(per, cr):
        n = max(0, t - h - c); h = t - n; pre += (2 * 70e9 * n + ATT * n * (h + n / 2)) / PF; C = t
        if hybrid:
            for k, a in s["pg"]:
                mem = (WB / B + kvb * C) / BW; ftok = (2 * 70e9 + ATT * C) / PF
                if k == 0: dec += max(mem, 2 * ftok) / (1 + p); C += 1   # an MTP pass emits 1+p tokens on average
                else:
                    c = max(0, min(k, int(mem / ftok) - 1)); n_p = -(-(a + 1) // (c + 1)) if c < k else 1
                    dec += n_p * max(mem, (c + 1) * ftok); C += a + 1
        else:
            j = 0
            while j < s["out"]:
                mem = (WB / B + kvb * C) / BW; ftok = (2 * 70e9 + ATT * C) / PF
                dec += max(mem, 2 * ftok) / (1 + p); C += 1; j += 1
    return pre, dec
for p in (0.75, 0.85, 0.90):
    m0 = [sum(x) for x in zip(*(gpu_mtp(v["steps"], p) for v in D2.values()))]
    m1 = [sum(x) for x in zip(*(gpu_mtp(v["steps"], p, hybrid=True) for v in D2.values()))]
    m2 = [sum(x) for x in zip(*(gpu_mtp(v["steps"], p, hybrid=True, orig=D2[k]["steps"]) for k, v in Da.items()))]
    print(f"MTP p={p:.2f}: MTP alone x{sum(m0)/bb2:.3f} of no-spec baseline; hybrid suffix+MTP x{sum(m1)/bb2:.3f} "
          f"(x{sum(m1)/sum(m0):.3f} of MTP alone); hybrid + references x{sum(m2)/bb2:.3f} (x{sum(m2)/sum(m0):.3f} of MTP alone)")
print("done")
