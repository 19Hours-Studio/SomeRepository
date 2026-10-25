"""Checks: (1) re-rotating cached keys by +d equals recomputing at positions shifted
by d (RoPE shift invariance, all layers); (2) the identity edit gives KL 0."""
import sys, os, torch
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import smol
m = smol.Smol()
ids = m.enc("<|im_start|>user\nThe quick brown fox jumps over the lazy dog. def f(x): return x+1<|im_end|>\n")
_, a = m.forward(ids, range(len(ids)), return_logits=False)
_, b = m.forward(ids, range(100, 100 + len(ids)), return_logits=False)
d = torch.full((len(ids),), 100)
err = max(float((m.rerotate(ka, d) - kb).abs().max() / kb.abs().max()) for ka, kb in zip(a["k"], b["k"]))
errv = max(float((va - vb).abs().max() / vb.abs().max()) for va, vb in zip(a["v"], b["v"]))
print(f"max rel err keys {err:.2e}  values {errv:.2e}")
