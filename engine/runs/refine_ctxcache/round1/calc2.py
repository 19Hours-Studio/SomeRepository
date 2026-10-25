"""Arithmetic and synthetic replays for the refined context-caching answer.
Prices are Anthropic multipliers of base input: write5m=1.25, write1h=2.0, read=0.1.
Run: python3 calc2.py
"""
import random, math, hashlib, itertools
from collections import defaultdict

W5, W1H, R = 1.25, 2.0, 0.1
random.seed(0)

print("== A. errata vs rewrite break-even (extra cost only) ==")
# rewrite: suffix S=N-p re-written at W instead of read at R  -> extra (W-R)*S once
# erratum: e new tokens written once (W*e) then read every later turn (R*e per turn)
for S, e in [(50_000, 500), (10_000, 2_000), (2_000, 2_000)]:
    T = ((W5 - R) * S - W5 * e) / (R * e)
    print(f"suffix={S:>6} e={e:>5}: break-even after {T:8.1f} turns")

print("\n== B. agent bill decomposition at 100% hit ==")
def agent_bill(turns=50, sys=10_000, step=2_000, out=300, out_price=5.0):
    reads = writes = 0
    ctx = sys
    writes += sys
    for t in range(turns):
        reads += ctx            # whole prior context read from cache
        new = step + out        # tool output + model's own output appended
        writes += new
        ctx += new
    inp = R * reads + W5 * writes
    outp = out_price * out * turns
    return R * reads, W5 * writes, outp
r, w, o = agent_bill()
tot = r + w + o
print(f"read {r/1e3:.0f}k ({r/tot:.0%})  write {w/1e3:.0f}k ({w/tot:.0%})  output {o/1e3:.0f}k ({o/tot:.0%})  [units of base-input token price]")
r2, w2, o2 = agent_bill(sys=10_000, step=2_000)
# same agent but tool results older than 10 turns hole-punched/compacted to 200 tokens
def agent_bill_compact(turns=50, sys=10_000, step=2_000, out=300, keep=10, stub=200):
    reads = 0; writes = sys
    hist = []
    for t in range(turns):
        ctx = sys + sum(hist)
        reads += ctx
        hist.append(step + out); writes += step + out
        if len(hist) > keep:
            i = len(hist) - keep - 1
            if hist[i] > stub + out:
                hist[i] = stub + out   # deletion served as cache hit (Idea 3) -> no rewrite
    return R * reads, W5 * writes
rc, wc = agent_bill_compact()
print(f"with in-place hole-punch of old tool results: read {rc/1e3:.0f}k vs {r/1e3:.0f}k -> input bill {(rc+wc)/(r+w):.2f}x")

print("\n== C. volatility-sorted layout (Smith's rule) ==")
# blocks with size s_i and per-request change prob lam_i; a change in block i
# forces recompute of every token from block i onward.
def expected_recompute(order, blocks):
    tot = 0.0
    sizes = [blocks[i][0] for i in order]
    suffix = list(itertools.accumulate(sizes[::-1]))[::-1]
    for k, i in enumerate(order):
        tot += blocks[i][1] * suffix[k]
    return tot
def sim_layout(n_blocks=12, trials=200):
    ratios = []
    hit_typ, hit_opt = [], []
    for _ in range(trials):
        blocks = [(random.choice([500, 2000, 8000, 20000]), random.choice([0.0, 0.01, 0.05, 0.2, 0.5])) for _ in range(n_blocks)]
        N = sum(b[0] for b in blocks)
        typical = list(range(n_blocks))              # authoring order (random wrt volatility)
        smith = sorted(range(n_blocks), key=lambda i: blocks[i][1] / blocks[i][0])
        a, b = expected_recompute(typical, blocks), expected_recompute(smith, blocks)
        # expected prob. block i changes -> recompute upper bounded by N; hit ~ 1 - recompute/N (approx for small lam)
        hit_typ.append(1 - min(a, N) / N); hit_opt.append(1 - min(b, N) / N)
        ratios.append(a / b if b else float('inf'))
    ratios.sort()
    print(f"median recompute reduction {ratios[len(ratios)//2]:.1f}x, p10 {ratios[len(ratios)//10]:.1f}x;"
          f" mean token hit {sum(hit_typ)/trials:.1%} -> {sum(hit_opt)/trials:.1%}")
sim_layout()

