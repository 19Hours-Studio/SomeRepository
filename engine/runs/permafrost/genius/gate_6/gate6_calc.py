"""Gate 6 kill test: KILLER margin and CHAIN ratio for the 8 ideas.
Every decisive input carries a source tag (see SOURCES at the end).
Run: python3 -I gate6_calc.py
"""
import math
import numpy as np

R = 8.314
g = 9.81
USD_RUB = 84.0                      # ledger cross-cutting
out = []
def say(s=""):
    print(s); out.append(s)

# ------------------------------------------------------------------
# Shared: Ni(CO)4 thermochemistry and vapour pressure
# ------------------------------------------------------------------
dH = -160.8e3          # J/mol, Ni(s)+4CO -> Ni(CO)4(g)   [S1 TAMU, NIST-type data]
dS = -409.5            # J/mol/K                          [S1]
def K(T):              # bar^-3
    return math.exp(-(dH - T * dS) / (R * T))
p20 = 315 * 133.322    # Pa at 20 C                       [S2 NIOSH]
Tb = 316.15            # 43 C normal boiling point         [S2]
dHv_R = math.log(101325 / p20) / (1 / 293.15 - 1 / Tb)
def psat(T):
    return p20 * math.exp(-dHv_R * (1 / T - 1 / 293.15))
Vm = 0.024055          # m3/mol, 20 C / 101.325 kPa (Russian standard m3)
Qgas = 38e9            # m3/yr Power of Siberia           [S3]
P = 9.8e6              # Pa                                [S3]
ngas = Qgas / Vm
M_Ni, M_CO = 58.693, 28.010

say("=" * 72); say("IDEA 1  repaired carbonyl Ni in Power of Siberia (25 kt/yr)")
x_ni, x_co = 2.7e-4, 3.5e-4
ni_t = ngas * x_ni * M_Ni / 1e6
p_ni = x_ni * P / 1e5; p_co = x_co * P / 1e5        # bar
T45 = 318.15
pco_req = (p_ni / K(T45)) ** 0.25
say(f"Ni carried {ni_t/1e3:.1f} kt/yr; dHvap={dHv_R*R/1e3:.1f} kJ/mol; "
    f"sat. ratio at -10C = {x_ni*P/psat(263.15):.2f}")
say(f"K(45C)={K(T45):.3g} bar^-3; CO required {pco_req/(P/1e5)*100:.4f} mol% "
    f"vs supplied {x_co*100:.3f} mol% -> MARGIN {p_co/pco_req:.2f}")
# temperature at which 0.035% CO stops being enough
Kneed = p_ni / p_co ** 4
Tmax = -dH / (R * math.log(Kneed) - dS)
say(f"0.035% CO is enough up to {Tmax-273.15:.0f} C (cap is 45 C)")
co_per_ni = (4 + x_co / x_ni) * M_CO / M_Ni
say(f"CO lost per t Ni = {co_per_ni:.2f} t (idea: 2.53 t, ~$514/t Ni -> ${514/2.53:.0f}/t CO)")
# CHAIN (per t contained Ni; payability loss counted as a cost, as the idea does)
Ni_price = 17000                     # $/t, LME Aug 2026        [S4]
U = 3900                             # mine-site C1 incl. truck to rail [S5]
T_toll = 2220                        # toll-option rail/port/TC costs   [S5]
L = 0.275 * Ni_price                 # 70-75 % payability (idea)
chain_idea = 7500                    # idea's own whole carbonyl+pipeline chain $6.6-8.4k
rail_alt = chain_idea - 960 + 27     # same refinery at BAM/PoS junction + rail pellets (idea)
now_conc = U + T_toll + L
now_rail = U + rail_alt
with1 = U + chain_idea
best_now = min(now_conc, now_rail)
say(f"now: sell concentrate {now_conc:,.0f}; refinery+rail {now_rail:,.0f}; "
    f"with idea {with1:,.0f} $/t Ni -> RATIO {best_now/with1:.2f}")
# check the $27 rail figure: Tynda->Svobodny ~580 km at ~3.9 rub/t-km (assumed tariff)
say(f"rail check 580 km x 3.9 rub/t-km = ${580*3.9/USD_RUB:.0f}/t")

