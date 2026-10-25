# Quality of server-side KV splicing on real SWE-agent traces, measured on a real model (Qwen3-0.6B).
# Policy: SWE-agent-style sliding clearing (old observations beyond the last KEEP are replaced by a
# placeholder). For each request we compare, on the agent's real next action (teacher-forced,
# first ACT tokens), the next-token distribution from
#   ref    : exact prefill of the sliding prompt (what a prefix cache that rewrites the suffix gives)
#   app    : exact prefill of the append-only prompt (nothing cleared) -> size of the clearing effect itself
#   S0     : chained splice: drop the span's KV, compute placeholder KV, re-rotate downstream keys (Leyline / llama.cpp seq_rm+seq_add)
#   SG     : chained splice but keep the position gap (no key re-rotation)
#   S<k>   : S0 + recompute the first k tokens after each cut (boundary repair)
# Usage: python3 -I spliceq.py data/traces.jsonl OUT.jsonl SHARD NSHARD
import sys, os, json, random, time, torch
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
torch.set_num_threads(int(os.environ.get("THREADS", 1)))
from qwen import Qwen3, DIR
from tokenizers import Tokenizer
import traces as T

KEEP = 5; CAP = int(os.environ.get("CAP", 9000)); ACT = 128; NTR = int(os.environ.get("NTR", 12)); KS = (16, 128); MAXEV = int(os.environ.get("MAXEV", 8))
tk = Tokenizer.from_file(f"{DIR}/tokenizer.json")
def wrap(role, text):
    if role == "tool": return f"<|im_start|>user\n<tool_response>\n{text}\n</tool_response><|im_end|>\n"
    return f"<|im_start|>{role}\n{text}<|im_end|>\n"
def enc(s): return tk.encode(s, add_special_tokens=False).ids

def prepare(tr):
    ids = [enc(wrap(r, t)) for r, t in zip(tr["role"], tr["text"])]
    ph = {}
    for i, (r, t) in enumerate(zip(tr["role"], tr["text"])):
        ph[i] = enc(wrap(r, f"Old environment output: ({t.count(chr(10)) + 1} lines omitted)"))
    return ids, ph

def select(Tr):
    ok = []
    for tr in Tr:
        ids, _ = prepare(tr); A = T.requests(tr)
        ev = [a for a in A if sum(len(ids[i]) for i in range(a)) <= CAP and T.old_obs(tr, a)]
        if len(ev) >= 4: ok.append(tr["id"])
    random.Random(0).shuffle(ok)
    return ok[:NTR]

def sl(c, a, b=None): return [(K[:, a:b], V[:, a:b]) for K, V in c]
def cat(*cs): return [(torch.cat([c[l][0] for c in cs], 1), torch.cat([c[l][1] for c in cs], 1)) for l in range(len(cs[0]))]

class Chain:  # a spliced KV cache for the sliding prompt, updated incrementally
    def __init__(s, m, mode, k=0, refresh=0):
        s.m, s.mode, s.k, s.refresh = m, mode, k, refresh
        s.cache = None; s.segs = []; s.pos = []; s.ids = []; s.nsplice = 0; s.work = 0
    def append(s, key, toks):
        start = s.pos[-1] + 1 if s.pos else 0
        _, s.cache = s.m.forward(toks, s.cache, start=start, want_logits=False)
        s.segs.append([key, len(toks)]); s.pos += list(range(start, start + len(toks))); s.ids += toks; s.work += len(toks)
    def off(s, key):
        o = 0
        for k_, n in s.segs:
            if k_ == key: return o, n
            o += n
    def splice(s, i, ph):
        a, n = s.off(i); b = a + n; p = len(ph); p0 = s.pos[a]
        _, c = s.m.forward(ph, sl(s.cache, 0, a), start=p0, want_logits=False); s.work += p
        rest = sl(s.cache, b); tail = s.pos[b:]
        delta = (p0 + p) - s.pos[b] if b < len(s.pos) else 0
        if s.mode == "gap" and delta <= 0: delta = 0           # keep original positions (hole in position ids)
        if delta: rest = [(s.m.shift_keys(K, delta), V) for K, V in rest]; tail = [x + delta for x in tail]
        s.cache = cat(c, rest) if b < len(s.pos) else c
        s.ids = s.ids[:a] + ph + s.ids[b:]; s.pos = s.pos[:a] + list(range(p0, p0 + p)) + tail
        idx = [j for j, (k_, _) in enumerate(s.segs) if k_ == i][0]; s.segs[idx] = [("ph", i), p]
        s.nsplice += 1
        if s.k:  # boundary repair: recompute the first k tokens after the cut on top of the spliced prefix
            e = min(a + p + s.k, len(s.ids))
            if e > a + p:
                _, c2 = s.m.forward(s.ids[a + p:e], sl(s.cache, 0, a + p), start=s.pos[a + p], want_logits=False)
                s.cache = cat(c2, sl(s.cache, e)); s.work += e - a - p
        if s.refresh and s.nsplice % s.refresh == 0:   # exact refresh from the first cut that is still stale
            _, s.cache = s.m.forward(s.ids, None, want_logits=False); s.pos = list(range(len(s.ids))); s.work += len(s.ids)