print("\n== D. RAG: per-query doc sets, order policy vs radix-tree hit rate ==")
def rag_sim(D=2000, k=5, Q=20000, doc_len=600, sys=2000, zipf=1.0, cap_docs=None):
    w = [1 / (i + 1) ** zipf for i in range(D)]
    pop_rank = {i: i for i in range(D)}  # doc 0 most popular (rank known from logs)
    def hsh(i): return hashlib.md5(str(i).encode()).hexdigest()
    res = {}
    for policy in ["relevance", "hash", "popularity"]:
        trie = set(); hit = tot = 0
        rnd = random.Random(1)
        for q in range(Q):
            docs = set()
            while len(docs) < k:
                docs.add(rnd.choices(range(D), weights=w)[0])
            docs = list(docs)
            if policy == "relevance": rnd.shuffle(docs)
            elif policy == "hash": docs.sort(key=hsh)
            else: docs.sort(key=lambda i: pop_rank[i])
            hit += sys; tot += sys  # shared system prompt
            path = ()
            matched = True
            for d in docs:
                path = path + (d,)
                tot += doc_len
                if matched and path in trie: hit += doc_len
                else: matched = False
                trie.add(path)
            tot += 50  # query
        res[policy] = hit / tot
    return res
for z in [0.8, 1.0, 1.2]:
    r_ = rag_sim(zipf=z)
    print(f"zipf={z}: " + "  ".join(f"{p}={v:.1%}" for p, v in r_.items()))
print("(segment cache upper bound = every repeated doc served: see E)")
def seg_bound(D=2000, k=5, Q=20000, zipf=1.0):
    w = [1 / (i + 1) ** zipf for i in range(D)]
    seen = set(); hit = tot = 0; rnd = random.Random(1)
    for q in range(Q):
        docs = set()
        while len(docs) < k: docs.add(rnd.choices(range(D), weights=w)[0])
        for d in docs:
            tot += 1; hit += d in seen; seen.add(d)
    return hit / tot
print(f"fraction of doc occurrences already seen (segment-cache ceiling, zipf=1): {seg_bound():.1%}")

print("\n== E. tier bandwidth vs recompute (Llama-3-70B, GQA) ==")
kv_bf16 = 80 * 8 * 128 * 2 * 2   # bytes/token
flop_tok = 2 * 70e9
for ctx in [8_000, 32_000, 128_000]:
    attn = 4 * 80 * 8192 * ctx / 2   # avg causal attention FLOPs/token (QK^T + AV)
    f = flop_tok + attn
    gpu8 = 8 * 989e12 * 0.45
    rec = gpu8 / f
    print(f"ctx {ctx:>6}: recompute on 8xH100 @45% = {rec/1e3:6.1f}k tok/s;"
          f" load BF16 KV: 1 NVMe(7GB/s) {7e9/kv_bf16/1e3:5.1f}k, 4 NVMe {28e9/kv_bf16/1e3:5.1f}k,"
          f" PCIe5 x8 GPUs(8x50GB/s) {400e9/kv_bf16/1e3:6.0f}k, 400Gb RDMA {50e9/kv_bf16/1e3:5.1f}k tok/s")
print(f"KV bytes/token: 70B BF16 {kv_bf16/1024:.0f} KB, FP8 {kv_bf16/2048:.0f} KB; DeepSeek-V3 MLA (576*61*2B) {576*61*2/1024:.0f} KB")

print("\n== F. storage-vs-recompute break-even reuse interval (70B BF16, 1M tokens) ==")
gb = kv_bf16 * 1e6 / 1e9
rec_cost = flop_tok * 1e6 / (989e12 * 0.45) / 3600 * 2.0
for tier, usd_gbh in [("HBM", 2.0 / 80), ("DRAM", 0.005), ("NVMe", 0.00022)]:
    hold = gb * usd_gbh
    print(f"{tier:4}: hold ${hold:6.3f}/h vs recompute ${rec_cost:.3f}/1M tok -> worth keeping if reused every < {rec_cost/hold*60:7.1f} min")

print("\n== G. Anthropic TTL choice for a context reused every g minutes ==")
for g in [3, 6, 20, 45, 90]:
    c5 = W5 if g > 5 else R      # 5m cache: expired -> re-write at 1.25
    c1 = R if g <= 60 else W1H   # 1h cache: hit at 0.1 (initial 2.0 write amortized)
    print(f"gap {g:>3} min: per-reuse cost 5m-TTL {c5:.2f}x, 1h-TTL {c1:.2f}x")
