"""Idea 3 - Self-charging frost separator cascade. All estimates in code.
Sources (see LOG.md):
 [A] Gauss limit of surface charge: sigma_max = eps0 * E_breakdown (3 MV/m, sea-level air) -> 26.6 uC/m2.
 [B] Free-fall tribo separators treat 0.1-2 mm grains; too fine grains stick to electrodes (Springer BHM review, s00501-016-0515-1).
 [C] Feldspar/quartz free-fall tribo separation works only after preheating feed >100 C (Peretti & Zucca, CNR/Univ. Cagliari)
     -> surface water film is the controlling variable.
 [D] Industrial tribo belt separators (STET): calcite/quartz, talc/magnesite, barite/quartz, fly ash (Bittner et al. 2014).
 [E] Mekhanobr-Tekhnika separator: dielectric drum charged by friction against a brush makes the field, but particles
     are still pre-charged by an HV source (rudmet.ru 30164) -> closest known 'self-charged field' work.
 [F] Saturation vapour pressure over ice (Murphy & Koop 2005 formula).
ASSUME flags mark assumptions.
"""
import math
eps0 = 8.854e-12
g = 9.81

print("== Round 1: how much charge can a grain carry, and how far does it drift? ==")
sigma_max = eps0 * 3e6
rho = 2700.0
for d_um in (100, 200, 400, 800):
    d = d_um * 1e-6
    qm_max = 6 * sigma_max / (rho * d)  # C/kg
    print(f"d={d_um} um: Gauss-limit q/m = {qm_max*1e6:6.0f} uC/kg; at 5% of limit {0.05*qm_max*1e6:5.1f} uC/kg")

# drift under drag (Schiller-Naumann), air at -40 C
mu, rho_a = 1.52e-5, 1.51
def fall(d, qm, E, h, dt=1e-4):
    m = rho * math.pi * d**3 / 6
    x = y = vx = vy = 0.0
    t = 0.0
    while y < h:
        v = math.hypot(vx, vy) + 1e-12
        Re = rho_a * v * d / mu
        Cd = 24 / max(Re, 1e-9) * (1 + 0.15 * Re**0.687)
        Fd = 0.5 * rho_a * Cd * math.pi * d**2 / 4 * v
        ax = qm * E - Fd * vx / m
        ay = g - Fd * vy / m
        vx += ax * dt; vy += ay * dt
        x += vx * dt; y += vy * dt; t += dt
    return x, t

for d_um in (150, 300, 600):
    d = d_um * 1e-6
    qm = 0.05 * 6 * sigma_max / (rho * d)
    for E in (2e5, 4e5):
        x, t = fall(d, qm, E, 1.5)
        print(f"d={d_um}um q/m={qm*1e6:5.1f} uC/kg E={E/1e5:.0f} kV/cm, 1.5 m plates: lateral drift {x*100:5.1f} cm in {t:.2f} s")

print("\n== Round 2: does the stage self-excite? charge supply vs leakage ==")
# per metre width of curtain
mdot = 1.0  # kg/s per m width (3.6 t/h/m) ASSUME typical free-fall loading
qm = 10e-6  # C/kg ASSUME (5 % of Gauss limit for ~300 um)
frac_sorted = 0.5  # fraction of charge that lands in the 'right' bin while the field is still low
I = mdot * qm * frac_sorted
C = 150e-12  # plate+bin capacitance per metre ASSUME
V_cap = 45e3  # 30 cm gap at 1.5 kV/cm
print(f"charging current {I*1e6:.1f} uA per m; time to {V_cap/1e3:.0f} kV with no leak {C*V_cap/I*1e3:.1f} ms")
for label, Rleak in (("temperate humid insulators (1e10 ohm)", 1e10), ("dry/clean 1e12", 1e12), ("-40 C frost-free 1e14", 1e14)):
    Vss = I * Rleak
    print(f"{label}: steady V = {min(Vss, 1e9)/1e3:,.0f} kV (cap {V_cap/1e3:.0f} kV) -> {'self-excites' if Vss > V_cap else 'does NOT reach field'}")

print("\n== Round 2b: the real leakage path is the GRAIN SURFACE (adsorbed water), controlled by RH at the grain surface ==")
def esat_ice(Tc):
    T = Tc + 273.15
    return math.exp(9.550426 - 5723.265 / T + 3.53068 * math.log(T) - 0.00728332 * T)  # Pa [F]
def esat_w(Tc):
    T = Tc + 273.15
    return 610.94 * math.exp(17.625 * Tc / (Tc + 243.04))
e_air = 0.9 * esat_ice(-40)
for Tore in (-40, -30, -20, -10, -5):
    rh = e_air / (esat_ice(Tore))
    print(f"ore surface {Tore:>4} C in -40 C air (90% RHi): effective RH at grain = {rh*100:5.1f}%")
e_temp = 0.5 * esat_w(20)
for Tpre in (60, 80, 100, 120):
    print(f"temperate plant: 20 C/50% air, feed preheated to {Tpre} C: RH at grain = {100*e_temp/esat_w(Tpre):4.1f}%")
# heating from comminution
for kwh in (5, 10, 15):
    dT = kwh * 3.6 / 0.8  # kJ/kg per kWh/t, cp 0.8 kJ/kgK
    print(f"dry grinding {kwh} kWh/t -> grain temperature rise up to {dT:.0f} K (if not removed)")

