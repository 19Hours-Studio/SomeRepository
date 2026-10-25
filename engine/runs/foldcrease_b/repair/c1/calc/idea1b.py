# Round 2: smooth Gaussian creases (no artificial corners); find T needed per metric, and regime map.
import numpy as np
N=2**16; L=0.15; x=np.linspace(-L/2,L/2,N,endpoint=False); dx=x[1]-x[0]
k=2*np.pi*np.fft.fftfreq(N,dx); k2=k**2; k2[0]=1e30
def flat(z,T,D): return np.real(np.fft.ifft(np.fft.fft(z)/(1+T/(D*k2))))
def met(z):
    s=np.gradient(z,dx); c=np.gradient(s,dx); return z.max()-z.min(),abs(s).max(),abs(c).max()
tgt=(2e-6,0.3e-3,0.5)
sig_htx=167e-6*np.exp(-0.5)/np.radians(1.24); print(f"HTX-implied Gaussian sigma {sig_htx*1e3:.2f} mm")
def Treq(h,sig,D):
    z=h*np.exp(-x**2/(2*sig**2))
    for T in np.logspace(0,5,400):
        d,s,c=met(flat(z,T,D))
        if d<=tgt[0] and s<=tgt[1] and c<=tgt[2]: return T
    return np.inf
Tmax={"OCA 50% sustained, lam 6.5mm":290,"OCA 50% sustained, graded bond lam 15mm":675}
print("T_required [N/m] for depth<=2um, slope<=0.3mrad, curvature<=0.5/m")
for D in [3.9e-4,1e-3]:
    for h in [5e-6,10e-6,20e-6,48e-6,167e-6]:
        row=[]
        for sig in [1.5e-3,3e-3,4.7e-3,8e-3]:
            row.append(Treq(h,sig,D))
        print(f"D={D:.1e} h={h*1e6:5.0f}um  sigma 1.5/3/4.7/8mm: "+"  ".join(f"{t:8.0f}" for t in row))
