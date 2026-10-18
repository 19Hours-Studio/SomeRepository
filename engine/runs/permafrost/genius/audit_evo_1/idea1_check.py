import math
d=math.radians
print("=== IDEA 1: thaw-slide checks ===")
# McRoberts & Morgenstern thawing infinite slope: F = c'/(g z sin b cos b) + (g'/g) tan(phi)/((1+2R^2) tan b)
for gp_g in (0.40,0.45,0.50):
  for phi in (25,28,30,33):
    for R in (0.9,1.6):
      tb=gp_g*math.tan(d(phi))/(1+2*R*R)
      print(f"g'/g={gp_g} phi={phi} R={R}: frictional threshold beta={math.degrees(math.atan(tb)):.2f} deg")
# cohesion threshold thickness
g=16.5 # kN/m3 thawed ice-rich muck
def zcrit(c,beta,R,gp_g=0.45,phi=28):
  b=d(beta)
  fric=gp_g*math.tan(d(phi))/((1+2*R*R)*math.tan(b))
  if fric>=1: return float('inf')
  return c/(g*math.sin(b)*math.cos(b)*(1-fric))
for beta in (5,8,10,12):
  for c in (0.5,2.0):
    print(f"beta={beta} c={c}: zcrit R0.9={zcrit(c,beta,0.9):.2f} m, R1.6={zcrit(c,beta,1.6):.2f} m")
# Thaw rate under periodic detachment (Stefan from 0 to h_d each cycle)
k=1.3 # W/mK thawed silt
season=100*86400
for ice_vol,label in ((0.35,'ordinary muck'),(0.5,'ice-rich'),(0.65,'yedoma >60% ice'),(0.8,'yedoma with wedges')):
  L=334e6*ice_vol*0.917/0.917  # J/m3 (volumetric latent heat ~ 306 MJ/m3 of ice * vol frac); use 306
  L=306e6*ice_vol
  for Ts in (8,10,12):
    for hd in (0.2,0.45,0.9):
      t_cycle=L*hd*hd/(2*k*Ts)
      rate=hd/t_cycle  # m/s
      print(f"{label:20s} Ts={Ts} hd={hd}: cycle {t_cycle/86400:5.1f} d, thaw/season {rate*season:5.2f} m, mean flux {k*Ts/(hd/2)*0+L*rate:6.1f} W/m2")
# natural single-season Stefan thaw
for ice_vol in (0.35,0.5,0.65):
  L=306e6*ice_vol
  for I in (1300,1700,2000):
    X=math.sqrt(2*k*I*86400/L)
    print(f"natural thaw ice {ice_vol} I={I} degC-d: {X:.2f} m")
# geometry: 3 m normal thaw at 10-12 deg face -> implied overburden
for beta in (10,11,12):
  for Y in (115,138):
    H=Y*math.sin(d(beta))/3.0
    print(f"beta={beta} Y={Y} m3/m: implied overburden H={H:.1f} m, face slope length {H/math.sin(d(beta)):.0f} m")
print("face for 0.5Mm3:",0.5e6/138,0.5e6/115)
# Bingham slurry flow condition: tau_y < rho g h sin(beta)
for rho in (1500,1700):
  for beta in (4,):
    for ty in (200,500,1000,2000):
      print(f"rho={rho} beta={beta} tau_y={ty}: min flowing thickness {ty/(rho*9.81*math.sin(d(beta))):.2f} m")
# carrying cost of 4-9 seasons pre-stripping
for r in (0.10,0.15,0.20):
  for n in (4,9):
    print(f"r={r} lead={n} yr: $0.30 now -> ${0.30*(1+r)**n:.2f}/m3 at mining; ratio vs $1.0 (1-yr lead {1.0*(1+r):.2f}): {1.0*(1+r)/(0.30*(1+r)**n):.2f}x")
# heat flux needed: 0.5 Mm3 per season over face area
for ice_vol in (0.35,0.5,0.65):
  L=306e6*ice_vol
  E=0.5e6*L
  area=4000*42  # m2 (face slope length ~42 m)
  print(f"ice {ice_vol}: energy {E:.2e} J, mean flux needed {E/season/area:.0f} W/m2 over {area:.0f} m2")
# meltwater released
for ice_vol in (0.35,0.5,0.65):
  print(f"ice {ice_vol}: water released per 0.5Mm3 ~ {0.5e6*ice_vol*0.917:.0f} m3")