say("=" * 72); say("IDEA 3  original carbonyl Ni in gas line (0.1 mol%, ~100 kt/yr)")
x3 = 1e-3
ni3 = ngas * x3 * M_Ni / 1e6
say(f"Ni carried {ni3/1e3:.1f} kt/yr; ideal sat. ratio at -10C {x3*P/psat(263.15):.2f}, "
    f"at -15C {x3*P/psat(258.15):.2f}")
p3 = x3 * P / 1e5
for Tc in (50, 80):
    req = (p3 / K(Tc + 273.15)) ** 0.25 / (P / 1e5) * 100
    say(f"  CO to stabilise at {Tc} C: {req:.3f} mol%")
kun_payable_lom, kun_life = 627e3, 19      # t payable Ni, years (2022 TEO) [S6]
kun_rate = kun_payable_lom / kun_life
say(f"largest Ni deposit near PoS/BAM corridor (Kun-Manie, 338 km road to BAM) "
    f"{kun_rate/1e3:.1f} kt/yr vs 100 kt/yr needed -> MARGIN {kun_rate/100e3:.2f}")
# CHAIN: refining is available to both routes; the pipeline only replaces pellet freight
co3 = 5.5 * M_CO / M_Ni                    # 4 bound + ~1.5 stabiliser (0.15 %)
co_cost = co3 * 203                        # $/t CO implied by idea 1
heat_net = 423e6 * 0.10 * 3.156e7 / 1e9    # GJ/yr, 90 % recuperation of 423 MW (idea 1)
heat_cost = heat_net * 2.0 / 100e3         # $2/GJ domestic gas, per t Ni at 100 kt
pipe_leg = co_cost + heat_cost + 50        # + bed/absorber capital charge (assumed)
freight_saved = 70                         # pellets by rail to port, ~1,500 km
R_ref = chain_idea - 960                   # carbonyl refinery cost implied by idea 1
base3 = U + R_ref + freight_saved
with3 = U + R_ref + pipe_leg
say(f"CO {co3:.2f} t/t Ni = ${co_cost:.0f}; bed heat ${heat_cost:.0f}; pipeline leg "
    f"${pipe_leg:.0f} vs freight saved ${freight_saved} -> now {base3:,.0f}, with "
    f"{with3:,.0f}, RATIO {base3/with3:.2f}")

# ------------------------------------------------------------------
say("=" * 72); say("IDEA 2  jacked frozen-block stripping")
W = 8000e3 * g                                  # N, block weight (idea)
area = 20 * 20
h_blk = 8000 / (area * 1.9)                     # m, at 1.9 t/m3 frozen overburden
mu = math.tan(math.radians(35))                 # loose sandy gravel phi 35 deg [S7]
F_req = mu * W
Raf = 0.20e6                                    # Pa, design adfreeze shear, sand, -2 C [S8]
F_av = area * Raf                               # next block's frozen base in shear
say(f"block h={h_blk:.1f} m; push needed {F_req/1e6:.0f} MN (mu={mu:.2f}); reaction of next "
    f"frozen block {F_av/1e6:.0f} MN -> MARGIN {F_av/F_req:.2f}")
side = 3 * 20 * h_blk * Raf
say(f"  if kerfs refreeze: need {(F_req+side)/1e6:.0f} MN vs {(F_av+side)/1e6:.0f} MN -> "
    f"{(F_av+side)/(F_req+side):.2f}")
