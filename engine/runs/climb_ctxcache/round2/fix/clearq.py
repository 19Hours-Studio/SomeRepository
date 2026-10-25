# How much does clearing itself (exact KV, no splice) move the next-token distribution, compared with
# the append-only prompt the agent actually ran? Same model, traces and truncation as spliceq.py.
# At every EVERY-th request whose append-only prompt fits in CAP tokens, score the real next assistant
# message under: append (reference), sliding keep-5, sliding keep-3. A proxy only: a 135M model, KL on
# teacher-forced tokens, not task success. Usage: python3 clearq.py MODEL.gguf data/traces.jsonl > out
import sys, json, random, os, torch, smol
MSGCAP = int(os.environ.get("MSGCAP", 192)); CAP = int(os.environ.get("CAP", 2048))
NTR = int(os.environ.get("NTR", 18)); EVERY = int(os.environ.get("EVERY", 2))
M = smol.Smol(sys.argv[1]); lines = open(sys.argv[2]).read().splitlines()
pick = sorted(random.Random(0).sample(range(len(lines)), NTR))
for ix in pick:
    t = json.loads(lines[ix]); roles = [m["role"] for m in t["msgs"]]
    S = [(M.enc(f"<|im_start|>{r}\n"), M.enc(m["text"])[:MSGCAP], M.enc("<|im_end|>\n")) for r, m in zip(roles, t["msgs"])]
    PHS = [M.enc(f"<|im_start|>{roles[i]}\nOld environment output: ({t['msgs'][i]['text'].count(chr(10))} lines omitted)<|im_end|>\n")
           for i in range(len(roles))]
    def prompt(a, keep):
        obs = [i for i in range(a) if i >= 2 and roles[i] in ("tool", "user")]
        el = set(obs[:-keep]) if keep and len(obs) > keep else set(); ids = []
        for i in range(a): ids += PHS[i] if i in el else S[i][0] + S[i][1] + S[i][2]
        return ids + S[a][0]
    A = [a for a, r in enumerate(roles) if r == "assistant"]
    for j, a in enumerate(A):
        tgt = S[a][1]; p0 = prompt(a, None)
        if len(p0) + len(tgt) > CAP: break
        if j % EVERY or len(tgt) < 2 or p0 == prompt(a, 3): continue
        ref = M.forward(p0 + tgt, M.new_cache(), last=len(tgt))[:-1]; y = torch.tensor(tgt[1:])
        lp = torch.log_softmax(ref, -1); r = {"id": t["id"], "turn": j, "ctx_append": len(p0), "tgt": len(tgt) - 1}
        for keep in (5, 3):
            p = prompt(a, keep); x = M.forward(p + tgt, M.new_cache(), last=len(tgt))[:-1]; lq = torch.log_softmax(x, -1)
            r[f"keep{keep}"] = {"ctx": len(p), "kl": (lp.exp() * (lp - lq)).sum(-1).mean().item(),
                                "top1": (ref.argmax(-1) == x.argmax(-1)).float().mean().item(),
                                "dnll": (torch.nn.functional.cross_entropy(x, y) - torch.nn.functional.cross_entropy(ref, y)).item()}
        print(json.dumps(r), flush=True)
