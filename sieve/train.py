"""SIEVE training loop (bit world): generate families -> predict -> pick checks on the lattice -> verify ->
propagate -> learn. Runs on CPU with --config tiny and on an RTX 3060 with --config small/base.

  python3 train.py --config tiny --rounds 20 --device cpu            # smoke test
  python3 train.py --config small --rounds 2000 --device cuda --amp  # RTX 3060

R-free: a fixed set of fully verified validation families (never trained on) sets the temperature and
is the only place metrics come from. Logs: <out>/log.jsonl, checkpoint: <out>/sieve.pt
"""
import argparse, json, math, os, random, time
import numpy as np
import torch
import torch.nn.functional as Fn
from bitworld import make_family, W, MASK
from lattice import Lattice
from model import build, batch_encode, n_params


def gen_round(rng, n_fam, uid0):
    stmts, edges = [], []
    for f in range(n_fam):
        s, e = make_family(rng, uid0 + f); off = len(stmts)
        stmts += s; edges += [(i + off, j + off) for i, j in e]
    return stmts, edges


@torch.no_grad()
def probs(model, stmts, dev, bs=512):
    model.eval(); out = []
    for i in range(0, len(stmts), bs):
        out.append(model.prob(batch_encode(stmts[i:i + bs], model.max_len, dev)).float().cpu())
    return torch.cat(out).numpy()


