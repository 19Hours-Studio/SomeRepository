import math
from math import erf, erfc
def brentq(f,a,b,tol=1e-14):
    fa=f(a); fb=f(b)
    for _ in range(300):
        m=0.5*(a+b); fm=f(m)
        if fa*fm<=0: b,fb=m,fm
        else: a,fa=m,fm
        if b-a<tol: break
    return 0.5*(a+b)
print("=== IDEA 2 ===")
# Neumann two-phase thaw under reservoir: surface T_w, initial ground T0, latent L
def neumann(Tw,T0,ku,kf,Cu,Cf,L,t):
    au=ku/Cu; af=kf/Cf
    def f(lam):
        return (ku*Tw*math.exp(-lam**2/au)/(math.sqrt(math.pi*au)*erf(lam/math.sqrt(au)))
                + kf*T0*math.exp(-lam**2/af)/(math.sqrt(math.pi*af)*erfc(lam/math.sqrt(af)))
                - L*lam)
    lam=brentq(f,1e-9,1e-2)
    return 2*lam*math.sqrt(t)
yr=365.25*86400
t=40*yr
for ice in (0.15,0.25,0.35):
  L=306e6*ice
  for T0 in (-2,-4,-6):
    res=[neumann(Tw,T0,1.8,2.4,2.6e6,2.0e6,L,t) for Tw in (1,2,3,4)]
    print(f"ice {ice} T0 {T0}: talik after 40 yr at Tw=1,2,3,4: "+", ".join(f"{x:.1f}" for x in res))
# section 8 m + 0.5-1.0 m bedrock cleanup
print("needed thaw depth for 8 m section incl 0.5-1 m bedrock: 8.5-9.0 m")
# dredge utilisation
for days in (82,120,138):
  print(f"{days} d at 600 m3/h 24h: {600*24*days/1e6:.2f} Mm3; util for 1.2 Mm3 = {1.2e6/(600*24*days):.0%}")
# depth window
for start_above_UMO in (0, 14, 17):
  for floor_below_UMO in (1.5,25):
    for rise in (0,19.5):
      d=start_above_UMO+floor_below_UMO+rise+8
      print(f"level at start UMO+{start_above_UMO}, floor UMO-{floor_below_UMO}, seasonal rise {rise}: max dredge depth to base of 8 m section = {d:.1f} m")
# plume: fines escape mass and dilution
for fines in (0.15,0.3):
  for esc in (0.005,0.013,0.05):
    solids=1.2e6*1.9  # t
    m=solids*fines*esc*1e9 # mg over season? -> mg
    rate=m/(120*86400)  # mg/s
    for Q in (300,480,1500):
      c=rate/(Q*1000) # mg/L
      print(f"fines {fines} esc {esc:.3f}: {solids*fines*esc/1e3:.1f} kt; fully mixed in Q={Q} m3/s -> +{c:.2f} mg/L")
# local plume near dredge: escape rate per hour vs mixing volume
for esc in (0.005,0.013):
  kg_s=600*1.9*1000/3600*0.3*esc  # kg/s of fines escaping at full rate (fines 30%)
  print(f"escape {esc}: {kg_s:.2f} kg/s fines at the cut; to stay <=0.25 mg/L needs dilution flow {kg_s*1e6/0.25/1000:.0f} m3/s")
# implied grade from cost
for c in (526,683):
  for ratio in (0.7,1.0):
    for gcost in (1050,2000):
      pass
print("implied g/m3 of section at cost parity: ", [round(c/(r*g),2) for c in (526,683) for r in (0.7,1.0) for g in (1050,2000)])
