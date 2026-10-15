"""Idea 1 - Spring sun-wind deflation placer.  Binding quantities:
 (a) net sublimation rate of a dark, harrowed, ice-cemented gravel surface in spring, WITHOUT melting
 (b) snow (fall + drift) arriving on the field vs that budget
 (c) wind window: quartz sand leaves, gold (incl. fine flakes) never suspends
 (d) sand-flux capacity vs supply (fetch limit)
 (e) cost per m3 and per gram recovered vs best practice
Sources (see NOTES.md): Pevek normals (Wikipedia climate table: Mar -21.4, Apr -14.3, May -2.2 C mean,
 May mean max +1.0 C; spring driest, 2-3 wet days/month); North Slope EC snow sublimation 0.06-0.15 mm/d;
 Shao & Lu 2000 threshold; Kawamura 1951 flux; Tabler snow-fence capacity; NOAA Barrow snow-off ~ early June.
"""
import math, numpy as np

# ---------- (a) hourly surface energy balance with 1-D ground conduction ----------
LAT = 69.7          # Pevek / Chaun placer district
S0 = 1361.0
sigma = 5.67e-8
Ls = 2.834e6        # J/kg latent heat of sublimation
cp = 1005.0
kappa = 0.4

def esat_ice(Tc):   # Pa, Murphy-Koop approx (Magnus over ice)
    return 611.15*math.exp(22.452*Tc/(272.55+Tc))

def decl(doy):
    return math.radians(23.44)*math.sin(2*math.pi*(284+doy)/365)

def sw_down(doy, hour, tau=0.72, cloud=0.0):
    d = decl(doy); phi = math.radians(LAT)
    h = math.radians(15*(hour-12))
    cz = math.sin(phi)*math.sin(d)+math.cos(phi)*math.cos(d)*math.cos(h)
    if cz <= 0.01: return 0.0
    clear = S0*cz*tau**(1/cz)
    return clear*(1-0.6*cloud**2)   # Kasten-Czeplak-like cloud reduction

def run_day(doy, Ta_mean, Ta_amp, U10, RH_ice, albedo=0.10, z0=1e-3, cloud=0.4,
            k_g=1.8, C_g=1.9e6, T_deep=-12.0, days=6, dry_layer=None, D_eff=6e-6, verbose=False):
    """Explicit 1-D conduction into frozen gravel; returns daily sublimation (kg/m2/d), Tsmax, melt energy."""
    nz, dz = 60, 0.025
    T = np.linspace(Ta_mean, T_deep, nz)
    dt = 60.0
    alpha = k_g/C_g
    assert alpha*dt/dz**2 < 0.5
    CH = kappa**2/(math.log(10/z0)*math.log(10/(z0/10)))
    out = []
    for day in range(days):
        E_day = 0.0; Tsmax = -99; melt = 0.0
        for step in range(int(86400/dt)):
            hour = step*dt/3600
            Ta = Ta_mean + Ta_amp*math.cos(2*math.pi*(hour-14)/24)
            TaK = Ta+273.15
            ea = RH_ice*esat_ice(Ta)
            eps_clear = 1.24*((ea/100)/TaK)**(1/7)
            eps = eps_clear*(1-cloud**2)+cloud**2*0.98
            LWd = eps*sigma*TaK**4
            SWn = (1-albedo)*sw_down(doy, hour, cloud=cloud)
            # solve surface temperature from flux balance with top-cell conduction (Newton)
            Ts = T[0]
            rho = 101325/(287*TaK)
            for _ in range(30):
                TsK = Ts+273.15
                qs = 0.622*esat_ice(min(Ts,0))/101325; qa = 0.622*ea/101325
                Ri = 9.81/TaK*(Ta-Ts)*10/U10**2
                fst = (1-10*Ri/(1+75*CH*math.sqrt(10/z0*abs(Ri)))) if Ri < 0 else 1/(1+15*Ri*math.sqrt(1+5*Ri))
                CHs = CH*fst
                Hs = rho*cp*CHs*U10*(Ts-Ta)
                if dry_layer:   # vapour must diffuse through a dry lag of thickness dry_layer
                    rv_s = esat_ice(min(Ts,0))/(461.5*TsK); rv_a = ea/(461.5*TaK)
                    E = (rv_s-rv_a)/(dry_layer/D_eff + 1/(CHs*U10))
                else:
                    E = rho*CHs*U10*(qs-qa)
                LE = Ls*E
                G = k_g*(Ts-T[1])/dz
                F = SWn+LWd-0.97*sigma*TsK**4-Hs-LE-G
                dF = -4*0.97*sigma*TsK**3-rho*cp*CHs*U10-k_g/dz - Ls*rho*CHs*U10*0.622/101325*esat_ice(min(Ts,0))*22.452*272.55/(272.55+Ts)**2
                Ts_new = Ts - F/dF
                if abs(Ts_new-Ts) < 1e-4: Ts = Ts_new; break
                Ts = Ts_new
            if Ts > 0:      # cap at melting: excess goes to melt (violates "no liquid water")
                Ts0 = 0.0; TsK = 273.15
                qs = 0.622*esat_ice(0)/101325
                E = rho*CHs*U10*(qs-0.622*ea/101325) if not dry_layer else E
                Hs = rho*cp*CHs*U10*(Ts0-Ta); G = k_g*(Ts0-T[1])/dz
                Fm = SWn+LWd-0.97*sigma*TsK**4-Hs-Ls*E-G
                melt += max(Fm,0)*dt; Ts = 0.0
            T[0] = Ts
            T[1:-1] = T[1:-1] + alpha*dt/dz**2*(T[2:]-2*T[1:-1]+T[:-2])
            E_day += E*dt; Tsmax = max(Tsmax, Ts)
        out.append((E_day, Tsmax, melt/334e3))
    return out[-1]

