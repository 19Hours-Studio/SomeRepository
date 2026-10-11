"""SIEVE training loop (bit world): generate families -> predict -> pick checks on the lattice -> verify ->
propagate -> learn. Runs on CPU with --config tiny and on an RTX 3060 with --preset 3060.

  python3 train.py --config tiny --rounds 20 --device cpu                     # smoke test
  python3 train.py --preset 3060                                              # RTX 3060, ~1 hour
  python3 train.py --preset 3060 --acq random --no-prop --out runs/baseline   # control without the lattice

R-free: a fixed set of fully verified validation families (never trained on) sets the temperature and
is the only place metrics come from. Logs: <out>/log.jsonl, checkpoint: <out>/sieve.pt
"""
import argparse, json, math, os, random, sys, time
import numpy as np
import torch
import torch.nn.functional as Fn
from bitworld import make_family, W
from lattice import Lattice
from model import build, collate, encode_np, n_params

PRESETS = {  # many fresh labels per round, large batches, few passes over each label (avoids memorizing)
    "3060": dict(config="small", device="cuda", amp=True, rounds=500, fams=256, checks=128, steps=10,
                 batch=512, eval_every=10, val_fams=128, buffer=300_000),
}


def gen_round(rng, n_fam, uid0):
    stmts, edges = [], []
    for f in range(n_fam):
        s, e = make_family(rng, uid0 + f); off = len(stmts)
        stmts += s; edges += [(i + off, j + off) for i, j in e]
    return stmts, edges


class Buffer:
    """FIFO replay of verified (or lattice-propagated) labels with per-family weights."""
    def __init__(self, cap): self.cap, self.enc, self.y, self.w, self.cex = cap, [], [], [], []

    def add(self, encs, y, w, cex):
        self.enc += encs; self.y += y; self.w += w; self.cex += cex
        if len(self.y) > self.cap:
            k = len(self.y) - self.cap
            self.enc, self.y, self.w, self.cex = self.enc[k:], self.y[k:], self.w[k:], self.cex[k:]
        self._w = np.asarray(self.w, dtype=np.float64); self._w /= self._w.sum()

    def sample(self, rng, n):
        return rng.choice(len(self.y), min(n, len(self.y)), p=self._w)


@torch.no_grad()
def logits_and_witness(model, encs, dev, bs=1024):
    model.eval(); z, w = [], []
    for i in range(0, len(encs), bs):
        o = model(collate(encs[i:i + bs], dev)); z.append(o["verdict"].float().cpu()); w.append(o["witness"].float().cpu())
    return torch.cat(z), torch.cat(w)


