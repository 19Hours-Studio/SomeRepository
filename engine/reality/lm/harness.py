"""Open reality: character-level language modelling of unseen Python source under a fixed compute budget.
Nobody knows the best tiny architecture here, so only measurement can tell. A candidate defines
`class Model(nn.Module)` with `__init__(self, vocab_size, max_len)` and a CAUSAL `forward(x [B,T]) -> logits [B,T,V]`
(position t may depend only on x[:, :t+1]; this is checked by perturbation before training).
Fitness = validation bits per character at the training context (lower is better); also reported at 2x context.
Usage: python3 -I harness.py CAND.py [--out RESULT.json] [--steps N] [--seed S]
"""
import argparse, json, math, os, time
import torch, torch.nn as nn, torch.nn.functional as F

HERE = os.path.dirname(os.path.abspath(__file__))
CHARS = "\n" + "".join(chr(i) for i in range(32, 127)); VOCAB = len(CHARS)   # 96
T_TRAIN, BS, MAXLEN = 128, 16, 512
PARAM_BUDGET = 150_000


def load(split):
    t = open(os.path.join(HERE, "data", split + ".txt")).read(); idx = {c: i for i, c in enumerate(CHARS)}
    return torch.tensor([idx[c] for c in t], dtype=torch.long)


def get_batch(data, T, bs, g):
    ix = torch.randint(len(data) - T - 1, (bs,), generator=g)
    x = torch.stack([data[i:i + T] for i in ix]); y = torch.stack([data[i + 1:i + T + 1] for i in ix])
    return x, y


def load_model(path):
    ns = {"torch": torch, "nn": nn, "F": F, "math": math, "__name__": "candidate"}
    exec(compile(open(path).read(), path, "exec"), ns)
    return ns["Model"](VOCAB, MAXLEN)


@torch.no_grad()
def causal_check(model, g):
    model.eval(); x = torch.randint(VOCAB, (2, 64), generator=g); base = model(x)
    for t0 in (0, 21, 62):
        x2 = x.clone(); x2[:, t0 + 1:] = torch.randint(VOCAB, x2[:, t0 + 1:].shape, generator=g)
        if (model(x2)[:, :t0 + 1] - base[:, :t0 + 1]).abs().max().item() > 1e-4:
            raise ValueError(f"non-causal: output at <= {t0} depends on later input")
    model.train()


@torch.no_grad()
def bpc(model, data, T, n=24, bs=16):
    model.eval(); tot = 0.0; cnt = 0
    starts = torch.linspace(0, len(data) - T - 2, n * bs).long()
    for k in range(n):
        s = starts[k * bs:(k + 1) * bs]
        x = torch.stack([data[i:i + T] for i in s]); y = torch.stack([data[i + 1:i + T + 1] for i in s])
        tot += F.cross_entropy(model(x).reshape(-1, VOCAB), y.reshape(-1), reduction="sum").item(); cnt += y.numel()
    model.train(); return tot / cnt / math.log(2)


def run(path, steps=3000, seed=0, lr=3e-3, time_cap=480):
    torch.manual_seed(seed); torch.set_num_threads(int(os.environ.get("THREADS", "1")))
    g = torch.Generator().manual_seed(seed); res = {"cand": os.path.basename(path), "seed": seed, "steps": steps}
    try:
        tr, va = load("train"), load("val"); model = load_model(path)
        npar = sum(p.numel() for p in model.parameters() if p.requires_grad); res["params"] = npar
        if npar > PARAM_BUDGET: raise ValueError(f"{npar} params > budget {PARAM_BUDGET}")
        x, _ = get_batch(tr, T_TRAIN, 2, g); out = model(x)
        if out.shape != (2, T_TRAIN, VOCAB): raise ValueError(f"bad output shape {tuple(out.shape)}")
        causal_check(model, g)
        opt = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=0.01)
        sched = torch.optim.lr_scheduler.OneCycleLR(opt, max_lr=lr, total_steps=steps, pct_start=0.1)
        t0 = time.time()
        for s in range(steps):
            x, y = get_batch(tr, T_TRAIN, BS, g)
            loss = F.cross_entropy(model(x).reshape(-1, VOCAB), y.reshape(-1))
            if not torch.isfinite(loss): raise ValueError(f"non-finite loss at step {s}")
            opt.zero_grad(); loss.backward(); torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0); opt.step(); sched.step()
            if time.time() - t0 > time_cap: raise TimeoutError(f"training exceeded {time_cap}s at step {s}")
        res["train_s"] = round(time.time() - t0, 1); res["train_bpc"] = round(loss.item() / math.log(2), 4)
        causal_check(model, g)
        res["bpc"] = round(bpc(model, va, T_TRAIN), 4); res["bpc_2x"] = round(bpc(model, va, 2 * T_TRAIN, n=12), 4)
        res["fitness"] = res["bpc"]
    except Exception as e:
        res["error"] = f"{type(e).__name__}: {e}"[:400]; res["fitness"] = 99.0
    return res


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("cand"); ap.add_argument("--out"); ap.add_argument("--steps", type=int, default=3000)
    ap.add_argument("--seed", type=int, default=0); a = ap.parse_args()
    r = run(a.cand, a.steps, a.seed); s = json.dumps(r, indent=1)
    if a.out: open(a.out, "w").write(s)
    print(s)
