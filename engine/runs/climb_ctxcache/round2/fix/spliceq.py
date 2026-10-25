# Quality of the server-side splice (Idea 3) on a real model and real traces, against full recompute.
# Model: SmolLM2-135M-Instruct (GGUF Q4_1 dequantized to fp32; smol.py). Traces: the 200 SWE-agent
# trajectories of round 1. Each trace is replayed under sliding last-KEEP clearing (the placeholder
# replaces each observation that leaves the window). Every message is cut to MSGCAP tokens and a trace
# is followed until the context reaches CAP tokens, to fit the 8k model on CPU.
# Modes, all scored on the same next assistant message (teacher-forced, its real tokens):
#   full     exact recompute of the cleared prompt (reference)
#   splice   one KV cache carried across turns; each cleared observation's KV is cut out, the placeholder's
#            KV is computed on the unchanged prefix, and later keys are RoPE-shifted (llama.cpp / Leyline)
#   noshift  same, but positions keep the gap (no key rotation)
#   keep+1   exact recompute that shows one more old observation (KEEP+1): the size of a context change
#            that harnesses already accept when they pick a window length
#   noise    exact recompute with a different prefill chunking (numerical floor)
# Metrics vs full: mean KL(full || mode) per target token (nats), top-1 agreement, and the change in NLL
# of the real next message. Usage: python3 spliceq.py MODEL.gguf data/traces.jsonl SHARD NSHARDS > out
import sys, json, random, os, torch, smol
KEEP = int(os.environ.get("KEEP", 3)); MSGCAP = int(os.environ.get("MSGCAP", 256))
CAP = int(os.environ.get("CAP", 3072)); NTR = int(os.environ.get("NTR", 24)); EVERY = int(os.environ.get("EVERY", 2))
M = smol.Smol(sys.argv[1]); shard, nsh = int(sys.argv[3]), int(sys.argv[4])
lines = open(sys.argv[2]).read().splitlines()
pick = sorted(random.Random(0).sample(range(len(lines)), NTR))

def seg_tokens(role, text):
    head = M.enc(f"<|im_start|>{role}\n"); body = M.enc(text)[:MSGCAP]; end = M.enc("<|im_end|>\n")
    return head, body, end

def metrics(ref, x):
    lp, lq = torch.log_softmax(ref, -1), torch.log_softmax(x, -1)
    kl = (lp.exp() * (lp - lq)).sum(-1)
    return kl, (ref.argmax(-1) == x.argmax(-1)).float()

def run_trace(t):
    roles = [m["role"] for m in t["msgs"]]; S = [seg_tokens(r, m["text"]) for r, m in zip(roles, t["msgs"])]
    full_ids = [h + b + e for h, b, e in S]
    PHS = [M.enc(f"<|im_start|>{roles[i]}\nOld environment output: ({t['msgs'][i]['text'].count(chr(10))} lines omitted)<|im_end|>\n")
           for i in range(len(roles))]
    is_obs = lambda i: i >= 2 and roles[i] in ("tool", "user")
    def elided(a, keep):
        obs = [i for i in range(a) if is_obs(i)]
        return set(obs[:-keep]) if len(obs) > keep else set()
    def prompt(a, keep):  # token list of msgs[:a] under sliding(keep) + header of msg a
        el = elided(a, keep); ids = []
        for i in range(a): ids += PHS[i] if i in el else full_ids[i]
        return ids + S[a][0]
    caches = {"splice": M.new_cache(), "noshift": M.new_cache()}
    spans = {m: [] for m in caches}   # per mode: list of [msg index, start, end, is_placeholder] in cache order
    done = 0; nclr = 0; rows = []; A = [a for a, r in enumerate(roles) if r == "assistant"]
    for j, a in enumerate(A):
        if len(prompt(a, KEEP)) + len(S[a][1]) > CAP: break
        el = elided(a, KEEP); newclr = 0
        for mode, c in caches.items():
            sh = mode == "splice"
            for sp in spans[mode]:
                if sp[0] in el and not sp[3]:
                    i, s0, s1, _ = sp; n = s1 - s0; ph = PHS[i]
                    M.splice(c, s0, s1, shift=sh); M.insert_at(c, s0, ph, shift=sh)
                    d = len(ph) - n; sp[2] = s0 + len(ph); sp[3] = True
                    for q in spans[mode]:
                        if q[1] > s0: q[1] += d; q[2] += d
                    newclr += mode == "splice"
            # append the messages since the last request, then the target message's header
            for i in range(done, a):
                s0 = len(c["pos"]); M.forward(full_ids[i], c, want_logits=False); spans[mode].append([i, s0, len(c["pos"]), False])
        nclr += newclr; done = a
        tgt = S[a][1]
        if not tgt: continue
        evaluate = nclr > 0 and (j % EVERY == 0)
        outs = {}
        for mode, c in caches.items():  # score the target on a copy, then append msg a for real
            if evaluate:
                tmp = {"k": list(c["k"]), "v": list(c["v"]), "pos": c["pos"].clone()}
                outs[mode] = M.forward(S[a][0] + tgt, tmp, last=len(tgt))[:-1]
        if evaluate:
            p = prompt(a, KEEP); ref = M.forward(p + tgt, M.new_cache(), last=len(tgt))[:-1]
            outs["noise"] = M.forward(p + tgt, M.new_cache(), chunk=384, last=len(tgt))[:-1]
            outs["keep+1"] = M.forward(prompt(a, KEEP + 1) + tgt, M.new_cache(), last=len(tgt))[:-1]
            y = torch.tensor(tgt[1:]); nll_ref = torch.nn.functional.cross_entropy(ref, y).item()
            r = {"id": t["id"], "turn": j, "ctx": len(p), "tgt": len(tgt) - 1, "clears": nclr,
                 "maxpos": int(caches["noshift"]["pos"].max())}
            for k, x in outs.items():
                kl, ag = metrics(ref, x)
                r[k] = {"kl": kl.mean().item(), "top1": ag.mean().item(),
                        "dnll": torch.nn.functional.cross_entropy(x, y).item() - nll_ref}
            rows.append(r); print(json.dumps(r), flush=True)
    return rows

for n, ix in enumerate(pick):
    if n % nsh == shard: run_trace(json.loads(lines[ix]))
