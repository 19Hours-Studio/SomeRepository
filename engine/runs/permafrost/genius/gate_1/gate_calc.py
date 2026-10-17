#!/usr/bin/env python3
"""Gate-1 kill test: KILLER margin (available/required) and CHAIN ratio (now/with idea)
for the 8 ideas in TASK.md. Inputs are tagged [S#] (sourced) or [A] (assumption, chosen
to favour the idea). Sources are listed in SRC at the bottom."""
import math

RUB_USD = 84.0                 # [L] ledger cross-cutting
P_DIESEL = 0.49                # $/kWh [L] mine-scale diesel ~41 rub/kWh
P_FNPP = 6.45 / RUB_USD        # $/kWh [L] Baimskaya floating NPP 6.45 rub/kWh


def verdict(m, r):
    if m >= 1 and r >= 1.5:
        return "ALIVE"
    if m < 0.3 or r < 1.1:
        return "DEAD"
    return "WOUNDED"


# NIST WebBook Shomate parameters for SiO2 (quartz) [S12]; H - H298 in kJ/mol, t = T/1000
ALPHA = (-6.076591, 251.6755, -324.7964, 168.5604, 0.002548, -917.6893, -910.8568)
BETA = (58.75340, 10.27925, -0.131384, 0.025210, 0.025601, -929.3292, -910.8568)


def dH(T, p):
    A, B, C, D, E, F, H = p
    t = T / 1000.0
    return A * t + B * t**2 / 2 + C * t**3 / 3 + D * t**4 / 4 - E / t + F - H


def h_quartz(T):  # kJ/mol above 298.15 K, alpha below 847 K, beta above (includes transition)
    return dH(T, ALPHA) if T <= 847 else dH(T, BETA)


MW_SIO2 = 60.084
res = {}

# ---------------- Burst-wave lithotripsy energy (Ideas 1, 5) [S1] ----------------
f, cyc, prf, p, bw = 170e3, 10, 200, 6.5e6, 7.6e-3
I0 = p**2 / (2 * 998 * 1482)                      # W/m2 pulse-average at focus
P_pulse = I0 * math.pi * (bw / 2) ** 2 / (2 * math.log(2))  # Gaussian beam power
duty = cyc / f * prf
P_avg = P_pulse * duty                             # W time-average (lower bound)
d = 8.2e-3
V_st = math.pi / 6 * d**3                          # m3, mean stone as sphere (largest-mass case)
rho_ua, rho_cy = 1600, 1650                        # kg/m3 [A] stone densities
t_ua, t_cy = 36.0, 14.7 * 60                       # s [S1]
e_ua_t = P_avg * t_ua / (V_st * rho_ua) / 3.6e3    # kWh/t  (J/kg /3.6e6 *1000)
e_cy_t = P_avg * t_cy / (V_st * rho_cy) / 3.6e3
e_ua_m3 = P_avg * t_ua / V_st / 3.6e6              # kWh/m3 of stone
print(f"BWL: I0={I0/1e4:.0f} W/cm2, P_pulse={P_pulse:.0f} W, duty={duty:.4f}, P_avg={P_avg:.2f} W")
print(f"BWL specific energy (acoustic): uric acid {e_ua_t:.0f} kWh/t ({e_ua_m3:.0f} kWh/m3), "
      f"cystine {e_cy_t:.0f} kWh/t")

# ---------------- IDEA 1: tuned-burst frozen ground ripping ----------------
matrix = 0.35                       # [A] only ice-cemented pore volume must fail (generous)
req1 = e_ua_m3 * matrix             # kWh/m3 acoustic, best stone type
grade = 0.196                       # g Au per m3 rock moved [S2]
l_per_m3 = 11.0 * (2 / 3) * grade   # l diesel/m3 earthmoving [L 11 l/g, 2/3 earthmoving]
avail1 = l_per_m3 * 10.0 * 0.35     # kWh shaft/m3 (10 kWh/l LHV, 35% engine) [A std]
m1 = avail1 / req1
C_A = 2550.0
shA = dict(energy=.10, labour=.20, inbound=.12, outbound=.002, processing=.20, capital=.15, other=.22)
earth_oz = C_A * (1 - shA["other"]) * 2 / 3        # earthmoving ~2/3 of physical cost [L]
m3_oz = 31.1035 / grade
bwl_oz = req1 * m3_oz * P_DIESEL                    # battery charged from site diesel power
C1 = C_A - earth_oz + bwl_oz                        # all earthmoving cost removed (generous)
r1 = C_A / C1
res[1] = (m1, r1)
print(f"\nIDEA1 req {req1:.0f} kWh/m3 vs avail {avail1:.1f} kWh/m3 (diesel {l_per_m3:.2f} l/m3) "
      f"-> M={m1:.3f}; BWL ${bwl_oz:,.0f}/oz, earthmoving removed ${earth_oz:,.0f}/oz; "
      f"C1=${C1:,.0f}/oz R={r1:.2f}")

