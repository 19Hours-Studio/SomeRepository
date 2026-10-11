"""Smoke tests: python3 test_sieve.py (torch parts are skipped if torch is not installed)."""
import random
import numpy as np
from bitworld import build_pool, make_family, Stmt, X, Y
from lattice import Lattice


def test_lattice_sound():
    st, ed, tr = build_pool(80, seed=5)
    assert sum(1 for i, j in ed if tr[i] and not tr[j]) == 0, "implication edge violated"
    lat = Lattice(len(st), ed)
    for i in random.Random(0).sample(range(len(st)), 40): lat.observe(i, tr[i])
    lab = lat.label >= 0
    assert (lat.label[lab] == tr[lab]).all(), "propagation produced a wrong label"
    assert lab.sum() > 40, "propagation added no labels"


def test_verifier_and_cex():
    s = Stmt(("add", X, Y), ("or", X, Y))                  # x + y == x | y : false in general
    ok, c = s.verify(); assert not ok and s.is_cex(*c)
    assert Stmt(("add", X, Y), ("or", X, Y), pre="disjoint").verify()[0]   # true when x & y == 0
    assert Stmt(("xor", X, Y), ("sub", ("or", X, Y), ("and", X, Y))).verify()[0]


def test_acquire_prefers_informative():
    st, ed = make_family(random.Random(1), 0)
    lat = Lattice(len(st), ed); p = np.full(len(st), 0.5)
    pick = lat.acquire(p, 1, np.random.default_rng(0))
    assert pick[0] == 0, "with flat beliefs the seed (largest cone) should be checked first"


def test_model():
    try:
        import torch
    except ImportError:
        print("torch not installed: model test skipped"); return
    from model import build, batch_encode
    st, _, _ = build_pool(4, seed=2); m = build("tiny")
    o = m(batch_encode(st[:7], m.max_len))
    assert o["verdict"].shape == (7,) and o["witness"].shape == (7, 2, 8)
    o["verdict"].sum().backward()


if __name__ == "__main__":
    for f in [test_lattice_sound, test_verifier_and_cex, test_acquire_prefers_informative, test_model]:
        f(); print("ok", f.__name__)
    print("OK: sieve smoke tests passed")
