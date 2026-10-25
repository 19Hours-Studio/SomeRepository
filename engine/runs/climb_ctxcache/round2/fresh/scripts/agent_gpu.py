# Where an own-stack operator's GPU time goes when serving the 200 SWE-agent sessions append-only
# with exact prefix caching (hit = previous prompt). Per request: prefill of new tokens (linear +
# attention over the cached context), decode (weights shared over a batch of 32, plus each step
# reading the whole cached KV), and HBM residency of the cached KV while the tool runs (measured
# execution_time from the trajectories). H100: 989 TFLOP/s x 45%, 3.35 TB/s x 70%, $2/h, 80 GB.
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r1_traces as T
FL = 0.45 * 989e12; BW = 0.7 * 3.35e12; HBM_S = 1 / 80e9          # GPU-seconds per byte-second of HBM held
BATCH = 32
# name: (KV bytes/token, linear FLOPs/token, attention FLOPs per query-key pair, weight bytes read per decode step)
M = {"dense 72B GQA, BF16 KV": (327680, 144e9, 4 * 80 * 64 * 128, 144e9),
     "dense 72B GQA, FP8 KV":  (163840, 144e9, 4 * 80 * 64 * 128, 144e9),
     "MoE 671B-A37B MLA (DeepSeek-V3), FP8 KV": (70272, 74e9, 2 * 61 * 128 * 320, 37e9),
     "MoE 30B-A3B GQA, BF16 KV": (98304, 6.6e9, 4 * 48 * 32 * 128, 6.6e9 * 2)}
def main():
  tr = T.load(sys.argv[1]); ex = {json.loads(l)["id"]: json.loads(l)["exec_s"] for l in open(sys.argv[2])}
  for name, (kvb, lin, att, wb) in M.items():
      c = dict(prefill_lin=0.0, prefill_att=0.0, dec_w=0.0, dec_kv=0.0, idle=0.0, miss_full=0.0)
      for t in tr:
          ntok = [T.tok(x) for x in t["text"]]; A = T.requests(t); es = ex[t["id"]]; prev = None
          for j, a in enumerate(A):
              L = T.TOOLS + sum(ntok[:a]); c0 = T.TOOLS + sum(ntok[:prev]) if prev is not None else 0
              new = L - c0; o = ntok[a]
              c["prefill_lin"] += new * lin / FL
              c["prefill_att"] += new * (c0 + new / 2) * att / FL
              c["dec_w"] += o * wb / BATCH / BW
              c["dec_kv"] += o * (L + o / 2) * kvb / BW
              if j < len(es) and es[j]: c["idle"] += L * kvb * es[j] * HBM_S        # KV parked in HBM while the tool runs
              c["miss_full"] += L * lin / FL + L * L / 2 * att / FL                 # same request with no cache
              prev = a
      tot = sum(v for k, v in c.items() if k != "miss_full")
      print(f"{name}: GPU-hours {tot/3600:.1f} with prefix caching (vs {(tot - c['prefill_lin'] - c['prefill_att'] + c['miss_full'])/3600:.1f} with none)")
      print("   " + "  ".join(f"{k} {v/tot:5.1%}" for k, v in c.items() if k != "miss_full"))

if __name__ == "__main__": main()