# Pevek normals (Wikipedia): Mar -21.4 (max -17.2), Apr -14.3 (max -10.3), May -2.2 (max +1.0)
periods = [("Mar 25", 84, -21.0, 4.0), ("Apr 15", 105, -14.3, 4.0), ("May 5", 125, -6.0, 4.5), ("May 20", 140, -2.0, 3.5)]
print("=== (a) sublimation of dark harrowed frozen gravel, U10=6 m/s, RH_ice=0.85, cloud=0.4 ===")
res = {}
for name, doy, Tm, amp in periods:
    for alb in (0.10, 0.80):
        E, Tsmax, meltmm = run_day(doy, Tm, amp, 6.0, 0.85, albedo=alb)
        res[(name, alb)] = (E, Tsmax, meltmm)
        print(f"{name} albedo {alb:.2f}: net sublimation {E:5.2f} mm w.e./d, Ts max {Tsmax:5.1f} C, melt {meltmm:5.2f} mm/d")
print("check vs measured snow sublimation (albedo 0.8 case) North Slope EC: 0.06-0.15 mm/d")

print("\n--- sensitivity (Apr 15) ---")
for U in (3, 6, 9):
    for RH in (0.7, 0.85, 1.0):
        E, Tsmax, m = run_day(105, -14.3, 4.0, U, RH)
        print(f"U10={U} RH_ice={RH}: E={E:5.2f} mm/d Tsmax={Tsmax:5.1f}")

print("\n--- dry lag limit (Apr 15, U=6): vapour through a freed-grain layer, D_eff=6e-6 m2/s ---")
for dl in (0.001, 0.003, 0.01, 0.03):
    E, Tsmax, m = run_day(105, -14.3, 4.0, 6.0, 0.85, dry_layer=dl)
    print(f"dry layer {dl*1000:4.0f} mm: E={E:5.2f} mm/d")

