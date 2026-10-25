"""Check GPU model vs MLPerf Inference v6.1 (preview) DeepSeek-R1 Interactive, 72-GPU systems.
Measured (secondary reports): VR200 NVL72 652,750 tok/s; GB300 NVL72 253,506-260,098 tok/s (output tokens).
Interactive TPOT bound: assumed 16 ms p99 (5x the 80 ms Server bound) -> >=62.5 tok/s/user; mean speed higher.
Workload: ISL ~0.8K, OSL ~3.9K -> decode context ~2.8K; prefill blended at 0.2 prompt tok per output tok.
Usage: python3 calib5.py > calib5.txt"""
import model5 as m
meas = {"GB300": 257e3 / 72, "Rubin": 652750 / 72}
for name, s in (("GB300", m.SYS["GB300"]), ("Rubin", m.rubin(1.0)), ("Rubin s1.43", m.rubin(1.43))):
    key = name.split()[0]
    pre = 1 / m.comp_time(m.R1, s, 1, 61, 800)
    for tau in (20, 45, 90):
        for p in (0.7, 0.8):
            cells = []
            for tier in (62.5, 100, 150):
                e = m.envelope(lambda k: m.gpu_points(s, tau * 1e-6, 2800, k, p, M=m.R1), (tier,), ks=range(4))
                if tier not in e: cells.append(f">={tier}: --"); continue
                dec = e[tier][0] * s["P"]
                bl = 1 / (1 / dec + 0.2 / pre)
                cells.append(f">={tier}: {bl:7,.0f} = {bl/meas[key]:4.1f}x meas (k{e[tier][1]},m{e[tier][3][3][1]})")
            print(f"{name:<12} tau {tau:>2}us p{p}  " + "  ".join(cells))
    print()
print("measured tok/s/GPU:", {k: round(v) for k, v in meas.items()}, " ratio Rubin/GB300 = %.2f" % (meas["Rubin"] / meas["GB300"]))
for tau in (20, 45):
    r = {}
    for name, s in (("GB300", m.SYS["GB300"]), ("Rubin", m.rubin(1.0))):
        e = m.envelope(lambda k: m.gpu_points(s, tau * 1e-6, 2800, k, 0.8, M=m.R1), (62.5, 100), ks=range(4))
        r[name] = {t: e[t][0] * s["P"] for t in (62.5, 100)}
    print(f"model Rubin35/GB300 at tau {tau}: " + ", ".join(f">={t}: {r['Rubin'][t]/r['GB300'][t]:.2f}" for t in (62.5, 100)))
