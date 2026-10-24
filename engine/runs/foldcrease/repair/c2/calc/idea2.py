# Idea 2: drumhead tension hinge. Set = intrinsic (stress-free) dip w0(x); tension T on plate D:
# D(w-w0)'''' = T w''  ->  w_hat = w0_hat * k^2/(k^2+T/D)
import numpy as np
from scipy.optimize import brentq
pi=np.pi
N=2**16; L=0.3; x=(np.arange(N)-N/2)*L/N; k=2*pi*np.fft.fftfreq(N,L/N)
def resid(T,D,depth,fwhm):
    s=fwhm/2.355; w0=-depth*np.exp(-x**2/(2*s**2))
    w=np.real(np.fft.ifft(np.fft.fft(w0)*k**2/(k**2+T/D+1e-30)))
    w-=w[0]
    return (w.max()-w.min()), np.abs(np.gradient(w,x)).max()
def T_need(D,depth,fwhm,dmax=1e-6,smax=0.5e-3):
    f=lambda T: max(resid(T,D,depth,fwhm)[0]/dmax, resid(T,D,depth,fwhm)[1]/smax)-1
    if f(1e-3)<0: return 0.0
    return brentq(f,1e-3,1e7)
print("R0 reproduce kill: 20um set, 3mm wide, D=1.6e-4, T=600 N/m")
for fw in [3e-3]:
    d,s=resid(600,1.6e-4,20e-6,fw); print(f"  residual depth {d*1e6:.1f} um, slope {s*1e3:.2f} mrad; T needed={T_need(1.6e-4,20e-6,fw):.0f} N/m")
print("\nR1 shift set to long wavelength (large bend radius => wide set). depth0 = f*pi^2*R/32")
for R,f in [(1.5e-3,0.08),(3e-3,0.04),(5e-3,0.02),(5e-3,0.04),(8e-3,0.02)]:
    a=pi*R; depth=f*pi**2*R/32; fw=0.6*a
    for D in [1.7e-4,1e-3]:
        T=T_need(D,depth,fw)
        print(f"  R={R*1e3:.1f}mm f={f:.2f}: set {depth*1e6:5.1f} um x {fw*1e3:4.1f} mm FWHM, D={D:.0e}: T_need={T:7.0f} N/m -> {T*0.15:6.0f} N on 150 mm fold line; UTG strain {T/(72e9*30e-6)*100:.3f}%")
