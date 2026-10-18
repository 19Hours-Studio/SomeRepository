import math, numpy as np
def freeze_cyl(R=1.1,Tg=-3.0,wv=0.35,Tin=1.0,years=6):
    dr=0.05; rmax=15.0
    n=int(rmax/dr); r=(np.arange(n)+0.5)*dr
    k=2.0; Cv=2.4e6
    L=np.where(r<R, wv*334e6,0.0)
    H=np.where(r<R,L+Cv*Tin,Cv*Tg)
    def temp(H): return np.where(H<0,H/Cv,np.where(H>L,(H-L)/Cv,0.0))
    dt=0.2*dr*dr/(k/Cv); t=0
    rf=np.r_[0,(r[:-1]+r[1:])/2, rmax]
    while t<years*3.156e7:
        T=temp(H); flux=np.zeros(n+1)
        flux[1:-1]=-k*(T[1:]-T[:-1])/dr; flux[-1]=-k*(Tg-T[-1])/(dr/2)
        H=H-(rf[1:]*flux[1:]-rf[:-1]*flux[:-1])/(r*dr)*dt; t+=dt
        if np.all(H[r<R]<=0): return round(t/86400)
    return None
for R in (0.8,1.1):
  for Tg in (-3.0,-5.0,-8.0):
    print("isolated hole R",R,"ground",Tg,"days:",freeze_cyl(R=R,Tg=Tg))
# panel slab at -8
k=2.0; C=2.4e6; a=k/C
for Tg in (-5,-8):
    Q=1.6*0.35*334e6
    t=(Q/(4*k*abs(Tg)))**2*math.pi*a
    print("panel slab ground",Tg,"years",round(t/3.156e7,2))
