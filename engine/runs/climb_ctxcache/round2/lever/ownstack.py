# Own-stack cost of each context policy on the same 200 real traces, in GPU time instead of API
# price multipliers (check1 item 5). Model: Llama-3-70B shape (80 layers, q dim 8192, GQA 8x128 KV,
# BF16 KV = 320 KB/token), one H100 (989 TFLOPS dense BF16 at 45% MFU, 3.35 TB/s HBM),
# decode batch 32 (weights 140 GB amortised over the batch). Per request:
#   prefill: recomputed tokens n = L - cached;  FLOPs = 2P*n + 4*layers*qdim*(L^2 - c^2)/2
#   decode : o output tokens, each max(FLOPs/peak, (weights/batch + L*KVB)/BW)
#   splice : recompute placeholder (+k boundary tokens); re-rotate downstream keys (read+write K, memory-bound)
# Usage: python3 -I ownstack.py data/traces.jsonl
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import traces as T

def horizon_seq(tr, ntok, W, R):  # same online rule as rule.py (rule.py runs on import, so it is copied here)
    A = T.requests(tr); seq = []; el = set()
    for j, a in enumerate(A):
        elig = T.old_obs(tr, a) - el
        if elig:
            S = sum(ntok[i] for i in elig); f = min(elig)
            X = sum(ntok[i] for i in range(f, a) if i not in elig) + T.PH * len(elig)
            if R * S * max(j, 1) >= (W - R) * X: el |= elig
        seq.append(T.ctx(tr, ntok, a, el))
    return seq

P = 70e9; NL = 80; QD = 8192; KVB = 320 * 1024; KB = KVB / 2
PEAK = 989e12 * 0.45; BW = 3.35e12; WB = 140e9; BATCH = int(os.environ.get("BATCH", 32))
W, R = T.PRICES["anthropic"]

def gpu_time(seq, outs, splice_k=None, refresh=0):
    pre = dec = rot = 0.0; prev = []; prevkeys = set(); ctxsum = 0; nsp = 0; reused = 0
    for s, o in zip(seq, outs):
        L = sum(t for _, t in s)
        if splice_k is None:
            c = T.lcp(prev, s)
        else:  # splice: everything already in the cache (same key) is reused; only new keys are computed
            n = sum(t for key, t in s if key not in prevkeys)
            for j, (key, t) in enumerate(s):               # downstream of each new placeholder: rotate keys, repair k
                if key not in prevkeys and isinstance(key, tuple) and key[0] == "ph":
                    down = sum(t2 for k2, t2 in s[j + 1:] if k2 in prevkeys)
                    rot += 2 * down * KB / BW; n += min(splice_k, down); nsp += 1
                    if refresh and nsp % refresh == 0: n = L   # periodic exact refresh
            c = L - min(n, L)
        x = L - c; reused += c
        pre += (2 * P * x + 4 * NL * QD * (L * L - c * c) / 2) / PEAK
        dec += o * max((2 * P + 4 * NL * QD * L) / PEAK, (WB / BATCH + L * KVB) / BW)
        prev = s; prevkeys = {k for k, _ in s}; ctxsum += L
    return pre, dec, rot, ctxsum / len(seq), reused, ctxsum

def main(path):
    tot = {}
    for tr in T.load(path):
        ntok = [T.tok(s) for s in tr["text"]]; A = T.requests(tr); outs = [ntok[a] for a in A]
        pols = {"append": (T.policy_seq(tr, ntok, "append", W, R), None, 0),
                "sliding (exact rewrite)": (T.policy_seq(tr, ntok, "sliding", W, R), None, 0),
                "batch5k (exact)": (T.policy_seq(tr, ntok, "batch", W, R, 5000), None, 0),
                "horizon (exact)": (horizon_seq(tr, ntok, W, R), None, 0),
                "sliding + splice": (T.policy_seq(tr, ntok, "sliding", W, R), 0, 0),
                "sliding + splice + k=128 repair": (T.policy_seq(tr, ntok, "sliding", W, R), 128, 0),
                "sliding + splice, refresh every 4": (T.policy_seq(tr, ntok, "sliding", W, R), 0, 4)}
        for k, (seq, sk, rf) in pols.items():
            r = gpu_time(seq, outs, sk, rf)
            tot[k] = [a + b for a, b in zip(tot.get(k, [0] * 6), r)]
    b = sum(tot["append"][:3])
    print(f"{'policy':36s} {'prefill h':>9s} {'decode h':>9s} {'rotate h':>9s} {'total h':>8s} {'vs append':>9s}  mean ctx  token reuse")
    for k, (p, d, r, cx, ru, cs) in tot.items():
        t = p + d + r
        print(f"{k:36s} {p/3600:9.3f} {d/3600:9.3f} {r/3600:9.4f} {t/3600:8.3f} {t/b-1:+9.1%}  {cx/200:8,.0f}  {ru/cs:.3f}")

if __name__ == "__main__":
    main(sys.argv[1])
