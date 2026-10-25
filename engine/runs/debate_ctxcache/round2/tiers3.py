# Own-stack tool-gap holding, ONE pricing basis (rental): HBM $2/h per 80 GB, DRAM $0.005/GB-h.
# Per turn choose pin (HBM) / swap (DRAM + reload over PCIe 50 GB/s, stall charged at full GPU $/s if not hidden
# behind the prefill of the new tokens) / discard (recompute prefix). 'min' = InferCept-style per-turn choice.
import replay3 as R
GPU_S = R.GPU_S; KVB = R.KVB
HBM_GBS, DRAM_GBS = 2 / 80 / 3600, 0.005 / 3600
def turn_costs(L, new, gap):
    pre, dec, _ = R.own_cost(L, L - new, 0, 300, 0)
    gb = (L - new) * KVB / 1e9
    pin = gb * HBM_GBS * gap
    reload = gb / 50; t_pre = pre / GPU_S
    swap = gb * DRAM_GBS * gap + max(0, reload - t_pre) * GPU_S
    disc = R.own_cost(L, 0, 0, 300, 0)[0] - pre            # extra prefill to recompute the prefix
    return pre + dec, dict(pin=pin, swap=swap, discard=disc)
for gap in (5, 30, 120, 600):
    tot = {k: 0.0 for k in ("pin", "swap", "discard", "min")}; base = 0
    for t in range(1, 50):
        L = 10_000 + t * 2300 + (t // 5) * 200
        b, c = turn_costs(L, 2300, gap); base += b
        for k in c: tot[k] += c[k]
        tot["min"] += min(c.values())
    s = {k: base + v for k, v in tot.items()}
    print(f"gap {gap:4d}s: pin ${s['pin']:.3f} swap ${s['swap']:.3f} discard ${s['discard']:.3f} min ${s['min']:.3f}"
          f" | swap vs pin {s['pin']/s['swap']:.2f}x, swap vs min(pin,discard) {min(s['pin'],s['discard'])/s['swap']:.2f}x")
print(f"reload stall check: L=120k reload {120e3*KVB/1e9/50:.2f}s vs prefill of 2.3k new tokens "
      f"{R.own_cost(120_000, 117_700, 0, 300, 0)[0]/GPU_S:.2f}s")
