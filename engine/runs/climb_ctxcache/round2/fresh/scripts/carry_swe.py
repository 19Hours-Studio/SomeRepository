# Output-KV carry-over on the 200 SWE-agent traces (append-only, as the agent actually ran).
# Today the assistant message of turn j is new input at turn j+1 (cache write, 1.25x on Anthropic,
# 1.0x on OpenAI). If the server keeps the KV it produced while decoding that message, the
# next request hits it (billed as a read, 0.1x). The tool output that follows stays a write.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r1_traces as T
tr = T.load(sys.argv[1])
for name, (W, R) in T.PRICES.items():
    base = carry = hit0 = hit1 = tot = out = 0
    for t in tr:
        ntok = [T.tok(x) for x in t["text"]]; A = T.requests(t); prev = None
        for a in A:
            L = T.TOOLS + sum(ntok[:a])
            if prev is None: c0 = 0; c1 = 0
            else:
                c0 = T.TOOLS + sum(ntok[:prev])                   # exact prefix = previous prompt
                c1 = c0 + ntok[prev]                               # + the assistant message it produced
            base += R * c0 + W * (L - c0); carry += R * c1 + W * (L - c1)
            hit0 += c0; hit1 += c1; tot += L; out += ntok[a]; prev = a
    o = T.OUT_PRICE * out
    print(f"{name:9s} append-only input {base/1e6:6.1f}M  with carry-over {carry/1e6:6.1f}M ({carry/base-1:+.1%})  "
          f"whole bill {(carry+o)/(base+o)-1:+.1%}  token hit {hit0/tot:.1%} -> {hit1/tot:.1%}")
