"""Replay Mooncake FAST25 traces (512-token blocks, prefix semantics) and compare
leaf-only LRU vs value-density eviction (expected reuse x recompute-FLOPs / bytes).
Usage: python3 -I sim_evict.py TRACE.jsonl
Cost models (exact config arithmetic):
  llama8b : dense GQA, 2N=16e9 FLOP/tok linear, attn 4*32*4096*p, 64 KiB/tok (FP8)
  dsv3    : MLA, 2N=74e9 (37B active), absorbed attn ~2*128*(576+512)*61*p, 70,272 B/tok (BF16 latent)
"""
import json, sys, heapq, math

BLK = 512
MODELS = {
    "llama8b": dict(lin=16e9, att=4 * 32 * 4096, bpt=65536),
    "dsv3": dict(lin=74e9, att=2 * 128 * (576 + 512) * 61, bpt=70272),
}

def block_flops(m, j):
    # FLOPs to recompute block j (tokens j*512 .. j*512+511) given prefix cached
    p0 = j * BLK
    s = BLK * p0 + BLK * (BLK - 1) / 2
    return BLK * m["lin"] + m["att"] * s

def run(reqs, cap_blocks, policy, m, half_life_s=600.0):
    if policy == "gdsf":
        half_life_s = 1e18
    # cache: hash -> node(parent, nchild, last, freq, j)
    cache = {}
    heap = []  # (score, version, hash) for leaves
    ver = {}
    tot = saved = 0.0
    hits = nblk = 0
    lam = math.log(2) / half_life_s
    clock = [0.0]
    cnorm = block_flops(m, 0)

    def score(h, now):
        n = cache[h]
        if policy == "lru":
            return n["last"]
        # value density with time decay: freq decayed to now; use log-space trick:
        # score ~ (freq * exp(-lam*(now-last))) * cost/bytes ; compare at eviction
        # time-invariant key: log(freq*cost) + lam*last  (monotone equivalent)
        if policy == "gdsf":
            return clock[0] + n["freq"] * n["cost"] / cnorm
        c = n["cost"] if policy == "flop" else 1.0
        return math.log(n["freq"] * c) + lam * n["last"]

    def push(h, now):
        v = ver.get(h, 0) + 1
        ver[h] = v
        heapq.heappush(heap, (score(h, now), v, h))

    for r in reqs:
        now = r["timestamp"] / 1000.0
        hs = r["hash_ids"]
        k = 0
        while k < len(hs) and hs[k] in cache:
            k += 1
        for j, h in enumerate(hs):
            c = block_flops(m, j)
            tot += c
            if j < k:
                saved += c
                hits += 1
        nblk += len(hs)
        # insert / touch
        parent = None
        for j, h in enumerate(hs):
            if h in cache:
                n = cache[h]
                # decay freq then add 1
                n["freq"] = n["freq"] * math.exp(-lam * (now - n["last"])) + 1
                n["last"] = now
            else:
                cache[h] = dict(parent=parent, nchild=0, last=now, freq=1.0,
                                cost=block_flops(m, j))
                if parent is not None:
                    cache[parent]["nchild"] += 1
            if cache[h]["nchild"] == 0:
                push(h, now)
            parent = h
        # evict leaves until within capacity
        cur = set(hs)
        skipped = []
        while len(cache) > cap_blocks and heap:
            s, v, h = heapq.heappop(heap)
            if h not in cache or ver.get(h) != v or cache[h]["nchild"] > 0:
                continue
            if h in cur:  # don't evict blocks of the current request; keep for later
                skipped.append((s, v, h))
                continue
            if policy == "gdsf":
                clock[0] = s
            p = cache[h]["parent"]
            del cache[h]
            if p is not None and p in cache:
                cache[p]["nchild"] -= 1
                if cache[p]["nchild"] == 0:
                    push(p, now)
        for e in skipped:
            heapq.heappush(heap, e)
        assert len(cache) <= max(cap_blocks, len(hs)) + 0 or not heap
    return saved / tot, hits / nblk

if __name__ == "__main__":
    reqs = [json.loads(l) for l in open(sys.argv[1])]
    for mname in sys.argv[2:] or ["llama8b", "dsv3"]:
        m = MODELS[mname]
        print(f"# {sys.argv[1].split('/')[-1]} model={mname}  (FLOP-saved fraction; gain vs LRU)")
        print("cap_Mtok   LRU   | flop_hl60  flop_hl180  flop_hl600 | GDSF(anchor+aging)")
        for cap in [500, 1000, 2000, 5000, 10000, 20000, 50000]:
            fl, _ = run(reqs, cap, "lru", m)
            out = []
            for pol, hl in [("flop", 60), ("flop", 180), ("flop", 600), ("gdsf", 0)]:
                f, _ = run(reqs, cap, pol, m, hl)
                out.append(f"{f:.3f}({f/fl-1:+.0%})")
            print(f"{cap*BLK/1e6:6.2f}  {fl:.3f} | " + "  ".join(out))