def dist(m, cache, start, act):
    lo, _ = m.forward(act, cache, start=start, keep=False)
    return torch.log_softmax(lo.float(), -1)

def cmp(ref, x, act):
    kl = (ref.exp() * (ref - x)).sum(-1)
    tgt = torch.tensor(act[1:] + [-1])[:len(act) - 1]
    nll = -x[:len(act) - 1].gather(1, tgt[:, None])[:, 0]
    return {"kl": kl[:-1].mean().item(), "kl_max": kl[:-1].max().item(), "top1": (ref.argmax(-1) == x.argmax(-1))[:-1].float().mean().item(), "nll": nll.mean().item()}

def walk(tr, ids, ph, A, chain, on_eval):
    """Replay the sliding policy request by request; keep `chain` (or None) in sync; call on_eval at eval points."""
    el = set(); done = 0; nev = 0
    for a in A:
        if sum(len(ids[i]) for i in range(a)) > CAP: break
        old = T.old_obs(tr, a); new_el = sorted(old - el, reverse=True)
        if chain is not None:
            for i in new_el:
                if i < done: chain.splice(i, ph[i])
            for i in range(done, a): chain.append(("ph", i) if i in old else i, ph[i] if i in old else ids[i])
        el |= set(new_el); done = a
        if not el: continue
        nev += 1
        if nev > MAXEV: break
        on_eval(a, el)

def run(path, out, shard, nshard):
    Tr = T.load(path); byid = {t["id"]: t for t in Tr}
    sel = select(Tr); m = Qwen3(); fo = open(out, "a"); tmp = os.environ.get("TMPD", "/tmp/claude-0/t")
    os.makedirs(tmp, exist_ok=True)
    print("selected", sel, flush=True)
    variants = {"S0": dict(mode="rot"), "SG": dict(mode="gap")}
    for k in KS: variants[f"S{k}"] = dict(mode="rot", k=k)
    for ti, tid in enumerate(sel):
        if ti % nshard != shard: continue
        tr = byid[tid]; ids, ph = prepare(tr); A = T.requests(tr); recs = {}
        def act_of(a): return enc("<|im_start|>assistant\n" + tr["text"][a])[:ACT]
        def ref_eval(a, el):  # exact references, stored on disk
            t0 = time.time(); act = act_of(a)
            sp = [t for i in range(a) for t in (ph[i] if i in el else ids[i])]
            _, rc = m.forward(sp, None, want_logits=False); ref = dist(m, rc, len(sp), act); del rc
            ap = [t for i in range(a) for t in ids[i]]
            _, ac = m.forward(ap, None, want_logits=False); app = dist(m, ac, len(ap), act); del ac
            torch.save((ref, app), f"{tmp}/{tid}_{a}.pt")
            rec = {"id": tid, "req": a, "n_cleared": len(el), "sliding_len": len(sp), "append_len": len(ap),
                   "ref": cmp(ref, ref, act), "app": cmp(ref, app, act), "ref_vs_app": cmp(app, ref, act)}
            if not recs:  # numerical floor: same exact prompt prefilled in two chunks instead of one
                h = len(sp) // 2
                _, c1 = m.forward(sp[:h], None, want_logits=False); _, c1 = m.forward(sp[h:], c1, want_logits=False)
                rec["floor"] = cmp(ref, dist(m, c1, len(sp), act), act); del c1
            rec["sec_ref"] = round(time.time() - t0, 1); recs[a] = rec
        walk(tr, ids, ph, A, None, ref_eval)
        for name, kw in variants.items():
            ch = Chain(m, **kw)
            def var_eval(a, el, ch=ch, name=name):
                act = act_of(a); assert ch.ids == [t for i in range(a) for t in (ph[i] if i in el else ids[i])], "token mismatch"
                ref, app = torch.load(f"{tmp}/{tid}_{a}.pt"); x = dist(m, ch.cache, ch.pos[-1] + 1, act)
                r = cmp(ref, x, act); r["kl_vs_app"] = cmp(app, x, act)["kl"]; r["work"] = ch.work; recs[a][name] = r
            walk(tr, ids, ph, A, ch, var_eval); del ch
        for a, rec in recs.items():
            fo.write(json.dumps(rec) + "\n"); os.remove(f"{tmp}/{tid}_{a}.pt")
            print(tid, a, rec["sliding_len"], rec["append_len"], {k: round(rec[k]["kl"], 4) for k in ["app"] + list(variants)}, flush=True)
        fo.flush()

if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