# ---------- season integration, with ALBEDO CONTROL (repair) ----------
# Repair: the surface albedo is a control knob (fresh-harrowed wet-dark gravel ~0.10; raked freeze-dried
# lag ~0.30; lag left 2-3 d with silt skin ~0.40). Each day pick the darkest albedo that keeps melt < 0.2 mm/d.
SITES = {
 # name: lat, Ta(doy) knots, amp, U10, RH_ice, cloud, snowfall mm/month
 "Pevek coast (Chaun placers)": (69.7, ([74,90,105,120,135,151],[-23.5,-19.5,-14.3,-8.5,-3.0,1.5]), 4.0, 6.0, 0.85, 0.40, 6.0),
 "Upper Kolyma/Indigirka upland": (63.5, ([74,90,105,120,135,151],[-22.0,-16.0,-9.0,-3.0,3.0,8.0]), 7.0, 3.5, 0.70, 0.30, 8.0),
}
summary = {}
for site, (lat, knots, amp, U, RH, cl, sf) in SITES.items():
    LAT = lat
    tot_fixed = 0; tot_ctrl = 0; days_ok = 0; rows = []
    for doy in range(74, 160, 4):
        Tm = float(np.interp(doy, *knots))
        E10, Tx10, m10 = run_day(doy, Tm, amp, U, RH, albedo=0.10, cloud=cl, days=3)
        best = None
        for alb in (0.10, 0.20, 0.30, 0.40, 0.55):
            E, Tx, m = run_day(doy, Tm, amp, U, RH, albedo=alb, cloud=cl, days=3)
            if m < 0.2:
                best = (alb, E, Tx, m); break
        if m10 < 0.2: tot_fixed += 4*E10
        if best and best[1] > 0:
            tot_ctrl += 4*best[1]; days_ok += 4
        rows.append((doy, Tm, E10, m10, best))
    print(f"\n=== {site}: lat {lat}, U10 {U}, RH_ice {RH}, cloud {cl}")
    for r in rows:
        b = r[4]
        bs = f"alb {b[0]:.2f} E {b[1]:5.2f} Tsmax {b[2]:5.1f}" if b else "melts at any albedo<=0.55"
        print(f" doy {r[0]:3d} Ta {r[1]:6.1f} | dark: E {r[2]:5.2f} melt {r[3]:5.2f} | controlled: {bs}")
    snowfall = sf*days_ok/30
    print(f" season gross sublimation: fixed dark {tot_fixed:.1f} mm; albedo-controlled {tot_ctrl:.1f} mm over {days_ok} d; snowfall on field {snowfall:.1f} mm (cleared by blade after each event)")
    summary[site] = (tot_ctrl, days_ok)

LAT = 69.7
# ---------- freed gravel and area ----------
site = max(summary, key=lambda k: summary[k][0])
E_gross, ndays = summary[site]
lag_eff = 0.6     # coarse lag/dry skin between rakes cuts the bare-ice rate (dry-layer runs above: 1 mm -> ~0.5x)
E_net = E_gross*lag_eff
print(f"\nbest site: {site}: gross {E_gross:.1f} mm, effective (lag factor {lag_eff}) {E_net:.1f} mm w.e./season, {ndays} d")
for theta in (0.10, 0.15, 0.20, 0.30):
    print(f"  pore ice {theta}: freed gravel {E_net/917/theta*1000:.0f} mm/season")
theta = 0.12      # repair: drained tailings dumps / autumn-ditched cut, measured target 0.10-0.15
free_season = E_net/917/theta
area_needed = 100000/free_season
print(f"area for 100,000 m3/yr at pore ice {theta}: {area_needed/1e6:.2f} km2 (claimed 0.21 m/yr, 0.5 km2)")

# ---------- (c) wind window: thresholds (Shao & Lu 2000) ----------
rho_a = 1.38; g = 9.81; AN = 0.0123; gam = 3e-4
def ut(rho_p, d):
    return math.sqrt(AN*(rho_p/rho_a*g*d + gam/(rho_a*d)))
print("\n(c) threshold friction velocity u*t (m/s)")
for d in (20e-6, 63e-6, 100e-6, 250e-6, 500e-6, 1000e-6):
    print(f"  quartz {d*1e6:5.0f} um: {ut(2650,d):.3f}    gold sphere {d*1e6:5.0f} um: {ut(19300,d):.3f}")
def eqd(D, t): return (1.5*D*D*t)**(1/3)
for D, t in ((150e-6, 10e-6), (300e-6, 20e-6), (75e-6, 5e-6)):
    de = eqd(D, t)
    print(f"  gold flake {D*1e6:.0f}x{t*1e6:.0f} um -> eq sphere {de*1e6:.0f} um, u*t(sphere) {ut(19300,de):.3f}; flake (drag x2.5) ~{ut(19300,de)/1.6:.3f}")
def ustar(U10, z0): return kappa*U10/math.log(10/z0)
for U in (4, 5, 6, 7, 8, 10):
    print(f"  U10 {U:2d} m/s -> u* {ustar(U,1e-3):.2f} (z0 1 mm); gust x1.5 -> {ustar(1.5*U,1e-3):.2f}")
mu = 1.6e-5
for d in (30e-6, 50e-6, 100e-6):
    vs = 19300*g*d**2/(18*mu)
    print(f"  gold {d*1e6:.0f} um Stokes settling {vs:.2f} m/s vs u* 0.3 -> Rouse {vs/(0.4*0.3):.0f}: never suspended")

