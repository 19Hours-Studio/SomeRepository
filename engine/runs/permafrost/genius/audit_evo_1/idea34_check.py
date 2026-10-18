import math
print("=== IDEA 3 ===")
L,B,T=130,14,3
for cb in (0.85,0.9,0.95):
  disp=L*B*T*cb*1.0
  print(f"Cb {cb}: displacement {disp:.0f} t; lightship implied for 2.9kt payload {disp-2900:.0f} t")
# payload at shallower drafts if lightship ~ 2000 t
for draft in (2.9,2.6,2.2,1.8):
  disp=L*B*draft*0.9
  print(f"draft {draft} m: displacement {disp:.0f} t -> payload with 2.0 kt lightship {disp-2000:.0f} t")
# lock clearance
print("lock clearance per side (14.3 m):", (14.3-14)/2, "m; (14.5):",(14.5-14)/2, "m; length slack", 135-130, "m")
# moat area and heat flux
moat=(L+4)*(B+4)-L*B
print("moat area per hull", moat, "m2")
for U in (2,5,10):
  for Ta in (-30,-45,-55):
    rho=1.45; cp=1005; Ch=1.5e-3
    Hs=rho*cp*Ch*U*(0-Ta)
    qs=3.8e-3; qa=0.0005 if Ta>-40 else 0.0001
    He=rho*2.5e6*Ch*U*(qs-qa)
    sigma=5.67e-8
    LW=sigma*273.15**4-0.75*sigma*(273.15+Ta)**4
    tot=Hs+He+LW
    print(f"U={U} Ta={Ta}: flux {tot:.0f} W/m2 -> {tot*moat/1e6:.2f} MW per hull")
# ice growth after heat outage (Stefan, bare ice)
for Ta in (-40,-50):
  for hrs in (12,24,72):
    h=math.sqrt(2*2.2*(-Ta)*hrs*3600/(917*334e3))
    print(f"outage Ta={Ta} {hrs} h: moat ice {h:.2f} m")
# capex savings sensitivity: saving = F - X, X inferred from claim
for F_claim,S_claim in ((0.20,0.15),(0.25,0.19)):
  X=F_claim-S_claim
  for F_real in (0.10,0.15,0.6*F_claim):
    print(f"claim F={F_claim:.2f} S={S_claim:.2f} -> X={X:.2f}; if foundations saved only {F_real:.3f}: capex saving {F_real-X:.3f}")
print("=== IDEA 4 ===")
vol=math.pi*0.9**2*100
for rho in (1.25,1.30,1.35):
  print(f"hole volume {vol:.1f} m3, mass at {rho}: {vol*rho:.0f} t")
m=331
print("holes for 20 kt:",20000/m)
for r in (33,40,53):
  for av in (1.0,0.8):
    print(f"rate {r} t/h avail {av}: 20 kt in {20000/r/24/av:.1f} d; 60 kt in {60000/r/24/av:.1f} d")
print("bluff per 20 kt:", 60.4*(1.8+0.6), "m; per 60 kt:", 3*60.4*2.4)
# web SF Mark-Bieniawski strip pillar
s1=6.2
for H in (15,30,50):
  for w in (0.6,0.9):
    h=1.8
    Sp=s1*(0.64+0.54*w/h)
    sig=0.025*H*(w+1.8)/w
    print(f"cover {H} m web {w}: strength {Sp:.2f} MPa, load {sig:.2f} MPa, SF {Sp/sig:.2f}; extraction {1.8/(1.8+w):.0%}")
# adfreeze anchor sensitivity (SP 25.13330 clay Raf table approx): -0.5:60, -1:100, -2:150, -3:200 kPa
cap_claim=(283,424)
for T,Raf in ((-3,200),(-2,150),(-1,100),(-0.5,60)):
  scale=Raf/200
  c=[x*scale for x in cap_claim]
  print(f"anchor at {T} C (Raf {Raf} kPa, scaled from -3C): each {c[0]:.0f}-{c[1]:.0f} kN; two = {2*c[0]:.0f}-{2*c[1]:.0f} kN vs 300 kN thrust -> SF {2*c[0]/300:.2f}-{2*c[1]/300:.2f}")
# cost ratios
for alt in (3700,5300,7400,10300):
  print(f"alt {alt}: ratio {alt/3200:.2f}; breakeven overrun {(alt/3200-1):.0%}")
