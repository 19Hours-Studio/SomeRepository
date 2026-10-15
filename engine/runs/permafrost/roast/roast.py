"""Point-by-point check of the external critique ("прожарка") of the permafrost run.

Every number the critique questions is recomputed here; inputs are named with their source.
Run: python3 roast.py > roast_out.txt
"""
import math

RHO_W, RHO_I = 1000.0, 917.0          # fresh water, ice, kg/m3
L_F = 334e3                           # latent heat of fusion, J/kg
G = 9.81
DAY = 86400.0


def hdr(s): print(f"\n== {s} ==")


# ---------------------------------------------------------------- 1. pod buoyancy
hdr("1a. Critique's case: 10 t ore (3000 kg/m3) floated by SOLID ice only")
m_ore, rho_ore = 10_000.0, 3000.0
v_ore = m_ore / rho_ore
w_net = m_ore - RHO_W * v_ore                     # weight in water, kg
lift_ice = RHO_W - RHO_I                          # 83 kg of lift per m3 of ice
m_ice = w_net / lift_ice * RHO_I
print(f"net weight in water {w_net:.0f} kg; ice needed {m_ice/1e3:.1f} t; pod {(m_ice+m_ore)/1e3:.1f} t; "
      f"payload {m_ore/(m_ice+m_ore):.0%}  -> the critique's arithmetic is right for solid ice")

hdr("1b. The repaired design: ore + packed SNOW (air) sealed in a liner, thin ice shell")
# box 5.0 x 2.2 x H, shell t_sh of ice; snow density rho_s; solve H for neutral buoyancy
for rho_s in (150, 250, 350):
    for t_sh in (0.08, 0.10):
        a, b = 5.0, 2.2
        # unknown H: total volume V = a*b*H; shell volume ~ area*t; snow fills the rest after ore
        for H in [x / 100 for x in range(60, 400)]:
            V = a * b * H
            area = 2 * (a * b + a * H + b * H)
            v_sh = area * t_sh
            v_s = V - v_ore - v_sh
            if v_s <= 0: continue
            mass = m_ore + v_sh * RHO_I + v_s * rho_s
            if mass <= RHO_W * V:            # neutral or positive
                break
        print(f"snow {rho_s} kg/m3, shell {t_sh*100:.0f} cm: H {H:.2f} m, volume {V:.1f} m3, pod {mass/1e3:.1f} t, "
              f"payload {m_ore/mass:.0%}, snow {v_s:.1f} m3, shell ice {v_sh*RHO_I/1e3:.1f} t")
print("-> with snow the pod is ~14-16 t, not 84 t; the air trapped in snow carries ~90% of the lift.")
print("   Condition: the snow must stay dry (sealed liner) while the shell is sprayed; soaked snow = critique's case.")

# ---------------------------------------------------------------- 1c. buoyancy DRIFT (not raised by the critique)
hdr("1c. Buoyancy drift from shell melt vs the +3..+9 kg trim window (10 t pod, ~40 m2 wetted)")
area = 40.0
nu, k_w, pr = 1.79e-6, 0.56, 13.4                 # water at 0 C
for u_rel in (0.04, 0.2):                        # pod lags the flow (0.8U) .. full under-ice velocity
    re = u_rel * 5.0 / nu
    nu_t = 0.037 * re ** 0.8 * pr ** (1 / 3)      # turbulent flat plate (river turbulence: use turbulent)
    h = nu_t * k_w / 5.0
    for dT in (0.005, 0.02, 0.1, 0.5, 2.0):
        melt = h * dT / (RHO_I * L_F)            # m/s
        dB = area * melt * DAY * lift_ice        # kg of lift lost per day
        days = 6.0 / dB                          # from +6 kg (mid-window) to 0
        print(f"u_rel {u_rel:.2f} m/s h {h:4.0f} W/m2K  water +{dT:<5} C: melt {melt*DAY*1e3:6.1f} mm/day, "
              f"lift loss {dB:7.1f} kg/day -> sinks after {days*24:6.1f} h ({days*0.16*86.4:6.1f} km at 0.16 m/s)")
print("Measured: Lena delta under ice -0.1..+0.8 C (Fedorova et al. 2020); below Krasnoyarsk HPP the Yenisei stays")
print("ice-free 200-300 km (warm release). So the trim window is used up in hours-days: the repaired pod sinks.")
shell_lift = 4.0 * lift_ice          # ~4 m3 of shell ice
snow_ice_lift = 1.6 * lift_ice       # ice skeleton of ~1.5 t snow
print(f"Total ice-derived lift that can melt away: shell {shell_lift:.0f} kg + snow skeleton {snow_ice_lift:.0f} kg "
      f"= {shell_lift+snow_ice_lift:.0f} kg; the trapped AIR (~6 t of lift) does not melt.")