# kerf energy -> diesel per m3
w = 0.25                                        # kerf width, m (assumed)
kerf_vol = 40 * h_blk * w                       # two shared 20 m sides per block
Lv = 0.40 * 917 * 334e3 + 2.0e6 * 4             # J/m3: 40 % ice + warm from -4 C
E = kerf_vol * Lv / 0.7                         # 70 % heater+drill efficiency
diesel = E / 36e6 / (area * h_blk)              # 36 MJ/l
say(f"kerf thaw diesel {diesel:.2f} l/m3 (claim 0.1; current ~1)")
# CHAIN, archetype A
A_now = 2550.0
phys = 1 - 0.22
earth = phys * 2 / 3 * A_now                    # ledger: earthmoving ~2/3 physically
ob_share = 0.875 / (0.875 + 0.125 * 1.5)        # 10.5 m OB : 1.5 m sands, sands 1.5x cost/m3
ob_cost = earth * ob_share
m3_per_oz = 11 * 31.1035 / 1.0                  # 11 l/g at ~1 l/m3
c_now = ob_cost / (m3_per_oz * 0.875)
hole_m_per_m3 = (40 / 0.2) * h_blk / (area * h_blk)   # holes every 0.2 m
c_idea = diesel * 1.64 + hole_m_per_m3 * 30 / 30 + 0.20 + 1020 / (area * h_blk) + 0.10
# fuel $1.64/l (ledger) | drilling 30 m/h per $30/h post | rigs | jacking $1,020/block | pumps
save = ob_cost * (1 - c_idea / c_now)
A_with = A_now - save
say(f"OB now ${c_now:.2f}/m3, with idea ${c_idea:.2f}/m3; save ${save:.0f}/oz -> "
    f"${A_with:.0f}/oz, RATIO {A_now/A_with:.2f} (10x claim would give "
    f"{A_now/(A_now-ob_cost*0.9):.2f})")

# ------------------------------------------------------------------
say("=" * 72); say("IDEA 4  snow-buoyed ice-shell pods (under-ice drift)")
rho_w = 1000.0
def winter_v():
    v_mean, Q_mean, Q_w, m = 0.6, 17773.0, 2000.0, 0.34   # [S9][S10][S11]
    return v_mean * (Q_w / Q_mean) ** m
v = winter_v()
say(f"winter depth-mean under-ice velocity (Lena, Q=2,000 m3/s) ~{v:.2f} m/s "
    f"= {v*86.4:.0f} km/day")
rho_ore, rho_snow, t_sh = 3.0, 0.25, 0.05       # [S12 snow 0.25 settled]
V_in = 1 / rho_ore + 1.0
a_in = V_in ** (1 / 3); a_out = a_in + 2 * t_sh
V_out = a_out ** 3; m_sh = (V_out - V_in) * 0.917
mass = 1.0 + rho_snow * 1.0 + m_sh
Nb = (V_out - mass) * 1000 * g                  # N, net buoyancy pressing on ice
mu_ii = 0.15                                    # lowest ice-on-ice value [S13]
D = 0.5 * rho_w * 1.05 * a_out ** 2 * v ** 2
say(f"pod {V_out:.2f} m3, net buoyancy {Nb/g:.0f} kg; friction {mu_ii*Nb:.0f} N vs drag "
    f"{D:.0f} N -> MARGIN {D/(mu_ii*Nb):.2f}")
cold = (m_sh * 2.1 * 30 + 1.0 * 0.8 * 30 + rho_snow * 2.1 * 30) * 1e6  # J, -30 C mean
say(f"cold content {cold/1e6:.0f} MJ -> freezes {cold/334e3:.0f} kg of water onto the pod "
    f"(bonds to the ice cover on contact)")
# chain, archetype B, 3 % Cu ore, pods replace truck haul, processing tolled downstream
B_now = 8500.0
ore_per_tCu = 1 / (0.03 * 0.9)
pod_cost = (0.25 * 30 + 3 + 1) * 1.10           # post-h x $30/h + equipment + moulds, 10 % lost
pods = ore_per_tCu * pod_cost
save_out = 0.05 * B_now
save_conc = 0.2 * (0.11 * 0.7 + 0.15 + 0.41 * 0.35) * B_now
B_with = B_now - save_out - save_conc + pods
say(f"pods ${pod_cost:.1f}/t ore x {ore_per_tCu:.0f} t = ${pods:.0f}/t Cu; savings "
    f"${save_out+save_conc:.0f} -> ${B_with:.0f}/t Cu, RATIO {B_now/B_with:.2f}")

# ------------------------------------------------------------------
say("=" * 72); say("IDEA 5  cold-brine chloride heap leach, gold carried in crude")
def rate_ratio(Ea, T1=243.15, T2=288.15):
    return math.exp(-Ea / R * (1 / T1 - 1 / T2))