@torch.no_grad()
def evaluate(model, val, dev):
    """Calibrate temperature on validation families, then report log loss, accuracy, ECE, witness hit rate."""
    stmts, encs, y, cex_rate = val
    z, wit = logits_and_witness(model, encs, dev); yt = torch.tensor(y, dtype=torch.float32)
    grid = torch.exp(torch.linspace(math.log(0.3), math.log(30), 60))
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
    ap.add_argument("--preset", choices=list(PRESETS), help="fills every option it defines; explicit flags still win")
    ap.add_argument("--config", default="tiny"); ap.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    ap.add_argument("--rounds", type=int, default=20); ap.add_argument("--fams", type=int, default=32, help="new families per round")
    ap.add_argument("--checks", type=int, default=16, help="verifier calls per round")
    ap.add_argument("--acq", default="lattice", choices=["lattice", "random"]); ap.add_argument("--no-prop", action="store_true")
    ap.add_argument("--coh", type=float, default=1.0); ap.add_argument("--wit", type=float, default=0.3)
    ap.add_argument("--steps", type=int, default=20); ap.add_argument("--batch", type=int, default=128)
    ap.add_argument("--lr", type=float, default=3e-4); ap.add_argument("--val-fams", type=int, default=64)
    ap.add_argument("--eval-every", type=int, default=5); ap.add_argument("--amp", action="store_true")
    ap.add_argument("--buffer", type=int, default=100_000); ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", default="runs/sieve")
    a = ap.parse_args()
    if a.preset:  # preset values unless the flag was given explicitly on the command line
        given = {x.split("=")[0].lstrip("-").replace("-", "_") for x in sys.argv[1:] if x.startswith("--")}
        for k, v in PRESETS[a.preset].items():
            if k not in given: setattr(a, k, v)
    if a.device == "cuda" and not torch.cuda.is_available():
        raise SystemExit("CUDA is not available: install the CUDA build of PyTorch (see sieve/README.md)")
    torch.manual_seed(a.seed); rng = random.Random(a.seed); nrng = np.random.default_rng(a.seed); dev = a.device
    if dev.startswith("cuda"): torch.backends.cuda.matmul.allow_tf32 = True
    os.makedirs(a.out, exist_ok=True); log = open(os.path.join(a.out, "log.jsonl"), "a")
    model = build(a.config).to(dev); opt = torch.optim.AdamW(model.parameters(), lr=a.lr, weight_decay=0.01)
    sched = torch.optim.lr_scheduler.LambdaLR(opt, lambda s: min(1.0, (s + 1) / 200) * 0.5 * (1 + math.cos(math.pi * min(1.0, s / (a.rounds * a.steps)))))
    print(f"SIEVE {a.config}: {n_params(model) / 1e6:.2f}M params on {dev}; rounds {a.rounds} x (fams {a.fams}, checks {a.checks}, "
          f"steps {a.steps}, batch {a.batch}); acq {a.acq}, propagation {not a.no_prop}", flush=True)
    vs, _ = gen_round(random.Random(10_000 + a.seed), a.val_fams, uid0=10**9)          # R-free validation families
    val = (vs, [encode_np(s, model.max_len) for s in vs], np.array([s.verify()[0] for s in vs], dtype=np.float32),
           np.array([s.violation_rate() for s in vs]))
    buf = Buffer(a.buffer); calls = labels = 0; t0 = time.time(); amp = a.amp and dev.startswith("cuda")
    for r in range(1, a.rounds + 1):
        stmts, edges = gen_round(rng, a.fams, uid0=r * a.fams); lat = Lattice(len(stmts), edges)
        encs = [encode_np(s, model.max_len) for s in stmts]
        if a.acq == "lattice":
            z, _ = logits_and_witness(model, encs, dev); p = torch.sigmoid(z / model.log_t.exp().cpu()).numpy()
            pick = lat.acquire(p, a.checks, nrng)
        else:
            pick = nrng.choice(len(stmts), a.checks, replace=False)
        cex = {}
        for i in pick:
            ok, c = stmts[i].verify(); lat.observe(i, ok, propagate=not a.no_prop); calls += 1
            if c: cex[i] = np.array([[(v >> j) & 1 for j in range(W)] for v in c], dtype=np.float32)
        lab = np.flatnonzero(lat.label >= 0); labels += len(lab)
        fam = np.array([s.fam for s in stmts]); fam -= fam.min()
        nver = np.bincount(fam[np.flatnonzero(lat.verified)], minlength=fam.max() + 1); nlab = np.bincount(fam[lab], minlength=fam.max() + 1)
        buf.add([encs[i] for i in lab], [float(lat.label[i]) for i in lab], [nver[fam[i]] / nlab[fam[i]] for i in lab], [cex.get(i) for i in lab])
        E = np.asarray(edges, dtype=np.int64)
        model.train()
        for _ in range(a.steps):
            idx = buf.sample(nrng, a.batch); y = torch.tensor([buf.y[k] for k in idx], device=dev)
            with torch.autocast("cuda", dtype=torch.bfloat16, enabled=amp):
                o = model(collate([buf.enc[k] for k in idx], dev))
                loss = Fn.binary_cross_entropy_with_logits(o["verdict"].float(), y)
                wi = [n for n, k in enumerate(idx) if buf.cex[k] is not None]
                if wi and a.wit > 0:
                    tgt = torch.from_numpy(np.stack([buf.cex[idx[n]] for n in wi])).to(dev)
                    loss = loss + a.wit * Fn.binary_cross_entropy_with_logits(o["witness"][wi].float(), tgt)
                if a.coh > 0 and len(E):
                    sel = E[nrng.choice(len(E), min(a.batch // 2, len(E)), replace=False)]
                    nodes, inv = np.unique(sel, return_inverse=True); inv = inv.reshape(-1, 2)
                    pc = torch.sigmoid(model(collate([encs[k] for k in nodes], dev))["verdict"].float())
                    inv = torch.from_numpy(inv).to(dev)
                    loss = loss + a.coh * Fn.relu(pc[inv[:, 0]] - pc[inv[:, 1]]).pow(2).mean()
            opt.zero_grad(set_to_none=True); loss.backward(); torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt.step(); sched.step()
        if r % a.eval_every == 0 or r == a.rounds:
            m = evaluate(model, val, dev); m.update(round=r, calls=calls, labels=labels, labels_per_call=round(labels / calls, 2),
                                                    loss=round(loss.item(), 4), sec=round(time.time() - t0, 1))
            print(json.dumps(m), flush=True); log.write(json.dumps(m) + "\n"); log.flush()
            torch.save({"model": model.state_dict(), "config": a.config, "args": vars(a)}, os.path.join(a.out, "sieve.pt"))


if __name__ == "__main__":
    main()
