"""Idea 1 - Spring Sun-Wind Deflation Placer: recompute stated numbers and attack them."""
import math

rho_i = 917.0     # ice kg/m3
Ls = 2.834e6      # latent heat of sublimation J/kg
kappa = 0.4

print("== 1. Stated arithmetic ==")
# gravel freed per mm w.e. for pore-ice volume fraction phi
for phi in (0.30, 0.15):
    mm_we_per_mm_gravel = phi * rho_i / 1000.0
    print(f"pore ice {phi}: 1 mm w.e. frees {1/mm_we_per_mm_gravel:.2f} mm gravel")
for rate in (0.014, 0.041):
    print(f" midwinter {rate} mm we/d -> {rate/(0.30*0.917):.3f} mm/d gravel (claim 0.05-0.15)")
for rate in (0.4, 0.7):
    print(f" spring {rate} mm we/d -> phi0.15: {rate/(0.15*0.917):.2f} mm/d ; phi0.30: {rate/(0.30*0.917):.2f} mm/d (claim 2.5-5)")
season = (31 - 15 + 1) + 30 + 10  # Mar15..May10 inclusive
print("season days Mar15-May10 =", season)
print("0.21 m / season -> required mean mm/d =", 210 / season)
print("required mean sublimation mm we/d at phi .15 =", 210 / season * 0.15 * 0.917)
print("area for 100,000 m3/y at 0.21 m/y = %.3f km2" % (1e5 / 0.21 / 1e6))
# energy for sublimation
for r in (0.4, 0.7):
    print(f" sublimation {r} mm/d needs {r*Ls/86400:.1f} W/m2 mean latent flux")

print("\n== 2. Wind window: gold vs quartz thresholds (Shao & Lu 2000) ==")
rho_a = 1.35  # air at about -10 C
g = 9.81
AN = 0.0123
def ust_t(d, rho_p, gamma=3e-4):
    return math.sqrt(AN * (rho_p / rho_a * g * d + gamma / (rho_a * d)))
for name, rho_p in (("quartz", 2650.0), ("gold", 19300.0)):
    for d_um in (25, 40, 50, 63, 80, 100, 150, 250, 500, 1000):
        print(f" {name:6s} d={d_um:5d} um  u*t={ust_t(d_um*1e-6, rho_p):.3f} m/s")
# find gold minimum threshold
best = min((ust_t(d*1e-6, 19300.0), d) for d in range(5, 2000))
print(" gold minimum threshold u*t = %.3f m/s at d = %d um" % best)
q500 = ust_t(500e-6, 2650.0)
q25 = ust_t(25e-6, 2650.0)
print(" quartz 25 um: %.3f, quartz 500 um: %.3f ; ratio gold-min/quartz-max = %.3f" % (q25, q500, best[0] / max(q25, q500)))
# gamma uncertainty 1.65e-4 .. 5e-4
for gam in (1.65e-4, 3e-4, 5e-4):
    gm = min((ust_t(d*1e-6, 19300.0, gam), d) for d in range(5, 2000))
    qmax = max(ust_t(25e-6, 2650.0, gam), ust_t(500e-6, 2650.0, gam))
    print(f"  gamma={gam:.2e}: gold min {gm[0]:.3f} at {gm[1]} um; quartz(25,500) max {qmax:.3f}; window {100*(gm[0]/qmax-1):+.1f}%")
# 10 m wind -> u* for plausible roughness of a harrowed gravel field
for z0 in (0.0005, 0.001, 0.003, 0.005, 0.01):
    for U in (7.0, 8.0, 10.0, 15.0):
        us = kappa * U / math.log(10.0 / z0)
        print(f"  z0={z0*1000:4.1f} mm U10={U:4.1f} m/s -> u*={us:.3f}")
# gust factor: 10 m gusts are ~1.4-1.6 x mean in open tundra
print(" with gust factor 1.4: U10=7 -> gust 9.8 m/s; z0=3 mm u* =", round(kappa*9.8/math.log(10/0.003), 3))

# Raupach drag partition: non-erodible pebble lag raises threshold
def raupach_R(lam, beta=90.0, m=0.5, sigma=1.0):
    return 1.0 / math.sqrt((1 - sigma*m*lam) * (1 + m*beta*lam))
for lam in (0.02, 0.05, 0.1, 0.2):
    print(f" pebble frontal-area index {lam}: threshold multiplier {1/raupach_R(lam):.2f}")

print("\n== 3. Vapour-diffusion resistance of the dry lag ==")
D_air = 2.1e-5  # m2/s water vapour in air ~ -10C
for por, tort in ((0.35, 1.5),):
    Deff = D_air * por / tort
    for U in (6.0,):
        ra = 1.0 / (2e-3 * U)  # aerodynamic resistance s/m, Ce=2e-3
        for dl_mm in (1, 3, 10, 20, 40):
            rdl = dl_mm / 1000.0 / Deff
            print(f" dry layer {dl_mm:3d} mm: r_dry={rdl:6.0f} s/m vs r_a={ra:.0f} s/m -> rate reduced x{(ra+rdl)/ra:.1f}")