print("\nRepair: enclose the cascade and ventilate it with OUTDOOR -40 C air warmed by grinding-mill heat:")
for Tw in (-20, -10, 0, 10):
    print(f"  outdoor air (90% RHi at -40 C) warmed to {Tw:>3} C: RH = {100*e_air/esat_w(Tw) if Tw>=0 else 100*e_air/esat_ice(Tw):4.1f}%")
air_m3 = 10*3600/(1.3*40)
print(f"  air needed per t ore to carry 10 kWh/t of mill heat with 40 K rise: {air_m3:.0f} m3/t")
print("\n== Round 3: cascade - stages, recovery, height (spodumene pegmatite 1.2 -> 6 % Li2O) ==")
def cascade(feed_grade, target, Sv, Sg, recycle=True, max_stages=30):
    # each stage sends fraction Sv of valuable and Sg of gangue to concentrate; tails of stage k>1 recycled to stage k-1 feed
    # solve steady state by iteration
    n = 1
    while n <= max_stages:
        Fv = [0.0] * n; Fg = [0.0] * n
        for _ in range(400):
            Cv = [0.0] * n; Cg = [0.0] * n; Tv = [0.0] * n; Tg = [0.0] * n
            newFv = [0.0] * n; newFg = [0.0] * n
            newFv[0] += feed_grade; newFg[0] += 1 - feed_grade
            for k in range(n):
                Cv[k] = Sv * Fv[k]; Cg[k] = Sg * Fg[k]
                Tv[k] = Fv[k] - Cv[k]; Tg[k] = Fg[k] - Cg[k]
                if k + 1 < n:
                    newFv[k + 1] += Cv[k]; newFg[k + 1] += Cg[k]
                if recycle and k > 0:
                    newFv[k - 1] += Tv[k]; newFg[k - 1] += Tg[k]
            Fv, Fg = newFv, newFg
        grade = Cv[-1] / (Cv[-1] + Cg[-1])
        rec = Cv[-1] / feed_grade
        load = sum(Fv) + sum(Fg)
        if grade >= target:
            return n, grade, rec, load, (Cv[-1] + Cg[-1])
        n += 1
    return None

feed = 0.012 / 0.075  # spodumene mass fraction (pure spodumene ~7.5-8 % Li2O)
target = 0.06 / 0.075
for Sv, Sg in ((0.85, 0.45), (0.80, 0.50), (0.75, 0.55), (0.70, 0.60)):
    res = cascade(feed, target, Sv, Sg)
    if res:
        n, gr, rec, load, mass = res
        print(f"stage split valuable {Sv:.2f}/gangue {Sg:.2f} (enrichment/stage {Sv/Sg:.2f}): {n} stages, grade {gr*7.5:.1f}% Li2O, "
              f"recovery {rec*100:.0f}%, circulating load {load:.1f}x feed, mass pull {mass*100:.1f}%")
    else:
        print(f"Sv={Sv} Sg={Sg}: target not reached in 30 stages")

print("\n== Round 4: cost per t ore vs (a) hauling raw ore (b) Arctic flotation plant ==")
ore_t = 300e3  # t/yr ore ASSUME small pegmatite / rare-metal mine
season_h = 150 * 24 * 0.85  # winter operation when air <= -25 C
tph = ore_t / season_h
n_st, load = 9, 7.2  # from Round 3 (Sv 0.85 / Sg 0.45)
width_per_stage = tph * load / n_st / 3.6  # m of curtain per stage at 3.6 t/h/m
stage_m_cost = 40e3  # $ per metre-wide stage (plates, liner, bins, frame, regulator, enclosure) ASSUME
lift_cost = 1.5e6    # conveyors returning middlings ASSUME
capex = n_st * width_per_stage * stage_m_cost + lift_cost
ann = capex * 0.15 + 0.5e6  # + crew/maintenance
grind = 12 * 0.33   # $/t ore: dry grinding 12 kWh/t on diesel power at 0.33 $/kWh (needed by both routes)
sep = ann / ore_t
print(f"{tph:.0f} t/h, {width_per_stage:.1f} m per stage x {n_st} stages, capex ${capex/1e6:.1f}M -> separation {sep:.2f} $/t ore; grinding {grind:.1f} $/t")
haul_km, rate = 700, 0.15  # ASSUME winter-road truck haul to rail/river port 0.10-0.20 $/t.km
mass_pull = 0.16
dry = grind + sep + mass_pull * haul_km * rate
haul_raw = haul_km * rate
flot = 25.0 + mass_pull * 1.08 * haul_km * rate  # ASSUME Arctic flotation opex+capex ~$20-30/t ore (heated plant, water, TSF); conc moisture 8 %
print(f"dry cascade + haul concentrate: {dry:.1f} $/t ore | haul raw ore: {haul_raw:.1f} $/t ore -> {haul_raw/dry:.1f}x | Arctic flotation + haul: {flot:.1f} -> {flot/dry:.1f}x")
recov_penalty = 0.10  # cascade recovery ~75-80 % vs flotation ~85-88 %
print(f"recovery penalty ~{recov_penalty*100:.0f} % of value: at 1.2% Li2O ore x 7.5% Li2O-spod. conc ~ $900/t conc (6%) -> ore value ~${0.16*0.8*900:.0f}/t; penalty ${0.16*900*recov_penalty:.0f}/t ore")