for Ea in (15.65e3, 22.68e3, 34.4e3):           # [S14]
    say(f"  Ea {Ea/1e3:.1f} kJ/mol: k(-30C)/k(+15C) = {rate_ratio(Ea):.2f}")
say(f"KILLER (Ea 22.7, chemical control): MARGIN {rate_ratio(22.68e3):.2f}")
yr_gain = (5 + 7 * rate_ratio(22.68e3)) / 5
say(f"annual leach throughput vs 5-month seasonal heap: x{yr_gain:.2f}")
# chain, archetype A proxy: 1 g/t heap, 70 % recovery
t_ore_oz = 31.1035 / (1.0 * 0.70)
cacl2 = 0.10 * 0.29 * 1000                      # kg/t ore lost with 10 % retained brine [S15][S16]
cacl2_cost = cacl2 / 1000 * (150 + 150)         # $/t ore, $150/t CaCl2 + $150/t freight [S17]
cyan = 0.4 * 2.6 + 1.5 * 0.2 + 1.9 * 0.15       # $/t ore avoided: 0.4 kg NaCN, 1.5 kg lime + freight (assumed)
cl2_kwh = 5 * 2.7                               # 5 kg Cl2/t ore x 2.7 MWh/t
d_inb = (cacl2_cost - cyan) * t_ore_oz
d_en = cl2_kwh * 0.08 * t_ore_oz
d_proc = -0.30 * 0.20 * A_now                   # ADR/EW/gold room ~30 % of processing removed
d_out = -0.002 * A_now
A5 = A_now + d_inb + d_en + d_proc + d_out
say(f"CaCl2 top-up {cacl2:.0f} kg/t ore -> +${d_inb:.0f}/oz; Cl2 power +${d_en:.0f}; "
    f"ADR removed ${d_proc:.0f}; -> ${A5:.0f}/oz, RATIO {A_now/A5:.2f}")

# ------------------------------------------------------------------
say("=" * 72); say("IDEA 6  seasonal thermal-diode thaw (black film + snow fences)")
def run(nt, nf, years, T0=None, spin=False):
    dz = 0.05; z = np.arange(0, 30 + dz, dz); n = len(z)
    th = 0.30; Lv = th * 1000 * 334e3                    # J/m3 latent
    Cf, Ct, kf, kt = 1.9e6, 2.5e6, 2.2, 1.6
    dt = 900.0
    if T0 is None:
        T = np.full(n, -4.0)
    else:
        T = T0.copy()
    H = np.where(T < 0, Cf * T, Lv + Ct * T)
    steps = int(365 * 86400 / dt)
    maxthaw = []
    for yr in range(years):
        md = 0.0
        for s in range(steps):
            day = s * dt / 86400
            Ta = -11.5 + 26.5 * math.sin(2 * math.pi * (day - 105) / 365)   # [S18]
            Ts = nt * Ta if Ta > 0 else nf * Ta
            Tn = np.where(H < 0, H / Cf, np.where(H > Lv, (H - Lv) / Ct, 0.0))
            Tn[0] = Ts
            frac = np.clip(H / Lv, 0, 1)
            k = kf * (1 - frac) + kt * frac
            kh = 0.5 * (k[1:] + k[:-1])
            q = -kh * (Tn[1:] - Tn[:-1]) / dz
            dH = np.zeros(n)
            dH[1:-1] = -(q[1:] - q[:-1]) / dz * dt
            dH[-1] = (q[-1] + 0.05) / dz * dt        # 0.05 W/m2 geothermal
            H = H + dH
            H[0] = Cf * Ts if Ts < 0 else Lv + Ct * Ts
            if s % 96 == 0:
                thawed = np.where(H[1:] > 0.5 * Lv)[0]
                if len(thawed):
                    md = max(md, z[1:][thawed].max())
        maxthaw.append(md)
    Tn = np.where(H < 0, H / Cf, np.where(H > Lv, (H - Lv) / Ct, 0.0))
    return maxthaw, Tn, z
nat, Tspin, z = run(1.0, 0.6, 15)
say(f"natural (n_t 1.0, n_f 0.6): active layer {nat[-1]:.2f} m, T(15 m) {Tspin[300]:.1f} C")
trt, Tend, _ = run(2.0, 0.25, 5, T0=Tspin)
say("treated (n_t 2.0, n_f 0.25): max thaw depth by year " +
    ", ".join(f"{d:.1f} m" for d in trt))