print("\n== 4. Effective season (no snow, no melt) ==")
# Assume usable when surface stays below 0 C AND sun high enough; mid-March too cold/dark, May melt
# Tiksi normals (approx): Mar -27, Apr -19 (daily max ~-11), May -4 (daily max ~-3, low -7)
# dark surface midday excess over air on a sunny day ~ (absorbed SW - net LW)/h
for month, SWdown_noon, Tair_max in (("mid-Mar", 250, -24), ("mid-Apr", 450, -11), ("early May", 600, -3)):
    absorbed = 0.88 * SWdown_noon
    netLW = 90.0
    h = 18.0  # W/m2K sensible transfer at ~6 m/s
    Ts = Tair_max + (absorbed - netLW - 15) / h   # 15 W/m2 to latent at limit
    print(f" {month}: noon dark-surface T ~ {Ts:+.1f} C (air max {Tair_max})")

print("\n== 5. Snow: spring snowfall/drift onto a 0.5 km2 dark field ==")
area = 0.476e6
# Snow cover in N Yakutia tundra ~35 cm at 0.3 g/cm3 until late May-early June (UNESCO Indigirka listing)
snow_we_mm = 350 * 0.3
print(" pre-existing snowpack to strip: %.0f mm w.e. = %.0f t over field" % (snow_we_mm, snow_we_mm/1000*area))
# Spring snowfall Mar15-May10, Tiksi ~ 8-12 mm w.e./month
for pr in (8, 12):
    tot = pr * season / 30.0
    print(f" spring snowfall at {pr} mm/month: {tot:.0f} mm w.e. -> {tot/1000*area:.0f} t; each 1 mm w.e. of fresh snow (~1 cm) covers the surface")
# albedo effect on absorbed energy
for alb in (0.12, 0.5, 0.8):
    print(f" albedo {alb}: absorbed fraction {1-alb:.2f}")

print("\n== 6. Harrow-and-rake machine time ==")
for width, speed, eff in ((12.0, 8.0, 0.8), (8.0, 6.0, 0.75)):
    ha_per_h = width * speed * 1000 * eff / 1e4
    passes = 2  # harrow + rake
    hours_day = area / 1e4 / ha_per_h * passes
    hours_season = hours_day * season
    for rate in (120.0, 200.0):
        cost = hours_season * rate
        print(f" {width} m @ {speed} km/h: {hours_day:.1f} tractor-h/day, {hours_season:.0f} h/season; at ${rate}/h -> ${cost:,.0f} = ${cost/1e5:.2f}/m3")
# windrowed lag must be loaded and hauled: +10 mm lag share
for lag_share in (0.45, 0.55):
    vol = 1e5 * lag_share
    for c in (0.6, 1.2):
        print(f" lag {lag_share:.0%} of volume loaded+hauled at ${c}/m3 -> ${vol*c/1e5:.2f}/m3 of pay")
# residue washing
for res in (0.25, 0.35):
    for wc in (3.0, 6.0):
        print(f" residue {res:.0%} washed at ${wc}/m3 -> ${res*wc:.2f}/m3 of pay")

print("\n== 7. Dust emission ==")
for defl in (0.20, 0.30):
    t = 1e5 * defl * 1.6
    print(f" deflated share {defl:.0%}: {t:,.0f} t of silt/sand per season = {t/season:,.0f} t/day from {area/1e6:.2f} km2")

print("\n== 8. Gold-loss detectability ==")
# Grade 0.5-1 g/m3, grain mass for 0.1 mm and 1 mm gold
for dmm in (0.1, 0.5, 1.0):
    m = 19300 * math.pi/6 * (dmm/1000)**3 * 1000  # grams
    for grade in (0.5, 1.0):
        n_per_m3 = grade / m
        # to measure 5% loss at 2 sigma from Poisson alone, need N grains with 2/sqrt(N) < 0.05 per arm
        N = (2/0.05)**2
        print(f" gold {dmm} mm ({m*1000:.3f} mg), grade {grade} g/m3: {n_per_m3:,.0f} grains/m3; need {N:.0f} grains/arm -> {N/n_per_m3:.2f} m3/arm (Poisson only)")
# with spatial CV of placer grade 60-100% between 1 m3 samples
for cv in (0.6, 1.0):
    n = (2*cv/0.05)**2
    print(f" spatial grade CV {cv:.0%}: need ~{n:.0f} paired samples to see a 5% loss at 2 sigma")
