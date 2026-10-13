"""Reality for the architecture engine: a fixed, equal training+evaluation run for any candidate sequence model.

A candidate is a Python file that defines `class Model(nn.Module)` with `__init__(self, vocab_size, max_len)` and
`forward(x: LongTensor[B, T]) -> FloatTensor[B, T, vocab_size]` (logits for every position; the model sees the whole
input, answers sit at BLANK positions, so any architecture - causal or not - is fair).
Four capability tasks, each trained at short lengths and tested in-distribution (ID) and at 2x length (OOD):
  mqar   multi-query associative recall: k1 v1 ... kn vn | q1 _ q2 _      (content-addressable lookup)
  copy   a1 ... an | _ ... _                                               (exact position-faithful copy)
  parity b1 ... bn | _                                                     (a flipping state; length generalisation)
  hop    a1 b1 ... an bn | x _  -> f(f(x))                                 (two-step composition)
Score per task = max(0, (acc - chance) / (1 - chance)); fitness = mean over tasks of (ID + OOD) / 2.
Usage: python3 -I harness.py CAND.py [--out RESULT.json] [--steps 1000] [--seed 0]
"""
import argparse, json, math, os, sys, time
import torch, torch.nn as nn, torch.nn.functional as F

PAD, SEP, BLANK = 0, 1, 2
TASKS = ["mqar", "copy", "parity", "hop"]
TOK = {t: 3 + i for i, t in enumerate(TASKS)}     # task marker tokens 3..6
S0, NSYM = 8, 24                                  # symbol tokens 8..31
VOCAB = S0 + NSYM
MAXLEN = 72
PARAM_BUDGET = 120_000
ID_N = {"mqar": 8, "copy": 8, "parity": 12, "hop": 8}   # max size seen in training; OOD = 2x
CHANCE = {"mqar": 1 / NSYM, "copy": 1 / NSYM, "parity": 0.5, "hop": 1 / 8}


