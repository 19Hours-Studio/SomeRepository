"""Idea 8 buoyancy budget, snow-pocket creep, and shell creep; Idea 5 lag feedback."""
import math

NET = 83.0
def eta(rho, T=0.0):
    return 7.62237e6 * (rho / 250.0) * math.exp(0.1 * (0 - T) + 0.023 * rho)

# pod: 8 t coal (flooded voids, bulk 0.85 t/m3) + 1.76 m3 snow, 1.2 m tall, shell 7-13 cm
for rho_coal in (1250, 1350, 1450):
    excess = 8000 * (1 - 1000 / rho_coal)
    for t in (0.07, 0.13):
        interior = 8 / 0.85 + 1.76
        hin = 1.2 - 2 * t
        foot = interior / hin
        W = 2.2
        Lp = foot / W
        A = 2 * ((W + 2 * t) * (Lp + 2 * t)) + 2 * 1.2 * ((W + 2 * t) + (Lp + 2 * t))
        shell_lift = A * t * NET
        need = excess - shell_lift
        rho_snow_max = 1000 - need / 1.76
        print(f"coal {rho_coal}: excess {excess:.0f} kg; shell {t} m area {A:.0f} m2 lift {shell_lift:.0f} kg; "
              f"snow must give {need:.0f} kg -> snow density <= {rho_snow_max:.0f} kg/m3")

print("\nSnow-pocket creep buoyancy loss (1.76 m3), stress = hydrostatic 13-20 kPa")
for rho in (150, 250, 300, 350, 450, 550):
    for sig in (13e3, 20e3):
        rate = sig / eta(rho)  # 1/s volumetric (linear viscous approx)
        loss = 1.76 * rate * 86400 * 1000
        print(f"rho {rho}: sigma {sig/1e3:.0f} kPa -> {rate*86400*100:.2f} %/day -> {min(loss, 1.76*(1000-rho)):.0f} kg/day buoyancy loss")

print("\nIce shell flexural creep (Glen n=3, A=2.4e-24 at 0 C), span 1.0-1.2 m, dp 15 kPa")
for t in (0.07, 0.10, 0.13):
    for b in (1.0, 1.2):
        sig = 0.5 * 15e3 * (b / t) ** 2
        rate = 2.4e-24 * sig ** 3
        print(f"t={t} span={b}: bending stress {sig/1e6:.2f} MPa -> creep {rate*86400*100:.1f} %/day")

print("\nIdea 5 lag feedback: rate halves per 1 mm of dry lag, 80% of freed material stays as lag, raked once a day")
for wq in (0.4, 0.7):
    for pore in (0.15,):
        free0 = wq * 1.09 / pore  # mm/day bare
        # dL/dt = 0.8*free0*2^-L  -> 2^L = 1 + 0.8*free0*ln2*t
        L = math.log2(1 + 0.8 * free0 * math.log(2) * 1.0)
        freed = L / 0.8
        print(f"{wq} mm w.e./d: bare {free0:.1f} mm/d, with lag over 1 day {freed:.1f} mm/d ({100*freed/free0:.0f}%)")
