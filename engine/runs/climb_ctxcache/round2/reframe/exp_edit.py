"""Real-model quality test of non-prefix KV reuse on real SWE-agent contexts.

Model: SmolLM2-135M-Instruct (Q4_1 GGUF from PyPI `llm-smollm2`), our own torch
forward pass (smol.py).  Context: the first messages of a real SWE-agent
trajectory (data/traces.jsonl), ChatML, each message truncated to MAXSEG tokens,
cut at the last assistant turn that fits in BUDGET tokens.  The evaluation
target is that real assistant message (first TGT tokens), teacher-forced.

Edit cases, all applied to the *middle* of the context:
  clear   : replace every tool output except the last KEEP with a 12-token
            placeholder (what SWE-agent / OpenHands / clear_tool_uses do)
  replace : one middle tool output is replaced by a different real tool output
  insert  : a real tool output from another trace is inserted mid-context
  reorder : two consecutive middle (assistant, tool) exchanges are swapped

For each case the reference EXACT is ordinary prefix caching: the unchanged
prefix is reused, everything from the first changed token is recomputed.
Reuse variants keep the original KV of every unchanged token:
  gap     : (clear only) original positions kept, so positions have holes
  shift   : keys re-rotated to their new contiguous positions (Leyline-style)
  shift+bK: as shift, but the first K unchanged tokens after every change point
            are recomputed
  shift+bK+tail: additionally the last TAIL prompt tokens are recomputed
New tokens (placeholders, inserted text) are always computed fresh, attending
to the assembled cache.  Metrics on the target tokens, vs EXACT: KL(EXACT||X),
top-1 agreement, and NLL of the real next action.  FULL (= unedited context,
i.e. what the model saw before the edit) is reported as the scale of the edit.

Usage: python3 -I exp_edit.py data/traces.jsonl SHARD NSHARDS out.jsonl
"""
import json, sys, os, random, math, torch
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import smol
from smol import cache_select, cache_cat

BUDGET = int(os.environ.get("BUDGET", 6000)); MAXSEG = 1200; TGT = 96; KEEP = 2
NTRACE = int(os.environ.get("NTRACE", 48)); TAIL = 256
PH = "Old environment output: ({n} lines omitted)"


def chatml(role, text):
    return f"<|im_start|>{role}\n{text}<|im_end|>\n"


def build(m, tr):
    """Return list of message segments (role, ids, raw_text) and the target ids."""
    segs = []
    for x in tr["msgs"]:
        role = x["role"]
        body = m.enc(x["text"])[:MAXSEG]
        segs.append((role, m.enc(f"<|im_start|>{role}\n") + body + m.enc("<|im_end|>\n"), x["text"]))
    # choose the last assistant message a with len(segs[:a]) <= BUDGET and >= KEEP+3 tool outputs before it
    best = None; tot = 0
    for a, s in enumerate(segs):
        if s[0] == "assistant" and a > 0:
            nobs = sum(1 for r, _, _ in segs[2:a] if r in ("tool", "user"))
            if tot <= BUDGET and nobs >= KEEP + 3:
                best = a
        tot += len(s[1])
        if tot > BUDGET:
            break
    if best is None:
        return None
    hdr = m.enc("<|im_start|>assistant\n")
    tgt = hdr + m.enc(segs[best][2])[:TGT]
    return segs[:best], tgt, len(hdr)


def obs_idx(segs):
    return [i for i in range(2, len(segs)) if segs[i][0] in ("tool", "user")]