# ---------------- IDEA 2: transpolar drift pods ----------------
s_now = 0.20                         # Siberian-shelf ice reaching TPD/Fram Strait, was ~0.5 [S3]
transit = 2.5                        # yr, 2-3 yr [S3]
pod = (1910 + 2135) / 2 * 1.15 / 27  # $/t capacity: new 20ft box EUR1910-2135 [S4], 27 t coal [A]
V = 83.0 * (1 - 0.55)                # mine-gate coal $/t [L arch. C FOB minus 55% outbound]
I = V * 0.10 * transit               # inventory carry 10%/yr [A]
K = pod * 0.12 * 3.0                 # pod capital charge per 3-yr cycle, CRF 12% [A]
Pl, Rt = 10.0, 20.0                  # placement; retrieval+return+onward $/t [A, favourable]
nsr_bulk = 8500 * 0.05 * (8.5e9 / 28e3) / 1.4e6   # $/t conc, ledger B outbound (truck+NSR)
C_now2 = V + nsr_bulk


def c_pod(s):
    return (V + I + K + Pl + (1 - s) * pod) / s + Rt


s_req = (V + I + K + Pl + pod) / (C_now2 - Rt + pod)
m2 = s_now / s_req
C2 = c_pod(s_now)
r2 = C_now2 / C2
res[2] = (m2, r2)
print(f"\nIDEA2 pod ${pod:.0f}/t-cap, V=${V:.0f}, NSR bulk ${nsr_bulk:.0f}/t -> now ${C_now2:.0f}/t; "
      f"s_req={s_req:.2f}, M={m2:.2f}; pods ${C2:.0f}/t at s=0.2 (${c_pod(1.0):.0f}/t at s=1); "
      f"R={r2:.2f}; vs NSR general cargo $190+V: s_req="
      f"{(V+I+K+Pl+pod)/((V+16000/RUB_USD)-Rt+pod):.2f}")

# ---------------- IDEA 3: flash-and-electrolyse lithium ----------------
C_D = 10200.0
shD = dict(energy=.09, labour=.14, inbound=.04, outbound=.015, processing=.18, capital=.42, other=.12)
li = 2 * 6.941 / 73.89               # t Li per t LCE
naoh = li / 6.941 * 39.997           # t NaOH per t LCE (Li2SO4 + 2NaOH -> 2LiOH + Na2SO4)
e_split = 4000.0                     # kWh/t NaOH, Na2SO4 membrane salt splitting [S5]
conc = 1 / (0.06 * (73.89 / 29.88) * 0.90)       # t SC6 per t LCE, 90% recovery [A]
dh1373 = h_quartz(1373.15) / MW_SIO2             # MJ/kg, SiO2 as cp proxy, 25->1100 C [S12,S6]
E_fjh = conc * dh1373 * 1000 / 3.6               # kWh/t LCE, 100% efficient (generous)
req3 = naoh * e_split + E_fjh
avail3 = C_D * shD["energy"] / P_DIESEL          # kWh the current energy budget buys off-grid
m3 = avail3 / req3
C3 = (C_D * shD["capital"] / 3.0                 # idea's own "several-fold" (3x) capital cut
      + req3 * P_DIESEL                          # all power from winter-road diesel
      + C_D * shD["processing"] * 0.6            # reagents gone, membranes/carbon/makeup remain [A]
      + 150.0                                    # inbound non-fuel [A]
      + C_D * shD["labour"] + C_D * shD["outbound"] * 1.5 + C_D * shD["other"])
r3 = C_D / C3
res[3] = (m3, r3)
print(f"\nIDEA3 NaOH {naoh:.3f} t/t, split {naoh*e_split:.0f} kWh, conc {conc:.2f} t, "
      f"dh {dh1373:.3f} MJ/kg, FJH {E_fjh:.0f} kWh -> req {req3:.0f} kWh/t LCE; avail {avail3:.0f} "
      f"-> M={m3:.2f}; (EDBM 3190: M={avail3/(naoh*3190+E_fjh):.2f}); C3=${C3:,.0f} R={r3:.2f}; "
      f"grid 6.45 rub/kWh avail={C_D*shD['energy']/P_FNPP:.0f} kWh")

