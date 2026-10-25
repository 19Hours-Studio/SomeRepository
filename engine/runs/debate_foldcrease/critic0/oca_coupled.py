"""Critic check: two-layer beam (UTG on top / panel+Ti below) coupled by an OCA shear layer.
The author's model sets OCA set to zero and assumes full decoupling. Here:
 folded state: slope theta(x) prescribed (0 -> pi/2 over half fold arc), solve OCA slip;
 the OCA keeps a fraction phi of its folded shear (unrecovered set);
 open state: free span |x|<a (theta free), theta=0 beyond (wings bonded to rigid halves);
 minimise E = int EAeff/2 du'^2 + D/2 theta'^2 + k/2 (du - s*theta - dset)^2.
Linear, small-slope in open state. Outputs residual depth, max slope, and folded axial stresses."""
import numpy as np, math
def solve(R=4e-3, Lfac=1.5, G=1e5, h=25e-6, phi=0.1, a_extra=3e-3, X=70e-3, n=1400,
          E1=72e9,t1=70e-6, E2=100e9,t2=40e-6, Ep=6e9,tp=25e-6):
    EA1=E1*t1; EA2=E2*t2+Ep*tp; EAeff=EA1*EA2/(EA1+EA2)
    zc=(E2*t2*t2/2+Ep*tp*(t2+tp/2))/EA2                     # NA of bottom composite
    D2=E2*t2**3/12+E2*t2*(t2/2-zc)**2+Ep*tp**3/12+Ep*tp*(t2+tp/2-zc)**2
    D=E1*t1**3/12+D2; s=t1/2+h+(t2+tp-zc); k=G/h
    x=np.linspace(0,X,n+1); dx=x[1]-x[0]; Lh=math.pi*R*Lfac/2
    thf=(math.pi/2)*np.minimum(x/Lh,1)
    # folded: EAeff du'' = k(du - s th), du(0)=0, du'(X)=0
    A=np.zeros((n+1,n+1)); b=np.zeros(n+1); A[0,0]=1
    for i in range(1,n):
        A[i,i-1]=A[i,i+1]=EAeff/dx**2; A[i,i]=-2*EAeff/dx**2-k; b[i]=-k*s*thf[i]
    A[n,n-1]=-1;A[n,n]=1
    du=np.linalg.solve(A,b); slip=du-s*thf; N1=EAeff*np.gradient(du,dx)
    # OCA shear strain and extra axial stresses in folded state
    gam=np.abs(slip).max()/h; sg1=np.abs(N1).max()/t1; sTi=np.abs(N1).max()/EA2*E2
    dset=phi*slip
    # open state: unknowns theta_i (i=1..m, x<a), du_i (i=1..n); quadratic -> least squares
    a=Lh+a_extra; m=int(a/dx)
    nv=m+n; rows=[]; rhs=[]
    def row(): return np.zeros(nv)
    # bending: sqrt(D) * (theta_{i+1}-theta_i)/dx over intervals, theta_0=0, theta_{m+1}=0
    for i in range(0,m+1):
        r=row()
        if i+1<=m: r[i]+=1/dx            # theta index i+1 -> var i
        if i>=1: r[i-1]-=1/dx
        rows.append(r*math.sqrt(D*dx)); rhs.append(0)
    for i in range(0,n):                 # axial: du_{i+1}-du_i
        r=row(); r[m+i]+=1/dx
        if i>=1: r[m+i-1]-=1/dx
        rows.append(r*math.sqrt(EAeff*dx)); rhs.append(0)
    for i in range(1,n+1):               # OCA shear at node i
        r=row(); r[m+i-1]=1
        if i<=m: r[i-1]=-s
        rows.append(r*math.sqrt(k*dx)); rhs.append(dset[i]*math.sqrt(k*dx))
    z=np.linalg.lstsq(np.array(rows),np.array(rhs),rcond=None)[0]
    th=np.concatenate([[0],z[:m],[0]])
    w=np.concatenate([[0],np.cumsum(th[1:]*dx)]); depth=abs(w[-1]-w[0])
    return dict(depth=depth,slope=np.abs(th).max(),gam=gam,sg1=sg1/1e6,sTi=sTi/1e6,s=s,D=D,
                lam=math.sqrt(D/(k*s*s)),lam_ax=math.sqrt(EAeff/k))
if __name__=="__main__":
    print("Proposed stack (70um UTG / 25um OCA / 25um panel + 40um Ti), R=4mm")
    for G in (1e4,3e4,1e5):
        for phi in (0.02,0.05,0.10):
            r=solve(G=G,phi=phi)
            print(f"G={G:7.0f}Pa phi_OCA={phi:.2f}: depth {r['depth']*1e6:6.2f} um  slope {r['slope']*1e3:5.2f} mrad"
                  f" | folded: OCA shear {r['gam']:.1f}, extra glass axial {r['sg1']:5.0f} MPa, extra Ti axial {r['sTi']:5.0f} MPa"
                  f" | s={r['s']*1e6:.0f}um lam_ax={r['lam_ax']*1e3:.0f}mm")
    print("\nsensitivity: free span margin a_extra and radius, G=1e5, phi=0.1")
    for ax in (1e-3,3e-3,8e-3):
        for R in (2e-3,4e-3):
            r=solve(G=1e5,phi=0.1,a_extra=ax,R=R)
            print(f"a_extra={ax*1e3:.0f}mm R={R*1e3:.0f}mm: depth {r['depth']*1e6:6.2f} um slope {r['slope']*1e3:5.2f} mrad")
    print("\nthinner OCA 10um, G=1e5, phi=0.1:",{k_:round(v*1e6,2) for k_,v in solve(h=10e-6,phi=0.1).items() if k_ in('depth',)},"um depth")
