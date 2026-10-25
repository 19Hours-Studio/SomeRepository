"""Round 8: replay vLLM's own suffix-decoding drafter -- the official Arctic Inference SuffixDecodingCache that vLLM's
`method: suffix` imports -- on the 42 sessions, at a sweep of its settings. Exact for a deterministic draft (see
extract2.py). Linear drafts (use_tree_spec=False), as vLLM v1 verifies a single path.

usage: python3 -I spec8b.py ARCTIC_SRC_DIR RAW_TRAJ_DIR TOKENIZER_JSON OUT_JSON [SHARD NSHARDS]
  SHARD/NSHARDS   run every NSHARDS-th config (configs are independent); merge the outputs with merge8b.py
  ARCTIC_SRC_DIR  arctic_inference-0.3.0 sdist (PyPI) with csrc/suffix_decoding built (cmake + nanobind) and _C*.so
                  copied into arctic_inference/suffix_decoding/
Needs numpy, tokenizers.
"""
import ast, glob, hashlib, json, os, sys
asrc, src, tokf, dst = sys.argv[1:5]
sys.path.insert(0, asrc)
import numpy as np
from tokenizers import Tokenizer
from arctic_inference.suffix_decoding import SuffixDecodingCache

tok = Tokenizer.from_file(tokf)
_c = {}
def ids(s):
    h = hashlib.sha1(s.encode()).hexdigest()
    if h not in _c: _c[h] = tok.encode(s, add_special_tokens=False).ids
    return _c[h]
def content_text(c):
    if isinstance(c, list): return "".join(x.get("text", "") for x in c if isinstance(x, dict))
    if isinstance(c, str) and c.startswith("[{"):
        try: return content_text(ast.literal_eval(c))
        except Exception: return c
    return c if isinstance(c, str) else ""
def parts(m):
    role = m.get("role", "none"); txt = content_text(m.get("content"))
    if role != "assistant": return [(role, txt)]
    out = [("thought", txt)]; tc = m.get("tool_calls")
    if isinstance(tc, str):
        try: tc = ast.literal_eval(tc)
        except Exception: tc = None
    for c in tc or []:
        f = c.get("function", {}); out.append(("args", f.get("name", "") + " " + (f.get("arguments") or "")))
    return out

# (max_spec_factor, min_token_prob, num_speculative_tokens); vLLM defaults: 1.0, 0.1, max_tree_depth (24)
CFG = {f"sx_a{a:g}_p{int(p*100)}_k{k}": (a, p, k) for a in (1.0, 2.0, 4.0) for p in (0.1,) for k in (4, 8, 24)}
CFG.update({"sx_a1_p30_k24": (1.0, 0.3, 24), "sx_a4_p30_k8": (4.0, 0.3, 8)})
if len(sys.argv) > 6:
    sh, ns = int(sys.argv[5]), int(sys.argv[6])
    CFG = {k: v for j, (k, v) in enumerate(CFG.items()) if j % ns == sh}
caches = {k: SuffixDecodingCache(max_tree_depth=24, max_cached_requests=10_000) for k in CFG}
def run(cache, rid, prompt, out, a, p, k):
    cache.start_request(rid, prompt)
    resp, passes = [], []
    while len(resp) < len(out):
        seq = np.concatenate([prompt, np.array(resp, dtype=np.int32)]) if resp else prompt
        r = cache.speculate(rid, seq, max_spec_tokens=k, max_spec_factor=a, min_token_prob=p, use_tree_spec=False)
        d = list(r.token_ids); acc = 0
        while acc < len(d) and len(resp) + acc < len(out) and d[acc] == out[len(resp) + acc]: acc += 1
        new = out[len(resp):len(resp) + acc + 1]
        passes.append((len(d), acc)); resp.extend(new); cache.add_active_response(rid, new)
    cache.stop_request(rid)
    return passes

res, rid = {}, 0
for f in sorted(glob.glob(os.path.join(src, "*.traj"))):
    d = json.load(open(f)); T = d["trajectory"]; steps = []
    for i, st in enumerate(T):
        q = st["query"]
        if i + 1 < len(T) and len(T[i + 1]["query"]) > len(q):
            nxt = [m for m in T[i + 1]["query"][len(q):] if m.get("role") == "assistant"]
            otext = "".join(t for m in nxt[:1] for _, t in parts(m))
        else: otext = st.get("response") or ""
        out = ids(otext)
        prompt = np.array([x for m in q for _, t in parts(m) for x in ids(t)], dtype=np.int32)
        rec = {"out": len(out)}
        if out:
            for k, (a, p, ns) in CFG.items(): rec[k] = run(caches[k], rid, prompt, out, a, p, ns)
        else:
            for k in CFG: rec[k] = []
        rid += 1; steps.append(rec)
    res[os.path.basename(f)[:-5]] = steps
    print(os.path.basename(f), len(T), file=sys.stderr, flush=True)
json.dump(res, open(dst, "w"))
Tt = sum(s["out"] for v in res.values() for s in v)
for k in CFG:
    P = sum(len(s[k]) for v in res.values() for s in v); K = sum(p[0] for v in res.values() for s in v for p in s[k])
    print(f"{k}: tokens/pass {Tt/P:.2f}, mean draft {K/P:.2f}")