# ---------------- IDEA 4: spodumene through nepheline alumina kilns ----------------
al2o3 = 877e3                        # t/yr Achinsk output (82% of 1,069 kt) [S7]
tol = 0.0005                         # max Li2O in smelter alumina, 0.05% [S8]
f_lce = 73.89 / 29.88                # t LCE per t Li2O
cap_lce = al2o3 * tol * f_lce
m4 = cap_lce / 45000.0
load = 45000 / f_lce / al2o3 * 100
# chain, idea-favourable: chem plant = 70% of 91 bn [A] cut 10x (claim); mine/conc + road stay
capK = C_D * shD["capital"]
cap_new = capK * (27.3 + 40.0 + 63.7 / 10) / 131.0
toll = 16.5 * 8 + 100 * 3 + 200      # limestone, kiln coal, strip/evap $/t LCE [A]
proc = C_D * shD["processing"] * 0.25 + toll
energy = C_D * shD["energy"] * 0.30
lab = C_D * shD["labour"] * 0.6
inb = C_D * shD["inbound"] * 0.25
outb = conc * 5000 * (0.61 * 106 / 5000) + C_D * shD["outbound"]   # rail ~5,000 km at RZD coal rate [L]
rec_pen = (capK * 67.3 / 131 + lab + energy + C_D * shD["processing"] * 0.25) * (0.90 / 0.82 - 1)
C4 = cap_new + proc + energy + lab + inb + outb + C_D * shD["other"] + rec_pen
r4 = C_D / C4
res[4] = (m4, r4)
print(f"\nIDEA4 Li capacity at spec {cap_lce:,.0f} t LCE/yr vs 45,000 -> M={m4:.3f}; "
      f"unstripped Li2O in alumina {load:.2f}% (limit 0.05%), strip needed {1-m4:.1%}; "
      f"C4=${C4:,.0f} R={r4:.2f} (rail {conc*5000*0.61*106/5000:.0f} $/t LCE)")

# ---------------- IDEA 5: resonant kimberlite unmaking ----------------
req5 = e_ua_t                        # kWh/t, best (weakest) stone type; kimberlite is stronger
avail5 = 20.0                        # kWh/t integrated crushing-grinding plant [S9]
m5 = avail5 / req5
cpc = 157.5e9 / 33.1e6 / RUB_USD     # ALROSA 2024 cost of sales per carat [S10]
t_ct = 1 / 1.34                      # t ore per ct, reserve grade 1.34 ct/t [S10]
C5 = cpc * (1 - 0.25) + req5 * t_ct * P_FNPP   # BWL replaces all processing (25% [A])
r5 = cpc / C5
C5_typ = cpc * 0.75 + math.sqrt(e_ua_t * e_cy_t) * t_ct * P_FNPP
res[5] = (m5, r5)
print(f"\nIDEA5 req {req5:.0f} vs avail {avail5:.0f} kWh/t -> M={m5:.2f}; cost ${cpc:.1f}/ct; "
      f"C5=${C5:.1f}/ct R={r5:.2f} (typical stone energy: R={cpc/C5_typ:.2f})")

# ---------------- IDEA 6: ore stream as heat battery (ledger mill = archetype B) ----------------
h600 = (h_quartz(873.15) + 0.0443 * 25) / MW_SIO2 * 1000 / 3.6   # kWh/t, 0 -> 600 C [S12]
ore = 70e6                           # t/yr Baimskaya [S11]
req6 = ore * h600 / 8760 / 1000      # MW average needed
avail6 = 106.0                       # MW: the 4th (reserve) floating unit of 4 x 106 MW [S11]
m6 = avail6 / req6
cu = 8.5e9 / 28e3                    # t Cu/yr [L]
C_B = 8500.0
charge = ore * h600 * P_FNPP / cu
grind_e = 18.0                       # kWh/t grinding [A, Bond]
grind_save = grind_e * 0.19 * ore * P_FNPP / cu      # 19% BWi drop [S13]
heat_save = C_B * 0.11 - grind_e * ore * P_FNPP / cu # generous: all non-grinding energy displaced
C6 = C_B + charge - grind_save - heat_save
r6 = C_B / C6
res[6] = (m6, r6)
print(f"\nIDEA6 heat {h600:.0f} kWh/t -> {req6:,.0f} MW vs surplus {avail6:.0f} MW -> M={m6:.3f} "
      f"(all 424 MW: {424/req6:.2f}); site gen {424*8760/ore*1000:.0f} kWh/t; "
      f"charge ${charge:,.0f}/t Cu, grind save ${grind_save:.0f}, heat save ${heat_save:.0f}; "
      f"C6=${C6:,.0f} R={r6:.2f}; grind saving / charge = {grind_e*0.19/h600:.3f}")

