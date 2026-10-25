"""Second pass over the same 42 SWE-agent .traj files (full text), producing traces/c4/steps2.json.

usage: python3 -I extract2.py RAW_TRAJ_DIR TOKENIZER_JSON OUT_JSON [KMAX NMAX NMIN]
  RAW_TRAJ_DIR    the 42 .traj files listed in pick.txt (s3://swe-bench-submissions/<key>)
  TOKENIZER_JSON  anthropic/tokenizer.json from the anthropic==0.30.0 wheel (legacy Claude tokenizer; a proxy
                  for the current Claude tokenizer, which is not public)

Per step it stores the request as messages [role, tokens, hash, kind] (kind: tool results split off from
assistant thought text and tool-call arguments), the generated output's token ids are replayed against the
request's token stream for speculative decoding (prompt lookup / suffix-tree style drafts), and the per-pass
draft outcome is stored, so calc.py needs no tokenizer and no raw data.
Also stores SWE-agent's own logged instance_cost for a check of the bill model.
"""
import ast, glob, hashlib, json, os, sys
from tokenizers import Tokenizer

src, tokf, dst = sys.argv[1:4]
tok = Tokenizer.from_file(tokf)
_cache = {}
def ids(s):
    h = hashlib.sha1(s.encode()).hexdigest()
    if h not in _cache: _cache[h] = tok.encode(s, add_special_tokens=False).ids
    return _cache[h]

def content_text(c):
    if isinstance(c, list): return "".join(x.get("text", "") for x in c if isinstance(x, dict))
    if isinstance(c, str) and c.startswith("[{"):
        try: return content_text(ast.literal_eval(c))
        except Exception: return c
    return c if isinstance(c, str) else ""

def parts(m):
    """-> list of (kind, text). Assistant messages: thought text, then tool-call name+arguments."""
    role = m.get("role", "none")
    txt = content_text(m.get("content"))
    if role != "assistant": return [(role, txt)]
    out = [("thought", txt)]
    tc = m.get("tool_calls")
    if isinstance(tc, str):
        try: tc = ast.literal_eval(tc)
        except Exception: tc = None
    for c in tc or []:
        f = c.get("function", {})
        out.append(("args", f.get("name", "") + " " + (f.get("arguments") or "")))
    return out

KMAX, NMAX, NMIN = (int(x) for x in (sys.argv[4:7] or (8, 4, 1)))  # draft <= KMAX tokens; longest suffix n-gram NMAX..NMIN
class Index:
    """n-gram -> most recent end position in a growing token stream (prompt-lookup decoding)."""
    def __init__(self): self.s, self.d = [], {}
    def extend(self, xs):
        for x in xs:
            self.s.append(x); L = len(self.s)
            for n in range(NMIN, NMAX + 1):
                if L >= n: self.d[tuple(self.s[L - n:])] = L
    def draft(self, tail):
        for n in range(min(NMAX, len(tail)), NMIN - 1, -1):
            p = self.d.get(tuple(tail[-n:]))
            if p is not None and p < len(self.s): return self.s[p:p + KMAX]
        return []

def spec(index, out, glob_index=None):
    """Replay realized output tokens. With a deterministic draft, 'sample y ~ p, accept iff y == draft' is exactly
    standard speculative sampling, so the realized outputs give the accepted-length distribution without a model.
    Returns list of (proposed k, accepted a) per verification pass (each pass emits a + 1 tokens)."""
    passes, j, gen, loc = [], 0, [], Index()
    while j < len(out):
        tail = (index.s[-NMAX:] + gen)[-NMAX:] if len(gen) < NMAX else gen[-NMAX:]
        # stream = prompt + generated so far; search the generated part first (most recent), then the prompt
        d = loc.draft(tail) or index.draft(tail)
        if not d and glob_index is not None: d = glob_index.draft(tail)
        a = 0
        while a < len(d) and j + a < len(out) and d[a] == out[j + a]: a += 1
        passes.append((len(d), a))
        gen.extend(out[j:j + a + 1]); loc.extend(out[j:j + a + 1]); j += a + 1
    return passes

res = {}
glob_out = Index()   # outputs of earlier sessions (suffix-decoding-style cross-request corpus), sessions in key order
for f in sorted(glob.glob(os.path.join(src, "*.traj"))):
    d = json.load(open(f))
    T = d["trajectory"]
    steps, index, prev_q, outs_s = [], None, None, []
    for i, st in enumerate(T):
        q = st["query"]
        msgs = []
        for m in q:
            for kind, t in parts(m):
                msgs.append([m.get("role", "none"), len(ids(t)), hashlib.sha1((kind + t).encode()).hexdigest()[:12], kind])
        # output = the assistant message appended in the next query (thought + tool call); last step: response text
        if i + 1 < len(T) and len(T[i + 1]["query"]) > len(q):
            nxt = [m for m in T[i + 1]["query"][len(q):] if m.get("role") == "assistant"]
            otext = "".join(t for m in nxt[:1] for _, t in parts(m))
        else:
            otext = st.get("response") or ""
        out = ids(otext)
        # rebuild the prompt-lookup index over the request's token stream (incrementally when append-only)
        qtexts = [t for m in q for _, t in parts(m)]
        if prev_q is not None and qtexts[:len(prev_q)] == prev_q:
            for t in qtexts[len(prev_q):]: index.extend(ids(t))
        else:
            index = Index()
            for t in qtexts: index.extend(ids(t))
        prev_q = qtexts
        p_local = spec(index, out)
        p_glob = spec(index, out, glob_out)
        # drafts when the server only sees a cleared prompt: results (pk) or results + tool inputs (pk2) older than
        # the last 3 are gone from the lookup stream (lower bound for batched clearing, which keeps 3..3+T)
        pc = {}
        for key, kinds in (("pk", ("tool",)), ("pk2", ("tool", "args"))):
            flat = [(kind, t) for m in q for kind, t in parts(m)]
            drop = set()
            for kd in kinds:
                ix = [j for j, (kind, _) in enumerate(flat) if kind == kd]
                drop |= set(ix[:-3])
            ci = Index()
            for j, (_, t) in enumerate(flat):
                if j not in drop: ci.extend(ids(t))
            pc[key] = spec(ci, out, glob_out)
        steps.append({"m": msgs, "out": len(out), "pl": p_local, "pg": p_glob, **pc})
        outs_s.append(out)
    for o in outs_s:   # add this session's outputs to the cross-session corpus only after the session
        glob_out.extend(o)
    name = os.path.basename(f)[:-5]
    ms = d.get("info", {}).get("model_stats", {})
    res[name] = {"steps": steps, "cost": ms.get("instance_cost"), "calls": ms.get("api_calls")}
    pass
json.dump(res, open(dst, "w"))
T_ = sum(s["out"] for v in res.values() for s in v["steps"])
for key in ("pl", "pg", "pk", "pk2"):
    P_ = sum(len(s[key]) for v in res.values() for s in v["steps"]); K_ = sum(p[0] for v in res.values() for s in v["steps"] for p in s[key])
    print(f"KMAX={KMAX} NMAX={NMAX} NMIN={NMIN} {key}: tokens/pass {T_/P_:.2f}, mean draft {K_/P_:.2f}")
