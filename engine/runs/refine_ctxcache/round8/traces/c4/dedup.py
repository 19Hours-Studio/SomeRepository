"""Round 7: how much of each new tool result / tool input repeats lines already visible in the context?

usage: python3 -I dedup.py RAW_TRAJ_DIR TOKENIZER_JSON OUT_JSON [MINRUN]
  same 42 .traj files and legacy Claude tokenizer as extract2.py.

Client-side "reference, don't repeat" rewrite, applied once when a message arrives and then persisted (so the history
stays append-only): every run of >= MINRUN consecutive lines that occurs verbatim and contiguously in an earlier
message of the same request (line numbers from `cat -n` included, so a shifted line never matches) is replaced by
    [<n> lines identical to lines <a>-<b> of message #<j>]
The model loses no information that is not still in its context. Per step we store the rewritten token count of every
message (same order as steps2.json 'm'), for three scopes of 'earlier': everything (keep-all), and only the last K = 3 or 10 tool
results / inputs plus non-tool messages (what stays visible under clearing with keep K; lower bound for batched).
"""
import glob, hashlib, json, os, sys
from tokenizers import Tokenizer
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

src, tokf, dst = sys.argv[1:4]
MINRUN = int(sys.argv[4]) if len(sys.argv) > 4 else 4
tok = Tokenizer.from_file(tokf)
_c = {}
def ntok(s):
    h = hashlib.sha1(s.encode()).hexdigest()
    if h not in _c: _c[h] = len(tok.encode(s, add_special_tokens=False).ids)
    return _c[h]

# message splitting identical to extract2.py
import ast
def content_text(c):
    if isinstance(c, list): return "".join(x.get("text", "") for x in c if isinstance(x, dict))
    if isinstance(c, str) and c.startswith("[{"):
        try: return content_text(ast.literal_eval(c))
        except Exception: return c
    return c if isinstance(c, str) else ""
def parts(m):
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

def lines_of(kind, t):
    # tool-call arguments are JSON: decode escaped newlines so file_text / new_str payloads compare line by line
    if kind == "args": t = t.replace("\\n", "\n").replace('\\"', '"')
    return [l.rstrip("\r") for l in t.split("\n")]

def rewrite(kind, t, earlier):
    """earlier: list of (msg_no, lines). Returns rewritten token count."""
    L = lines_of(kind, t)
    idx = {}
    for j, ls in earlier:
        for p, l in enumerate(ls):
            if l.strip(): idx.setdefault(l, []).append((j, p))
    src_lines = dict(earlier)
    out, k, saved_any = [], 0, False
    while k < len(L):
        best = (0, None, None)
        if L[k].strip():
            for j, p in idx.get(L[k], [])[-16:]:
                ls = src_lines[j]; n = 0
                while k + n < len(L) and p + n < len(ls) and L[k + n] == ls[p + n]: n += 1
                if n > best[0]: best = (n, j, p)
        n, j, p = best
        if n >= MINRUN:
            out.append(f"[{n} lines identical to lines {p+1}-{p+n} of message #{j}]"); k += n; saved_any = True
        else:
            out.append(L[k]); k += 1
    return ntok("\n".join(out)) if saved_any else None

res = {}
for f in sorted(glob.glob(os.path.join(src, "*.traj"))):
    T = json.load(open(f))["trajectory"]
    steps, prev, cache = [], None, {}
    for st in T:
        flat = [(kind, t) for m in st["query"] for kind, t in parts(m)]
        key = [hashlib.sha1((k + t).encode()).hexdigest()[:12] for k, t in flat]
        rows = {"all": [], "k3": [], "k10": []}
        for j, (kind, t) in enumerate(flat):
            ck = tuple(key[:j + 1])
            if ck not in cache:
                base = ntok(t)
                r_all = r_k3 = r_k10 = base
                if kind in ("tool", "args") and t:
                    earlier = [(i, lines_of(flat[i][0], flat[i][1])) for i in range(j)]
                    v = rewrite(kind, t, earlier); r_all = min(base, v) if v is not None else base
                    # visible under keep-K clearing: last K of each clearable kind before j, plus the rest
                    rk = []
                    for K in (3, 10):
                        vis = set()
                        for kd in ("tool", "args"):
                            ix = [i for i in range(j) if flat[i][0] == kd]; vis |= set(ix[-K:])
                        earlierK = [(i, ls) for i, ls in earlier if flat[i][0] not in ("tool", "args") or i in vis]
                        v = rewrite(kind, t, earlierK); rk.append(min(base, v) if v is not None else base)
                    r_k3, r_k10 = rk
                cache[ck] = (base, r_all, r_k3, r_k10)
            b, a, k3, k10 = cache[ck]
            rows["all"].append(a); rows["k3"].append(k3); rows["k10"].append(k10)
        steps.append(rows)
    res[os.path.basename(f)[:-5]] = steps
    print(os.path.basename(f), flush=True)
json.dump(res, open(dst, "w"))
