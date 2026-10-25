# Sanity checks of smol.py: tokenizer round-trip, next-token accuracy on English text and on a real
# trace (correct RoPE convention gives far lower loss than the wrong one), chunked == unchunked prefill,
# splice+reinsert of the same tokens == original cache, and timing.
import sys, time, json, torch, smol
M = smol.Smol(sys.argv[1]); tr = json.loads(open(sys.argv[2]).readline())
txt = ("The quick brown fox jumps over the lazy dog. Python is a programming language that lets you work quickly "
       "and integrate systems more effectively. The capital of France is Paris, and the capital of Germany is Berlin.")
code = tr["msgs"][6]["text"][:6000]
for name, s in (("english", txt), ("trace file view", code)):
    ids = M.enc(s); assert M.tk.decode(ids) == s, "tokenizer round-trip"
    for rt in ("normal", "neox"):
        if rt == "neox":
            orig = M.rope
            def neox(x, pos, o=orig):
                h = x.shape[-1] // 2; y = torch.cat([x[..., :h], x[..., h:]], -1)
                z = torch.stack([y[..., :h], y[..., h:]], -1).flatten(-2); r = o(z, pos)
                return torch.cat([r[..., 0::2], r[..., 1::2]], -1)
            M.rope = neox
        lg = M.forward(ids, M.new_cache()); M.rope = smol.Smol.rope.__get__(M)
        nll = torch.nn.functional.cross_entropy(lg[:-1], torch.tensor(ids[1:])).item()
        acc = (lg[:-1].argmax(-1) == torch.tensor(ids[1:])).float().mean().item()
        print(f"{name:16s} rope={rt:6s} tokens={len(ids):5d} nll={nll:.3f} top1={acc:.3f}  chars/token={len(s)/len(ids):.2f}")
long = "".join(m["text"] for m in tr["msgs"][1:])
ids = M.enc(long)[:1500]
c1 = M.new_cache(); l1 = M.forward(ids, c1, chunk=4096); c2 = M.new_cache(); l2 = M.forward(ids, c2, chunk=256)
print("chunked vs unchunked max |dlogit|:", (l1 - l2).abs().max().item())
c3 = M.new_cache(); M.forward(ids, c3, want_logits=False); a, b = 400, 700
M.splice(c3, a, b); M.insert_at(c3, a, ids[a:b])
print("splice+reinsert same tokens: max |dK| =", max((x - y).abs().max().item() for x, y in zip(c1["k"], c3["k"])),
      " max |dV| =", max((x - y).abs().max().item() for x, y in zip(c1["v"], c3["v"])), " pos equal:", bool((c1["pos"] == c3["pos"]).all()))
cl = M.new_cache(); M.forward(ids, cl); lt = M.forward(ids[:10], cl, last=3)
cf = M.new_cache(); lfull = M.forward(ids + ids[:10], cf)
print("last= option vs full logits, max |dlogit|:", (lt - lfull[-3:]).abs().max().item())
t = time.time(); M.forward(M.enc(long)[:1000], M.new_cache(), last=0); print(f"1000-token prefill (shared machine): {time.time()-t:.1f}s")
