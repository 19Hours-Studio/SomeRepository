"""Checks for Ideas 4, 5, 6 (freeze-dry deflation placers)."""
import math

print("=== IDEA 4: slope irradiance at Tiksi (71.6 N), 37 deg south face ===")
lat = math.radians(71.6)
tilt = math.radians(37.0)
albedo_snow = 0.8

def decl(doy):
    return math.radians(23.45) * math.sin(2 * math.pi * (284 + doy) / 365)

def day_integrals(doy, kd):
    """Return daily horizontal and tilted totals (relative units) for a clear-ish sky with diffuse fraction kd.
    Beam on horizontal ~ sin(h) * tau^(1/sin h) (simple air-mass attenuation)."""
    d = decl(doy)
    H = 0.0
    T = 0.0
    beam_h = 0.0
    for i in range(1440):
        w = math.radians((i / 1440.0) * 360 - 180)  # hour angle
        sinh = math.sin(lat) * math.sin(d) + math.cos(lat) * math.cos(d) * math.cos(w)
        if sinh <= 0.02:
            continue
        am = 1 / sinh
        Ib = 1361 * 0.75 ** am            # beam normal (clear sky)
        # incidence on south-facing slope tilted 37 deg
        cosi = (math.sin(lat - tilt) * math.sin(d) + math.cos(lat - tilt) * math.cos(d) * math.cos(w))
        bh = Ib * sinh
        bt = Ib * max(cosi, 0.0)
        beam_h += bh
        T += bt
    # build global with diffuse fraction kd: G = B/(1-kd); D = kd*G
    G = beam_h / (1 - kd)
    D = kd * G
    Gt = T + D * (1 + math.cos(tilt)) / 2 + albedo_snow * G * (1 - math.cos(tilt)) / 2
    Gt_noref = T + D * (1 + math.cos(tilt)) / 2
    return G, Gt, Gt_noref, T / beam_h

for doy, label in ((74, "Mar 15"), (90, "Mar 31"), (100, "Apr 10"), (110, "Apr 20")):
    for kd in (0.3, 0.5, 0.7):
        G, Gt, Gn, rb = day_integrals(doy, kd)
        print(f"{label} kd={kd}: beam ratio {rb:.2f}; global ratio tilted/horizontal {Gt/G:.2f} (incl. snow reflection), {Gn/G:.2f} (no reflection)")
# noon ratio
for doy, label in ((80, "Mar 21"), (110, "Apr 20")):
    d = decl(doy)
    h = math.pi / 2 - lat + d
    inc = abs((math.pi / 2 - tilt) - h)
    print(f"{label}: noon sun elevation {math.degrees(h):.1f}, noon beam ratio {math.cos(inc)/math.sin(h):.2f}")

# area check
for retreat in (0.02, 0.09, 0.11):
    print(f"face retreat {retreat} m -> {100000/retreat/1e6:.2f} km2 face for 100,000 m3")
print("0.9 km2 / 213 km =", 0.9e6 / 213e3, "m face slant per m ridge -> ridge height", 0.9e6 / 213e3 * math.sin(tilt), "m")
for pore in (0.06, 0.15, 0.30):
    print(f"5.2 kg/m2 sublimation with pore ice {pore}: retreat {5.2/(pore*917):.3f} m")
print("Mar 0.08-0.13 x31 =", 0.08 * 31, 0.13 * 31, "; Apr1-20 0.41-0.67 x20 =", 0.41 * 20, 0.67 * 20,
      "; sum", 0.08 * 31 + 0.41 * 20, 0.13 * 31 + 0.67 * 20)

print("\n=== IDEA 5/6: wind thresholds (Shao & Lu 2000) ===")
rho_a = 1.40  # cold air
def ustar_t(d, rho_p):
    AN, gamma = 0.0123, 3e-4
    return math.sqrt(AN * (rho_p / rho_a * 9.81 * d + gamma / (rho_a * d)))
for d in (25e-6, 63e-6, 100e-6, 250e-6, 500e-6):
    print(f"d={d*1e6:.0f} um: quartz u*t={ustar_t(d,2650):.3f}, gold sphere u*t={ustar_t(d,19300):.3f} m/s")
def ustar(U10, z0):
    return 0.4 * U10 / math.log(10 / z0)
for U in (7, 8, 15, 20, 30, 40):
    print(f"U10={U} m/s: u* = {ustar(U,1e-4):.2f} (z0=0.1mm) / {ustar(U,1e-3):.2f} (1mm) / {ustar(U,5e-3):.2f} (5mm)")

# settling velocity with realistic drag (Ferguson & Church style for air): iterate Cd = 24/Re(1+0.15Re^0.687)
mu = 1.62e-5
def ws(d, rho_p):
    w = rho_p * 9.81 * d * d / (18 * mu)
    for _ in range(200):
        Re = rho_a * w * d / mu
        Cd = 24 / max(Re, 1e-9) * (1 + 0.15 * Re ** 0.687)
        w_new = math.sqrt(4 * rho_p * 9.81 * d / (3 * Cd * rho_a))
        w = 0.5 * w + 0.5 * w_new
    return w
print("\nSettling velocities in air (sphere, non-Stokes drag)")
for d in (10e-6, 20e-6, 30e-6, 50e-6, 100e-6):
    print(f"gold d={d*1e6:.0f} um: Stokes {19300*9.81*d*d/(18*mu):.2f} m/s, drag-corrected {ws(d,19300):.2f} m/s; quartz {ws(d,2650):.3f} m/s")
# flake: 100 um diameter x 10 um thick -> volume-equivalent sphere, shape factor penalty ~0.5
d_eq = (1.5 * (100e-6) ** 2 * 10e-6) ** (1 / 3)
print(f"flake 100x10 um: volume-equivalent sphere {d_eq*1e6:.0f} um, sphere ws {ws(d_eq,19300):.2f} m/s; with shape factor 0.4-0.6 -> {0.4*ws(d_eq,19300):.2f}-{0.6*ws(d_eq,19300):.2f} m/s")

print("\n=== IDEA 5 season and area ===")
for wq in (0.4, 0.7):
    for pore in (0.15, 0.30):
        print(f"{wq} mm w.e./day, pore ice {pore}: frees {wq*1.09/pore:.1f} mm/day gravel")
days = (31 - 15 + 1) + 30 + 10
print("Mar15-May10 days =", days, "; 2.5-5 mm/d ->", 2.5 * days, 5 * days, "mm")
print("0.4-0.7 mm w.e./day x", days, "d =", 0.4 * days, 0.7 * days, "mm w.e. vs idea 6 model 13 x 0.6 =", 13 * 0.6)
print("idea-5 total vs idea-6 total ratio:", 0.4 * days / 7.8, 0.7 * days / 7.8)
print("area 100,000/0.21 =", 100000 / 0.21 / 1e6, "km2")

print("\n=== IDEA 6 ===")
for pore in (0.08, 0.15):
    fr = 7.8 * 1.09 / pore
    print(f"7.8 mm w.e. with pore ice {pore}: {fr:.0f} mm gravel -> {100000/(fr/1000)/1e6:.2f} km2")
# cost per gram check
for c, g in ((3.7, 8), (4.5, 9), (6.0, 12.5)):
    print(f"${c}/m3 / ${g}/g -> implied recovered grams {c/g:.2f} g/m3 (grade 0.6 -> recovery {c/g/0.6:.2f})")
