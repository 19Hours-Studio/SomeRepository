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

print("\nR2 design point: tolerable set fraction f at design tension (linear model => scales with f)")
for R in [4e-3,5e-3]:
    for D in [2e-4,3e-4]:
        a=pi*R; fw=0.6*a
        for T in [700,1000]:
            # T_need scales ~linearly with depth for fixed width -> find f where T_need=T
            g=lambda f: T_need(D,f*pi**2*R/32,fw)-T
            fa=brentq(g,1e-4,0.5)
            print(f"  R={R*1e3:.0f}mm D={D:.0e} T={T}N/m: f_allowed={fa*100:.2f}%  (set depth {fa*pi**2*R/32*1e6:.0f} um)")
print("\nOCA shear in view area with iso-strain end clamp: flattening slip ~ (f/R)*d*a")
G=5e4; t=25e-6; d=50e-6
for R,f in [(5e-3,0.03)]:
    slip=(f/R)*d*pi*R; g=slip/t; print(f"  slip {slip*1e6:.1f} um, gamma {g:.2f}, tau {G*g/1e3:.1f} kPa (vs 10.5 kPa creep-test stress; kill had 25 kPa)")
print("\nHinge: thermal + spring + user work")
T=700; Lf=0.15; F=T*Lf; span=0.14
for frame,cte in [("Al",23e-6),("Ti",8.6e-6)]:
    dx=(cte-5e-6)*60*span
    for stroke in [0.3e-3,1e-3]:
        print(f"  {frame} frame: thermal mismatch {dx*1e6:.0f} um over 60 K; spring stroke {stroke*1e3:.1f} mm -> tension swing +-{dx/stroke*50:.0f}%  work/cycle {F*stroke:.3f} J")
print(f"  total force {F:.0f} N; stack elastic stroke {T/(72e9*30e-6+10e9*30e-6)*span*1e6:.0f} um")