@torch.no_grad()
def evaluate(model, val, dev):
    """Calibrate temperature on validation families, then report log loss, accuracy, ECE, witness hit rate."""
    stmts, y, cex_rate = val; model.eval(); logits, wit = [], []
    for i in range(0, len(stmts), 512):
        o = model(batch_encode(stmts[i:i + 512], model.max_len, dev)); logits.append(o["verdict"].float().cpu()); wit.append(o["witness"].float().cpu())
    z = torch.cat(logits); wit = torch.cat(wit); yt = torch.tensor(y, dtype=torch.float32)
    grid = torch.exp(torch.linspace(math.log(0.3), math.log(10), 40))
    lls = torch.stack([Fn.binary_cross_entropy_with_logits(z / t, yt) for t in grid]); t = grid[int(lls.argmin())]
    model.log_t.fill_(math.log(float(t)))
    p = torch.sigmoid(z / t).numpy(); bins = np.minimum((p * 10).astype(int), 9)
    ece = sum(abs(p[bins == k].mean() - y[bins == k].mean()) * (bins == k).mean() for k in range(10) if (bins == k).any())
    false_idx = np.flatnonzero(~y.astype(bool)); bits = (wit[false_idx] > 0).int().numpy(); pw = 1 << np.arange(W)
    hits = [stmts[i].is_cex(int((b[0] * pw).sum()), int((b[1] * pw).sum())) for i, b in zip(false_idx, bits)]
    return dict(val_logloss=round(float(lls.min()), 4), val_acc=round(float(((p > 0.5) == y).mean()), 4), val_ece=round(float(ece), 4),
                temperature=round(float(t), 3), witness_hit=round(float(np.mean(hits)), 4) if hits else None,
                random_point_hit=round(float(np.mean(cex_rate[false_idx])), 4) if len(false_idx) else None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="tiny"); ap.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    ap.add_argument("--rounds", type=int, default=20); ap.add_argument("--fams", type=int, default=32, help="new families per round")
    ap.add_argument("--checks", type=int, default=16, help="verifier calls per round")
    ap.add_argument("--acq", default="lattice", choices=["lattice", "random"]); ap.add_argument("--no-prop", action="store_true")
    ap.add_argument("--coh", type=float, default=1.0); ap.add_argument("--wit", type=float, default=0.3)
    ap.add_argument("--steps", type=int, default=20); ap.add_argument("--batch", type=int, default=128)
    ap.add_argument("--lr", type=float, default=3e-4); ap.add_argument("--val-fams", type=int, default=64)
    ap.add_argument("--eval-every", type=int, default=5); ap.add_argument("--amp", action="store_true")
    ap.add_argument("--seed", type=int, default=0); ap.add_argument("--out", default="runs/sieve")
    a = ap.parse_args()
    torch.manual_seed(a.seed); rng = random.Random(a.seed); nrng = np.random.default_rng(a.seed); dev = a.device
    os.makedirs(a.out, exist_ok=True); log = open(os.path.join(a.out, "log.jsonl"), "a")
    model = build(a.config).to(dev); opt = torch.optim.AdamW(model.parameters(), lr=a.lr, weight_decay=0.01)
    print(f"SIEVE {a.config}: {n_params(model) / 1e6:.2f}M params on {dev}", flush=True)
    vs, _ = gen_round(random.Random(10_000 + a.seed), a.val_fams, uid0=10**9)          # R-free validation families
    val = (vs, np.array([s.verify()[0] for s in vs], dtype=np.float32), np.array([s.violation_rate() for s in vs]))
    buf = []  # (stmt, label, weight, cex)
    calls = labels = 0; t0 = time.time(); amp = a.amp and dev.startswith("cuda")
    for r in range(1, a.rounds + 1):
        stmts, edges = gen_round(rng, a.fams, uid0=r * a.fams); lat = Lattice(len(stmts), edges)
        p = probs(model, stmts, dev)
        pick = lat.acquire(p, a.checks, nrng) if a.acq == "lattice" else nrng.choice(len(stmts), a.checks, replace=False)
        cex = {}
        for i in pick:
            ok, c = stmts[i].verify(); lat.observe(i, ok, propagate=not a.no_prop); calls += 1
            if c: cex[i] = c
        lab = np.flatnonzero(lat.label >= 0); labels += len(lab)
        fam = np.array([s.fam for s in stmts]); nver = np.bincount(fam[np.flatnonzero(lat.verified)], minlength=fam.max() + 1)
        nlab = np.bincount(fam[lab], minlength=fam.max() + 1)
        for i in lab: buf.append((stmts[i], float(lat.label[i]), nver[fam[i]] / nlab[fam[i]], cex.get(i)))
        E = torch.tensor(edges, dtype=torch.long)
        model.train()
        for _ in range(a.steps):
            w = np.array([b[2] for b in buf]); idx = nrng.choice(len(buf), min(a.batch, len(buf)), p=w / w.sum())
            bb = [buf[k] for k in idx]; y = torch.tensor([b[1] for b in bb], device=dev)
            with torch.autocast("cuda", dtype=torch.bfloat16, enabled=amp):
                o = model(batch_encode([b[0] for b in bb], model.max_len, dev))
                loss = Fn.binary_cross_entropy_with_logits(o["verdict"].float(), y)
                wi = [k for k, b in enumerate(bb) if b[3] is not None]
                if wi and a.wit > 0:
                    tgt = torch.tensor([[[(c >> j) & 1 for j in range(W)] for c in bb[k][3]] for k in wi], dtype=torch.float32, device=dev)
                    loss = loss + a.wit * Fn.binary_cross_entropy_with_logits(o["witness"][wi].float(), tgt)
                if a.coh > 0 and len(E):
                    sel = E[torch.randperm(len(E))[:a.batch]]; nodes, inv = torch.unique(sel, return_inverse=True)
                    pc = torch.sigmoid(model(batch_encode([stmts[int(k)] for k in nodes], model.max_len, dev))["verdict"].float())
                    loss = loss + a.coh * Fn.relu(pc[inv[:, 0]] - pc[inv[:, 1]]).pow(2).mean()
            opt.zero_grad(set_to_none=True); loss.backward(); torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0); opt.step()
        if r % a.eval_every == 0 or r == a.rounds:
            m = evaluate(model, val, dev); m.update(round=r, calls=calls, labels=labels, labels_per_call=round(labels / calls, 2),
                                                    loss=round(float(loss), 4), sec=round(time.time() - t0, 1))
            print(json.dumps(m), flush=True); log.write(json.dumps(m) + "\n"); log.flush()
            torch.save({"model": model.state_dict(), "config": a.config, "args": vars(a)}, os.path.join(a.out, "sieve.pt"))


if __name__ == "__main__":
    main()
