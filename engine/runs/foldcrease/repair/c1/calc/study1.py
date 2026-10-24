import numpy as np
from crease import teardrop_profile, metrics, residual_kr, D_lam
def smooth(x,k,width_mm):
    if width_mm<=0: return k
    h=(x[1]-x[0])*1e3; n=int(width_mm/h); 
    ker=np.hanning(2*n+1); ker/=ker.sum(); return np.convolve(k,ker,mode='same')
def solve_lin(x,kr,T,D=D_lam):
    n=len(x); h=x[1]-x[0]
    D2=(np.eye(n,k=-1)-2*np.eye(n)+np.eye(n,k=1))[1:-1]/h**2
    D1=(np.eye(n,k=1)-np.eye(n))[:-1]/h
    A=np.vstack([np.sqrt(D*h)*D2, np.sqrt(T*h)*D1]); b=np.concatenate([np.sqrt(D*h)*kr[1:-1],np.zeros(n-1)])
    free=np.arange(2,n-2); w=np.zeros(n); w[free]=np.linalg.lstsq(A[:,free],b,rcond=None)[0]
    sl=np.gradient(w,x); return w,sl,np.gradient(sl,x)
def run(R,c,T,sm=0.0,n=900,neck_ratio=3.0):
    x,k=teardrop_profile(R,n=n,neck_ratio=neck_ratio); k=smooth(x,k,sm)
    w,s,cu=solve_lin(x,c*k,T); return metrics(x,w,s,cu)
if __name__=="__main__":
    # calibration: today's teardrop, R=2 mm, sharp transitions, untensioned crease = BASE um
    for eps_c in [0.003,0.005]:
      for base in [60,150]:
        d_unit=run(2.0,1.0,0)['depth_um']; c2=base/d_unit
        phi=c2/residual_kr(2.0,1.0,eps_c); c3=residual_kr(3.0,phi,eps_c)
        print(f"\neps_c={eps_c} base={base}um phi={phi:.3f} c2={c2:.4f} c3={c3:.4f}")
        for sm in [0,2.0,4.0]:
          for T in [0,1000,3150]:
            m=run(3.0,c3,T,sm); print(f"  smooth={sm}mm T={T:5d}: depth {m['depth_um']:7.2f} um slope {m['slope_mrad']:6.2f} mrad curv {m['curv_inv_m']:.2f}/m")
    print("\nsqrt(D/T) mm:",[round(np.sqrt(D_lam/T)*1e3,2) for T in [300,1000,3150]])
