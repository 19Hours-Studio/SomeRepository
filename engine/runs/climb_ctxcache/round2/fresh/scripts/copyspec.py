# Lossless prompt-lookup speculative decoding on the real SWE-agent outputs.
# Every assistant message is re-decoded against its true continuation: at each verify pass the last
# 3 tokens are looked up in everything the model has seen (prompt + text generated so far); if found,
# the K tokens that followed the most recent occurrence are proposed; the pass accepts the matching
# prefix plus one token from the target model. Output is identical to normal decoding (greedy
# acceptance; with sampling, standard speculative rejection sampling keeps the distribution).
# Tokens: GPT-2 pre-tokenizer pieces as a proxy (no BPE vocabulary can be downloaded here). Usage: copyspec.py traces K
import json, sys, re
# GPT-2 pre-tokenizer pattern (BPE then splits rare words further, which makes copies longer, not shorter)
TOK = re.compile(r"'s|'t|'re|'ve|'m|'ll|'d| ?\w+| ?[^\s\w]+|\s+(?!\S)|\s+")
K = int(sys.argv[2]) if len(sys.argv) > 2 else 8
tot_out = passes = proposed = 0; per_msg = []
for line in open(sys.argv[1]):
    t = json.loads(line); ctx = []; idx = {}
    def add(tokens):
        for x in tokens:
            ctx.append(x)
            if len(ctx) >= 4: idx[tuple(ctx[-4:-1])] = len(ctx) - 1   # trigram -> position of the token that followed it
    for m in t["msgs"]:
        toks = TOK.findall(m["text"])
        if m["role"] == "assistant":
            i = 0; p = 0
            while i < len(toks):
                prop = []
                if len(ctx) >= 3:
                    j = idx.get(tuple(ctx[-3:]))
                    if j is not None: prop = ctx[j:j + K]
                acc = 0
                while acc < len(prop) and i + acc < len(toks) and prop[acc] == toks[i + acc]: acc += 1
                step = min(acc + 1, len(toks) - i)
                proposed += len(prop); add(toks[i:i + step]); i += step; p += 1
            tot_out += len(toks); passes += p; per_msg.append(len(toks) / max(1, p))
        else:
            add(toks)
per_msg.sort()
print(f"K={K}: assistant tokens {tot_out}, verify passes {passes}: {tot_out/passes:.2f} tokens per pass "
      f"(median message {per_msg[len(per_msg)//2]:.2f}, p90 {per_msg[9*len(per_msg)//10]:.2f}); proposed tokens per output token {proposed/tot_out:.2f}")