need = 8.0                                        # typical shallow placer section [S19]
say(f"KILLER thaw depth after 3 yr {trt[2]:.1f} m vs {need} m -> MARGIN {trt[2]/need:.2f}")
# chain: removes the frozen-ground premium only on the thawed fraction
frozen_premium = 0.45                             # share of earthmoving cost due to frozen ground (assumed)
frac_thawed = min(1.0, trt[2] / need)
film = 1.0 * 0.5 + 0.2                            # $/m2/yr geotextile (3-season life) + fences (assumed)
area_per_oz = 1 / (need) * m3_per_oz              # m2 of deposit mined per oz
treat = film * area_per_oz * 3                    # 3 years ahead of mining
A6 = A_now - earth * frozen_premium * frac_thawed + treat
say(f"frac thawed {frac_thawed:.2f}; treatment ${treat:.0f}/oz -> ${A6:.0f}/oz, "
    f"RATIO {A_now/A6:.2f}")

# ------------------------------------------------------------------
say("=" * 72); say("IDEA 7  river-to-pole drift pods")
arrive = 0.20                                     # Laptev-shelf ice reaching Fram Strait [S20]
need7 = 0.90
say(f"arrival fraction {arrive:.2f} vs {need7:.2f} needed -> MARGIN {arrive/need7:.2f}")
tag = 420 + 16 * 36                               # tracker + 36 months airtime [S21]
ore_pod = 10.0                                    # t ore per pod (generous)
ore_per_tCu7 = 1 / (0.01 * 0.9)                   # 1 % Cu run-of-mine
tag_per_tCu = tag / ore_pod * ore_per_tCu7 / arrive
B7 = B_now * (1 - 0.05 - 0.11 * 0.5) + tag_per_tCu
say(f"tags alone ${tag}/pod -> ${tag_per_tCu:,.0f}/t Cu delivered; with idea >= ${B7:,.0f}/t Cu, "
    f"RATIO {B_now/B7:.2f}")

# ------------------------------------------------------------------
say("=" * 72); say("IDEA 8  ice-shell under-ice ore drift (sack + air bladder, warmed to 0 C)")
rho8 = 2.8
V_ore8 = 1 / rho8
V_air = 1 - V_ore8 + 0.03                          # bladder sized for ~3 % reserve (assumed)
V8 = V_ore8 + V_air + 0.25                         # + ice shell
a8 = V8 ** (1 / 3)
D8 = 0.5 * rho_w * 1.05 * a8 ** 2 * v ** 2
N_max = D8 / mu_ii                                 # buoyancy above which a package sticks
sig = math.hypot(1 / rho8 ** 2 * 0.10, 0.02 * (1 - 1 / rho8)) * 1000   # kg; sd rho 0.10, fill 2 %
from math import erf
Phi = lambda x: 0.5 * (1 + erf(x / math.sqrt(2)))
window = N_max / g
best = Phi((window / 2) / sig) - Phi((-window / 2) / sig)
say(f"drag {D8:.0f} N -> moving window 0..{window:.0f} kg net buoyancy; scatter sd {sig:.0f} kg; "
    f"best delivered fraction {best:.2f} vs 0.95 -> MARGIN {best/0.95:.2f}")
# chain, archetype A, 1.5 g/t ore [S22], 90 % recovery
t_oz8 = 31.1035 / (1.5 * 0.9)
pkg = (8 + 2) + 0.3 * 30 + 3                       # sack+bladder | 0.3 post-h | equipment
pkg = pkg / best                                    # pay for lost/stuck packages
save8 = (0.20 * 0.4 + 0.10 * 0.42 + 0.12 * 0.4 + 0.15 * 0.2 + 0.20 * 0.3) * A_now
A8 = A_now - save8 + pkg * t_oz8
say(f"package ${pkg:.1f}/t ore x {t_oz8:.0f} t/oz = ${pkg*t_oz8:.0f}/oz; plant/power savings "
    f"${save8:.0f}/oz -> ${A8:.0f}/oz, RATIO {A_now/A8:.2f}")

