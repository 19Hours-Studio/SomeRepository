# Stale-information leakage of KV splicing, on a real model (Qwen3-0.6B).
# A tool output early in a real SWE-agent context states "port = OLD". It is then (a) corrected to
# "port = NEW" or (b) cleared to a placeholder, and the KV cache is spliced (span replaced, downstream
# keys re-rotated, downstream KV NOT recomputed) or repaired (first k downstream tokens recomputed),
# vs exact recomputation. Query at the end: which port? We score log P(NEW) - log P(OLD) of the answer.
# Downstream filler = the following real messages of the trace (about DOWN tokens).
# REFMSG=1: the next agent message refers to the port without restating it (downstream KV most likely to encode it).
# Usage: [REFMSG=1] python3 -I needle.py data/traces.jsonl OUT.jsonl
import sys, os, json, random, torch
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
torch.set_num_threads(int(os.environ.get("THREADS", 1)))
from qwen import Qwen3
import traces as T, spliceq as S

N = int(os.environ.get("N", 24)); DOWN = int(os.environ.get("DOWN", 1500)); KS = (0, 128, 512)
Q = S.enc("<|im_start|>user\nAccording to the most recent output of `cat /testbed/deploy.ini` above, what is the port? Answer with the number only.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n")

CLR = S.enc(S.wrap("tool", "Old environment output: (6 lines omitted)"))
def obs(v): return S.enc(S.wrap("tool", f"OBSERVATION:\n$ cat /testbed/deploy.ini\n[server]\nhost = 0.0.0.0\nport = {v}\nworkers = 4\n"))

def score(m, cache, start, a, b):  # log P(answer a) - log P(answer b) after the query
    out = {}
    for v in (a, b):
        t = S.enc(str(v)); lo, _ = m.forward(Q + t, cache, start=start, keep=False)
        lp = torch.log_softmax(lo.float(), -1); n0 = len(Q) - 1
        out[v] = sum(lp[n0 + j, t[j]].item() for j in range(len(t)))
    return out[a] - out[b]

def main(path, outp):
    Tr = T.load(path); rnd = random.Random(1); m = Qwen3()
    ndone = sum(1 for _ in open(outp)) if os.path.exists(outp) else 0; fo = open(outp, "a")   # resumable
    for trial in range(N):
        tr = rnd.choice(Tr); old, new = rnd.sample(range(2000, 9999), 2)
        if trial < ndone: continue
        ids, ph = S.prepare(tr)
        pre = ids[0] + ids[1][:400] + S.enc("<|im_end|>\n")          # system + truncated task
        down, j = [], 2
        while len(down) < DOWN and j < len(ids): down += ids[j][:600]; j += 1
        if os.environ.get("REFMSG"):  # harder case: the very next agent message refers to the value without restating it
            down = S.enc(S.wrap("assistant", "I have read deploy.ini and noted the configured port; I will use exactly that port when I start the server later.")) + down
        rec = {"trial": trial, "id": tr["id"], "old": old, "new": new, "down": len(down)}
        _, cp = m.forward(pre, None, want_logits=False)
        # exact references
        for name, span in (("exact_old", obs(old)), ("exact_new", obs(new)), ("exact_cleared", CLR)):
            _, c = m.forward(span + down, cp, want_logits=False, keep="new"); c = S.cat(cp, c)
            rec[name] = score(m, c, len(pre) + len(span) + len(down), new, old)
        # stale cache: computed with the OLD observation
        so = obs(old); _, cs = m.forward(so + down, cp, want_logits=False, keep="new"); stale = S.cat(cp, cs)
        for edit, span in (("corr", obs(new)), ("clear", CLR)):
            a = len(pre); b = a + len(so); p = len(span)
            _, c = m.forward(span, S.sl(stale, 0, a), want_logits=False, keep="new")
            rest = S.sl(stale, b); delta = p - len(so)
            if delta: rest = [(m.shift_keys(K, delta), V) for K, V in rest]
            sp = S.cat(S.sl(stale, 0, a), c, rest); toks = pre + span + down
            for k in KS:
                cc = sp
                if k:
                    e = min(a + p + k, len(toks))
                    _, c2 = m.forward(toks[a + p:e], S.sl(sp, 0, a + p), want_logits=False, keep="new")
                    cc = S.cat(S.sl(sp, 0, a + p), c2, S.sl(sp, e))
                rec[f"{edit}_splice_k{k}"] = score(m, cc, len(toks), new, old)
        fo.write(json.dumps(rec) + "\n"); fo.flush()
        print({k: (round(v, 2) if isinstance(v, float) else v) for k, v in rec.items()}, flush=True)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
