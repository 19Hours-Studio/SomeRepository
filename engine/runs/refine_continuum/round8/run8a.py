"""Round 8a: per-layer latency by machine class, from measured speeds. Usage: python3 run8a.py > run8a.txt"""
import model8 as e, model5 as m, model7 as q
print("== GPU class: model max tok/s/user (V4-Pro, p=0.8, best k<=3 i.e. MTP-depth as deployed) vs tau at f0")
print("   measured: GB300 NVL72 AgentX V4-Pro wall ~160-170 tok/s/user (Rubin 30x GB300 at 160, 2x at 110: NVIDIA);"
      " fastest public V4-Pro APIs 98-176 tok/s (Artificial Analysis), 280 (one secondary report)")
for ctx in (65536, q.C128):
    for t0 in (10, 20, 40, 60, 80, 100, 120, 150):
        g = e.gpu_env_tau(e.gb300_prof(), e.tau_gpu(t0), ctx=ctx, ks=range(4))
        r = e.gpu_env_tau(q.RUBIN_PROF(), e.tau_gpu(t0), ctx=ctx, ks=range(4))
        r7 = e.gpu_env_tau(q.RUBIN_PROF(), e.tau_gpu(t0), ctx=ctx, ks=range(8))
        print(f"  ctx {ctx//1024:4d}K tau0 {t0:4d} us: GB300 max {g['max']:6.0f} | Rubin max (k<=3) {r['max']:6.0f} (k<=7) {r7['max']:6.0f}")
print("\n== static-schedule class: implied per-layer step time from measured output speeds (Artificial Analysis)")
for name, spd, L in (("Groq 3 LPX, Gemma 4 31B, 100K ctx", 3431, 60), ("Cerebras, GLM-4.7 (355B MoE, multi-wafer)", 1008, 92),
                     ("Cerebras, gpt-oss-120b (high)", 1697, 36)):
    for acc in (1.0, 2.0, 2.5):
        print(f"  {name:<44} {spd:5d} tok/s, {L} layers, {acc:.1f} accepted/step -> {acc/(spd*L)*1e6:5.1f} us per layer-step")
print("  Continuum-7 at 0.55 V: tau = 7 + 3/0.635 = %.1f us + compute c (12.5 us at the bulk point)" % (e.tau_sym(0.635) * 1e6))
print("\n== GPU-class implied per-layer step time from measured walls (62 layers incl. MTP)")
for name, spd in (("GB300 V4-Pro wall", 165), ("fastest V4-Pro API (AA)", 176), ("secondary 280 tok/s report", 280)):
    for acc in (1.8, 2.5):
        print(f"  {name:<30} {spd:4d} tok/s/user, {acc} accepted/step -> {acc/(spd*62)*1e6:5.0f} us per layer-step")
