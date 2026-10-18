"""IDEA 2 - Thaw-consolidation gravity stripping.  Anchor: thaw-generated excess pore pressure makes the thawed
ice-rich muck move itself downslope into the mined cell - gravity replaces dozing.

Sources:
 M1 Morgenstern & Nixon (1971) thaw-consolidation ratio R = alpha/(2 sqrt(cv)), X = alpha sqrt(t);
    McRoberts & Morgenstern (1974) infinite thawing slope FS = (g'/g)*(1/(1+2R^2))*tan(phi')/tan(beta)
    (cited in Aga et al., EGUsphere-2026-916 review of ALDF; equations from textbook - flagged K).
 M2 Lewkowicz (Fosheim Pen.): ALDs on slopes 2->40 deg; movement on very low angles needs dynamic loading and
    very low undrained strength from high pore pressure.
 M3 Kizyakov et al. 2024 (Batagay megaslump, Yana Upland): headwall up to 55 m, retreat 5-15 m/yr,
    ~1 Mm3/yr thawed sediment+ice, ground ice up to 87 vol%.
 M4 Yukon/Klondike: hydraulicking/ground-sluicing and natural thaw of muck with monitors is old practice;
    dozer push economic 50-100 m (Ukr. mining journal); baseline fuel 0.30 l/m3 (idea).
 K  textbook: cv of thawed ice-rich silt 1e-8..1e-6 m2/s; phi' 25-30 deg; gamma_sat 17-18 kN/m3;
    thawing index of N-Yakutia (Batagay/Deputatsky) ~1,600-1,800 C*day; kt thawed silt 1.2-1.5 W/mK;
    summer net radiation (Jun-Jul) 100-150 W/m2 mean on S-facing slope.
"""
import math
g_w = 9.81
print("=== 2a. Thaw-consolidation ratio R and critical slope (McRoberts-Morgenstern) ===")
gsat, phi = 17.5, math.radians(28)
gp = gsat - g_w
for X_season, label in ((1.6, "graded surface, thawed layer left in place"), (3.0, "sprinkled + thin layer removed")):
    t = 100 * 86400
    alpha = X_season / math.sqrt(t)
    for cv in (1e-8, 1e-7, 1e-6):
        R = alpha / (2 * math.sqrt(cv))
        tanb = (gp / gsat) * (1 / (1 + 2 * R * R)) * math.tan(phi)
        print(f"{label:44s} X={X_season} m/100d alpha={alpha:.2e} cv={cv:.0e} R={R:5.2f} -> beta_crit={math.degrees(math.atan(tanb)):5.1f} deg")

print("\n=== 2b. Cohesion: minimum sheet thickness to slide at the graded angle (R=1) ===")
R = 1.0
for beta_d in (5, 8, 10):
    b = math.radians(beta_d)
    fs_fric = (gp / gsat) * (1 / (1 + 2 * R * R)) * math.tan(phi) / math.tan(b)
    for c in (0.5, 2.0, 5.0):
        if fs_fric >= 1:
            print(f"beta {beta_d} deg: frictional FS {fs_fric:.2f} >= 1 -> never slides"); break
        z = c / (gsat * math.sin(b) * math.cos(b) * (1 - fs_fric))
        print(f"beta {beta_d:2d} deg c'={c} kPa: frictional FS {fs_fric:.2f}; sheet must be >= {z:4.2f} m thick")

print("\n=== 2c. Throughput limited by energy: graded sheet vs engineered headwall (thaw slump) ===")
ice_vol = 0.6
Lv = ice_vol * 917 * 334e3          # J per m3 frozen muck (latent only)
sens = 2.0e6 * 5                    # warm 5 K? (frozen at -3..-5 -> 0, plus thawed to +2): ~10 MJ/m3
E = Lv + sens
print(f"energy to thaw 1 m3 muck at 60% ice: {E/1e6:.0f} MJ")
# graded surface: Stefan conduction-limited through own thawed layer
I_t = 1700 * 1.3 * 86400            # surface thawing index (n=1.3 bare) in C*s
kt = 1.3
X = math.sqrt(2 * kt * I_t / E)
print(f"graded surface Stefan thaw per season: {X:.2f} m  (only removed when it slides: once per season)")
# headwall (slump) mode: ablation-limited, face kept bare
for q in (60, 100, 150):
    abl = q * 100 * 86400 / E
    print(f"headwall face heat flux {q} W/m2 -> ablation {abl:.1f} m/season horizontal (Batagay obs 5-15 m/yr)")
# sprinkled creek water: heat from 10 C water cooling to 1 C
w_heat = 4.18e6 * 9
print(f"creek water (10->1 C) melts {w_heat/E:.2f} m3 muck per m3 water; a 0.2 m3/s creek over 100 d -> "
      f"{0.2*86400*100*w_heat/E/1e3:.0f} k m3/season extra")

print("\n=== 2d. Scale: headwall length needed for a 1 Mm3/yr placer stripping programme ===")
for H in (5, 8, 12):
    for retreat in (5, 10):
        L = 1e6 / (H * retreat)
        print(f"muck {H:2d} m, retreat {retreat:2d} m/yr -> headwall length {L/1e3:.1f} km (Batagay: ~1 Mm3/yr natural)")

print("\n=== 2e. Runout: does the slurry reach the mined cell? Bingham stop condition tau_y = rho g h sin(beta) ===")
rho = 1650
for ty in (200, 500, 1000):
    for h in (0.3, 0.6):
        s = ty / (rho * g_w * h)
        print(f"tau_y {ty:4d} Pa, flow {h} m -> stops below {math.degrees(math.asin(min(s,1))):4.1f} deg")
# thawed volume shrink: 60% ice -> excess water drains; solids+pore at ~45% porosity
solids = 1 - ice_vol - 0.05
consol = solids / (1 - 0.45)
print(f"consolidated volume of 1 m3 frozen muck after thaw: {consol:.2f} m3 -> fits in mined cell volume (pay+muck) easily")

print("\n=== 2f. Cost per gram Au recovered: stripping line ===")
grade, rec = 0.7, 0.85   # g/m3 sands, plant recovery (typical Russian placer)
SR = 7.5                 # m3 muck per m3 sands (5-10, idea)
cases = {
  "dozer layer-by-layer natural thaw (cheapest current)": 1.00,  # $/m3: 200 m3/h D375-class ~$200/h incl 0.3 l/m3 fuel
  "hydraulic monitor stripping / ground sluicing": 0.60,          # cheap where water & gradient; sediment licence limits
  "excavator+truck frozen, drill/blast": 3.50,
  "gravity: graded sheet (2a-2c) + 30% dozer cleanup": 0.20 + 0.30*1.00,
  "gravity: engineered slump headwall + sprinkling + 15% cleanup": 0.15 + 0.15*1.00,
}
for k, c in cases.items():
    print(f"{k:62s} ${c:4.2f}/m3 muck -> ${c*SR/(grade*rec):6.2f}/g Au")
total_other = 45.0   # $/g Au: sands mining, washing, camp, G&A, royalties (Russian placer AISC ~$60/g total - K)
base = 1.00*SR/(grade*rec) + total_other
grav = (0.15+0.15)*SR/(grade*rec) + total_other
print(f"total cost/g: baseline {base:.0f}, slump-gravity {grav:.0f} -> saving {100*(1-grav/base):.0f}% of delivered cost")