with open("gate6_results.txt", "w") as f:
    f.write("\n".join(out) + "\n")

# ------------------------------------------------------------------
# SOURCES (decisive inputs; ledger values are from TASK.md)
# S1  dH/dS Ni+4CO->Ni(CO)4: https://www.chem.tamu.edu/rgroup/hughbanks/courses/102H/lecturenotes/class2-2.pdf
# S2  Ni(CO)4 VP 315 mmHg @20C, bp 43C: https://www.cdc.gov/niosh/npg/npgd0444.html
# S3  Power of Siberia 38 bcm/yr, 9.8 MPa: https://biztrend.ru/en/sila-sibiri/26-our-projects/234-power-of-siberia.html
# S4  LME Ni ~$17,000/t Aug 2026: https://yieh.com/en/News/lme-nickel-prices-rebound-toward-17200/161850
# S5  Kun-Manie C1 split $3,900 + $2,220/t; AISC $9,890/t; 338 km road to BAM:
#     https://www.lse.co.uk/rns/AMC/projected-c1-nickel-costs-below-industry-average-79e2wuzfj0vxhah.html
#     https://www.miningweekly.com/article/amur-considering-two-production-options-for-kun-manie-2019-02-26
# S6  Kun-Manie 2022 TEO 627 kt payable Ni / 19 yr: https://www.investegate.co.uk/announcement/7112202
# S7  sandy gravel phi 33-40 deg, loose 35 deg: https://geotechdata.info/parameter/angle-of-friction
# S8  SNiP 2.02.04-88 Raf sand 0.20 MPa @-2C, 0.26 @-3C: https://dnaop.com/html/31372_5.html
# S9  Lena lower course 0.5-0.7 m/s: https://booksite.ru/fulltext/1/001/008/069/456.htm
# S10 Lena Kyusyur mean 17,773 m3/s: https://en.wikipedia.org/wiki/Lena_River
# S11 Lena Kusur Jan-Apr 1,378-2,814 m3/s: https://hess.copernicus.org/preprints/hess-2016-254/hess-2016-254.pdf
#     v~Q^m (Leopold & Maddock): https://www.usgs.gov/publications/hydraulic-geometry-stream-channels-and-some-physiographic-implications
# S12 settled snow ~0.25 g/cm3: https://roofonline.com/weight-of-snow
# S13 ice-on-ice friction 0.15-0.76: https://arxiv.org/pdf/1502.04173 ; hold-strengthening: https://www.poac.com/Papers/2013/pdf/POAC13_047.pdf
# S14 Au chloride leach Ea 15.65/22.68/34.4 kJ/mol: https://ijmse.iust.ac.ir/article-1-654-en.html
# S15 heap residual moisture 10 %: https://emrlibrary.gov.yk.ca/minerals/MajorMines/carmackscopper/supporting_docs2/heap_leach_facility_water_balance_1998Dec.pdf
# S16 CaCl2 eutectic 29.9 %: https://www.engineeringtoolbox.com/calcium-chloride-water-d_1186.html
# S17 CaCl2 RMB 900-1,100/t: https://www.guidechem.com/price/en/10043-52-4.html
# S18 Susuman MAAT -11.5C: https://en.wikipedia.org/wiki/Susuman ; July ~15C: https://www.weatherapi.com/history/july/q/susuman-2200905
#     n_t asphalt 1.4-2.3: https://www.owenscorning.com/dms/10023478 ; n_f to 0.17: https://permafrost.gi.alaska.edu/biblio/n-factor-nonsorted-circles-along-climate-gradient-arctic-alaska
# S19 frozen placers loose section to 15 m: https://zolotodb.ru/files/137.pdf
# S20 ~20 % of shelf ice completes Transpolar Drift, 2-3 yr: https://epic.awi.de/id/eprint/55542/1/PM_02042019_Transpolardrift_EN.pdf
# S21 tracker $419.95, airtime ~$16/month: https://www.sparkfun.com/products/19042
# S22 Magadan ore ~1.5 g/t: https://finance.mail.ru/article/na-kolyme-dobudut-poryadka-54-tonn-zolota-po-itogam-2024-goda-62630177/