# ---------------- IDEA 7: floating bluff coal miner ----------------
N_dep, r_km, area = 20, 100.0, 1.6e6   # deposits [S14]; Arctic Yakutia area [S15]
cov = min(1.0, N_dep * math.pi * r_km**2 / area)   # upper bound, no clustering
m7 = cov / 1.0
C_set = 275.0
pit = C_set * (1 - 0.85)              # non-logistics part of settlement coal [L]
haul = 100 * 4.0 / RUB_USD * 2        # 100 km at 2x LORP 3-5 rub/t-km [L]
C7 = pit * 2 + haul + 10.0            # barge mining at 2x pit cost, yard $10 [A]
r7 = C_set / C7
res[7] = (m7, r7)
print(f"\nIDEA7 coverage {cov:.2f} (20 deposits / 97 settlements = {20/97:.2f}) -> M={m7:.2f}; "
      f"C7=${C7:.0f}/t R={r7:.2f}")

# ---------------- IDEA 8: frozen placer dry-washing ----------------
R_dry, R_wet = 0.60, 0.85             # dry pneumatic best [S16]; wet sluice [A, S17]
fixed = C_A * shA["other"]            # MET/taxes per oz, independent of recovery
save = C_A * shA["capital"] * 0.5 + C_A * shA["processing"] / 3   # year-round, no water [A]
var = C_A - fixed - save
R_req = R_wet * var / (C_A - fixed)
m8 = R_dry / R_req
C8 = fixed + var * R_wet / R_dry
r8 = C_A / C8
res[8] = (m8, r8)
print(f"\nIDEA8 R_req={R_req:.2f} vs R_dry={R_dry:.2f} -> M={m8:.2f}; equal-recovery R="
      f"{C_A/(fixed+var):.2f}; C8=${C8:,.0f}/oz R={r8:.2f}")

print("\nSUMMARY")
for k, (m, r) in res.items():
    print(f"IDEA {k}: MARGIN {m:.3f}  RATIO {r:.2f}  -> {verdict(m, r)}")

SRC = {
    "S1": "Maxwell et al. 2015 J Urol 193:338 (PMC4384893); UW APL ASA 2013 slides: 170 kHz, 10-cycle, 200 Hz, "
          "6.5 MPa, -6 dB 7.6 mm, 8.2 mm stones, 36 s-14.7 min",
    "S2": "sibran.ru placer resource paper: 0.196 g/m3 open-pit placers",
    "S3": "Krumpen et al. 2019 Sci Rep 9:5459; AWI press release 2 Apr 2019 (half -> 20%, 2-3 yr transit)",
    "S4": "used-machines.com new 2025 20ft containers EUR 1,910-2,135 FOB",
    "S5": "US5258106 / EP0522382 Na2SO4 electrolysis ~4,000 kWh/t NaOH; NWU EDBM 3.19 kWh/kg",
    "S6": "Chem. Ind. Eng. Prog. 2020 39(9):3478 (spodumene transition >1060 C); Rice FJH preprint 2024",
    "S7": "RUSAL / En+ Achinsk page: 1,069 kt capacity, 877 kt, 82%",
    "S8": "J Cent South Univ 2019 (Li equilibrium in aluminate liquor): Li2O <0.05% in alumina; "
          "ICSOBA 2025 AA36: Li >99% precipitated in 2 h",
    "S9": "Thunder Said Energy comminution note: ~20 kWh/t integrated crushing-grinding",
    "S10": "Rapaport/Interfax 2024: ALROSA cost of sales RUB157.5bn, 33.1 Mct; JORC 1.34 ct/t",
    "S11": "inbusiness.kz / eastrussia.ru: Baimskaya 70 Mt/yr, 4 FPUs ~424 MW, one reserve",
    "S12": "NIST Chemistry WebBook SiO2 (quartz) Shomate parameters",
    "S13": "Minerals 2022 12(5):593: 19% BWi drop after 300-600 C; Acta Montanistica Slovaca 2005: quartz 5-21%",
    "S14": "Batugina et al. 2014 Nauka i obrazovanie No.4: 20 coal deposits in polar Yakutia, 632 Mt",
    "S15": "arcticandnorth.ru / porarctic.ru: Arctic Yakutia 1.6 Mkm2, 97 settlements, 13 districts",
    "S16": "E3S Web Conf 56:03012 (2018): POS-2000 dry pneumatic separator, Au to concentrate up to 60%",
    "S17": "RU patent 2548272 (digital.spmi.ru): sluices recover <0.5 mm gold at 25-78%",
}