# ---------- (d) sand flux capacity vs supply (fetch) ----------
def kawamura(us, ust):
    if us <= ust: return 0
    r = ust/us
    return 2.78*rho_a/g*us**3*(1-r)*(1+r)**2
for U in (5, 6, 7):
    q = kawamura(ustar(U, 1e-3), 0.23)
    cap_day = q*3600*12          # 12 h/d at that wind
    supply = free_season/ndays*0.40*1700   # kg/m2/d of sand+silt freed
    print(f"(d) U10 {U}: saltation capacity {q*1000:.1f} g/m/s -> {cap_day/1000:.2f} t/m/d; supply {supply:.2f} kg/m2/d -> max fetch {cap_day/supply:.0f} m")

# ---------- (e) cost per m3 and per gram ----------
A = area_needed
days = ndays
tractor_h = 90.0     # 300 hp tractor + 12 m harrow or rake (ownership+fuel+operator), $/h
pass_h = A/(12*8e3*0.8)
n_pass = days*2 + 6   # harrow + rake windrow daily, + 6 snow-clear passes
cost_field = pass_h*n_pass*tractor_h
cost_snow = A*0.35*0.5          # plough off 0.35 m spring snow once, $0.5/m3
cost_fence = 4*math.sqrt(A)*15  # snow fences on windward sides, $15/m/yr
residue = 0.25*100000
cost_lag = residue*1.0           # load windrowed lag, short haul, $1/m3
wash = 6.0                        # $/m3 summer feed+wash (baseline, NOTES)
cost_wash = residue*wash
cost_trap = 30000                 # downwind low saltation trap lip + sampling of trapped sand for gold
total = cost_field+cost_snow+cost_fence+cost_lag+cost_wash+cost_trap
print(f"\n(e) area {A/1e6:.2f} km2; pass {pass_h:.1f} h; field ${cost_field:,.0f}; snow ${cost_snow:,.0f}; fence ${cost_fence:,.0f};"
      f" lag load ${cost_lag:,.0f}; wash residue ${cost_wash:,.0f}; trap ${cost_trap:,.0f}")
unit = total/1e5
print(f" TOTAL ${total:,.0f}/yr -> ${unit:.2f} per m3 of pay gravel processed")
# baselines per m3 (NOTES): (1) tailings re-treatment, excavator+mobile trommel/sluice $4.0/m3;
# (2) conventional bulldozer-sluice summer feed+wash $6.0/m3;  (3) dredge where thawed & boulder-free $2.5/m3
for label, grade, base in (("old tailings", 0.25, 4.0), ("thin-overburden cut", 0.6, 6.0)):
    rec_new = 0.80   # fine/flaky gold partly lost in gusts / trapped sand (unknown; target 0.80-0.90)
    rec_base = 0.80
    c_new = unit/(grade*rec_new); c_base = base/(grade*rec_base)
    print(f" {label} {grade} g/m3: deflation ${c_new:.1f}/g recovered vs best practice ${c_base:.1f}/g -> {c_base/c_new:.2f}x")

# ---------- best-regime variant: wind-scoured bench/tailings site, low pore ice ----------
print("\n=== best regime: wind-scoured bench or old-dump surface, pore ice 0.08-0.12, light snow skim only ===")
for theta in (0.08, 0.12):
    fs = E_net/917/theta; A2 = 100000/fs
    ph = A2/(12*8e3*0.8)
    field = ph*(ndays*2+6)*tractor_h
    snow = A2*0.10*0.3            # skim 0.10 m wind-packed residual snow, $0.3/m3
    fence = 2*math.sqrt(A2)*15
    tot = field+snow+fence+cost_lag+cost_wash+cost_trap
    u = tot/1e5
    print(f" theta {theta}: freed {fs*1000:.0f} mm/yr, area {A2/1e6:.2f} km2, cost ${u:.2f}/m3 -> vs $6.0 bulldozer-sluice {6.0/u:.2f}x, vs $4.0 tailings trommel {4.0/u:.2f}x")
# thermal drying alternative for dry (waterless) concentration: evaporate pore ice/water
for theta in (0.08, 0.12):
    q = theta*1000*2.6e6/0.6     # J per m3, 60% dryer efficiency
    L = q/36e6                   # litres diesel (36 MJ/L)
    print(f" thermal drying of thawed gravel with {theta*100:.0f}% water: {L:.1f} L diesel/m3 = ${L*0.9:.1f}/m3 (fuel only) -> freeze-drying replaces this")