def edits(m, segs, donor, rng):
    """Each edit -> list of pieces: ('reuse', seg_i) or ('new', ids)."""
    out = {}
    ob = obs_idx(segs); stale = ob[:-KEEP]
    pieces = []
    for i in range(len(segs)):
        if i in stale:
            n = segs[i][2].count("\n") + 1
            pieces.append(("new", m.enc(chatml(segs[i][0], PH.format(n=n)))))
        else:
            pieces.append(("reuse", i))
    out["clear"] = pieces
    mid = stale[len(stale) // 2]
    d_ids = m.enc(chatml("tool", donor))[:MAXSEG]
    out["replace"] = [("new", d_ids) if i == mid else ("reuse", i) for i in range(len(segs))]
    ins = []
    for i in range(len(segs)):
        ins.append(("reuse", i))
        if i == mid:
            ins.append(("new", d_ids))
    out["insert"] = ins
    # swap exchange (mid-1, mid) with (mid+1, mid+2) if they form assistant/tool pairs
    j = mid
    if j + 2 < len(segs) and segs[j - 1][0] == "assistant" and segs[j + 1][0] == "assistant" and j + 2 not in ob[-KEEP:]:
        order = list(range(len(segs)))
        order[j - 1:j + 3] = [j + 1, j + 2, j - 1, j]
        out["reorder"] = [("reuse", i) for i in order]
    return out


def flatten(segs, pieces, offs):
    """Token list of the edited prompt + for each token its source orig index (or -1 if new)."""
    ids, src = [], []
    for kind, v in pieces:
        if kind == "new":
            ids += v; src += [-1] * len(v)
        else:
            ids += segs[v][1]; src += list(range(offs[v], offs[v] + len(segs[v][1])))
    return ids, src


def first_change(src):
    for t, s in enumerate(src):
        if s != t:
            return t
    return len(src)


def assemble(m, base, ids, src, mode, K=0, tail=0, gap_pos=None):
    """Build a KV cache for prompt `ids` from base KV (computed on the original
    prompt).  src[t] = original index of token t or -1 if new.  Returns cache,
    next position, and number of tokens recomputed."""
    n = len(ids)
    pos = list(gap_pos) if mode == "gap" else list(range(n))
    fc = first_change(src)
    recompute = [False] * n
    for t in range(fc, n):
        if src[t] < 0:
            recompute[t] = True
    # boundary recompute: first K reused tokens after every change point
    if K:
        run = 0
        for t in range(fc, n):
            if src[t] < 0:
                run = K; continue
            if t == fc or src[t] != src[t - 1] + 1:
                run = K
            if run > 0:
                recompute[t] = True; run -= 1
    if tail:
        for t in range(max(fc, n - tail), n):
            recompute[t] = True
    cache = cache_select(base, list(range(fc)))  # exact shared prefix
    t = fc; nrec = 0
    while t < n:
        u = t
        while u < n and recompute[u] == recompute[t]:
            u += 1
        if recompute[t]:
            _, cache = m.forward(ids[t:u], pos[t:u], cache, return_logits=False)
            nrec += u - t
        else:
            idx = torch.tensor(src[t:u]); piece = cache_select(base, idx)
            newp = torch.tensor(pos[t:u]); d = newp - piece["pos"]
            if bool((d != 0).any()):
                piece["k"] = [m.rerotate(k, d) for k in piece["k"]]
            piece["pos"] = newp
            cache = cache_cat(cache, piece)
        t = u
    nxt = (max(pos) + 1) if n else 0
    return cache, nxt, nrec


def score(m, cache, nxt, tgt, hl):
    lo, _ = m.forward(tgt, range(nxt, nxt + len(tgt)), cache)
    lo = lo[hl - 1:-1].double()
    return torch.log_softmax(lo, -1)


def cmp(ref, x, tgt, hl):
    y = torch.tensor(tgt[hl:])
    kl = (ref.exp() * (ref - x)).sum(-1)
    return {"kl": float(kl.mean()), "top1": float((ref.argmax(-1) == x.argmax(-1)).double().mean()),
            "nll": float(-x.gather(1, y[:, None]).mean())}


def main():
    path, shard, nsh, outp = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    T = [json.loads(l) for l in open(path)]
    rng = random.Random(0)
    order = list(range(len(T))); rng.shuffle(order)
    m = smol.Smol()
    done = set()
    if os.path.exists(outp):
        done = {json.loads(l)["id"] for l in open(outp)}
    fo = open(outp, "a")
    picked = 0
    for k, ti in enumerate(order):
        if picked >= NTRACE:
            break
        tr = T[ti]
        b = build(m, tr)
        if b is None:
            continue
        picked += 1
        if (picked - 1) % nsh != shard or tr["id"] in done:
            continue
        segs, tgt, hl = b
        # donor tool output: a real observation from the next trace in the order
        dn = T[order[(k + 1) % len(T)]]["msgs"]
        donor = max((x["text"] for x in dn[2:12] if x["role"] in ("tool", "user")), key=len)[:3000]
        offs = [0]
        for s in segs:
            offs.append(offs[-1] + len(s[1]))
        orig = [t for s in segs for t in s[1]]
        rgen = random.Random(ti)
        lo_full, base = m.forward(orig, range(len(orig)), return_logits=False)
        full = score(m, base, len(orig), tgt, hl)
        rec = {"id": tr["id"], "ntok": len(orig), "nseg": len(segs), "cases": {}}
        for case, pieces in edits(m, segs, donor, rgen).items():
            ids, src = flatten(segs, pieces, offs)
            fc = first_change(src)
            ex_c, nx, nrec_ex = assemble(m, base, ids, src, "exact", tail=len(ids))
            exact = score(m, ex_c, nx, tgt, hl)
            r = {"ntok": len(ids), "first_change": fc, "n_new": sum(1 for s in src if s < 0),
                 "recompute_exact": nrec_ex, "FULL": cmp(exact, full, tgt, hl), "EXACT": cmp(exact, exact, tgt, hl)}
            variants = [("shift", 0, 0), ("shift+b16", 16, 0), ("shift+b64", 64, 0), ("shift+b16+tail", 16, TAIL)]
            if case == "clear":
                # gap positions: each segment (or its placeholder) starts at its original offset
                gp = []
                for i, (kind, v) in enumerate(pieces):
                    L = len(v) if kind == "new" else len(segs[v][1])
                    gp += list(range(offs[i], offs[i] + L))
                variants = [("gap", 0, 0), ("gap+b16", 16, 0)] + variants
            for name, K, tail in variants:
                mode = "gap" if name.startswith("gap") else "shift"
                c, nx, nrec = assemble(m, base, ids, src, mode, K=K, tail=tail,
                                       gap_pos=gp if mode == "gap" else None)
                x = score(m, c, nx, tgt, hl)
                r[name] = cmp(exact, x, tgt, hl); r[name]["recompute"] = nrec
            rec["cases"][case] = r
        fo.write(json.dumps(rec) + "\n"); fo.flush()
        print(tr["id"], {c: round(v["shift"]["kl"], 4) for c, v in rec["cases"].items()}, flush=True)


if __name__ == "__main__":
    main()