hdr("1d. Repair: tolerate drift instead of trimming it away (window = drag / (mu g))")
for u in (0.16, 0.24):
    drag_pod = 0.5 * RHO_W * 1.0 * (2.2 * 1.2) * u ** 2
    for sail in (0, 20, 40):                     # drogue area m2, Cd ~1.2
        drag = drag_pod + 0.5 * RHO_W * 1.2 * sail * u ** 2
        for mu in (0.5, 0.1, 0.05):
            win = drag / (mu * G)
            ok = "covers full melt" if win >= shell_lift + snow_ice_lift else ""
            print(f"U {u} m/s drogue {sail:2d} m2 mu {mu:4}: drag {drag:5.0f} N -> window 0..{win:5.0f} kg {ok}")
print("-> a 40 m2 drogue + polymer skids (mu <= 0.1) gives a window wider than ALL melt-able lift (~460 kg):")
print("   start at +450 kg and the pod never leaves the window. Unknown: mu of polymer on 0 C river ice at")
print("   0.05-0.2 m/s (no data found; low-speed ice friction is non-monotonic), and diving under keels needs")
print("   drag > B*g -> keels must be handled by STRINGS (pods on a rope share the whole string's drag).")

# ---------------------------------------------------------------- 1e. throughput, ice volumes
hdr("1e. Throughput and ice/snow handled")
season_t, pod_t, days = 144_000, 10, 120
pods = season_t / pod_t
print(f"{pods:.0f} pods per season = {pods/days:.0f}/day (critique: right).")
print(f"solid-ice design: {pods*m_ice/1e9:.2f} Mt ice; snow design: ~{pods*(4.0*RHO_I+1.6*RHO_I)/1e9*1e3:.0f} kt of "
      f"shell+snow ice ({pods*7.6:.0f} m3 snow/season = {pods*7.6/days:.0f} m3/day)")
q_freeze = pods / days * 4.0 * RHO_I * L_F / DAY
print(f"heat to remove to freeze the shells: {q_freeze/1e6:.1f} MW (snowmaking-gun scale, free at -40 C air)")

# ---------------------------------------------------------------- 1f. pilot statistics
hdr("1f. Zero-loss pilot: 95% upper bound on loss probability")
for n in (20, 59, 299):
    print(f"n={n:3d}, 0 lost -> p < {1 - 0.05 ** (1 / n):.1%}")
print("-> critique right: 20 pods test the MECHANISM (stall, freeze-in, sinking), not industrial reliability.")
print("What loss rate is tolerable depends on cargo value (pod + cargo lost vs road saved, 700 km):")
road = {"winter road $0.117/t-km": 0.117 * 700, "critique's $0.14/t-km": 0.14 * 700}
for cargo, value in (("coal", 100), ("spodumene SC6", 900), ("Ni/Cu concentrate", 2500)):
    for name, cost in road.items():
        save = cost - 7.3
        print(f"  {cargo:18s} ${value:4d}/t vs {name}: saves ${save:5.1f}/t -> break-even loss {save/(value+save):5.1%}")
print("  vs summer barge ($0.025/t-km = $17.5/t at 700 km): saves ~$10/t -> break-even loss 9% coal, 1% SC6")

# ---------------------------------------------------------------- 2. tribo cascade
hdr("2a. Self-charging separator: energy and current")
qm, E, dx = 10e-6, 3e5, 0.30           # C/kg (5% of Gauss limit), V/m, lateral drift m
feed = 98 / 3.6                         # kg/s (98 t/h)
print(f"work done by the field per kg: {qm*E*dx:.2f} J/kg = {qm*E*dx*1e3/3.6e3:.2f} Wh/t "
      f"(grinding ~10 kWh/t = 36,000 J/kg)")
print(f"charging current {feed*qm*1e6:.0f} uA total; power at 45 kV {feed*qm*45e3:.0f} W")
print("-> critique right that kV != power, but separation needs FIELD, not power: the energy to deflect the grains")
print("   is ~1 J/kg, ~10^4x below grinding. Energy is not the bottleneck; charge CONTRAST between minerals is.")

