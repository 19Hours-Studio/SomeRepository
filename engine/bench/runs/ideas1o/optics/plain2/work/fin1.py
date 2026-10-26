import json, math, sys, numpy as np
sys.path.insert(0,'.')
import sim
s=math.sin(math.radians(3))
def build(c, a, N, w, sub=4):
    F=(0.0,a); mirrors=[]
    for side in (1,-1):
        xs=np.linspace(0,0.5,N+1) if c>=0.5 else None
        for i in range(N):
            x0,x1=xs[i],xs[i+1]; xm=0.5*(x0+x1)
            phi=math.acos(min(1,math.sqrt(xm/c)))
            up = (i%2==0)
            t_c = c*math.cos(phi)*math.sin(phi)*(1 if up else -1)
            L=math.hypot(xm,t_c); K=L-t_c
            pts=[]
            for x in np.linspace(x0,x1,sub+1):
                t=(x*x-K*K)/(2*K); pts.append([side*x, a+t])
            mirrors.append(pts)
    rec=[[0,a-w/2],[0,a+w/2]]
    return {"receiver":rec,"mirrors":mirrors}
if __name__=="__main__":
    c=float(sys.argv[1]); N=int(sys.argv[2]); w=float(sys.argv[3])
    d=build(c,0.5,N,w)
    json.dump(d,open('work/fin1.json','w'))
    eta=sim.trace(np.array(d['receiver'],float),d['mirrors'])
    print(eta, eta/w*s)
