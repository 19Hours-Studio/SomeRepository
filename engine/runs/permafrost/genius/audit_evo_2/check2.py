import math
print("=== IDEA 2 ===")
def seg_below(r,c):  # area of circle below a chord at distance c below centre
    return r*r*math.acos(c/r)-c*math.sqrt(r*r-c*c)
T=1.8
best=[]
for r in [x/100 for x in range(60,131,5)]:
  for c in (0.3,0.4,0.5):
    pen=r-c
    if not (0.4-1e-9<=pen<=0.6+1e-9): continue
    chord=2*math.sqrt(r*r-c*c)
    for sweep in (0.65,0.70,0.74):
      s=chord/sweep
      above=math.pi*r*r-seg_below(r,c)
      top=c+r
      ext=above/(s*T)   # fraction of seam cross-section removed (if top<=T)
      fac=s/(s-2*r) if s>2*r else float('inf')
      dil=seg_below(r,c)/(math.pi*r*r)
      best.append((r,c,sweep,round(s,2),round(ext,2),round(fac,2),round(top,2),round(dil,2)))
print("r c sweep spacing extraction stressfactor holetop bedrock_frac_of_feed")
for b in best: print(b)
g=20e3
for H in (10,20,30,40):
    print("cover",H,"m: gamma*H MPa",g*H/1e6," pillar stress at factor 4.5:",round(g*H*4.5/1e6,2))
# implied factor from text: 0.9-1.8 MPa at 10-20 m
print("implied factor",0.9e6/(g*10),1.8e6/(g*20))
# backfill freezing: 1-D slab, both sides into ground at Tg
k=2.0; C=2.4e6; a=k/C
for Tg in (-1,-2,-3,-5):
  for wv in (0.3,0.4):
    thick=1.8*0.61+0.5  # rough backfilled thickness (m) per unit seam area
    Q=thick*wv*334e6*1.0   # J/m2 latent of backfill water  (wv vol fraction water)
    # heat absorbed by two semi-infinite sides with surface held at 0C: q_total(t)=2*2*k*dT*sqrt(t/(pi a))
    t=(Q/(4*k*abs(Tg)))**2*math.pi*a
    print("ground",Tg,"C water frac",wv,"latent MJ/m2",round(Q/1e6),"freeze time yr",round(t/3.156e7,1))
# cold content of pillars only
for Tg in (-2,-3,-5):
    cold=0.39*2.3*C*abs(Tg)
    lat=0.61*2.3*0.35*334e6
    print("pillar cold MJ/m2",round(cold/1e6,1),"backfill latent MJ/m2",round(lat/1e6),"fraction",round(cold/lat,3))
# isolated single hole r=1.1 freeze time numeric (cylindrical, enthalpy method)
def freeze_cyl(R=1.1,Tg=-3.0,wv=0.35,years=5):
    import numpy as np
    dr=0.05; rmax=12.0
    n=int(rmax/dr)
    r=(np.arange(n)+0.5)*dr
    k=np.full(n,2.0); Cv=np.full(n,2.4e6)
    L=np.where(r<R, wv*334e6,0.0)
    # enthalpy H: T<0: Cv*T ; 0..L: phase ; T>0
    T0=np.where(r<R,1.0,Tg)
    H=np.where(r<R,L+Cv*T0,Cv*T0)
    def temp(H):
        return np.where(H<0,H/Cv,np.where(H>L,(H-L)/Cv,0.0))
    dt=0.2*dr*dr/(2.0/2.4e6)
    t=0; out=[]
    rf=np.r_[0,(r[:-1]+r[1:])/2, rmax]
    while t<years*3.156e7:
        Tt=temp(H)
        flux=np.zeros(n+1)
        flux[1:-1]=-k[0]*(Tt[1:]-Tt[:-1])/dr
        flux[-1]=-k[0]*(Tg-Tt[-1])/(dr/2)
        dH=-(rf[1:]*flux[1:]-rf[:-1]*flux[:-1])/(r*dr)*dt
        H=H+dH; t+=dt
        inner=H[r<R]
        if np.all(inner<=0):
            return t/86400
    return None
for Tg in (-1.5,-3.0,-5.0):
    print("isolated hole R=1.1, ground",Tg,"days to freeze:",freeze_cyl(Tg=Tg))
# cost check
for cm in (45,50,55):
    for rec_pergm3 in (1.25,1.39,1.5):
        pass
print("cost/m3 / 36 $/g -> g recovered per m3 feed:",[round(c/36,2) for c in (45,50,55)])
print("3 g/m3 * dilution 1.8/2.3 * sweep 0.7 * plant rec 0.85 =",round(3*1.8/2.3*0.7*0.85,2))
print("36/29 =",round(36/29,2)," 36/23 =",round(36/23,2))
print("open-water season rate: 70-100k m3/130 d =",round(70e3/130),"-",round(100e3/130),"m3/d ; winter 215k/280 =",round(215e3/280))
