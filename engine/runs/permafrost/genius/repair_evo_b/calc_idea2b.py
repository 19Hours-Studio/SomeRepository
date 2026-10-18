"""IDEA 2 round 3: inclined self-cleaning face (10-12 deg) instead of whole-surface 8-10 deg sheet or vertical headwall."""
import math
gsat, gw, phi = 17.5, 9.81, math.radians(28); gp = gsat - gw
E = 194e6                     # J/m3 (calc_idea2)
for beta_d in (10, 12, 14):
    b = math.radians(beta_d)
    for cv in (1e-7, 3e-7):
        X = 3.0; alpha = X/math.sqrt(100*86400); R = alpha/(2*math.sqrt(cv))
        fs = (gp/gsat)/(1+2*R*R)*math.tan(phi)/math.tan(b)
        for c in (0.5, 1.0, 2.0):
            zc = c/(gsat*math.sin(b)*math.cos(b)*(1-fs)) if fs < 1 else float('inf')
            print(f"face {beta_d} deg cv {cv:.0e} R {R:.2f} FS_fric {fs:.2f} c'={c}: self-detaching sheet {zc:.2f} m")
print()
H = 8.0                       # muck thickness
for beta_d, thaw_n in ((10, 3.0), (12, 3.0), (10, 2.0)):
    b = math.radians(beta_d)
    slope_len = H/math.sin(b)
    retreat = thaw_n/math.sin(b)            # horizontal retreat per season
    v_per_m = thaw_n*slope_len               # m3 per m of face per season
    print(f"face {beta_d} deg, normal thaw {thaw_n} m/season: slope length {slope_len:.0f} m, horiz. retreat {retreat:.0f} m/season, "
          f"{v_per_m:.0f} m3 per m face per season")
    for width in (60, 100, 150):
        print(f"   valley pay width {width} m -> longitudinal face swept across in {width/retreat:.1f} seasons; "
              f"for 0.5 Mm3/season need {0.5e6/v_per_m/1e3:.1f} km of face")
# compare: vertical headwall 8 m at 10 m/yr -> 80 m3/m
print("vertical 8 m headwall at 10 m/yr: 80 m3/m/season (half of inclined face)")
# number of dozers replaced: baseline 200 m3/h * 10 h * 100 d = 200k m3/season per dozer
print(f"0.5 Mm3/season baseline needs {0.5e6/(200*20*100):.1f} dozers (2x10h shifts, 100 d); gravity mode keeps ~15-30% cleanup")
