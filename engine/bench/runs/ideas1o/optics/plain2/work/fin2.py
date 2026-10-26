import sys, math, json, numpy as np
sys.path.insert(0,'..')
import sim
s=math.sin(math.radians(3))
def build(c,a,N,w,xmin,sub=3):
    mirrors=[]
    xs=np.linspace(xmin,0.5,N+1)
    for side in (1,-1):
        for i in range(N):
            x0,x1=xs[i],xs[i+1]; xm=0.5*(x0+x1)
            phi=math.acos(min(1,math.sqrt(xm/c)))
            up=(i%2==0)
            t_c=c*math.cos(phi)*math.sin(phi)*(1 if up else -1)
            L=math.hypot(xm,t_c); K=L-t_c
            mirrors.append([[side*x,a+(x*x-K*K)/(2*K)] for x in np.linspace(x0,x1,sub+1)])
    return {"receiver":[[0,a-w/2],[0,a+w/2]],"mirrors":mirrors}
def score(d):
    w=np.linalg.norm(np.subtract(d['receiver'][1],d['receiver'][0]))
    eta=sim.trace(np.array(d['receiver'],float),d['mirrors']); return eta, eta/w*s
if __name__=="__main__":
  for xmin in [0.01,0.03,0.06]:
    for N in [200,600]:
      print(xmin,N,*score(build(0.5,0.5,N,0.0523,xmin)))
