"""Find where a request breaks the prompt cache relative to the previous request of the same session.

Usage: python3 -I cachediff.py prev.json next.json [--read 0.1 --write 1.25]
Accepts Anthropic Messages or OpenAI Chat/Responses request bodies (system/tools/messages/input).
Token counts are chars/4 estimates; for exact numbers diff the token IDs your server logs.
"""
import json, re, sys

TS = re.compile(r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}(:\d{2})?|\b1[6-9]\d{8}\b")   # ISO times, unix secs
UUID = re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b")


def blocks(req):
    """Flatten a request into (label, canonical-ish text) in the order the server renders it."""
    out = []
    for i, t in enumerate(req.get("tools", [])):
        out.append((f"tools[{i}]", json.dumps(t, ensure_ascii=False)))
    sysm = req.get("system")
    if sysm is not None:
        for i, b in enumerate(sysm if isinstance(sysm, list) else [sysm]):
            out.append((f"system[{i}]", b if isinstance(b, str) else json.dumps(b, ensure_ascii=False)))
    for i, m in enumerate(req.get("messages", req.get("input", [])) or []):
        c = m.get("content", m) if isinstance(m, dict) else m
        parts = c if isinstance(c, list) else [c]
        for j, p in enumerate(parts):
            if isinstance(p, dict):
                p = {k: v for k, v in p.items() if k != "cache_control"}   # markers do not change tokens
            out.append((f"messages[{i}].{m.get('role', '?') if isinstance(m, dict) else '?'}[{j}]",
                        p if isinstance(p, str) else json.dumps(p, ensure_ascii=False)))
    return out


def cause(a, b):
    if a == b:
        return None
    if TS.sub("", a) == TS.sub("", b):
        return "only timestamps differ -> move them to the tail or drop them"
    if UUID.sub("", a) == UUID.sub("", b):
        return "only UUIDs/request ids differ -> make them stable or move them to the tail"
    try:
        ja, jb = json.loads(a), json.loads(b)
        if json.dumps(ja, sort_keys=True) == json.dumps(jb, sort_keys=True):
            return "same JSON, different key order -> serialize with sort_keys"
        if isinstance(ja, dict) and "thinking" in json.dumps(ja) and "thinking" not in json.dumps(jb):
            return "reasoning removed from an earlier turn -> keep it, or splice it out server-side"
    except (ValueError, TypeError):
        pass
    if sorted(a.split("\n")) == sorted(b.split("\n")):
        return "same lines, different order (unordered listing?) -> sort before sending"
    k = next((i for i, (x, y) in enumerate(zip(a, b)) if x != y), min(len(a), len(b)))
    return f"content edit at char {k}: {a[max(0, k-30):k+30]!r} -> {b[max(0, k-30):k+30]!r}"


def main(p, n, read=0.1, write=1.25):
    A, B = blocks(json.load(open(p))), blocks(json.load(open(n)))
    tok = lambda s: max(1, len(s) // 4)
    i = next((i for i, (x, y) in enumerate(zip(A, B)) if x != y), min(len(A), len(B)))
    hit = sum(tok(t) for _, t in B[:i]); tot = sum(tok(t) for _, t in B)
    print(f"first divergent block: {B[i][0] if i < len(B) else '(none: pure append)'}")
    if i < len(A) and i < len(B):
        print(f"cause: {cause(A[i][1], B[i][1])}")
        seen = {x for _, x in A[i:]}
        same = [(lab, t) for lab, t in B[i + 1:] if t in seen]
        if same:
            print(f"{len(same)} later blocks (~{sum(tok(t) for _, t in same):,} tok) are unchanged in content "
                  f"but recomputed: exact errata (Idea 1) or segment reuse (Ideas 2-3) would save them")
    print(f"cacheable prefix ~{hit:,} of ~{tot:,} tokens ({hit/max(tot,1):.1%}); "
          f"recomputed ~{tot-hit:,}, input cost x{(hit*read+(tot-hit)*write)/(tot*read+1e-9):.1f} of a full hit")
    n_bp = sum(json.dumps(x).count("cache_control") for x in json.load(open(n)).get("messages", []))
    if len(B) - i > 20 and n_bp <= 1:
        print("warning: divergence is >20 blocks before the end; with a single end breakpoint the ~20-block "
              "lookback will not find the cached prefix -> add explicit breakpoints at stable boundaries")


if __name__ == "__main__":
    args = sys.argv[1:]
    kw = {}
    for k in ("--read", "--write"):
        if k in args:
            j = args.index(k); kw[k[2:]] = float(args[j + 1]); del args[j:j + 2]
    main(*args, **kw)
