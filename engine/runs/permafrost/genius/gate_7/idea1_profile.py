# Idea 1 follow-up: peak |Tzz| along a profile (not just lens centre), depth sensitivity
import math, importlib.util, sys
spec = importlib.util.spec_from_file_location("calc", "calc.py")
G = 6.674e-11
def prism_gz(x1, x2, y1, y2, z1, z2, rho):
    s = 0.0
    for i, x in enumerate((x1, x2)):
        for j, y in enumerate((y1, y2)):
            for k, z in enumerate((z1, z2)):
                mu = (-1) ** (i + j + k)
                r = math.sqrt(x*x + y*y + z*z)
                s += mu * (z * math.atan2(x*y, z*r) - x*math.log(r + y) - y*math.log(r + x))
    return -G * rho * s
def tzz_at(x0, mass_t, thick, ztop, drho, rho_c=1.35, hlo=0.5, hhi=1.5):
    s = math.sqrt(mass_t / rho_c / thick) / 2
    glo = prism_gz(-s - x0, s - x0, -s, s, ztop + hlo, ztop + thick + hlo, drho)
    ghi = prism_gz(-s - x0, s - x0, -s, s, ztop + hhi, ztop + thick + hhi, drho)
    return (glo - ghi) / (hhi - hlo) / 1e-9
for m, th in [(3000, 3.0), (3000, 2.0), (10000, 3.0)]:
    for zt in (3.0, 4.5, 6.0):
        for drho in (-1350, -950):
            prof = [abs(tzz_at(x, m, th, zt, drho)) for x in [i * 0.5 for i in range(0, 80)]]
            pk = max(prof)
            print(f"M={m} t th={th} m top={zt} m drho={drho}: centre {prof[0]:.1f} E, peak {pk:.1f} E, "
                  f"margin vs 60 E (SNR3@20E) {pk/60:.2f}, vs 100 E (SNR5) {pk/100:.2f}")
