"""Round 8: replay vLLM's own suffix-decoding drafter (Arctic Inference / SuffixDecoding rule) on the 42 sessions,
so the speculative baseline is the strongest model-free drafter that ships in vLLM, at a sweep of its settings.

usage: python3 -I spec8.py RAW_TRAJ_DIR TOKENIZER_JSON OUT_JSON

Drafter (single path, as vLLM v1 proposes linear drafts):
  * two corpora: the current request's prompt (+ tokens generated so far), and a global corpus of all earlier
    outputs (earlier steps of this session and earlier sessions; vLLM keeps up to 10,000 cached requests);
  * find the longest suffix of (prompt + generated) of length p <= depth that occurs in a corpus;
  * extend greedily with the most frequent next token among the matching occurrences, multiplying the empirical
    conditional frequencies into a path probability; stop when it falls below min_prob, or at min(alpha*p, depth-p,
    num_spec) tokens (vLLM: max_spec_factor alpha, max_tree_depth, num_speculative_tokens);
  * take the corpus whose path has the higher score (sum of path probabilities = expected accepted tokens).
Each verification pass is stored as (proposed k, accepted a); the replay is exact for a deterministic draft (see
extract2.py). Also stores the per-step action class for the parallel-tool-call bound.
"""
import ast, glob, hashlib, json, os, sys
from tokenizers import Tokenizer

src, tokf, dst = sys.argv[1:4]
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

DEPTH, NOCC = 24, 32   # vLLM default max_tree_depth; occurrences kept per n-gram (most recent)
class Corpus:
    def __init__(self): self.s, self.d = [], {}
    def extend(self, xs):
        s, d = self.s, self.d
        for x in xs:
            s.append(x); L = len(s)
            for n in range(1, min(DEPTH, L) + 1):
                k = hash(tuple(s[L - n:]))
                v = d.get(k)
                if v is None: d[k] = [L]
                else:
                    v.append(L)
                    if len(v) > NOCC: del v[0]
    def occ(self, ctx):
        """longest suffix of ctx (<= DEPTH) with an occurrence that has a continuation -> (p, end positions)"""
        best = (0, None)
        for n in range(1, min(DEPTH, len(ctx)) + 1):
            v = self.d.get(hash(tuple(ctx[-n:])))
            if not v: break
            v = [e for e in v if e < len(self.s)]
            if not v: break
            best = (n, v)
        return best
    def draft(self, ctx, alpha, minp, nspec):
        p, ends = self.occ(ctx)
        if not p: return [], 0.0
        lim = min(int(alpha * p), DEPTH - p, nspec)
        out, prob, score, cur = [], 1.0, 0.0, ends
        while len(out) < lim and cur:
            cnt = {}
            for e in cur:
                if e < len(self.s): cnt[self.s[e]] = cnt.get(self.s[e], 0) + 1
            if not cnt: break
            t, c = max(cnt.items(), key=lambda z: z[1])
            prob *= c / sum(cnt.values())
            if prob < minp: break
            out.append(t); score += prob
            cur = [e + 1 for e in cur if e < len(self.s) and self.s[e] == t]
        return out, score

CFG = {"sd_a1_p10": (1.0, 0.1, 24), "sd_a2_p10": (2.0, 0.1, 24), "sd_a4_p10": (4.0, 0.1, 24),
       "sd_a1_p30": (1.0, 0.3, 24), "sd_a2_p30": (2.0, 0.3, 24)}
def spec(prompt, out, gl, alpha, minp, nspec):
    """prompt corpus (this request), gl (earlier outputs), gen (this request's output so far)"""
    passes, j, gen = [], 0, Corpus()
    while j < len(out):
        ctx = (prompt.s[-DEPTH:] + gen.s)[-DEPTH:]
        cands = [c.draft(ctx, alpha, minp, nspec) for c in (gen, prompt, gl)]
        d = max(cands, key=lambda z: z[1])[0]
        a = 0
        while a < len(d) and j + a < len(out) and d[a] == out[j + a]: a += 1
        passes.append((len(d), a))
        gen.extend(out[j:j + a + 1]); j += a + 1
    return passes

RO = ("str_replace_editor view", "grep", "find ", "ls", "cat ", "head ", "tail ", "sed -n", "cd /testbed && grep",
      "cd /testbed && find", "cd /testbed && ls", "cd /testbed && cat")
res = {}
gl = Corpus()   # earlier outputs (identical for every config: it holds realized tokens)
for f in sorted(glob.glob(os.path.join(src, "*.traj"))):
    d = json.load(open(f)); T = d["trajectory"]; steps = []
    pc, prev = None, None
    for i, st in enumerate(T):
        q = st["query"]
        if i + 1 < len(T) and len(T[i + 1]["query"]) > len(q):
            nxt = [m for m in T[i + 1]["query"][len(q):] if m.get("role") == "assistant"]
            otext = "".join(t for m in nxt[:1] for _, t in parts(m))
        else: otext = st.get("response") or ""
        out = ids(otext)
        qt = [t for m in q for _, t in parts(m)]
        if prev is not None and qt[:len(prev)] == prev:
            for t in qt[len(prev):]: pc.extend(ids(t))
        else:
            pc = Corpus()
            for t in qt: pc.extend(ids(t))
        prev = qt
        rec = {"ro": st.get("action", "").strip().startswith(RO), "out": len(out)}
        for k, (al, mp, ns) in CFG.items(): rec[k] = spec(pc, out, gl, al, mp, ns)
        gl.extend(out)   # vLLM adds each finished request's output to the global tree
        steps.append(rec)
    print(os.path.basename(f), len(T), len(pc.s), file=sys.stderr, flush=True)
    res[os.path.basename(f)[:-5]] = steps
json.dump(res, open(dst, "w"))
Tt = sum(s["out"] for v in res.values() for s in v)
for k in CFG:
    P = sum(len(s[k]) for v in res.values() for s in v); K = sum(p[0] for v in res.values() for s in v for p in s[k])
    print(f"{k}: tokens/pass {Tt/P:.2f}, mean draft {K/P:.2f}")
