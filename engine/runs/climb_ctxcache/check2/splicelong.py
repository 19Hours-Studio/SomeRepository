# check2: splice quality over LONG splice chains (the cost claim assumes ~55 splices/trace; the author's
# test reaches <=9). Same model/code as round2/fix (smol.py), shorter messages so many more turns fit.
# At each eval point: reference A = full recompute of the cleared prompt (author's reference),
# reference B = the append-only prompt the agent actually ran (when it fits in ACAP).
# Reports KL(full||splice), KL(append||splice), KL(append||full), dNLL on the real next message.
import sys, json, random, os, torch
sys.path.insert(0, os.environ["FIX"]); import smol
KEEP = int(os.environ.get("KEEP", 3)); MSGCAP = int(os.environ.get("MSGCAP", 64))
CAP = int(os.environ.get("CAP", 3072)); ACAP = int(os.environ.get("ACAP", 4096))
NTR = int(os.environ.get("NTR", 12)); EVERY = int(os.environ.get("EVERY", 4))
M = smol.Smol(sys.argv[1]); shard, nsh = int(sys.argv[3]), int(sys.argv[4])
lines = open(sys.argv[2]).read().splitlines()
pick = sorted(random.Random(1).sample(range(len(lines)), NTR))
def met(ref, x, y):
    lp, lq = torch.log_softmax(ref, -1), torch.log_softmax(x, -1)
    return {"kl": (lp.exp() * (lp - lq)).sum(-1).mean().item(), "top1": (ref.argmax(-1) == x.argmax(-1)).float().mean().item()}
def nll(x, y): return torch.nn.functional.cross_entropy(x, y).item()
for n, ix in enumerate(pick):
    if n % nsh != shard: continue
    t = json.loads(lines[ix]); roles = [m["role"] for m in t["msgs"]]
    S = [(M.enc(f"<|im_start|>{r}\n"), M.enc(m["text"])[:MSGCAP], M.enc("<|im_end|>\n")) for r, m in zip(roles, t["msgs"])]
    full_ids = [h + b + e for h, b, e in S]
    PHS = [M.enc(f"<|im_start|>{roles[i]}\nOld environment output: ({t['msgs'][i]['text'].count(chr(10))} lines omitted)<|im_end|>\n") for i in range(len(roles))]
    is_obs = lambda i: i >= 2 and roles[i] in ("tool", "user")
    def elided(a, keep):
        if keep is None: return set()
        obs = [i for i in range(a) if is_obs(i)]; return set(obs[:-keep]) if len(obs) > keep else set()
    def prompt(a, keep):
        el = elided(a, keep); ids = []
        for i in range(a): ids += PHS[i] if i in el else full_ids[i]
        return ids + S[a][0]
    c = M.new_cache(); spans = []; done = 0; nclr = 0
    A = [a for a, r in enumerate(roles) if r == "assistant"]
    for j, a in enumerate(A):
        if len(prompt(a, KEEP)) + len(S[a][1]) > CAP: break
        el = elided(a, KEEP)
        for sp in spans:
            if sp[0] in el and not sp[3]:
                i, s0, s1, _ = sp; ph = PHS[i]
                M.splice(c, s0, s1); M.insert_at(c, s0, ph); d = len(ph) - (s1 - s0); sp[2] = s0 + len(ph); sp[3] = True
                for q in spans:
                    if q[1] > s0: q[1] += d; q[2] += d
                nclr += 1
        for i in range(done, a):
            s0 = len(c["pos"]); M.forward(full_ids[i], c, want_logits=False); spans.append([i, s0, len(c["pos"]), False])
        done = a; tgt = S[a][1]
        if len(tgt) < 2 or nclr == 0 or j % EVERY: continue
        y = torch.tensor(tgt[1:])
        tmp = {"k": list(c["k"]), "v": list(c["v"]), "pos": c["pos"].clone()}
        xs = M.forward(S[a][0] + tgt, tmp, last=len(tgt))[:-1]
        p = prompt(a, KEEP); assert len(tmp["pos"]) == len(p) + len(tgt), "cache/prompt length mismatch"
        xf = M.forward(p + tgt, M.new_cache(), last=len(tgt))[:-1]
        r = {"id": t["id"], "turn": j, "ctx": len(p), "clears": nclr, "tgt": len(tgt) - 1,
             "s_vs_full": met(xf, xs, y), "dnll_s_full": nll(xs, y) - nll(xf, y)}
        pa = prompt(a, None)
        if len(pa) + len(tgt) <= ACAP:
            xa = M.forward(pa + tgt, M.new_cache(), last=len(tgt))[:-1]
            r["actx"] = len(pa); r["s_vs_app"] = met(xa, xs, y); r["f_vs_app"] = met(xa, xf, y)
            r["dnll_s_app"] = nll(xs, y) - nll(xa, y); r["dnll_f_app"] = nll(xf, y) - nll(xa, y)
        print(json.dumps(r), flush=True)