hdr("2b. Space charge of the falling curtain (a real throughput limit)")
eps0 = 8.854e-12
for width in (1.0, 21.8):
    flow = feed / width                 # kg/s per metre of width
    c = flow / (0.5 * 3.0)              # kg/m3 in a 0.5 m deep curtain falling at 3 m/s
    e_sc = qm * c * 0.25 / eps0
    print(f"{width:4.1f} m wide: {flow:5.2f} kg/s/m, {c:5.2f} kg/m3, unipolar space-charge field {e_sc/1e5:6.1f} kV/cm")
print("-> at 1 m width the stream's own charge exceeds air breakdown (30 kV/cm); the researcher's 21.8 m wide stages")
print("   bring it to ~1-2 kV/cm, the same order as the applied 3 kV/cm, so throughput per metre is capped.")

hdr("2c. 'Humidity 90%' - which humidity")
def p_ice(t):  # Pa, Murphy & Koop 2005
    T = t + 273.15
    return math.exp(9.550426 - 5723.265 / T + 3.53068 * math.log(T) - 0.00728332 * T)
pv = 0.9 * p_ice(-40)
print(f"air at -40 C, 90% RH over ice: vapour pressure {pv:.1f} Pa, {pv*0.018/8.314/233.15*1e3:.3f} g/m3")
for tg in (-40, -20, 0):
    print(f"  grain surface at {tg:4d} C: relative humidity at the surface {pv/p_ice(tg):6.1%}")
print("-> it is RH at the grain surface (sets the adsorbed water film), not ore moisture. Ore moisture is a separate")
print("   problem: permafrost ore carries ice; pegmatite ~0.5% -> 5 kg/t to sublimate/evaporate ~14 MJ/t (4 kWh/t).")
print("   Unknown: surface conductivity at -40 C may be far below that at +20 C at equal RH, so the original")
print("   'cold keeps charge' claim is untested either way - a cold-room Faraday-cup measurement decides it.")

hdr("2d. Stage selectivity 0.85/0.45 - where from")
print("Not from data: no published tribo-separation of spodumene from quartz/feldspar was found (2024 IMPC search).")
print("Benchmarks that ARE published: DMS 0.6% -> 5.7% Li2O at ~90% recovery (Kazakh ore); sensor sorting rejects")
print("28-32% of mass at 84-94% Li2O recovery (dry, commercial, STEINERT at CBL Brazil).")
for sv, sg in ((0.85, 0.45), (0.80, 0.50), (0.75, 0.55)):
    print(f"  per-stage split valuable {sv} / gangue {sg}: enrichment per stage {sv/sg:.2f}")

# ---------------------------------------------------------------- 3. chain per kg Li2O recovered
hdr("3. Whole chain per kg of Li2O RECOVERED (700 km, 1.2% Li2O ore, mining $15/t ore in all cases)")
grade, mine = 0.012, 15.0
def chain(name, proc, rec, haul_per_t, conc_grade=0.06):
    pull = grade * rec / conc_grade
    cost = mine + proc + pull * haul_per_t
    kg = grade * rec * 1000
    return name, cost, kg, cost / kg, pull
for road_rate in (0.117, 0.14):
    wr = road_rate * 700
    rows = [
        chain("A raw ore by winter road, DMS at railhead", 12.0 + wr * (1 / (grade * 0.9 / 0.06)) * 0, 0.90, 0),
        chain("D DMS/flotation on site + conc by winter road", 25.0, 0.85, wr),
        chain("E DMS/flotation on site + conc by summer barge", 25.0, 0.85, 0.025 * 700),
        chain("D' DMS/flotation on site + conc by under-ice pods", 25.0, 0.85, 7.3),
        chain("B tribo cascade + conc by winter road", 10.34, 0.82, wr),
        chain("C tribo cascade + conc by under-ice pods", 10.34, 0.82, 7.3),
    ]
    # case A: all ore hauled
    a = rows[0]; rows[0] = (a[0], a[1] + wr, a[2], (a[1] + wr) / a[2], 1.0)
    print(f"-- winter road ${road_rate}/t-km")
    base = rows[1][3]
    for name, cost, kg, ckg, pull in rows:
        print(f"  {name:52s} ${cost:6.1f}/t ore, {kg:5.1f} kg Li2O, ${ckg:5.2f}/kg Li2O, {base/ckg:4.1f}x vs D")
print("Spodumene SC6 ~ $900/t = ~$15/kg Li2O, so every case is far below the price; the comparison is between cases.")