def sample(task, n, g):
    """One example of size n: (input tokens, target tokens with -100 except at blanks)."""
    r = lambda k: int(torch.randint(k, (1,), generator=g))
    if task == "mqar":
        keys = torch.randperm(NSYM, generator=g)[:n].tolist(); vals = [r(NSYM) for _ in range(n)]
        x = [TOK[task]]; [x.extend([S0 + k, S0 + v]) for k, v in zip(keys, vals)]; x.append(SEP)
        y = [-100] * len(x); m = max(1, n // 2)
        for i in torch.randperm(n, generator=g)[:m].tolist():
            x += [S0 + keys[i], BLANK]; y += [-100, S0 + vals[i]]
    elif task == "copy":
        a = [S0 + r(NSYM) for _ in range(n)]
        x = [TOK[task]] + a + [SEP] + [BLANK] * n; y = [-100] * (n + 2) + a
    elif task == "parity":
        b = [r(2) for _ in range(n)]
        x = [TOK[task]] + [S0 + v for v in b] + [SEP, BLANK]; y = [-100] * (n + 2) + [S0 + sum(b) % 2]
    elif task == "hop":
        dom = torch.randperm(NSYM, generator=g)[:n].tolist(); f = {}
        img = torch.randperm(n, generator=g).tolist()          # f maps the domain onto itself, so f(f(x)) exists
        for a, j in zip(dom, img): f[a] = dom[j]
        x = [TOK[task]]; [x.extend([S0 + a, S0 + f[a]]) for a in dom]
        q = dom[r(n)]; x += [SEP, S0 + q, BLANK]; y = [-100] * (len(x) - 1) + [S0 + f[f[q]]]
    return x, y


def batch(task_list, nmax, bs, g, exact=False):
    xs, ys = [], []
    for _ in range(bs):
        t = task_list[int(torch.randint(len(task_list), (1,), generator=g))]
        n = nmax[t] if exact else 2 + int(torch.randint(nmax[t] - 1, (1,), generator=g))
        x, y = sample(t, n, g); xs.append(x); ys.append(y)
    T = max(map(len, xs))
    X = torch.full((bs, T), PAD, dtype=torch.long); Y = torch.full((bs, T), -100, dtype=torch.long)
    for i, (x, y) in enumerate(zip(xs, ys)):
        X[i, :len(x)] = torch.tensor(x); Y[i, :len(y)] = torch.tensor(y)
    return X, Y


def load_model(path):
    ns = {"torch": torch, "nn": nn, "F": F, "math": math, "__name__": "candidate"}
    exec(compile(open(path).read(), path, "exec"), ns)
    if "Model" not in ns: raise ValueError("candidate defines no class Model")
    return ns["Model"](VOCAB, MAXLEN)


@torch.no_grad()
def evaluate(model, task, n, g, reps=8, bs=64):
    model.eval(); ok = tot = 0
    for _ in range(reps):
        X, Y = batch([task], {task: n}, bs, g, exact=True)
        P = model(X).argmax(-1); m = Y != -100
        ok += (P[m] == Y[m]).sum().item(); tot += m.sum().item()
    model.train(); acc = ok / tot
    return acc, max(0.0, (acc - CHANCE[task]) / (1 - CHANCE[task]))


def run(path, steps=3000, seed=0, bs=32, lr=3e-3, time_cap=420):
    torch.manual_seed(seed); torch.set_num_threads(int(os.environ.get("THREADS", "4")))
    g = torch.Generator().manual_seed(seed)
    res = {"cand": os.path.basename(path), "seed": seed, "steps": steps}
    try:
        model = load_model(path)
        npar = sum(p.numel() for p in model.parameters() if p.requires_grad); res["params"] = npar
        if npar > PARAM_BUDGET: raise ValueError(f"{npar} params > budget {PARAM_BUDGET}")
        X, Y = batch(TASKS, ID_N, 4, g)
        out = model(X)
        if out.shape != (X.shape[0], X.shape[1], VOCAB): raise ValueError(f"bad output shape {tuple(out.shape)}")
        opt = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=0.01)
        sched = torch.optim.lr_scheduler.OneCycleLR(opt, max_lr=lr, total_steps=steps, pct_start=0.1)
        t0 = time.time(); last = None
        for s in range(steps):
            X, Y = batch(TASKS, ID_N, bs, g)
            loss = F.cross_entropy(model(X).reshape(-1, VOCAB), Y.reshape(-1), ignore_index=-100)
            if not torch.isfinite(loss): raise ValueError(f"non-finite loss at step {s}")
            opt.zero_grad(); loss.backward(); torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0); opt.step(); sched.step()
            last = loss.item()
            if time.time() - t0 > time_cap: raise TimeoutError(f"training exceeded {time_cap}s at step {s}")
        res["train_s"] = round(time.time() - t0, 1); res["final_loss"] = round(last, 4)
        ge = torch.Generator().manual_seed(10_000 + seed); sc = {}
        for t in TASKS:
            a_id, s_id = evaluate(model, t, ID_N[t], ge); a_ood, s_ood = evaluate(model, t, 2 * ID_N[t], ge)
            sc[t] = {"id_acc": round(a_id, 3), "ood_acc": round(a_ood, 3), "id": round(s_id, 3), "ood": round(s_ood, 3)}
        res["tasks"] = sc
        res["fitness"] = round(sum((v["id"] + v["ood"]) / 2 for v in sc.values()) / len(sc), 4)
        res["cell"] = "".join(str(2 if v["ood"] >= 0.8 else 1 if v["id"] >= 0.8 else 0) for v in sc.values())
    except Exception as e:  # any failure is a measurement too
        res["error"] = f"{type(e).__name__}: {e}"[:400]; res["fitness"] = 0.0
    return res


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("cand"); ap.add_argument("--out"); ap.add_argument("--steps", type=int, default=3000)
    ap.add_argument("--seed", type=int, default=0); a = ap.parse_args()
    r = run(a.cand, a.steps, a.seed); s = json.dumps(r, indent=1)
    if a.out: open(a.out, "w").write(s)
    print(s)
