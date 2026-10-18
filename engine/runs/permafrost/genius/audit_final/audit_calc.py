"""Adversarial recomputation of the 4 permafrost ideas (audit_final).
Every number printed here is either (a) a recomputation of a number stated in TASK.md,
(b) a consistency / window check built from the idea's own numbers, or (c) a sensitivity
run over a plausible range taken from a cited measurement. Units SI unless noted."""
import math

RHO_W, RHO_I, L_F = 1000.0, 917.0, 334e3      # kg/m3, kg/m3, J/kg
G = 9.81
DAY = 86400.0
pr = print

def hdr(s):
    pr("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)

# ---------------------------------------------------------------------------
hdr("IDEA 1  Talik dredging under lakes")
# 1a. ice thickness, Stefan-type h = a*sqrt(FDD)
for a in (0.017, 0.024, 0.027):
    pr(f"alpha={a:.3f} m/(degC d)^0.5 : FDD5000 -> {a*math.sqrt(5000):.2f} m, FDD6500 -> {a*math.sqrt(6500):.2f} m")
k_i = 2.2
for fdd in (5000, 6500):
    h = math.sqrt(2 * k_i * fdd * DAY / (RHO_I * L_F))
    pr(f"pure Stefan (no snow, k_i=2.2): FDD {fdd} -> {h:.2f} m")
# FDD of Verkhoyansk from monthly normals (Wikipedia via search)
verk = [-45.3, -41.6, -29.6, -12.4, 3.7, 13.2, 16.4, 11.5, 2.6, -14.3, -34.7, -43.4]
mdays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
fdd_v = sum(-t * d for t, d in zip(verk, mdays) if t < 0)
pr(f"Verkhoyansk FDD from monthly means ~ {fdd_v:.0f} degC.d -> ice at a=0.024: {0.024*math.sqrt(fdd_v):.2f} m, a=0.027: {0.027*math.sqrt(fdd_v):.2f} m")

# 1b. melt power for 300-850 m3/day of ice
for v in (300, 850):
    p = v * RHO_I * L_F / DAY / 1e6
    p20 = v * RHO_I * (L_F + 2100 * 20) / DAY / 1e6
    pr(f"melt {v} m3/d ice: {p:.2f} MW (latent only), {p20:.2f} MW incl. warming from -20 C")

# 1c. pond heat balance
A_pond = 1500.0
for P, dT in ((0.69e6, 35), (0.81e6, 45)):
    q = P / A_pond
    pr(f"stated {P/1e6:.2f} MW / 1500 m2 = {q:.0f} W/m2 at dT={dT} K -> {q/dT:.1f} W/m2K")
# measured: Makinson Inlet polynya ~1000 langley/day at air -30 C, water -1 C, wind 5 m/s
q_mak = 1000 * 41840 / DAY
c_mak = q_mak / 29.0
pr(f"Makinson Inlet measured: {q_mak:.0f} W/m2 at dT=29 K, 5 m/s -> {c_mak:.1f} W/m2K")
for dT in (35, 45):
    pr(f"  scaled to dT={dT}: {c_mak*dT:.0f} W/m2 -> {c_mak*dT*A_pond/1e6:.2f} MW for 1500 m2")
pr(f"max open area for 1.0 MW: at stated coef 12.0-13.1 W/m2K and dT 45/35 -> {1e6/(12.0*45):.0f}-{1e6/(13.1*35):.0f} m2;"
   f" at Makinson coef -> {1e6/(c_mak*45):.0f}-{1e6/(c_mak*35):.0f} m2")

# bulk-formula sensitivity to wind
def pond_flux(Ta_C, U, Ch=1.5e-3, Ce=1.5e-3, eps_a=0.70):
    Ts = 273.15 + 0.5
    Ta = 273.15 + Ta_C
    rho_a = 101325 / (287.05 * Ta)
    H = rho_a * 1005 * Ch * U * (Ts - Ta)
    es = 611 * math.exp(17.27 * 0.5 / (0.5 + 237.3))
    ea = 611 * math.exp(21.87 * Ta_C / (Ta_C + 265.5))   # saturation over ice
    qs, qa = 0.622 * es / 101325, 0.622 * ea / 101325
    LE = rho_a * 2.5e6 * Ce * U * (qs - qa)
    LW = 0.97 * 5.67e-8 * Ts ** 4 - eps_a * 5.67e-8 * Ta ** 4
    # free convection floor ~ 5 W/m2K on sensible at very low wind
    H = max(H, 5.0 * (Ts - Ta))
    return H + LE + LW
for Ta in (-35, -45):
    row = ", ".join(f"U={U}:{pond_flux(Ta, U)*A_pond/1e6:.2f}MW" for U in (1, 2, 3, 4, 5, 6))
    pr(f"bulk model, Ta={Ta}: {row}")
# freeze-in after heat loss
for q in (500, 750):
    r = q / (RHO_I * L_F)
    pr(f"open pond freezing at {q} W/m2: {r*3600*1000:.1f} mm/h, first day ~{r*DAY*100:.0f} cm")

# 1d. steady talik under circular lake (Lachenbruch/Mackay type)
def talik(R, Tg, Tb, Gg):
    f = lambda z: Tg + Gg * z + (Tb - Tg) * (1 - z / math.sqrt(z * z + R * R))
    z, step, zmax = 0.01, 0.25, -Tg / Gg + 1.0
    while z < zmax:
        if f(z + step) <= 0:
            lo, hi = z, z + step
            for _ in range(50):
                m = 0.5 * (lo + hi)
                lo, hi = (m, hi) if f(m) > 0 else (lo, m)
            return 0.5 * (lo + hi)
        z += step
    return float('inf')
pairs = []
for Tg in [x * 0.5 for x in range(-20, -3)]:          # -10 ... -2 C
    for Tb in [x * 0.5 for x in range(2, 11)]:         # +1 ... +5 C
        for Gg in (0.02, 0.025, 0.03):
            z50 = talik(50, Tg, Tb, Gg)
            if 15 <= z50 <= 22:
                pairs.append((z50, talik(100, Tg, Tb, Gg), Tg, Tb, Gg))
z100 = [p[1] for p in pairs if math.isfinite(p[1])]
pr(f"parameter sets giving 15-22 m under R=50 m: {len(pairs)}; same sets under R=100 m: {min(z100):.0f}-{max(z100):.0f} m"
   f" (stated 36-67 m); ratio z100/z50 = {min(p[1]/p[0] for p in pairs):.2f}-{max(p[1]/p[0] for p in pairs):.2f}")

# 1e. lake-area exhaustion: rate x window
for vol, h in ((300, 1.2), (850, 1.9)):
    A_day = vol / h
    pr(f"ice {vol} m3/d at {h} m -> pond advance {A_day:.0f} m2/day (cut length ~{A_day:.0f} m/day for 2x2 m grid)")
A_lo, A_hi = 300 / 1.2, 850 / 1.9
for D in (100, 200):
    Al = math.pi * (D / 2) ** 2
    pr(f"lake {D} m across: area {Al:.0f} m2 -> exhausted in {Al/A_hi:.0f}-{Al/A_lo:.0f} days")
for days in (300,):
    need = (A_lo * days, A_hi * days)
    dia = [2 * math.sqrt(a / math.pi) for a in need]
    pr(f"{days} d/yr needs {need[0]:.0f}-{need[1]:.0f} m2 of lake per year = one lake {dia[0]:.0f}-{dia[1]:.0f} m across;"
       f" = {need[0]/7854:.0f}-{need[1]/7854:.0f} lakes of 100 m or {need[0]/31416:.1f}-{need[1]/31416:.1f} lakes of 200 m")
for life in (10, 15):
    a = (A_lo * 300 * life, A_hi * 300 * life)
    pr(f"  {life}-yr dredge life: {a[0]/1e6:.2f}-{a[1]/1e6:.2f} km2 -> single lake {2*math.sqrt(a[0]/math.pi):.0f}-{2*math.sqrt(a[1]/math.pi):.0f} m across")
# implied daily ground volume
for A_day in (A_lo, A_hi):
    pr(f"  ground dug at {A_day:.0f} m2/d x 15.5-16 m soil = {A_day*15.5:.0f}-{A_day*16:.0f} m3/d")

# 1f. ice disposal
for h in (1.2, 1.9):
    cap = (RHO_W - RHO_I) * h / RHO_I
    blk = 4 * h
    pr(f"ice {h} m: floating sheet carries only {cap:.2f} m of stacked ice before flooding;"
       f" 2x2 m block = {blk*RHO_I/1000:.1f} t, net buoyancy {blk*(RHO_W-RHO_I)/1000:.2f} t (cannot sink)")
winter = 300 - 165
for v in (300, 850):
    tot = v * winter
    pr(f"{v} m3/d x {winter} winter days = {tot:.0f} m3 ice = {tot/7854:.1f} m over a 100-m lake, {tot/31416:.1f} m over a 200-m lake")
pr(f"blocks/day: {300/(4*1.2):.0f}-{850/(4*1.9):.0f} (4.4-7.0 t each), i.e. {300/(4*1.2)/24:.1f}-{850/(4*1.9)/24:.1f} lifts/hour 24/7")

# 1g. value arithmetic
pr(f"710 rub/g / 210 rub/m3 -> {710/210:.2f} m3 per g -> recovered grade {210/710:.3f} g/m3")
pr(f"method-attributable gain 1.16x vs 'several times' (>=3x): short by {3/1.16:.1f}x")
# 1h. statistics: block-months per arm to detect 16% per-gram difference
for cv in (0.3, 0.5):
    d = math.log(1.16)
    n = 2 * (1.96 + 0.84) ** 2 * cv ** 2 / d ** 2
    pr(f"grade CV {cv} between monthly blocks -> n = {n:.0f} block-months per arm to see 1.16x at 95%/80%")

# ---------------------------------------------------------------------------
hdr("IDEA 2  Jacked frozen-block stripping")
V = 40 * 40 * 10
M = 30400e3
W = M * G
U_full = RHO_W * G * V
pr(f"block 40x40x10 = {V} m3, 30,400 t -> {M/V/1000:.2f} t/m3; weight {W/1e6:.1f} MN; full-submergence uplift {U_full/1e6:.1f} MN")
pr(f"face stress 92 MN / 400 m2 = {92/400:.3f} MPa ; installed 19x5 = 95 MN ; margin {95-92} MN = {3/92*100:.1f}%")
pr(f"implied friction: dry {92/(W/1e6):.3f}; fully submerged {92/((W-U_full)/1e6):.3f}")
for mu in (0.58, 0.65, 0.70, 0.78):
    row = []
    for sub in (1.0, 0.9, 0.8):
        Wp = (W - sub * U_full) / 1e6
        row.append(f"sub{int(sub*100)}%:{mu*Wp:.0f}MN")
    pr(f"mu={mu} (phi'={math.degrees(math.atan(mu)):.0f} deg): " + ", ".join(row))
cap = 3.5 * 92
pr(f"brace SF 3.5 -> {cap:.0f} MN over 1600 m2 = {cap/1600:.2f} MPa implied frozen base shear strength")
for tau in (0.2, 0.5, 1.0):
    a = 3.0 / tau
    pr(f"3 MN margin / {tau} MPa bond = {a:.1f} m2 of unthawed bridge allowed = {a/1600*100:.2f}% of base, {a/2800*100:.2f}% of base+3 side kerfs")
# drilling window
blocks = 190000 / V
for v in (1.0, 0.6, 0.5, 0.3, 0.1):
    h_bit = 7600 / v / 60
    tot = blocks * h_bit
    pr(f"v={v} m/min: {h_bit:.0f} h bit-time/block; {blocks:.2f} blocks need {tot:.0f} h"
       f" = {tot/100:.1f}-{tot/120:.1f} h/day over a 100-120 d season")
pr("season capacity at 20 h/day x 100-120 d = 2000-2400 h -> max output vs rate:")
for v in (1.0, 0.6, 0.5, 0.3, 0.1):
    out = [min(190000, hrs * v * 60 / 7600 * V) for hrs in (2000, 2400)]
    pr(f"  v={v}: {out[0]:.0f}-{out[1]:.0f} m3/season (stated 190,000 at 1 m/min)")
# per-gram cost vs rate (calibrated on the idea's own two points: 760 rub/g at 1 m/min, 990 at 0.5)
Sf = 990 - 760
for v in (1.0, 0.6, 0.5, 0.3, 0.1):
    c = 760 + Sf * (1 / v - 1)
    pr(f"  v={v}: {c:.0f} rub/g -> {990/c:.2f}x vs 990 baseline")
# diesel for hot-water drilling vs rate; Talalay 2018: 10 L/min at 60 C -> 0.57-0.62 m/min in ice
P_tal = 10 / 60 * 4186 * 60
pr(f"Talalay et al. 2018 washer drill heat: 10 L/min x 60 K = {P_tal/1e3:.1f} kW for 0.57-0.62 m/min in clean ice")
for P in (42e3, 108e3):
    for v in (1.0, 0.3, 0.1):
        e = P / (v / 60) / 3.6e6           # kWh per m
        l_per_m3 = e * 7600 / 8.5 / V       # 10 kWh/l at 85% burner
        pr(f"  P={P/1e3:.0f} kW v={v}: {e:.2f} kWh/m -> {l_per_m3:.3f} l diesel per m3 overburden (drilling heat only)")
# creek-water heat balance for needle thawing at 10 m3 water / m3 pay
for ice in (0.15, 0.25):
    for dTg in (3, 6):
        Q = ice * RHO_I * L_F + 2.0e6 * dTg
        for eta in (1.0, 0.5, 0.3):
            Tw = 0.5 + Q / (10 * 4.186e6 * eta)
            pr(f"  ice {ice:.2f}, ground -{dTg} C, efficiency {eta}: need {Q/1e6:.0f} MJ/m3 -> creek water >= {Tw:.1f} C")
# cantilever over a mined (un-backfilled) cell
for sub in (0.0, 1.0):
    w = (W - sub * U_full) / 40
    S = 40 * 10 ** 2 / 6
    for a in (10, 15, 20):
        pr(f"  overhang {a} m, submerged={sub}: bending stress {w*a*a/2/S/1e6:.2f} MPa")
# struts for a 40 m push
for SF in (1, 3):
    I = SF * 5e6 * 40 ** 2 / (math.pi ** 2 * 210e9)
    pr(f"Euler strut 40 m, 5 MN, SF {SF}: I >= {I:.4f} m4")
D, t = 1.0, 0.03
I_t = math.pi / 8 * D ** 3 * t
m_t = math.pi * D * t * 7850 * 40 / 1000
pr(f"  1.0 m x 30 mm tube: I={I_t:.4f} m4, {m_t:.0f} t per 40 m strut, x19 = {19*m_t:.0f} t")
# labour share of 62 rub/m3
for crew in (8, 12):
    loaded = 155.6e3 * 1.3
    cost = crew * loaded * 4
    pr(f"crew {crew} x 4 months x {loaded/1e3:.0f}k rub/month loaded = {cost/1e6:.1f} M rub = {cost/190000:.0f} rub/m3 of the 62")
pr(f"diesel 0.12-0.15 l/m3 x 80-100 rub/l = {0.12*80:.0f}-{0.15*100:.0f} rub/m3")
pr(f"diesel ratios: 0.30/0.15={0.30/0.15:.1f}, 0.65/0.12={0.65/0.12:.1f}; 990/760={990/760:.2f}")

# ---------------------------------------------------------------------------
hdr("IDEA 3  Floating bluff coal miner")
pr(f"2100/18={2100/18:.1f}, 2500/18={2500/18:.1f} rub/GJ (stated 117-141); 6962/332 -> {6962/332:.2f} MJ/kg implied baseline coal")
pr(f"ratios 332/141={332/141:.2f}, 332/117={332/117:.2f}")
pr(f"people: 42,000/7={42000/7:.0f}, 56,000/7={56000/7:.0f}; per village (5-8): {42000/7/8:.0f}-{56000/7/5:.0f}")
for rate in (15, 5):
    for hours in (24, 12):
        m3 = 60 * hours * rate
        pr(f"stone {rate} m3/h x {hours} h x 60 d = {m3:.0f} m3 -> {m3/0.46/1000:.1f}-{m3/0.23/1000:.1f} kt coal at 0.46-0.23 m3/t")
pr(f"stated scaling: 15->5 m3/h (3x) gives 42-56 -> 8-16 kt, i.e. {42/16:.1f}-{56/8:.1f}x")
# ETH HEAP autonomous dry-stone rate
wall = 10 * 1.7 * 4
hrs = 109 * 17.4 / 60
heap = wall / hrs
pr(f"HEAP pilot wall {wall:.0f} m3, 109 stones x 17.4 min = {hrs:.1f} h -> {heap:.2f} m3/h; required 15 m3/h = {15/heap:.1f}x SOTA")
out_heap = (8 * heap / 5, 16 * heap / 5)
out_heap24 = (60 * 24 * heap / 0.46, 60 * 24 * heap / 0.23)
pr(f"output at HEAP rate: idea's own linear scaling {out_heap[0]:.1f}-{out_heap[1]:.1f} kt; 24 h/day {out_heap24[0]/1000:.1f}-{out_heap24[1]/1000:.1f} kt")
for fixed in (0.6, 0.8):
    for ratio in (42 / out_heap24[1] * 1000, 56 / out_heap[0]):
        c = (1 - fixed) + fixed * ratio
        pr(f"  fixed share {fixed}, output down {ratio:.1f}x -> cost x{c:.1f}: {2100*c:.0f}-{2500*c:.0f} rub/t = {2100*c/18:.0f}-{2500*c/18:.0f} rub/GJ vs 332")
# surplus rock at the site limit 1 m3 rock per m3 coal
rho_coal, rho_rock_bank = 1.3, 2.3
placed_density = (1 - 0.38) * 2.6
rock_t_per_t = rho_rock_bank / rho_coal
facing_t = (0.23 * placed_density, 0.46 * placed_density)
surplus = (rock_t_per_t - facing_t[1], rock_t_per_t - facing_t[0])
pr(f"rock at limit: {rock_t_per_t:.2f} t rock per t coal; facing uses {facing_t[0]:.2f}-{facing_t[1]:.2f} t/t; surplus {surplus[0]:.2f}-{surplus[1]:.2f} t/t"
   f" -> {42*surplus[0]:.0f}-{56*surplus[1]:.0f} kt of riprap per season to barge and place")
# summer thaw behind a porous revetment at the waterline
for Tw in (10, 15):
    for ice in (0.10, 0.30):
        Lv = ice * RHO_I * L_F
        for k in (1.5, 2.5):
            X = math.sqrt(2 * k * Tw * 100 * DAY / Lv)
            pr(f"  Tw={Tw} C, ice {ice:.2f}, k={k}: thaw {X:.1f} m in 100 d behind open rock")
# ice-sized riprap
for h in (1.2, 2.0):
    pr(f"river ice {h} m -> stone >= {h:.1f} m (bridge guide) / D100 ~ {2.5*h:.1f} m (IAHR 1997); mass of {h:.1f} m cube = {h**3*2.6:.1f} t")
# demand side
pop_arctic = 67798
coal_arctic = 88 + 115 + 1.8
pc = coal_arctic * 1000 / pop_arctic
pr(f"Arctic Yakutia utility coal 2016 {coal_arctic:.0f} kt / {pop_arctic} people = {pc:.1f} t/person (stated 7)")
pr(f"42-56 kt at {pc:.1f} t/person = {42000/pc:.0f}-{56000/pc:.0f} people = {42000/pc/pop_arctic*100:.0f}-{56000/pc/pop_arctic*100:.0f}% of Arctic Yakutia;"
   f" 6000-8000 people at {pc:.1f} t = {6000*pc/1000:.0f}-{8000*pc/1000:.0f} kt")
pr(f"one barge 42-56 kt = {42/coal_arctic*100:.0f}-{56/coal_arctic*100:.0f}% of all Arctic Yakutia utility coal")

# ---------------------------------------------------------------------------
hdr("IDEA 4  Wintering miner-barge boilerhouses")
def nonheating(monthly, thr=8.0):
    # monthly means at mid-month (day 15 + cumulative). Linear interpolation, count days > thr
    mids = []
    c = 0
    for d in mdays:
        mids.append(c + d / 2)
        c += d
    days_above = 0
    temps = []
    for day in range(365):
        # find bracketing months
        for i in range(12):
            j = (i + 1) % 12
            a, b = mids[i], mids[j] + (365 if j == 0 else 0)
            dd = day if day >= mids[0] else day + 365
            if a <= dd < b:
                t = monthly[i] + (monthly[j] - monthly[i]) * (dd - a) / (b - a)
                break
        else:
            t = monthly[0]
        temps.append(t)
        if t > thr:
            days_above += 1
    heat = [t for t in temps if t <= thr]
    return days_above, sum(heat) / len(heat)
chok = [None, None, None, None, -4.9, 6.7, 10.6, 8.1, 1.6, None, None, None]
sred_may = (-1.0, 1.0)
cases = {
    "Verkhoyansk": verk,
    "Chokurdakh(May-Sep)": [-34.0, -33.0, -27.0, -18.0, -4.9, 6.7, 10.6, 8.1, 1.6, -12.0, -26.0, -32.0],
    "Srednekolymsk(May=-1)": [-38.0, -35.0, -26.0, -13.0, -1.0, 11.2, 13.9, 10.1, 3.2, -12.0, -28.0, -36.0],
    "Srednekolymsk(May=+1)": [-38.0, -35.0, -26.0, -13.0, 1.0, 11.2, 13.9, 10.1, 3.2, -12.0, -28.0, -36.0],
}
for name, m in cases.items():
    nh, tmean = nonheating(m)
    pr(f"{name}: days with mean > 8 C = {nh}; heating season = {365-nh} d (mean {tmean:.1f} C); 92-d absence leaves {max(0,92-nh)} heating days uncovered")
pr("(winter-month values other than May-Sep only affect the heating-season mean, not the window)")
# coal need at 1.3 MW average
for days in (275, 286, 314):
    for eta in (0.75, 0.85):
        for lhv in (18e6, 21e6):
            t = 1.3e6 * days * DAY / (eta * lhv) / 1000
            pr(f"  {days} d, eta {eta}, {lhv/1e6:.0f} MJ/kg: {t:.0f} t coal (hold 2000 t)")
pr(f"2000 t at Idea-3 7 t/person -> {2000/7:.0f} people; stated 300-700 implies {2000/700:.1f}-{2000/300:.1f} t/person")
# peak/average consistency
for name, m in (("Verkhoyansk", verk),):
    nh, tmean = nonheating(m)
    for tdes in (-50, -55):
        r = (20 - tdes) / (20 - tmean)
        pr(f"{name}: design {tdes} C, heating mean {tmean:.1f} C -> peak/avg {r:.2f} (stated 3.2/1.3 = {3.2/1.3:.2f});"
           f" 3.2 MW peak => avg {3.2/r:.2f} MW")
# hold heating to keep coal unfrozen
for Uv in (0.3, 1.0):
    for dT in (40, 60):
        q = 2200 * Uv * dT
        pr(f"  deck 2200 m2, U={Uv}, dT={dT}: {q/1e3:.0f} kW = {q/1.3e6*100:.0f}% of 1.3 MW")
# draft check vs reference barge V1500 (75 x 17.2 m, 1500 t at 1.8 m)
for Cb in (0.85, 0.9, 1.0):
    ls_ref = 75 * 17.2 * 1.8 * Cb - 1500
    area_ref = 2 * 75 * 17.2 + 2 * (75 + 17.2) * 3.5
    area_new = 2 * 100 * 22 + 2 * (100 + 22) * 2.5
    ls_new = ls_ref * area_new / area_ref
    T = (2000 + ls_new + 60) / (100 * 22 * Cb)
    pr(f"Cb={Cb}: ref lightship {ls_ref:.0f} t -> 100x22 m hull {ls_new:.0f} t -> draft {T:.2f} m (stated 1.26)")
pr(f"stated 1.26 m with Cb=1 implies lightship+boiler <= {100*22*1.26-2000:.0f} t; with Cb=0.9 <= {100*22*1.26*0.9-2000:.0f} t")
# hull utilisation
for rt in (12, 22):
    trips = 92 // rt
    pr(f"round trip {rt} d -> {trips} conventional coal trips in 92 d = {trips*2000} t vs 2000 t for the bunker barge ({trips}x)")
pr(f"92-12={92-12}, 92-22={92-22}; 8080/5000={8080/5000:.2f}, 8080/3000={8080/3000:.2f}; implied old cost 8080/0.88={8080/0.88:.0f}-{8080/0.66:.0f} rub/t")
