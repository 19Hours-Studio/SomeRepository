import sys, math, json, numpy as np
from fast import score, trace, s
R=math.radians
def parab(F, ang_e, K, psis):
    # parabola focus F, source direction angle ang_e: r = K/(1-cos(psi-ang_e))
    return [[F[0]+K/(1-math.cos(p-ang_e))*math.cos(p), F[1]+K/(1-math.cos(p-ang_e))*math.sin(p)] for p in psis]
def facet(F, c, ph0, ph1, ang_e, kap, sub):
    pm=0.5*(ph0+ph1); L=kap*c*math.cos(pm)
    K=L*(1-math.cos(pm-ang_e))
    return parab(F, ang_e, K, np.linspace(ph0,ph1,sub+1))
def fold_for(P0, P1, e, x_prev):
    # flat fold converting vertical-down light into direction d=-e, intercepting strip of rays P+mu*e
    d=-e; n=d+np.array([0,1.0]); n/=np.linalg.norm(n); t=np.array([n[1],-n[0]])
    # fold line: points X with (X-Q).n=0, Q=Pm+lam*e. intersection of P+mu e: mu=((Q-P).n)/(e.n)
    def ends(lam):
        Pm=(P0+P1)/2; Q=Pm+lam*e
        R0=P0+((Q-P0)@n)/(e@n)*e; R1=P1+((Q-P1)@n)/(e@n)*e
        return R0,R1
    a0,a1=ends(0.0); b0,b1=ends(1.0)
    lo0=min(a0[0],a1[0]); dlo=min(b0[0],b1[0])-lo0
    lam=max(0.02, (x_prev-lo0)/dlo) if dlo>1e-9 else 0.02
    R0,R1=ends(lam)
    return [list(R0),list(R1)], max(R0[0],R1[0]), min(R0[1],R1[1])
def build(c=0.2, a=0.6, nU=30, nS=40, kap=0.97, wfac=1.0, phmax=85, phmin=-27, sub=4, gap=0.0):
    F=(0.0,a); M=[]
    # upper arc direct: phi in [30,phmax]
    ph=np.linspace(R(30),R(phmax),nU+1)
    for i in range(nU): M.append(facet(F,c,ph[i],ph[i+1],R(90),kap,sub))
    # side fan phi in [phmin,30], from 30 downward
    ph=np.linspace(R(30),R(phmin),nS+1)
    xprev=c*0.75
    for i in range(nS):
        p0,p1=ph[i+1],ph[i]; pm=0.5*(p0+p1); ae=3*pm
        f=facet(F,c,p0,p1,ae,kap,sub)
        e=np.array([math.cos(ae),math.sin(ae)])
        fo,xr,ylow=fold_for(np.array(f[0]),np.array(f[-1]),e,xprev+gap)
        if ylow<0 or xr>0.5: continue
        xprev=xr
        M.append(f); M.append(fo)
    full=M+[[[-p[0],p[1]] for p in m] for m in M]
    w=2*s*c*wfac
    return {"receiver":[[0,a-w/2],[0,a+w/2]],"mirrors":full}
if __name__=="__main__":
    d=build()
    json.dump(d,open('fan.json','w'))
    print(*score(d))
