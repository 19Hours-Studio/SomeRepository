"""Round-8 additions on top of round7/model7.py and round6/model5.py (both imported unchanged).

  * Per-class exposed per-layer latency tau can be set per system (tau_fn(f) -> seconds). Round 7 used
    tau(f) = 7 + 3/f us for every system (the 'symmetric' case, kept as the conservative bound).
  * 'Measured' case: GPU-class tau fitted so the model reproduces the measured V4-Pro interactivity wall
    (GB300 NVL72 ~165 tok/s/user on AgentX V4-Pro, NVIDIA blog); static-schedule class tau checked against
    Artificial Analysis speeds of LPX (Gemma 4 31B) and Cerebras (GLM-4.7, gpt-oss-120b).
  * Prefill energy per prompt token for end-to-end tok/MW (prefill is compute-bound on every system).
"""
import math, sys, os
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(H, "..", "round7")); sys.path.insert(0, os.path.join(H, "..", "round6"))
import model5 as m, model7 as q, run7 as r7

def tau_sym(f): return (7 + 3 / f) * 1e-6
def tau_gpu(t0):
    """GPU-class: t0 us at f0, of which 3 us scales with 1/f (same split as the symmetric law)."""
    return lambda f: (t0 - 3 + 3 / f) * 1e-6

def gpu_env_tau(profs, tau_fn, ctx=q.C128, p=0.8, M=m.V4, ks=range(8)):
    c = []
    for lab, s, f in profs:
        tau = tau_fn(f)
        c.append((lab, m.envelope(lambda k: m.gpu_points(s, tau, ctx, k, p, M=M), q.T, ks=ks)))
    return q.best_over(c)

def pipe_env_tau(profs, tau_fn, ctx=q.C128, p=0.8, M=m.V4, gs=(1, 2, 3, 4, 6)):
    c = []
    for lab, s, f in profs:
        tau = tau_fn(f)
        for g in gs:
            c.append((f"{lab} g{g}", m.envelope(lambda k: m.pipe_points(s, tau, ctx, k, p, M=M, gmin=g), q.T)))
    return q.best_over(c)

GB300 = dict(m.SYS["GB300"], imb=q.IMB_G, s=1.0, P_maxq=m.SYS["GB300"]["P"])
def gb300_prof(): return [("0.75V", GB300, 1.0)]

def prefill_J_per_tok(s, ctx, M=m.V4):
    """J per prompt token at the profile s (compute-bound, eta 0.6, imbalance, zero-skip as in decode),
    average attention context ctx/2, provisioned slot power, same 0.85 derate as decode."""
    t = m.comp_time(M, s, 1, M["L0"], ctx // 2)
    return t * s["P"] / m.DERATE
