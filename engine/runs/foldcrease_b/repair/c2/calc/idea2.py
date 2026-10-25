# Idea 2: open-state tension. Beam-column with eigencurvature: D(w''-k0)'' - T w'' = 0
# far-field flat -> Fourier: w_hat = w0_hat * (k l)^2/(1+(k l)^2), l = sqrt(D/T)
import numpy as np
x=np.linspace(-0.1,0.1,2**16); dx=x[1]-x[0]; k=2*np.pi*np.fft.fftfreq(x.size,dx)
def dent(H,fwhm):  s=fwhm/2.355; return -H*np.exp(-x**2/(2*s**2))
def tens(w0,D,T):
    l2=D/T; W=np.fft.fft(w0)*(k**2*l2)/(1+k**2*l2); return np.real(np.fft.ifft(W))
def metr(w): return (w.max()-w.min()), np.degrees(np.abs(np.gradient(w,dx)).max())
cases={"Duo new (HTX 48um)":48e-6,"Oppo N6 claim 50um":50e-6,"Duo 3000 folds 167um":167e-6,"low-creep stack 10um":10e-6}
Ds={"decoupled ~3e-4":3e-4,"bonded 25C ~2e-3":2e-3,"bonded -20C x40 on decoupled":1.2e-2}
fwhm=8e-3   # crease visible width assumption (8 mm FWHM) -> check vs Duo slope 1.24deg
H,sl=metr(dent(167e-6,fwhm)); print(f"check: 167um dent FWHM 8mm -> max slope {sl:.2f} deg (HTX 1.24deg) ok-ish")
for fw in [8e-3,15e-3]:
  print(f"\n--- crease FWHM {fw*1e3:.0f} mm; tension T needed for PV<=1um AND slope<=0.02deg")
  for cn,H0 in cases.items():
    for dn,D in Ds.items():
        w0=dent(H0,fw); Tneed=None
        for T in np.logspace(1,6,300):
            pv,s=metr(tens(w0,D,T))
            if pv<=1e-6 and s<=0.02: Tneed=T;break
        if Tneed: print(f"{cn:24s} D={dn:28s} T={Tneed:9.0f} N/m  -> 50um UTG stress {Tneed/50e-6/1e6:6.1f} MPa, hinge force {Tneed*0.15:6.0f} N")
        else: print(f"{cn:24s} D={dn:28s} T>1e6 N/m (impossible)")
# glass edge clamp, frame moment, thermal
T=2000; print(f"\nT={T}N/m: edge clamp epoxy shear over 2mm bond = {T/2e-3/1e6:.1f} MPa; glass strain {T/(72e9*50e-6)*100:.3f}% -> stretch over 140mm {T/(72e9*50e-6)*0.14*1e6:.0f} um")
for fr,cte in [("Al 23ppm",23e-6),("Ti 8.6ppm",8.6e-6)]:
    dth=(cte-8.5e-6)*40*0.14; print(f"{fr}: thermal mismatch over 140mm, dT=40K = {dth*1e6:.1f} um -> dT tension change with series spring 1mm travel = {dth/1e-3*100:.0f}% ")
F=T*0.15
for e in [2e-3,0.3e-3]:
    M=F*e; EI=110e9*0.15*(4e-3)**3/12; kap=M/EI; print(f"reaction offset {e*1e3:.1f}mm: wing moment {M:.2f} N m -> bow over 70mm {kap*0.07**2/2*1e6:.0f} um")
